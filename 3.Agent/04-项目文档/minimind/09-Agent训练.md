---
title: MiniMind — Agent 强化学习训练（多轮工具调用）
tags:
  - minimind
  - agent
  - tool-calling
  - reinforcement-learning
---

# Agent RL：多轮工具调用能力

`train_agent.py` 将 **多轮工具调用（tool calling）** 建模为可 roll out 的交互过程，并用 **强化学习（与 GRPO 同族）** 优化策略：模型学会在需要时发出 `<tool_call>`、读取 `<tool_response>`、再续写，直到给出最终答案。

---

## 训练目标与数据形态

- **目标**：在 **模拟环境** 中学会 **正确次数 / 正确参数 / 最终答案含 ground truth** 的多轮行为，而非依赖真实外部 API。
- **数据集**：`AgentRLDataset`，每条样本通常包含：
  - **`conversations`**：对话消息列表，并带 **`tools`** 字段（可供模型理解的工具 schema / 说明）。
  - **`gt`**：**ground truth** 列表（数值或字符串等），用于奖励中的「答案是否命中 GT」校验。

---

## 模拟工具与环境

共 **6 种模拟工具**（名称与职责一一对应）：

| 工具 | 用途（直觉） |
|------|----------------|
| `calculate_math` | 数学表达式计算 |
| `unit_converter` | 单位换算 |
| `get_current_weather` | 当前天气查询 |
| `get_current_time` | 当前时间查询 |
| `get_exchange_rate` | 汇率查询 |
| `translate_text` | 文本翻译 |

**模拟执行环境**：各工具返回来自 **mock 表** 的固定或查表式结果（如 `WEATHER_DATA`、`TIME_DATA` 等），**无需真实网络/API**，保证训练可复现、成本低。

---

## 多轮 Rollout：`rollout_single`

单条样本的交互 rollout 可概括为「生成 → 解析工具 → 执行 → 拼观察 → 再生成」，循环直至结束或达到轮数上限。

1. **生成**：模型自回归生成当前轮回复。
2. **解析**：从文本中解析 `<tool_call> ... </tool_call>`（若存在）。
3. **执行**：在 mock 环境执行对应工具，得到结构化或文本结果。
4. **拼接观察**：将工具输出包装为 `<tool_response>...</tool_response>`（或项目约定等价形式）拼回上下文，**继续下一轮生成**。
5. **`max_turns=3`**：最多 **3 轮**上述循环，防止无限对话。

### 张量与 mask 约定（用于 PPO/GRPO 类 loss）

- **`prompt_ids`**：通常 **只记录第一轮** 的 prompt token（起点固定，便于对齐「同一题」的组内比较）。
- **`response_ids`**：**跨所有轮** 拼接的「模型生成 + 工具响应观察」序列（生成片段与观察片段按时间顺序交错出现）。
- **`response_mask`**：
  - 模型 **自主生成** 的位置 → **1**（参与 policy loss）。
  - **工具响应 / 环境观察** 注入的 token → **0**（**不对观察算 loss**，避免把环境当 policy 梯度对象）。
- **`response_old_logps`**：
  - 生成位置：记录采样时的 **真实 logprob**。
  - 观察位置：填 **0**（与 mask 配合，保证旧策略统计与 loss 聚合一致）。

---

## Reward：`calculate_rewards`

奖励分 **「无工具调用」** 与 **「有工具调用」** 两条主逻辑，并最终 **clip 到 \([-3.0, 3.0]\)**。

### 无工具调用时

综合 **长度奖励**、**思考奖励**（鼓励适度推理/结构化思考）、**RM 打分**（`train_agent.py` 会加载 `LMForRewardModel`，仅在本分支传入 `get_score`），以及 **重复惩罚**（抑制复读、模板化刷屏等）。

### 有工具调用时

典型项包括：

- **工具对齐分**（与源码 `tool_gap` 一致）：`valid_call_count` 统计 **工具名在样本 `tools` schema 内且 `CHECK_ARGS` 校验通过** 的调用次数；再令  
  \(\text{tool\_gap} = |\text{valid\_call\_count} - \text{len}(gt)| + \max(0, \text{len}(\text{tool\_calls}) - \text{valid\_call\_count})\)（同时惩罚「与 GT 条数不一致」与「多余/非法调用」）。  
  - **`tool_gap == 0`**：**+0.5**  
  - 否则：**\(-0.5 \times \text{tool\_gap}\)**
- **参数校验**：`CHECK_ARGS` 对每个被调用工具检查 **必要参数是否齐全、类型/范围是否合理**。
- **GT 文本验证**：`validate_gt_in_text` 在 **最终回答文本**（有工具链时取最后一轮去掉 `</think>` 后的文本）上校验：  
  - **字符串 GT**：**大小写不敏感**子串匹配（`lower()`）；  
  - **数值 GT**：从文本抽取数字后与 GT 比较差值 **\(< 10^{-6}\)**（并处理逗号分隔）。
- **GT 分**：**\(2.5 \times \frac{|\text{verified}|}{\text{len}(gt)}\)**（`gt` 非空时按命中比例计分）。
- **未完成惩罚**：若 **用尽 `max_turns` 仍未完成**（例如仍未产出合格最终答案）：**-0.5**。
- **标签闭合扣分**：对每个 **turn** 的作答字符串 `s`，累加 `abs(s.count("<tool_call>") - s.count("</tool_call>"))`，再执行 **`reward -= 0.5 *` 上述各 turn 之和**。

---

## Loss 与默认超参

- **Loss**：与 **GRPO** 同族流程；实现上可在 **CISPO / GRPO** 等变体间切换（组内归一化 advantage、按 token 聚合 KL/clip 项等，与 `train_grpo.py` 思路一致）。
- **默认超参（常见配置）**：
  - `num_generations=4`（每组采样条数）
  - `max_gen_len=768`（单段生成长度上限）
  - `max_total_len=2500`（整段上下文总长控制）
  - `thinking_ratio=0.1`：每步 rollout 以该概率令 `open_thinking=True` 传入 `apply_chat_template`（`random.random() < thinking_ratio`）。**默认 0.1** 明显低于 `train_grpo.py` / `train_ppo.py` 里数据集侧的 **0.9**，Agent 侧更少强制长思考格式。
  - `loss_type` 默认 **`"cispo"`**（可选 `"grpo"`，与 CLI `choices` 一致）

---

## 小结

Agent 训练把 **工具生态** 收束到 **可 mock 的封闭环境**，用 **多轮 rollout + 只对生成算 loss** 的方式稳定优化；奖励同时约束 **调用次数、参数合法性、最终答案是否命中 GT**，并用 **clip** 控制极端梯度信号。
