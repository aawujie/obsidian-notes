---
title: GPT-2到KimiK3架构演进
type: 笔记
created: 2026-07-29
updated: 2026-07-29
sources:
  - https://x.com/waterloo_intern/status/2081762065392541951
tags:
  - LLM
  - architecture
  - attention
  - KimiK3
  - transformer
---

# GPT-2到KimiK3：七年架构演进

> 原文：*22580: From GPT2 to Kimi3, Explained* — @waterloo_intern (ali)
> 核心论点：KimiK3 参数量是 GPT-2 的 22,580 倍，但每一代架构变化都在解决上一代的具体缺陷，不是盲目堆参数。

---

## 演进链条

```
GPT-2 (2019)
  → Linear Attention
    → DeltaNet
      → Gated DeltaNet
        → Kimi Linear (KDA)
          → KimiK3 (2026)
```

---

## 1. GPT-2 → Linear Attention

**GPT-2 瓶颈**：KV cache 随序列长度 $O(N)$ 线性增长，memory bandwidth 成瓶颈。

**Linear Attention 解法**：用 ELU+1 替换 softmax 中的指数运算，将 QK 乘积变成可重新结合的形式，把 cache 压缩为固定大小的 $D \times D$ 状态矩阵。

**代价**：ELU+1 是 softmax 核的近似，表达能力下降。

---

## 2. Linear Attention → DeltaNet

**问题**：固定 size 的 cache 写满后，新信息与旧信息互相干扰（purely additive，旧数据永不离开 cache）。

**DeltaNet 解法（Delta Rule）**：
- 写入前先查出当前 cache 对应位置的旧信息
- 计算差值，用差值更新
- 实现精准覆写而非叠加

**训练并行化**：chunk-wise 分块 → within-chunk 做标准 attention，across-chunk 走 recurrent state。$C=1$ FLOPs 最少，$C=64/128$ 硬件效率最高。

---

## 3. DeltaNet → Gated DeltaNet

**问题**：Delta Rule 能精准覆写单条，但没法批量清理（context switch 无效）。

**Gated DeltaNet 解法**：
- 引入 Mamba 的门控衰减参数 $\alpha$
- 对 cache 做整体衰减后写入新信息
- 融合 Delta Rule + Mamba 门控

---

## 4. Gated DeltaNet → Kimi Linear (KDA)

**核心改进**：单一标量 $\alpha$ → per-channel 细粒度 $\alpha$，每个维度独立控制衰减。

**效果**：受控对比下超越 full attention，decode 吞吐提升最多 6x。

---

## 5. Kimi Linear → KimiK3

整体结构：**23 个四层 macrocycle**，每个 macrocycle 3 层 KDA + 1 层 MLA。

### 新增特性

| 特性 | 作用 |
|:---|:---|
| **Gated MLA** | 门控控制 MLA 输出进入 residual stream 的比例 |
| **Latent MoE** | 898 expert（2 shared + 896 routed），每 token 选 16；在 latent space 运算，FLOPs 减半 |
| **SiTU 激活** | 替换 SiLU；但无 fused kernel 时裸跑慢 3x |
| **AttnRes** | 每 12 层插入 blockwise attention residual |

### AttnRes 详解

核心公式：

$$h_l = \alpha_0 \cdot h_1 + \sum_{i=1}^{l-1} \alpha_i \cdot f_i(h_i)$$

- 每层不是简单叠加所有前层输出，而是通过学习到的 query-key dot product 给每层输出加权
- 每 12 个 decoder layer 打包成一个 block，只对 block 边界做 AttnRes
- 效果：缓解 residual dilution，约 1.25x 算力优势，约 2% 推理延迟增加

---

## 总结

> 固定容量的联想记忆（$D \times D$ 状态矩阵）必须有淘汰策略。纯加法线性操作在容量满后必然引入干扰，所以需要门控/路由/衰减这类学习式选择机制，而 **attention 是最高效的选择性读取手段**。

KimiK3 的核心不是 scale，是每代架构都在**给 capacity 赋予明确的功能角色**——KDA 做常驻 recurrent memory，MLA 做定期 softmax 检索，MoE 做稀疏专家容量，AttnRes 做跨层选择性访问。
