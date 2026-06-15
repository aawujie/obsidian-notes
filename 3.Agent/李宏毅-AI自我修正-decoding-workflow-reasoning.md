---
title: 李宏毅 - AI 自我修正：从 Decoding、Workflow 到 Reasoning
type: lecture-note
created: 2026-06-15
updated: 2026-06-15
sources:
  - https://youtu.be/m3i2mk5hs8U
tags:
  - AI
  - LLM
  - SelfCorrection
  - Reasoning
  - 李宏毅
share_link: https://share.note.sx/9a6i8fa6#gbHVghZOAIDx3Ui19A+N36zIokC7of2Jh9Eb0lHUA9Q
share_updated: 2026-06-15T17:01:38+08:00
---

# 李宏毅 — AI 能自我修正嗎？從 Decoding、Workflow 到 Reasoning

> **来源**：[YouTube](https://youtu.be/m3i2mk5hs8U) | **讲师**：李宏毅（Hung-yi Lee） | **时长**：87min

## 核心问题

语言模型能不能在**没有人类介入**的情况下，自己发现自己错了，自己修正自己的行为？

这是 2025 年机器学习第七讲（Reasoning）的延伸，讲一年后的新进展。

---

## 三大路线

| 路线                              | 方法         | 核心思路                           |
| :------------------------------ | :--------- | :----------------------------- |
| **① 修改 Inference 过程（Decoding）** | 不改参数，改生成过程 | 从 representation/logit 中提取错误信号 |
| **② 修改 Workflow**               | 不改参数，改工作流程 | 插入反思指令让模型自我反省                  |
| **③ 修改参数（Reasoning）**           | 直接训练模型     | RL / SFT 让模型学会何时该自我修正          |

---

## 一、Decoding 层面：从 Representation 中提取错误信号

### 1.1 Error Detection — 从 Representation 判断对错

**方法**：收集模型答对和答错时的 Representation，训练一个 Binary Classifier 来区分。

**关键发现**（2023年文献）：
- 真的能训练出 classifier，根据 Representation 预测答案是否正确
- 该 classifier 有泛化能力，训练在一堆问题上，可以预测另一堆问题的正确率
- **意味着**：正确/错误的信号已经编码在 Representation 中，我们只是需要知道怎么提取

### 1.2 Error Correction — TruthX（2024）

**方法**：
1. 收集答对时的 Representation（平均）和答错时的 Representation（平均）
2. 两者相减 → 得到「正确 vs 错误」的差距向量（黄色 vector）
3. 把差距向量**加到**本来会答错的 Representation 上
4. 模型就有可能给出正确答案

**局限**：需要收集额外数据（先问模型一堆问题，知道答对/答错的 Representation）

### 1.3 Contrastive Decoding — 无需额外数据

**核心思路**：每次生成 token 时，同时制造一个「大概率答错」的状态，把正常状态和错误状态的输出相减，远离错误答案。

**具体做法**：
- 正常输入 → 得到正常概率分布（蓝色）
- 对输入做修改 → 制造出大概率答错的状态 → 得到错误概率分布（绿色）
- 蓝色 - 绿色 × α → 得到修正后的分布（黄色）
- 每生成一个 token 都做一次这样的操作

**优点**：
- 不改模型参数
- 纯 Inference 阶段可以套用
- 不需要额外收集数据

**缺点**：
- 需要额外运算（每次 inference 都要再做一次制造错误状态的操作）

#### Contrastive Decoding 的早期版本（2022）

- 用大模型（GPT-2 large）的输出当「正常」，小模型（GPT-2 small）的输出当「错误」
- 两者相减 → 差距最大的 token 才是被 decode 出来的 token
- 例：「奥巴马出生在檀香山，他出生在哪一年？」 → 大模型答「檀香山」（错），小模型也答「檀香山」，但相减后最高概率变成 **1961**（正确）

#### DoLA — Decoding by Contrasting Layers（2023）

- 不用额外小模型，用同一模型**前面层**的输出当「错误状态」
- 基于 **Large Lens** 技术：把 LM Head 接到中间层也能 decode 出有意义的内容
  - 例：LLaMA2 把法文翻中文时，中间层 decode 出英文 → 说明模型内心先用英文思考
- 用最后一层的概率分布减去前面层的概率分布
- **优势**：不需要额外模型，前面层本来就要跑，overhead 很小
- 已集成到 HuggingFace Transformers 套件中

#### Layer Contrastive Decoding（2025）— 视觉领域应用

- 把 Contrastive Decoding 应用到视觉语言模型
- 用 Vision Encoder 前面层的输出 vs 最后层，做对比解码

---

## 二、Workflow 层面：插入反思指令

### 2.1 基本思路

不改参数，改模型的工作流程——在 prompt 中插入反思指令，让模型自己检查答案。

### 2.2 Self-Correction 的困境

**核心矛盾**：**顽固与接受批评是 trade-off**

| 性质 | 效果 |
|:---|:---|
| 顽固（高 confidence） | 不容易改错，但也不容易改对 |
| 容易接受批评（低 confidence） | 容易改错，但也容易把对的改掉 |

**实验发现**：
- 模型如果高概率修改自己的答案 → confidence level 就低 → 坚持不住正确答案
- 插入的反思指令会影响模型行为（即使指令是程序自动插入的）

**三种指令的效果**：

| 指令类型 | 内容 | 效果 |
|:---|:---|:---|
| 中性 | 「再做一次」 | 默认行为 |
| Confidence | 「你应该是对的，再给我一次答案」 | confidence ↑，变固执 |
| Quitting | 「你确定吗？最好再想一想」（暗示答案错了） | confidence ↓，更容易改答案 |

**结论**：
- 顽固模型 → 应该多批判它
- 缺乏信心模型 → 应该多肯定它
- 每个模型需要不同的反思指令 → 这就是文献上反思到底有没有用结论 mixed 的原因

### 2.3 Reflection 的算力经济学

**关键问题**：反思需要额外算力，这笔投资划算吗？

**对比实验**：
- 灰色线：majority vote（不反思，只多 sample 几次投票）
- 其他颜色线：加上反思（1次、2次、4次……32次）

**发现**：
- **按答案数量比较**（左图）：加上反思确实更好，甚至只用 1/4 的 sample 就得到同样正确率
- **按算力比较**（右图）：同样算力下，**不反思（majority vote）反而更好**

**结论**：
- Verification/Reflection 是**奢侈品**——在投入大量算力达到极限后，再做 verification 才能发挥作用
- 算力有限时 → 先多产生不同答案（majority vote），直到饱和后再加 reflection
- 要得到 3.8% 的进步，需要投入 **100倍以上**的运算资源

**教训**：提出新 workflow 时，必须和 majority vote 这个 baseline 比较，否则结论会被质疑

---

## 三、Reasoning 层面：直接修改参数让模型学会自我修正

### 3.1 从 Workflow 到 Reasoning

| 区别 | Workflow | Reasoning |
|:---|:---|:---|
| 反思触发 | 硬插入额外指令 | 模型自己学会何时该反思 |
| 资源浪费 | 不管答案对错都要反思 | 答案对了就不反思，错了才反思 |
| 智能 | 较低 | 较高——知道何时该改何时不该改 |

### 3.2 正确知识 ≠ 自我修正能力

**反直觉发现**（2024论文）：
- 模型明明有正确知识，却不会自我修正
- 例：问「告诉我一个出生在纽约的政治家」 → 模型答「希拉蕊」（错，她出生在芝加哥）
- 但问同一模型「希拉蕊在哪出生」 → 它知道「芝加哥」
- **明明有正确知识，回答错误时却没有惊觉自己错了**

**深层发现**：
- 自我修正是一种**独立的能力**，与知识量不一定关联
- 它可以被抽取成一个 **steering vector**
- 把 steering vector 加到模型中，即使不需要修正时也会自我修正
- → 自我修正是一种「状态」，可能需要额外训练才能具备

### 3.3 训练自我修正的方法

#### 方法一：Revise（分步训练）

**两步法**：
1. **先教 Error Detection**：看错误答案 → 输出 `<refine>` token；看正确答案 → 输出 EOS（结束）
2. **再教 Error Correction**：输入 + 错误输出 + `<refine>` → 学会输出正确答案

**关键发现**：Detection 和 Correction 分开学比合在一起学效果更好

#### 方法一的问题：Output Drift

**问题**：教模型修正错误后，模型参数变了 → 犯的错误也变了
- 原来模型看到输入 X → 输出绿色（错误）
- 训练后模型变了 → 看到输入 X → 输出红色（另一种错误）
- 模型只学过修改绿色错误，没学过修改红色错误 → 反而可能更差

**解决**：不能只教修正，必须把「产生答案 + 自我修正」整套 pipeline 综合训练

#### 方法二：Reinforcement Learning（主流做法）

**核心思路**：
- 给模型输入 → 让它做 Reasoning（输出一长串 token）→ 只看最终答案
- 答案对 → Positive Reward
- 答案错 → Negative Reward

**常用算法**：
- **GRPO**（Group Relative Policy Optimization）
  - DeepSeek-R1 使用的方法
  - 从同一问题 sample 多个答案 → 相互比较 → 用相对排名决定 reward
- **PPO**（Proximal Policy Optimization）
  - OpenAI o1 使用的方法（推测）

**RL 训练的关键发现**：
1. **RL 训练后模型学会了自我修正**
   - 从 Reasoning 过程中可以看到：模型先给出答案 → 发现不对 → 重新思考 → 给出正确答案
   - 这是**涌现出来的**，不是被教出来的
2. **但 RL 训练的效果可以被「伪造」**
   - 如果在 SFT 阶段就教模型「先写错误答案，再写反思，再写正确答案」的模式
   - RL 训练后模型就会照这个模式走 → 看起来像自我修正，实际是照剧本演戏
   - DeepSeek-R1 的论文特别强调：他们没有在 SFT 中教反思模式，RL 训练后的自我修正是**真正涌现**的

### 3.4 RL 训练 Reasoning 的更多发现

#### Reasoning 长度与表现的关系

- 训练过程中，模型输出的 Reasoning 长度会逐渐变长
- 但最终表现和 Reasoning 长度之间**没有必然的正相关**
- 更长的思考不一定更好

#### "Wait" 模式的涌现

- RL 训练后，模型会在 Reasoning 中突然出现 "Wait..." 或类似词
- 这标志着模型在**中途发现思路有问题**，停下来重新思考
- 这是自我修正能力的涌现标志

#### Budget Forcing

- 强制控制 Reasoning 的长度（token 数上限）
- 发现：即使强制缩短 Reasoning，模型仍能保持不错的表现
- → Reasoning 长度不是关键，关键是有没有学会**何时该反思**

#### PRM vs ORM

| 方法 | 定义 | 问题 |
|:---|:---|:---|
| **ORM**（Outcome Reward Model） | 只判断最终答案对错 | 不知道哪一步错了 |
| **PRM**（Process Reward Model） | 判断每一步对错 | 需要标注每一步的对错（昂贵） |

- DeepSeek-R1 发现：PRM 不一定比 ORM 好
- PRM 可能导致 **reward hacking**——模型学会迎合 PRM 而不是真正解决问题

#### Voyager 模式 — RL 训练的终极自我修正

- 任务：让模型玩 Minecraft
- 模型自己写代码 → 执行 → 看结果 → 如果失败就反思 → 修改代码 → 重试
- 这是一种**多轮自我修正**，不是一次性推理

---

## 四、总结与核心洞察

### 4.1 三条路线的对比

| 路线 | 改什么 | 优势 | 代价 |
|:---|:---|:---|:---|
| Decoding | Inference 过程 | 不改参数、即插即用 | 额外运算、需制造错误状态 |
| Workflow | Prompt/流程 | 不改参数、灵活 | 算力可能不划算、指令敏感 |
| Reasoning | 模型参数 | 最智能、自动判断 | 训练成本高、涌现性不可控 |

### 4.2 核心洞察

1. **自我修正 ≠ 有知识**：知道答案和发现自己答错是两回事，修正是一种独立能力
2. **顽固和谦逊是 trade-off**：让模型接受批评会降低 confidence，可能把对的也改掉
3. **Reflection 是奢侈品**：算力有限时，多 sample + majority vote 比 reflection 更划算
4. **RL 训练的自我修正是涌现的**：不是被教的，而是 reward signal 自然催生的
5. **SFT 教反思 = 照剧本演戏**：如果先教反思模式再 RL，模型只是照模式走，不是真反思

### 4.3 引用文献索引

| 文献 | 年份 | 关键贡献 |
|:---|:---|:---|
| Contrastive Decoding 原始论文 | 2022 | 大模型 - 小模型概率分布相减 |
| Representation Classifier | 2023 | 从 Representation 判断答案正确性 |
| TruthX | 2024 | 正确/错误 Representation 相减修正答案 |
| DoLA | 2023 | 同模型前层 vs 后层对比解码 |
| Layer CD | 2025 | Contrastive Decoding 应用到视觉模型 |
| Self-Correction Reflection 分析 | 2024 | 顽固 vs 谦逊 trade-off、指令影响 |
| Reflection 算力经济学 | 2024 | Verification 是奢侈品，majority vote 更划算 |
| 正确知识 ≠ 自我修正 | 2024 | Steering vector、修正能力独立 |
| Revise | 2024 | 分步训练 Error Detection + Correction |
| Output Drift 问题 | 2024 | 训练修正后模型犯的错误变了 |
| DeepSeek-R1 | 2025 | RL 训练涌现自我修正、PRM vs ORM |
| Voyager | 2023 | Minecraft 多轮自我修正 |

---

> ⏳ 转录完整版待 faster-whisper 完成后更新
