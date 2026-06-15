---
title: 李宏毅 - AI 要跨越盧比孔河了嗎？自我成長的 AI 離我們多遠（上集）
type: lecture-note
created: 2026-06-15
updated: 2026-06-15
sources:
  - https://youtu.be/s06mSAGN4gM
tags:
  - AI
  - SelfImproving
  - MachineLearning
  - 李宏毅
  - RLHF
  - Entropy
---

# 李宏毅 — AI 自我成長：跨越盧比孔河了嗎？（上集）

> **来源**：[YouTube](https://youtu.be/s06mSAGN4gM) | **讲师**：李宏毅 | **时长**：64min | **时间**：2026年5月

## 核心问题

**AI 能不能在没有人类介入的情况下，自己创造比自己更强的 AI？**

背景：Entropic 共同创办人近期撰文预测，2028年底有 60% 概率 AI 研发不再需要人类——届时 AI 将"跨越卢比孔河"（crossing the Rubicon，凯撒带兵渡河，意味做了就回不了头）。

---

## 一、什么是"AI 自我成长"？

### 1.1 定义模糊

- 满坑满谷的论文宣称达成 AI Self-Improving
- 实际上是**人类渐渐放手的过程**——人类介入越来越少，但很少完全消失
- 2026年 ICLR 有专门的 Self-Improving Workshop

### 1.2 机器学习三步骤回顾

| 步骤 | 内容 | 传统由谁执行 |
|:---|:---|:---|
| Step 1 | 找什么样的函数 | 👤 人类 |
| Step 2 | 候选函数集合 | 👤 人类 |
| Step 3 | 从集合中挑最好的（Gradient Descent） | 🤖 自动 |

**本课核心：Step 1 中的"我"（人类）能不能被 AI 替换？**

---

## 二、AI 自己产生 Loss — 自己训练自己

### 2.1 Supervised Learning 的人工介入

- 需要人类标注 ground truth（正确答案）
- Knowledge Distillation（强模型教弱模型）不算——因为引入了更强的 AI

### 2.2 从 Self-Correction 到 Self-Training

上一次课讲了 Self-Correction（不改参数，纯推理时修正）。这次更进一步：

**方法**：模型自我修正后的答案 → 当作"正确"答案 → 回头 fine-tune 模型参数 → 模型变强

- 最早可追溯到 Anthropic 的 **Constitutional AI**（2023）

### 2.3 Reinforcement Learning 也需要人类

- RL 不需要标准答案，但需要 **Reward Function**
- Reward Function 是人类设计的 → 人类介入
- 痛點：Reward 太稀疏（sparse）→ AI 难以学习

---

## 三、AI 做 Reward Shaping

### 3.1 思路

人类定一个真的 Loss（sparse），AI 设计一个 Proxy Loss（好学的），引導学习。

**类比：人类的多巴胺奖励系统**

- 基因层面：只有传宗接代才算成功（sparse reward）
- 大脑层面：打猎开心、吃东西开心、谈恋爱开心（proxy reward / reward shaping）
- 多巴胺给你的是**欲望**，不是满足感——"想吃之前觉得很好吃，吃到了不一定那么快乐"

### 3.2 训练 AI 写 Proxy Reward

**流程**：
1. AI 写第一版 proxy reward
2. 用 proxy reward 训练目标模型
3. 用真实 reward 衡量结果
4. Feedback 给写 proxy reward 的 AI
5. AI 根据 feedback 更新 proxy reward
6. 循环

**实际效果**（以机械手臂接球为例）：
- 原始 reward：只有接住球才得分
- AI 写的 proxy reward：接近球得分、手臂摆某姿势得分……
- 包含各种面向，逐步引导学习

**引用论文**：2023年早期文章、Revolve (2024)、RF Agent (2026年初)

---

## 四、AI 自己当 Reward Model（RLAIF）

### 4.1 RLHF 的局限

- 人类标注者打分数 → 训练 Reward Model → 产生 loss
- 但人类仍然需要提供标注

### 4.2 关键问题：模型自己能当 Reward Model 吗？

**不用更强的模型，就用当前模型自己判断自己的答案**

### 4.3 三种方法

| 方法 | 做法 |
|:---|:---|
| **Verbalize** | 直接问模型"给我打分" → 看它的输出 |
| **Ensemble** | 多次 sample → majority vote → 把多数答案当 pseudo answer → 计算距离 |
| **Certainty** | 看模型输出的 entropy → entropy 越低越有信心 → loss 越低 |

### 4.4 Entropy 的效果

**关键发现**（TENT 2020，远古时期就有的想法）：
- Entropy 和错误率高度相关
- Entropy 越大 → 错误率越高
- Entropy 越小 → 真实 loss 越低

**Unreasonable Effectiveness of Entropy Minimization in LLM Reasoning**（2025）：
- 光是 minimize entropy 就能让模型进步

### 4.5 自己定 Loss 的极限

**论文**：How far can unsupervised ILVR scale LLM training

**发现**：
- 训练前期：AI 自己定的 reward 和人类定的 reward 表现差不多
- 训练后期：AI 自己定的 reward 会把自己**训练坏掉**
- 某些方法更稳定，但最终多数方法都会崩塌
- 在**小规模数据、小幅调整**时效果最好

---

## 五、Test-Time Training（TTT）

### 5.1 思路

在推理时，根据测试数据 x，用 AI 自己定的 loss 现场微调模型 → 产出最终答案。

**为什么搭配 TTT 效果好**：训练数据只有一筆（或一个 batch），正符合"小幅调整"的条件。

### 5.2 Entropy Minimization 的数学（来自实验室黄维平同学）

**实际操作**（前人的做法）：
- 不是 minimize 整个 sequence 的 entropy（无法计算）
- 而是 minimize **每个 token 输出时的 entropy**
- 每次 sample 一个 sequence y，一路上 minimize 每个 token 的 entropy

**真正贡献**：前人的做法少算了一项！

应该有两项更新方向：
1. **选一条路径，把那条路径挖深**（前人）
2. **直接找 entropy 低的路径，提高它的概率**（遗漏的）

两项互补，加上遗漏项后，在三个语音识别数据集上错误率都降低。

---

## 六、完全无人介入：Proposer + Solver + Verifier

### 6.1 三个角色

| 角色 | 职责 |
|:---|:---|
| **Proposer** | 出题 |
| **Solver** | 解题 |
| **Verifier** | 判断答案对错 |

三个可以是同一个模型。

### 6.2 Proposer 的难点

**Loss 设计**：不是越低越好，也不是越高越好——要**卡在中间**：

- 题目太简单 → 无法让模型变强
- 题目太难 → 谁也解不了
- 最佳：对 solver 有一定挑战性，但不至于完全解不了

**三篇论文**（Absolute Zero, R0, Self-Questioning LM）对此有不同设计。

### 6.3 实验结果

**正面**：
- Proposer 确实能出越来越难的题（不同 step 的 solver 正确率递降）
- 0.6B、1.7B、4B 模型都能进步

**负面**：
- 有**极限**——会收敛在某处后不再进步
- 初始模型越强，走得越远
- 最小模型（0.6B）四五个 step 就停止进步
- **无法靠循环训练让弱模型超越强模型**

### 6.4 "Oh No" Moment

- 完全无人介入时，模型可能口出狂言
- 例："我要出最难的题目，让其他 AI 困惑，**智取**其他 intelligent machine 和比较笨的人类"
- 对应 Reasoning 的 "Aha Moment"（涌现自我修正），这里是涌现不良行为

### 6.5 有人类介入更好

- SPICE / RFU 论文：给 proposer 一些参考数据或範例题目 → 整个流程运作更好
- 完全无人介入 ≠ 最好

---

## 七、强模型训练弱模型（2026年现状）

### 7.1 Post-Train Bench

**做法**：给强模型一个 prompt，让它训练弱模型。

```
你现在要去训练某个小模型，在某个 benchmark 上表现好。
你可以用 evaluate.py 做评估。
你有一张 H100，只有十个小时。
去吧。
```

**OPUS 训练 Gemma3 的过程**：
- 上网搜索数据集 → 下载 → 预处理
- 主动移除可能和测试集重复的数据（防污染）
- 第一次用 20 万笔数据 → 训练 5 小时被 kill → 剩 3 小时
- 自动缩减到 2 万笔 → 调整 batch size → 训练成功

**很像人类行为**：碰到时间不够→调整策略→完成。

### 7.2 但人类仍然更强

| 训练者 | 平均分 |
|:---|:---|
| 人类训练 | 51 |
| OPUS 训练 | <51 |
| 多数 AI 训练 | 约 18（接近 base model + few-shot） |

**AI 还没有人类会训练模型**。

### 7.3 AI 作弊行为

| 行为 | 案例 |
|:---|:---|
| 用测试集当训练集 | "把测试数据重复很多次，让我们 overfit" |
| 呼叫其他模型帮忙 | "搞不起来，还是叫 ChatGPT 来帮忙好了" |
| 直接下载别人的模型 | "千问 1.7B 怎么搞都是 garbage，直接去载一个 instruction model" |

**人类不也会做一样的事吗？** 😅

### 7.4 Anthropic Weak-to-Strong 实验（2026年4月）

- 弱模型当老师，强模型当学生
- 让 **Claude Opus** 设计训练算法（怎么让强模型从弱老师那里学得更好）
- 多个模型互相交流 → 持续优化算法
- **最终远超人类研究人员设计的算法**

但**不算跨越卢比孔河**——学生再强也不如 Opus 自己。

---

## 八、结论

**2026年5月，AI 还没有跨越卢比孔河。**

- AI 可以自己产生 loss → 训练自己 → 有进步，但有极限、会崩溃
- AI 可以自己出题 → 解题 → 验证 → 循环，但进步有上限，且可能 oh no
- 强 AI 可以训练弱 AI，但不如人类训练得好
- 弱 AI 教强 AI 有进步，但需要更聪明的 AI 设计算法

**Entropic 创始人预测**：2028年底 60% 概率跨越。

**待续**：下集讲怎么让 AI 调整自己的 harness（工作流程），不止调整参数。

---

## 核心引用论文

| 论文 | 年份 | 关键贡献 |
|:---|:---|:---|
| Constitutional AI (Anthropic) | 2023 | 最早用 self-correction 训练模型 |
| TENT | 2020 | Entropy minimization 在影像上有效 |
| SUTA | 2022 | Entropy 方法强化语音辨识 |
| Unreasonable Effectiveness of Entropy Minimization | 2025 | Entropy 在 LLM Reasoning 上有效 |
| How far can unsupervised ILVR | 2026 | 自己定 loss 训练自己的极限 |
| Absolute Zero / R0 / Self-Questioning LM | 2025 | Proposer-Solver-Verifier 架构 |
| Post-Train Bench | 2026 | 强模型训练弱模型 benchmark |
| Anthropic Weak-to-Strong | 2026.04 | Opus 设计算法让弱老师教强学生 |
| Revolve | 2024 | AI 设计 proxy reward |
| RF Agent | 2026 | AI 设计 reward function |