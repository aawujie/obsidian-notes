# Prometheus & Grafana 监控体系指南

> 创建日期:: 2026-03-09
> 标签:: #监控 #Prometheus #Grafana #DevOps #可观测性
> 分类:: 技术文档/监控体系

---

## 📌 概述

**Prometheus** 和 **Grafana** 是云原生时代最流行的开源监控组合，构成了现代可观测性基础设施的核心。

```
┌─────────────────────────────────────────────────────────────┐
│                      监控数据流向                            │
├─────────────────────────────────────────────────────────────┤
│  目标系统 → Prometheus → Grafana → 用户仪表盘                 │
│  (被监控)   (采集存储)   (可视化)    (查看告警)               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔍 Prometheus (普罗米修斯)

### 核心定位

**时间序列数据库 + 数据采集引擎**

---

### 💡 深入理解：Prometheus 本质是什么？

#### Prometheus 的多重身份

```
┌─────────────────────────────────────────────────────────────┐
│                    Prometheus 架构                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  数据采集   │  │  时序数据库  │  │  查询引擎   │         │
│  │  (Scraper)  │→ │   (TSDB)    │→ │  (PromQL)   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                            ↓                                │
│                     ┌─────────────┐                         │
│                     │   告警引擎   │                         │
│                     │ (Alertmanager)│                       │
│                     └─────────────┘                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 四个核心组件

| 组件 | 角色 | 说明 |
|------|------|------|
| **TSDB** | 数据库 | 存储时序数据（磁盘上的 `data/` 目录） |
| **Scraper** | 采集器 | 定期从目标拉取指标（Pull 模型） |
| **PromQL Engine** | 查询引擎 | 解析和执行 PromQL 查询 |
| **Alertmanager** | 告警系统 | 基于规则触发告警（独立组件） |

#### Prometheus TSDB 存储结构

```
prometheus/
├── data/
│   ├── 01CZ64K5V5E7V8K3Z3Z3Z3Z3Z3/    ← 时间块 (2 小时一个块)
│   │   ├── chunks/                    ← 压缩后的数据块
│   │   ├── index/                     ← 索引文件
│   │   └── meta.json                  ← 元数据
│   ├── 01CZ64K5V5E7V8K3Z3Z3Z3Z3Z4/
│   ├── wal/                           ← Write-Ahead Log (预写日志)
│   └── queries.active                 ← 活跃查询
└── prometheus.yml                     ← 配置文件
```

#### 核心存储特性

| 特性              | 说明                                                                |
| --------------- | ----------------------------------------------------------------- |
| **时间块 (Block)** | <span style="color:rgb(195, 117, 255)">每 2 小时数据打包成一个块，独立压缩</span> |
| **WAL 日志**      | 先写日志再落盘，保证数据不丢失                                                   |
| **内存映射 (mmap)** | 查询时直接 mmap 块文件，减少内存拷贝                                             |
| **自动压缩**        | Gorilla 压缩算法，压缩率 ~5:1                                             |
| **自动过期**        | 配置保留时长后自动删除旧块                                                     |

#### Prometheus vs 其他时序数据库

| 维度 | Prometheus | InfluxDB | TimescaleDB |
|------|------------|----------|-------------|
| **定位** | 监控系统 | 通用 TSDB | PostgreSQL 扩展 |
| **数据模型** | 指标 + 标签 | 测量 + 标签 + 字段 | 表 + 行 + 列 |
| **采集方式** | Pull (拉取) | Push (推送) | 两者都支持 |
| **查询语言** | PromQL | InfluxQL/Flux | SQL |
| **存储引擎** | 自研 TSDB | TSM 引擎 | PostgreSQL |
| **集群支持** | 需 Thanos | 商业版 | 内置 |
| **典型场景** | 云原生监控 | IoT/通用 | 需要 SQL 的场景 |

#### ⚠️ Prometheus 不适合的场景

| 场景        | 原因           | 替代方案                                                               |
| --------- | ------------ | ------------------------------------------------------------------ |
| **长期存储**  | 默认只保留 15 天   | Thanos / Cortex / VictoriaMetrics                                  |
| **高基数数据** | 标签组合爆炸导致内存溢出 | InfluxDB / ClickHouse                                              |
| **精确去重**  | 不支持精确去重逻辑    | 专用数据库                                                              |
| **事务支持**  | 无 ACID 事务    | 关系数据库                                                              |
| **随机读写**  | 只支持追加写入      | 关系数据库                                                              |
| **日志存储**  | 不是为日志设计的     | <span style="color:rgb(195, 117, 255)">Loki / Elasticsearch</span> |

#### 📝 总结

| 问题                    | 答案                                                                         |
| --------------------- | -------------------------------------------------------------------------- |
| **Prometheus 是数据库吗？** | ✅ 是，内置了自研的时序数据库引擎                                                          |
| **只是数据库吗？**           | ❌ 不是，还包含采集、查询、告警等完整功能                                                      |
| **能当通用数据库用吗？**        | ❌ 不适合，<span style="color:rgb(195, 117, 255)">专为监控场景设计</span>               |
| **能长期存储吗？**           | ❌ 原生不支持，<span style="color:rgb(195, 117, 255)">需配合 Thanos/Cortex</span>    |
| **和 Grafana 什么关系？**   | <span style="color:rgb(195, 117, 255)">Prometheus 存储数据，Grafana 负责展示</span> |

> **一句话理解**：Prometheus = 时序数据库 + 数据采集器 + 查询引擎 + 告警系统
> 
> **数据库是它的核心存储引擎，但监控才是它的完整使命。**

---

### 架构组件

| 组件                    | 功能                                                                      |
| --------------------- | ----------------------------------------------------------------------- |
| **Prometheus Server** | 核心服务，负责采集和存储数据                                                          |
| **Exporters**         | <span style="color:rgb(195, 117, 255)">将各种系统的指标暴露为 Prometheus 格式</span> |
| **Pushgateway**       | 支持短期任务推送指标                                                              |
| **Alertmanager**      | 处理告警路由、去重、静默                                                            |
| **Service Discovery** | 自动发现监控目标（K8s、Consul 等）                                                  |

### 数据模型

```promql
# 指标格式
metric_name{label1="value1", label2="value2"}

# 示例
http_requests_total{method="POST", handler="/api/users", status="200"}
```

### 核心概念

- **Metric（指标）**: 带时间戳的数值数据
- **Label（标签）**: 多维度标识，用于过滤和聚合
- **PromQL**: <span style="color:rgb(195, 117, 255)">Prometheus 查询语言，功能强大</span>

### 常用 PromQL 示例

```promql
# 查询当前值
node_cpu_seconds_total

# 速率计算（每秒增长）
rate(http_requests_total[5m])

# 聚合查询
sum(rate(http_requests_total[5m])) by (service)

# 百分位计算
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

### 四种指标类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| **Counter** | 只增不减的计数器 | 请求总数、错误数 |
| **Gauge** | 可增可减的瞬时值 | CPU 使用率、内存占用 |
| **Histogram** | 直方图，统计分布 | 请求延迟、响应时间 |
| **Summary** | 摘要，计算分位数 | 延迟百分位 |

---

## 📊 Grafana

### 核心定位

**数据可视化与仪表盘平台**

### 支持的数据源

- **时序数据库**: <span style="color:rgb(195, 117, 255)">Prometheus</span>, InfluxDB, TimescaleDB
- **关系数据库**: <span style="color:rgb(195, 117, 255)">MySQL</span>, <span style="color:rgb(195, 117, 255)">PostgreSQL</span>, SQL Server
- **日志系统**: Elasticsearch, Loki
- **云服务**: AWS CloudWatch, Azure Monitor, Google Cloud
- **其他**: Jaeger, Zipkin, Datadog, New Relic

### 核心功能

1. **仪表盘 (Dashboards)**: 可定制的可视化面板
2. **告警 (Alerting)**: 基于阈值的告警规则
3. **探索 (Explore)**: 临时查询和数据探索
4. **告警通知**: 支持邮件、Slack、钉钉、企业微信等

### 面板类型

- Time series（时间序列图）
- Stat（统计数字）
- Gauge（仪表盘）
- Bar chart（柱状图）
- Heatmap（热力图）
- Table（表格）
- Logs（日志）
- Trace（链路追踪）

---

## 🔌 Grafana 插件推荐

### 🏆 官方必装插件

| 插件名称 | 类型 | 用途 |
|----------|------|------|
| **Prometheus** | Data Source | Prometheus 数据源连接 |
| **Loki** | Data Source | 日志查询和展示 |
| **Tempo** | Data Source | 分布式追踪 |
| **Alertmanager** | App | 告警管理 |
| **Worldmap Panel** | Panel | 地理数据可视化 |

### ⭐ 热门社区插件

#### 数据源插件

| 插件 | 描述 | 安装命令/ID |
|------|------|-------------|
| **ClickHouse** | 高性能 OLAP 数据库支持 | `grafana-clickhouse-datasource` |
| **Redis** | Redis 监控数据源 | `redis-datasource` |
| **MongoDB** | MongoDB 数据源 | `grafana-mongodb-datasource` |
| **Elasticsearch** | ES 日志和指标 | 内置 |

#### 面板插件

| 插件 | 描述 | 适用场景 |
|------|------|----------|
| **Bar Gauge** | 条形仪表盘 | 多指标对比 |
| **Pie Chart** | 饼图 | 占比展示 |
| **Status History** | 状态历史 | 服务状态时间线 |
| **State Timeline** | 状态时间线 | 告警状态变化 |
| **XY Chart** | 散点图 | 相关性分析 |
| **Canvas Panel** | 自定义画布 | 拓扑图、流程图 |
| **Business Text** | 富文本 | 自定义说明文字 |
| **Flowchart Panel** | 流程图 | 业务流程展示 |

#### 应用插件

| 插件 | 描述 | 用途 |
|------|------|------|
| **Grafana Image Renderer** | 图片渲染 | 仪表盘截图、告警图片 |
| **Grafana Report** | 报告生成 | 定期生成 PDF 报告 |
| **Clock Panel** | 时钟 | 显示时间、倒计时 |
| **Announcement** | 公告 | 仪表盘顶部公告栏 |

### 🎨 仪表盘模板推荐

从 [Grafana Dashboards](https://grafana.com/grafana/dashboards/) 导入现成模板：

| 模板 ID | 名称 | 用途 |
|---------|------|------|
| **1860** | Node Exporter Full | Linux 服务器完整监控 |
| **315** | Kubernetes Cluster | K8s 集群监控 |
| **10771** | Prometheus Stats | Prometheus 自身监控 |
| **9614** | MySQL Overview | MySQL 数据库监控 |
| **11613** | Redis Dashboard | Redis 监控 |
| **14072** | Nginx Dashboard | Nginx 服务监控 |
| **12559** | Docker Container | Docker 容器监控 |

---

## 🚀 快速开始

### Docker 部署（推荐）

```bash
# docker-compose.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
    restart: unless-stopped
    depends_on:
      - prometheus

volumes:
  prometheus_data:
  grafana_data:
```

### Prometheus 配置示例

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']

  - job_name: 'kubernetes'
    kubernetes_sd_configs:
      - role: pod
```

### 常用 Exporters

| Exporter | 端口 | 用途 |
|----------|------|------|
| **Node Exporter** | 9100 | Linux/Unix 系统指标 |
| **cAdvisor** | 8080 | Docker 容器指标 |
| **MySQL Exporter** | 9104 | MySQL 数据库 |
| **Redis Exporter** | 9121 | Redis 数据库 |
| **Nginx Exporter** | 9113 | Nginx 服务 |
| **Blackbox Exporter** | 9115 | 网络探测（HTTP/TCP/ICMP） |

---

## 📈 最佳实践

### 指标命名规范

```
# 格式：<name>_<unit>_<per>
# 示例：
http_requests_total          # 总请求数（Counter）
node_memory_usage_bytes      # 内存使用字节数（Gauge）
http_request_duration_seconds # 请求延迟秒数（Histogram）
```

### 标签设计原则

- 使用小写和数字
- 避免高基数标签（如 user_id、email）
- 保持标签值有限且可枚举
- 统一标签命名（如 `instance`, `job`, `service`）

### 告警规则设计

```yaml
# rules.yml
groups:
  - name: example
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "高 CPU 使用率"
          description: "{{ $labels.instance }} CPU 使用率超过 80%"
```

### 保留策略

| 数据保留时间 | 存储需求 | 建议 |
|--------------|----------|------|
| 15 天 | 基准 | 默认配置 |
| 30 天 | 2x | 一般生产环境 |
| 90 天 | 6x | 合规要求 |
| 长期存储 | - | 使用 Thanos/Cortex |

---

## 🔗 相关资源

### 官方文档

- [Prometheus 官方文档](https://prometheus.io/docs/)
- [Grafana 官方文档](https://grafana.com/docs/)
- [PromQL 官方文档](https://prometheus.io/docs/prometheus/latest/querying/basics/)

### 学习资源

- [Awesome Prometheus](https://github.com/roaldnefs/awesome-prometheus) - 资源集合
- [Grafana Dashboards](https://grafana.com/grafana/dashboards/) - 仪表盘模板
- [Prometheus 实战](https://yunlzheng.gitbook.io/prometheus-book/) - 中文教程

### 进阶方案

| 方案 | 用途 |
|------|------|
| **Thanos** | Prometheus 高可用 + 长期存储 |
| **Cortex** | 多租户时序数据库 |
| **VictoriaMetrics** | 高性能 Prometheus 替代 |
| **Mimir** | Grafana  Labs 的时序数据库 |
| **Loki** | 日志聚合（Grafana  Labs） |
| **Tempo** | 分布式追踪（Grafana  Labs） |

---

## 📝 笔记链接

- [[Kubernetes 监控体系]]
- [[ELK Stack 日志系统]]
- [[Docker 容器管理]]
- [[Linux 性能调优]]
- [[时序数据库 (TSDB) 完全指南]]

---

## 🛠️ 实战方案：GitLab Pipeline 监控

### 场景描述

监控 GitLab CI/CD Pipeline 运行状态，实现：
- 实时查看 Pipeline 执行情况和成功率
- 统计各项目的构建频率和耗时
- 失败 Pipeline 及时告警通知
- 分析构建瓶颈和优化方向

### 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    GitLab Pipeline 监控架构                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  GitLab API → gitlab-exporter → Prometheus → Grafana            │
│     ↓            ↓              ↓           ↓                   │
│  (数据源)    (指标转换)      (存储)      (展示告警)              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 步骤一：部署 GitLab Exporter

#### 方案 A：使用现成 Exporter（推荐）

```bash
# 使用 gitlab-ci-pipelines-exporter
docker run -d \
  --name gitlab-exporter \
  -p 8080:8080 \
  -e GITLAB_URL=https://gitlab.com \
  -e GITLAB_TOKEN=glpat-xxxxxxxxxxxxx \
  -v ./config.yml:/etc/gitlab-ci-pipelines-exporter/config.yml \
  quay.io/qubecir/gitlab-ci-pipelines-exporter:latest
```

#### 配置文件 `config.yml`

```yaml
gitlab:
  url: https://gitlab.com
  token: glpat-xxxxxxxxxxxxx  # GitLab Personal Access Token

projects:
  - name: group/project-1
    pull:
      pipelines: true
      metrics:
        - success_count
        - failed_count
        - duration_seconds
  - name: group/project-2
    pull:
      pipelines: true

pull:
  pipelines:
    enabled: true
    max_age_seconds: 86400  # 只拉取 24 小时内的数据
  environments:
    enabled: true
```

#### 方案 B：自建 Exporter（Python 示例）

```python
# gitlab_exporter.py
import requests
import time
from prometheus_client import start_http_server, Gauge, Counter

GITLAB_URL = "https://gitlab.com"
GITLAB_TOKEN = "glpat-xxxxxxxxxxxxx"

# 定义指标
pipeline_status = Gauge('gitlab_pipeline_status', 'Pipeline 状态', ['project', 'branch'])
pipeline_duration = Gauge('gitlab_pipeline_duration_seconds', 'Pipeline 耗时', ['project', 'branch'])
pipeline_total = Counter('gitlab_pipeline_total', 'Pipeline 总数', ['project', 'status'])

def fetch_pipelines():
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    projects = ["group%2Fproject-1", "group%2Fproject-2"]  # URL 编码
    
    for project in projects:
        resp = requests.get(
            f"{GITLAB_URL}/api/v4/projects/{project}/pipelines",
            headers=headers,
            params={"per_page": 100}
        )
        for p in resp.json():
            status = 1 if p['status'] == 'success' else 0
            pipeline_status.labels(project=project, branch=p['ref']).set(status)
            pipeline_duration.labels(project=project, branch=p['ref']).set(p.get('duration', 0))
            pipeline_total.labels(project=project, status=p['status']).inc()

if __name__ == '__main__':
    start_http_server(8000)
    while True:
        fetch_pipelines()
        time.sleep(60)
```

### 步骤二：配置 Prometheus

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'gitlab-exporter'
    static_configs:
      - targets: ['gitlab-exporter:8080']
    scrape_interval: 30s
    
  - job_name: 'gitlab-custom-exporter'
    static_configs:
      - targets: ['localhost:8000']
    scrape_interval: 60s
```

### 步骤三：Grafana 仪表盘配置

#### 关键指标面板

| 面板名称 | 指标类型 | PromQL 示例 |
|----------|----------|-------------|
| **Pipeline 成功率** | Stat | `sum(gitlab_pipeline_status{status="success"}) / sum(gitlab_pipeline_status) * 100` |
| **今日构建次数** | Stat | `sum(increase(gitlab_pipeline_total[24h]))` |
| **平均构建耗时** | Stat | `avg(gitlab_pipeline_duration_seconds)` |
| **失败 Pipeline 趋势** | Time series | `sum(increase(gitlab_pipeline_total{status="failed"}[1h]))` |
| **各项目构建状态** | Bar gauge | `gitlab_pipeline_status by (project)` |
| **构建耗时分布** | Histogram | `histogram_quantile(0.95, rate(gitlab_pipeline_duration_bucket[5m]))` |

#### 推荐仪表盘布局

```
┌────────────────────────────────────────────────────────────┐
│  📊 GitLab CI/CD 监控仪表盘                                  │
├────────────────────────────────────────────────────────────┤
│  [成功率 98%]  [今日构建 156]  [平均耗时 3m20s]  [失败 3]     │
├────────────────────────────────────────────────────────────┤
│  📈 24 小时 Pipeline 趋势图 (成功/失败/取消)                   │
├────────────────────────────────────────────────────────────┤
│  📊 各项目构建状态对比  │  📊 构建耗时 Top10 项目              │
├────────────────────────────────────────────────────────────┤
│  📋 最近失败 Pipeline 列表 (表格)                            │
└────────────────────────────────────────────────────────────┘
```

### 步骤四：告警规则配置

```yaml
# alert_rules.yml
groups:
  - name: gitlab_pipeline_alerts
    rules:
      # Pipeline 连续失败告警
      - alert: GitLabPipelineHighFailureRate
        expr: |
          sum(increase(gitlab_pipeline_total{status="failed"}[1h])) 
          / sum(increase(gitlab_pipeline_total[1h])) > 0.2
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "GitLab Pipeline 失败率过高"
          description: "过去 1 小时 Pipeline 失败率 {{ $value | humanizePercentage }}"

      # 单个项目连续失败
      - alert: GitLabProjectPipelineFailed
        expr: |
          gitlab_pipeline_status{status="failed"} == 0
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "项目 {{ $labels.project }} Pipeline 失败"
          description: "分支 {{ $labels.branch }} 构建失败"

      # 构建耗时过长
      - alert: GitLabPipelineSlow
        expr: |
          gitlab_pipeline_duration_seconds > 600  # 超过 10 分钟
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Pipeline 构建耗时过长"
          description: "项目 {{ $labels.project }} 构建耗时 {{ $value }}秒"
```

### 步骤五：告警通知配置

#### Alertmanager 配置

```yaml
# alertmanager.yml
global:
  smtp_smarthost: 'smtp.example.com:587'
  smtp_from: 'alertmanager@example.com'

route:
  group_by: ['alertname']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'slack-notifications'
  routes:
    - match:
        severity: critical
      receiver: 'critical-alerts'

receivers:
  - name: 'slack-notifications'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/xxx/yyy/zzz'
        channel: '#ci-alerts'
        title: '🚨 GitLab Pipeline 告警'
        text: '{{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'

  - name: 'critical-alerts'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/xxx/yyy/zzz'
        channel: '#ci-critical'
    email_configs:
      - to: 'devops-team@example.com'
```

### 关键指标说明

| 指标名称 | 类型 | 说明 |
|----------|------|------|
| `gitlab_pipeline_status` | Gauge | Pipeline 状态（1=成功，0=失败） |
| `gitlab_pipeline_duration_seconds` | Gauge | Pipeline 执行耗时（秒） |
| `gitlab_pipeline_total` | Counter | Pipeline 执行总数（按状态分类） |
| `gitlab_pipeline_queued_seconds` | Gauge | Pipeline 排队等待时间 |
| `gitlab_job_status` | Gauge | 单个 Job 状态 |
| `gitlab_runner_status` | Gauge | Runner 在线状态 |

### 常用 PromQL 查询

```promql
# 过去 24 小时成功率
sum(increase(gitlab_pipeline_total{status="success"}[24h])) 
/ sum(increase(gitlab_pipeline_total[24h])) * 100

# 各项目平均构建耗时
avg(gitlab_pipeline_duration_seconds) by (project)

# 失败次数 Top10 项目
topk(10, sum(increase(gitlab_pipeline_total{status="failed"}[7d])) by (project))

# 构建耗时 P95
histogram_quantile(0.95, rate(gitlab_pipeline_duration_bucket[5m]))

# 当前排队中的 Pipeline
sum(gitlab_pipeline_status{status="running"})
```

### 扩展功能

| 功能 | 实现方式 |
|------|----------|
| **钉钉/企业微信通知** | Alertmanager Webhook |
| **构建报告邮件** | Grafana Report 插件 |
| **与 GitLab 双向同步** | GitLab API + Webhook |
| **多 GitLab 实例** | 多个 Exporter 实例 + Label 区分 |
| **成本分析** | 统计 Runner 使用时长 × 单价 |

### 注意事项

1. **Token 权限**：GitLab Token 需要 `read_api` 权限
2. **API 限流**：GitLab.com 有 API 调用限制，建议拉取间隔 ≥30s
3. **数据保留**：Pipeline 数据建议保留 7-30 天，避免存储膨胀
4. **自托管 GitLab**：如果是自建 GitLab，替换 `GITLAB_URL` 即可
5. **高可用**：生产环境建议部署多个 Exporter 实例

---

*最后更新:: 2026-03-09*
