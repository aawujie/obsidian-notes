# 3.Agent 知识库索引

> 重组日期：2026-04-17

---

## 目录结构

```
3.Agent/
├── 01-模型基础/          Transformer、注意力、模型组件、数学、可解释性
├── 02-训练与微调/        微调技术(LoRA/DPO/GRPO)、训练基础、工具链
├── 03-推理与部署/        LLM推理架构、KV Cache、MoE、量化(TurboQuant)
├── 04-Agent架构与模式/   Agent设计模式、架构调研、访谈笔记
├── 05-项目文档/          minimind、EvoMap、OpenClaw-MC、NanoClaw等项目
├── 06-OpenClaw/          OpenClaw完整源码剖析(Track0/A/B)、核心配置
├── 07-工具与平台/        Cursor、提示词、API集成、DevOps、监控
├── 08-参考资料/          论文PDF、可视化HTML、学习路线、杂项
```

---

## 01-模型基础

### Transformer与注意力 (16 篇)
- Transformer架构从零理解 / Transformer 入门与基础概念
- Transformer 注意力机制详解 / Transformer MLP 如何存储知识
- Transformer词汇表与BPE / Transformer学习率调度
- Transformer 可解释性详解 - 李宏毅（自 9.Coding 移入）
- 注意力机制入门图解 / 注意力机制详解 / 注意力机制 Attention 核心原理（自 9.Coding 移入）
- 多头注意力深入理解 / Masked Multi-Head Attention
- Flash Attention 详解 - 李宏毅（自 9.Coding 移入）
- 词汇表Vocabulary构建
- 李宏毅-Self-Attention与Transformer详解（中英文两版共存）

### 模型组件 (14 篇)
- Embedding全面理解 / 位置编码从零理解
- Position-wise FFN / Feed-Forward Network (FFN)（自 9.Coding 移入）
- Layer Normalization / LayerNorm vs Softmax - 本质区别（自 9.Coding 移入）
- Batch Normalization / 批量归一化 BN 核心原理 / 批量规范化 BN 详解（自 9.Coding 移入）
- Label Smoothing
- Positional Embedding 详解 - 李宏毅（自 9.Coding 移入）
- Transformer 位置编码详解（自 9.Coding 移入）
- RoPE旋转位置编码详解 / RoPE旋转位置编码研究笔记

### 数学基础 (3 篇)
- Entropy_CrossEntropy_KLDivergence
- Math_Becomes_Difficult（从加法到傅里叶变换）
- 投影矩阵 Projection Matrix

### 可解释性 (6 篇 + 图片)
- 稀疏自编码器 Sparse Autoencoder
- AI_Interpretability_Anthropic / Neuronpedia
- Towards-Monosemanticity / monosemantic-features-zh / toy-model-zh
- images_toy/ + monosemantic-features-images/ (配图)

### 模型架构 (2 篇)
- Qwen3-8B 模型结构解析
- 多语言模型跨语言对齐机制

---

## 02-训练与微调

### 微调技术 (18 篇)
- LoRA微调原理 / LoRA线性代数几何视角 / LoRA原理可视化详解
- PEFT 参数高效微调概览 / LLaMA-Factory 快速上手
- 微调技术 Fine-tuning（自 9.Coding 移入）
- DPO Direct Preference Optimization / DPO vs RLHF 对比笔记
- GRPO Group Relative Policy Optimization / GRPO组相对策略优化研究笔记
- GSPO-组序列策略优化研究笔记
- Adam Optimizer / Teacher Forcing / BLEU Score / 余弦退火

### 训练基础 (2 篇)
- 混合精度训练 Mixed Precision Training
- 大模型训练系统优化（自 9.Coding 移入）

### 工具与实验代码
- [[huggingface_intro_marimo]] — HuggingFace 入门
- [[qwen3_fine_tuning]] / [[qwen3_fine_tuning_marimo]] — Qwen3 微调
- [[transformer_training_marimo]] / [[transformer_tutorial_marimo]] / [[transformer_inference_marimo]] — Transformer 教程

> 代码文件统一在 `Resources/marimo/` 下。

---

## 03-推理与部署

### LLM推理与架构 (9 篇)
- KV Cache / KV Cache 详解 - 李宏毅（自 9.Coding 移入）
- Dense vs MoE / MOE (混合专家模型)
- YaRN - RoPE 上下文扩展 / YaRN 上下文扩展研究笔记
- LEX Transformer 长度外推研究笔记
- LLM 推理框架对比（自 9.Coding 移入） / vLLM 并发原理（自 9.Coding 移入）

### TurboQuant (8 篇)
- _导航 / TurboQuant 实际实现详解 / TurboQuant 源码逐行解读
- Turbo Quant 详解（自 9.Coding 移入）
- Walsh-Hadamard 变换入门 / Lloyd-Max 最优量化原理
- Perplexity 与模型质量评估 / GPU 内存带宽与推理加速原理

---

## 04-Agent架构与模式 (8 篇)
- 五种-Agent-Skill-设计模式
- OrbitOS-vault 架构详解 / Maton API 集成中间层详解
- OpenClaw + NotebookLM - AI 指挥 AI 的知识系统
- Hermes Agent 项目调研报告 / Anthropic_创始人访谈笔记
- CLI-Anything 让软件 Agent 化（自 9.Coding 移入）
- Compaction Mode Safeguard 详解（自 9.Coding 移入）

---

## 05-项目文档

### minimind (15 篇系列)
- 00-项目总览 → 15-位置编码（编号式系列文档）

### EvoMap (2 篇 + 1 概览)
- EvoMap - AI自我进化基础设施 / 00-概览 / 01-核心概念

### OpenClaw Mission Control (3 篇)
- 00-Overview / 01-Implementation-Plan / 02-Prompts

### 其他项目
- NanoClaw - 轻量级 AI 原生框架
- Vivgrid - AI Agent 全生命周期管理平台
- Project-NOMAD项目分析报告 / Takopi 项目分析
- ZeroClaw 安装配置指南 / YouDub-webui-视频中文化工具
- sentiment-analysis (marimo实验)

---

## 06-OpenClaw (100+ 篇)

### OpenClaw核心 (7 篇)
- 配置教程 / 多Agent配置完全指南 / 权限体系
- memorySearch 原理 / Skills和插件扩展路径详解
- Subagent 模型指定方式 / 专用Agent vs 子Agent对比

### Track0-安装教程 (核心概念/安装部署/工具系统/通道接入/Gateway配置/AI模型Provider/自动化/故障排查)
### TrackA-工程主线 (00-59, 函数级源码剖析)
### TrackB-AI核心框架 (00-21, 原理+实战)

---

## 07-工具与平台

### Cursor (4 篇)
- Automations / Cloud Agent / Hooks / Subagents 使用指南

### 提示词与技巧 (2 篇)
- Gemini 提示词技巧 / Prompt

### API与集成 (1 篇)
- Stripe 购买链接类型详解

### DevOps工具 (5 篇)
- Cursor CLI Agent / tmux / Discord 超时排查 / Discord 私信 vs 群聊@Bot / WandB

### 监控与可观测性 (2 篇)
- Grafana - 可视化与告警平台 / Prometheus - 监控指标收集系统

---

## 08-参考资料

### Papers (6 篇 PDF)
- DeepSeek-R1-GRPO / GSPO / Length-Extrapolatable-Transformer
- Roformer-RoPE / SAPO-GSPO-Qwen / YaRN-Context-Extension

### 可视化
- [[attention-viz.html]] / [[eigenvalue-viz.html]] / [[evd-vs-svd.html]]
- [[positional-encoding-viz.html]] / [[svd-viz.html]] / [[transformer-viz.html]]

> 可视化文件统一在 `Resources/html/` 下。

### 学习路线与杂项
- AI学习路线（8周） / TypeScript vs Python 对比
- 卡尔达肖夫尺度-文明分级理论
- imgs/ (配图)