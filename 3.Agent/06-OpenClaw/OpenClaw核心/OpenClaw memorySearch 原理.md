# OpenClaw memorySearch 原理

> 创建日期:: 2026-02-27
> 标签:: #OpenClaw #Agent #向量检索 #记忆系统 #Embedding

---

## 🧠 核心架构

OpenClaw 的 memorySearch 是一个**基于向量检索的语义记忆系统**，允许 AI 智能体通过语义搜索历史笔记和对话记录。

```
┌─────────────────────────────────────────────────────────────┐
│                    Memory Search Pipeline                    │
├─────────────────────────────────────────────────────────────┤
│  1. 文件源 → 2. 分块 → 3. 嵌入 → 4. 索引 → 5. 检索 → 6. 排序  │
└─────────────────────────────────────────────────────────────┘
```

---

## 1️⃣ 数据源 (Sources)

索引的 Markdown 文件来源：

| 来源 | 路径 | 说明 |
|------|------|------|
| 长期记忆 | `MEMORY.md` | Curated 长期记忆 |
| 每日日志 | `memory/YYYY-MM-DD.md` | append-only 日常记录 |
| 额外路径 | `extraPaths` | 用户配置的额外目录 |
| 会话记录 | `sessions/*.jsonl` | 实验性，会话转录本 |

---

## 2️⃣ 分块 (Chunking)

文件被切分为重叠的文本块：

- **默认大小**: ~400 tokens
- **重叠**: 80 tokens
- **目的**: 保持上下文完整性，避免语义断裂

---

## 3️⃣ 嵌入 (Embeddings)

将文本块转换为向量，支持多种 provider：

| Provider | 模型 | 说明 |
|----------|------|------|
| `openai` | `text-embedding-3-small` | 默认，支持 Batch API |
| `gemini` | `gemini-embedding-001` | Google 原生 |
| `voyage` | Voyage AI | 可选 |
| `mistral` | Mistral AI | 可选 |
| `local` | GGUF 模型 | node-llama-cpp 本地运行 |

### 自动选择逻辑

```
1. 配置 local 且模型存在 → 本地
2. 尝试 OpenAI key
3. 尝试 Gemini key
4. 尝试 Voyage/Mistral
5. 全部失败 → 禁用
```

---

## 4️⃣ 索引存储 (SQLite + sqlite-vec)

### 数据库结构

```sql
-- 向量表 (使用 sqlite-vec 扩展)
CREATE VIRTUAL TABLE vec_chunks USING vec0(
  embedding FLOAT[1536],  -- 向量维度取决于模型
  metadata JSON
);

-- 全文搜索表 (FTS5)
CREATE VIRTUAL TABLE fts_chunks USING fts5(
  text, path, source
);
```

### 存储位置

```
~/.openclaw/memory/<agentId>.sqlite
```

### 缓存

支持 embedding cache，避免重复嵌入相同文本：

```json5
cache: { 
  enabled: true, 
  maxEntries: 50000 
}
```

---

## 5️⃣ 混合检索 (Hybrid Search)

### 检索流程

```
Vector Similarity (语义匹配) + BM25 (关键词匹配)
              ↓
       加权融合 (vectorWeight + textWeight)
              ↓
       可选：时间衰减 + MMR 多样性重排
              ↓
         Top-K 结果
```

### 为什么混合？

| 检索方式 | 擅长场景 | 示例 |
|----------|----------|------|
| **Vector** | 语义匹配 | "Mac Studio" ≈ "gateway 主机" |
| **BM25** | 精确 token | ID、错误码、变量名 |

### 加权融合公式

```
finalScore = vectorWeight × vectorScore + textWeight × textScore
```

默认权重：`vectorWeight: 0.7`, `textWeight: 0.3`

---

## 6️⃣ 后处理 (Post-processing)

### 时间衰减 (Temporal Decay)

```
decayedScore = score × e^(-λ × ageInDays)

其中 λ = ln(2) / halfLifeDays
```

**效果**（半衰期 30 天）：
- 今天：100%
- 7 天：~84%
- 30 天：50%
- 90 天：12.5%

**永久记忆**（不衰减）：
- `MEMORY.md`
- 非日期文件（如 `memory/projects.md`）

### MMR 重排 (Maximal Marginal Relevance)

**目的**: 减少重复结果，增加多样性

```
score = λ × relevance − (1−λ) × max_similarity_to_selected
```

- `lambda = 1.0` → 纯相关性
- `lambda = 0.0` → 最大多样性
- 默认：`0.7`（平衡）

---

## 🔧 完整配置示例

```json5
agents: {
  defaults: {
    memorySearch: {
      enabled: true,
      provider: "openai",
      model: "text-embedding-3-small",
      fallback: "gemini",
      
      // 混合搜索
      query: {
        hybrid: {
          enabled: true,
          vectorWeight: 0.7,
          textWeight: 0.3,
          candidateMultiplier: 4,
          mmr: { enabled: true, lambda: 0.7 },
          temporalDecay: { enabled: true, halfLifeDays: 30 }
        }
      },
      
      // 同步策略
      sync: {
        onSessionStart: true,
        onSearch: true,
        watch: true,
        intervalMinutes: 5,
        watchDebounceMs: 1500
      },
      
      // 缓存
      cache: { enabled: true, maxEntries: 50000 },
      
      // 分块
      chunking: { tokens: 400, overlap: 80 }
    }
  }
}
```

---

## 🛠️ 工具接口

### Agent 工具

| 工具 | 参数 | 说明 |
|------|------|------|
| `memory_search` | query, maxResults, minScore | 语义搜索 |
| `memory_get` | path, from, lines | 读取具体文件 |

### CLI 命令

```bash
# 查看状态
openclaw memory status
openclaw memory status --deep

# 手动索引
openclaw memory index --verbose

# 搜索
openclaw memory search "release checklist"

# 指定 agent
openclaw memory status --agent main
```

---

## 🔄 同步机制

### 文件监听

使用 chokidar 监听文件变化：
- 监听目标：`MEMORY.md` + `memory/**/*.md`
- 防抖延迟：1.5 秒

### 触发条件

| 触发器 | 说明 |
|--------|------|
| `onSessionStart` | 会话启动时 |
| `onSearch` | 搜索时（如果 dirty） |
| `watch` | 文件变化监听 |
| `intervalMinutes` | 定时任务 |
| Session Delta | 转录本达阈值（100KB 或 50 条） |

---

## 🎯 QMD 后端 (实验性)

可选替代 SQLite 的搜索后端：

```json5
memory: {
  backend: "qmd",
  qmd: {
    includeDefaultMemory: true,
    update: { interval: "5m", debounceMs: 15000 },
    limits: { maxResults: 6, timeoutMs: 4000 },
    paths: [
      { name: "docs", path: "~/notes", pattern: "**/*.md" }
    ]
  }
}
```

**特点**:
- 使用 [QMD](https://github.com/tobi/qmd) sidecar
- 本地运行 (Bun + node-llama-cpp)
- 自动下载 GGUF 模型
- 支持 BM25 + 向量 + reranking

---

## 📊 状态查询输出

```bash
openclaw memory status --deep
```

返回信息：
- ✅ provider/model
- ✅ 文件数/分块数
- ✅ 缓存状态（entries/maxEntries）
- ✅ vector/FTS 可用性
- ✅ fallback 状态
- ✅ batch 任务状态

---

## 🔗 相关文档

- [OpenClaw Memory 概念](/concepts/memory)
- [OpenClaw CLI memory](/cli/memory)
- [Session Management + Compaction](/reference/session-management-compaction)

---

## 💡 最佳实践

1. **定期整理 MEMORY.md** — 将日常笔记中的 durable facts 迁移到长期记忆
2. **启用混合搜索** — 同时获得语义匹配和精确匹配能力
3. **配置时间衰减** — 避免旧信息 outrank 新上下文
4. **使用缓存** — 减少重复 embedding 的 API 调用
5. **监控状态** — 定期 `openclaw memory status` 检查索引健康

---

## 🔧 手动索引命令

### 首次配置后建立索引

```bash
# 为指定 agent 建立索引
openclaw memory index --agent main

# 带详细输出
openclaw memory index --agent main --verbose

# 为所有 agent 索引
openclaw memory index
```

### 触发时机

| 场景        | 命令                                   | 说明                 |
| --------- | ------------------------------------ | ------------------ |
| **首次配置后** | `openclaw memory index --agent main` | 配置生效后必须执行一次        |
| **索引损坏**  | `openclaw memory index --force`      | 强制重建索引             |
| **检查状态**  | `openclaw memory status`             | 查看 `Dirty: yes/no` |
| **深度诊断**  | `openclaw memory status --deep`      | 检查 vector/FTS 可用性  |
|           |                                      |                    |

### 状态解读

```
Indexed: 9/9 files · 19 chunks  ← 已索引文件数/总文件数
Dirty: no                       ← no=索引最新，yes=有待索引变更
```

---

## 🤖 AI 自动索引机制

### 自动触发条件

OpenClaw 会在以下场景**自动触发索引**（无需手动执行）：

| 触发器       | 配置项                        | 默认值     | 说明                     |
| --------- | -------------------------- | ------- | ---------------------- |
| **会话启动**  | `sync.onSessionStart`      | `true`  | 新会话开始时检查并同步            |
| **搜索时**   | `sync.onSearch`            | `true`  | 执行 `memory_search` 时检查 |
| **文件监听**  | `sync.watch`               | `true`  | chokidar 监听文件变化        |
| **定时任务**  | `sync.intervalMinutes`     | `5`     | 每 5 分钟检查一次             |
| **会话转录本** | `sync.sessions.deltaBytes` | `100KB` | 达到阈值后后台索引              |

### 工作流程

```
文件变更 (MEMORY.md / memory/*.md)
       ↓
chokidar 监听 (防抖 1.5 秒)
       ↓
标记 Dirty
       ↓
等待触发条件 (onSearch / interval / onSessionStart)
       ↓
后台异步索引 (不阻塞对话)
       ↓
更新 SQLite + 缓存
```

### 配置示例

```json5
agents: {
  defaults: {
    memorySearch: {
      sync: {
        onSessionStart: true,   // 会话启动时同步
        onSearch: true,         // 搜索时同步
        watch: true,            // 文件监听
        watchDebounceMs: 1500,  // 防抖延迟
        intervalMinutes: 5,     // 定时检查
        sessions: {
          deltaBytes: 100000,   // 100KB 触发
          deltaMessages: 50     // 50 条消息触发
        }
      }
    }
  }
}
```

### 常见问题

**Q: 为什么配置后搜索不到内容？**
A: 首次配置需要手动执行一次 `openclaw memory index` 建立初始索引。

**Q: 修改笔记后多久能搜到？**
A: 默认 1.5 秒防抖 + 下次触发条件（搜索/定时/会话启动），通常 <5 分钟。

**Q: 如何强制重新索引？**
A: `openclaw memory index --force` 或修改 `memorySearch.chunking` 参数触发重建。
