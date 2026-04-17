# LLM 推理框架对比

> **整理时间：** 2026-04-01

---

## 1. 主流框架概览

| 框架 | 平台 | 硬件 | 定位 | 核心特点 |
|------|------|------|------|----------|
| **vLLM** | Linux/Win | Nvidia GPU | 生产服务 | PagedAttention、高吞吐、OpenAI API 兼容 |
| **MLX** | macOS | Apple Silicon | 本地开发 | 统一内存、Apple 原生优化 |
| **llama.cpp** | 全平台 | CPU/GPU/APU | 边缘部署 | GGUF 格式、量化、极低资源 |
| **TensorRT-LLM** | Linux | Nvidia GPU | 生产优化 | Nvidia 官方、极致性能 |
| **TGI** | Linux | Nvidia GPU | 生产服务 | HuggingFace 出品、多模型支持 |
| **DeepSpeed** | Linux | Nvidia GPU | 训练+推理 | 微软出品、大规模分布式 |
| **OpenLLM** | 全平台 | 多硬件 | 快速部署 | BentoML 出品、易用 |
| **SGLang** | Linux | Nvidia GPU | 编程框架 | 结构化生成、多轮对话优化 |
| **LM Studio** | macOS/Win | 多硬件 | 桌面应用 | GUI、一键运行、本地优先 |
| **Ollama** | macOS/Win/Linux | 多硬件 | 本地运行 | 极简命令行、预置模型 |

---

## 2. 详细对比

### 2.1 vLLM（生产环境首选）

**定位：** 高性能 LLM 推理和服务引擎

**代码示例：**
```python
from vllm import LLM

# 启动服务
llm = LLM(model="meta-llama/Llama-2-7b")
output = llm.generate("Hello, my name is")

# 或使用 API 服务
# python -m vllm.entrypoints.openai.api_server --model llama-2-7b
```

**核心特性：**
| 特性 | 说明 |
|------|------|
| **PagedAttention** | 优化 KV Cache 内存管理，减少碎片 |
| **Continuous Batching** | 连续批处理，提高吞吐量 |
| **Tensor Parallelism** | 多 GPU 张量并行 |
| **Pipeline Parallelism** | 流水线并行 |
| **OpenAI API** | 兼容 OpenAI API 格式 |

**优点：**
- 吞吐量业界最高
- 成熟稳定，生产验证
- 生态丰富，社区活跃
- 多 GPU 支持完善

**缺点：**
- 仅限 Nvidia GPU
- Linux 为主，Windows 支持有限
- 配置相对复杂

**适用场景：**
- 生产环境部署
- 高并发 API 服务
- 多 GPU 集群

---

### 2.2 MLX（Mac 最优选择）

**定位：** Apple Silicon 优化框架

**代码示例：**
```python
import mlx.core as mx
from mlx_lm import load, generate

# 加载模型
model, tokenizer = load("mlx-community/Llama-2-7B-mlx")

# 生成
response = generate(model, tokenizer, "Hello, how are you?")
```

**核心特性：**
| 特性 | 说明 |
|------|------|
| **Unified Memory** | CPU/GPU 共享内存，无需拷贝 |
| **Metal** | 原生 Metal 性能优化 |
| **Lazy Evaluation** | 延迟计算，自动图优化 |
| **NumPy-like API** | 类似 NumPy 的 API 设计 |

**优点：**
- Mac 上性能最优
- 统一内存架构，大模型友好
- API 简洁，易于使用
- Apple 官方支持

**缺点：**
- 仅限 Apple Silicon
- 生态较新，功能有限
- 不支持 CUDA

**适用场景：**
- Mac 本地开发
- 个人实验/研究
- 不想用云端 API

---

### 2.3 llama.cpp（最通用）

**定位：** 跨平台边缘推理

**代码示例：**
```bash
# 命令行
./main -m llama-2-7b.gguf -p "Hello" -n 100

# Python
from llama_cpp import Llama

llm = Llama(model_path="llama-2-7b.gguf", n_gpu_layers=35)
output = llm("Hello, my name is", max_tokens=100)
```

**核心特性：**
| 特性 | 说明 |
|------|------|
| **GGUF Format** | 专用量化格式，高效存储 |
| **Quantization** | 支持 2-8 bit 量化 |
| **Cross-Platform** | C++ 实现，全平台支持 |
| **Low Resource** | CPU 也能跑大模型 |

**优点：**
- 纯 C++，无依赖
- 支持 CPU（ARM/x86）
- 手机/嵌入式都能跑
- 量化选择丰富

**缺点：**
- 性能不如 GPU 优化框架
- API 较底层
- 开发体验一般

**适用场景：**
- 边缘设备部署
- 低资源环境
- 移动端推理
- 嵌入式系统

---

### 2.4 TensorRT-LLM（Nvidia 最强）

**定位：** Nvidia GPU 极致优化

**代码示例：**
```python
from tensorrt_llm import LLM

llm = LLM(model="llama-2-7b")
output = llm.generate("Hello")
```

**核心特性：**
| 特性 | 说明 |
|------|------|
| **FP8/INT8** | 极致量化优化 |
| **Kernel Fusion** | 算子融合，减少开销 |
| **Multi-GPU** | 多 GPU 并行 |
| **Nvidia Optimized** | 官方深度优化 |

**优点：**
- Nvidia 官方出品
- 极致性能
- 生产级稳定

**缺点：**
- 仅限 Nvidia GPU
- 配置复杂
- 商业许可限制
- 学习曲线陡峭

**适用场景：**
- 极致性能需求
- 企业级部署
- Nvidia 生态深度用户

---

### 2.5 TGI (Text Generation Inference)

**定位：** HuggingFace 生产服务

**代码示例：**
```bash
# Docker 启动
docker run -p 8080:80 \
  -v $(pwd)/data:/data \
  ghcr.io/huggingface/text-generation-inference:2.0 \
  --model-id meta-llama/Llama-2-7b

# API 调用
curl http://localhost:8080/generate \
  -X POST \
  -d '{"inputs":"Hello","parameters":{"max_new_tokens":100}}'
```

**核心特性：**
| 特性 | 说明 |
|------|------|
| **Multi-Model** | 支持多个模型同时服务 |
| **Streaming** | 流式输出支持 |
| **HuggingFace Hub** | 直接加载 Hub 模型 |
| **Production Ready** | 生产级特性 |

**优点：**
- HuggingFace 官方
- 与 HF 生态无缝集成
- 多模型支持
- 功能丰富

**缺点：**
- 主要支持 Nvidia
- 资源占用较高
- 启动较慢

**适用场景：**
- HuggingFace 生态用户
- 多模型服务
- 快速原型验证

---

### 2.6 Ollama（最简单）

**定位：** 本地一键运行

**代码示例：**
```bash
# 安装
curl -fsSL https://ollama.com/install.sh | sh

# 运行模型
ollama run llama2
ollama run qwen:7b
ollama run gemma:2b

# 自定义模型 (Modelfile)
cat > Modelfile << EOF
FROM llama2
PARAMETER temperature 0.7
SYSTEM "You are a helpful assistant."
EOF
ollama create my-model -f Modelfile
```

**核心特性：**
| 特性 | 说明 |
|------|------|
| **One-Click** | 一键安装运行 |
| **Model Hub** | 内置模型仓库 |
| **Modelfile** | 自定义模型配置 |
| **Cross-Platform** | 全平台支持 |

**优点：**
- 极简命令行
- 自动下载模型
- 零配置
- 本地优先

**缺点：**
- 性能非最优
- 功能较简单
- 主要本地使用

**适用场景：**
- 快速体验
- 本地聊天
- 非技术用户
- 快速原型

---

### 2.7 LM Studio（GUI 首选）

**定位：** 图形界面模型运行

**特点：**
- 一键下载/运行模型
- 内置聊天界面
- 支持 GGUF 格式
- 可视化参数调整
- 本地优先设计

**优点：**
- 图形界面友好
- 无需命令行
- 适合非技术用户
- 快速上手

**缺点：**
- 功能有限
- 性能一般
- 高级功能缺失

**适用场景：**
- 非技术用户
- 可视化操作
- 快速体验

---

## 3. 性能对比

| 框架 | 吞吐量 | 延迟 | 易用性 | 硬件支持 | 成熟度 |
|------|--------|------|----------|----------|--------|
| **vLLM** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Nvidia | ⭐⭐⭐⭐⭐ |
| **MLX** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Apple | ⭐⭐⭐ |
| **llama.cpp** | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | 全平台 | ⭐⭐⭐⭐ |
| **TensorRT-LLM** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | Nvidia | ⭐⭐⭐⭐ |
| **TGI** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Nvidia | ⭐⭐⭐⭐ |
| **Ollama** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 全平台 | ⭐⭐⭐ |
| **LM Studio** | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | 桌面 | ⭐⭐⭐ |

---

## 4. 选择决策树

```
开始
│
├─ 生产环境部署？
│  ├─ 是 → Nvidia GPU？
│  │  ├─ 是 → 极致性能？
│  │  │  ├─ 是 → TensorRT-LLM
│  │  │  └─ 否 → vLLM（推荐）
│  │  └─ 否 → llama.cpp / TGI
│  └─ 否 → 继续
│
├─ Mac 用户？
│  ├─ 是 → MLX（推荐）
│  └─ 否 → 继续
│
├─ 本地快速体验？
│  ├─ 是 → 命令行？
│  │  ├─ 是 → Ollama
│  │  └─ 否 → LM Studio
│  └─ 否 → 继续
│
├─ 边缘设备/低资源？
│  ├─ 是 → llama.cpp
│  └─ 否 → 继续
│
└─ 默认推荐 → vLLM（服务器）/ Ollama（本地）
```

---

## 5. 场景推荐

| 场景 | 推荐框架 | 理由 |
|------|----------|------|
| **生产 API 服务** | vLLM | 吞吐量最高，生态成熟 |
| **Mac 本地开发** | MLX | Apple 原生优化 |
| **快速体验/聊天** | Ollama | 极简，零配置 |
| **非技术用户** | LM Studio | GUI 友好 |
| **边缘设备** | llama.cpp | 极低资源 |
| **Nvidia 极致性能** | TensorRT-LLM | 官方深度优化 |
| **多模型服务** | TGI | HuggingFace 生态 |
| **手机/嵌入式** | llama.cpp | 跨平台，轻量化 |

---

## 6. 快速开始命令

### vLLM
```bash
pip install vllm
python -m vllm.entrypoints.openai.api_server --model llama-2-7b
```

### MLX
```bash
pip install mlx-lm
python -c "from mlx_lm import load, generate; m,t=load('mlx-community/Llama-2-7B-mlx'); print(generate(m,t,'Hello'))"
```

### llama.cpp
```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make
./main -m model.gguf -p "Hello"
```

### Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama run llama2
```

### TGI
```bash
docker run -p 8080:80 ghcr.io/huggingface/text-generation-inference:2.0 --model-id llama-2-7b
```

---

## 7. 总结

| 框架 | 一句话描述 |
|------|-----------|
| **vLLM** | 生产环境首选，吞吐量之王 |
| **MLX** | Mac 用户必备，Apple 原生 |
| **llama.cpp** | 万能钥匙，哪里都能跑 |
| **TensorRT-LLM** | Nvidia 极致性能 |
| **TGI** | HuggingFace 生态服务 |
| **Ollama** | 最简单，一键运行 |
| **LM Studio** | GUI 用户友好 |

**选择原则：**
1. **生产 + Nvidia** → vLLM
2. **Mac** → MLX
3. **快速体验** → Ollama
4. **低资源** → llama.cpp
5. **非技术** → LM Studio

---

*本笔记整理了主流 LLM 推理框架的详细对比，包括特性、优缺点、适用场景和快速开始命令。*
