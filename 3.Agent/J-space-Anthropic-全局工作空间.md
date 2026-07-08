---
title: "J-space：Anthropic 发现 Claude 内部的全局工作空间"
type: research-note
created: 2026-07-08
updated: 2026-07-08
sources:
  - https://www.anthropic.com/research/global-workspace
  - https://transformer-circuits.pub/2026/workspace/index.html
  - https://github.com/anthropics/jacobian-lens
  - https://techorange.com/2026/07/07/anthropic-a-global-workspace-in-claude
tags:
  - AI
  - interpretability
  - Anthropic
  - Claude
  - consciousness
---

## 概述

2026年7月6日，Anthropic 可解释性团队（16位作者，Wes Gurnee、Nicholas Sofroniew、Jack Lindsey 领衔）发表论文 *"Verbalizable Representations Form a Global Workspace in Language Models"*。

在 Claude 内部发现了一个自发形成的内部工作空间，命名为 **J-space**（J 空间）。

## 什么是 J 空间

Claude 神经网络内部的一小组神经活动模式，充当"内部白板"——模型在这里"想"概念，但不会写进输出文本。

核心特征：

| 特征 | 说明 |
|:---|:---|
| 容量极小 | 同时只容纳几十个活跃概念，占模型激活方差的 6-10% |
| 连接极广 | 被网络中更多部位读取和写入，某些区域差异达百倍 |
| 自发涌现 | 不是工程师设计，训练过程中自行形成 |
| 与 CoT 不同 | 思维链是写出来的文字，J-space 是神经激活中默默运作 |

## 发现工具：J-lens

J-lens（雅可比透镜）——对每个词汇，计算某个内部激活对未来生成该词概率的平均线性效应。是 logit lens 的改进，在中间层也保持可解读。

## 三层结构

| 阶段 | 层范围 | 功能 |
|:---|:---|:---|
| 感官模式 | ~0-38 层 | 处理原始输入，多不可解读 |
| 工作空间模式 | ~38-92 层 | J-space 所在，抽象且持久 |
| 运动模式 | ~92-100 层 | 与输出对齐，准备词汇 |

## J-lens 读到什么（不出现在输出中）

- 读到含 bug 的代码 → J-space 浮现 "ERROR"
- 读到 prompt injection → 浮现 "injection" 和 "fake"
- 读到蛋白质序列 → 浮现该蛋白质的生物功能
- 多步数学题 → 中间步骤按顺序出现
- 图片识别 → 选中鼻子位置浮现 "nose"

## 五特性

| 特性 | 验证 |
|:---|:---|
| 可引用性 | 注入概念后 88% 出现在 top-5 |
| 自主调制 | 可要求"想"或"不想"某概念 |
| 内部推理 | 交换中间步骤会改变结论（60-70%） |
| 灵活泛化 | 同一概念可回答不同问题 |
| 选择性 | 自动化任务不依赖 J-space |

## 消融实验

| 任务 | 关闭 J-space 后 |
|:---|:---|
| MMLU、情感分析、SQuAD | 85-95%，基本无损 |
| 多步推理 | 95% → 5% |
| 类比补全、翻译、密码解码 | 严重退化 |
| 带 CoT 的数学 | ~70%，因步骤写在了文本里 |

## AI 安全意义

1. **意图监控**：不诚实行为时 J-space 浮现 "manipulation"、"realistic"，输出中不可见
2. **行为干预**：可主动注入或移除 J-space 中的概念
3. **模型法医**：对 misaligned 模型生物，J-lens 能发现隐藏倾向

## 重要声明

**不是意识。** Anthropic 明确：研究涉及"访问意识"（access consciousness），不是"现象意识"（phenomenal consciousness）。"全局工作空间"类比是有用比喻，不是证明。

## 开源

- 代码：[anthropics/jacobian-lens](https://github.com/anthropics/jacobian-lens)（Apache 2.0，Python）
- 交互演示：[neuronpedia.org/jlens](https://neuronpedia.org/jlens)
- 外部专家评注：Anthropic 邀请神经科学、哲学、LLM 可解释性专家撰写

## 行业反响

- **Axios**：论文中 "conscious" 一词出现超 200 次
- **VentureBeat**："mirrors a leading theory of consciousness"
- **Ethan Mollick**："some really interesting research"
- **LessWrong**：详细 review 认为 "fantastic paper"
- **Brian Roemmele**：批评本质是品牌营销——让 Claude 更强大、更可控、Anthropic 是唯一做严肃科学的

## 我的判断

- 工具层面：J-lens 是 logit lens 的重要升级，开源可验证
- 安全层面：如果能读取"没说出口的想法"，对 alignment auditing 是质的突破
- 哲学层面：刻意用全局工作空间理论框定，谨慎回避意识声明，但也有品牌信号成分
- 局限：单次前向传播（无反馈循环）、只包含词语、J-lens "不完美的方法"

**一句话：Anthropic 找到了 Claude 内部的"黑板"——神经层面默默运作，能读能写能改，对推理至关重要，对安全监控有实际价值。**