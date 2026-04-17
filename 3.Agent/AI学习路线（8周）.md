# AI/NLP 学习路线（8周）

> 制定日期：2026-03-29
> 基于：Transformer 系列教程 + HuggingFace 入门

---

## 当前基础

```
✅ Transformer 原理（架构/训练/推理）
✅ 各种基础概念（BN/LN/Adam/BLEU/BPE/位置编码/FFN）
✅ HuggingFace 基础（Pipeline/Tokenizer/AutoModel/Fine-tuning）
✅ 大模型微调基础概念（LoRA/QLoRA/LLaMA-Factory）
```

---

## Week 1-2：第一个完整项目

**目标**：独立完成情感分析项目

### 内容
- [ ] HuggingFace Trainer 实战
- [ ] 真实数据集预处理（ChnSentiCorp 或电影评论）
- [ ] 模型评估（F1、混淆矩阵、Accuracy）
- [ ] 模型保存和加载（`model.save_pretrained`）
- [ ] 跑通 `sentiment_analysis_marimo.py`

### 产出
- GitHub 上一个跑通的情感分析项目
- 写一篇项目总结笔记

### 参考资料
- [[huggingface_intro_marimo]] — HuggingFace 入门
- `knowledge-base/Projects/sentiment-analysis/`

---

## Week 3-4：大模型微调

**目标**：用 LoRA 微调一个中文大模型

### 内容
- [ ] 安装并上手 LLaMA-Factory
- [ ] 了解 instruction tuning 数据格式（Alpaca/ShareGPT）
- [ ] QLoRA 微调 Qwen2.5 或 ChatGLM
- [ ] 评估微调效果（对话质量）
- [ ] 了解 LoRA rank/alpha 超参数调节

### 产出
- 一个能对话的微调模型
- 笔记：LoRA 微调踩坑记录

### 参考资料
- [[Adam Optimizer]] — 优化器原理
- [[Transformer词汇表与BPE]] — 分词基础

---

## Week 5-6：RAG（检索增强生成）

**目标**：给大模型接上知识库，构建问答系统

### 内容
- [ ] 向量数据库（Faiss 或 Chroma）
- [ ] Embedding 模型（text2vec / bge-m3）
- [ ] LangChain 基础用法
- [ ] 构建文档问答 Bot
- [ ] 召回优化（BM25 + 向量混合检索）

### 产出
- 一个基于自己文档的问答 Bot
- 可以用 Obsidian Vault 作为知识库来源！

### 参考资料
- [[BLEU Score]] — 评估指标
- [[Transformer推理策略]] — 推理原理

---

## Week 7-8：部署上线

**目标**：把模型变成可用的完整服务

### 内容
- [ ] FastAPI 封装模型接口
- [ ] 模型量化推理（vLLM 或 ONNX）
- [ ] Gradio 或 Streamlit 前端
- [ ] Docker 打包部署
- [ ] 性能测试（QPS、延迟）

### 产出
- 一个可公开演示的完整 AI 应用
- 部署文档

---

## 每周节奏

```
周一/二：学概念（文档/笔记）
周三/四：跑代码（动手实践）
周五：总结 + 写笔记到 Obsidian
周末：复习 + 准备下周
```

---

## 里程碑

| 时间 | 能力 |
|------|------|
| **2周后** | 独立完成 NLP 分类任务 |
| **4周后** | 能微调中文大模型 |
| **6周后** | 能做 RAG 问答应用 |
| **8周后** | 能部署完整 AI 产品 |

---

## 技术栈总览

```
基础层:     PyTorch + Transformer 原理
工具层:     HuggingFace Transformers + Datasets
微调层:     LLaMA-Factory + PEFT (LoRA/QLoRA)
应用层:     LangChain + Faiss + FastAPI
展示层:     Gradio / Streamlit
```

---

## 相关笔记

- [[transformer_tutorial_marimo]] — Transformer 架构篇
- [[transformer_training_marimo]] — Transformer 训练篇
- [[transformer_inference_marimo]] — Transformer 推理篇
- [[huggingface_intro_marimo]] — HuggingFace 入门
- [[Adam Optimizer]] — 优化器
- [[Batch Normalization]] / [[Layer Normalization]] — 归一化
- [[BLEU Score]] — 评估指标
- [[Transformer词汇表与BPE]] — 分词
