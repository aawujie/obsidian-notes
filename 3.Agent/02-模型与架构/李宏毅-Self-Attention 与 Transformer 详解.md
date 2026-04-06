---
share_link: https://share.note.sx/umbvnzgp#3PMOHZroTJa6WxF8s2+wzslWctYCJJAuJBS+53JitvQ
share_updated: 2026-03-22T10:50:00+08:00
---
# 李宏毅：Self-Attention 与 Transformer 详解

> 视频笔记整理（完整版）| 深度学习架构核心

---

# Part 1: Self-Attention 基础

---

## 一、为什么需要 Self-Attention？

### 传统网络的局限

**现有假设**：输入是一个向量
- Regression：输出一个数值
- Classification：输出一个类别

**新问题**：输入是一排向量（Sequence），且长度可变

---

## 二、哪些场景输入是向量序列？

| 领域 | 输入 | 向量化方式 |
|------|------|------------|
| **文字处理** | 句子 | One-hot / Word Embedding |
| **语音处理** | 声音信号 | 每 25ms 一帧，步长 10ms |
| **图网络** | Social Network | 每个节点 = 一个向量 |
| **分子结构** | 分子图 | 每个原子 = One-hot 向量 |

---

## 三、Self-Attention 运算流程

### 步骤详解

```
Step 1: q = a × W^Q, k = a × W^K, v = a × W^V
Step 2: α = q · k  (Attention Score)
Step 3: α' = softmax(α)
Step 4: b = Σ(α'ᵢ · vᵢ)
```

**W^Q、W^K、W^V 是唯一需要学习的参数！**

---

## 四、Multi-Head Self-Attention

> "相关性"有多种不同的形式，需要多个 Q 负责不同种类的相关性。

```
aᵢ → qᵢ¹, qᵢ² → Head 1, Head 2 → concat → 输出
```

---

## 五、Positional Encoding

> Self-Attention 没有位置信息，需要额外添加位置向量。

```
aⁱ = aⁱ + eⁱ  (eⁱ 是位置向量)
```

---

# Part 2: Sequence to Sequence 模型

---

## 六、Seq2Seq 模型定义

```
输入：一个序列（长度 N）
输出：一个序列（长度 M）
M 由机器自己决定！
```

### 架构

```
┌──────────┐     ┌──────────┐
│ Encoder  │ ──► │ Decoder  │
└──────────┘     └──────────┘
```

---

## 七、Seq2Seq 的应用场景

| 任务 | 输入 | 输出 |
|------|------|------|
| 语音辨识 | 声音讯号 | 文字 |
| 语音翻译 | 声音讯号（A 语言） | 文字（B 语言） |
| 机器翻译 | 源语言句子 | 目标语言句子 |
| 聊天机器人 | 用户输入 | 回复 |
| 摘要生成 | 长文章 | 摘要 |

### 万物皆可 QA

> 很多 NLP 任务都可以看作 Question Answering 问题。

---

## 八、Seq2Seq 的局限性

> Seq2Seq 像瑞士刀，什么都能做，但不一定是最好的。

- 定制模型往往效果更好
- 例：语音辨识用 RNN Transducer 更优

---

# Part 3: Transformer Encoder

---

## 九、Encoder 的职责

```
输入：一排向量（序列）
输出：一排向量（同样长度）
```

---

## 十、Encoder Block 结构

```
输入
  │
  ▼
┌─────────────────┐
│ Positional      │
│ Encoding        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Multi-Head      │
│ Attention       │
└────────┬────────┘
         │
    ┌────┴────┐
    │   Add   │ ← Residual
    └────┬────┘
         │
         ▼
┌─────────────────┐
│  Layer Norm     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Feed Forward   │
└────────┬────────┘
         │
    ┌────┴────┐
    │   Add   │ ← Residual
    └────┬────┘
         │
         ▼
┌─────────────────┐
│  Layer Norm     │
└────────┬────────┘
         │
         ▼
输出
```

**重复 N 次**（原论文 N=6）

---

## 十一、Residual Connection

```
输出 = 输入 + 变换 (输入)
y = x + F(x)
```

**作用**：缓解梯度消失，深层网络更容易训练

---

## 十二、Layer Normalization

### Layer Norm vs Batch Norm

| | Batch Norm | Layer Norm |
|---|-----------|------------|
| 依赖 batch | 是 | 否 |
| 序列长度变化 | 难处理 | 无影响 |
| Transformer | ❌ | ✅ |

```
Layer Norm: 对同一个 sample，跨 dimension 计算 mean/std
```

---

# Part 4: Transformer Decoder

---

## 十三、Decoder 的两种类型

| 类型 | 缩写 | 生成方式 |
|------|------|----------|
| **自回归 Decoder** | AT | 逐词生成 |
| **非自回归 Decoder** | NAT | 一次性生成 |

---

## 十四、自回归 Decoder（AT）运作流程

### 核心机制

```
Decoder 把自己的输出当作下一刻的输入！
```

### 详细步骤

```
Step 1: 输入 BOS（Begin of Sentence）起始符号
        ↓
Step 2: Decoder 输出概率分布 → 取最高概率词作为输出
        ↓
Step 3: 把输出词作为新输入
        ↓
Step 4: 重复 Step 2-3，直到生成 END 符号
```

### 关键符号

| 符号 | 全称 | 作用 |
|------|------|------|
| **BOS** | Begin of Sentence | 起始信号，告诉 Decoder 开始生成 |
| **END** | End of Sentence | 终止信号，告诉 Decoder 停止生成 |

> BOS 和 END 可以共用一个符号，使用场景不冲突。

### 核心问题：错误传播

```
Decoder 用自身输出作为输入
→ 一旦某步生成错误
→ 后续都基于错误信息生成
→ 一步错，步步错！
```

这就是 **Error Propagation（错误传播）** 问题。

---

## 十五、Masked Self-Attention

### 为什么需要 Mask？

```
Encoder：一次性读取完整输入序列
Decoder：逐词生成，生成第 N 个词时
        只能看到左侧已生成的词
        看不到右侧未生成的内容
```

### Mask 的作用

```
原始 Attention Matrix:
        位置 1  位置 2  位置 3  位置 4
位置 1    ✓     ✓      ✓      ✓
位置 2    ✓     ✓      ✓      ✓
位置 3    ✓     ✓      ✓      ✓
位置 4    ✓     ✓      ✓      ✓

Masked Attention Matrix:
        位置 1  位置 2  位置 3  位置 4
位置 1    ✓     ✗      ✗      ✗
位置 2    ✓     ✓      ✗      ✗
位置 3    ✓     ✓      ✓      ✗
位置 4    ✓     ✓      ✓      ✓

✓ = 可见    ✗ = 被 Mask 屏蔽
```

### 实现方式

```
在 Softmax 之前，将右侧位置的 Attention Score 设为 -∞
Softmax(-∞) = 0，相当于忽略这些位置
```

---

## 十六、非自回归 Decoder（NAT）

### 核心逻辑

```
AT: 逐词生成，串行
NAT: 一次性输入多个 BOS，并行生成完整序列
```

### 长度如何确定？

| 方法 | 说明 |
|------|------|
| **方法 1** | 额外训练分类器，预测输出长度 |
| **方法 2** | 设最大长度，输入固定数量 BOS，忽略 END 后内容 |

### NAT 优缺点

| | 优势 | 劣势 |
|---|------|------|
| **速度** | ✅ 推理极快，并行生成 | - |
| **控制** | ✅ 可精准控制输出长度 | - |
| **效果** | - | ❌ 通常弱于 AT |
| **问题** | - | ❌ 存在 Multi-modality 问题 |

**适用场景**：语音合成（需精确控制长度）

---

## 十七、Cross Attention：Encoder-Decoder 桥梁

### 核心机制

```
Cross Attention = Encoder 和 Decoder 的信息传递通道

Query (Q): 来自 Decoder 的输出
Key (K):   来自 Encoder 的输出
Value (V): 来自 Encoder 的输出
```

### 运算流程

```
Decoder 输出 → Q
              ↓
Encoder 输出 → K, V
              ↓
         Q × K → Attention Score
              ↓
         加权求和 V
              ↓
         提取 Encoder 关键信息
              ↓
         用于 Decoder 生成
```

### 连接方式

```
原始 Transformer:
Decoder 每一层都读取 Encoder 最后一层的输出

可优化方向:
多层连接方式可自定义（研究方向）
```

---

## 十八、Decoder 完整结构

### Transformer Decoder Block

```
输入（来自上一时刻）
         │
         ▼
┌─────────────────────┐
│  Masked Self-       │
│  Attention          │
└─────────┬───────────┘
          │
    ┌─────┴─────┐
    │  Add & Norm │
    └─────┬─────┘
          │
          ▼
┌─────────────────────┐
│  Cross Attention    │ ← 来自 Encoder
│  (Q from Decoder,   │
│   K,V from Encoder) │
└─────────┬───────────┘
          │
    ┌─────┴─────┐
    │  Add & Norm │
    └─────┬─────┘
          │
          ▼
┌─────────────────────┐
│   Feed Forward      │
└─────────┬───────────┘
          │
    ┌─────┴─────┐
    │  Add & Norm │
    └─────┬─────┘
          │
          ▼
     输出（到下一时刻）
```

### Decoder vs Encoder

| 模块 | Encoder | Decoder |
|------|---------|---------|
| Self-Attention | 普通 | **Masked** |
| Cross Attention | ❌ 无 | ✅ 有 |
| 输入来源 | 原始序列 | 自身输出 + Encoder 输出 |

---

# Part 5: Transformer 训练

---

## 十九、Teacher Forcing 训练法

### 训练数据

```
语音辨识：声音 - 文字 配对数据
机器翻译：源语言 - 目标语言 配对数据
```

### 训练过程

```
推理时：Decoder 输入 = 自身生成的内容
训练时：Decoder 输入 = 正确答案（Ground Truth）
```

### 损失函数

```
每个位置 = 分类任务
损失 = Cross Entropy（交叉熵）

总损失 = 所有位置的 Cross Entropy 之和
       = L(y₁, ŷ₁) + L(y₂, ŷ₂) + ... + L(END, ŷₙ)
```

---

## 二十、Exposure Bias 问题

### 核心矛盾

```
训练时：Decoder 输入全是正确答案
推理时：Decoder 输入是自身生成的内容（可能有错）

训练与推理的输入分布不一致！
```

### 后果

```
模型从未见过错误输入
→ 面对错误输入时表现极差
→ 加剧错误传播
→ 一步错，步步错
```

---

## 二十一、Schedule Sampling 解决方案

### 核心思路

```
训练时不再只输入正确答案
而是随机混入模型自身生成的内容
让模型提前适应错误输入
```

### 实现方式

```
训练时输入 = 
  以概率 p: 正确答案（Ground Truth）
  以概率 1-p: 模型自身生成的内容

p 随训练进度逐渐减小
```

### 注意事项

```
传统 Schedule Sampling 适用于 RNN/LSTM
Transformer 版本需调整，避免破坏并行化能力
```

---

# Part 6: 序列生成优化技巧

---

## 二十二、Copy Mechanism（复制机制）

### 使用场景

```
聊天机器人：复述用户人名
摘要生成：提取原文关键句
机器翻译：翻译专有名词
```

### 核心思想

```
不需要模型创造新词
而是从输入中复制信息
```

### 实现模型

| 模型 | 说明 |
|------|------|
| **Pointer Network** | 指针网络，直接指向输入位置 |
| **Copy Network** | 复制网络，结合生成与复制 |

**效果**：大幅降低生僻词、专有名词的错误率

---

## 二十三、Guided Attention（约束注意力）

### 适用场景

```
语音辨识：注意力应从左到右移动
语音合成：注意力应按顺序遍历输入
```

### 核心思想

```
要求注意力按固定顺序移动
避免模型漏看输入信息
```

### 实现方法

| 方法 | 说明 |
|------|------|
| **Monotonic Attention** | 单调注意力，顺序移动 |
| **Location-aware Attention** | 位置感知注意力 |

---

## 二十四、Beam Search（束搜索）

### Greedy Decoding 的问题

```
Greedy: 每步选概率最高的词
问题：可能错过全局最优序列
```

### Beam Search 原理

```
保留 Top-K 条最优路径
综合选择全局概率最高的序列
```

### 适用场景

| 适用 | 不适用 |
|------|--------|
| 语音辨识 | 文本续写 |
| 机器翻译 | 语音合成 |
| 答案唯一的任务 | 需要创造力的任务 |

> 创造力任务用 Beam Search 易导致重复、生硬。

---

## 二十五、随机性优化

### 适用任务

```
文本生成、语音合成等需要创造力的任务
```

### 核心思想

```
推理时加入少量噪声（随机性）
生成结果更自然，避免机械重复
```

---

## 二十六、强化学习优化评估指标

### 问题

```
训练用：Cross Entropy（可微）
评估用：BLEU（不可微）
二者不完全对齐
```

### 解决方案

```
把 BLEU 作为强化学习的 Reward
用 RL 优化生成效果
```

### 适用场景

```
对评估指标要求高的场景
如机器翻译比赛
```

---

# Part 7: 对比与总结

---

## 二十七、Self-Attention vs CNN vs RNN

| | CNN | RNN | Self-Attention |
|---|-----|-----|----------------|
| **并行化** | ✅ | ❌ | ✅ |
| **长距离依赖** | ❌ | ❌ | ✅ |
| **感受野** | 固定 | 全局（衰减） | 全局 |
| **位置信息** | ✅ 内置 | ✅ 内置 | ❌ 需编码 |
| **计算复杂度** | O(n) | O(n) | O(n²) |
| **数据需求** | 少 | 中 | 多 |

---

## 二十八、Transformer 完整架构图

```
┌─────────────────────────────────────────────────────────┐
│                      Transformer                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │                   Decoder                        │   │
│  │  ┌─────────────────────────────────────────┐    │   │
│  │  │ Output Embedding + Positional Encoding  │    │   │
│  │  └──────────────────┬──────────────────────┘    │   │
│  │                     │                           │   │
│  │  ┌──────────────────▼──────────────────────┐    │   │
│  │  │         Masked Multi-Head Attention     │    │   │
│  │  └──────────────────┬──────────────────────┘    │   │
│  │                     │                           │   │
│  │  ┌──────────────────▼──────────────────────┐    │   │
│  │  │              Add & Norm                  │    │   │
│  │  └──────────────────┬──────────────────────┘    │   │
│  │                     │                           │   │
│  │  ┌──────────────────▼──────────────────────┐    │   │
│  │  │    Cross Attention (Q←Dec, K,V←Enc)     │◄───┼───┐
│  │  └──────────────────┬──────────────────────┘    │   │ │
│  │                     │                           │   │ │
│  │  ┌──────────────────▼──────────────────────┐    │   │ │
│  │  │              Add & Norm                  │    │   │ │
│  │  └──────────────────┬──────────────────────┘    │   │ │
│  │                     │                           │   │ │
│  │  ┌──────────────────▼──────────────────────┐    │   │ │
│  │  │           Feed Forward                   │    │   │ │
│  │  └──────────────────┬──────────────────────┘    │   │ │
│  │                     │                           │   │ │
│  │  ┌──────────────────▼──────────────────────┐    │   │ │
│  │  │              Add & Norm                  │    │   │ │
│  │  └──────────────────┬──────────────────────┘    │   │ │
│  │                     │                           │   │ │
│  │           (重复 N 次)                          │   │ │
│  │                     │                           │   │ │
│  │  ┌──────────────────▼──────────────────────┐    │   │ │
│  │  │         Linear + Softmax                 │    │   │ │
│  │  └──────────────────┬──────────────────────┘    │   │ │
│  │                     │                           │   │ │
│  │                     ▼                           │   │ │
│  │              输出概率分布                        │   │ │
│  └─────────────────────────────────────────────────┘   │ │
│                                                         │ │
│  ┌─────────────────────────────────────────────────┐   │ │
│  │                   Encoder                        │   │ │
│  │  ┌─────────────────────────────────────────┐    │   │ │
│  │  │  Input Embedding + Positional Encoding  │    │   │ │
│  │  └──────────────────┬──────────────────────┘    │   │ │
│  │                     │                           │   │ │
│  │  ┌──────────────────▼──────────────────────┐    │   │ │
│  │  │         Multi-Head Attention            │    │   │ │
│  │  └──────────────────┬──────────────────────┘    │   │ │
│  │                     │                           │   │ │
│  │  ┌──────────────────▼──────────────────────┐    │   │ │
│  │  │              Add & Norm                  │    │   │ │
│  │  └──────────────────┬──────────────────────┘    │   │ │
│  │                     │                           │   │ │
│  │  ┌──────────────────▼──────────────────────┐    │   │ │
│  │  │           Feed Forward                   │    │   │ │
│  │  └──────────────────┬──────────────────────┘    │   │ │
│  │                     │                           │   │ │
│  │  ┌──────────────────▼──────────────────────┐    │   │ │
│  │  │              Add & Norm                  │────┼─┘
│  │  └──────────────────┬──────────────────────┘    │
│  │                     │                           │
│  │           (重复 N 次)                          │
│  │                     │                           │
│  │                     ▼                           │
│  │              Encoder 输出                       │
│  └─────────────────────────────────────────────────┘
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 二十九、面试高频问题

### Q1: Self-Attention 和 CNN 的区别？
A: CNN 只看局部，Self-Attention 看全局。CNN 是 Self-Attention 的特例。数据少用 CNN，数据多用 Self-Attention。

### Q2: Self-Attention 和 RNN 的区别？
A: RNN 串行无法并行；Self-Attention 并行效率高。RNN 长距离依赖衰减；Self-Attention 直接捕捉。

### Q3: 为什么用 Q、K、V 三个向量？
A: 解耦查询和匹配。Q="我要找什么"，K="我是什么"，V="我的内容"。

### Q4: 为什么要除以 √d_k？
A: 防止点积过大，导致 softmax 梯度消失。

### Q5: Self-Attention 时间复杂度？
A: O(n² × d)，序列长时计算量是瓶颈。

### Q6: Multi-Head Attention 作用？
A: 学习多种"相关性"，每个 Head 关注不同关系。

### Q7: 为什么需要 Positional Encoding？
A: Self-Attention 无位置信息，需额外编码。

### Q8: Transformer 为什么用 Layer Norm？
A: 不依赖 batch size，对变长序列友好，训练推理一致。

### Q9: Residual Connection 作用？
A: 缓解梯度消失，深层网络易训练。

### Q10: Decoder 为什么用 Masked Self-Attention？
A: 生成第 N 个词时，只能看左侧已生成内容，不能看右侧。

### Q11: Cross Attention 的 Q、K、V 来源？
A: Q 来自 Decoder，K、V 来自 Encoder。

### Q12: 什么是 Teacher Forcing？
A: 训练时 Decoder 输入正确答案，而非自身生成内容。

### Q13: 什么是 Exposure Bias？
A: 训练输入正确答案，推理输入自身生成，分布不一致。

### Q14: 如何解决 Exposure Bias？
A: Schedule Sampling，训练时混入模型自身生成内容。

### Q15: AT vs NAT 的区别？
A: AT 逐词生成串行；NAT 一次性并行生成。NAT 更快但效果略差。

---

## 三十、记忆口诀

### Self-Attention

> **Q 查 K 匹配得分，Softmax 归一成权。**  
> **V 是内容待抽取，加权求和全局现。**

### Transformer Encoder

> **位置编码先加上，多头注意全局看。**  
> **残差连接保梯度，层归一化稳训练。**

### Transformer Decoder

> **Mask 屏蔽未生成，Cross 连接编码器。**  
> **BOS 开始 END 终止，自回归逐词生。**

### 训练技巧

> **教师强制给答案，曝光偏差要解决。**  
> **复制机制引输入，束搜索选最优。**

---

## 三十一、要点总结图

```
┌─────────────────────────────────────────────────────┐
│              Transformer 核心要点                    │
├─────────────────────────────────────────────────────┤
│  Encoder                                            │
│  ───────                                            │
│  • 输入：向量序列                                    │
│  • 结构：Multi-Head Attention + Add&Norm + FC       │
│  • 重复 N 次                                        │
├─────────────────────────────────────────────────────┤
│  Decoder                                            │
│  ───────                                            │
│  • 输入：自身输出 + Encoder 输出                     │
│  • 结构：Masked Attention + Cross Attention + FC    │
│  • AT: 逐词生成 | NAT: 并行生成                      │
│  • BOS 开始 | END 终止                              │
├─────────────────────────────────────────────────────┤
│  训练                                               │
│  ─────                                              │
│  • Teacher Forcing: 输入正确答案                    │
│  • Exposure Bias: 训练推理分布不一致                │
│  • Schedule Sampling: 混入自身生成内容              │
├─────────────────────────────────────────────────────┤
│  优化技巧                                           │
│  ─────────                                          │
│  • Copy Mechanism: 从输入复制                       │
│  • Guided Attention: 约束注意力顺序                 │
│  • Beam Search: 保留 Top-K 路径                     │
│  • RL 优化：用 BLEU 作 Reward                       │
└─────────────────────────────────────────────────────┘
```

---

# Part 8: Self-Attention 变形与加速技术

> 视频来源：【李宏毅机器学习】各式各样神奇的自注意力机制（Self-attention）变型  
> 整理时间：2026-03-22

---

## 三十二、为什么需要 Self-Attention 变形？

### 核心痛点：N² 计算瓶颈

```
标准 Self-Attention:
- N 个 Key × N 个 Query = N² 次内积
- 得到 N×N 的 Attention Matrix
- 计算量正比于 O(N²)
```

### 何时成为瓶颈？

```
只有当 N 非常长时，Self-Attention 才主导整个网络运算！

例：256×256 图片
- 每个 Pixel 作为一个单位
- N = 256×256 = 65,536
- N² = (256×256)² = 256⁴ ≈ 43 亿次运算！
```

### 重要提醒

```
Self-Attention 只是 Transformer 的一个模块！

如果 Feed-Forward 部分的运算量更大
→ 加速 Self-Attention 帮助有限

只有序列非常长时
→ Self-Attention 变形才能发挥真正效用
```

---

## 三十三、基于人工先验的加速方法

### 核心思路

```
根据人类对问题的理解
直接设定某些位置的 Attention Weight 为 0
不需要计算所有 N×N 个数值
```

---

### 1. Local Attention（局部注意力）

**别名**：Truncated Attention

**做法**：
```
每个位置只看左右邻居
远距离的 Attention Weight 直接设为 0
只计算局部的数值
```

**Attention Matrix 示意**：
```
    1 2 3 4 5 6 7 8
1   ■ ■ ■ □ □ □ □ □
2   ■ ■ ■ ■ □ □ □ □
3   ■ ■ ■ ■ ■ □ □ □
4   □ ■ ■ ■ ■ ■ □ □
5   □ □ ■ ■ ■ ■ ■ □
6   □ □ □ ■ ■ ■ ■ ■
7   □ □ □ □ ■ ■ ■ ■
8   □ □ □ □ □ ■ ■ ■

■ = 需要计算  □ = 直接设为 0
```

**问题**：
```
只看小范围资讯 → Attention 和 CNN 没什么差别
那直接用 CNN 就好！
```

---

### 2. Strided Attention（跨距注意力）

**做法**：
```
不是看紧邻的邻居
而是间隔几格，看更远位置的资讯
间隔数可以自己根据任务决定
```

**Attention Matrix 示意**：
```
    1 2 3 4 5 6 7 8
1   ■ □ ■ □ ■ □ ■ □
2   □ ■ □ ■ □ ■ □ ■
3   ■ □ ■ □ ■ □ ■ □
4   □ ■ □ ■ □ ■ □ ■
5   ■ □ ■ □ ■ □ ■ □
6   □ ■ □ ■ □ ■ □ ■
7   ■ □ ■ □ ■ □ ■ □
8   □ ■ □ ■ □ ■ □ ■
```

---

### 3. Global Attention（全局注意力）

**核心思想**：
```
加入特殊 Token（Special Token）
让它收集整个序列的信息
```

**两种做法**：
```
方法 1：从原有序列里选 Token 当特殊 Token
       - BERT 里的 [CLS] Token
       - 句子末尾的句号

方法 2：直接额外添加新的特殊 Token
       - 不管输入是什么，都固定加几个
       - 它们和所有 Token 互相 Attend
```

**Attention Matrix 示意**（假设位置 4 是特殊 Token）：
```
    1 2 3 4 5 6 7 8
1   □ □ □ ■ □ □ □ □
2   □ □ □ ■ □ □ □ □
3   □ □ □ ■ □ □ □ □
4   ■ ■ ■ ■ ■ ■ ■ ■  ← 特殊 Token 行：全部计算
5   □ □ □ ■ □ □ □ □
6   □ □ □ ■ □ □ □ □
7   □ □ □ ■ □ □ □ □
8   □ □ □ ■ □ □ □ □
        ↑
    特殊 Token 列：全部计算
```

**比喻**：
> 特殊 Token 就像"里长"，大家都认识里长，里长也认识所有人，资讯通过里长传递。

---

### 4. 组合方案：Longformer & BigBird

> 小孩子才做选择，成熟的方案是全部都用！

**Multi-head 机制的优势**：
```
设定多个 Head
让每个 Head 做不同的事：
- 有的 Head 做 Local Attention
- 有的做 Strided Attention
- 有的做 Global Attention
```

**Longformer**：
```
组合：Local + Strided + Global Attention
```

**BigBird**：
```
在 Longformer 基础上 + Random Attention

Random Attention：
- 随机选一些 Token
- 让它们彼此之间也做 Attention
```

---

## 三十四、基于数据驱动的加速方法

### 核心思路

```
不用人工规则，用数据驱动的方法
快速估算哪些位置会有大的 Attention Value
把很小的直接设 0
```

---

### 5. Reformer & Rin Transformer（聚类方法）

**做法**：
```
对 Query 和 Key 做快速聚类（Clustering）
把相近的向量归为同一簇
只有同簇的 Query 和 Key，才计算 Attention Weight
不同簇直接设 0
```

**疑问**：
```
Q: 聚类本身会不会很耗运算？
A: 聚类有很多快速近似方法
   复杂度远低于 N²
   能有效降低整体计算量
```

---

### 6. Sparse Sorting Network（稀疏排序网络）

**核心思想**：
```
用一个额外的小网络
输入序列，输出一个 0-1 二值 Mask 矩阵
- 深色为 1（需要计算）
- 浅色为 0（直接设 0）
```

**特点**：
```
- 过程是可微分的
- Mask 矩阵会和主网络一起训练
- 让模型自己决定 Attention 的计算位置
```

**进一步优化**：
```
让多个输入向量共用同一个 Mask
降低小网络的输出维度
再放大成 N×N 的 Mask
避免运算量回到 N²
```

---

## 三十五、基于低秩近似的加速方法

### 7. Informer

**实验发现**：
```
Attention Matrix 其实是低秩矩阵！

- 很多列是重复的、线性相关的
- 存在大量冗余信息
- 不需要完整矩阵
```

**做法**：
```
1. 从 N 个 Key 里挑 K 个最具代表性的
2. 只计算这 K 个 Key 和所有 Query 的 Attention
   得到 N×K 矩阵（而非 N×N）
3. 对应挑出 K 个 Value
   用 Attention Weight 对这 K 个 Value 做加权
```

**为什么不精简 Query？**
```
精简 Query 会缩短输出序列长度！

如果任务需要每个位置都输出 Label（如序列标注）
→ 不能精简 Query

只有分类这类只输出一个 Label 的任务
→ 才可以精简 Query
```

---

### 8. Compress Attention

**做法**：
```
用 CNN 对 Key 序列做下采样
缩短长度作为代表 Key
```

---

### 9. Linformer

**做法**：
```
把 Key 矩阵（D×N）乘一个 N×K 的投影矩阵
得到 D×K 矩阵
每一列是原有 Key 的线性组合，作为代表 Key
```

---

## 三十六、基于矩阵乘法优化的加速方法

### 核心洞察

**标准 Self-Attention 的矩阵运算**：
```
输入 I → 乘 W_Q 得 Q（D×N）
       → 乘 W_K 得 K（D×N）
       → 乘 W_V 得 V（D'×N）

Attention Matrix A = Softmax(K^T · Q)  ← O(N²) 瓶颈！

输出 O = A · V
```

**改变矩阵相乘顺序**：
```
先算 V · K^T，再乘 Q

Step 1: V·K^T
        D'×N 乘 N×D → 得到 D'×D 小矩阵
        运算量：O(D'·N·D)

Step 2: (V·K^T) · Q
        D'×D 乘 D×N → 得到 D'×N
        运算量：O(D'·D·N)

总复杂度：O(N)  ← 从 O(N²) 降到 O(N)！

当 N 远大于 D 时，提速极其明显
```

**问题**：
```
Softmax(exp(Q·K^T)) 不能直接拆开！

exp(Q·K^T) ≠ exp(Q) · exp(K^T)
```

**解决方案**：
```
用核函数技巧（Kernel Trick）
把 exp(Q·K^T) 拆解为 F(Q) · F(K)^T
保留 Softmax 的同时，实现线性复杂度
```

**代表模型**：
- **Linear Transformer**
- **Performer**

---

## 三十七、颠覆性方法：不需要 Attention？

### 10. Synthesizer

**颠覆性问题**：
```
做 Self-Attention，一定要用 Q 和 K 算 Attention 吗？
```

**答案**：
```
不需要！

直接把 Attention Matrix 当作网络的可学习参数
训练时直接优化这个 N×N 矩阵
不再计算 Attention Weight
```

**实验结果**：
```
性能下降不多！

让我们重新思考 Attention 的价值：
- 过去认为 Attention 要随输入动态变化
- 其实固定的 Attention 矩阵也能学到足够的模式
```

---

### 11. Attention-Free 方法

```
处理序列一定要用 Attention 吗？

现在已经有一系列 Attention-Free 的方法
用 MLP 等结构替代 Attention

这又是另一个故事...
```

---

## 三十八、Long Range Arena 基准对比

| 模型 | 速度 | 效果 | 内存 | 核心方法 |
|------|------|------|------|----------|
| **标准 Transformer** | 🐌 最慢 | ⭐⭐⭐⭐⭐ 最好 | 🔴 最大 | 完整 N×N Attention |
| **Local Attention** | 🚀 最快 | ⭐⭐ 较差 | 🟢 最小 | 只看局部邻居 |
| **Reformer** | ⚡ 快 | ⭐⭐⭐ 一般 | 🟡 中 | 聚类方法 |
| **Sparse Sorting Network** | ⚡ 快 | ⭐⭐⭐ 略降 | 🟢 小 | 学习 Mask |
| **Informer** | 🚀 极快 | ⭐⭐⭐⭐ 好 | 🟢 小 | 低秩近似 |
| **Performer** | 🚀 极快 | ⭐⭐⭐⭐ 好 | 🟢 小 | 核函数技巧 |
| **Linear Transformer** | 🚀 极快 | ⭐⭐⭐⭐ 好 | 🟢 小 | 矩阵重排 |
| **Synthesizer** | ⚡ 快 | ⭐⭐⭐ 略降 | 🟡 中 | 固定 Attention |

**图例说明**：
```
横轴：速度（越右越快）
纵轴：效果（分数越高越好）
圆圈大小：内存占用
```

**结论**：
```
长序列场景优选：
- Informer
- Performer
- Linear Transformer

速度极快，效果和标准 Transformer 差距较小
```

---

## 三十九、Self-Attention 变形总结

### 加速方法分类

```
┌─────────────────────────────────────────────────────────┐
│           Self-Attention 加速方法分类                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 基于人工先验                                        │
│     ─────────———                                        │
│     • Local Attention（局部）                           │
│     • Strided Attention（跨距）                         │
│     • Global Attention（全局特殊 Token）                │
│     • Longformer / BigBird（组合方案）                  │
│                                                         │
│  2. 基于数据驱动                                        │
│     ─———————                                            │
│     • Reformer / Rin Transformer（聚类）                │
│     • Sparse Sorting Network（学习 Mask）               │
│                                                         │
│  3. 基于低秩近似                                        │
│     ─———————                                            │
│     • Informer（选代表性 Key）                          │
│     • Compress Attention（CNN 下采样）                  │
│     • Linformer（线性投影）                             │
│                                                         │
│  4. 基于矩阵优化                                        │
│     ─———————                                            │
│     • Linear Transformer（改变乘法顺序）                │
│     • Performer（核函数技巧）                           │
│                                                         │
│  5. 颠覆性方法                                          │
│     ─———————                                            │
│     • Synthesizer（固定 Attention 矩阵）                │
│     • Attention-Free（MLP 替代）                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 四十、选择建议

### 何时使用标准 Transformer？
```
• 序列长度适中（N < 1000）
• 对效果要求极高
• 计算资源充足
```

### 何时使用加速变形？
```
• 序列非常长（N > 1000）
• Self-Attention 主导运算
• 需要长程依赖建模

推荐：Informer / Performer / Linear Transformer
```

### 何时用 Local Attention？
```
• 局部信息足够（如 CNN 任务）
• 速度优先，效果次要
```

### 何时用 Global Attention？
```
• 需要全局信息聚合
• 类似 [CLS] 的分类任务
```

---

## 延伸阅读

- **Longformer**: 《Longformer: The Long-Document Transformer》
- **BigBird**: 《Big Bird: Transformers for Longer Sequences》
- **Reformer**: 《Reformer: The Efficient Transformer》
- **Informer**: 《Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting》
- **Performer**: 《Rethinking Attention with Performers》
- **Linformer**: 《Linformer: Self-Attention with Linear Complexity》
- **Synthesizer**: 《Synthesizer: Rethinking Self-Attention for Transformer Models》
- **Long Range Arena**: 《Long Range Arena: A Benchmark for Efficient Transformers》

---

*整理时间：2026-03-22*  
*来源：李宏毅机器学习课程视频*  
*内容：Self-Attention 变形与加速技术（Part 8）*

---

## 延伸阅读

- 《Attention is All You Need》原论文
- 《On Layer Normalization in the Transformer Architecture》
- 《Power Norm: Rethinking Batch Normalization in Transformers》
- 《Grammar as a Foreign Language》
- 李宏毅 ML 课程：YouTube/B 站

---

*整理时间：2026-03-22*  
*来源：李宏毅机器学习课程视频*  
*内容：Self-Attention + Transformer（完整）*
