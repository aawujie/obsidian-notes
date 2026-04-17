---
title: MiniMind — Tokenizer 与数据处理
tags:
  - minimind
  - tokenizer
  - dataset
  - data-processing
---

# Tokenizer 与数据处理

本文梳理 MiniMind 中 **Tokenizer 训练**（`train_tokenizer.py`）与 **语言建模数据集**（`lm_dataset.py`）的设计，以及对话数据的预处理技巧。

---

## Tokenizer 训练（`train_tokenizer.py`）

### BPE 与词表规模

- 使用 **Byte Pair Encoding (BPE)**，基于 Hugging Face **`tokenizers`** 库构建与训练。
- 目标词表大小 **`vocab_size = 6400`**，在极小模型场景下兼顾表达能力与嵌入/输出层参数量。

### 特殊 Token 设计

| 语义        | Token 字符串     | 典型用途              |
| --------- | ------------- | ----------------- |
| 序列开始（BOS） | `<im_start>`  | 对话/片段起始           |
| 序列结束（EOS） | `<im_end>`    | 轮次或整段结束           |
| 填充（PAD）   | `<endoftext>` | 对齐 batch 长度时的 pad |

> 命名风格贴近 **Qwen / ChatML** 生态，便于复用既有模板与习惯。

### 工具调用（Tool Calling）相关 Token

为 Agent / 函数调用场景预留显式边界：

- `<tool_call>` … `</tool_call>`
- `<tool_response>` … `</tool_response>`

便于在序列中区分「模型发起的工具调用」与「环境返回的工具结果」，后续在 Chat Template 或监督信号中可对齐解析。

### 思考（Thinking）相关 Token

- `<think>` … `</think>`（`lm_dataset.post_processing_chat` 删除的空思考块即该标签对；与 Chat 模板里 reasoning 占位写法一致）

用于链式推理或 RL 中「可开关的思考段」；与数据后处理（见下文）配合，可控制空思考占位对训练的影响。

### 预留 Buffer Token

词表中为将来扩展（新特殊符号、新角色标记、新协议字段等）**预留 buffer**，减少「线上新增 token 必须重训 tokenizer」的摩擦。具体数量与命名以仓库实现为准。

### Chat Template（Jinja2）

- 使用 **Jinja2** 模板，格式上 **兼容 Qwen 系 Chat 模板** 的常见字段与角色标签。
- 支持在模板中编排 **tools** 与 **thinking** 段落，使同一份 tokenizer + template 可覆盖：纯对话 SFT、带工具监督、带思考段等数据形态。

### 压缩率测试

训练或合并词表后，建议用 **中英文混合** 的代表性样本统计：

- 字符数 / UTF-8 字节数 vs token 数；
- 与目标 `max_seq_len`、数据管线成本（IO、padding 比例）联合评估。

---

## 五种 `Dataset` 类（`lm_dataset.py`）

### 1. `PretrainDataset`

| 项目 | 说明 |
|------|------|
| 数据格式 | **JSONL**，每行含 **`text`** 字段 |
| 正文截断 | `tokenizer(..., add_special_tokens=False, max_length=max_length-2, truncation=True)`，为 **BOS + EOS** 各预留 1 个位置 |
| 拼接规则 | 序列级 **`[bos_id] + tokens + [eos_id]`**，再 **pad** 到 **`max_length`** |
| Padding | 右侧用 **`pad_token_id`** 填充到 **`max_length`** |
| Labels | `labels = input_ids.clone()`，再将 **pad 位置**置为 **`-100`**（与 `CrossEntropyLoss(ignore_index=-100)` 一致） |

适用于 **自回归预训练**（Next Token Prediction）。

### 2. `SFTDataset`

| 项目 | 说明 |
|------|------|
| 数据格式 | **`conversations`** 列表（多轮角色消息） |
| 模板 | 对整条对话 **`apply_chat_template`** |
| 边界 token | `bos_id = tokenizer(f'{tokenizer.bos_token}assistant\n', add_special_tokens=False).input_ids`，`eos_id = tokenizer(f'{tokenizer.eos_token}\n', add_special_tokens=False).input_ids`（与 ChatML 模板中 assistant 段起止一致） |
| Loss 范围 | **`generate_labels`**：在整段 `input_ids` 上扫描上述片段，仅 **assistant 回复** 区间 `labels[j]=input_ids[j]`，其余为 **`-100`** |

实现「**只对模型该说的部分学梯度**」，抑制对 system/user 的过拟合。

### 3. `DPODataset`

| 项目 | 说明 |
|------|------|
| 数据格式 | 偏好对：**`chosen` / `rejected`** |
| 模板 | 两侧各为完整对话列表，分别 **`apply_chat_template`** |
| Mask | **`generate_loss_mask`** 标记 **assistant 回复区域**，DPO 中仅在该区域累计 log prob / 相关统计 |

与 DPO 损失「在回答片段上比较策略与参考模型」一致。

### 4. `RLAIFDataset`

| 项目 | 说明 |
|------|------|
| 用途 | **PPO / GRPO** 等在线或伪在线 RL 管线 |
| 返回内容 | **只返回 prompt**（不含最后一轮 **assistant** 完成内容） |
| Thinking | `thinking_ratio` 默认 **0.5**：`use_thinking = random.random() < thinking_ratio`，`apply_chat_template(..., open_thinking=use_thinking, add_generation_prompt=True)` |

### 5. `AgentRLDataset`

| 项目  | 说明                                                                             |
| --- | ------------------------------------------------------------------------------ |
| 用途  | **Agent RL**（工具、环境交互）                                                          |
| 解析  | 从 **`conversations`** 中解析 **tools** 与 **gt**（ground truth）等字段，供环境 step 或奖励设计使用 |

---

## 数据预处理技巧

### `pre_processing_chat`

- 仅当 **`conversations[0].role != 'system'`** 且 **`random.random() < add_system_ratio`**（默认 **0.2**，即 20%）时，在列表头部插入一条随机 **system**（**中英文混合** 模板池）；若首条已是 **system** 或任一轮含 **`tools`** 字段则**不插入**（含 tools 时整段 `conversations` 原样返回）。

### `post_processing_chat`

- 参数 **`empty_think_ratio=0.2`**：当 `random.random() > empty_think_ratio` 时（约 **80%**）执行替换。
- 删除的子串与源码完全一致：`'<think>\n\n</think>\n\n'`（先 `in` 检测再 `replace(..., '')`），用于去掉模板生成的**空思考占位**；`pre_processing_chat` 在 **`any(conv.get('tools') for conv in conversations)`** 时对整条 `conversations` **原样返回**（不做 system 增广）；`post_processing_chat` 作用于已渲染的 **prompt 字符串**，与是否含 tools 无额外短路（但若上游未生成该子串则不会命中）。

避免无信息思考段占用上下文、扭曲长度分布或干扰 RL/SFT 的有效信号。

---

## 小结

- **Tokenizer**：6400 BPE + Qwen 风格特殊符号 + tool/thinking token + buffer，Jinja2 Chat Template 统一多任务格式。
- **Dataset**：从纯文本预训练到 SFT、DPO、RLAIF、Agent RL，通过 **template + label/mask** 精确控制 **loss 作用区间**。
- **预处理**：system 增广与空思考清洗，改善数据质量与训练稳定性。

---

## 相关笔记

- [[00-项目总览]]（若已建立）
- [[03-预训练]]
- [[04-SFT微调]]
- [[05-对齐训练-DPO]]
