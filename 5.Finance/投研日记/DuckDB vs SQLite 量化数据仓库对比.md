---
title: DuckDB vs SQLite 量化数据仓库技术选型
type: note
created: 2026-06-26
updated: 2026-06-26
sources: []
tags: [量化投资, 数据工程, DuckDB, SQLite, 技术选型, 数据仓库]
---

# DuckDB vs SQLite 量化数据仓库技术选型

## 一、一句话定位

SQLite 是给应用程序做事务存储的（OLTP），DuckDB 是给分析师跑分析查询的（OLAP）。量化数据仓库场景下，**DuckDB 完胜**。

---

## 二、核心差异速查

| 维度 | SQLite | DuckDB |
|:---|:---|:---|
| **设计目标** | 事务型数据库（OLTP） | 分析型数据库（OLAP） |
| **执行引擎** | 逐行扫描（火山模型） | 向量化列式扫描 |
| **存储格式** | 自有 B-tree 行式存储 | 直接读写 Parquet/CSV/JSON |
| **压缩** | 不压缩 | Parquet 自带压缩，省 5-10 倍空间 |
| **并发模型** | 多读单写，写锁锁全库 | 单进程为主，多读无锁 |
| **部署** | 零配置，一个 `.db` 文件 | 零配置，`pip install duckdb` |
| **SQL 标准** | 基础 SQL，窗口函数有限 | 完整 SQL，丰富窗口/聚合/嵌套 |
| **大数据性能** | 百万行开始吃力 | 亿行级别轻松 |
| **索引** | 需要手动建索引 | 列式存储天然高效，无需索引 |
| **生态** | 全球最广泛部署的嵌入式数据库 | 新兴分析引擎，数据科学社区活跃 |

---

## 三、执行引擎：逐行 vs 向量化

### SQLite：火山模型（Volcano Model）

```
SELECT AVG(close) FROM stock_daily WHERE date > '2024-01-01'

执行过程：
1. 读一行 → 检查 date 条件 → 如果通过，提取 close → 累加
2. 读下一行 → 检查 date 条件 → 如果通过，提取 close → 累加
3. ...重复 625 万次
4. 返回 sum / count
```

每行数据都要走一遍完整的函数调用链，CPU 分支预测频繁失败，cache miss 高。

### DuckDB：向量化执行

```
SELECT AVG(close) FROM stock_daily WHERE date > '2024-01-01'

执行过程：
1. 一次读 4096 行（一个 batch）到 CPU cache
2. 向量化过滤：4096 行的 date 字段并行比较
3. 向量化聚合：4096 行的 close 字段并行累加
4. 重复，每次处理 4096 行
```

每次处理一个向量，SIMD 指令集并行，cache 友好，CPU 利用率极高。

**性能差距：不是 2 倍 3 倍，是 10 倍到 100 倍。**

---

## 四、存储格式：行式 vs 列式

### SQLite 行式存储

```
磁盘上的实际存储：
[000001.SZ | 2024-01-01 | 10.00 | 10.50 | 9.80 | 10.20 | 1000000]
[000001.SZ | 2024-01-02 | 10.20 | 10.80 | 10.10 | 10.50 | 1200000]
[000002.SZ | 2024-01-01 | 20.00 | 20.50 | 19.80 | 20.20 | 500000]
...
```

查 `AVG(close)` 时，需要把整行读出来，再取 close 字段。其他字段（open/high/low/volume）全部浪费带宽。

### DuckDB/Parquet 列式存储

```
磁盘上的实际存储：
close 列: [10.20, 10.50, 20.20, ...]
open 列:  [10.00, 10.20, 20.00, ...]
high 列:  [10.50, 10.80, 20.50, ...]
volume 列: [1000000, 1200000, 500000, ...]
```

查 `AVG(close)` 时，只读 close 那一列。其他列不碰。IO 量直接减少 80%。

**列式存储 + 压缩 = 同量数据，DuckDB 文件大小只有 SQLite 的 1/5 到 1/10。**

---

## 五、量化场景实测对比

### 场景设定

- 5000 只 A 股 × 5 年 × 250 交易日 = **625 万行日线数据**
- 字段：symbol, date, open, high, low, close, volume, amount, turnover, trade_status

### 查询 1：单标的全历史

```sql
SELECT * FROM stock_daily WHERE symbol = '000001.SZ' ORDER BY date
```

| | SQLite | DuckDB |
|---|---|---|
| 耗时 | ~50ms | ~10ms |
| 差距 | | 5 倍 |

### 查询 2：全市场聚合

```sql
SELECT date, AVG(close), MEDIAN(close), STDDEV(close)
FROM stock_daily
GROUP BY date
ORDER BY date
```

| | SQLite | DuckDB |
|---|---|---|
| 耗时 | ~8s | ~0.3s |
| 差距 | | 27 倍 |

### 查询 3：滚动窗口计算

```sql
SELECT symbol, date, close,
       AVG(close) OVER (PARTITION BY symbol ORDER BY date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) AS ma_20,
       STDDEV(close) OVER (PARTITION BY symbol ORDER BY date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) AS std_20
FROM stock_daily
```

| | SQLite | DuckDB |
|---|---|---|
| 耗时 | ~35s | ~1.2s |
| 差距 | | 29 倍 |

### 查询 4：多表 JOIN（日线 + 复权因子 + 行业分类）

```sql
SELECT d.symbol, d.date, d.close * a.factor AS adj_close, i.industry
FROM stock_daily d
JOIN adjust_factor a ON d.symbol = a.symbol AND d.date = a.date
JOIN industry i ON d.symbol = i.symbol
WHERE d.date = '2024-12-31'
```

| | SQLite | DuckDB |
|---|---|---|
| 耗时 | ~12s | ~0.4s |
| 差距 | | 30 倍 |

**结论：** 简单查询差距不大，但一到聚合、窗口、JOIN，DuckDB 就是降维打击。

---

## 六、为什么 SQLite 在量化场景下不行

### 1. 行式存储的根本劣势

量化分析极少需要"查某一只股票某一天的全部字段"。更常见的是：

- 全市场某一天的截面数据（`WHERE date = '2024-12-31'`）→ 列式跳过无关字段，行式全读
- 单字段的聚合运算（`AVG(close)`）→ 列式只读一列，行式每行全读
- 窗口函数（滚动均值、排名）→ 列式向量化，行式逐行循环

### 2. 没有真正的列式压缩

SQLite 不压缩数据。全市场 5 年日线（625 万行 × 10 字段）≈ **500MB-1GB**。同样的数据存 Parquet，压缩后 ≈ **50-100MB**。

### 3. 写锁是灾难

SQLite 写操作会锁整个数据库。如果你在回测过程中想同时更新数据，对不起，等着。DuckDB 追加新 Parquet 文件不影响正在读的查询。

### 4. 窗口函数支持弱

SQLite 3.25+ 开始支持窗口函数，但实现是逐行计算的，没有向量化优化。QuantSkills 的 `backtest` 协议里大量滚动计算（滚动 Sharpe、滚动 IC、滚动换手），在 SQLite 上跑直接卡死。

### 5. 没有原生 Parquet 支持

SQLite 不能直接读 Parquet。你得先写 ETL 把 Parquet 数据 INSERT 进 SQLite，数据量大了这一步本身就慢。

---

## 七、DuckDB 的劣势（什么时候该用 SQLite）

### 1. 事务性写入

高频 INSERT/UPDATE/DELETE（比如每秒几百次写入），SQLite 更快。DuckDB 不擅长频繁小写入。

**量化场景：** 不适用。数据是批量拉取后追加，不是高频写入。

### 2. 多进程并发写

SQLite 支持 WAL 模式下的多读单写。DuckDB 是单进程模型，多进程同时写同一个文件不安全。

**量化场景：** 不适用。通常是一个人跑分析，不需要多进程并发写。

### 3. 嵌入式设备 / 极小数据量

如果数据量 < 10 万行，DuckDB 的优势体现不出来，SQLite 的生态更成熟。

**量化场景：** 不适用。量化数据轻松百万行起步。

### 4. 生态成熟度

SQLite 有 20 年历史，文档、工具、社区无与伦比。DuckDB 还在快速迭代中，API 可能变化。

**量化场景：** 可以接受。DuckDB 的 Python API 已经足够稳定。

---

## 八、SQLite 的正确使用场景

不是"SQLite 不好"，是"SQLite 不该用来做 OLAP"。SQLite 的正确战场：

- 移动端 App 本地存储（微信、WhatsApp 都在用）
- 浏览器端（SQLite Wasm）
- 嵌入式设备（IoT 传感器数据）
- 网站后端请求缓存
- 配置文件存储（比 JSON 强 100 倍）
- 小型业务系统的数据持久化

**核心判断：你是要"存数据"还是"分析数据"？** 存数据用 SQLite，分析数据用 DuckDB。

---

## 九、量化数据仓库的推荐架构

```
┌─────────────────────────────────────────────────┐
│                    数据源                          │
│   Pandadata / Tushare / RiceQuant / 东方财富       │
└─────────────────────┬───────────────────────────┘
                      │ 批量拉取（每日/按需）
                      ▼
┌─────────────────────────────────────────────────┐
│               本地 Parquet 文件                    │
│  stock_daily/year=2026/month=06/part.parquet     │
│  stock_minute/...                                │
│  factor/...                                      │
│  adjust_factor/...                               │
│  industry/...                                    │
└─────────────────────┬───────────────────────────┘
                      │ SQL 查询
                      ▼
┌─────────────────────────────────────────────────┐
│                  DuckDB                           │
│  ┌─────────────┐  ┌─────────────┐               │
│  │ 因子计算     │  │ 回测分析     │               │
│  │ 滚动窗口     │  │ 截面聚合     │               │
│  │ 多表 JOIN   │  │ 分组统计     │               │
│  └─────────────┘  └─────────────┘               │
└─────────────────────┬───────────────────────────┘
                      │ DataFrame
                      ▼
┌─────────────────────────────────────────────────┐
│                  pandas/numpy                     │
│              最终因子计算 & 回测                    │
└─────────────────────────────────────────────────┘
```

**分工原则：**
- **DuckDB**：做数据过滤、聚合、JOIN、窗口函数这些"重活"
- **pandas**：只处理 DuckDB 吐出来的精炼数据，做最终因子计算
- **不在 pandas 里做全表扫描**，不在 SQLite 里做聚合分析

---

## 十、总结

| 问题 | 答案 |
|:---|:---|
| 量化数据仓库用 SQLite 还是 DuckDB？ | **DuckDB** |
| 差距多大？ | 聚合/窗口/JOIN 场景 **10-100 倍** |
| SQLite 什么时候用？ | 事务写入、嵌入式、小数据量 |
| 两个能一起用吗？ | 可以，各司其职。但要明确谁管什么 |
| Pandadata-warehouse 选 DuckDB 对吗？ | **技术选型完全正确**，问题在于没写脚本 |

**一句话：SQLite 是瑞士军刀，DuckDB 是电锯。你要切一棵树，别用瑞士军刀。**

---

> **笔记说明**：本文基于 QuantSkills 12 技能包调研中 `pandadata-warehouse` 的技术选型展开，结合量化场景的实际查询需求做对比分析。性能数据为估算值，实际表现取决于硬件和数据分布。