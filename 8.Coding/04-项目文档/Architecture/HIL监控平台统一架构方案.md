# HIL 监控平台统一架构方案

> 将 `gitlab_runner_tool` 的功能迁移到 `prometheus_grafana` 项目，统一监控和管理平台。
> 创建时间：2026-03-18
> 状态：方案设计

---

## 一、现状分析

### 1.1 当前两套系统

| 维度 | prometheus_grafana | gitlab_runner_tool |
|------|-------------------|-------------------|
| 定位 | Runner 实时状态监控 | Job 管理 + Runner 运维 |
| 数据采集 | 自定义 Exporter（轮询 GitLab API） | CI 脚本主动上报 + GitLab API 查询 |
| 存储 | Prometheus TSDB（时序指标） | SQLite（事件记录） |
| 展示 | Grafana Dashboard | 自研 Web UI（FastAPI + Jinja2） |
| 技术栈 | Docker Compose + Python | FastAPI + Paramiko + WebSocket |
| 部署 | 远程服务器 10.24.99.65 | hil_auto_test 仓库内 |

### 1.2 两套系统的重叠与互补

```
                    prometheus_grafana          gitlab_runner_tool
                    ──────────────────          ──────────────────
Runner 在线/离线        ✅ (实时 15s)              ✅ (API 缓存 12s)
Runner 暂停/恢复        ❌                         ✅ (Web UI 按钮)
Runner 当前 Job         ✅ (job_info 指标)         ✅ (running jobs 列表)
Job 执行历史            ❌                         ✅ (SQLite 7天)
Job 阶段进度            ❌                         ✅ (stages_json)
Job 耗时分析            ❌                         ✅ (直方图/CDF/箱线图)
Pipeline 管理           ❌                         ✅ (查看/取消/重试)
SSH 终端                ❌                         ✅ (WebSocket)
历史数据回填            ✅ (backfill.py)           ❌
系统指标 (CPU/内存)     ✅ (Node Exporter)         ❌
告警通知                ❌                         ✅ (飞书, FOTA 自动暂停)
```

### 1.3 gitlab_runner_tool 数据库现状

- **路径**：`hil_auto_test/gitlab_runner_tool/data/job_stages.db`
- **大小**：56MB
- **记录数**：~3,446 条（7天数据）
- **日增量**：~500 条/天
- **覆盖**：6 车型 × 10 功能域 × 11 Runner

---

## 二、目标架构

### 2.1 设计原则

1. **单一数据源**：消除两套系统的重叠，每种数据只存一处
2. **关注点分离**：时序指标用 Prometheus，事件明细用 PostgreSQL
3. **统一展示**：所有可视化收敛到 Grafana
4. **接口兼容**：CI 脚本的上报接口保持不变，零侵入迁移
5. **轻量管理**：操作类功能（暂停/恢复/SSH）保留为独立微服务

### 2.2 架构总览

```
                          ┌─────────────────────────────────────┐
                          │          数据采集层                   │
                          ├─────────────────────────────────────┤
                          │                                     │
   GitLab API ────────────┤  Runner Exporter (:9253)            │
   (轮询 30s)             │  - Runner 状态、在线、活跃            │
                          │  - 当前 Job 信息                     │
                          │  - Job 聚合指标 (新增)                │
                          │                                     │
   CI Scripts ────────────┤  Job API Service (:8080, 新建)       │
   (POST 上报)            │  - 接收阶段进度上报                    │
                          │  - 写入 PostgreSQL                   │
                          │  - 推送 Prometheus 指标               │
                          └────────────┬──────────┬─────────────┘
                                       │          │
                          ┌────────────▼──┐  ┌────▼──────────┐
                          │  PostgreSQL   │  │  Prometheus   │
                          │  (:5432)      │  │  (:9090)      │
                          │               │  │               │
                          │  jobs 表       │  │  时序指标      │
                          │  job_stages 表 │  │  Runner 状态   │
                          │  (事件明细)    │  │  Job 聚合      │
                          └───────┬───────┘  └──────┬────────┘
                                  │                  │
                          ┌───────▼──────────────────▼────────┐
                          │            Grafana (:3000)         │
                          │                                    │
                          │  Dashboard: Runner 实时状态          │
                          │  Dashboard: Job 通过率趋势           │
                          │  Dashboard: Job 历史明细             │
                          │  Dashboard: 耗时分析                 │
                          │  Dashboard: Pipeline 概览           │
                          │  Alerting: 异常告警 → 飞书           │
                          └──────────────────────────────────── ┘

                          ┌─────────────────────────────────────┐
                          │       管理 API Service (:8081)       │
                          │  (轻量 FastAPI, 从 runner_tool 精简)  │
                          │                                     │
                          │  POST /runners/{id}/pause            │
                          │  POST /runners/{id}/resume           │
                          │  POST /pipelines/trigger             │
                          │  WS   /terminal (SSH)                │
                          │                                     │
                          │  Grafana Data Links 链接到此服务       │
                          └─────────────────────────────────────┘
```

### 2.3 Docker Compose 服务清单

```yaml
services:
  # === 数据存储 ===
  prometheus:
    image: prom/prometheus:latest
    ports: ["9090:9090"]
    volumes:
      - prometheus_data:/prometheus
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  postgres:                          # 新增
    image: postgres:16-alpine
    ports: ["5432:5432"]
    environment:
      POSTGRES_DB: hil_monitor
      POSTGRES_USER: hil
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

  # === 数据展示 ===
  grafana:
    image: grafana/grafana:latest
    ports: ["3000:3000"]
    environment:
      GF_AUTH_ANONYMOUS_ENABLED: "true"
      GF_AUTH_ANONYMOUS_ORG_ROLE: Viewer
      GF_INSTALL_PLUGINS: "grafana-clock-panel,grafana-piechart-panel"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning

  # === 数据采集 ===
  node-exporter:
    image: prom/node-exporter:latest
    ports: ["9100:9100"]

  # gitlab-runner-exporter: 宿主机 uv run（已有）
  # job-api-service: 宿主机或 Docker（新建）

volumes:
  prometheus_data:
  postgres_data:                     # 新增
  grafana_data:
```

---

## 三、数据模型设计

### 3.1 PostgreSQL 表结构

```sql
-- 核心 Job 记录表
CREATE TABLE jobs (
    job_id              BIGINT PRIMARY KEY,
    job_name            TEXT,
    job_status          TEXT NOT NULL,          -- running/success/failed/canceled
    started_at          TIMESTAMPTZ,
    finished_at         TIMESTAMPTZ,
    duration_seconds    DOUBLE PRECISION,
    runner_name         TEXT,
    runner_id           INTEGER,
    function_case       TEXT,                   -- fusa/parking/hmi/...
    vehicle_id          TEXT,                   -- P03/P177/C01/DE09
    pipeline_id         BIGINT,
    ref                 TEXT,                   -- 分支
    commit_sha          TEXT,
    failure_reason      TEXT,
    web_url             TEXT,
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW()
);

-- Job 阶段进度表（一对多）
CREATE TABLE job_stages (
    id                  SERIAL PRIMARY KEY,
    job_id              BIGINT REFERENCES jobs(job_id) ON DELETE CASCADE,
    stage               TEXT NOT NULL,          -- 初始化/环境配置/升级/测试执行/...
    progress            INTEGER,                -- 0-100
    message             TEXT,
    recorded_at         TIMESTAMPTZ NOT NULL
);

-- 索引
CREATE INDEX idx_jobs_started     ON jobs(started_at);
CREATE INDEX idx_jobs_status      ON jobs(job_status);
CREATE INDEX idx_jobs_vehicle     ON jobs(vehicle_id);
CREATE INDEX idx_jobs_function    ON jobs(function_case);
CREATE INDEX idx_jobs_runner      ON jobs(runner_name);
CREATE INDEX idx_jobs_pipeline    ON jobs(pipeline_id);
CREATE INDEX idx_stages_job       ON job_stages(job_id);
CREATE INDEX idx_stages_recorded  ON job_stages(recorded_at);

-- 数据清理（保留 30 天）
-- 通过 pg_cron 或外部定时任务执行
-- DELETE FROM jobs WHERE started_at < NOW() - INTERVAL '30 days';
```

### 3.2 Prometheus 指标设计

#### 已有指标（Runner Exporter 现有）

| 指标 | 类型 | 标签 | 说明 |
|------|------|------|------|
| `gitlab_runner_state` | Gauge | runner_id, description, category | Runner 状态 |
| `gitlab_runner_online` | Gauge | runner_id, description | 是否在线 |
| `gitlab_runner_active` | Gauge | runner_id, description | 是否激活 |
| `gitlab_runner_job_info` | Gauge | runner_id, job_id, job_name, ... | 当前 Job |
| `gitlab_runner_running_job_count` | Gauge | runner_id | 运行中 Job 数 |

#### 新增指标（Job API Service 暴露）

| 指标 | 类型 | 标签 | 说明 |
|------|------|------|------|
| `hil_job_completed_total` | Counter | vehicle_id, function_case, status | 已完成 Job 总数 |
| `hil_job_duration_seconds` | Histogram | vehicle_id, function_case | Job 耗时分布 |
| `hil_job_stage_duration_seconds` | Histogram | vehicle_id, function_case, stage | 各阶段耗时 |
| `hil_job_failure_total` | Counter | vehicle_id, function_case, failure_reason | 失败分类计数 |
| `hil_job_in_progress` | Gauge | vehicle_id, function_case, runner_name | 当前进行中 Job |

---

## 四、组件详细设计

### 4.1 Job API Service（新建）

**职责**：接收 CI 脚本的 Job 阶段上报，写入 PostgreSQL，暴露 Prometheus 指标。

**接口设计**（兼容原有 API）：

```
POST /api/jobs/{job_id}/stage          # CI 脚本上报阶段进度（兼容原接口）
GET  /api/jobs/{job_id}                # 查询 Job 详情
GET  /api/jobs                         # Job 列表（分页、过滤）
GET  /metrics                          # Prometheus 指标端点
GET  /health                           # 健康检查
```

**请求体**（与原 API 兼容）：

```json
{
  "stage": "测试执行",
  "progress": 60,
  "message": "已完成 120/200 条用例",
  "job_status": "running",
  "job_name": "P03_Task_1_test",
  "runner_name": "gwm_oriny_1",
  "runner_id": 9731,
  "pipeline_id": 32737562,
  "function_case": "parking",
  "vehicle_id": "P03",
  "ref": "master",
  "web_url": "https://code.deeproute.ai/..."
}
```

**技术选型**：
- FastAPI + asyncpg（异步 PostgreSQL）
- prometheus-client（指标暴露）
- 可运行在宿主机或 Docker 容器中

### 4.2 管理 API Service（从 runner_tool 精简）

**职责**：提供 Runner 管理、Pipeline 触发、SSH 终端等操作接口。

**保留的端点**：

```
POST   /api/runners/{id}/pause         # 暂停 Runner
POST   /api/runners/{id}/resume        # 恢复 Runner
GET    /api/runners                     # Runner 列表
POST   /api/pipelines/trigger          # 触发 Pipeline
POST   /api/pipelines/{id}/cancel      # 取消 Pipeline
POST   /api/jobs/{id}/retry            # 重试 Job
WS     /api/terminal/{runner_id}       # SSH Web 终端
```

**弃用的部分**：
- Jinja2 模板渲染（由 Grafana 替代）
- Job 历史查询和图表（由 Grafana + PostgreSQL 替代）
- 自带的数据缓存层（由 PostgreSQL 替代）

### 4.3 Grafana Dashboard 规划

#### Dashboard 1: Runner 实时状态

**数据源**：Prometheus

| 面板 | 类型 | 查询 |
|------|------|------|
| Runner 状态表 | Table | `gitlab_runner_state`，显示状态/在线/是否暂停 |
| 在线率时间线 | State Timeline | `gitlab_runner_online` 按 runner 分组 |
| 当前运行 Job | Table | `gitlab_runner_job_info` |
| Runner 利用率 | Pie Chart | 各 runner 的 running_job_count 占比 |

#### Dashboard 2: Job 通过率趋势

**数据源**：Prometheus

| 面板 | 类型 | 查询 |
|------|------|------|
| 总体通过率 | Stat | `rate(hil_job_completed_total{status="success"}) / rate(hil_job_completed_total)` |
| 按车型通过率 | Time Series | 按 vehicle_id 分组 |
| 按功能域通过率 | Bar Chart | 按 function_case 分组 |
| 失败原因分布 | Pie Chart | `hil_job_failure_total` 按 failure_reason |

#### Dashboard 3: Job 历史明细

**数据源**：PostgreSQL

| 面板 | 类型 | 查询 |
|------|------|------|
| Job 列表 | Table | `SELECT * FROM jobs ORDER BY started_at DESC` |
| 按状态过滤 | Variable | `$status`, `$vehicle_id`, `$function_case` |
| Job 阶段时间线 | State Timeline | 从 job_stages 表提取各阶段起止时间 |
| 单 Job 详情 | Drill-down | 点击 Job → 查看阶段进度和日志链接 |

#### Dashboard 4: 耗时分析

**数据源**：PostgreSQL + Prometheus

| 面板 | 类型 | 说明 |
|------|------|------|
| 耗时分布直方图 | Histogram | `SELECT duration_seconds FROM jobs WHERE ...` |
| 耗时趋势（P50/P95） | Time Series | Prometheus histogram_quantile |
| 按功能域耗时对比 | Box Plot | PostgreSQL 聚合 |
| 按 Runner 耗时对比 | Bar Chart | PostgreSQL 聚合 |
| 各阶段耗时分析 | Stacked Bar | `job_stages` 表计算各阶段占比 |

#### Dashboard 5: Pipeline 概览

**数据源**：PostgreSQL

| 面板 | 类型 | 说明 |
|------|------|------|
| 活跃 Pipeline 列表 | Table | 按 pipeline_id 分组，显示进度 |
| Pipeline 成功率 | Gauge | 历史 Pipeline 成功率 |
| 每日 Pipeline 统计 | Bar Chart | 每日触发/成功/失败 Pipeline 数 |

#### 告警规则

| 告警 | 条件 | 通知渠道 |
|------|------|---------|
| Runner 离线 | `gitlab_runner_online == 0` 持续 5min | 飞书 Webhook |
| Job 通过率过低 | 最近 1h 通过率 < 80% | 飞书 Webhook |
| Job 超时 | `hil_job_in_progress` 持续 > 3h | 飞书 Webhook |
| FOTA 失败 | `hil_job_failure_total{failure_reason="fota"}` 增长 | 飞书 + 自动暂停 |

---

## 五、数据流详解

### 5.1 实时数据流（Runner 状态）

```
GitLab API ──(30s 轮询)──→ Runner Exporter ──(scrape 30s)──→ Prometheus ──→ Grafana
```

与现有一致，不做改动。

### 5.2 Job 生命周期数据流

```
CI Job 启动
  │
  ├── before_script 各阶段
  │   └── POST /api/jobs/{id}/stage {"stage":"初始化", "progress":0}
  │   └── POST /api/jobs/{id}/stage {"stage":"升级", "progress":20}
  │   └── POST /api/jobs/{id}/stage {"stage":"测试执行", "progress":60}
  │
  ├── Job 完成
  │   └── POST /api/jobs/{id}/stage {"job_status":"success/failed", "progress":100}
  │
  └── Job API Service 处理
      ├── INSERT/UPDATE jobs 表
      ├── INSERT job_stages 表
      ├── 更新 Prometheus Counter/Histogram
      └── 如果 failed → 检查是否触发告警
```

### 5.3 历史数据迁移

```
SQLite (job_stages.db)
  │
  ├── 一次性迁移脚本 (migrate_sqlite_to_pg.py)
  │   ├── 读取 SQLite jobs → INSERT PostgreSQL jobs
  │   ├── 解析 stages_json → INSERT PostgreSQL job_stages
  │   └── 校验：对比两端记录数
  │
  └── 完成后 SQLite 标记为归档
```

---

## 六、实施计划

### Phase 0：基础设施准备（0.5 天）

- [ ] docker-compose.yml 新增 PostgreSQL 服务
- [ ] 创建 init.sql（建表语句）
- [ ] 验证 PostgreSQL 容器启动和数据持久化
- [ ] Grafana provisioning 添加 PostgreSQL 数据源

### Phase 1：Job API Service（1-2 天）

- [ ] 创建 `job_api/` 目录，FastAPI 项目结构
- [ ] 实现 `POST /api/jobs/{id}/stage`（兼容原接口）
- [ ] 实现 PostgreSQL 读写（asyncpg）
- [ ] 实现 Prometheus 指标暴露（`/metrics`）
- [ ] 健康检查端点
- [ ] 单元测试

### Phase 2：数据迁移（0.5 天）

- [ ] 编写 `migrate_sqlite_to_pg.py`
- [ ] 迁移 SQLite 历史数据到 PostgreSQL
- [ ] 数据校验（记录数、状态分布、时间范围）

### Phase 3：Grafana Dashboard（1-2 天）

- [ ] Dashboard 1: Runner 实时状态
- [ ] Dashboard 2: Job 通过率趋势
- [ ] Dashboard 3: Job 历史明细
- [ ] Dashboard 4: 耗时分析
- [ ] Dashboard 5: Pipeline 概览
- [ ] 配置告警规则（Runner 离线、通过率过低）

### Phase 4：管理 API 精简（1 天）

- [ ] 从 runner_tool 提取管理端点到独立服务
- [ ] 保留：Runner 暂停/恢复、Pipeline 触发、SSH 终端
- [ ] 弃用：Web UI、Job 历史页面、图表页面
- [ ] Grafana Data Links 配置

### Phase 5：切换与验收（0.5 天）

- [ ] 修改 CI 脚本中的 API 地址（或通过环境变量切换）
- [ ] 并行运行新旧系统 1-2 天
- [ ] 验证数据一致性
- [ ] 旧系统下线

### 总工期估算：4-6 天

---

## 七、目录结构规划

```
prometheus_grafana/
├── docker-compose.yml                # 新增 postgres 服务
├── prometheus.yml                    # 不变
├── init.sql                          # PostgreSQL 建表（新增）
├── .env.example                      # 新增 POSTGRES_PASSWORD
│
├── gitlab_exporter/                  # 已有，不变
│   ├── exporter.py
│   ├── backfill.py
│   └── ...
│
├── job_api/                          # 新增：Job API Service
│   ├── app.py                        #   FastAPI 主程序
│   ├── models.py                     #   数据模型
│   ├── db.py                         #   PostgreSQL 连接和操作
│   ├── metrics.py                    #   Prometheus 指标定义
│   ├── config.py                     #   配置
│   ├── pyproject.toml                #   依赖管理
│   └── tests/                        #   测试
│
├── manage_api/                       # 新增：管理 API（从 runner_tool 精简）
│   ├── app.py                        #   Runner 管理 + Pipeline 触发
│   ├── gitlab_client.py              #   GitLab API 封装
│   ├── ssh_terminal.py               #   SSH WebSocket
│   └── ...
│
├── grafana/                          # 扩展
│   └── provisioning/
│       ├── datasources/
│       │   ├── prometheus.yml        #   已有
│       │   └── postgresql.yml        #   新增
│       └── dashboards/
│           ├── gitlab-runner.json    #   已有 Runner 状态
│           ├── job-pass-rate.json    #   新增
│           ├── job-history.json      #   新增
│           ├── job-duration.json     #   新增
│           └── pipeline-overview.json#   新增
│
├── scripts/                          # 已有 + 新增
│   ├── check_block_permissions.sh
│   ├── backup_recent_blocks.sh
│   └── migrate_sqlite_to_pg.py      #   新增：数据迁移脚本
│
└── start_exporter.sh                 # 已有
```

---

## 八、风险与缓解

| 风险 | 级别 | 缓解措施 |
|------|------|---------|
| CI 脚本切换 API 地址中断上报 | 高 | 新旧并行运行，通过环境变量控制，逐步切换 |
| PostgreSQL 容器重启数据丢失 | 高 | named volume 持久化 + 定期备份 |
| Grafana 插件不足（Button Panel 等） | 中 | 管理操作保留独立 API，Grafana 通过 Data Links 跳转 |
| 历史数据迁移丢失 | 中 | 迁移后对比两端数据量和分布 |
| SSH 终端迁移复杂度 | 中 | 保留为独立微服务，不纳入 Grafana |
| Prometheus 指标膨胀（高基数标签） | 低 | 避免用 job_id 等高基数字段做标签 |

---

## 九、与现有系统对比

| 维度 | 现状（两套系统） | 目标（统一平台） |
|------|---------------|---------------|
| 展示平台 | Grafana + 自研 Web UI | Grafana 统一 |
| 数据源 | Prometheus + SQLite | Prometheus + PostgreSQL |
| 服务数量 | Prometheus + Grafana + Exporter + runner_tool | Prometheus + Grafana + PostgreSQL + Exporter + Job API + 管理 API |
| 运维复杂度 | 两套独立部署 | Docker Compose 统一编排 |
| 数据保留 | TSDB 15天 + SQLite 7天 | TSDB 15天 + PostgreSQL 30天 |
| 告警 | 飞书（runner_tool 自有） | Grafana Alerting → 飞书 |
| 可扩展性 | 低（自研 UI 需开发） | 高（Grafana Dashboard 灵活） |

---

## 十、决策记录

### 为什么选 PostgreSQL 而不是继续用 SQLite？

1. **并发安全**：SQLite 写锁会阻塞 CI 脚本上报，PostgreSQL 支持高并发写入
2. **Grafana 原生支持**：PostgreSQL 是 Grafana 内置数据源，无需额外插件
3. **查询能力**：PostgreSQL 支持窗口函数、CTE、JSONB 等高级查询
4. **可扩展**：未来可引入 TimescaleDB 扩展，获得时序数据超能力

### 为什么不全部放 Prometheus？

1. Prometheus 不适合存储事件型数据（每个 Job 是一次性事件，不是持续指标）
2. Prometheus 标签不适合高基数字段（job_name、failure_reason 等字符串）
3. Prometheus 默认保留期短，不适合长期历史查询
4. 聚合指标（通过率、耗时分布）→ Prometheus；明细数据（单条 Job 详情）→ PostgreSQL

### 为什么保留管理 API 而不是用 Grafana 插件？

1. Grafana 社区 Button Panel 插件不够稳定，API 调用体验差
2. SSH 终端是 WebSocket 长连接，Grafana 不支持
3. Pipeline 触发需要复杂表单（变量选择），Grafana 不擅长

---

## 附录：相关文档

- [[Prometheus-Grafana 监控系统]] — 当前 prometheus_grafana 项目结构和技术栈
- [[HIL-Job优化方案]] — Pipeline Job 合并优化（数据来源之一）
- [[Pipeline 代码架构全解]] — HIL Pipeline 系统架构
