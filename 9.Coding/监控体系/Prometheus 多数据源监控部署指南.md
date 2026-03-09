# Prometheus 多数据源监控部署指南

> 创建日期:: 2026-03-09
> 标签:: #监控 #Prometheus #Grafana #Exporter #多数据源
> 分类:: 技术文档/监控体系

---

## 📌 核心思想

> **Exporter <span style="color:rgb(255, 77, 77)">多样化</span>，Prometheus <span style="color:rgb(255, 77, 77)">统一化</span>，Grafana <span style="color:rgb(255, 77, 77)">简单化</span>**

在真实生产环境中，需要监控的数据源多种多样：**GitLab CI/CD**、**NVIDIA GPU 集群**、**数据库**、**消息队列**、**Web 服务**等。

**关键问题**：是否需要为每个数据源配置一个 Grafana 数据源？

**答案**：❌ 不需要！<span style="color:rgb(255, 77, 77)"><b>只需一个 Prometheus 数据源</b></span>，所有监控数据都通过它统一接入。

---

## 🏗️ 为什么只需要一个 Prometheus 数据源？

### 三层架构

```
┌─────────────────────────────────────────────────────────────┐
│                    多数据源监控架构                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  【采集层】Exporter 多样化                                   │
│  GitLab      Mac 系统      MySQL      Nginx      GPU        │
│    ↓           ↓             ↓          ↓         ↓         │
│  GitLab     Node         MySQL       Nginx     DCGM        │
│  Exporter   Exporter     Exporter    Exporter  Exporter    │
│    ↓           ↓             ↓          ↓         ↓         │
│  :8080      :9100         :9104      :9113     :9400       │
│    └───────────┴─────────────┴──────────┴─────────┘         │
│                            ↓                                │
│  【存储层】Prometheus 统一化                                 │
│              ┌─────────────────────────┐                    │
│              │    Prometheus           │                    │
│              │  (唯一数据源/核心枢纽)    │                    │
│              └─────────────────────────┘                    │
│                            ↓                                │
│  【展示层】Grafana 简单化                                    │
│              ┌─────────────────────────┐                    │
│              │    Grafana              │                    │
│              │  (只连接 Prometheus)     │                    │
│              └─────────────────────────┘                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 各层级作用对比

| 层级 | 组件 | 作用 | 数量 |
|------|------|------|------|
| **采集层** | Exporter | 采集不同数据源的指标 | 多个（每个数据源一个） |
| **存储层** | Prometheus | 统一存储所有指标 | **1 个**（核心枢纽） |
| **展示层** | Grafana | 统一展示和告警 | **1 个**（连接 Prometheus） |

### 核心逻辑

```
不同数据源 → 部署对应 Exporter → Prometheus 统一抓取 → Grafana 一个数据源展示
```

---

## ✅ 优势

| 优势 | 说明 |
|------|------|
| **统一管理** | 所有指标在一个地方查询，无需切换数据源 |
| **简化配置** | Grafana 只需配置一个 Prometheus 数据源 |
| **跨数据源关联** | 可以在一个图表中对比不同系统（如 CPU vs GitLab 构建数） |
| **易于扩展** | 添加新数据源只需加 Exporter，Grafana 无需改动 |
| **降低复杂度** | 不需要管理多个数据源连接和权限 |

---

## 🔌 常见数据源 Exporter 清单

| 数据源 | Exporter | 端口 | Grafana 仪表盘 ID |
|--------|----------|------|------------------|
| **GitLab CI/CD** | gitlab-ci-pipelines-exporter | 8080 | 自定义 |
| **NVIDIA GPU** | dcgm-exporter | 9400 | 12239 |
| **MySQL** | mysqld_exporter | 9104 | 9614 |
| **PostgreSQL** | postgres_exporter | 9187 | 9628 |
| **Redis** | redis_exporter | 9121 | 11613 |
| **Nginx** | nginx-prometheus-exporter | 9113 | 14072 |
| **Docker** | cAdvisor | 8080 | 12559 |
| **Kubernetes** | kube-state-metrics | 8080 | 315 |
| **Elasticsearch** | elasticsearch_exporter | 9114 | 2326 |
| **Kafka** | kafka_exporter | 9308 | 7589 |
| **RabbitMQ** | rabbitmq_exporter | 9419 | 10991 |
| **Node Exporter** | node-exporter | 9100 | 1860 |

---

## 🚀 快速部署（Docker Compose）

### 完整配置文件

```yaml
# docker-compose.yml
version: '3.8'

services:
  # ============ Prometheus (统一存储) ============
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
      - '--web.enable-lifecycle'
    restart: unless-stopped

  # ============ Grafana (统一展示) ============
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

  # ============ 各种 Exporter (按需添加) ============
  
  # Mac/服务器监控
  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
    restart: unless-stopped

  # GitLab Pipeline
  gitlab-exporter:
    image: quay.io/qubecir/gitlab-ci-pipelines-exporter:latest
    container_name: gitlab-exporter
    ports:
      - "8081:8080"
    volumes:
      - ./gitlab-exporter-config.yml:/etc/gitlab-ci-pipelines-exporter/config.yml
    restart: unless-stopped

  # MySQL
  mysql-exporter:
    image: prom/mysqld-exporter:latest
    container_name: mysql-exporter
    ports:
      - "9104:9104"
    environment:
      - DATA_SOURCE_NAME=user:password@(mysql-host:3306)/
    restart: unless-stopped

  # Redis
  redis-exporter:
    image: oliver006/redis_exporter:latest
    container_name: redis-exporter
    ports:
      - "9121:9121"
    command:
      - '--redis.addr=redis-host:6379'
    restart: unless-stopped

  # Nginx
  nginx-exporter:
    image: nginx/nginx-prometheus-exporter:latest
    container_name: nginx-exporter
    ports:
      - "9113:9113"
    command:
      - '--nginx.scrape-uri=http://nginx-host:80/stub_status'
    restart: unless-stopped

volumes:
  prometheus_data:
  grafana_data:
```

---

## 📝 Prometheus 配置

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    monitor: 'multi-source-monitor'

# 抓取配置
scrape_configs:
  # Prometheus 自身
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Node Exporter (服务器指标)
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['host.docker.internal:9100']

  # GitLab Pipeline
  - job_name: 'gitlab-exporter'
    static_configs:
      - targets: ['gitlab-exporter:8080']
    scrape_interval: 30s

  # MySQL
  - job_name: 'mysql-exporter'
    static_configs:
      - targets: ['mysql-exporter:9104']

  # Redis
  - job_name: 'redis-exporter'
    static_configs:
      - targets: ['redis-exporter:9121']

  # Nginx
  - job_name: 'nginx-exporter'
    static_configs:
      - targets: ['nginx-exporter:9113']
```

**关键点**：每个数据源一个 `job_name`，通过 `job` 标签区分。

---

## 📊 Grafana 配置

### 自动配置数据源

```yaml
# grafana/provisioning/datasources/prometheus.yml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true      # ← 设为默认，导入仪表盘时自动选中
    editable: true
```

**效果**：Grafana 启动时自动创建 Prometheus 数据源，无需手动配置！

### 推荐仪表盘模板

| 监控对象 | 仪表盘 ID | 说明 |
|----------|-----------|------|
| **Node Exporter** | 1860 | 最全面的服务器监控 |
| **NVIDIA GPU** | 12239 | DCGM Exporter 官方 |
| **MySQL** | 9614 | 官方推荐 |
| **Redis** | 11613 | 官方推荐 |
| **Nginx** | 14072 | 官方推荐 |
| **Docker** | 12559 | 容器监控 |
| **Kubernetes** | 315 | K8s 集群监控 |

### 导入方法

1. Grafana → Dashboards → Import
2. 输入仪表盘 ID（如 `1860`）
3. **Prometheus 已自动选中**（因为是默认数据源）
4. 点击 Import

---

## 🔍 如何在 Grafana 中区分不同数据源？

### 通过 job 标签筛选

每个 Exporter 在 Prometheus 中对应一个 `job`，通过标签筛选：

```promql
# 只查 Mac 系统指标
{job="node-exporter"}

# 只查 GitLab 指标
{job="gitlab-exporter"}

# 只查 MySQL 指标
{job="mysql-exporter"}

# 查所有目标状态
up
```

### 通过指标前缀区分

| 数据源 | 指标前缀 | 示例 |
|--------|----------|------|
| Node Exporter | `node_` | `node_cpu_seconds_total` |
| GitLab | `gitlab_ci_` | `gitlab_ci_pipeline_status` |
| MySQL | `mysql_` | `mysql_global_status_connections` |
| Redis | `redis_` | `redis_connected_clients` |
| Nginx | `nginx_` | `nginx_http_requests_total` |
| GPU (DCGM) | `DCGM_` | `DCGM_FI_DEV_GPU_TEMP` |

---

## 📈 仪表盘组织方式

| 方式 | 说明 | 适用场景 |
|------|------|----------|
| **不同仪表盘** | 每个数据源一个独立仪表盘 | 推荐，清晰分离 |
| **同一仪表盘不同 Panel** | 一个仪表盘里多个面板展示不同数据源 | 需要对比分析 |
| **文件夹分类** | 按业务/环境分组（如 Prod/Staging） | 多环境管理 |

### 推荐结构

```
Grafana Dashboards/
├── 📁 Infrastructure/
│   ├── Node Exporter Full (Mac/服务器)
│   └── Docker Container
├── 📁 Database/
│   ├── MySQL Overview
│   └── Redis Dashboard
├── 📁 CI/CD/
│   └── GitLab Pipeline
├── 📁 Web/
│   └── Nginx Dashboard
└── 📁 GPU/
    └── NVIDIA DCGM
```

---

## 🎯 专项配置：GitLab Pipeline 监控

### Exporter 配置

```yaml
# gitlab-exporter-config.yml
gitlab:
  url: https://gitlab.com
  token: glpat-xxxxxxxxxxxxx  # 需要 read_api 权限

projects:
  - name: group/project-1
  - name: group/project-2

pull:
  pipelines:
    enabled: true
    max_age_seconds: 86400  # 只拉取 24 小时内的数据
```

### 关键指标

| 指标名 | 类型 | 说明 |
|--------|------|------|
| `gitlab_ci_pipeline_status` | Gauge | Pipeline 状态（1=成功） |
| `gitlab_ci_pipeline_duration_seconds` | Gauge | 执行耗时 |
| `gitlab_ci_pipeline_queued_duration_seconds` | Gauge | 排队时间 |
| `gitlab_ci_pipeline_run_count` | Counter | 执行次数 |

### PromQL 示例

```promql
# Pipeline 成功率
sum(gitlab_ci_pipeline_status{status="success"}) / sum(gitlab_ci_pipeline_status) * 100

# 平均构建耗时
avg(gitlab_ci_pipeline_duration_seconds)

# 失败趋势
sum(increase(gitlab_ci_pipeline_run_count{status="failed"}[1h]))
```

---

## 🎯 专项配置：NVIDIA GPU 监控

### DCGM Exporter 配置

```yaml
# docker-compose.yml 片段
dcgm-exporter:
  image: nvcr.io/nvidia/k8s/dcgm-exporter:latest
  container_name: dcgm-exporter
  ports:
    - "9400:9400"
  runtime: nvidia
  cap_add:
    - SYS_ADMIN
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: all
            capabilities: [gpu]
```

### 关键 GPU 指标

| 指标名 | 说明 | 告警阈值 |
|--------|------|----------|
| `DCGM_FI_DEV_GPU_TEMP` | GPU 温度 | > 85°C |
| `DCGM_FI_DEV_POWER_USAGE` | 功耗 (W) | > 额定功率 90% |
| `DCGM_FI_DEV_GPU_UTIL` | GPU 利用率 | - |
| `DCGM_FI_DEV_FB_FREE` | 显存剩余 | < 10% |
| `DCGM_FI_DEV_RETIRED_DBE` | 双位 ECC 错误 | > 0 |

### GPU 告警规则

```yaml
# alert_rules.yml
groups:
  - name: gpu_alerts
    rules:
      - alert: GPUTemperatureHigh
        expr: DCGM_FI_DEV_GPU_TEMP > 85
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "GPU {{ $labels.gpu }} 温度过高"
          description: "温度 {{ $value }}°C 超过 85°C"
```

---

## ✅ 快速验证

```bash
# 1. 启动所有服务
docker compose up -d

# 2. 查看服务状态
docker compose ps

# 3. 检查 Exporter 是否正常
curl http://localhost:9100/metrics    # Node Exporter
curl http://localhost:8081/metrics    # GitLab Exporter
curl http://localhost:9104/metrics    # MySQL Exporter

# 4. 检查 Prometheus 抓取目标
# 浏览器访问：http://localhost:9090/targets
# 所有目标应该是 UP 状态

# 5. 测试 PromQL 查询
# 浏览器访问：http://localhost:9090/graph
# 输入：up                    → 所有 job 状态
# 输入：{job="node-exporter"} → 只查 Node Exporter 指标

# 6. 访问 Grafana
# 浏览器访问：http://localhost:3000
# 账号/密码：admin / admin
# 导入仪表盘 ID: 1860 (Node Exporter Full)
```

---

## ⚠️ 注意事项

| 事项 | 说明 |
|------|------|
| **Exporter 部署位置** | 必须能访问到被监控服务（网络可达） |
| **认证配置** | 数据库/Redis 等需要配置账号密码 |
| **抓取频率** | 不同数据源可设置不同 `scrape_interval` |
| **标签管理** | 给不同 job 加标签便于筛选（如 `category`, `env`） |
| **资源消耗** | Exporter 越多，Prometheus 内存占用越高 |
| **数据保留** | 默认 15 天，需要长期存储用 Thanos |
| **NVIDIA GPU** | 需要宿主机安装 NVIDIA 驱动 |
| **Mac 监控** | Node Exporter 在 Mac 上部分指标不可用 |

---

## 🔧 故障排查

### Exporter 显示 DOWN

```bash
# 1. 检查容器是否运行
docker compose ps

# 2. 查看容器日志
docker compose logs <exporter-name>

# 3. 测试网络连通性
docker exec prometheus wget -q http://<exporter>:<port>/metrics

# 4. 检查 Prometheus 配置
docker exec prometheus cat /etc/prometheus/prometheus.yml
```

### 指标查询不到

```promql
# 1. 确认指标名称
# 浏览器访问 Exporter 的 /metrics 端点查看

# 2. 确认时间范围
# Grafana 右上角时间范围是否正确

# 3. 确认标签过滤
# 是否使用了错误的 job 标签

# 4. 使用 Explore 模式
# Grafana → Explore → 输入指标名测试
```

---

## 📈 扩展建议

| 需求 | 方案 |
|------|------|
| **长期存储** | 部署 Thanos 或 VictoriaMetrics |
| **高可用** | Prometheus 集群 + 负载均衡 |
| **日志监控** | 添加 Loki + Promtail |
| **链路追踪** | 添加 Tempo 或 Jaeger |
| **告警通知** | Alertmanager + Slack/钉钉/企业微信 |
| **自动发现** | Kubernetes SD / Consul SD |
| **自定义指标** | 应用集成 Prometheus Client |

---

## 🔗 相关资源

### 官方文档

- [Prometheus Exporters](https://prometheus.io/docs/instrumenting/exporters/)
- [Grafana Dashboards](https://grafana.com/grafana/dashboards/)
- [NVIDIA DCGM](https://github.com/NVIDIA/dcgm-exporter)

### Exporter 仓库

- [gitlab-ci-pipelines-exporter](https://github.com/qaboud/gitlab-ci-pipelines-exporter)
- [dcgm-exporter](https://github.com/NVIDIA/dcgm-exporter)
- [awesome-prometheus](https://github.com/roaldnefs/awesome-prometheus)

### 相关笔记

- [[Prometheus & Grafana 监控体系指南]]
- [[时序数据库 (TSDB) 完全指南]]
- [[Kubernetes 监控体系]]

---

## 📝 总结

| 问题 | 答案 |
|------|------|
| **需要多个 Grafana 数据源吗？** | ❌ 不需要，一个 Prometheus 就够了 |
| **如何区分不同监控对象？** | 通过 `job` 标签和指标前缀 |
| **添加新数据源要改 Grafana 吗？** | ❌ 不用，只需加 Exporter + 改 Prometheus 配置 |
| **Grafana 仪表盘怎么组织？** | 按数据源/业务创建不同仪表盘 |

> **核心思想**：Exporter 多样化，Prometheus 统一化，Grafana 简单化

---

*最后更新:: 2026-03-09*
