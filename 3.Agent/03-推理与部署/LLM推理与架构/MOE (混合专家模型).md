# MoE（混合专家模型）

> 创建日期：2026-03-29
> 状态：了解概念即可，深入学习见文末待办

---

## 是什么

MoE = Mixture of Experts，混合专家模型。

核心思路：**不是每次都用全部参数，而是每个 token 只激活其中一部分"专家"**。

```
Dense 模型：每个 token 经过全部参数
MoE 模型：每个 token 只经过 top-k 个专家

Mixtral 8x7B：
  总参数 = 47B
  每次激活 = 2 个专家 ≈ 13B 的计算量
  → 花 13B 的钱，享受 47B 的容量
```

---

## 架构结构

```
输入 token
    ↓
Router（Gate 网络）
    ↓ 打分，选 top-k 专家
Expert 1  Expert 2  ... Expert N
    ↓ 只有被选中的专家参与计算
加权求和输出
    ↓
下一层
```

每一个 FFN 层都替换成 MoE 层，Attention 层保持不变。

---

## 为什么要 MoE

| 对比 | Dense 7B | MoE 47B（激活13B）|
|------|----------|-------------------|
| 计算量 | 7B | ≈13B |
| 模型容量 | 7B | 47B |
| 效果 | 一般 | 好得多 |
| 显存 | 14GB | 94GB（全部要加载）|

**核心优势**：用接近的计算量，存储更多知识。

---

## 主要难点

### 1. Expert Collapse（专家塌缩）
```
某个专家稍强 → Gate 更多选它 → 它更强 → 其他专家废了
```
解法：auxiliary loss 强制负载均衡

### 2. 负载不均衡
某些专家永远很忙，某些永远空闲。
GPU 要等最慢的专家 → 计算效率低。

### 3. 分布式通信开销
专家分散在不同 GPU，token 要跨卡传输（All-to-All）。
大规模时通信占总时间 30%+。

### 4. 显存占用高
计算量是 13B，但 47B 参数全要加载到显存。
部署成本远高于同等算力的 Dense 模型。

### 5. 上下文断裂
同一句话的 token 被发到不同专家，专家看不到邻居 token。

---

## 代表模型

| 模型 | 专家数 | 激活专家 | 总参数 | 特点 |
|------|--------|---------|--------|------|
| Mixtral 8x7B | 8 | 2 | 47B | 开源，效果好 |
| DeepSeek-V2/V3 | 64（细粒度）| 6+2共享 | 236B | 共享专家创新 |
| Qwen MoE | 64 | 8 | — | 阿里系 |
| GPT-4 | 未公开 | 未公开 | 未公开 | 据传是 MoE |

---

## DeepSeek 的创新

DeepSeek 引入了两个改进：

1. **共享专家**：每个 token 都经过的专家（解决上下文断裂）
2. **细粒度专家**：用 64 个小专家代替 8 个大专家（提升专业化）

```
普通 MoE：8 个专家，选 2 个
DeepSeek：64 个小专家 + 2 个共享专家，选 6+2 个
```

---

## 和普通 Transformer 的关系

```
Transformer = Attention + FFN
MoE Transformer = Attention + MoE（FFN × N + Router）

其他都一样，只是把 FFN 层换成了 MoE 层。
```

所以 **Transformer 原理搞懂了，MoE 只是 FFN 的升级版**。

---

## 一句话总结

> MoE = 多个 FFN 专家 + 一个路由器，每次只激活少数专家。
> 用接近的计算量，撑起更大的模型容量。

---

## ☑️ 待办：深入学习路径

> 现阶段了解概念即可，按以下顺序学完再回来深入。

```
[ ] Week 1-2：HuggingFace 实战（情感分析项目）← 你在这里
[ ] Week 3-4：LoRA/QLoRA 微调中文大模型
[ ] Week 5-6：RAG 问答系统
[ ] Week 7-8：模型部署（FastAPI + vLLM）
      ↓ 完成后
[ ] 深入 MoE Step 1：读 Switch Transformer 论文（2021，Google）
[ ] 深入 MoE Step 2：读 Mixtral 技术报告
[ ] 深入 MoE Step 3：读 DeepSeek-V2 论文（共享专家 + 细粒度）
[ ] 深入 MoE Step 4：跑一个 Mixtral 推理，感受显存占用
[ ] 深入 MoE Step 5：尝试 MoE 模型的 LoRA 微调
```

**推荐论文顺序：**
1. `Switch Transformer`（2021）— 最简洁的 MoE 入门
2. `Mixtral of Experts`（2024）— 开源 MoE 标杆
3. `DeepSeek-V2`（2024）— 最有创新的 MoE 设计

---

## 相关笔记

- [[Transformer架构从零理解]] — MoE 的基础
- [[Position-wise FFN]] — MoE 替换的就是这一层
- [[LoRA微调原理]] — 将来 MoE 微调用得上
