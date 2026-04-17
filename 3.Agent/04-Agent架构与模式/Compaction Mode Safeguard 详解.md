# Compaction Mode: Safeguard 详解

## 📌 概述

`compaction.mode: safeguard` 是**数据压缩/整理的安全保护模式**，常见于数据库、日志系统或存储引擎中。

---

## 🎯 核心概念

### 什么是 Compaction（压缩/整理）？

将分散的数据块合并、清理过期数据、优化存储结构的过程。

```
压缩前：[数据 A] [空洞] [数据 B] [空洞] [数据 C]
            ↓ compaction
压缩后：[数据 A][数据 B][数据 C] [空闲空间]
```

---

## 🛡️ Safeguard 模式特点

```
┌─────────────────────────────────────────┐
│  safeguard 保护模式                      │
├─────────────────────────────────────────┤
│ ✅ 保留更多数据冗余                       │
│ ✅ 压缩前做完整性检查                     │
│ ✅ 失败时自动回滚                         │
│ ✅ 降低数据丢失风险                       │
│ ⚠️  压缩速度较慢                          │
│ ⚠️  占用空间稍多                          │
└─────────────────────────────────────────┘
```

---

## 📊 模式对比

| 维度 | safeguard | aggressive | disabled |
|------|-----------|------------|----------|
| **安全性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **压缩率** | 60-70% | 80-90% | 0% |
| **速度** | 慢 | 快 | N/A |
| **空间占用** | 多 | 少 | 最多 |
| **适用场景** | 生产环境 | 测试/开发 | 临时数据 |

---

## 📝 常见应用场景

### 1. SQLite / LevelDB / RocksDB

```json
{
  "compaction": {
    "mode": "safeguard",
    "threshold": 0.8
  }
}
```

### 2. 日志系统（Loki、Elasticsearch）

```yaml
compaction:
  mode: safeguard  # 保留更多索引，查询更快
```

### 3. GitLab Runner Tool（SQLite）

Job 历史数据压缩时更保守：
- 保留更多原始数据
- 降低数据库损坏风险
- 查询性能更好

---

## 💡 使用建议

| 环境 | 推荐模式 | 原因 |
|------|----------|------|
| **生产环境** | safeguard | 数据安全第一 |
| **开发测试** | aggressive | 节省空间 |
| **临时数据** | disabled | 不需要压缩 |
| **关键业务** | safeguard | 可回滚、可恢复 |
| **日志归档** | aggressive | 压缩率优先 |

---

## 🔧 配置示例

```json
// 生产环境配置
{
  "database": {
    "path": "./data/job_stages.db",
    "compaction": {
      "mode": "safeguard",
      "schedule": "0 2 * * *",
      "retention_days": 30
    }
  }
}

// 开发环境配置
{
  "database": {
    "path": "./data/job_stages.db",
    "compaction": {
      "mode": "aggressive",
      "schedule": "0 3 * * *"
    }
  }
}
```

---

## ⚠️ 注意事项

1. **safeguard 模式不是万能的**
   - 仍需定期备份
   - 监控磁盘空间

2. **模式切换时机**
   - 生产→开发：可随时切换
   - 开发→生产：建议重建索引

3. **性能影响**
   - safeguard 模式下压缩任务耗时约增加 30-50%
   - 但查询性能通常更好（数据更完整）

---

## 📚 相关资源

- [RocksDB Compaction](https://github.com/facebook/rocksdb/wiki/Compaction)
- [SQLite WAL Mode](https://www.sqlite.org/wal.html)
- [Elasticsearch Index Lifecycle](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management.html)

---

**创建时间**: 2026-02-27  
**标签**: #数据库 #性能优化 #配置管理 #技术笔记
