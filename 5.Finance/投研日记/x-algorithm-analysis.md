# X-Algorithm 推荐系统源码分析报告

> 分析日期：2026-05-16 | 仓库：x-algorithm | X For You Feed Algorithm

---

## 一、概览

### 1.1 仓库目的

这是 X（原 Twitter）"For You"推荐信息流的**核心推荐系统**开源仓库。它将用户关注账号的内容（In-Network）与机器学习发现的全球语料库内容（Out-of-Network）融合，使用基于 **Grok-1 开源模型**移植而来的 Transformer 进行统一排序。

### 1.2 整体架构

```
┌────────────────────────────────────────────────────────────────────┐
│                          X 客户端请求                               │
└────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│                      HOME MIXER (Rust)                             │
│   Orchestration Layer - gRPC Service                              │
│                                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ Query        │  │ Candidate    │  │ Filter       │              │
│  │ Hydrators    │  │ Sources      │  │ (14 filters) │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ Scorer       │  │ Selector     │  │ Side         │              │
│  │ (3 scorers)  │  │ (TopK)       │  │ Effects      │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
└────────────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌──────────────┐  ┌─────────────────┐  ┌──────────────────┐
│   THUNDER    │  │    PHOENIX      │  │      GROX        │
│  (Rust)      │  │   (Python)      │  │    (Python)      │
│              │  │                 │  │                  │
│ In-Memory    │  │ Two-Stage ML:   │  │ Content          │
│ Post Store   │  │ 1. Retrieval    │  │ Understanding:   │
│ + Kafka      │  │    (Two-Tower)  │  │ - Spam Detection │
│ Ingestion    │  │ 2. Ranking      │  │ - Safety/PTOS    │
│              │  │    (Grok Trans- │  │ - Embedding      │
│              │  │     former)     │  │ - Classification │
└──────────────┘  └─────────────────┘  └──────────────────┘
```

### 1.3 技术栈

| 组件 | 语言 | 框架/关键依赖 |
|-------|------|--------------|
| Home Mixer | Rust | Tonic (gRPC), Tokio, DashMap |
| Thunder | Rust | DashMap, Kafka, Tonic (gRPC) |
| Candidate Pipeline | Rust | Tokio, Tonic, Tracing |
| Phoenix | Python | JAX, Haiku (DeepMind), NumPy |
| Grox | Python | asyncio, gRPC, multiprocessing |

### 1.4 关键设计原则

1. **零手工特征工程**：完全由 Grok Transformer 从用户行为序列中学习相关性
2. **Candidate Isolation**：排序时候选之间不能互相关注，确保分数一致性
3. **Hash-Based Embeddings**：多哈希函数做嵌入查找，避免大规模嵌入表的存储
4. **多动作预测**：预测 15+ 种行为的概率，加权组合为最终排序分数
5. **可组合 Pipeline 架构**：Source/Hydrator/Filter/Scorer/Selector 的模块化设计

---

## 二、各模块详解

### 2.1 Candidate Pipeline（候选管道框架）

**语言：** Rust | **位置：** `candidate-pipeline/` | **行数：** ~500 lines

这是整个推荐系统的基础框架，定义了 7 个核心 trait，形成了一个可组合的流水线架构：

#### 2.1.1 核心 Traits

| Trait | 文件 | 职责 | 执行方式 |
|-------|------|------|---------|
| `QueryHydrator` | `query_hydrator.rs` | 从外部服务获取用户上下文（关注列表、行为序列等） | 并行 |
| `Source` | `source.rs` | 获取候选内容（来自 Thunder、Phoenix 等） | 并行 |
| `Hydrator` | `hydrator.rs` | 丰富候选内容元信息（帖子数据、作者信息、媒体等） | 并行 |
| `Filter` | `filter.rs` | 过滤不合格候选（去重、去屏蔽、去旧帖等） | 串行（顺序重要） |
| `Scorer` | `scorer.rs` | 打分排序（ML 预测、加权组合、多样性） | 串行 |
| `Selector` | `selector.rs` | 按分数排序并截取 Top-K | 单次 |
| `SideEffect` | `side_effect.rs` | 异步副作用（缓存、日志、Kafka 发布） | 并行（异步） |

#### 2.1.2 执行引擎（`candidate_pipeline.rs`）

```rust
async fn execute(&self, query: Q) -> PipelineResult<Q, C> {
    let hydrated_query = self.hydrate_query(query).await;           // 1. 并行水合查询
    let hydrated_query = self.hydrate_dependent_query(hydrated_query).await; // 2. 依赖查询水合
    let candidates = self.fetch_candidates(&hydrated_query).await;  // 3. 并行获取候选
    let hydrated_candidates = self.hydrate(&hydrated_query, candidates).await; // 4. 并行水合候选
    let (kept, filtered) = self.filter(&hydrated_query, hydrated_candidates); // 5. 串行过滤
    let scored = self.score(&hydrated_query, kept).await;           // 6. 串行打分
    let result = self.select(&hydrated_query, scored);              // 7. 选择 Top-K
    let post_selected = self.hydrate_post_selection(...).await;     // 8. 后选水合
    let (final, post_filtered) = self.filter_post_selection(...);   // 9. 后选过滤
    self.run_side_effects(input);                                   // 10. 异步副作用
}
```

**关键工程实现：**
- Hydrator/Source 并行执行通过 `futures::future::join_all` 实现
- Filter 串行执行保证过滤顺序（如先去重再检查）
- 每个 stage 都有 tracing span 和 metrics 埋点
- `enable()` 方法支持运行时通过 `Decider` 动态开关组件

### 2.2 Home Mixer（编排层）

**语言：** Rust | **位置：** `home-mixer/` | **行数：** ~15,000+ lines

Home Mixer 是 For You Feed 的总指挥中心，它包含两个核心 Pipeline 实现：

#### 2.2.1 PhoenixCandidatePipeline（主页排序流水线）

这是**最核心的流水线**，完整实现了从候选生成到最终排序的全流程：

**Query Hydrators (15个):**
| Hydrator | 获取数据 |
|----------|---------|
| `ScoringSequenceQueryHydrator` | 用户行为序列（用于 Phoenix Ranker） |
| `RetrievalSequenceQueryHydrator` | 用户行为序列（用于 Phoenix Retrieval） |
| `FollowedUserIdsQueryHydrator` | 关注用户列表 |
| `BlockedUserIdsQueryHydrator` | 屏蔽用户列表 |
| `MutedUserIdsQueryHydrator` | 静音用户列表 |
| `SubscribedUserIdsQueryHydrator` | 订阅用户列表 |
| `CachedPostsQueryHydrator` | Redis 缓存的待展示帖子 |
| `MutualFollowQueryHydrator` | 双向关注关系 |
| `ImpressionBloomFilterQueryHydrator` | 曝光 Bloom Filter |
| `UserDemographicsQueryHydrator` | 用户人口统计信息 |
| `FollowedGrokTopicsQueryHydrator` | 关注的 Grok 主题 |
| `FollowedStarterPacksQueryHydrator` | 关注的 Starter Pack |
| `InferredGrokTopicsQueryHydrator` | 推断的 Grok 主题 |
| `IpQueryHydrator` | IP 地理位置 |
| `UserInferredGenderQueryHydrator` | 推断的性别 |

**Candidate Sources (6个):**
| Source | 来源 | 类型 |
|--------|------|------|
| `ThunderSource` | Thunder 内存存储 | In-Network |
| `TweetMixerSource` | TweetMixer 服务 | 混合 |
| `PhoenixSource` | Phoenix 检索服务 | Out-of-Network |
| `PhoenixTopicsSource` | Phoenix 主题检索 | 主题化 OON |
| `PhoenixMOESource` | Phoenix MoE 检索 | MoE 变体 |
| `CachedPostsSource` | Redis 缓存 | 缓存 |

**Candidate Hydrators (10个):**
| Hydrator | 注入数据 |
|----------|---------|
| `InNetworkCandidateHydrator` | In/Out-Network 标记，Mutual Follow 信息 |
| `CoreDataCandidateHydrator` | 帖子核心文本 + 媒体数据 |
| `QuoteHydrator` | 引用推文展开 |
| `VideoDurationCandidateHydrator` | 视频时长 |
| `HasMediaHydrator` | 媒体类型检测（图片/视频/GIF） |
| `SubscriptionHydrator` | 订阅内容标记 |
| `GizmoduckCandidateHydrator` | 作者完整信息（用户名、认证、粉丝数） |
| `BlockedByHydrator` | 作者是否屏蔽了当前用户 |
| `FilteredTopicsHydrator` | 用户过滤的主题 |
| `LanguageCodeHydrator` | 内容语言代码 |

**Pre-Scoring Filters (14个):**
```
DropDuplicatesFilter → CoreDataHydrationFilter → AgeFilter → SelfTweetFilter
→ RetweetDeduplicationFilter → IneligibleSubscriptionFilter →
PreviouslySeenPostsFilter → PreviouslySeenPostsBackupFilter →
PreviouslyServedPostsFilter → MutedKeywordFilter → AuthorSocialgraphFilter
→ VideoFilter → TopicIdsFilter → NewUserTopicIdsFilter
```

**Scorers (3个，串行执行):**

1. **PhoenixScorer** - 调用 Phoenix ML 服务获取 19 维预测分数
2. **RankingScorer** - 包含三个子评分器：
   - **WeightedScorer**：加权组合 19 个预测概率
   - **AuthorDiversityScorer**：衰减来自同一作者的连续帖子分数
   - **OONScorer**：调整 Out-of-Network 内容分数
3. **VMRanker** - 视频内容额外排序

**Post-Selection Filters (3个):**
- `VFFilter` - Visibility Filtering（删除/垃圾/暴力/血腥）
- `AncillaryVFFilter` - 辅助 VF 过滤
- `DedupConversationFilter` - 会话线程去重

**Side Effects (6个):**
- `PhoenixExperimentsSideEffect` - 实验数据写入 Kafka
- `RerankingKafkaSideEffect` - 重排序数据写入 Kafka
- `RedisPostCandidateCacheSideEffect` - 候选缓存到 Redis
- `ScoredStatsSideEffect` - 打分统计记录
- `MutualFollowStatsSideEffect` - 互关统计
- `PhoenixRequestCacheSideEffect` - Phoenix 请求缓存

#### 2.2.2 ForYouCandidatePipeline（顶层编排流水线）

这是一个**更上层的编排**，它调用 `ScoredPostsServer`（内部运行 PhoenixCandidatePipeline），然后在此基础上：

- 添加 **AdsSource** - 广告候选注入
- 添加 **WhoToFollowSource** - 推荐关注
- 添加 **PromptsSource** - 提示类内容
- 添加 **PushToHomeSource** - 推送内容
- 使用 **BlenderSelector** 进行多源混合排序
- 运行广告注入的 **SafeGapBlender** 确保广告与内容之间保持品牌安全间距
- 侧效应包括服务历史更新、Kafka 事件发布等

#### 2.2.3 广告系统（`ads/`）

**SafeGapBlender** - 品牌安全广告插入算法：
```
1. 识别帖子流中适合放广告的"安全间隙"（非敏感内容之后）
2. 根据广告要求的 minimum spacing 和 ideal position 计算最佳插入位
3. 贪心算法在安全间隙中寻找最近的合适位置
4. interleave 广告和帖子形成最终 feed
```

#### 2.2.4 权重评分系统（`WeightedScorer`）

```rust
Weighted Score = Σ(weight_i × P(action_i))

正向行为权重:  Favorite(×1.0), Reply(×0.5), Repost(×0.3),
              Dwell(×0.2), Click, Share, Quote, VQV
负向行为权重:  NotInterested, Block, Mute, Report (负权重)
连续行为:      DwellTime (连续值预测)

最终分数需要 offset 处理确保在正值范围
```

### 2.3 Thunder（In-Network 内容存储）

**语言：** Rust | **位置：** `thunder/` | **行数：** ~1,000 lines

#### 2.3.1 核心设计

Thunder 是一个**纯内存的帖子存储和实时摄入系统**：

```
┌──────────────────────────────────────────────────────────┐
│                      THUNDER                             │
│                                                          │
│   Kafka ──────▶ PostStore (DashMap based)                │
│   (Create/Delete    │                                    │
│    Events)          ├── posts: DashMap<i64, LightPost>   │
│                     ├── original_posts_by_user            │
│                     ├── secondary_posts_by_user           │
│                     ├── video_posts_by_user               │
│                     └── deleted_posts                     │
│                                                          │
│   gRPC Service:                                          │
│     get_in_network_posts(user_id, following_ids,          │
│                          exclude_ids, max_results)        │
│                                                          │
│   Auto-trim: 每 2 分钟清理过期帖子                        │
│   Retention: 可配置（默认 2 天）                          │
└──────────────────────────────────────────────────────────┘
```

#### 2.3.2 关键实现细节

- **DashMap**（Rust 的无锁并发 HashMap）存储所有数据
- 每个用户维护三个时间线：
  - `original_posts_by_user`：原创帖子（非回复、非转发）
  - `secondary_posts_by_user`：回复 + 转发
  - `video_posts_by_user`：视频帖子
- 使用 `VecDeque` 维护按时间排序的帖子引用（`TinyPost { post_id, created_at }`）
- **次级内容过滤逻辑**：对于回复，只有当回复对象是原创帖、或回复了一条整个线程的根帖且回复了关注用户时才会展示
- **Concurrency Limiting**：通过 `Semaphore` 限制并发请求数，超限时返回 `RESOURCE_EXHAUSTED`
- **Request Timeout**：使用`Instant`计时，超时后截断处理以防长尾请求阻塞
- **简单排序**：按 `created_at` 倒序排列，纯时间线排序无 ML

### 2.4 Phoenix（机器学习排序与召回）

**语言：** Python (JAX/Haiku) | **位置：** `phoenix/` | **行数：** ~2,500 lines

这是整个系统的**算法核心**，提供两阶段推荐：

#### 2.4.1 阶段一：Retrieval（Two-Tower 召回模型）

```
USER TOWER                          CANDIDATE TOWER
┌──────────────┐                   ┌──────────────────┐
│ User Hashes  │                   │ Candidate Hashes │
│ + History    │                   │ (post + author)  │
│   Sequence   │                   │                  │
└──────┬───────┘                   └───────┬──────────┘
       │                                   │
       ▼                                   ▼
┌──────────────┐                   ┌──────────────────┐
│  Grok Trans- │                   │  CandidateTower  │
│  former      │                   │  (MLP Projection)│
│  (shared)    │                   │  or Mean Pooling │
└──────┬───────┘                   └───────┬──────────┘
       │                                   │
       ▼                                   ▼
  User Embedding                  Candidate Embeddings
  [B, D] L2-norm                  [N, D] L2-norm
       │                                   │
       └─────────── dot product ───────────┘
                       │
                       ▼
               Top-K by Similarity
               (从百万 → 千级别)
```

**关键算法细节：**

1. **User Tower** 使用和 Ranker 相同的 Grok Transformer 架构，通过 **Masked Mean Pooling** 将变长历史序列编码为固定维度向量
2. **Candidate Tower** 支持两种模式：
   - `enable_linear_proj=True`：两层 MLP（Linear → SiLU → Linear）+ L2 normalization
   - `enable_linear_proj=False`：简单 Mean Pooling + L2 normalization（参数更少但表达力更低）
3. **相似度搜索**：`dot product` 在 L2-normalized 空间中等价于 cosine similarity
4. 发布版本包含 ~537K 运动类帖子的预计算语料库

#### 2.4.2 阶段二：Ranking（基于 Grok Transformer 的排序模型）

这是整个系统的决策核心：

**模型架构：**
```
输入                          Transformer          输出
────────────────────────────────────────────────────────
User Embedding [B, 1, D]  ──┐
                              │
History Seq [B, S, D]      ──┼──▶ 4 层 Grok ──▶ 取出候选
  (帖子+作者+行为+产品面)     │    Transformer    位置的输出
                              │    (+ Candidate
Candidate Seq [B, C, D]    ──┘    Isolation Mask)
  (帖子+作者+产品面+发布时间)
                                       │
                                       ▼
                              ┌────────┴────────┐
                              │                 │
                         Unembedding    Continuous Head
                         (19 actions)   (8 continuous)
                              │                 │
                              ▼                 ▼
                         P(fav,reply,...)  Dwell Time 等
                         Sigmoid 输出      Sigmoid 输出
```

**核心技术创新：Candidate Isolation（候选隔离）**

这是 Phoenix 最精妙的设计：

```
Attention Mask（1 = 可以关注，0 = 不能关注）:

          User  │  History (S)  │  Candidates (C)
   ─────┬───────┼───────────────┼──────────────────
   User │   1   │  1  1  1  1   │  0  0  0  0  0
   ─────┼───────┼───────────────┼──────────────────
   Hist │   1   │  1  1  1  1   │  0  0  0  0  0
   ─────┼───────┼───────────────┼──────────────────
   Cand │   1   │  1  1  1  1   │  1  0  0  0  0   ← 仅对角线
   Cand │   1   │  1  1  1  1   │  0  1  0  0  0
   Cand │   1   │  1  1  1  1   │  0  0  1  0  0
```

- 候选之间**不能互相关注**（除自身外）
- 候选可以关注用户嵌入和历史序列
- 这确保候选分数不会因为 batch 中其他候选的存在而改变
- 分数变得 **consistent 和 cacheable**

**Embedding 系统：Hash-Based Lookups**

```python
# 使用线性同余哈希将原始 ID 映射到嵌入表
raw = (id * scale + bias) % modulus
hash_value = (raw % (num_buckets - 1)) + 1  # 0 保留给 padding

# 支持多哈希捕获不同特征
# user: 2 hash functions
# item: 2 hash functions
# author: 2 hash functions
# 嵌入表: 1,000,000 entries each
```

**特征工程（全自动学习）：**

输入特征包括：
- **User**：多哈希 ID 嵌入 + 可选 IP 地址嵌入
- **History Posts**：多哈希 ID 嵌入 + 作者嵌入 + 行为类型嵌入 + 产品面（Product Surface）嵌入 + Dwell Time 连续值投影
- **Candidates**：多哈希 ID 嵌入 + 作者嵌入 + 产品面嵌入 + 帖子发布时长（Post Age Bucket）嵌入

**19 个预测目标：**

| 索引 | 行为 | 类型 |
|------|------|------|
| 0 | Favorite | 离散 |
| 1 | Reply | 离散 |
| 2 | Repost | 离散 |
| 3 | Photo Expand | 离散 |
| 4 | Click | 离散 |
| 5 | Profile Click | 离散 |
| 6 | Video Quality View | 离散 |
| 7 | Share | 离散 |
| 8 | Share via DM | 离散 |
| 9 | Share via Copy Link | 离散 |
| 10 | Dwell | 离散 |
| 11 | Quote | 离散 |
| 12 | Quoted Click | 离散 |
| 13 | Follow Author | 离散 |
| 14 | Not Interested | 离散（负反馈） |
| 15 | Block Author | 离散（负反馈） |
| 16 | Mute Author | 离散（负反馈） |
| 17 | Report | 离散（负反馈） |
| 18 | Dwell Time | 连续值 |

#### 2.4.3 推理流水线（`run_pipeline.py`）

端到端推理实现了 **Retrieval → Ranking** 的完整流程：

```
artifacts/
  retrieval/
    model_params.npz (3 MB)     ← 召回 Transformer + Candidate Tower
    embedding_tables.npz (1.4G) ← User/Item/Author 嵌入表
    config.json
  ranker/
    model_params.npz (3 MB)     ← 排序 Transformer + Action Head
    embedding_tables.npz (1.4G) ← User/Item/Author 嵌入表
    config.json
  sports_corpus.npz             ← 537K 预计算候选表示
  example_sequence.json         ← 示例用户行为历史
```

Model Config (Mini Version):
- Embedding dim: 128, Layers: 4, Heads: 4, Key size: 32
- History seq len: 127, Candidate seq len: 64
- Widening factor: 2

### 2.5 Grox（内容理解管线）

**语言：** Python (asyncio) | **位置：** `grox/` | **行数：** ~3,000 lines

Grox 是一个**独立的异步内容理解服务**，通过 gRPC 对外暴露，负责：

#### 2.5.1 系统架构

```
┌──────────────────────────────────────────────────────┐
│                    GROX SERVICE                       │
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │  Dispatcher  │  │   Engine     │  │  gRPC      │ │
│  │  (Producer)  │  │  (Consumer)  │  │  Server    │ │
│  │              │  │              │  │            │ │
│  │ Task         │  │ Queue ──────▶│  │            │ │
│  │ Generators ──▶│  │   Engine    │  │            │ │
│  │              │  │              │  │            │ │
│  │ Fill Loop    │  │ ◀── Result   │  │            │ │
│  │ Result Loop  │  │    Queue     │  │            │ │
│  └──────────────┘  └──────────────┘  └────────────┘ │
│                                                      │
│  Components:                                         │
│  ├── plans/         (任务执行计划/DAG)                │
│  ├── tasks/         (具体处理任务)                    │
│  ├── classifiers/   (分类器)                         │
│  ├── embedder/      (多模态嵌入生成器)                │
│  ├── summarizer/    (内容摘要生成器)                  │
│  ├── data_loaders/  (Kafka/Strato 数据加载器)         │
│  └── schedules/     (调度上下文和类型)                │
└──────────────────────────────────────────────────────┘
```

#### 2.5.2 核心组件详解

**Executor Pattern（Plan + Task DAG）：**

```
Plan (DAG 任务图):
  TASKS = { "task_a": TaskA, "task_b": TaskB, ... }
  TASK_DEPENDENCIES = {
    "task_a": set(),        # 无依赖，可立即执行
    "task_b": {"task_a"},   # 依赖 task_a 完成
  }

执行流程:
  1. 按拓扑顺序启动所有 Task
  2. 每个 Task 等待其依赖的 Future 完成
  3. 依赖返回 SKIPPED → 后续 Task 自动跳过
  4. 依赖成功 → 继续执行后续 Task
  5. 异步并行执行无依赖关系的 Task
```

**任务生成器（Task Generators）：**

Dispatcher 支持 15+ 种任务生成器，通过配置驱动：
- `PostStreamTaskGenerator` - 实时帖子流任务
- `PostSafetyStreamTaskGenerator` - 安全审核流任务
- `PostEmbeddingV5StreamTaskGenerator` - 帖子嵌入（V5）流
- `MinTractionPostStreamForGroxTaskGenerator` - 最小互动量过滤
- `SafetyPtosDeluxeStreamTaskGenerator` - PTOS 政策执行
- 等等

**内容分类器：**
| 分类器 | 功能 |
|--------|------|
| `SpamEapiLowFollowerClassifier` | 低粉丝账号垃圾评论检测 |
| `SafetyPtosClassifier` | PTOS（Policy/Terms of Service）违规检测 |
| `BangerInitialScreenClassifier` | 爆款内容初筛 |
| `ReplyRankingClassifier` | 回复排序 |
| `PostSafetyScreenDeluxeClassifier` | 帖子安全综合筛查 |

**嵌入生成器：**
- `MultimodalPostEmbedderV2` - 多模态帖子嵌入 V2
- `MultimodalPostEmbedderV5` - 多模态帖子嵌入 V5（最新版）

**摘要生成器：**
- `EapiSummarizer` - 基于外部 API 的摘要服务
- `PostEmbeddingSummarizer` - 用于嵌入生成的帖子摘要

#### 2.5.3 并发模型

```
Dispatcher (独立进程)          Engine (独立进程)
     │                              │
     ├── fill_loop()                ├── _poll_task() 循环
     │   └── TaskGenerator.poll()   │   └── Queue.get()
     │       └── 生成任务            │
     │                              │
     ├── _submit_task()             ├── _process_task()
     │   └── Queue.put()            │   └── PlanMaster.exec()
     │                              │       └── DAG 执行
     ├── result_loop()              │
     │   └── Queue.get()            ├── _resp_queue.put()
     │   └── 重试/ack               │
     │                              │
     └── 使用 multiprocessing.Process 隔离
```

关键特性：
- **Process 隔离**：Dispatcher 和 Engine 在不同进程中运行
- **async/await + Queue** 通信
- **重试机制**：失败任务最多重试 N 次（tenacity 库）
- **优雅关闭**：shutdown_event + queue_connection_shutdown_event 两级关闭信号
- **Metrics**：全面的 Prometheus 指标埋点

---

## 三、完整数据流

### 3.1 端到端请求处理链路

```
用户请求 "For You" Feed
        │
        ▼
┌──────────────────────────────────────────────────────────────┐
│ ForYouCandidatePipeline.execute(query)                       │
│                                                              │
│ 1. Query Hydration (并行)                                     │
│    ├── Served History (Redis)                                │
│    └── Past Request Timestamps (Redis)                       │
│                                                              │
│ 2. Sources (并行) → 交给 ScoredPostsServer 处理              │
│    ├── ScoredPostsSource ─────────────────────┐              │
│    ├── AdsSource                              │              │
│    ├── WhoToFollowSource                      │              │
│    ├── PromptsSource                          │              │
│    └── PushToHomeSource                       │              │
│                                               │              │
│ 3. 混合排序 (BlenderSelector + SafeGapBlender) │              │
│                                               │              │
│ 4. Side Effects (异步并行)                     │              │
│    ├── 更新 Served History                     │              │
│    ├── Kafka 事件发布                          │              │
│    └── Response Stats                         │              │
└───────────────────────────────────────────────┼──────────────┘
                                                │
                    ┌───────────────────────────┘
                    ▼
┌──────────────────────────────────────────────────────────────┐
│ ScoredPostsServer → PhoenixCandidatePipeline.execute(query)  │
│                                                              │
│ 1. Query Hydration (15 个并行)                                │
│    ├── 用户行为序列 (UserActionAggregation)                   │
│    ├── 关注/屏蔽/静音列表 (SocialGraph)                       │
│    ├── 曝光 Bloom Filter                                     │
│    ├── IP 地理位置                                           │
│    └── 人口统计/性别推断/主题偏好等                            │
│                                                              │
│ 2. Candidate Sources (6 个并行)                               │
│    ├── ThunderSource ──▶ gRPC ──▶ Thunder                    │
│    │   └── get_in_network_posts(following_ids, exclude_ids)  │
│    │       └── PostStore.get_all_posts_by_users()             │
│    │           ├── original_posts (per user, max N)           │
│    │           └── secondary_posts (per user, max M)          │
│    │           └── sort by recency                            │
│    │                                                          │
│    ├── PhoenixSource ──▶ gRPC ──▶ Phoenix Retrieval          │
│    │   └── retrieve(user_id, history_seq, top_k)              │
│    │       ├── User Tower: encode(user + history) → [B, D]   │
│    │       └── dot-product with corpus → Top-K               │
│    │                                                          │
│    ├── PhoenixTopicsSource ──▶ 主题化检索                     │
│    ├── PhoenixMOESource ──▶ MoE 变体检索                      │
│    ├── TweetMixerSource ──▶ TweetMixer 服务                   │
│    └── CachedPostsSource ──▶ Redis 缓存                       │
│                                                              │
│ 3. Hydration (10 个并行)                                      │
│    ├── 标记 In-Network + Mutual Follow                        │
│    ├── 获取帖子核心数据 (TweetEntityService)                   │
│    ├── 展开引用帖子                                           │
│    ├── 获取视频时长/媒体类型                                   │
│    ├── 获取作者完整信息 (Gizmoduck)                            │
│    ├── 获取屏蔽关系                                           │
│    └── 获取语言代码                                           │
│                                                              │
│ 4. Pre-Scoring Filters (14 个，串行)                          │
│    DropDup → CoreDataFailed → Age → Self →                   │
│    RetweetDedup → Subscription → PreviouslySeen →            │
│    MutedKeyword → BlockedAuthor → Video → TopicFilter        │
│                                                              │
│ 5. Scoring (3 个 Scorers，串行)                               │
│    ├── PhoenixScorer: gRPC → Phoenix Ranker                  │
│    │   └── predict(user_history, candidates)                  │
│    │       ├── Hash IDs → Embedding Table Lookups            │
│    │       ├── Build Input Embeddings                        │
│    │       │   [User | History Posts+Authors+Actions |       │
│    │       │    Candidates+Authors+Age]                      │
│    │       ├── 4-layer Grok Transformer                      │
│    │       │   + Candidate Isolation Mask                    │
│    │       │   + RoPE Position Encoding                      │
│    │       ├── Extract Candidate Outputs                     │
│    │       ├── Unembedding → 19 action logits                │
│    │       └── Sigmoid → 19 engagement probabilities         │
│    │                                                          │
│    ├── RankingScorer:                                         │
│    │   ├── WeightedScorer: combine 19 probs with weights     │
│    │   │   Final = Σ(weight_i × P(action_i)) + offset        │
│    │   ├── AuthorDiversityScorer:                             │
│    │   │   For each author's Nth post in sorted order:       │
│    │   │   adjusted = score × (decay^position + floor)       │
│    │   └── OONScorer:                                         │
│    │       If !in_network: score × OON_WEIGHT_FACTOR          │
│    │                                                          │
│    └── VMRanker: 视频内容额外评优                             │
│                                                              │
│ 6. Selection: Top-K by final score                           │
│                                                              │
│ 7. Post-Selection Processing:                                │
│    ├── Hydrators: VF check, Brand Safety, TweetType          │
│    └── Filters: VF, AncillaryVF, DedupConversation           │
│                                                              │
│ 8. Side Effects (6 个，异步并行)                              │
│    ├── Kafka: 分数数据给实验系统                               │
│    ├── Kafka: 重排序数据给训练                                 │
│    ├── Redis: 候选缓存                                       │
│    └── Stats: 打分统计                                       │
└──────────────────────────────────────────────────────────────┘
        │
        ▼
  Ranked Feed Response (排序后的帖子列表)
```

### 3.2 规模估算

| 阶段 | 候选数 | 说明 |
|------|--------|------|
| Thunder Source | ~100-500 | 每个关注用户的最近帖子 |
| Phoenix Retrieval | ~200 | Top-K from 百万级语料库 |
| All Sources Combined | ~500-1000 | 多源合并 |
| After Filters | ~200-500 | 过滤后剩余 |
| After Scoring | ~200-500 | 都有分数 |
| Final Selection | ~50-100 | Top-K 截断 |
| After Post-Selection | ~50-100 | VF 过滤后 |

---

## 四、工程亮点与技术要点

### 4.1 技术决策亮点

**1. 双语言技术栈的合理分工**

| 职责 | 语言 | 理由 |
|------|------|------|
| 在线服务编排 | Rust | 低延迟、内存安全、零成本抽象 |
| ML 模型推理 | Python/JAX | 深度学习生态、JIT 编译 |
| 内容理解 | Python | 灵活易扩展、AI/ML 工具链 |

**2. Candidate Isolation - 排序系统的最关键创新**

传统推荐系统中，Listwise 排序会因为 batch 组成不同导致同一候选的分数变化，不满足一致性和可缓存性要求。Phoenix 通过特殊的 Attention Mask（候选间只有对角线为1）实现了 **Pointwise scoring in a batched transformer**。这既利用了 Transformer 的表达能力，又保证了分数一致性。

**3. Hash-Based Embeddings vs Traditional Embedding Tables**

使用多哈希函数将数十亿级 ID 空间映射到固定大小的嵌入表（1M entries）：
- 避免存储海量嵌入表（数十亿 × 128 维 → 数百 GB）
- Hash 碰撞可通过多哈希缓解
- 训练时自动学习哈希冲突下的最优分配

**4. Candidate Pipeline 的 trait-based 设计**

完全解耦了业务逻辑（sources/hydrators/filters/scorers）和管道执行引擎：
- 新候选源只需实现 `Source` trait
- 新过滤器只需实现 `Filter` trait
- 执行引擎负责并行调度、容错、监控

**5. Grox 的 Plan + Task DAG 调度**

将复杂的内容理解任务建模为有向无环图（DAG）：
- 声明式定义任务依赖
- 自动并行化无依赖任务
- 依赖失败时自动传播跳过信号

### 4.2 推荐系统创新

**1. 端到端学习替代手工特征**

传统推荐系统需要大量手工特征工程（文本特征、社交特征、时效性特征等）。Phoenix 完全由 Transformer 从行为序列中自学习内容相关性，消除了：
- 特征工程的开发维护成本
- 特征存储和传输的基础设施成本
- 特征更新和一致性维护的运维成本

**2. 多动作联合预测**

预测 19 种行为（而非单一 CTR）并用可配置权重组合：
- 允许产品团队通过调整权重灵活控制优化目标
- 负反馈（Block/Mute/Report）的纳入天然抑制低质量内容
- 不同产品面可使用不同权重组合

**3. 召回和排序共享 Transformer 架构**

Phoenix 的 User Tower（召回）使用和 Ranker 相同的 Transformer 架构，使得两者的表示空间一致，减少了架构不一致带来的信息损失。

### 4.3 工程实现亮点

**1. Thunder 的 Sub-Millisecond 查找**

- `DashMap` 无锁并发 HashMap
- 全内存存储，零外部依赖
- Kafka 实时摄入 + 定期过期清理
- 三级分类存储（原创/回复+转发/视频）优化不同场景

**2. 多层缓存策略**

- **Redis 候选缓存**：避免重复计算
- **Phoenix Request 缓存**：跨请求复用 ML 推理结果
- **Impression Bloom Filter**：概率性地过滤已曝光内容

**3. 完善的实验系统**

- `Decider` 机制允许运行时动态切换实验组
- 多集群路由（FOU/LAP7）支持 A/B 测试
- 新用户特殊处理（阈值判断、独立集群）

**4. 可观测性**

- 全链路 Tracing（OpenTelemetry/Tracing）
- 丰富的 Prometheus Metrics
- 每阶段执行耗时统计
- Filter 过滤率统计

### 4.4 安全与合规

**1. 多层内容安全过滤**

- Pre-scoring: AuthorSocialgraphFilter, MutedKeywordFilter
- Post-scoring: VFFilter (deleted/spam/violence/gore)
- Grox: SpamDetection, PTOS Policy Enforcement, Safety Screening

**2. 品牌安全（Brand Safety）**

广告插入的 SafeGapBlender 确保广告不出现在敏感内容附近

---

## 五、各模块代码量与技术债务分析

### 5.1 代码量分布

| 模块 | 文件数 | 主要语言 | 复杂度评价 |
|------|--------|---------|-----------|
| home-mixer | ~60+ | Rust | **极高** - 最多组件耦合 |
| phoenix | 10 | Python | **高** - 算法核心 |
| grox | ~50 | Python | **中高** - 大量业务逻辑 |
| thunder | 8 | Rust | **中低** - 职责清晰 |
| candidate-pipeline | 9 | Rust | **低** - 框架简洁 |

### 5.2 值得关注的设计

1. **Home Mixer 的复杂性**：`PhoenixCandidatePipeline` 构造需要 30+ 个外部客户端的依赖注入，这是微服务架构的典型复杂性痛点
2. **Python/Rust 边界**：Phoenix 模型通过 gRPC 与 Rust 服务通信，引入了序列化开销和网络延迟
3. **Grok-1 的适应性调整**：Transformer 代码从原始 Grok-1 复制并适配，可能在模型更新时需要手动同步

---

## 六、总结与启示

### 6.1 架构总结

X-Algorithm 代表了**工业级推荐系统的先进实践**：

1. **两级漏斗架构**：百万级召回 → 千级精排 → 百级输出
2. **端到端 ML**：一个 Transformer 完成所有相关性判断，最小化手工特征
3. **多层安全网**：内容安全从候选获取开始，经过 14 道过滤 + VF 检查 + Grox 审查
4. **全链路异步**：Source/Hydrator 并行执行 + SideEffect 异步处理
5. **实验友好**：Decider 机制 + 多集群路由支持生产级 A/B 测试

### 6.2 关键数据指标

| 指标 | 数值 |
|------|------|
| Phoenix 模型参数 | ~30M (mini) / 更大 (production) |
| 嵌入表大小 | 1M users + 1M items + 1M authors × 128D = ~1.4GB |
| 行为预测维度 | 19 (15 离散 + 4 负反馈 + 连续预测) |
| In-Network 来源 | Thunder 内存存储（Kafka 实时摄入）|
| Out-of-Network 来源 | Phoenix Two-Tower 检索（百万级语料库）|
| 最终输出 | Top-K 排序帖子（数量可配置）|

### 6.3 核心启示

1. **Transformer 在推荐系统中的应用已经成熟**：不仅 NLP，推荐也进入了大模型时代
2. **Candidate Isolation 是优雅的设计模式**：在 batch 推理中保证 pointwise 一致性
3. **Hash-based Embedding 是应对大规模 ID 空间的有效方案**：以可控的碰撞换取可伸缩的存储
4. **微服务编排的复杂性需要框架化**：CandidatePipeline 的 trait 设计让业务逻辑专注于"做什么"而非"怎么调度"
5. **内容安全需要纵深防御**：不能靠单一模型，需要多层过滤 + 独立审核服务
6. **Rust 在推荐基础设施中的地位正在上升**：低延迟、高并发、内存安全的优势明显

---

*分析完成于 2026-05-16 | 基于 https://github.com/xai-org/x-algorithm Apache 2.0 许可源码*