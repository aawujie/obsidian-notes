# Prometheus 并发采集机制详解

> 创建日期:: 2026-03-09
> 标签:: #Prometheus #并发 #Goroutine #架构设计 #时序数据库
> 分类:: 技术文档/监控体系

---

## 📌 核心问题

**Prometheus 如何同时从多个数据源采集数据？**

- 是多线程吗？
- 是多进程吗？
- Goroutine 用单核还是多核？
- 数据会冲突吗？
- 性能如何？

---

## 🎯 答案：Pull Model + Goroutine 两级调度

> **不是传统多线程/多进程，而是 Prometheus 的 "Scrape 模型"（抓取模型）+ Go 语言 Goroutine 两级调度并发**

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

### 3. 并发模型：Goroutine 两级调度

Prometheus 用 **Go 语言** 编写，使用 **Goroutine**（轻量级协程）实现并发。

#### ⚠️ 关键：<span style="color:rgb(255, 77, 77)">两级调度模型</span>

```
┌─────────────────────────────────────────────────────────────┐
│              Go 两级调度架构                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  【用户态调度】Go Runtime Scheduler                         │
│  Goroutine → OS Thread (M:N 映射)                           │
│         ↓                                                   │
│  Go 运行时在用户态决定哪个 Goroutine 在哪个 OS Thread 上运行    │
│         ↓                                                   │
│  【内核态调度】OS Kernel Scheduler                          │
│  OS Thread → CPU Core                                       │
│         ↓                                                   │
│  操作系统内核决定哪个 Thread 在哪个 CPU 核心上运行             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### M:N 调度模型详解

```
┌─────────────────────────────────────────────────────────────┐
│                  Go M:N 调度                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  10000 Goroutines  →  8 OS Threads  →  8 CPU Cores         │
│       ↓                    ↓                 ↓              │
│    用户态               内核态             硬件              │
│   (Go 调度)           (OS 调度)                            │
│                                                             │
│  优势：                                                     │
│  - Goroutine 切换不需要内核参与                            │
│  - 少量 OS Thread 减少内核调度开销                         │
│  - 自动负载均衡                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 为什么 Goroutine 比传统线程高效？

```
┌─────────────────────────────────────────────────────────────┐
│                传统线程 vs Goroutine 切换                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  【传统线程】                                                │
│  Thread 切换 → 系统调用 → 内核态 → 保存寄存器 → 恢复寄存器   │
│              ↑                                              │
│         每次切换都要进入内核态，开销大！                      │
│                                                             │
│  【Goroutine】                                               │
│  Goroutine 切换 → Go 运行时 → 保存少量寄存器 → 恢复寄存器    │
│                 ↑                                           │
│            纯用户态切换，开销极低！                          │
│                 ↓                                           │
│  OS Thread 切换 → 内核态 (由 OS 决定，Go 无法控制)            │
│                                                             │
│  关键：Goroutine 大部分切换在用户态完成，                    │
│        只有 OS Thread 调度才需要内核态！                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Goroutine vs 传统线程

| 特性       | Goroutine                                                 | 传统线程                     |
| -------- | --------------------------------------------------------- | ------------------------ |
| **内存占用** | 几 KB (栈)                                                  | 几 MB (栈)                 |
| **创建开销** | 极低 (用户态分配)                                                | 较高 (系统调用)                |
| **调度**   | **两级调度**：<br>1. Go 运行时 (用户态)<br>2. OS 内核 (内核态)            | **一级调度**：<br>OS 内核 (内核态) |
| **并发数**  | 数万 +                                                      | 数百 - 数千                  |
| **切换开销** | 低 (用户态切换)                                                 | 高 (内核态切换)                |
| **通信**   | <span style="color:rgb(255, 77, 77)">Channel</span> (用户态) | 锁/信号量 (内核态)              |

**优势**：Prometheus 可以为每个 Job、每个 Target 创建独立的 Goroutine，并发抓取而几乎无开销。

---

### 💡 Goroutine 使用单核还是多核？

**答案：多核！Go 运行时自动利用所有可用的 CPU 核心。**

#### <span style="color:rgb(255, 77, 77)">GOMAXPROCS</span> 机制

```
┌─────────────────────────────────────────────────────────────┐
│              Go 多核调度架构                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Go Program (Prometheus)                                    │
│         ↓                                                   │
│  GOMAXPROCS = CPU 核心数 (默认)                              │
│         ↓                                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ OS Thread 1  → CPU Core 1                           │   │
│  │   ├─ Goroutine 1 (Scrape: node-exporter)            │   │
│  │   ├─ Goroutine 5 (Scrape: mysql-exporter)           │   │
│  │   └─ Goroutine 9 (Query handler)                    │   │
│  │                                                     │   │
│  │ OS Thread 2  → CPU Core 2                           │   │
│  │   ├─ Goroutine 2 (Scrape: gitlab-exporter)         │   │
│  │   ├─ Goroutine 6 (TSDB compaction)                 │   │
│  │   └─ Goroutine 10 (Alert manager)                  │   │
│  │                                                     │   │
│  │ OS Thread 3  → CPU Core 3                           │   │
│  │   ├─ Goroutine 3 (Scrape: redis-exporter)          │   │
│  │   └─ Goroutine 7 (Remote write)                    │   │
│  │                                                     │   │
│  │ OS Thread 4  → CPU Core 4                           │   │
│  │   ├─ Goroutine 4 (Scrape: nginx-exporter)          │   │
│  │   └─ Goroutine 8 (HTTP server)                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 关键配置：GOMAXPROCS

| 配置 | 说明 | 默认值 |
|------|------|--------|
| **GOMAXPROCS** | 限制 Go 程序使用的 CPU 核心数 | Go 1.5+ = CPU 核心数 |
| **查看当前值** | `runtime.GOMAXPROCS(0)` | - |
| **设置方式** | 环境变量 `GOMAXPROCS=4` 或代码设置 | - |

```bash
# 启动时设置
GOMAXPROCS=4 prometheus

# 或者在 Kubernetes 中
env:
  - name: GOMAXPROCS
    value: "4"
```

#### 多核优势

| 优势         | 说明                                   |
| ---------- | ------------------------------------ |
| **并行抓取**   | 多个 Goroutine 在不同 CPU 核心上同时执行 HTTP 请求 |
| **并行写入**   | TSDB 写入和 Scrape 可以并行执行               |
| **不阻塞查询**  | 查询处理在独立 Goroutine 上，不影响抓取            |
| **自动负载均衡** | Go 调度器自动将 Goroutine 分配到空闲核心          |

#### 实际测试

```bash
# 查看你的 Mac 有几个 CPU 核心
sysctl -n hw.ncpu

# 启动 Prometheus 并查看 CPU 使用
docker stats prometheus

# 如果 GOMAXPROCS 设置正确，应该能看到多核 CPU 都被利用
```

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

### 1. <span style="color:rgb(255, 77, 77)">WAL (Write-Ahead Log)</span>

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
| **Prometheus** | Goroutine 两级调度 | Pull |
| **InfluxDB** | 线程池 | Push |
| **TimescaleDB** | PostgreSQL 进程 | Push |
| **VictoriaMetrics** | Goroutine 两级调度 | Pull/Push |

---

## ✅ 总结

| 问题 | 答案 |
|------|------|
| **是多线程吗？** | ❌ 不是传统线程，是 **Goroutine（协程）** |
| **是多进程吗？** | ❌ 不是，单进程多协程模型 |
| **使用单核还是多核？** | ✅ **多核**，Go 自动利用所有 CPU 核心 |
| **只在用户态调度吗？** | ❌ 不是，**两级调度**（用户态 + 内核态） |
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

> **不是多线程/多进程采集，而是 Prometheus 主动拉取 + Goroutine 两级调度并发！**

---

## 🔗 相关资源

### 官方文档

- [Prometheus Architecture](https://prometheus.io/docs/introduction/overview/)
- [Prometheus TSDB](https://prometheus.io/docs/prometheus/latest/storage/)
- [Go Goroutines](https://go.dev/tour/concurrency/1)
- [Go Scheduler](https://go.dev/blog/scheduler)

### 源码阅读

- [Scrape Manager](https://github.com/prometheus/prometheus/blob/main/scrape/manager.go)
- [Scrape Loop](https://github.com/prometheus/prometheus/blob/main/scrape/scrape.go)
- [TSDB](https://github.com/prometheus/prometheus/tree/main/tsdb)
- [Go Runtime Scheduler](https://github.com/golang/go/blob/master/src/runtime/proc.go)

### 相关笔记

- [[Prometheus & Grafana 监控体系指南]]
- [[Prometheus 多数据源监控部署指南]]
- [[时序数据库 (TSDB) 完全指南]]

---

*最后更新:: 2026-03-09*
