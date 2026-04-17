# Prometheus - 监控指标收集系统

> 💎 **标签**: #监控 #Prometheus #DevOps #可观测性 #时间序列数据库

---

## 📌 概述

**Prometheus** 是一个开源的系统监控和告警工具包，最初由 SoundCloud 开发，现在是 CNCF（云原生计算基金会）的毕业项目。它专注于**指标（Metrics）的收集、存储和查询**。

### 核心特点

- **多维数据模型**：使用 `metric_name{label1="value1", label2="value2"}` 格式
- **PromQL**：强大的查询语言，支持聚合、过滤、数学运算
- **Pull 模型**：主动从目标抓取指标（也可通过 Pushgateway 支持 Push）
- **时间序列数据库**：高效存储和压缩时序数据
- **服务发现**：自动发现 Kubernetes、EC2、Consul 等目标
- **告警管理**：内置 Alertmanager 处理告警路由、去重、静默

---

## 🏗️ 架构组件

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  Exporters  │───▶│  Prometheus  │───▶│  Grafana    │
│  (节点/应用) │    │   Server     │    │  (可视化)   │
└─────────────┘    └──────┬───────┘    └─────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │ Alertmanager│
                   │  (告警管理)  │
                   └─────────────┘
```

### 主要组件

| 组件 | 说明 |
|------|------|
| **Prometheus Server** | 核心服务，负责抓取、存储、查询指标 |
| **Exporters** | 将各种系统的指标暴露为 Prometheus 格式 |
| **Pushgateway** | 支持短期任务推送指标 |
| **Alertmanager** | 处理告警去重、分组、路由、静默 |
| **Service Discovery** | 自动发现监控目标 |

---

## 📊 指标类型

### 1. Counter（计数器）
只增不减的累积值，适合统计请求数、错误数等。
```promql
http_requests_total{method="POST", handler="/api/users"}
```

### 2. Gauge（仪表盘）
可增可减的瞬时值，适合温度、内存使用率等。
```promql
node_memory_MemAvailable_bytes
```

### 3. Histogram（直方图）
统计分布情况，可计算百分位数（p95, p99）。
```promql
http_request_duration_seconds_bucket
```

### 4. Summary（摘要）
类似 Histogram，由服务端计算分位数。
```promql
http_request_duration_seconds{quantile="0.95"}
```

---

## 🔧 常用 Exporters

| Exporter | 用途 | 端口 |
|----------|------|------|
| **Node Exporter** | Linux/Unix 系统指标 | 9100 |
| **cAdvisor** | Docker 容器指标 | 8080 |
| **MySQL Exporter** | MySQL 数据库 | 9104 |
| **Redis Exporter** | Redis 缓存 | 9121 |
| **Nginx Exporter** | Nginx 服务器 | 9113 |
| **Blackbox Exporter** | HTTP/TCP/DNS 探测 | 9115 |

---

## 📝 配置示例

### prometheus.yml
```yaml
global:
  scrape_interval: 15s      # 抓取间隔
  evaluation_interval: 15s  # 规则评估间隔

alerting:
  alertmanagers:
    - static_configs:
        - targets: ["alertmanager:9093"]

rule_files:
  - "alerts.yml"

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "node"
    static_configs:
      - targets: ["node-exporter:9100"]
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
```

### 告警规则 (alerts.yml)
```yaml
groups:
  - name: example
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "高 CPU 使用率"
          description: "{{ $labels.instance }} CPU 使用率超过 80%"
```

---

## 📈 PromQL 常用查询

### 基础查询
```promql
# 当前值
node_memory_MemAvailable_bytes

# 5 分钟平均
avg_over_time(node_cpu_seconds_total[5m])

# 增长率（每秒）
rate(http_requests_total[5m])

# 增加量
increase(http_requests_total[1h])
```

### 聚合函数
```promql
# 按标签分组求和
sum by (job) (rate(http_requests_total[5m]))

# 百分比
node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100

# Top N
topk(5, rate(http_requests_total[5m]))
```

---

## 🚨 告警管理

### Alertmanager 功能
- **分组（Grouping）**：将相关告警合并为一条通知
- **抑制（Inhibition）**：某些告警触发时抑制其他告警
- **静默（Silencing）**：维护期间临时关闭告警
- **路由（Routing）**：根据标签路由到不同接收器（邮件/Slack/钉钉等）

### 通知渠道
- 邮件
- Slack / Discord
- 钉钉 / 企业微信
- PagerDuty / OpsGenie
- Webhook 自定义

---

## 💡 最佳实践

### ✅ 推荐做法
1. **合理的抓取间隔**：核心服务 15s，非核心 30s-60s
2. **标签设计**：避免高基数标签（如用户 ID）
3. **保留策略**：根据存储调整 `--storage.tsdb.retention.time`
4. **联邦集群**：大规模部署使用 Federation
5. **备份配置**：使用 Git 管理配置和告警规则

### ❌ 避免事项
1. 不要在标签中使用无限基数的值（如邮箱、IP）
2. 不要存储过长的历史数据（考虑长期存储方案如 Thanos）
3. 不要忽略告警疲劳（合理设置阈值和静默）

---

## 🔗 相关资源

- 官网：https://prometheus.io
- 文档：https://prometheus.io/docs
- GitHub: https://github.com/prometheus/prometheus
- Exporters: https://prometheus.io/docs/instrumenting/exporters
- PromQL 教程：https://prometheus.io/docs/prometheus/latest/querying/basics

---

## 📚 关联笔记

- [[Grafana]] - 可视化与告警面板
- [[Alertmanager]] - 告警管理配置
- [[Node Exporter]] - 系统指标采集
- [[Kubernetes 监控]] - K8s 监控方案

---

*创建时间：2026-02-20*
