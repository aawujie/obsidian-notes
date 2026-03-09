# Prometheus 多数据源监控部署指南

> 创建日期:: 2026-03-09
> 标签:: #监控 #Prometheus #Grafana #Exporter #多数据源
> 分类:: 技术文档/监控体系

---

## 📌 概述

在真实生产环境中，需要监控的数据源多种多样：**GitLab CI/CD**、**NVIDIA GPU 集群**、**数据库**、**消息队列**、**Web 服务**等。

本文介绍如何在 Prometheus + Grafana 架构下，统一接入和管理多数据源监控。

---

## 🏗️ 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    多数据源监控架构                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  GitLab      NVIDIA GPU      MySQL      Nginx      自定义应用    │
│    ↓            ↓             ↓          ↓           ↓          │
│  GitLab     DCGM-Exporter  MySQL       Nginx      App Metrics   │
│  Exporter   (NVIDIA)      Exporter    Exporter     Exporter    │
│    ↓            ↓             ↓          ↓           ↓          │
│  :8080       :9400          :9104      :9113       :8000        │
│    └────────────┴────────────┴──────────┴───────────┘           │
│                         ↓                                       │
│              ┌─────────────────────┐                            │
│              │    Prometheus       │                            │
│              │  (统一抓取 + 存储)    │                            │
│              └─────────────────────┘                            │
│                         ↓                                       │
│              ┌─────────────────────┐                            │
│              │      Grafana        │                            │
│              │  (统一展示 + 告警)    │                            │
│              └─────────────────────┘                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 核心逻辑

```
不同数据源 → 部署对应 Exporter → Prometheus 配置抓取 → Grafana 导入仪表盘
```

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
| **Blackbox** | blackbox_exporter | 9115 | 5344 |
| **Node Exporter** | node-exporter | 9100 | 1860 |

---

## 🚀 快速部署（Docker Compose）

### 完整配置文件

```yaml
# docker-compose.yml
version: '3.8'

services:
  # ============ Prometheus ============
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

  # ============ Grafana ============
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
      - GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-piechart-panel
    restart: unless-stopped
    depends_on:
      - prometheus

  # ============ Node Exporter (本机监控) ============
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
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    restart: unless-stopped

  # ============ GitLab Pipeline Exporter ============
  gitlab-exporter:
    image: quay.io/qubecir/gitlab-ci-pipelines-exporter:latest
    container_name: gitlab-exporter
    ports:
      - "8081:8080"
    volumes:
      - ./gitlab-exporter-config.yml:/etc/gitlab-ci-pipelines-exporter/config.yml
    restart: unless-stopped

  # ============ NVIDIA GPU Exporter (DCGM) ============
  # 需要宿主机有 NVIDIA 驱动和 GPU
  dcgm-exporter:
    image: nvcr.io/nvidia/k8s/dcgm-exporter:latest
    container_name: dcgm-exporter
    ports:
      - "9400:9400"
    runtime: nvidia
    cap_add:
      - SYS_ADMIN
    environment:
      - DCGM_EXPORTER_LISTEN=:9400
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

  # ============ MySQL Exporter ============
  mysql-exporter:
    image: prom/mysqld-exporter:latest
    container_name: mysql-exporter
    ports:
      - "9104:9104"
    environment:
      - DATA_SOURCE_NAME=monitor:password@(mysql-host:3306)/
    restart: unless-stopped

  # ============ Redis Exporter ============
  redis-exporter:
    image: oliver006/redis_exporter:latest
    container_name: redis-exporter
    ports:
      - "9121:9121"
    command:
      - '--redis.addr=redis-host:6379'
      - '--redis.password=your-password'
    restart: unless-stopped

  # ============ Nginx Exporter ============
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

# 告警规则
rule_files:
  - "alert_rules.yml"

# 抓取配置
scrape_configs:
  # Prometheus 自身
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
    labels:
      category: 'monitoring'

  # Node Exporter (服务器指标)
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['host.docker.internal:9100']
    labels:
      category: 'infrastructure'

  # GitLab Pipeline
  - job_name: 'gitlab-exporter'
    static_configs:
      - targets: ['gitlab-exporter:8080']
    scrape_interval: 30s
    labels:
      category: 'cicd'

  # NVIDIA GPU
  - job_name: 'dcgm-exporter'
    static_configs:
      - targets: ['dcgm-exporter:9400']
    scrape_interval: 15s
    labels:
      category: 'gpu'

  # MySQL
  - job_name: 'mysql-exporter'
    static_configs:
      - targets: ['mysql-exporter:9104']
    labels:
      category: 'database'

  # Redis
  - job_name: 'redis-exporter'
    static_configs:
      - targets: ['redis-exporter:9121']
    labels:
      category: 'database'

  # Nginx
  - job_name: 'nginx-exporter'
    static_configs:
      - targets: ['nginx-exporter:9113']
    labels:
      category: 'web'
```

---

## 📊 Grafana 仪表盘配置

### 自动配置数据源

```yaml
# grafana/provisioning/datasources/prometheus.yml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
```

### 推荐仪表盘模板

| 监控对象 | 仪表盘 ID | 导入命令 |
|----------|-----------|----------|
| **Node Exporter** | 1860 | 最全面的服务器监控 |
| **NVIDIA GPU** | 12239 | DCGM Exporter 官方 |
| **MySQL** | 9614 | 官方推荐 |
| **Redis** | 11613 | 官方推荐 |
| **Nginx** | 14072 | 官方推荐 |
| **Docker** | 12559 | 容器监控 |
| **Kubernetes** | 315 | K8s 集群监控 |

### 导入方法

**方法 A：在线导入（推荐）**
1. Grafana → Dashboards → Import
2. 输入仪表盘 ID（如 `12239`）
3. 选择 Prometheus 数据源
4. 点击 Import

**方法 B：离线导入**
1. 从 https://grafana.com/grafana/dashboards/ 下载 JSON
2. Grafana → Dashboards → Import → Upload JSON file

---

## 🎯 专项配置：NVIDIA GPU 监控

### DCGM Exporter 配置

```yaml
# dcgm-exporter-config.yaml
version: 0.1.0
no-hostname: false
collectors:
  - fieldID: 100
    fieldName: DCGM_FI_DEV_GPU_TEMP
    fieldHelp: Temperature Help info
  - fieldID: 155
    fieldName: DCGM_FI_DEV_POWER_USAGE
    fieldHelp: Power Usage Help info
  - fieldID: 203
    fieldName: DCGM_FI_DEV_GPU_UTIL
    fieldHelp: GPU Utilization Help info
  - fieldID: 204
    fieldName: DCGM_FI_DEV_MEM_COPY_UTIL
    fieldHelp: Memory Copy Utilization Help info
  - fieldID: 205
    fieldName: DCGM_FI_DEV_ENC_UTIL
    fieldHelp: Encoder Utilization Help info
  - fieldID: 206
    fieldName: DCGM_FI_DEV_DEC_UTIL
    fieldHelp: Decoder Utilization Help info
```

### 关键 GPU 指标

| 指标名 | 说明 | 告警阈值 |
|--------|------|----------|
| `DCGM_FI_DEV_GPU_TEMP` | GPU 温度 | > 85°C |
| `DCGM_FI_DEV_POWER_USAGE` | 功耗 (W) | > 额定功率 90% |
| `DCGM_FI_DEV_GPU_UTIL` | GPU 利用率 | - |
| `DCGM_FI_DEV_MEM_COPY_UTIL` | 显存拷贝利用率 | - |
| `DCGM_FI_DEV_FB_FREE` | 显存剩余 | < 10% |
| `DCGM_FI_DEV_SM_CLOCK` | SM 时钟频率 | - |
| `DCGM_FI_DEV_RETIRED_DBE` | 双位 ECC 错误 | > 0 |

### GPU 告警规则

```yaml
# alert_rules.yml
groups:
  - name: gpu_alerts
    rules:
      # GPU 温度过高
      - alert: GPUTemperatureHigh
        expr: DCGM_FI_DEV_GPU_TEMP > 85
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "GPU {{ $labels.gpu }} 温度过高"
          description: "GPU {{ $labels.gpu }} 温度 {{ $value }}°C 超过 85°C"

      # GPU 显存不足
      - alert: GPUMemoryLow
        expr: DCGM_FI_DEV_FB_FREE / DCGM_FI_DEV_FB_TOTAL < 0.1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "GPU {{ $labels.gpu }} 显存不足"
          description: "GPU {{ $labels.gpu }} 剩余显存 {{ $value | humanizePercentage }}"

      # GPU ECC 错误
      - alert: GPUECCError
        expr: DCGM_FI_DEV_RETIRED_DBE > 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "GPU {{ $labels.gpu }} ECC 错误"
          description: "GPU {{ $labels.gpu }} 检测到 {{ $value }} 个双位 ECC 错误"
```

---

## 🎯 专项配置：GitLab Pipeline 监控

### Exporter 配置

```yaml
# gitlab-exporter-config.yml
gitlab:
  url: https://gitlab.com
  token: glpat-xxxxxxxxxxxxx

projects:
  - name: group/project-1
  - name: group/project-2

pull:
  pipelines:
    enabled: true
    max_age_seconds: 86400
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

## ✅ 快速验证

```bash
# 1. 启动所有服务
docker-compose up -d

# 2. 查看服务状态
docker-compose ps

# 3. 检查 Exporter 是否正常
curl http://localhost:9100/metrics    # Node Exporter
curl http://localhost:9400/metrics    # NVIDIA GPU
curl http://localhost:8081/metrics    # GitLab Exporter

# 4. 检查 Prometheus 抓取目标
# 浏览器访问：http://localhost:9090/targets
# 所有目标应该是 UP 状态

# 5. 测试 PromQL 查询
# 浏览器访问：http://localhost:9090/graph
# 输入：up                    → 所有 job 状态
# 输入：DCGM_FI_DEV_GPU_TEMP  → GPU 温度
# 输入：node_cpu_seconds_total → CPU 使用率

# 6. 访问 Grafana
# 浏览器访问：http://localhost:3000
# 账号/密码：admin / admin
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
| **NVIDIA GPU** | 需要宿主机安装 NVIDIA 驱动，Docker 需要 nvidia-runtime |
| **Mac 监控** | Node Exporter 在 Mac 上部分指标不可用 |

---

## 🔧 故障排查

### Exporter 显示 DOWN

```bash
# 1. 检查容器是否运行
docker-compose ps

# 2. 查看容器日志
docker-compose logs <exporter-name>

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
# 是否使用了错误的标签过滤条件

# 4. 使用 explore 模式
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

*最后更新:: 2026-03-09*
