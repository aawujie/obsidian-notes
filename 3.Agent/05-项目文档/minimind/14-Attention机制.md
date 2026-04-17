---
tags: [minimind, attention, transformer, concepts]
---

# Attention 机制

Transformer 的核心。理解了 Attention 就理解了大模型的骨架。

---

## 一句话

> 每个 token 看一眼所有其他 token，算出"该关注谁"，然后按关注度加权提取信息。

---

## Q、K、V 是什么

把 Attention 想成一个**搜索系统**：

| 角色    | 全称       | 类比          | 做什么         |
| ----- | -------- | ----------- | ----------- |
| **Q** | Query 查询 | 你在搜索框里打的关键词 | "我想找什么？"    |
| **K** | Key 键    | 每篇文档的标题/标签  | "这篇文档讲什么？"  |
| **V** | Value 值  | 每篇文档的正文内容   | "这篇文档的实际内容" |

流程：
1. 拿 Q 和每个 K 做**点积**（相似度匹配）
2. 结果过 Softmax（归一化成概率）
3. 用这些概率对 V 做**加权求和**（提取信息）

---

## 矩阵形状

假设序列长度 `n`，head 维度 `d`：

```
输入: X → [batch, n, hidden_size]

经过线性变换:
Q = X × W_q → [batch, n, d]     每个位置一个查询向量
K = X × W_k → [batch, n, d]     每个位置一个键向量
V = X × W_v → [batch, n, d]     每个位置一个值向量

注意力计算:
scores = Q × K^T → [batch, n, n]   n² 个相似度分数
                         ↑
                    这就是注意力矩阵

attn = softmax(scores / √d)        归一化
output = attn × V → [batch, n, d]  加权提取
```

**关键**：注意力矩阵是 `n × n`，这就是 O(n²) 复杂度的来源。

---

## 序列长度 vs 向量维度

容易混淆的两个"长度"：

| 概念 | 符号 | 典型值 | 含义 |
|------|------|--------|------|
| **序列长度** | n | 768 / 2048 / 1M | 一次输入多少个 token |
| **head 维度** | d | 64 / 96 / 128 | 每个 Q/K/V 向量有多长 |

**1M 上下文指的是 n = 1000000，不是 d = 1000000。**

d 始终很小（通常 ≤ 128），因为它只是一个"语义向量"的维度。
n 可以很大，因为它是"要处理多少个 token"。

---

## 计算量和显存

注意力矩阵 `[n, n]` 的代价：

| 序列长度 n | 矩阵元素数 | fp16 显存 | 感受    |
| ------ | ----- | ------- | ----- |
| 768    | 59 万  | 1.2 MB  | 毫无压力  |
| 2K     | 400 万 | 8 MB    | 轻松    |
| 32K    | 10 亿  | 2 GB    | 一张卡搞定 |
| 128K   | 160 亿 | 32 GB   | 快爆了   |
| 1M     | 1 万亿  | 2 TB    | 单卡放不下 |

这就是为什么长上下文需要 [[13-长上下文技术]] 中的各种优化。

---

## Multi-Head Attention（多头注意力）

不只一组 Q/K/V，而是**多组并行**：

```
hidden_size = 768
num_heads = 8
head_dim = 768 / 8 = 96

每个 head 独立做 Attention:
head_1: Q₁K₁V₁ → output₁   关注语法关系
head_2: Q₂K₂V₂ → output₂   关注语义相似
head_3: Q₃K₃V₃ → output₃   关注位置邻近
...

最后拼起来: concat(output₁, output₂, ...) × W_o → [batch, n, 768]
```

每个 head 学到**不同的注意力模式**，组合起来理解更丰富。

---

## GQA（Grouped-Query Attention）

标准 MHA 中每个 head 有自己的 Q、K、V，总共 `3 × num_heads × head_dim` 参数。
推理时 KV Cache 也是 `num_heads × n × head_dim`。

**GQA 的做法**：多个 Q head 共享一组 K/V。

```
标准 MHA (minimind 如果用):
  Q heads: 8 组
  K heads: 8 组
  V heads: 8 组
  KV Cache: 8 × n × 96

GQA (minimind 实际用):
  Q heads: 8 组
  K heads: 4 组 ← 只有 4 组！
  V heads: 4 组
  KV Cache: 4 × n × 96 → 省一半！

  每 2 个 Q head 共享 1 组 KV
```

**好处**：推理时 KV Cache 缩小，长上下文更省显存，速度更快，精度几乎不掉。

minimind: `num_attention_heads=8, num_key_value_heads=4`（2:1 分组）

---

## Flash Attention

不改 Attention 的数学，只改**内存访问模式**：

```
标准方式（慢）:
  1. 算出完整的 [n, n] 注意力矩阵 → 写入显存
  2. 对整个矩阵做 softmax → 读写显存
  3. 矩阵乘以 V → 读写显存
  = 3 次完整的 n² 显存读写

Flash Attention（快）:
  把 Q/K/V 切成小块，一块一块地:
  1. 算一小块注意力分数
  2. 立刻做 softmax（在 SRAM 里，不写回显存）
  3. 立刻乘以 V 得到部分结果
  4. 累加到最终输出
  = 不需要存完整的 [n, n] 矩阵！
```

**类比**：标准方式像是把整本书复印出来再看；Flash Attention 像是翻一页看一页，看完就翻走。

显存从 O(n²) 降到 O(n)，速度提升 2-4×。

minimind: 当 `config.flash_attn=True` 时用 PyTorch 的 `scaled_dot_product_attention`（底层调 Flash Attention）。

---

## Causal Mask（因果遮罩）

生成式模型（GPT 系列）用的是 **Causal / Masked Self-Attention**：

```
位置 1 只能看 [1]
位置 2 只能看 [1, 2]
位置 3 只能看 [1, 2, 3]
...

注意力矩阵变成下三角:

  1 2 3 4 5
1 ✓ ✗ ✗ ✗ ✗
2 ✓ ✓ ✗ ✗ ✗
3 ✓ ✓ ✓ ✗ ✗
4 ✓ ✓ ✓ ✓ ✗
5 ✓ ✓ ✓ ✓ ✓
```

**为什么**：生成时你还没生成后面的 token，不能偷看未来。

---

## KV Cache（推理加速）

生成第 n+1 个 token 时，前 n 个 token 的 K 和 V 不会变。

```
不用 Cache（慢）:
  生成 token 5 时，重新算 token 1-4 的 K、V
  生成 token 6 时，重新算 token 1-5 的 K、V
  → 大量重复计算

用 Cache（快）:
  生成 token 5 时，只算 token 5 的 Q/K/V
  把 token 5 的 K/V 追加到缓存
  Q₅ 和缓存中的 [K₁,K₂,K₃,K₄,K₅] 做点积
  → 每步只算 1 个 token 的变换！
```

**代价**：缓存越来越大，占显存。这就是为什么 GQA（减少 KV 头）和 KV 压缩很重要。

---

## minimind 中的 Attention

```python
# model/model_minimind.py 中的关键参数
num_attention_heads = 8      # Q 有 8 个 head
num_key_value_heads = 4      # KV 有 4 个 head (GQA)
head_dim = 768 / 8 = 96      # 每个 head 的维度
flash_attn = True            # 可选 Flash Attention
```

特殊设计：
- **QK Norm**：对 Q 和 K 做 RMSNorm，训练更稳定
- **GQA**：2:1 分组，KV Cache 减半
- **RoPE**：旋转位置编码注入到 Q 和 K 中（不是加，是旋转）
- **YaRN**：推理时可选的 RoPE 外推

---

> 术语速查：[[12-术语速查]] | 长上下文技术：[[13-长上下文技术]] | 模型架构全貌：[[01-模型架构]]
