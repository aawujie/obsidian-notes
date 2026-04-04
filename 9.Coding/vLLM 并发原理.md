# vLLM 并发原理

> 核心思想：把操作系统的虚拟内存分页思想搬到 GPU 推理上

---

## 核心机制

### 1. Continuous Batching（连续批处理）

**传统批处理的问题**：
- "等齐了再跑"——一批请求必须全部完成才能处理下一批
- 快请求等慢请求，GPU 空闲浪费

**vLLM 的方案**：
- **请求随时加入/离开**：每个请求的 token 生成速度不同，动态调整 batch 大小
- **细粒度调度**：以 token 为单位调度，某个请求生成完 EOS 就立刻腾出位置给新请求
- **GPU 利用率最大化**：没有"空等"的浪费

---

### 2. PagedAttention（分页注意力）⭐

**传统 Attention 的问题**：
- 需要为每个序列预分配**连续**的 KV Cache
- 内存碎片严重
- 无法动态扩展
- batch 大小受限

**vLLM 的解决方案**：

| 概念 | 说明 |
|------|------|
| **Block** | KV Cache 分成固定大小的块（如 16 个 token 一块） |
| **非连续存储** | 每个序列的 block 可以分散在显存中 |
| **页表（Block Table）** | 记录逻辑 token → 物理 block 的映射关系 |
| **动态分配** | 需要时再分配新 block，用完释放 |

**效果**：
- 显存利用率提升 **60-80%**
- 支持更大的 batch 和更长的上下文
- 内存浪费极少（仅最后一块可能有少量碎片）

---

## 架构设计

```
请求队列 → Scheduler (CPU) → Worker (GPU)
              ↓
        维护 block table
```

- **Scheduler**：CPU 上运行，决定每个 iteration 哪些请求参与 forward
- **Worker**：负责实际的 GPU 计算
- **异步调度**：CPU 调度下一批时，GPU 在跑当前批

---

## 实际表现

### 优势
- **吞吐量优先**：适合高并发、多用户场景
- **多 LoRA 支持**：不同请求可用不同 LoRA adapter，共享基座模型
- **长上下文友好**：分页机制让长序列不再"吃光"显存

### 调优参数
- `max_num_batched_tokens`：控制每批最大 token 数（延迟敏感场景可调小）
- `block_size`：block 大小（默认 16）
- `gpu_memory_utilization`：显存占用比例（默认 0.9）

---

## 一句话总结

> vLLM 用 **"分页内存管理 + 动态批处理"** 把显存利用率和 GPU 吞吐量都拉满了，本质是把操作系统的虚拟内存思想搬到了 GPU 推理上。

---

## 参考资料

- vLLM 论文：[Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180)
- GitHub: https://github.com/vllm-project/vllm

---

**创建时间**:: 2026-04-04
**标签**:: #AI #大模型 #推理优化 #vLLM #部署
