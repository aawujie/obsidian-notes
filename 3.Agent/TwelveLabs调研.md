---
title: Twelve Labs API 调研
type: concept
created: 2026-06-12
updated: 2026-06-12
tags: [AI, video-understanding, API, 调研, 自动剪辑]
---

# Twelve Labs API 调研

## 概述

Twelve Labs 是一家专注于**视频理解**的 AI 公司，核心产品是视频原生多模态基础模型。其 API 平台提供视频索引、语义搜索、内容分析和自动分段等能力，定位为"视频领域的 OpenAI"。

---

## 1. 收费标准

### 1.1 Free Plan（免费额度）

| 项目 | 额度 |
|------|------|
| 总视频时长 | **600 分钟（10 小时）**，累计计算，不随删除重置 |
| 每个 Index 视频时长上限 | 10 小时 |
| 每个 Index 视频数量上限 | 100 个 |
| 用途 | 索引 + 分析共享这 10 小时额度 |
| 信用卡 | 不需要 |

注意：Playground 中的示例视频（约 1 小时）也计入免费额度。免费额度用完后不会自动升级，需手动升级到 Developer Plan。

### 1.2 Developer Plan（按量付费）

Developer Plan 有 3 个 Tier，根据月消费自动升级：

| Tier | 条件 |
|------|------|
| Tier 1 | 默认（添加支付方式后） |
| Tier 2 | 月消费 ≥ $200 |
| Tier 3 | 月消费 ≥ $400 |

#### Marengo（嵌入模型）

| 计费项 | 单价 | 说明 |
|--------|------|------|
| 视频索引 | **$0.042 / 分钟** | 一次性费用 |
| 基础设施（Embedding 存储） | **$0.0015 / 分钟 / 月** | 按月计费 |
| 搜索 API | **$4 / 1000 次查询** | |
| Embed API - 视频 | $0.042 / 分钟 | |
| Embed API - 音频 | $0.0083 / 分钟 | |
| Embed API - 图片 | $0.10 / 1000 次请求 | |
| Embed API - 文本 | $0.07 / 1000 次请求 | |

#### Pegasus（视频语言模型）

| 计费项 | 单价 | 说明 |
|--------|------|------|
| 视频索引 | $0.042 / 分钟 | 一次性费用 |
| 基础设施 | $0.0015 / 分钟 / 月 | |
| Analyze API - 输入视频 | **$0.0292 / 分钟** | 按分析时长计费 |
| Analyze API - 输出文本 | **$0.0075 / 1000 tokens** | |
| 视频分段 (Segmentation) | 视频时长 × 分段定义数量 | 如 1 小时视频 × 3 个分段定义 = 3 小时计费 |

#### 计费示例

以每月处理 600 分钟视频、1000 次搜索为例：

| 项目 | 计算 | 费用 |
|------|------|------|
| Marengo 索引 | 600 × $0.042 | $25.20 |
| 基础设施 | 600 × $0.0015 | $0.90 |
| 搜索 API | 1000 次查询 | $4.00 |
| **合计** | | **~$30.10/月** |

#### Pegasus 成本优势

Pegasus 的 Embedding 存储策略是其核心成本优势。相比之下：

- **Google Gemini 1.5 Pro** 缓存价格：$4.5 / 1M tokens / 小时存储
- **Twelve Labs Pegasus** 存储：$0.09 / 视频小时 / 月

对于需要反复查询同一视频的场景（如视频库检索），Pegasus 的存储成本约为 Gemini 的 **1/36000**。

### 1.3 Enterprise Plan

- 自定义价格，联系销售
- 自定义速率限制
- 专用云部署选项
- Organizations 功能（跨团队共享 Index）
- 发票不含费用明细（与 Developer 相反）

### 1.4 速率限制（Free vs Developer Tier 1）

| 类别 | Free Plan | Developer Tier 1 |
|------|-----------|-----------------|
| 索引 (DPD) | 3,000 分钟 | 3,000 分钟 |
| 索引 (RPM) | 60 | 60 |
| 搜索 (RPM) | 600 | 600 |
| 分析 (DPD) | 3,000 分钟 | 3,000 分钟 |
| 分析 (RPM) | 60 | 60 |
| 分析 (TPM) | 30K | 30K |
| Embed - 视频 (RPM) | 25 | 25 |

DPD = 每日分钟数, RPM = 每分钟请求数, TPM = 每分钟 Token 数

---

## 2. 技术原理

### 2.1 整体架构：感知 + 推理

Twelve Labs 的技术栈围绕两个核心模型构建，形成"感知 → 推理"流水线：

```
视频输入 → Marengo (感知：编码) → Pegasus (推理：生成) → 文本输出
                ↓
          嵌入向量（用于搜索/分类）
```

### 2.2 Marengo — 视频嵌入模型（感知层）

**当前版本：Marengo 3.0**（2025 年 11 月发布，Marengo 2.7 已于 2026 年 3 月 30 日下线）

#### 架构特点

- **Transformer-based 架构**，在单一统一框架中处理视频
- **多向量嵌入 (Multi-Vector Embedding)**：不同于传统方法将所有信息压缩为单一向量，Marengo 3.0 将视频分解为多个专用向量，分别捕获：
  - 视觉外观（对象、场景、动作）
  - 运动动态（动作时序、镜头运动）
  - 音频（语音、音乐、音效、静音）
  - OCR 文本（屏幕文字、字幕）
  - 标志/Logo 检测
- **512 维嵌入**：相比 Marengo 2.7 的 1024 维减少 50%，比 Amazon Nova (3072d) 小 6 倍，比 Google Vertex (1408d) 小 3 倍
- **训练数据**：使用 Pegasus 对 1000 万+ 视频进行重新标注，生成高质量描述

#### 核心能力

| 能力 | 说明 |
|------|------|
| 多模态理解 | 同时处理视频、音频、图像、文本 |
| 长视频支持 | 最多 **4 小时**视频，文件最大 **6GB** |
| 多语言 | 支持 **36 种语言**（不含英语）的跨语言搜索 |
| 组合搜索 | 图片 + 文字组合查询（Composed Multimodal Search） |
| 实体搜索 | 定义任意人物/物体，搜索其执行特定动作的片段 |
| 运动智能 | 识别足球、篮球、棒球、冰球等运动动作 |
| 小目标检测 | 可检测小至画面 10% 的对象 |
| 索引速度 | 通常为视频时长的 30-40%，Marengo 3.0 比 2.7 快 2 倍 |

#### Benchmark 表现

Marengo 3.0 综合基准得分 **78.5%**，对比竞品：
- Amazon Nova: 61.8%
- Google Vertex: 50.2%

在视频检索、图像检索、音频检索三个维度均领先。

### 2.3 Pegasus — 视频语言模型（推理层）

**当前版本：Pegasus 1.5**（API 文档中已使用；Pegasus 1.2 为 2025 年 2 月发布）

#### 架构

Pegasus 采用 **Encoder-Decoder** 架构，包含三个核心组件：

1. **Video Encoder（视频编码器）**
   - 由 Marengo 2.6 提供支持（Pegasus-1 论文）
   - 从视频帧和 ASR（语音识别）数据生成丰富的多模态嵌入
   - 捕获视觉和听觉的本质信息

2. **Video-Language Alignment Model（视频-语言对齐模型）**
   - 将视频嵌入映射到语言嵌入空间
   - 建立视频和文本的共享表示空间
   - 使用 Token 缩减技术优化长视频处理效率

3. **Large Language Model Decoder（大语言模型解码器）**
   - 接收对齐后的嵌入和用户提示
   - 生成文本输出（摘要、回答、描述等）
   - 使用高效注意力机制处理长上下文

#### 训练策略

- **两阶段训练**：预训练 + 指令微调
- **预训练阶段**：初始化 Video Encoder 和 LLM 的预训练权重，使用大规模多模态数据集训练
- **指令微调阶段**：使用专有多模态指令数据集进行监督微调
- **防灾难性遗忘**：选择性解冻参数 + 精确调整学习率

#### 核心能力

| 能力 | 说明 |
|------|------|
| 视频时长 | Pegasus 1.2 支持 1 小时，Pegasus 1.5 异步模式支持 2 小时 |
| 零样本视频问答 | 无需微调即可回答问题 |
| 视频摘要 | 生成简洁描述、亮点、章节 |
| 时序定位 | 精确识别事件时间戳 |
| 视频分段 | 自定义分段定义，提取结构化 JSON 元数据 |
| 视觉引用提示 | 支持箭头、框选等视觉标记引导模型关注 |
| 3D 空间理解 | 理解空间关系和导航路径 |
| 时序推理 | 维持事件时间顺序，理解叙事逻辑 |
| 真实世界知识 | 识别特定地点、物体、品牌、游戏等 |

#### 输出格式

- 开放式文本生成（Q&A、摘要、标题）
- 结构化 JSON（自定义字段）
- 时间戳分段（章节、亮点、场景）
- 多选生成（从列表中选择）

### 2.4 Marengo vs Pegasus 对比

| 维度 | Marengo 3.0 | Pegasus 1.5 |
|------|------------|------------|
| **角色** | 感知（编码） | 推理（生成） |
| **输出** | 嵌入向量 | 自然语言文本 |
| **用途** | 语义搜索、分类、相似度匹配 | 问答、摘要、分段、对话 |
| **交互方式** | 返回最匹配的视频片段 | 生成文本回答 |
| **处理速度** | 快（30-40%视频时长） | 较慢（需 LLM 推理） |
| **成本** | 低（一次索引，反复搜索） | 较高（每次分析均计费） |
| **视频时长** | 4 小时 | 1-2 小时 |
| **典型场景** | 视频库搜索、内容审核、推荐 | 自动生成章节、亮点提取、内容理解 |

### 2.5 部署方式

- **Twelve Labs SaaS**：直接 API 调用，Python/Node.js SDK
- **Amazon Bedrock**：AWS 托管，企业级集成，支持同步/异步推理
- 23 个 AWS 区域可用（全球跨区域推理）

---

## 3. 竞品对比

### 3.1 与 OpenAI Whisper 对比

| 维度 | Twelve Labs | OpenAI Whisper |
|------|-----------|----------------|
| **核心能力** | 视频全模态理解（视觉+音频+文本） | 纯音频转录（语音→文字） |
| **视觉理解** | 原生支持 | 不支持 |
| **时序推理** | 原生支持 | 不支持 |
| **视频搜索** | 语义搜索、以文搜视频 | 不支持 |
| **转录质量** | 通过 ASR 实现，非核心优势 | 业界领先的转录准确率 |
| **适用场景** | 视频内容理解、搜索、自动剪辑 | 字幕生成、音频转录 |
| **开源** | 闭源 | 开源 |

**结论**：Whisper 是 Twelve Labs 的**互补工具**而非竞争对手。在自动剪辑场景中，Whisper 可用于高质量字幕转录，Twelve Labs 用于视觉内容理解。

### 3.2 与 Gemini Vision 对比

| 维度 | Twelve Labs | Google Gemini Vision |
|------|-----------|---------------------|
| **模型定位** | 视频原生专用模型 | 通用多模态 LLM |
| **视频理解深度** | 深度优化，多向量嵌入 | 广度覆盖，非专用优化 |
| **时序定位** | 精确时间戳、分段 | 一般性时序理解 |
| **长视频** | 4 小时（Marengo 3.0） | Gemini 1.5 Pro 支持 1 小时+ |
| **视频搜索** | 原生语义搜索 + 混合搜索 | 不支持结构化搜索 |
| **存储成本** | $0.09/视频小时/月 | $4.5/1M tokens/小时（缓存） |
| **OCR 能力** | 支持但非最强 | Gemini 2.0 Flash 在 OCR 和视觉推理上更强 |
| **易用性** | 专用 API，中等集成难度 | 单一 API，低集成难度 |
| **适用场景** | 视频库索引、专业视频分析 | 快速视频问答、内容摘要 |

**结论**：Gemini 适合快速、灵活的视频问答场景；Twelve Labs 适合需要精确索引、语义搜索和专业视频分析的生产环境。

### 3.3 与 Amazon Nova / Google Vertex 对比

| 维度 | Marengo 3.0 | Amazon Nova | Google Vertex |
|------|-----------|------------|--------------|
| 综合基准 | **78.5%** | 61.8% | 50.2% |
| 嵌入维度 | **512d** | 3072d | 1408d |
| 存储效率 | 最优 | 6x 更大 | 3x 更大 |
| 视频原生 | 是 | 从图像模型扩展 | 从图像模型扩展 |
| 多语言 | 36 种语言 | 有限 | 有限 |

### 3.4 竞争定位总结

```
                        视频理解深度
                             ↑
              高  ── Twelve Labs (视频原生专用)
              │   Google Gemini (通用多模态)
              │   Amazon Nova (嵌入模型)
              │   OpenAI Whisper (仅音频)
              低  ──────────────────────────→
                        模态广度
              ← 音频 ──── 图像+文本 ──── 视频全模态 →
```

- **Twelve Labs** 是唯一从零开始为视频设计的原生模型，在**视频理解深度**和**时序推理**上具有独特优势
- **Gemini** 是通用多模态模型，能力广度大但视频专用优化不足
- **Whisper** 是纯音频工具，在视频理解中起辅助作用
- **Amazon Nova / Google Vertex** 是通用嵌入模型，视频场景下性能不如 Marengo

---

## 4. 在 WelooAI 自动剪辑场景中的应用

### 4.1 场景描述

WelooAI 自动剪辑场景的核心需求：**输入长视频 → 自动识别精彩片段 → 生成短视频剪辑**。

### 4.2 技术方案：Twelve Labs 全流程

```
┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────┐
│ 视频上传  │ →  │ Marengo 索引  │ →  │ Pegasus 分析  │ →  │ 剪辑生成  │
│ (Upload) │    │ (Embedding)  │    │ (Segment/QA) │    │ (FFmpeg) │
└──────────┘    └──────────────┘    └──────────────┘    └──────────┘
                      ↓                    ↓
              语义搜索索引          时间戳 + 描述 + JSON
              (可复用)              (结构化元数据)
```

#### Step 1: 视频上传与索引

```python
from twelvelabs import TwelveLabs

client = TwelveLabs(api_key="YOUR_API_KEY")

# 创建 Index
index = client.index.create(
    name="weloo-batch-001",
    models=[
        {"name": "pegasus1.5", "options": ["visual", "audio"]},
    ],
)

# 上传视频
task = client.task.create(
    index_id=index.id,
    file="input_video.mp4",
    language="zh"
)
task.wait_for_done()
```

#### Step 2: 视频分段（亮点检测）

使用 Pegasus 1.5 的 Segment API 自动检测精彩片段：

```python
from twelvelabs.types import AsyncResponseFormat, VideoContext_AssetId

# 定义分段规则
task = client.analyze_async.tasks.create(
    video=VideoContext_AssetId(asset_id=asset.id),
    model_name="pegasus1.5",
    analysis_mode="time_based_metadata",
    min_segment_duration=15.0,   # 最短 15 秒
    max_segment_duration=120.0,  # 最长 2 分钟
    response_format=AsyncResponseFormat(
        type="segment_definitions",
        segment_definitions=[
            {
                "id": "highlights",
                "description": "识别视频中的精彩片段：高能时刻、情绪爆发点、关键转折、笑点、动作高潮",
                "fields": [
                    {"name": "title", "type": "string", "description": "片段标题"},
                    {"name": "description", "type": "string", "description": "片段内容描述"},
                    {"name": "emotion", "type": "string", "description": "情绪类型",
                     "enum": ["exciting", "funny", "touching", "surprising", "intense"]},
                    {"name": "score", "type": "number", "description": "精彩程度评分 1-10"},
                    {"name": "hashtags", "type": "string", "description": "推荐标签，逗号分隔"},
                ]
            }
        ]
    )
)
```

#### Step 3: 剪辑生成

```python
import ffmpeg

for segment in result.segments:
    start = segment.start_time
    end = segment.end_time
    title = segment.metadata["title"]
    score = segment.metadata["score"]

    if score >= 7:  # 只保留高评分片段
        (
            ffmpeg
            .input("input_video.mp4", ss=start, to=end)
            .output(f"clips/{title}.mp4", vcodec="libx264", acodec="aac")
            .run()
        )
```

### 4.3 成本估算

以处理 **100 小时视频**，生成 **500 个剪辑片段**为例：

| 操作 | 计算 | 费用 |
|------|------|------|
| 视频索引 (Marengo) | 6000 分钟 × $0.042 | $252.00 |
| 基础设施 (月) | 6000 分钟 × $0.0015 | $9.00 |
| 视频分析 (Pegasus) | 6000 分钟 × $0.0292 | $175.20 |
| 分段定义 (假设 1 个) | 含在分析中 | $0 |
| 输出 Token (约 500K) | 500 × $0.0075 | $3.75 |
| **一次处理总费用** | | **~$439.95** |

此后，已索引的视频可反复搜索，仅需支付搜索 API 费用（$4/1000 次）。

### 4.4 与其他方案的集成建议

在 WelooAI 自动剪辑场景中，推荐 **Twelve Labs 为主 + 辅助工具** 的组合方案：

| 环节 | 推荐工具 | 原因 |
|------|---------|------|
| 语音转文字（字幕） | **OpenAI Whisper** | 转录质量最高，开源免费 |
| 视频内容理解 | **Twelve Labs Pegasus** | 视频原生，时序推理强 |
| 语义搜索/片段检索 | **Twelve Labs Marengo** | 多向量嵌入，搜索精度高 |
| 视觉 OCR/文字识别 | **Gemini 2.0 Flash** | OCR 能力更强（可选） |
| 视频剪辑 | **FFmpeg / moviepy** | 标准工具，稳定可靠 |
| 社交平台适配 | 自定义逻辑 | 按平台裁剪格式和时长 |

### 4.5 Twelve Labs 已有类似案例

Twelve Labs 官方和社区已有多个自动剪辑相关项目：

| 项目 | 功能 | 技术栈 |
|------|------|--------|
| **Video Highlight Generator** | 自动生成 YouTube 章节时间戳和亮点 | Twelve Labs + moviepy |
| **Cactus** | 长视频自动转短视频 Reels | Twelve Labs + GPT-4o |
| **AI Sports Recap** | 体育发布会自动生成亮点+摘要 | Pegasus + GPT-4o + Docker |
| **Dyn Sport** | 体育赛事自动亮点提取和分发 | Marengo 2.7 + Pegasus 1.2 |
| **TwelveSocial** | 长视频转社交媒体剪辑 | Twelve Labs + OpenAI + FFmpeg |
| **Stich Studios** | 体育视频元数据管理和亮点生成 | Twelve Labs + PostgreSQL |

---

## 5. 总结与建议

### 优势

1. **视频原生**：从零开始为视频设计的架构，非图像模型扩展，时序推理能力独特
2. **多向量嵌入**：比单一向量更精确地捕获视频的多模态信息
3. **成本可控**：一次索引后可反复查询，存储成本远低于 Gemini 等通用方案
4. **API 设计完善**：Segment API 直接输出结构化 JSON，天然适合自动剪辑流水线
5. **AWS Bedrock 集成**：企业级部署，无需自建基础设施

### 劣势

1. **闭源**：模型架构不完全公开，定制化受限
2. **生态较小**：相比 OpenAI/Google，社区和第三方工具较少
3. **中文支持**：36 种语言但中文性能待实测验证
4. **价格不低**：$0.042/分钟的视频索引成本在大量视频时累积较快
5. **OCR 不如 Gemini 2.0 Flash**：如需精确文字识别，可能需要辅助工具

### 建议

对于 WelooAI 自动剪辑场景，**推荐采用 Twelve Labs 作为核心视频理解引擎**，配合 Whisper 做字幕转录、FFmpeg 做剪辑。核心原因：

- Segment API 可以直接输出结构化亮点数据（时间戳+描述+标签+评分），无需额外后处理
- 多向量嵌入确保搜索精度，减少误检
- 一次索引后可反复低成本查询，适合持续处理视频库

如果预算有限，可以先用 Free Plan（600 分钟）验证效果，再升级到 Developer Plan。

---

## 参考来源

- [Twelve Labs 定价页](https://www.twelvelabs.io/pricing)
- [Twelve Labs 定价计算器](https://www.twelvelabs.io/pricing-calculator)
- [Twelve Labs FAQ](https://docs.twelvelabs.io/docs/resources/frequently-asked-questions)
- [Twelve Labs 速率限制](https://docs.twelvelabs.io/docs/get-started/rate-limits)
- [Marengo 2.7 介绍](https://www.twelvelabs.io/blog/introducing-marengo-2-7)
- [Marengo 3.0 介绍](https://www.twelvelabs.io/blog/marengo-3-0)
- [Pegasus 1.2 介绍](https://www.twelvelabs.io/blog/pegasus-1-2)
- [Pegasus-1 技术报告 (arXiv)](https://arxiv.org/html/2404.14687)
- [Twelve Labs 研究页面](https://www.twelvelabs.io/research)
- [Roboflow Twelve Labs 概述](https://blog.roboflow.com/twelve-labs-video-understanding/)
- [Twelve Labs 视频分段指南](https://docs.twelvelabs.io/v1.3/docs/guides/segment-videos)
- [YouTube 章节亮点生成器教程](https://www.twelvelabs.io/blog/youtube-chapter-timestamp)
- [Twelve Labs 媒体与娱乐案例](https://docs.twelvelabs.io/docs/resources/from-the-community/media-and-entertainment)
- [Dyn Sport 案例研究](https://www.twelvelabs.io/case-studies/dyn-sport)
- [AWS Marengo 3.0 公告](https://aws.amazon.com/about-aws/whats-new/2025/10/twelvelabs-marengo3-embed-amazon-bedrock/)