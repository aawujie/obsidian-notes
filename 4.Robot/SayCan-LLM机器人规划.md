---
title: SayCan-LLM机器人规划
type: paper-note
created: 2026-06-01
tags: [embodied-ai, paper-note, llm-planning, robot]
---

## 论文信息
- **标题**: Do As I Can, Not As I Say: Grounding Language in Robotic Affordances
- **作者/机构**: Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Daniel Ho, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Eric Jang, Rosario Jauregui Ruano, Kyle Jeffrey, Sally Jesmonth, Nikhil Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Kuang-Huei Lee, Sergey Levine, Yao Lu, Linda Luu, Carolina Parada, Peter Pastor, Jornell Quiambao, Kanishka Rao, Jarek Rettinghouse, Diego Reyes, Pierre Sermanet, Nicolas Sievers, Clayton Tan, Alexander Toshev, Vincent Vanhoucke, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Mengyuan Yan, Andy Zeng — Google Robotics / Everyday Robots
- **发表时间**: 2022 (arXiv:2204.01691)
- **arXiv/链接**: https://arxiv.org/abs/2204.01691
- **发表会议**: CoRL 2022

## 核心问题
LLM 拥有丰富的语义知识，但缺乏真实世界的物理经验。直接让 LLM 输出机器人动作会遇到严重问题：LLM 可能建议机器人执行它根本做不到的动作（如"捡起枕头"但机器人没有对应的夹爪），或者建议不安全的动作，或者不考虑动作的时间顺序。SayCan 要解决的核心问题是：**如何将 LLM 的语义知识有效地"接地"到机器人的实际物理能力上？**

## 关键方法

1. **双因子评分机制 (Two-Factor Scoring)**
   对每个候选技能，最终得分 = LLM 语义概率 x 可负担性概率 (affordance)。即：
   $$P(skill | instruction, state) \propto P_{LLM}(skill | instruction) \times P_{affordance}(skill | state)$$
   这个乘积确保机器人只选择既"语义上合理"又"物理上可行"的技能。

2. **可负担性函数 (Affordance Functions)**
   每个原子技能都通过强化学习 (RL) 训练，并附带一个价值函数 (value function)。该价值函数输出在当前状态下该技能成功的概率，即"可负担性"。如果当前状态连物体都看不到，捡取技能的可负担性就接近 0。

3. **LLM 只做高层规划，不做底层控制**
   LLM 被结构化 prompt 告知所有可用技能及其描述，然后输出下一个技能的候选分布。底层执行完全由 RL 训练的策略完成。LLM 不直接控制电机。

4. **时间闭环 (Temporal Grounding)**
   每执行一步后，用新的状态重新评估可负担性，更新 LLM prompt 中的历史记录，然后重新规划下一步。这天然防止了动作顺序错乱的问题。

5. **技能库 (Skill Repertoire)**
   技能包括导航技能（如"走到桌子旁"）、操作技能（如"捡起可乐罐"）和组合技能。技能在真实厨房环境中训练。

## 重要细节

- **实验平台**: 真实移动操作机器人（轮式底座 + 机械臂），在厨房环境中执行 101 个任务
- **任务示例**: "我洒了咖啡，能帮我拿清洁工具吗？" — 机器人需要理解并执行多步骤操作
- **对比基线**: LLM-only（无 affordance grounding）经常建议不可行的动作，SayCan 显著优于
- **可解释性**: 两个因子的分解使得可以清楚解释为什么选择了某个技能（语义相关性 vs 物理可行性）
- **局限性**: 技能库是预定义的固定集合，不能泛化到技能库之外的新任务；每个技能需要单独训练 RL 策略

## 与面试50题的关系
- **Q10**: LLM/VLM 在机器人规划中的应用 — SayCan 是 LLM 用于机器人规划的开创性工作，其双因子评分的思路深刻影响了后续工作

## 个人思考