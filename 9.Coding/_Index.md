# 9.Coding 知识库索引

> 重组日期：2026-04-17

---

## 目录结构

```
9.Coding/
├── 01-深度学习/          CNN/RNN/经典网络/PyTorch/NLP/语音
├── 02-后端开发/          Nest.js、Supabase
├── 03-电商与建站/        WooCommerce、SEO、电商方案
├── 04-项目文档/          Ornitho-Vector、SIL、RSSHub等项目
├── 05-基础设施/          Docker、监控(Prometheus/Grafana)、部署运维
├── 06-工具与平台/        AI工具(Claude/OpenClaw)、开发工具、飞书、Electron
├── 07-网络安全/          Kali、WiFi、Root、攻防
├── 08-测试与质量/        HIL测试、BLC迁移、GitLab
├── 09-杂项与参考/        算法、演讲、密码管理、数学
```

---

## 01-深度学习

### CNN与卷积 (14 篇)
- 卷积核心概念 / 卷积代码实现 / 卷积填充与步幅
- 多输入输出通道卷积 / CNN局部性 / CNN平移不变性
- 填充与步幅 Q&A 李沐 / 神经网络参数管理
- 1×1 卷积通道降维（Inception核心）
- AlexNet / VGG / GoogLeNet Inception / NIN / ResNet

### RNN与序列 (6 篇)
- RNN基础 / LSTM / GRU
- 语言模型与N元语法 / Seq2Seq束搜索速记
- Memory Caching - RNN长记忆增强技术

### PyTorch (4 篇)
- 参数管理 Parameter vs Buffer / 模型文件读写 / 自定义层实现
- Cifar10数据集深度学习实战

### NLP与语音 (3 篇)
- NLP文本预处理核心流程
- FunASR语音识别模型详解 / FunASR AutoModel封装与底层推理框架

---

## 02-后端开发 (6 篇)
- Nest Hero Road 33 - 后端完整性分析报告 / 项目现状与优化方案
- Supabase 本地开发到云端部署
- Supabase 电商架构方案 / v3整合版 / vs Medusa差距分析

---

## 03-电商与建站 (9 篇)
- WooCommerce 技术架构详解 / 搭建完整指南 / 本地建站与部署 / 本地开发同步服务器
- 腾讯云部署WooCommerce完整指南(服务器版/SSH版)
- 为什么WooCommerce还在用PHP / SEO原理与电商实践
- 电商方案对比 - Supabase vs WordPress vs Medusa

---

## 04-项目文档

### Ornitho-Vector (4 篇)
- 项目技术方案 / 修复版v2.0 / 最终版v6.0 / v9.0代码详解

### software-in-loop (12 篇)
- 架构概览 / 核心与复杂度分析 / 历史Bug修复 / 新增车型适配
- chassis / for_local / for_remote / gui / proto / pybind_so / server / tools / utility

### Architecture (2 篇)
- HIL监控平台统一架构方案 / Pipeline代码架构全解

### 其他项目 (3 篇)
- RSSHub架构分析 / new-api项目分析 / tenacitOS项目分析

---

## 05-基础设施

### Docker (1 篇)
- Docker打镜像原理

### 监控体系 (7 篇)
- Prometheus & Grafana监控体系指南 / Prometheus-Grafana监控系统 / Grafana统一迁移方案
- Prometheus并发采集机制 / 多数据源监控部署 / TSDB压缩机制与数据丢失防护
- 时序数据库TSDB完全指南

### 部署与运维 (6 篇)
- SSH端口转发 - 访问远程网络资源 / SSH端口转发用法
- Cloudflare完整功能手册 / Cloudflare Workers vs Pages
- rsync命令详解 / VitePress构建静态文档网站

---

## 06-工具与平台

### AI工具 (6 篇)
- Claude_Code第三方API配置教程
- OpenClaw命令 / OpenClaw配置-自定义API和Skills / OpenClaw-微信配置笔记 / OpenClaw TTS vs Message对比
- NotebookLM CLI命令清单

### 开发工具 (9 篇)
- Homebrew Services完全指南 / JupyterLab vs Notebook对比
- JSONL格式详解 / Python Entrypoints详解 / JIT即时编译详解
- LSP (Language Server Protocol) / marimo下一代Python笔记本
- Next.js开发工具面板详解 / React Query详解
- pyJianYingDraft剪映自动化草稿工具

### 飞书与协作 (2 篇)
- 飞书应用文档创建-API实践 / lark-cli消息监听与处理教程

### Electron (1 篇)
- QuQu跨平台实现原理详解

---

## 07-网络安全 (4 篇)
- WiFi破解原理 - 通俗讲解
- 一加外接网卡搭建移动攻防平台 / 一加vs华为Root政策对比
- 荣耀V9安装Kali Linux完整教程

---

## 08-测试与质量 (5 篇)
- BLC迁移至hil_auto_test-分阶段方案 / HIL测试失败记录-待修复
- Auto Diagnosis HIL自动诊断平台教程 / HIL-Job优化方案
- GitLab MR假冲突-force-push后缓存未刷新

---

## 09-杂项与参考
- 1Password密码管理器 / C++ Traits编程
- FFD装箱算法 / 布朗运动 / Elon Musk 2003年创业演讲整理
- imgs/ (配图)