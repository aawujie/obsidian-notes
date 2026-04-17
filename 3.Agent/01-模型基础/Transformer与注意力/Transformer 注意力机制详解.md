# Transformer 注意力机制详解

> 基于 3Blue1Brown 视频整理，深入讲解 Self-Attention 的计算原理

---

## 核心目标

Transformer 的目标：**逐步调整嵌入向量，使其编码更丰富的上下文含义**

```
输入: "The cat sat..."
    ↓
初始嵌入: [The] [cat] [sat] ... (仅编码单个词)
    ↓
注意力层 × N
    ↓
最终嵌入: [The_contextual] [cat_contextual] [sat_contextual] ... (编码上下文)
    ↓
预测下一个 token
```

---

## 高维空间的语义方向

**关键概念**：嵌入向量处于高维空间（如 GPT-3 的 12,288 维），不同方向编码不同语义。

经典例子：
```
woman - man + uncle ≈ aunt
```
- 存在"性别"方向
- 加上这个方向，男词变女词

**注意力机制的作用**：计算需要添加什么向量，将通用嵌入移动到特定语义方向。

---

## 动机示例

### 示例 1：一词多义

"mole" 在不同上下文中的含义：
- "American **shrew mole**" → 鼹鼠（动物）
- "one **mole** of carbon dioxide" → 摩尔（化学单位）
- "biopsy of the **mole**" → 痣（医学）

**初始嵌入**：三个 "mole" 的向量完全相同（仅查表，无上下文）

**注意力后**：根据周围词更新向量方向
- "shrew" + "American" → 动物方向
- "carbon dioxide" → 化学方向
- "biopsy" → 医学方向

### 示例 2：专有名词

"tower" 的嵌入：
- 通用方向：高大建筑
- 前面有 "Eiffel" → 更新为埃菲尔铁塔方向（关联巴黎、法国、钢铁）
- 前面有 "miniature" → 更新为微缩模型方向（不再关联高大）

### 示例 3：长距离依赖

输入："...因此凶手是____"（整本推理小说）

最后一个向量（原本是 "was" 的嵌入）必须编码：
- 全书所有线索
- 嫌疑人信息
- 推理结论

→ 通过多层注意力，信息从全文汇聚到最后一个向量

---

## 单头注意力计算流程

### 简化示例

输入："a fluffy blue creature roamed the verdant forest"

目标：形容词更新对应的名词
- "fluffy" + "blue" → 更新 "creature"
- "verdant" → 更新 "forest"

### 步骤 1：Query（查询）

**概念**：每个词问"我需要什么信息？"

```python
# 名词 "creature" 的 query
Q_creature = W_q @ E_creature
# 维度: (128,) = (128, 12288) @ (12288,)

# 语义："我在找前面的形容词"
```

**计算**：
- 矩阵 $W_q$: (key_query_dim, embedding_dim) = (128, 12288)
- 输入嵌入 $E$: (embedding_dim,) = (12288,)
- 输出 Query $Q$: (key_query_dim,) = (128,)

### 步骤 2：Key（键）

**概念**：每个词回答"我能提供什么信息？"

```python
# 形容词 "fluffy" 的 key
K_fluffy = W_k @ E_fluffy

# 形容词 "blue" 的 key  
K_blue = W_k @ E_blue

# 语义："我是形容词，我在名词前面"
```

### 步骤 3：计算注意力分数

**方法**：Query 和 Key 的点积

```python
score_creature_fluffy = Q_creature · K_fluffy  # 大正数（相关）
score_creature_blue = Q_creature · K_blue      # 大正数（相关）
score_creature_the = Q_creature · K_the        # 小/负数（无关）
```

**可视化**：网格图，点的大小表示分数高低

```
        fluffy  blue  creature  roamed  the  verdant  forest
fluffy    ·      ·      ·        ·      ·      ·        ·
blue      ·      ·      ·        ·      ·      ·        ·
creature  ●●●   ●●●     ·        ·      ·      ·        ·
roamed    ·      ·      ·        ·      ·      ·        ·
the       ·      ·      ·        ·      ·      ·        ·
verdant   ·      ·      ·        ·      ·      ·       ●●●
forest    ·      ·      ·        ·      ·     ●●●       ·
```

### 步骤 4：Softmax 归一化

**目标**：将分数转为概率分布（每列 0-1，和为 1）

```python
# 对每列应用 softmax
attention_weights = softmax(scores / sqrt(d_k), dim=0)
```

**技术细节**：除以 $\sqrt{d_k}$（128 的平方根 ≈ 11.3）用于数值稳定性。

**结果**：注意力模式 (Attention Pattern)

```
        creature  forest
fluffy    0.5       0
blue      0.5       0
the       0         0
verdant   0         0.5
forest    0         0
```

### 步骤 5：Value（值）

**概念**：如果相关，应该添加什么信息？

```python
V_fluffy = W_v @ E_fluffy  # "fluffy" 要添加的信息
V_blue = W_v @ E_blue      # "blue" 要添加的信息
```

**加权求和**：
```python
delta_E_creature = 0.5 * V_fluffy + 0.5 * V_blue + 0 * V_others
```

### 步骤 6：更新嵌入

```python
E_creature_new = E_creature + delta_E_creature
```

**结果**："creature" 的嵌入现在编码了"fluffy blue creature"

---

## 数学公式

原始论文中的紧凑表达：

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

其中：
- $Q = W_q E$ (queries)
- $K = W_k E$ (keys)  
- $V = W_v E$ (values)
- $d_k$ = key/query 维度（如 128）

---

## Masking（掩码）

**问题**：训练时同时预测所有位置的下一个 token，不能让后面的词影响前面的词（泄露答案）。

**解决方案**：将未来位置的分数设为 $-\infty$，softmax 后变为 0。

```
        pos1  pos2  pos3  pos4
pos1      ✓     0     0     0
pos2      ✓     ✓     0     0
pos3      ✓     ✓     ✓     0
pos4      ✓     ✓     ✓     ✓
```

- 下三角矩阵（因果掩码）
- GPT 系列始终使用此掩码

---

## 复杂度分析

注意力矩阵大小 = $(\text{context\_size})^2$

| 上下文长度 | 注意力矩阵大小 |
|-----------|---------------|
| 1K | 1M |
| 4K | 16M |
| 32K | 1B |
| 100K | 10B |

**瓶颈**：上下文长度是 LLM 扩展的主要挑战，近年有变体 aimed at 更 scalable 的注意力机制。

---

## Value 矩阵的分解

### 朴素实现

$W_v$: (embedding_dim, embedding_dim) = (12288, 12288)

参数量：~1.5亿（比其他矩阵大 100 倍）

### 实际实现（低秩分解）

```
W_v = W_v_up @ W_v_down

W_v_down: (key_query_dim, embedding_dim) = (128, 12288)
W_v_up:   (embedding_dim, key_query_dim) = (12288, 128)
```

**概念**：
- $W_v\_down$：将高维嵌入压缩到低维空间
- $W_v\_up$：从低维空间映射回高维嵌入

**优势**：参数量大幅减少，与其他矩阵相当。

---

## 多头注意力 (Multi-Head Attention)

### 动机

不同 head 学习不同类型的上下文关系：
- Head 1：形容词 → 名词
- Head 2：代词 → 先行词
- Head 3：时间词关联
- Head 4：情感分析
- ...

### 实现

```python
# GPT-3: 96 个 heads
heads = [AttentionHead(W_q_i, W_k_i, W_v_up_i, W_v_down_i) 
         for i in range(96)]

# 每个 head 独立计算
delta_E_total = sum(head(E) for head in heads)

# 更新嵌入
E_new = E + delta_E_total
```

### 参数统计 (GPT-3)

每个 head：
- $W_q$: (128, 12288) ≈ 157万
- $W_k$: (128, 12288) ≈ 157万
- $W_v\_down$: (128, 12288) ≈ 157万
- $W_v\_up$: (12288, 128) ≈ 157万
- **每 head 总计**: ~630万

96 heads × 630万 = **~6亿参数/层**

96 层 × 6亿 = **~580亿参数**（注意力部分）

**对比**：GPT-3 总参数 1750亿，注意力占 **~33%**

---

## 命名约定说明

**我的命名**（概念清晰）：
- $W_v\_down$：value down projection
- $W_v\_up$：value up projection

**论文/代码中的命名**（容易混淆）：
- "Value matrix" 通常只指 $W_v\_down$（第一步）
- $W_v\_up$ 被合并到 "Output matrix"（所有 heads 的 up 矩阵拼接）

**注意**：实现细节可能分散注意力，但了解有助于阅读其他资料。

---

## 多层堆叠

```
Input
  ↓
[Attention] → [MLP] → [Attention] → [MLP] → ... (×96层)
  ↓
Output
```

**效果**：
- 第 1-12 层：学习词法、语法关系
- 第 13-48 层：学习语义、实体关系
- 第 49-96 层：学习抽象概念、情感、科学事实

每层嵌入都变得更 nuanced，能编码更高层次的概念。

---

## 关键结论

1. **注意力机制本质**：Query-Key-Value 框架
   - Query："我需要什么？"
   - Key："我能提供什么？"
   - Value："具体提供什么信息？"

2. **并行计算**：注意力高度并行化，适合 GPU 加速

3. **规模优势**：可扩展性让模型能从海量数据学习

4. **参数分布**：
   - 注意力：~33%（580亿）
   - MLP：~66%（1160亿）
   - 其他：~1%

5. **上下文限制**：注意力矩阵大小 = $O(n^2)$，是长上下文的主要瓶颈

---

## 参考资源

- 原始论文：Attention Is All You Need (2017)
- 推荐作者：Andrej Karpathy, Chris Olah
- 历史视频：Vivek (动机讲解), Britt Cruz (LLM 发展史)

---

*Created: 2026-04-12*
