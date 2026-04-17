# KV Cache 详解

> **视频来源：** [李宏毅 - KV Cache 课程](https://youtu.be/fDQaadKysSA?si=p4HKJUZLUN3pfJpK)
> **提取时间：** 2026-04-01

---

## 1. 语言模型生成的两个阶段

语言模型的生成过程可以分为两个阶段：

### 1.1 Prefill（预填充）
- 输入一个**非常长的 Sequence**（人类输入的 Prompt）
- 一次性处理所有输入 token
- 为每个 token 计算 Q、K、V

### 1.2 Decode（解码）
- **逐个 token 输出**
- 每生成一个 token，就将其作为下一个输入
- 循环直到生成结束符

**示例流程：**
```
输入："李宏毅几班"
→ 输出 "大"
→ 输入 "李宏毅几班大"
→ 输出 "金"
→ 输入 "李宏毅几班大金"
→ 输出 "<结束符>"
```

---

## 2. KV Cache 核心概念

### 2.1 什么是 KV Cache？

在 Prefill 阶段：
- 每个 token 都会计算出对应的 **Q、K、V**
- 计算 Attention 时：
  - Q1 与 K1 算 Attention Weight，乘 V1 得 O1
  - Q2 与前两个 K 算 Attention，对 V1、V2 做 Weighted Sum 得 O2
  - Q3 与前三个 K 算 Attention，对 V1-V3 做 Weighted Sum 得 O3
- **Q1、Q2、Q3 计算 O1、O2、O3 可以并行运算**

**关键洞察：**
- 计算完成后，**Q 可以丢弃**
- 但 **K1-K3 和 V1-V3 需要保存下来**
- 把 V 和 K 存下来这件事，就叫做 **KV Cache**

### 2.2 为什么需要 KV Cache？

当模型开始生成（Decode 阶段）：
- 第 4 个 token 进来，得到 Q4、K4、V4
- 如果不缓存，需要把第 4 个 token 和前面所有 token 重新丢进模型重新计算 K、V
- **太花时间！**

**使用 KV Cache 后：**
- Q4 直接与之前存下来的 K1-K3 算 Attention
- 也与 K4 算 Attention
- 得到 Attention Weight 后与 V1-V4 做 Weighted Sum 得到 Output
- **节省了重新计算 V1-V3 和 K1-K3 的时间**

后续第 5 个 token 也一样：
- 只需要算自己的 Q5、V5、K5
- 前面 4 个 token 的 V 和 K 不需要重算

---

## 3. KV Cache 的内存压力

### 3.1 为什么能撑爆 GPU？

KV Cache 可以直接撑爆你以为非常大的 GPU 内存，原因有二：

1. **要存的 K 和 V 非常多**
   - 每产生/输入一个 token，就要存一组 K 和 V
   - 如果输入或输出的 Sequence 很长，就会撑爆仓库

2. **K 和 V 不止一组**
   - 通常有多组 QKV（Multi-Head Attention）
   - 每个 Query 都有自己对应的 Value 和 Key

### 3.2 实际计算：Gemma 2 (27B) 为例

模型参数：
- 46 个 Layer
- 30 个 Head（先假设是普通 Attention，无视 GQA）
- 每个 Head 的向量维度：128
- 数据格式：FP16（每个数字 2 bytes）
- 有 Value 有 Key，所以要 ×2

**计算：**
```
46 × 30 × 128 × 2 × 2 = 736 KB ≈ 0.72 MB/ token
```

**A100 (80GB) 的情况：**
- 最多只能存约 114k 个 token（约 10 万）
- 今天很多场景对 Context 的需求远超 10 万
- 输入/输出 Sequence 太长时会出现 **CUDA Out of Memory**

---

## 4. 优化 KV Cache 的方法

### 4.1 Multi-Query Attention (MQA)

**思想：**
- 仍然可以有多个 Query
- 但**所有 Query 共用同一组 Value 和 Key**

**原因：**
- Value 和 Key 是会被存下来的东西
- Query 不会被存下来
- 所以 Query 多组没关系，但 Value 和 Key 只有一组可以减少仓库占用

**问题：**
- Multi-Query Attention 的表现并不好

### 4.2 Grouped-Query Attention (GQA)

**思想（介于 MHA 和 MQA 之间）：**
- 仍然可以有多组 Value 和 Key
- 但**每一组 Value 和 Key 配给多个 Query**
- Query 的数目比 Key 和 Value 的数目多

**示例：**
- 同一组 V 和 K 配两个 Query
- 有 4 个 Query，但只有 2 组 V 和 K
- 相当于运作一个有 4 个 Query 的 Multi-Head Attention，但只有 2 组 V 和 K

**为什么要这样设计？**
- 如果不了解 KV Cache，可能会觉得让不同的 V 和 K 共享 Query 也是一种操作
- 但实际上之所以让不同 Query 共享同样的 V 和 K，就是为了 handle KV Cache 的问题
- **只有 V 和 K 会被存下来，Query 不需要被存**

**应用：**
- LLaMA、Gemma 等知名模型都有用到 GQA

### 4.3 Multi-Head Latent Attention (DeepSeek 使用)

**思想：**
- 把一大堆 Query 和 Key **压缩成一个向量**
- 存在仓库里时，**只存这个向量**，不存多组 V 和 K

**实现方式：**
- 在 x 到多组 V 和 K 中间放一个 **Bottleneck Layer**
- 输入 x，得到一个维度比较小的向量（压缩后的向量 C）
- 再把 C 乘上不同的 Transform，得到不同的 Query 和 Key

**神奇之处：**
- **不需要解压缩！**
- 可以直接在压缩的维度上做运算

**数学原理：**
```
原本：a = Q^T × K = Q^T × (Wk × C)
等价于：a = (Wk^T × Q)^T × C = Q'^T × C
```
- 把 Q 压缩成 Q'，直接与 C 做 Dot Product
- 结果与解压缩后再做是一样的（不是近似，是等价）

**Weighted Sum 也一样：**
- 不需要把 C 解压缩回 V 再做 Weighted Sum
- 可以直接在压缩的 C 上做 Weighted Sum
- 做完再解压缩一次即可

**优势：**
- 压缩过程只需要做一次
- 不需要对 Sequence 长度的 C 都去做解压缩
- 甚至得到的结果比原来的 Multi-Head Attention 还要稍微好一点点

### 4.4 Sliding Window Attention

**思想：**
- 每次做 Attention 时，**不要 Attend 整个 Sequence**
- 只 Attend 前面某一个 Window 的范围（如 4096）
- 确保 KV Cache 有固定上限

**问题：**
- Query 能 Attend 的范围变少了
- 模型可能无法考虑非常长的 Sequence

**缓解：**
- 内容通常是多层的
- 虽然最上面一层只看前面两个 Key
- 但这个位置的 Query 其实又多看了前面两个位置
- 如果 Transformer 层数够多，看的范围仍然可以非常大
- 看的范围取决于深度

**应用：**
- Mistral 7B 的某个版本用过

**变体：**
- 某些 Layer 用 Sliding Window，某些 Layer 做完整 Attention
- GPT OSS（OpenAI 近年释出的模型）用一层 Sliding Window、一层完整 Attention 的设置

### 4.5 Streaming LLM

**核心发现：**
- Sliding Window Attention 往往会让模型表现变差
- 尤其是在输入 sequence 非常长的时候
- **但如果 attention 的范围能包含整个 sequence 最开始的几个 token，就没事了！**

**实现：**
- 在 sliding window 基础上，**额外加上最前面的几个 token**
- 甚至**不需要额外的 training**
- 在 inference 时加上最前面的 token，表现就大增

**实验结果：**
- 横轴：输入 sequence 长度
- 纵轴：perplexity（越小越好）
- Dense Attention（完整 attention）：到某长度后表现突然变差
- Window Attention：超过 window 后表现瞬间变差
- **Streaming LLM：可以处理非常长的输入，表现稳定**

**为什么第一个 token 这么重要？**
- Attention weight 合起来必须是 1（强制归一化）
- 每个 Query 无论如何都需要 attend 一些东西
- 如果没什么好 attend 的，模型预设行为是 attend 在第一个 token
- 如果没给第一个 token，模型整个世界就崩坏了
- 给了第一个 token，模型就知道怎么做 attention 了

### 4.6 KV Cache Pruning

**思想：**
- 直接把没用的 KV 从数据库里丢掉

**发现（Scissorhands、H2O 等论文）：**
- 根本不需要存那么多 Key 和 Value
- 多数 Key 和 Value 后来都没被用上
- 只有少数 token 会被反复 attend

**可视化观察：**
- 在 178、228、278 等位置检查 attention 状况
- 发现多数 token（如某个区域的 token）从来没人 attend
- 存这些 token 的 K 和 V 只是在占用空间
- 少数 token 被反复 attend，这些应该被存下来

**方法：**
- 如果一组 K 和 V 一直没人 attend，就丢掉
- 类似 "数据库里没人拿的东西，过几天就被丢掉"

**效果：**
- 可以压缩 5 倍（只保留 20% 的 token 的 K 和 V）
- 在很多任务上表现仍然差不多
- 但在很难的任务上，随便丢掉 K 和 V 表现还是会变差

---

## 5. 跨对话 KV Cache（Cache Input）

### 5.1 跨对话共享

KV Cache 不仅可以是同一个对话里的，还可以**跨对话**：

**示例：**
- 对话 A："大家好我是大金" → 存下 K 和 V
- 对话 B："大家好我是小金"
- 前五個 token（"大家好我是"）一模一样
- 可以把对话 A 前五个 token 的 K 和 V 挪到对话 B 直接使用

**限制：**
- 只有**一样的前缀（prefix）**可以共用 K 和 V
- 虽然 "金" 这个字在两个对话都有，但不能把 A 的 "金" 的 KV Cache 挪到 B 用
- 因为每个 token 的 representation 取决于前面看过什么 token
- 一旦前面变了（大→小），K 和 V 就不一样了

### 5.2 商业应用：Cache Input 折扣

多数语言模型服务（ChatGPT、Gemini、Claude、DeepSeek）都有 **Cache Input** 折扣：

**GPT-4o 定价示例：**
- 正常输入（短 context）：$2.5 / million tokens
- 长 sequence：$5 / million tokens
- **Cache input：打 10% 折扣（只收 $0.25）**

**为什么可以这么慷慨？**
- 如果 input 有 cache 到，对模型/平台来说几乎不需要额外计算
- Key 和 Value 都是已经算好的
- 直接把已算好的 K 和 V 拿到新的 session 使用即可

**Cache 原理图示：**
- 原 sequence 存在 cache 里
- 新 sequence 和原 sequence 只有最后两个 token 不一样
- 前面可以 match 到一大堆东西，这些 token 的运算打 1 折
- 但如果只是在前面多一个不一样的 token，就破坏整个 cache 结果

### 5.3 如何最大化 Cache Hit？

**关键原则：**
- 越稳定不动的内容，放在越前面
- 越可能变动的内容，放在越后面

**AI Agent 场景：**
- 对 AI agent 说 "你好" 时，会在句子前面加上非常长的 system prompt
- System prompt 内容通常不变（agent 的名字、灵魂、存在目标）
- 很有可能用上 cache hit

**Claude 的 System Prompt 设计：**
- 最前面：有哪些工具可以用（几乎固定）
- 后面：日期（每次都会变）
- 日期一变，cache 就被破坏，所以日期应该放在后面

**Prompt 写法优化示例：**

❌ 不好的写法（cache hit 低）：
```
帮我订从台北到波士顿的班机
帮我订从旧金山到纽约的班机
```
- 只 hit 了 "帮我订从" 这几个字
- 地点一换，cache hit 就没用了

✅ 好的写法（cache hit 高）：
```
帮我订从 X 到 Y 的班机
X = 台北
Y = 波士顿

帮我订从 X 到 Y 的班机
X = 旧金山
Y = 纽约
```
- 句子前面都一样
- 变量放在 sequence 最后面
- 可能 hit 到比较长的 cache，省更多钱

**实际效果：**
- 论文实测：在 Gemini 2.5 Pro 和 GPT-4o 上，至少可以达到 **50% 甚至更多的金钱节省**

---

## 6. 各种方法总结对比

| 方法 | 核心思想 | 是否改变原有 Attention | 是否需要训练 | 额外代价 |
|------|---------|----------------------|------------|---------|
| **Flash Attention** | 少搬数据 | 否 | 否 | 一点点额外运算 + 烧脑 |
| **KV Cache** | 储存已算好的 K、V | 否 | 否 | 占用仓库（内存） |
| **Multi-Query Attention** | 所有 Query 共用同一组 K、V | 是 | 是 | 明显伤害模型能力 |
| **Grouped-Query Attention** | 同一组 K、V 配多个 Query | 是 | 是 | 轻微改变模型 |
| **Multi-Head Latent Attention** | 压缩 K、V，不解压缩直接计算 | 是 | 是 | 有时表现反而更好 |
| **Sliding Window Attention** | 只 Attend 固定范围 | 是 | 可选 | 看的范围变少 |
| **Streaming LLM** | Sliding Window + 保留最前面几个 token | 是 | 可选 | 几乎无代价 |
| **KV Cache Pruning** | 丢掉没用的 K、V | 是 | 否 | 可能伤害模型能力 |
| **Speculative Decoding** | 用小模型帮助大模型生成 | 否 | 否 | 额外的小模型算力 |

### 详细说明

**Flash Attention：**
- 精神：少搬数据
- 非常强大，算出来的结果就是原有的 attention
- 不需要重新训练模型
- 代价：一点点额外的运算（为了要减少搬运数据必须做修正）+ 烧脑

**KV Cache：**
- 储存已经算出来的 Key 和 Value
- 不会改变原来的 attention，不需要重新训练模型
- 虽然可以加快速度，但坏处是占用了仓库

**GQA/MQA：**
- 让同一组的 Key 和 Value 可以有多组不同的 Query
- 会改变原来的 attention（算出来的跟原来的不一样了）
- 需要对模型做定制化的训练
- 尤其是 MQA，让所有 Query 共用同一组 K、V，在文献上发现会明显伤害模型的能力

**Multi-Head Latent Attention：**
- 压缩 Key 和 Value
- 神奇的是不需要做多次的解压缩
- 会改变原来的 attention，需要训练模型
- 但文献上结果有时反而比原来的 attention 表现更好

**Sliding Window / Streaming LLM：**
- 改变了 attention 的范围
- 会改变原有的 attention
- 是否需要训练：每一篇文献不一样，可以训练也可以不训练

**KV Cache Pruning：**
- 把一些没用到的 Key 和 Value 丢掉
- 会改变原有的 attention
- 不需要重新训练模型
- 如果做得不好会伤害模型能力

**Speculative Decoding：**
- 用一个小模型来帮助大模型的