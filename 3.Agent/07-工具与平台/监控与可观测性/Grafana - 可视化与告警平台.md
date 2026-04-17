# Grafana - 可视化与告警平台

> 💎 **标签**: #监控 #Grafana #可视化 #DevOps #可观测性 #Dashboard

---

## 📌 概述

**Grafana** 是一个开源的数据可视化和监控平台，主要用于展示时间序列数据。它本身不存储数据，而是作为**数据源的可视化前端**，支持 Prometheus、InfluxDB、MySQL、Elasticsearch 等多种数据源。

### 核心特点

- **多数据源支持**：40+ 种数据源插件（Prometheus、MySQL、ES、CloudWatch 等）
- **丰富的图表**：时序图、仪表盘、热力图、直方图、地理图等
- **灵活的 Dashboard**：可自定义面板、变量、模板
- **告警系统**：内置告警规则、通知渠道、告警状态管理
- **权限管理**：团队、角色、文件夹级权限控制
- **插件生态**：丰富的面板插件和数据源插件

---

## 🏗️ 架构组件

```
┌─────────────────┐
│    Grafana      │
│   (可视化层)     │
└────────┬────────┘
         │
    ┌────┴────┬────────────┬──────────┐
    │         │            │          │
    ▼         ▼            ▼          ▼
┌───────┐ ┌───────┐  ┌─────────┐ ┌────────┐
│PromQL │ │ MySQL │  │Elastic- │ │ Loki   │
│数据源 │ │ 数据源 │  │ search  │ │ (日志) │
└───────┘ └───────┘  └─────────┘ └────────┘
```

### 主要组件

| 组件 | 说明 |
|------|------|
| **Dashboard** | 可视化面板，包含多个 Panel |
| **Panel** | 单个图表或可视化组件 |
| **Data Source** | 数据源配置（Prometheus、MySQL 等） |
| **Alert Rule** | 告警规则定义 |
| **Notification Channel** | 告警通知渠道（邮件、Slack 等） |
| **Folder** | Dashboard 分组和权限管理 |

---

## 📊 核心概念

### 1. Dashboard（仪表板）
多个 Panel 的集合，用于展示相关的监控指标。
- 支持导入/导出（JSON 格式）
- 支持模板变量（动态筛选）
- 支持自动刷新（5s、10s、30s 等）
- 支持时间范围选择（1h、24h、7d 等）

### 2. Panel（面板）
单个可视化组件，支持多种类型：
- **Time series**：时序图（最常用）
- **Stat**：单值统计（当前值、百分比）
- **Gauge**：仪表盘（进度条式）
- **Bar chart**：柱状图
- **Table**：表格
- **Heatmap**：热力图
- **Geomap**：地理图

### 3. Data Source（数据源）
Grafana 支持的数据源类型：
```
时序数据库: Prometheus, InfluxDB, TimescaleDB, Graphite
关系数据库: MySQL, PostgreSQL, SQL Server
日志系统: Loki, Elasticsearch
云平台: AWS CloudWatch, Azure Monitor, GCP Monitoring
其他: Jaeger (追踪), Zipkin, Alertmanager
```

### 4. Variables（变量）
动态参数，用于 Dashboard 的灵活筛选：
```
$job     → 服务名称 (api, web, worker)
$instance → 实例 IP (192.168.1.1, 192.168.1.2)
$region  → 区域 (us-east, cn-north)
```

---

## 🔧 安装与配置

### Docker 安装
```bash
docker run -d \
  -p 3000:3000 \
  -e "GF_SECURITY_ADMIN_PASSWORD=admin" \
  -v grafana-storage:/var/lib/grafana \
  --name grafana \
  grafana/grafana:latest
```

### 配置文件 (grafana.ini)
```ini
[server]
http_port = 3000
domain = monitoring.example.com
root_url = %(protocol)s://%(domain)s:%(http_port)s/

[security]
admin_user = admin
admin_password = admin

[users]
allow_sign_up = false

[auth.anonymous]
enabled = false

[alerting]
enabled = true
evaluation_timeout_seconds = 30
```

---

## 📈 创建 Dashboard 示例

### 1. 添加 Prometheus 数据源
```
设置 → Data Sources → Add data source → Prometheus
URL: http://prometheus:9090
```

### 2. 创建 CPU 使用率面板

**Panel 配置**:
- Type: Time series
- Title: CPU Usage by Instance
- Query:
```promql
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```
- Legend: `{{instance}}`
- Unit: Percent (0-100)
- Min: 0, Max: 100

### 3. 创建内存使用率面板

**Panel 配置**:
- Type: Gauge
- Title: Memory Usage
- Query:
```promql
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
```
- Thresholds:
  - Green: 0-60
  - Yellow: 60-80
  - Red: 80-100

### 4. 创建请求量统计面板

**Panel 配置**:
- Type: Stat
- Title: Requests per Second
- Query:
```promql
sum(rate(http_requests_total[5m]))
```
- Unit: reqps (requests per second)
- Color mode: Background
```

---

## 🚨 告警配置

### 告警规则结构
```
Alert Name: High CPU Usage
Folder: Infrastructure
Evaluation group: every 1m
Condition: WHEN last() OF query(A, 5m, now) IS ABOVE 80
```

### 告警通知渠道

#### 1. 邮件通知
```ini
[smtp]
enabled = true
host = smtp.gmail.com:587
user = alert@example.com
password = xxxxx
from_address = alert@example.com
```

#### 2. Slack 通知
```json
{
  "url": "https://hooks.slack.com/services/xxx/yyy/zzz",
  "channel": "#alerts",
  "username": "Grafana"
}
```

#### 3. 钉钉通知
```json
{
  "url": "https://oapi.dingtalk.com/robot/send?access_token=xxx",
  "message_type": "markdown"
}
```

### 告警状态
- **Normal**：正常，未触发
- **Pending**：触发中，持续时间未达阈值
- **Firing**：已触发，发送告警
- **NoData**：无数据
- **Error**：查询错误

---

## 💡 最佳实践

### ✅ Dashboard 设计
1. **分层设计**：
   - L1: 全局概览（业务 KPI）
   - L2: 服务层级（各服务指标）
   - L3: 实例层级（单机详情）

2. **合理布局**：
   - 重要指标放顶部
   - 相关指标放一起
   - 使用 Row 分组

3. **变量使用**：
   - 用变量替代硬编码值
   - 支持多选和全部选项
   - 使用 `label_values()` 动态获取

### ✅ 告警设计
1. **告警分级**：
   - P0: 紧急（电话通知）
   - P1: 重要（Slack + 邮件）
   - P2: 一般（邮件）

2. **避免告警风暴**：
   - 合理设置 `for` 持续时间
   - 使用告警分组
   - 配置静默规则

3. **有意义的告警**：
   - 清晰的标题和描述
   - 包含实例和指标信息
   - 提供 runbook 链接

### ❌ 避免事项
1. Dashboard 过于复杂（>50 个 Panel）
2. 查询过于频繁（刷新间隔 <10s）
3. 告警阈值不合理（过多误报）
4. 没有文档和说明

---

## 🔗 实用技巧

### 1. 导入现成 Dashboard
Grafana 官方库：https://grafana.com/grafana/dashboards

```
Node Exporter Full → ID: 1860
Prometheus Stats → ID: 2
Nginx → ID: 12708
```

### 2. 导出 Dashboard
```bash
# 通过 API 导出
curl -H "Authorization: Bearer <token>" \
  http://localhost:3000/api/dashboards/uid/<uid>
```

### 3. 使用模板变量
```promql
# 动态选择 job
label_values(job)

# 动态选择 instance
label_values(node_cpu_seconds_total, instance)

# 依赖变量
label_values(http_requests_total{job="$job"}, instance)
```

### 4. 常用 PromQL + Grafana 组合
```promql
# 同比/环比
metric / metric offset 1d

# 移动平均
avg_over_time(metric[1h])

# 预测
predict_linear(metric[1h], 3600)

# 分位数
histogram_quantile(0.95, rate(metric_bucket[5m]))
```

---

## 🔌 常用插件

### 面板插件
- **Pie Chart**：饼图
- **Worldmap Panel**：世界地图
- **Discrete**：离散状态图
- **Flowcharting**：流程图

### 数据源插件
- **Redis**：Redis 数据库
- **MongoDB**：MongoDB 数据库
- **Snowflake**：Snowflake 数据仓库
- **Datadog**：Datadog 监控

---

## 📚 关联笔记

- [[Prometheus]] - 监控指标收集系统
- [[Loki]] - 日志聚合系统
- [[Alertmanager]] - 告警管理配置
- [[监控体系设计]] - 整体监控方案

---

## 🔗 相关资源

- 官网：https://grafana.com
- 文档：https://grafana.com/docs
- Dashboard 库：https://grafana.com/grafana/dashboards
- 插件库：https://grafana.com/grafana/plugins
- GitHub: https://github.com/grafana/grafana

---

*创建时间：2026-02-20*
