---
title: Inner-Monologue-环境反馈规划
type: paper-note
created: 2026-06-01
tags: [embodied-ai, paper-note, llm-planning, robot]
---

## 论文信息
- **标题**: Inner Monologue: Embodied Reasoning through Planning with Language Models
- **作者/机构**: Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy Zeng, Jonathan Tompson, Igor Mordatch, Yevgen Chebotar, Pierre Sermanet, Tomas Jackson, Noah Brown, Linda Luu, Sergey Levine, Karol Hausman, Brian Ichter — Google Robotics / Everyday Robots
- **发表时间**: 2022 (arXiv:2207.05608)
- **arXiv/链接**: https://arxiv.org/abs/2207.05608
- **发表会议**: CoRL 2022

## 核心问题
SayCan 虽然实现了 LLM 与机器人能力的对接，但它的规划是"相对开环"的——LLM 生成计划后就顺序执行，缺少对执行过程中环境反馈的充分利用。**现实世界中，机器人执行动作经常会失败，需要根据执行结果重新规划。** Inner Monologue 要解决的问题是：**如何让 LLM 在机器人执行过程中持续接收环境反馈（成功/失败检测、场景感知、人类交互），形成闭环的"内心独白"式推理？**

## 关键方法

1. **多模态反馈注入**
   系统将三种类型的反馈以文本形式注入 LLM 的 prompt：
   - **成功检测 (Success Detection)**: 动作执行后是否成功（如"捡起苹果：成功" / "捡起苹果：失败"）
   - **场景感知 (Scene Observation)**: 摄像头看到的物体和文字（如"场景：抽屉已打开，苹果在抽屉里"）
   - **人类交互 (Human Feedback)**: 用户中途给出的新指令或问题回答

2. **内心独白 (Inner Monologue) 机制**
   LLM 持续看到一段文本形式的"对话历史"，包括：
   ```
   Robot: 我去拿苹果
   Scene: 桌子上有苹果和香蕉
   Robot: 捡起苹果
   Outcome: 成功
   Robot: 把苹果放进抽屉
   Scene: 抽屉是关着的
   Robot: 先打开抽屉
   ```
   这种格式让 LLM 能够持续推理和重新规划，就像人类在内心自言自语一样。

3. **闭环重规划 (Closed-Loop Replanning)**
   当检测到动作失败时，LLM 自动生成恢复策略。例如捡取失败后，LLM 可能决定换个角度再试，或者先移动障碍物。

4. **与 SayCan 的对比**
   - SayCan 主要依赖预训练的可负担性函数来接地
   - Inner Monologue 更强调**运行时的环境反馈**作为接地信号
   - 两者可以互补：SayCan 的可负担性 + Inner Monologue 的环境反馈

5. **语言驱动的 API 调用**
   LLM 输出的不是底层动作，而是调用预定义的机器人技能 API（如 `pick(apple)`, `open(drawer)`, `goto(table)`），技能由底层控制器执行。

## 重要细节

- **实验平台**: 与 SayCan 相同的移动操作机器人平台
- **任务类型**: 长序列多步骤任务，如"把冰可乐放进抽屉"、"做一杯咖啡"、"清理桌面"
- **鲁棒性提升**: 相比开环 LLM 规划，Inner Monologue 在任务完成率上有显著提升，特别是在需要错误恢复的场景
- **场景文本的重要性**: 机器人能读取场景中的文字（如产品标签、门牌号），这些信息被注入为文本反馈
- **人类交互**: 支持任务中途的人类干预，如"不要用那个杯子，用左边的"
- **局限性**: 仍然依赖预定义的技能 API 集合；LLM 推理速度可能影响实时性

## 与面试50题的关系
- **Q10**: LLM/VLM 在机器人规划中的应用 — Inner Monologue 展示了闭环反馈在 LLM 规划中的重要性，是 SayCan 的自然演进

## 个人思考