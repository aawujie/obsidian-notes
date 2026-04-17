---
title: MiniMind — SFT 微调（全参 / LoRA）
tags:
  - minimind
  - SFT
  - LoRA
  - fine-tuning
---

# SFT 微调

监督微调（SFT）在预训练权重上，用对话或指令数据对齐「聊天形态」与任务行为。MiniMind 提供 **全参数 SFT**（`train_full_sft.py`）与 **手写 LoRA**（`train_lora.py` + `model_lora.py`）两条路径。

---

## Full SFT（`train_full_sft.py`）

### 初始化与数据

| 项目 | 说明 |
|------|------|
| 初始化权重 | 基于 **预训练 checkpoint** |
| 数据文件（要点） | `sft_t2t_mini.jsonl` |
| 格式 | **`conversations`** 多轮结构 |

### 默认超参数（要点）

| 超参数 | 典型取值 |
|--------|----------|
| `from_weight` | **`pretrain`**（全参 SFT 默认从预训练权重起训） |
| `batch_size` | **16** |
| `learning_rate` | **1e-5** |
| `max_seq_len` | **768** |
| `accumulation_steps` | **1** |
| `epochs` | **2**（`argparse` 默认） |

### Loss Mask（只对 assistant 计算 loss）

`generate_labels` 的核心思想：

1. 对整段应用 chat template 后得到 token 序列与 labels 初值。
2. 将 **非 assistant 回复区域** 的 label 置为 **`-100`**（与 `CrossEntropyLoss(ignore_index=-100)` 配合）。
3. **assistant 段** 由 `SFTDataset` 用 **与 tokenizer 绑定的片段** 定位：`{tokenizer.bos_token}assistant\n` 作为段起点、`{tokenizer.eos_token}\n` 作为段结束标记（见 `lm_dataset.py` 中 `bos_id` / `eos_id` 与 `generate_labels`），仅在该区间内把 **label 设为对应 `input_ids`**，其余位置为 **`-100`**。

效果：**system / user / 工具占位** 等不参与梯度，模型主要学习「如何接话」。

### 训练循环

要点：**与预训练脚本在训练循环层面完全一致**（AMP、裁剪、调度、DDP、checkpoint 等复用同一套工程模式），差异集中在 **Dataset 与 label 生成**。

---

## LoRA 微调（`train_lora.py` + `model_lora.py`）

### 设计取向

- **不依赖 PEFT**：LoRA 层与注入逻辑 **纯手写**，便于阅读、裁剪与在极简仓库中离线运行。

### `LoRA` 模块

| 矩阵 | 形状直觉 | 初始化 |
|------|----------|--------|
| **A** | `in_features → rank` | 高斯噪声，**`std = 0.02`** |
| **B** | `rank → out_features` | **全零** |

训练初期 **`B @ A ≈ 0`**，前向近似等于原模型，优化过程平滑。

### `apply_lora` 注入规则

- 对 **`nn.Linear`** 且权重为 **方阵**（**`weight.shape[0] == weight.shape[1]`**）的层动态挂载 LoRA。
- 目的：在典型 Transformer 中主要覆盖 **自注意力 q/k/v/o 及 MLP 中方形投影**（具体以代码中的过滤条件为准）。

### Monkey-patch 前向

对目标层的 `forward` 做包装：

```text
output = original_forward(x) + lora(x)
```

即在原输出上 **加性** 叠加低秩修正。

### 参数冻结与保存

| 项目 | 说明 |
|------|------|
| 优化 | **冻结非 LoRA 参数**，优化器只包含 LoRA 相关参数 |
| `save_lora` | 仅保存 **参数名含 `'lora'`** 的 state，且 **`half()`** 降低体积 |
| `load_lora` / `merge_lora` | 将 LoRA 权重加载回基座；`merge_lora` 将低秩更新 **合并进原 Linear** 便于推理部署 |

### 默认超参数（要点）

| 超参数 | 典型取值 |
|--------|----------|
| `from_weight` | **`full_sft`**（LoRA 默认基座；与全参 SFT 的 `pretrain` 不同） |
| `lora_name` | **`lora_medical`**（保存前缀 / checkpoint 名） |
| `learning_rate` | **1e-4** |
| `rank` | **16**（`apply_lora(..., rank=16)` 默认） |
| `epochs` | **10** |
| `batch_size` | **32** |
| `max_seq_len` | **340** |
| `accumulation_steps` | **1** |

### 与 `torch.compile` 的兼容性

- **Monkey-patch 与 `torch.compile` 不兼容**（图捕获与动态替换 forward 易冲突）。
- `train_lora.py` 在 **`--use_compile 1`** 时会 **强制改回 0** 并打日志（`monkey-patch forward 与 torch.compile 不兼容，use_compile 已自动关闭`），避免图捕获与动态替换 `forward` 冲突。

---

## Full SFT vs LoRA（选型简表）

| 维度 | Full SFT | LoRA |
|------|----------|------|
| 可训练参数量 | 全模型 | 仅低秩分支 |
| 显存 / 吞吐 | 更高 | 相对较低 |
| 上限 | 分布大改时更灵活 | rank 与注入层限制表达力 |
| compile | 可按环境开启 | 建议关闭 |

---

## 相关笔记

- [[02-Tokenizer与数据处理]]
- [[03-预训练]]
- [[05-对齐训练-DPO]]
