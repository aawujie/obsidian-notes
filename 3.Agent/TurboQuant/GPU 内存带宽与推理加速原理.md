# GPU 内存带宽与推理加速原理

> **目的：** 理解为什么压缩 KV Cache 能加速推理（不仅仅是省内存）
> **前置知识：** LLM 推理基础（Prefill/Decode）、KV Cache 概念
> **创建日期：** 2026-04-02

---

## 1. LLM 推理的两个瓶颈

### 1.1 计算瓶颈（Compute-bound）

GPU 的算力不够用。

```
典型场景：Prefill 阶段
  - 同时处理大量 token
  - 矩阵乘法密集
  - GPU 核心满载
  - 瓶颈：FLOPS（每秒浮点运算次数）
```

### 1.2 内存带宽瓶颈（Memory-bound）

GPU 从显存读数据的速度不够快。

```
典型场景：Decode 阶段（逐 token 生成）
  - 每次只生成 1 个 token
  - 需要读取整个 KV Cache
  - 计算很简单（一个向量 × 矩阵）
  - 但数据量巨大
  - 瓶颈：内存带宽（GB/s）
```

---

## 2. 内存带宽：容易被忽略的瓶颈

### 2.1 内存带宽是什么？

GPU 显存（VRAM）到计算核心之间的数据传输速度。

```
类比：
  GPU 计算核心 = 工厂里的工人（很多很快）
  GPU 显存 = 仓库（很大）
  内存带宽 = 仓库到工厂的传送带速度

  如果传送带太慢，工人再多也没用——大家都在等材料
```

### 2.2 各硬件的内存带宽

| 硬件 | 显存 | 带宽 | 适合 |
|------|------|------|------|
| M2 Pro | 32 GB（统一） | 200 GB/s | 本地推理 |
| M5 Max | 128 GB（统一） | 546 GB/s | 大模型推理 |
| RTX 4090 | 24 GB GDDR6X | 1008 GB/s | 训练/推理 |
| A100 | 80 GB HBM2e | 2039 GB/s | 数据中心 |
| H100 | 80 GB HBM3 | 3352 GB/s | 数据中心 |

### 2.3 Decode 阶段的带宽计算

以 Qwen3.5-35B (MoE) 在 M5 Max 为例：

```
每次生成 1 个 token 需要读取：
  模型权重：~18 GB（Q4_K_M 量化后）
  KV Cache（32K context, q8_0）：
    46 layers × 32 heads × 32K tokens × 128 dim × 2 bytes × 2 (K+V)
    ≈ 18 GB

  总读取量 ≈ 36 GB

M5 Max 带宽：546 GB/s
理论最大 decode 速度：546 / 36 ≈ 15 tok/s

实际测量：~17 tok/s（接近理论极限！）
```

**关键认知：Decode 几乎是纯带宽瓶颈，GPU 大部分时间在"等数据"。**

---

## 3. 为什么压缩 KV Cache 能加速

### 3.1 减少读取量

```
q8_0 KV Cache（8-bit）：每个值 1 byte
turbo3 KV Cache（3.5-bit）：每个值 ~0.44 bytes

32K context 的 KV Cache：
  q8_0:   18 GB
  turbo3: ~8 GB  ← 减少了 10 GB！

每次 decode 总读取量：
  q8_0:   18 (权重) + 18 (KV) = 36 GB
  turbo3: 18 (权重) + 8 (KV) = 26 GB

理论加速：36/26 = 1.38x
```

### 3.2 但有反量化开销

读完压缩数据后，GPU 需要**解压缩**才能计算 attention。

```
q8_0 decode：
  读 KV → 直接计算 attention

turbo3 decode：
  读压缩 KV → 反量化（WHT + 查表）→ 计算 attention
                  ↑ 这步有额外计算开销
```

### 3.3 实际平衡

| 上下文长度 | 带宽节省 | 反量化开销 | 净效果 |
|-----------|----------|-----------|--------|
| 短（2K） | 小 | 相对大 | 略慢 |
| 中（8K） | 中 | 相对小 | 接近持平 |
| **长（32K+）** | **大** | **相对很小** | **加速** |

**上下文越长，KV Cache 在总读取量中的比例越大，压缩的加速效果越明显。**

```
turbo3 vs q8_0 prefill 速度：
  2K:  1.02x（基本相同）
  8K:  1.03x
  16K: 1.06x
  32K: 1.10x ← 上下文越长越快！
```

---

## 4. Apple Silicon 统一内存的特殊性

### 4.1 统一内存架构（UMA）

```
传统 GPU（Nvidia）：
  CPU 内存 ←→ PCIe 总线 ←→ GPU 显存
  数据需要来回拷贝

Apple Silicon（M1-M5）：
  CPU 和 GPU 共享同一块内存
  无需拷贝！
  但带宽较低（200-546 GB/s vs NVIDIA 的 1000+ GB/s）
```

### 4.2 对 TurboQuant 的意义

Apple Silicon 的带宽更宝贵（相对 NVIDIA 更低），所以 KV Cache 压缩的**相对收益更大**。

```
M5 Max：
  带宽 546 GB/s，总内存 128 GB
  可以跑 104B 模型（如 Command-R+），但带宽紧张
  turbo3 减少 KV Cache 读取量 → 直接加速 decode

NVIDIA RTX 4090：
  带宽 1008 GB/s，但显存只有 24 GB
  大模型根本放不下，压缩的意义主要是省内存
```

---

## 5. GPU 内存层次

GPU 有多层缓存，速度差异巨大：

```
                速度         大小
  寄存器        ~80 TB/s     ~20 KB / SM
  共享内存/L1   ~19 TB/s     ~100 KB / SM
  L2 缓存       ~6 TB/s      4-96 MB
  显存（HBM）   ~2 TB/s      24-80 GB
```

### 5.1 L2 缓存效应

TurboQuant 在 M1/M2（较小的 L2 缓存）上 turbo3 decode 明显变慢：

```
M1 Max 64GB：
  turbo3 decode: -37.9% vs q8_0  ← 灾难！
  turbo4 decode: +33.9% vs q8_0  ← 反而快了！
  
原因：turbo3 的 WHT 反量化代码复杂，导致 L2 缓存驱逐
      turbo4 用更简单的 nibble 直接提取，缓存友好

M5 Max 128GB：
  turbo3 decode: 0.90x q8_0  ← 可接受
  原因：M5 的 L2 缓存更大，能容纳反量化代码
```

**这就是为什么推荐在 pre-M5 硬件上用 turbo4 而非 turbo3。**

---

## 6. Sparse V：从带宽角度理解

### 6.1 问题

Decode 时，需要反量化**整个 KV Cache 的 V**，即使 softmax 给大部分位置的权重接近 0。

### 6.2 解法

```
传统 decode：
  V 反量化：[v1, v2, v3, v4, ..., v32000] 全部反量化
  attention：[0.8, 0.0001, 0.0000, 0.1999, ...] × V

Sparse V decode：
  检查 attention weight > 1e-6?
  V 反量化：[v1, -, -, v4, ...] 只反量化重要位置
  节省了约 50% 的反量化计算 + 对应的内存读取！
```

### 6.3 效果

```
32K context MoE 模型（attention 约占 30% decode 时间）：
  反量化节省约 50%
  attention 加速约 22.8%
  总 decode 加速约 7-8%

128 token 短上下文：
  attention 占比很小
  总加速仅 +0.7%
```

**Sparse V 的收益与上下文长度正相关——长上下文场景收益最大。**

---

## 7. 全局视图：为什么压缩有意义

```
                        短上下文 (2K)            长上下文 (32K)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
模型权重读取              18 GB                   18 GB
KV Cache 读取 (q8_0)     1.1 GB (6%)             18 GB (50%)
KV Cache 读取 (turbo3)   0.5 GB (3%)             8 GB (31%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
压缩节省                  0.6 GB (微不足道)        10 GB (显著！)
```

**结论：KV Cache 压缩是一个"上下文越长越值"的优化。**

在 128K context 的极端场景下（如 Command-R+ 104B），KV Cache 占总读取量的 80%+，压缩的加速效果最为显著。

---

## 关键要点总结

1. **Decode 是内存带宽瓶颈**：GPU 大部分时间在等数据，不是在计算
2. **压缩 KV Cache = 减少读取量 = 加速 decode**（前提是反量化开销可控）
3. **上下文越长，压缩收益越大**（因为 KV Cache 在总读取量中的占比增加）
4. **L2 缓存大小影响反量化性能**：复杂算法在小缓存硬件上可能反而更慢
5. **Apple Silicon UMA 带宽宝贵**：压缩的相对收益比 NVIDIA 更大

---

## 相关笔记

- [[TurboQuant 实际实现详解]] — 理解压缩管线
- [[Flash Attention 详解 - 李宏毅]] — 另一种带宽优化思路
- [[KV Cache 详解 - 李宏毅]] — KV Cache 的基础
- [[LLM 推理框架对比]] — 各框架如何处理推理优化

---

*Decode 的核心矛盾：读很多（整个 KV Cache），算很少（1 个 token 的 attention）。压缩直接缓解这个矛盾。*
