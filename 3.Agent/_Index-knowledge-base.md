# 领域知识索引

> 本文件是知识库的总入口。每当新增知识文档时，在对应分类下添加条目。

---

## Concepts（术语概念）

### Transformer 与注意力（10 篇）

- [[Transformer架构从零理解]] — Encoder-Decoder 完整架构、残差连接、位置编码
- [[Transformer 可解释性详解 - 李宏毅]] — Attention 可视化、探针分析
- [[Transformer词汇表与BPE]] — BPE/WordPiece 分词算法
- [[Transformer学习率调度]] — Warmup + 衰减策略
- [[注意力机制入门图解]] — Q/K/V 直觉图解
- [[注意力机制详解]] — 缩放点积注意力、加性注意力、Softmax 归一化、多头注意力数学推导
- [[多头注意力深入理解]] — 多子空间并行、reshape 技巧
- [[Masked Multi-Head Attention]] — 因果掩码、Decoder 自注意力
- [[Flash Attention 详解 - 李宏毅]] — IO 感知注意力、Tiling、在线 Softmax
- [[词汇表Vocabulary构建]] — 词表构建流程

### 模型组件（7 篇）

- [[Embedding全面理解]] — 词嵌入、查找表、训练方式
- [[位置编码从零理解]] — 三角函数编码、旋转矩阵、RoPE
- [[Positional Embedding 详解 - 李宏毅]] — 绝对/相对位置编码对比
- [[Position-wise FFN]] — 逐位置前馈网络
- [[Layer Normalization]] — LN vs BN、Pre-LN vs Post-LN
- [[Batch Normalization]] — BN 原理与局限
- [[Label Smoothing]] — 标签平滑正则化

### 训练与评估（4 篇）

- [[Adam Optimizer]] — 动量 + 自适应学习率
- [[Teacher Forcing]] — 训练时用真实标签替代预测
- [[BLEU Score]] — 机器翻译评估指标
- [[LoRA微调原理]] — 低秩适配、QLoRA

### LLM 推理与架构（5 篇）

- [[KV Cache 详解 - 李宏毅]] — Prefill/Decode、内存压力、GQA/MQA/MLA/Sliding Window/Pruning
- [[KV Cache]] — 占位索引（详见上条）
- [[LLM 推理框架对比]] — vLLM/MLX/llama.cpp/TensorRT-LLM/Ollama 对比
- [[MOE (混合专家模型)]] — Router + Top-k Expert、稀疏激活
- [[多语言模型跨语言对齐机制]] — 跨语言表示对齐

### TurboQuant 知识合集（8 篇）

- [[TurboQuant/_导航|TurboQuant 导航]] — 阅读顺序和知识链检查
- [[Turbo Quant 详解]] — 完整概述：论文原理、实测数据、使用建议（已纠正科普误解）
- [[TurboQuant 实际实现详解]] — 源码级管线解析（Norm → WHT → Lloyd-Max），三个关键发现
- [[TurboQuant 源码逐行解读]] — 逐文件逐函数源码解读：调用关系、数据流、设计决策、与 C 实现差异
- [[Walsh-Hadamard 变换（WHT）入门]] — 核心旋转操作：蝶形运算、O(d log d)、高斯化定理
- [[Lloyd-Max 最优量化原理]] — 最优码本构建：迭代算法、高斯分布质心、率失真理论
- [[Perplexity 与模型质量评估]] — PPL / KL 散度 / NIAH 测试方法论
- [[GPU 内存带宽与推理加速原理]] — Decode 带宽瓶颈、压缩加速原理、L2 缓存效应

### 机器人（2 篇）

- [[Unitree G1 WBT Dataset 调研报告]] — Unitree 人形机器人数据集
- [[人形机器人全身控制-核心知识点]] — 全身运动控制

### 其他

- [[LSP (Language Server Protocol)]] — 语言服务器协议（开发工具）

<!-- - [[智驾核心术语解析]] — BLC/DTU/DSM/DEM/SSM 等 -->

---

## Architecture（系统架构）

- [[Pipeline 代码架构全解]] — hil_auto_test/pipeline/ 完整架构：CLI 命令体系、LPT 分组、FUSA 合并、Mixin 编排、Jinja2 模板、端到端流程
- [[HIL监控平台统一架构方案]] — 将 gitlab_runner_tool 迁移到 prometheus_grafana 项目：PostgreSQL + Prometheus 双数据源、Job API Service、Grafana Dashboard 统一展示

## Modules（模块详解）

<!-- - [[canbus-mcu 源码分析]] — CAN 总线通信、信号收发、OEM 适配 -->

## Testing（测试体系）

- [[BLC迁移至hil_auto_test-分阶段方案]] — 三阶段迁移方案：阶段0 最小可用（独立子目录）、阶段1 框架集成（portal_test + pipeline）、阶段2 架构演进（Channel 抽象 + 用例统一）
- [[HIL测试失败记录-待修复]] — fixed-use-high-speed-gateway 分支已有失败：get_runnable_mask 全 False、smoke_test 数量变化、stdout/stderr 不一致

## Infrastructure（基础设施）

- [[Prometheus-Grafana 监控系统]] — GitLab Runner 监控：自定义 Exporter、Docker Compose 编排、Grafana Dashboard、历史数据回填
- [[HIL-Job优化方案]] — 两阶段 Job 合并：Phase1 智能分组（-175 Jobs）、Phase2 FUSA 约束合并（-84 Jobs），总计 479→220，节省 11h Runner 时间
- [[飞书应用文档创建-API实践]] — 飞书自建应用通过 Open API 创建云文档、写入结构化内容、设置分享权限。核心发现：应用只能在自己的空间创建文档，通过文档级权限开放访问
- [[OpenClaw配置-自定义API和Skills]] — OpenClaw AI coding agent 配置自定义 OpenAI 兼容 API + Cursor skills 加载

## Projects（项目）

- `Projects/llama-factory-quickstart/` — LLaMA-Factory 快速上手
- `Projects/software-in-loop/` — SIL 仿真项目（架构概览、chassis/server/gui/proto 等模块）

---

## 统计

| 分类 | 文件数 |
|------|--------|
| Transformer 与注意力 | 10 |
| 模型组件 | 7 |
| 训练与评估 | 4 |
| LLM 推理与架构 | 5 |
| TurboQuant | 8 |
| 机器人 | 2 |
| 其他 | 1 |
| Architecture | 2 |
| Testing | 2 |
| Infrastructure | 4 |
| Projects | 2 |
| **总计** | **47** |
