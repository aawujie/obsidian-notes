# Prometheus 并发采集机制详解

> 创建日期:: 2026-03-09
> 标签:: #Prometheus #并发 #Goroutine #架构设计 #时序数据库
> 分类:: 技术文档/监控体系

---

## 📌 核心问题

**Prometheus 如何同时从多个数据源采集数据？**

- 是多线程吗？
- 是多进程吗？
- 数据会冲突吗？
- 性能如何？

---

## 🎯 答案：Pull Model + Goroutine

> **不是多线程/多进程，而是 Prometheus 的 "Scrape 模型"（抓取模型）+ Go 语言 Goroutine 并发**

---

## 🏗️ 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│              Prometheus 数据采集架构                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           Prometheus Server                          │   │
│  │  ┌───────────────────────────────────────────────┐  │   │
│  │  │         Scrape Manager (抓取管理器)            │  │   │
│  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐         │  │   │
│  │  │  │ Scrape  │ │ Scrape  │ │ Scrape  │  ...   │  │   │
│  │  │  │ Loop 1  │ │ Loop 2  │ │ Loop 3  │         │  │   │
│  │  │  │ (Job 1) │ │ (Job 2) │ │ (Job 3) │         │  │   │
│  │  │  └────┬────┘ └────┬────┘ └────┬────┘         │  │   │
│  │  │       │           │           │               │  │   │
│  │  │       └───────────┴───────────┘               │  │   │
│  │  │                  ↓                             │  │   │
│  │  │         TSDB Storage (统一存储)                │  │   │
│  │  └───────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ↓                                  │
│         HTTP GET /metrics (定期拉取)                        │
│         ↓           ↓           ↓           ↓               │
│  node-exporter  gitlab-exp  mysql-exp  nginx-exp           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 三层结构

| 层级 | 组件 | 作用 | 数量 |
|------|------|------|------|
| **采集层** | Exporter | 暴露指标数据 | 多个（每个数据源一个） |
| **调度层** | Scrape Manager | 并发抓取管理 | 1 个（多 Goroutine） |
| **存储层** | TSDB | 统一存储 | 1 个（并发安全） |

---

## 🔍 工作原理详解

### 1. Pull Model（拉取模型）

Prometheus **主动** 从 Exporter 拉取数据，而不是被动接收：

```
┌─────────────────────────────────────────────────────────────┐
│                    Pull vs Push                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Push Model (推送模型)                                      │
│  Exporter → 主动推送 → Prometheus                           │
│  ❌ 问题：Prometheus 无法控制节奏，容易丢失数据               │
│                                                             │
│  Pull Model (拉取模型) ← Prometheus 采用                     │
│  Prometheus → 主动拉取 → Exporter                           │
│  ✅ 优势：                                                   │
│     - Prometheus 控制抓取节奏                               │
│     - 可以精确知道目标是否存活                              │
│     - 便于调试（直接 curl /metrics）                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. 每个 Job 一个 Scrape Loop

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'node-exporter'      # Job 1 → Scrape Loop 1
    scrape_interval: 15s
    static_configs:
      - targets: ['localhost:9100']

  - job_name: 'gitlab-exporter'    # Job 2 → Scrape Loop 2
    scrape_interval: 30s
    static_configs:
      - targets: ['localhost:8080']

  - job_name: 'mysql-exporter'     # Job 3 → Scrape Loop 3
    scrape_interval: 15s
    static_configs:
      - targets: ['localhost:9104']
```

**每个 Job 配置**：
- 独立的抓取间隔（`scrape_interval`）
- 独立的抓取目标列表（`targets`）
- 独立的抓取循环（`Scrape Loop`）

---

### 3. 并发模型：Goroutine（协程）

Prometheus 用 **Go 语言** 编写，使用 **Goroutine**（轻量级协程）实现并发：

```
┌─────────────────────────────────────────────────────────────┐
│                  Scrape Manager                             │
│                                                             │
│  主线程 → 启动各个 Job 的 Scrape Loop                        │
│              ↓                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Goroutine 1 (Scrape Loop: node-exporter)           │   │
│  │    while true:                                      │   │
│  │      HTTP GET http://localhost:9100/metrics         │   │
│  │      解析响应 → 添加标签 (job, instance)             │   │
│  │      写入 TSDB                                      │   │
│  │      sleep 15s                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Goroutine 2 (Scrape Loop: gitlab-exporter)         │   │
│  │    while true:                                      │   │
│  │      HTTP GET http://localhost:8080/metrics         │   │
│  │      解析响应 → 添加标签 (job, instance)             │   │
│  │      写入 TSDB                                      │   │
│  │      sleep 30s                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Goroutine 3 (Scrape Loop: mysql-exporter)          │   │
│  │    while true:                                      │   │
│  │      HTTP GET http://localhost:9104/metrics         │   │
│  │      解析响应 → 添加标签 (job, instance)             │   │
│  │      写入 TSDB                                      │   │
│  │      sleep 15s                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Goroutine vs 传统线程

| 特性 | Goroutine | 传统线程 |
|------|-----------|----------|
| **内存占用** | 几 KB | 几 MB |
| **创建开销** | 极低 | 较高 |
| **调度** | Go 运行时用户态调度 | 操作系统内核调度 |
| **并发数** | 数万 + | 数百 - 数千 |
| **通信** | Channel | 锁/信号量 |

**优势**：Prometheus 可以为每个 Job、每个 Target 创建独立的 Goroutine，并发抓取而几乎无开销。

---

### 4. 同一 Job 内的多 Target 并行抓取

如果一个 Job 有多个目标，会**并行抓取**：

```yaml
- job_name: 'kubernetes-pods'
  scrape_interval: 15s
  static_configs:
    - targets: 
      - 'pod1:8080'
      - 'pod2:8080'
      - 'pod3:8080'
      - 'pod4:8080'
```

```
Scrape Loop (kubernetes-pods)
        ↓
  启动多个 Goroutine 并行抓取
  ┌─────┴─────┬─────────┬─────┐
  ↓           ↓         ↓     ↓
pod1        pod2      pod3  pod4  (同时抓取)
```

---

## 📊 数据写入流程

```
┌─────────────────────────────────────────────────────────────┐
│                    数据写入流程                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Scrape Loop (Goroutine)                                    │
│    ↓                                                        │
│  1. HTTP GET /metrics                                       │
│    ↓                                                        │
│  2. 解析文本格式 (Prometheus Exposition Format)             │
│    ↓                                                        │
│  3. 添加标签 (job, instance, 自定义标签)                     │
│    ↓                                                        │
│  4. Appender (事务接口)                                     │
│    ↓                                                        │
│  5. WAL (Write-Ahead Log, 预写日志) ← 保证数据不丢失         │
│    ↓                                                        │
│  6. Memory Block (内存中的时间序列块)                        │
│    ↓ (每 2 小时)                                             │
│  7. TSDB Block (压缩成磁盘块)                                │
│                                                             │
│  多个 Goroutine → 同一个 TSDB (并发安全)                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 并发安全机制

多个 Goroutine 同时写入 TSDB，如何保证数据安全？

### 1. WAL (Write-Ahead Log)

```
┌─────────────────────────────────────────────────────────────┐
│                      WAL 机制                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Goroutine 1 → 写 WAL → 提交                                │
│  Goroutine 2 → 写 WAL → 提交                                │
│  Goroutine 3 → 写 WAL → 提交                                │
│         ↓                                                   │
│  WAL 文件按顺序追加写入 (原子操作)                            │
│         ↓                                                   │
│  即使 Prometheus 崩溃，重启后可以从 WAL 恢复数据              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. 内存分片 (Sharding)

```
┌─────────────────────────────────────────────────────────────┐
│                    内存分片机制                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  时间序列 → 哈希 → 分配到不同分片                            │
│                                                             │
│  Series Hash → Shard 0 → Lock 0                             │
│  Series Hash → Shard 1 → Lock 1                             │
│  Series Hash → Shard 2 → Lock 2                             │
│                                                             │
│  不同分片 → 不同锁 → 减少锁竞争                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3. 无锁读取 (Lock-Free Read)

```
┌─────────────────────────────────────────────────────────────┐
│                    无锁读取机制                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  写入：持续进行 (Goroutine 不断抓取)                         │
│    ↓                                                        │
│  查询：创建内存快照 (Snapshot)                              │
│    ↓                                                        │
│  查询在快照上执行 → 不阻塞写入                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4. 批量提交 (Batch Commit)

```
┌─────────────────────────────────────────────────────────────┐
│                    批量提交机制                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  单次 Scrape → 采集数千个指标样本                           │
│    ↓                                                        │
│  批量打包 → 一次提交                                        │
│    ↓                                                        │
│  减少锁竞争 → 提高吞吐量                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📈 性能数据

| 指标 | 数值 | 说明 |
|------|------|------|
| **单节点抓取能力** | 100 万 + 时间序列 | 官方推荐上限 |
| **每秒抓取样本数** | 50 万 - 100 万 | 取决于硬件 |
| **并发 Goroutine 数** | 数百个 | 每个 Job/Target 一个 |
| **内存占用** | 1-2GB / 10 万序列 | 样本保留 15 天 |
| **抓取延迟** | < 1 秒 | 99% 的 Scrape |
| **压缩率** | 5:1 - 10:1 | Gorilla 压缩算法 |

### 性能瓶颈

| 瓶颈 | 表现 | 解决方案 |
|------|------|----------|
| **CPU** | Scrape 延迟增加 | 减少抓取频率/样本数 |
| **内存** | OOM | 降低保留时长/分片 |
| **磁盘 IO** | 写入延迟 | 使用 SSD/降采样 |
| **网络** | Scrape Timeout | 优化网络/就近部署 |

---

## 🆚 与其他方案对比

### Prometheus vs 传统推送模型

| 特性 | Prometheus (Pull) | 推送模型 (Push) |
|------|-------------------|-----------------|
| **控制权** | Prometheus 控制节奏 | Exporter 控制节奏 |
| **存活检测** | 自动 (Scrape 失败=DOWN) | 需要额外机制 |
| **调试** | 直接 `curl /metrics` | 需要查看日志 |
| **防火墙** | 需要开放 Exporter 端口 | 需要开放 Prometheus 端口 |
| **短期任务** | 需 Pushgateway | 原生支持 |

### Prometheus vs 其他 TSDB

| 数据库 | 并发模型 | 采集方式 |
|--------|----------|----------|
| **Prometheus** | Goroutine | Pull |
| **InfluxDB** | 线程池 | Push |
| **TimescaleDB** | PostgreSQL 进程 | Push |
| **VictoriaMetrics** | Goroutine | Pull/Push |

---

## ✅ 总结

| 问题 | 答案 |
|------|------|
| **是多线程吗？** | ❌ 不是传统线程，是 **Goroutine（协程）** |
| **是多进程吗？** | ❌ 不是，单进程多协程模型 |
| **如何并发抓取？** | 每个 Job 一个 Goroutine，并行执行 |
| **数据会冲突吗？** | ❌ 不会，TSDB 有完善的并发控制 |
| **性能如何？** | 单节点可处理 100 万 + 时间序列 |
| **采集模型？** | Pull Model（主动拉取） |

---

## 🎯 核心架构

```
【采集层】多个 Exporter (不同进程/容器)
    ↓ HTTP
【调度层】Prometheus Scrape Manager
    ├─ Goroutine 1 → node-exporter
    ├─ Goroutine 2 → gitlab-exporter
    ├─ Goroutine 3 → mysql-exporter
    └─ ... (每个 Job 一个协程)
    ↓
【存储层】TSDB (并发安全)
    ├─ WAL (预写日志)
    ├─ 内存分片
    ├─ 无锁读取
    └─ 批量提交
```

> **不是多线程/多进程采集，而是 Prometheus 主动拉取 + Goroutine 并发！**

---

## 🔗 相关资源

### 官方文档

- [Prometheus Architecture](https://prometheus.io/docs/introduction/overview/)
- [Prometheus TSDB](https://prometheus.io/docs/prometheus/latest/storage/)
- [Go Goroutines](https://go.dev/tour/concurrency/1)

### 源码阅读

- [Scrape Manager](https://github.com/prometheus/prometheus/blob/main/scrape/manager.go)
- [Scrape Loop](https://github.com/prometheus/prometheus/blob/main/scrape/scrape.go)
- [TSDB](https://github.com/prometheus/prometheus/tree/main/tsdb)

### 相关笔记

- [[Prometheus & Grafana 监控体系指南]]
- [[Prometheus 多数据源监控部署指南]]
- [[时序数据库 (TSDB) 完全指南]]

---

*最后更新:: 2026-03-09*
