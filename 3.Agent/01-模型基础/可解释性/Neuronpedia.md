# Neuronpedia - AI 模型可解释性平台

**网站**: https://www.neuronpedia.org  
**类型**: AI 可解释性（Interpretability）工具  
**创始人**: Johnny Lin（前 Apple 工程师）  
**最后更新**: 2026-04-12

---

## 📋 简介

Neuronpedia 是一个**开源的 AI 模型可解释性平台**，用于探索、操控和实验 AI 模型的内部工作机制。

**核心目标**：打开 AI 模型的黑盒，让你能"看透"神经元/特征具体代表什么含义。

---

## 🎯 核心功能

### 1️⃣ Explore（探索）
- 浏览超过 **4TB** 的激活数据、解释和元数据
- 支持 probes、latents/features、自定义向量、concepts 等

### 2️⃣ Graph（电路图）
- 可视化模型的内部推理步骤
- 基于 Anthropic 的 **Circuit Tracing** 技术
- [在线演示](https://www.neuronpedia.org/gemma-2-2b/graph)

### 3️⃣ Steer（操控）
- 通过调整激活值来修改模型行为
- 支持 instruct（对话）和 reasoning 模型
- 可自定义温度、强度、种子等参数
- [示例：Gemma 2 - Cat Steering](https://www.neuronpedia.org/gemma-2-9b-it/steer?saved=cm7cp63af00jx1q952neqg6e5)

### 4️⃣ Search（搜索）
- 搜索 **5000 万+** 潜在特征/向量
- 支持按解释文本的语义相似度搜索
- 支持通过推理运行自定义文本匹配
- [搜索入口](https://www.neuronpedia.org/search-explanations)

### 5️⃣ API + Libraries
- 全球首个可解释性 API（2024 年 3 月）
- 提供 Python/TypeScript 库
- 大多数端点有 OpenAPI 规范和交互式文档
- [API Playground](https://www.neuronpedia.org/api-doc)

### 6️⃣ Inspect（检查）
- 深入查看每个 probe/latent/feature
- 显示 top activations、top logits、激活密度
- 支持实时推理测试
- 可编译成可分享的列表，支持 IFrame 嵌入

---

## 📦 支持的模型

| 厂商 | 模型 |
|------|------|
| **Google DeepMind** | Gemma 2/3 系列（270M ~ 27B） |
| **Meta** | Llama 3.1/3.3（8B ~ 70B） |
| **OpenAI** | GPT-2 Small, GPT-OSS-20B |
| **Alibaba** | Qwen2.5, Qwen3（1.7B ~ 7B） |
| **DeepSeek** | DeepSeek-R1-Distill-Llama-8B |
| **EleutherAI** | Pythia-70M-Deduped |

---

## 🔬 技术概念

### SAE（Sparse Autoencoder，稀疏自编码器）
- 用于提取模型中的"特征"（features）
- 将模型的神经元激活分解为更易理解的概念
- 例如：Gemma Scope 提供 16k 维度的 SAE
- 技术原理详见：[[稀疏自编码器 Sparse Autoencoder]]

### Features/Latents（特征/潜变量）
- 每个特征代表一个概念
- 示例类别：🌮 食物、📰 新闻、📖 文学、👯 个人、💻 编程、🔬 技术、🏫 学术、💼 商业、⚖️ 法律、🗼 文化
- Neuronpedia 已标注 **5000 万+** 特征

### Circuit Tracing（电路追踪）
- 追踪模型内部的推理路径
- 理解模型如何从输入得到输出
- 由 Anthropic 在 2025 年论文中首创

### Transcoders（转码器）
- 用于细粒度的可解释电路分析
- 连接不同层的特征表示

---

## 🚀 使用场景

| 场景 | 说明 |
|------|------|
| **AI 安全研究** | 理解模型为何做出某些决策，检测对齐问题 |
| **调试模型** | 找出导致错误输出的神经元/特征 |
| **特征发现** | 探索模型学到了什么概念（如"欺骗"、"奉承"等） |
| **教育学习** | 学习 AI 可解释性技术，理解神经网络内部 |
| **实验操控** | 通过"steering"修改模型行为，测试假设 |

---

## 📚 重要研究发布

| 时间 | 项目 | 机构 |
|------|------|------|
| 2026-01 | Assistant Axis | Anthropic |
| 2025-12 | Gemma Scope 2 | Google DeepMind |
| 2025-08 | Circuit Analysis Landscape | Anthropic, EleutherAI, DeepMind |
| 2025 | Llama Scope | OpenMOSS, Fudan University |
| 2024 | GPT-2 Small SAEs | OpenAI, Joseph Bloom, Apollo Research |

---

## 💡 简单理解

想象你有一个黑盒 AI 模型，它说了一句话。你想知道：

1. **为什么**它说这句话？
2. **哪些神经元**被激活了？
3. 这些神经元代表**什么概念**？
4. 能否**修改**它的行为？

Neuronpedia 就是帮你打开这个黑盒的工具：
- ✅ **能看到** - 浏览神经元激活
- ✅ **能搜索** - 按概念查找特征
- ✅ **能操控** - 调整激活值改变输出
- ✅ **能追踪** - 可视化推理路径

---

## 🔗 相关笔记

- [[稀疏自编码器 Sparse Autoencoder]] - SAE 技术原理解释

---

## 🔗 外部链接

- **官网**: https://www.neuronpedia.org
- **GitHub**: https://github.com/hijohnnylin/neuronpedia
- **文档**: https://docs.neuronpedia.org
- **API**: https://www.neuronpedia.org/api-doc
- **社区 Slack**: https://join.slack.com/t/opensourcemechanistic/shared_invite/zt-3m2fulfeu-0LnVnF8yCrKJYQvWLuCQaQ
- **博客**: https://www.neuronpedia.org/blog

---

## 🏆 支持机构

Neuronpedia 由以下机构支持：
- Decode Research
- Open Philanthropy
- Long Term Future Fund
- AISTOF
- Anthropic
- Manifund

---

## 📖 引用

```bibtex
@misc{neuronpedia,
  title = {Neuronpedia: Interactive Reference and Tooling for Analyzing Neural Networks},
  year = {2023},
  note = {Software available from neuronpedia.org},
  url = {https://www.neuronpedia.org},
  author = {Lin, Johnny}
}
```

---

*最后更新：2026-04-12*
