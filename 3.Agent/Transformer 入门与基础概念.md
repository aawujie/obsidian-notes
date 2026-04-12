# Transformer 入门与基础概念

> 基于 3Blue1Brown 视频整理，介绍 GPT 和 Transformer 的核心概念

---

## GPT 的含义

| 字母 | 全称 | 含义 |
|------|------|------|
| **G** | Generative | 生成新文本 |
| **P** | Pretrained | 预训练：从海量数据学习 |
| **T** | Transformer | 核心架构：Transformer 神经网络 |

**Pretrained 的含义**：模型先在大量数据上预训练，然后可以针对特定任务微调。

---

## Transformer 的应用

Transformer 不仅用于文本生成，还广泛应用于：

| 应用 | 输入 | 输出 |
|------|------|------|
| **语音识别** | 音频 | 文字转录 |
| **语音合成** | 文本 | 合成语音 |
| **图像生成** | 文本描述 | 图像 (DALL-E, Midjourney) |
| **机器翻译** | 源语言文本 | 目标语言文本 |
| **文本生成** | 前文 | 预测下一个 token (ChatGPT) |

---

## 自回归生成原理

### 核心任务

**输入**：一段文本  
**输出**：下一个 token 的概率分布

```
输入: "The cat sat on the..."
输出: {mat: 0.4, chair: 0.3, floor: 0.2, ...}
```

### 如何生成长文本

```python
# 自回归生成循环
text = "Once upon a time"
for _ in range(100):
    # 1. 预测下一个 token 的分布
    probs = model.predict(text)
    # 2. 从分布中采样
    next_token = sample(probs)
    # 3. 追加到文本
    text += next_token
```

**效果对比**：
- **GPT-2**（小模型）：生成故事不连贯
- **GPT-3**（大模型，相同架构）：生成合理、连贯的故事

**关键洞察**：规模（参数数量）带来质的提升。

---

## 数据流概览

```
输入文本
    ↓
[Tokenization] → 拆分成 tokens
    ↓
[Embedding] → 每个 token 变成向量
    ↓
[Attention Block] × N → 向量间传递信息，更新含义
    ↓
[MLP Block] × N → 独立处理每个向量
    ↓
[Unembedding] → 最后一个向量 → 概率分布
    ↓
采样 → 生成下一个 token
```

---

## 关键组件详解

### 1. Tokenization（分词）

**概念**：将文本拆分成小片段（tokens）

```
"Hello world!" → ["Hello", " world", "!"]
```

**特点**：
- 通常是单词或单词片段
- 也可能包含标点、子词等
- 对于图像/音频：小块图像/声音片段

**词表大小**：GPT-3 约 50,257 个 tokens

---

### 2. Embedding（嵌入）

**概念**：将每个 token 映射到高维向量

```python
# 嵌入矩阵 W_E: (vocab_size, embedding_dim)
# GPT-3: (50257, 12288)

E_hello = W_E[:, token_id("Hello")]  # 12288 维向量
```

**关键特性**：
- 语义相似的词，向量距离近
- 高维空间（GPT-3: 12,288 维）
- 方向编码语义

**经典例子**：
```
woman - man ≈ queen - king
```
- 存在"性别"方向

**其他例子**：
```
Italy - Germany + Hitler ≈ Mussolini
Germany - Japan + sushi ≈ bratwurst
cats - cat ≈ 复数方向
```

**点积的意义**：
- 正数：方向相似
- 零：垂直（无关）
- 负数：方向相反

**参数统计**：
- W_E: 50,257 × 12,288 ≈ **6.17亿参数**

---

### 3. 上下文大小（Context Size）

**概念**：模型一次能处理的 token 数量

| 模型 | 上下文大小 |
|------|-----------|
| GPT-3 | 2,048 |
| GPT-4 | 8,192 / 32,768 |
| Claude | 100K+ |

**数据形状**：(context_size, embedding_dim) = (2048, 12288)

**限制**：
- 长对话中，早期信息可能被"遗忘"
- 是 Transformer 的主要瓶颈之一

---

### 4. 注意力块（Attention Block）

**作用**：让向量间传递信息，更新含义

**例子**：
```
"a machine learning model" vs "a fashion model"
```
- "model" 的初始嵌入相同
- 注意力块根据上下文更新其含义

**详细内容**：见下一章《Transformer 注意力机制详解》

---

### 5. MLP 块（Multi-Layer Perceptron）

**作用**：独立处理每个向量，类似"提问-回答"机制

**特点**：
- 向量间不交互
- 并行处理
- 主要存储事实知识

**详细内容**：见《Transformer MLP 如何存储知识》

---

### 6. Unembedding（反嵌入）

**作用**：将最后一个向量映射到词表大小的 logits

```python
# W_U: (embedding_dim, vocab_size)
# GPT-3: (12288, 50257)

logits = E_last @ W_U  # (vocab_size,) = (50257,)
```

**为什么只用最后一个向量？**
- 训练时，每个位置同时预测下一个 token
- 推理时，只关心序列末尾的预测

**参数统计**：
- W_U: 12,288 × 50,257 ≈ **6.17亿参数**

---

## Softmax 函数

### 作用

将任意实数列表转换为概率分布：
- 每个值在 (0, 1) 之间
- 所有值之和为 1

### 公式

$$\text{softmax}(x_i) = \frac{e^{x_i}}{\sum_{j} e^{x_j}}$$

### 特性

- 最大值的输出接近 1
- 较小值的输出接近 0
- 但比直接取 max "更软"（保留一些概率给次优选项）
- 连续可导

### Temperature（温度）

$$\text{softmax}(x_i / T) = \frac{e^{x_i / T}}{\sum_{j} e^{x_j / T}}$$

| Temperature | 效果 |
|-------------|------|
| T → 0 | 最确定，总是选最大值 |
| T = 1 | 标准 softmax |
| T > 1 | 更均匀，更多随机性 |
| T → ∞ | 均匀分布 |

**实际应用**：
- **T=0**：生成可预测、但可能平庸的文本
- **T=2**：更有创意，但可能混乱
- API 通常限制 T ≤ 2

---

## 深度学习基础回顾

### 核心思想

**传统编程**：
```python
def classify_image(image):
    # 手动编写规则...
    if has_fur(image) and has_whiskers(image):
        return "cat"
```

**机器学习**：
```python
model = NeuralNetwork()
# 从数据学习参数
for image, label in training_data:
    prediction = model(image)
    adjust_parameters(prediction, label)
```

### 深度学习的格式要求

1. **输入**：实数数组（张量）
2. **多层变换**：每层都是实数数组
3. **输出**：最终层 = 期望输出
4. **权重交互**：仅通过加权求和（矩阵乘法）
5. **非线性**：穿插非线性函数（如 ReLU）

### GPT-3 参数统计

| 组件 | 参数量 |
|------|--------|
| Embedding (W_E) | ~6.17亿 |
| Unembedding (W_U) | ~6.17亿 |
| Attention (96层 × 96 heads) | ~580亿 |
| MLP (96层) | ~1160亿 |
| **总计** | **~1750亿** |

**权重 vs 数据**：
- **权重（蓝色/红色）**：模型学到的参数，决定行为
- **数据（灰色）**：具体输入，如某段文本

---

## 本章为注意力机制打下的基础

理解注意力机制需要掌握：

1. ✅ **词嵌入**：高维向量，方向编码语义
2. ✅ **Softmax**：将 logits 转为概率分布
3. ✅ **点积**：衡量向量相似度
4. ✅ **矩阵乘法**：深度学习的基本操作

**下一步**：深入学习 Attention 机制（Query-Key-Value 框架）

---

## 关键概念总结

| 概念 | 说明 |
|------|------|
| Token | 文本的最小单位（词或子词） |
| Embedding | 将 token 映射到高维向量 |
| Context Size | 模型能处理的 token 数量 |
| Attention | 向量间传递上下文信息 |
| MLP | 独立处理向量，存储知识 |
| Softmax | 转换为概率分布 |
| Logits | Softmax 前的原始输出 |
| Temperature | 控制生成的随机性 |

---

*Created: 2026-04-12*
