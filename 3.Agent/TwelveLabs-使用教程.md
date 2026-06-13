---
title: TwelveLabs 视频理解平台使用教程
type: tutorial
created: 2026-06-13
updated: 2026-06-13
tags:
  - twelve-labs
  - video
  - AI
  - API
  - 视频理解
  - 语义搜索
---

# TwelveLabs 视频理解平台使用教程

> API Key: `tlk_3R…56EH`（存于 TOOLS.md）
> 文档：https://docs.twelvelabs.io

## 概述

TwelveLabs 是一个视频理解平台，提供两个核心能力：

- **Marengo 模型**：视频语义搜索（搜文本 → 找到视频中的对应片段）
- **Pegasus 模型**：视频内容分析（根据 prompt 生成摘要、剧情描述、角色识别等）

## 架构概念

```
API Key → Index (索引) → Video (上传视频) → Task (索引任务)
                                    ↓
                              Search (语义搜索)
                              Analyze (Pegasus 分析)
```

- **Index**：视频容器，创建时绑定模型（Marengo 或 Marengo+Pegasus）
- **Task**：上传视频后自动触发的索引任务，等待 `ready` 后可用
- **Search**：Marengo 模型，文本搜视频片段，返回时间戳+语音转录
- **Analyze**：Pegasus 模型，根据 prompt 分析视频内容，生成文本

## 1. 创建 Index

### 仅搜索（Marengo）

```bash
curl -s -X POST "https://api.twelvelabs.io/v1.3/indexes" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "index_name": "My Index",
    "models": [
      {
        "model_name": "marengo3.0",
        "model_options": ["visual", "audio"]
      }
    ],
    "addons": ["thumbnail"]
  }'
```

### 搜索 + 分析（Marengo + Pegasus）

```bash
curl -s -X POST "https://api.twelvelabs.io/v1.3/indexes" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "index_name": "Pegasus Analysis Index",
    "models": [
      {
        "model_name": "marengo3.0",
        "model_options": ["visual", "audio"]
      },
      {
        "model_name": "pegasus1.2",
        "model_options": ["visual", "audio"]
      }
    ],
    "addons": ["thumbnail"]
  }'
```

返回 `_id` 即为 index_id。

**注意**：Pegasus 的 index 有 90 天过期时间（`expires_at` 字段）。

### 查看已有 Index

```bash
curl -s "https://api.twelvelabs.io/v1.3/indexes" \
  -H "x-api-key: $API_KEY"
```

## 2. 上传视频

### 上传方式（multipart/form-data）

```bash
curl -s -X POST "https://api.twelvelabs.io/v1.3/tasks" \
  -H "x-api-key: $API_KEY" \
  -F "index_id=$INDEX_ID" \
  -F "video_file=@/path/to/video.mp4"
```

返回 `video_id`。

### 检查索引状态

```bash
curl -s "https://api.twelvelabs.io/v1.3/tasks/$TASK_ID" \
  -H "x-api-key: $API_KEY" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['status'])"
```

等待 `status: ready` 后即可搜索/分析。

**注意**：该端点已标记为 Legacy，未来会拆分为上传 + 索引两步。但目前仍可用。

## 3. 语义搜索（Marengo）

### 文本搜索

```bash
curl -s -X POST "https://api.twelvelabs.io/v1.3/search" \
  -H "x-api-key: $API_KEY" \
  -F "index_id=$INDEX_ID" \
  -F "query_text=外星人 斯皮尔伯格" \
  -F "search_options=visual" \
  -F "search_options=audio"
```

返回字段：

| 字段 | 含义 |
|:---|:---|
| `rank` | 排名 |
| `score` | 相关性分数 |
| `start` / `end` | 片段起止时间（秒） |
| `video_id` | 所属视频 |
| `thumbnail_url` | 该时间点的缩略图 |
| `transcription` | 该片段的语音转录文本 |

### 提取关键信息

```bash
curl -s ... | python3 -c "
import json,sys
d=json.load(sys.stdin)
for item in d['data'][:5]:
    print(f\"#{item['rank']} [{item['start']:.1f}s] {item['transcription'][:80]}\")
"
```

## 4. 视频分析（Pegasus）

### 提交分析任务

```bash
curl -s -X POST "https://api.twelvelabs.io/v1.3/analyze/tasks" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "VIDEO_ID",
    "index_id": "INDEX_ID",
    "prompt": "请详细描述这个视频的剧情：发生了什么、有哪些主要角色、关键情节转折点"
  }'
```

返回 `task_id`。

### 查询分析结果

```bash
curl -s "https://api.twelvelabs.io/v1.3/analyze/tasks/$TASK_ID" \
  -H "x-api-key: $API_KEY"
```

状态流程：`queued` → `processing` → `ready`

结果在 `result.data` 字段中（Unicode 编码，需解码）。

### 提取结果

```bash
curl -s "https://api.twelvelabs.io/v1.3/analyze/tasks/$TASK_ID" \
  -H "x-api-key: $API_KEY" \
  | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(d.get('result',{}).get('data',''))
"
```

## 5. 已验证效果

| 视频 | 时长 | 搜索测试 | 分析测试 |
|:---|:---|:---|:---|
| 斯皮尔伯格《解禁日》解析 | 3分20秒 | ✅ "外星人"→命中语音转录 | 未测（需Pegasus index） |
| 潜意识编程赌局短片 | 5分 | ✅ "number 55 jersey intuition"→精准命中55号球衣片段 | ✅ Pegasus正确识别了Will Smith、剧情反转、潜意识编程机制 |

**Pegasus 分析质量**：能识别演员（Will Smith）、角色名（Mr. Lee Yuan）、精确时间点（3分22秒转折、4分13秒揭秘）、核心机制（潜意识暗示/环境编程）。

## 6. 当前 Index 清单

| Index ID | 名称 | 模型 | 视频数 |
|:---|:---|:---|:---|
| `6a2cd452f383f92c3dad781b` | My Index (Default) | marengo3.0 | 2 |
| `6a2cdc940d802ff693542170` | Pegasus Analysis Index | marengo3.0 + pegasus1.2 | 1 |

## 7. 常用命令速查

```bash
API_KEY=***

# 列出所有 index
curl -s "https://api.twelvelabs.io/v1.3/indexes" -H "x-api-key: $API_KEY"

# 上传视频
curl -s -X POST "https://api.twelvelabs.io/v1.3/tasks" \
  -H "x-api-key: $API_KEY" \
  -F "index_id=$INDEX_ID" \
  -F "video_file=@video.mp4"

# 搜索视频
curl -s -X POST "https://api.twelvelabs.io/v1.3/search" \
  -H "x-api-key: $API_KEY" \
  -F "index_id=$INDEX_ID" \
  -F "query_text=搜索关键词" \
  -F "search_options=visual" \
  -F "search_options=audio"

# 分析视频
curl -s -X POST "https://api.twelvelabs.io/v1.3/analyze/tasks" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"video_id":"VIDEO_ID","index_id":"INDEX_ID","prompt":"你的分析问题"}'

# 查询分析结果
curl -s "https://api.twelvelabs.io/v1.3/analyze/tasks/$TASK_ID" \
  -H "x-api-key: $API_KEY"
```

## 8. 踩坑记录

1. **Search 必须用 `multipart/form-data`**，不能用 `application/json`。参数名是 `query_text`，不是 `query`。
2. **Analyze 必须用 `application/json`**，不能用 `multipart/form-data`。
3. **Pegasus 版本**：当前 API 支持 `pegasus1.2`，不是 `pegasus1.5`。
4. **默认 Index 只有 Marengo**，不能做分析，需要单独创建带 Pegasus 的 index。
5. **Pegasus Index 有 90 天过期**，注意 `expires_at` 字段。
6. **上传视频的 `/tasks` 端点已标记 Legacy**，未来会拆分为 `/assets` 上传 + `/indexed-assets` 索引两步。
7. **分析结果在 `result.data`** 字段，不是 `analysis_result`。