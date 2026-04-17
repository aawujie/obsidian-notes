# Perplexity 与模型质量评估

> **目的：** 理解 TurboQuant 使用的质量评估指标
> **前置知识：** 概率基础、交叉熵概念
> **创建日期：** 2026-04-02

---

## 1. Perplexity (PPL)：最核心的指标

### 1.1 直觉理解

Perplexity = **模型的"困惑度"**，衡量模型预测下一个 token 时有多"犹豫"。

```
PPL = 1    → 完美预测，每个 token 都 100% 确定
PPL = 10   → 平均每个位置"犹豫"于 10 个候选
PPL = 100  → 非常困惑，几乎在猜
```

**PPL 越低，模型越好。**

### 1.2 数学定义

给定文本序列 $w_1, w_2, \ldots, w_N$：

$$\text{PPL} = \exp\left(-\frac{1}{N}\sum_{i=1}^{N} \log P(w_i \mid w_1, \ldots, w_{i-1})\right)$$

展开来说：
1. 模型对每个 token 给出概率 $P(w_i | \text{前文})$
2. 取 log 再平均 → 平均 log 似然（越大越好）
3. 取负号 → 交叉熵（越小越好）
4. 取 exp → PPL（越小越好）

### 1.3 为什么用 PPL 而不是准确率？

| 指标 | 问题 |
|------|------|
| 准确率（top-1 match） | 太粗糙，两个都错的模型分不出好坏 |
| 交叉熵 | 数字太小不直觉（如 1.81 vs 1.82） |
| **PPL** | 有直觉意义（"在 N 个词里选"），差异清晰 |

---

## 2. PPL 在 TurboQuant 中的使用

### 2.1 基本比较

| Cache Type | PPL | vs q8_0 |
|------------|-----|---------|
| f16（基线） | 6.121 | -0.16% |
| q8_0（8-bit） | 6.111 | baseline |
| **turbo4** | **6.125** | **+0.23%** |
| q4_0 | 6.142 | +0.52% |
| turbo3 | 6.176 | +1.06% |
| turbo2 | 6.507 | +6.48% |

### 2.2 怎么读这些数字？

```
q8_0 PPL = 6.111
turbo3 PPL = 6.176

差异 = +0.065（绝对值）= +1.06%（相对）

含义：turbo3 量化让模型平均每个 token 多"犹豫"了约 1%
实际影响：对人类几乎不可感知
```

### 2.3 什么算"灾难性"退化？

```
PPL 变化 < 1%     → 优秀（turbo4）
PPL 变化 1-3%     → 可接受（turbo3）
PPL 变化 3-10%    → 有感知但可用（turbo2）
PPL 变化 > 100%   → 灾难性（如 PPL 3556）

例：Qwen2.5-7B Q4_K_M + turbo3/turbo3 → PPL 3556
    这意味着模型输出基本是乱码
```

### 2.4 测试方法论

TurboQuant 用 **wikitext** 数据集来测 PPL：

```
步骤：
1. 取 wikitext-2 或 wikitext-103 的测试集
2. 按固定 context 长度切分（如 512 tokens/chunk）
3. 对每个 chunk 计算 PPL
4. 取平均值

重要参数：
- context = 512   → 短上下文 PPL
- context = 32K   → 长上下文 PPL（更严格的测试）
- chunks = 50     → 统计显著性更好
- CI ±0.021       → 95% 置信区间
```

---

## 3. KL 散度（KL Divergence）

### 3.1 什么是 KL 散度？

衡量两个概率分布的"距离"。在 TurboQuant 中：

$$D_{KL}(P_{f16} \| P_{quant}) = \sum_i P_{f16}(i) \log \frac{P_{f16}(i)}{P_{quant}(i)}$$

对每个 token 位置，比较 f16（无量化）和量化后的 next-token 概率分布。

### 3.2 TurboQuant 的 KL 散度结果

| Cache | Mean KLD | Δp RMS | Same top-p % |
|-------|----------|--------|-------------|
| q8_0 | 0.001549 | 1.23% | 98.43% |
| turbo4 | 0.009633 | 2.71% | 95.98% |
| q4_0 | 0.008091 | 2.75% | 95.83% |
| turbo3 | 0.016145 | 4.09% | 94.31% |

### 3.3 怎么读这些数字？

```
KLD = 0.001549 (q8_0)
  → 概率分布几乎没变

KLD = 0.016145 (turbo3)
  → 概率分布有轻微偏移
  → 但 94.31% 的时间 top token 仍然一致

Same top-p % = 95.98% (turbo4)
  → 100 次预测中，约 96 次选出的最优 token 与 f16 一致
  → 只有 4 次选了不同的 token
```

### 3.4 PPL vs KL 散度

| 指标 | 衡量什么 | 优点 | 缺点 |
|------|----------|------|------|
| PPL | 模型整体预测能力 | 端到端，最终指标 | 不知道哪里出了问题 |
| KL 散度 | 每个位置的概率偏移 | 精细，可定位问题 | 不直接对应用户体验 |

两个指标互补：PPL 是"最终成绩"，KL 散度是"诊断工具"。

---

## 4. NIAH（Needle In A Haystack）检索测试

### 4.1 什么是 NIAH？

测试 LLM 在长上下文中检索特定信息的能力。

```
方法：
1. 准备一段很长的"干草"（无关文本，如 Paul Graham 的文章）
2. 在某个位置插入一个"针"（如 "The best thing to do in San Francisco is eat a sandwich"）
3. 在最后问模型："The best thing to do in San Francisco is...?"
4. 检查模型能否正确回答

变量：
- 上下文长度：4K, 8K, 16K, 32K
- 针的位置（depth）：0%, 25%, 50%, 75%, 100%
```

### 4.2 为什么 NIAH 重要？

PPL 衡量的是"平均预测能力"，但 KV cache 压缩可能导致**特定位置的信息丢失**。NIAH 直接测试这一点。

### 4.3 TurboQuant 的 NIAH 结果

```
Single needle (9 positions):
  q8_0:                7/9 (77.8%)
  turbo3:              7/9 (77.8%)
  turbo3 + sparse V:   9/9 (100%)  ← 有意思！

Multi-key + 3 distractors (32K):
  q8_0:   100%
  turbo3: 100%
```

**关键发现：** 量化没有系统性地损害检索能力。turbo3 + sparse V 甚至更好（可能因为去除了低权重位置的量化噪声）。

---

## 5. Sparse V 的质量验证

Sparse V 是一个独立的优化：跳过 softmax attention weight < 1e-6 的位置的 V 反量化。

验证方法：PPL ON/OFF 对比。

```
50 chunks × 32K context on wikitext-103:

turbo3 WITHOUT sparse V: PPL = 7.1796
turbo3 WITH sparse V:    PPL = 7.1796
差异:                     0.0000 ← 精确为零！

CI ±0.021 → 在统计上确认无影响
```

这证明那些被跳过的位置确实"没有贡献"——它们的 attention weight 是因为 softmax 归一化而非零的噪声。

---

## 6. 评估方法论小结

| 指标 | 用途 | TurboQuant 中的阈值 |
|------|------|---------------------|
| PPL（Perplexity） | 整体语言建模质量 | < +3% vs q8_0 可接受 |
| KL 散度 | 概率分布偏移 | < 0.02 可接受 |
| Same top-p % | Top token 一致性 | > 94% 可接受 |
| NIAH 通过率 | 长上下文检索能力 | 100% 或接近 |
| MSE | 向量重建误差 | 越低越好（用于调参） |
| Cosine Similarity | 方向保持度 | > 0.9 可接受 |

---

## 关键要点总结

1. **PPL 是核心指标**：越低越好，衡量模型预测下一个 token 的"困惑度"
2. **< 1% PPL 劣化在实际使用中不可感知**（turbo4 的 +0.23%）
3. **KL 散度是诊断工具**，PPL 是最终指标，两者互补
4. **NIAH 检验检索能力**，确保压缩不丢失关键信息
5. **统计严格性很重要**：需要足够的 chunks、CI 置信区间

---

## 相关笔记

- [[TurboQuant 实际实现详解]] — PPL 数据的来源
- [[BLEU Score]] — 另一种评估指标（翻译任务）
- [[KV Cache 详解 - 李宏毅]] — 理解 KV Cache 压缩的动机

---

*PPL 的直觉：一个 PPL=6 的模型，平均每个位置在 6 个候选 token 中"犹豫"。*
