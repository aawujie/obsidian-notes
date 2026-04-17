# Pipeline 代码架构全解

> 本文档是 `hil_auto_test/pipeline/` 代码库的完整架构参考，供 AI 或开发者快速理解模块设计，无需逐文件分析。
> 最后更新: 2026-03-13

---

## 目录结构

```
pipeline/
├── __init__.py                    # 包根，version=2.0.0
├── ready_mr_notify.py             # 独立脚本：GitLab MR → 飞书 Webhook 通知
├── prepare_and_run.sh             # 入口 shell
├── pytest.ini                     # pytest 配置
├── requirements.txt               # Python 依赖
│
├── cli/                           # 命令行入口
│   ├── __main__.py                # python -m pipeline.cli 入口
│   ├── main.py                    # argparse 主逻辑，注册所有子命令
│   └── handlers/                  # 各子命令处理器
│       ├── artifacts.py           #   artifacts fetch
│       ├── cases.py               #   cases collect/count/filter-tag/apply-grouping/select
│       ├── feishu.py              #   feishu write-metrics
│       ├── gitlab.py              #   gitlab calculate-metrics
│       ├── info.py                #   info vehicles/functions/platform
│       ├── metrics.py             #   metrics summarize/aggregate/merge/check-pass-rate
│       ├── pipeline.py            #   pipeline generate/generate-batch
│       └── report.py              #   report send/error
│
├── config/                        # 配置文件（YAML + TXT）
│   ├── __init__.py                # 兼容旧导入路径，委托到 core.config
│   ├── runners.yaml               # 平台/车型/Runner 映射（核心配置）
│   ├── function_cases.yaml        # 功能域定义（timeout/tags/grouping 参数）
│   ├── settings.yaml              # 全局设置（重试、S3 等）
│   ├── fota.yaml                  # FOTA 升级工具配置
│   └── tags/                      # Tag 文件
│       ├── *_default.txt          # 各功能域默认 tag 列表
│       ├── tag_to_scenario.txt    # tag → scenario 文件映射
│       └── tag_to_fusa_args*.txt  # tag → FUSA 参数映射
│
├── core/                          # 核心业务逻辑
│   ├── __init__.py                # 导出核心模型
│   ├── models.py                  # 所有数据模型（dataclass）
│   ├── config/                    # 配置加载器
│   │   ├── platforms.py           # runners.yaml → PlatformConfig
│   │   ├── runners.py             # runners.yaml → Runner 配置
│   │   ├── function_cases.py      # function_cases.yaml → FunctionCaseConfig
│   │   ├── grouping.py            # function_cases.yaml → GroupingConfig
│   │   ├── settings.py            # settings.yaml → Settings
│   │   ├── fota.py                # fota.yaml → FotaConfig
│   │   └── tags.py                # tags/*.txt → tag 列表/映射
│   ├── domain/                    # 领域逻辑
│   │   ├── grouping.py            # TaskGrouper — LPT 任务分组
│   │   ├── fusa_grouping.py       # FusaTagMerger — FUSA tag 合并
│   │   ├── csv_labeler.py         # 将分组标签写入 CSV
│   │   └── grouping_report.py     # 分组评估报告生成
│   ├── services/                  # 服务编排层
│   │   ├── pipeline.py            # PipelineGenerator（组合 Single + Batch Mixin）
│   │   ├── pipeline_single.py     # 单流水线生成（grouping/FUSA/smoke）
│   │   ├── pipeline_batch.py      # 批量流水线生成（飞书配置驱动）
│   │   ├── cases.py               # CaseManager — 用例收集/过滤/计数
│   │   ├── selection.py           # CaseSelector — 选择 + 分组 + baseline
│   │   ├── metrics.py             # MetricsAggregator — 指标聚合
│   │   └── reporting.py           # ResultReporter — 报告格式化 + 飞书发送
│   └── utils/
│       └── csv.py                 # CSV 读写/合并/过滤工具函数
│
├── integrations/                  # 外部系统集成
│   ├── adas_farm/                 # ADAS Farm API
│   │   ├── client.py              # AdasFarmClient HTTP 客户端
│   │   ├── artifacts.py           # ArtifactsFetcher 制品获取
│   │   └── models.py              # 制品数据模型
│   ├── feishu/                    # 飞书集成
│   │   ├── webhook.py             # FeishuWebhook（HMAC 签名）
│   │   ├── feishu_bitable.py      # FeishuBitableService（批量配置读取）
│   │   ├── spreadsheet.py         # 飞书电子表格 API
│   │   └── write_metrics.py       # 指标写入飞书表格
│   ├── gitlab/
│   │   └── metrics.py             # GitLabMetrics — 流水线指标计算
│   └── runner_manager/
│       └── progress_reporter.py   # ProgressReporter — Runner Manager 进度上报
│
├── templates/                     # Jinja2 模板
│   ├── pipeline.yml.j2            # 单流水线 GitLab CI 模板
│   └── batch_pipeline.yml.j2      # 批量触发流水线模板
│
├── scripts/                       # Shell 脚本（CI 阶段执行）
│   ├── lib/                       # 公共库（common/platform/s3/progress）
│   ├── prepare/                   # prepare 阶段（用例收集/制品获取）
│   ├── test/                      # test 阶段（升级/健康检查/执行）
│   │   ├── upgrade/               # FOTA/Driver 升级
│   │   │   ├── fota/              # 各平台 FOTA 脚本
│   │   │   ├── lib/               # SSH/磁盘/版本工具
│   │   │   └── timesync/          # 时间同步 + CCP 配置字
│   │   └── ...                    # start_server/run_cases/deal_result 等
│   ├── report/                    # report 阶段（发送报告）
│   └── utils/                     # 通用工具脚本
│
└── tests/                         # 单元测试 + 集成测试
    ├── conftest.py                # pytest fixtures
    ├── test_task_grouper.py       # TaskGrouper 测试
    ├── test_fusa_grouping.py      # FusaTagMerger 测试
    ├── test_batch_serial_strategy.py  # 批量串行排序测试
    ├── test_pipeline_service.py   # PipelineGenerator 测试
    ├── test_case_manager.py       # CaseManager 测试
    ├── test_selection.py          # CaseSelector 测试
    ├── test_metrics_aggregator.py # MetricsAggregator 测试
    ├── test_reporting.py          # ResultReporter 测试
    ├── test_grouping_report.py    # GroupingReport 测试
    ├── test_config.py             # 配置加载测试
    ├── test_csv_utils.py          # CSV 工具测试
    ├── test_cli_*.py              # CLI 各子命令测试
    └── test_runner_manager.py     # ProgressReporter 测试
```

---

## 数据模型 (`core/models.py`)

所有核心数据结构均为 Python `dataclass`，分为以下几组：

### 分组相关

| 模型 | 用途 | 关键字段 |
|------|------|---------|
| `GroupingConfig` | 分组参数 | `avg_case_time_seconds`(5), `max_task_duration_seconds`(600), `task_init_cost_seconds`(90), `scenario_switch_cost_seconds`(3), `runner_count` |
| `ScenarioInfo` | 单个场景信息 | `name`, `count` |
| `CsvAnalysis` | CSV 分析结果 | `mode`("scenario"/"simple"), `scenarios`, `no_scenario_count`, `valid_count` |
| `TaskGroup` | 一个分组 | `label`, `scenarios: List[ScenarioInfo]`, `total_cases`, `estimated_time_seconds`, `switch_count` |

### 流水线相关

| 模型 | 用途 | 关键字段 |
|------|------|---------|
| `PipelineConfig` | 单流水线配置 | `vehicle_id`, `function_case`, `platform`, `tags`, `pipeline_mode`, `driver_url`, `fota_url`, `runner_hostname`, `job_priority`, `timeout`, `output_file` |
| `TestJob` | CI Job 定义 | `name`, `tag`, `variables: Dict` |
| `BatchTriggerJob` | 批量触发 Job | `vehicle_id`, `function_case`, `tags`, `driver_url`, `fota_url`, `needs_previous`(串行链) |
| `BatchConfig` | 批量流水线配置 | `batch_mode`, `trigger_jobs: List[BatchTriggerJob]`, `output_file` |

### 指标 / 报告

| 模型 | 用途 | 关键字段 |
|------|------|---------|
| `TestMetrics` | 原始测试指标 | `total_cases`, `selected_cases`, `executed_cases`, `passed`, `failed`, `error`, `server_start_*` |
| `ReportMetrics` | 报告指标（含格式化） | 继承 TestMetrics 字段 + `execution_rate`, `pass_rate_of_executed`, `pipeline_wall_clock_time_seconds` 等 |
| `SelectionResult` | 用例选择结果 | `total`, `runnable`, `skipped`, `tasks: List[TaskGroup]`, `tagged_csv_path`, `baseline_json_path` |
| `ReportConfig` | 报告上下文 | `vehicle_id`, `platform`, `function_case`, `pipeline_mode`, `job_url`, `pipeline_url`, 支持 `from_env()` |

---

## 核心领域逻辑 (`core/domain/`)

### TaskGrouper — LPT 任务分组

> 文件: `grouping.py` | 核心类: `TaskGrouper`

**目的**: 将测试用例分成多个 TaskGroup，使每组执行时间尽量均衡，充分利用多台 Runner 并行执行。

**两种模式**:

1. **Scenario 模式**（CSV 含 `scenario` 列）:
   - 分析 CSV 提取各 scenario 的用例数
   - `_rebalance_scenarios`: 大 scenario 按理想容量拆分为 `Name#1`, `Name#2`...
   - 按用例数降序排列
   - **LPT (Longest Processing Time)** 算法: 每次将最大 scenario 放入当前最空闲的 bin
   - 时间估算: `init_cost + cases × avg_case_time + switch_cost`

2. **Simple 模式**（无 scenario 列）:
   - 根据 `max_task_duration` 计算每个 task 可执行的最大用例数
   - 均匀分配，对齐到 `runner_count` 的整数倍

**Runner 对齐**: `num_tasks` 总是向上取整为 `runner_count` 的倍数，确保所有 Runner 都被利用。

**关键方法**:
- `analyze_csv(csv_path) → CsvAnalysis` — 自动检测 scenario/simple 模式
- `group_by_scenario(scenarios) → List[TaskGroup]` — LPT 分组
- `group_by_count(total_cases) → List[TaskGroup]` — 简单均分
- `apply_to_csv(input, output) → List[TaskGroup]` — 分析 + 分组 + 写标签

### FusaTagMerger — FUSA Tag 合并

> 文件: `fusa_grouping.py` | 核心类: `FusaTagMerger`

**目的**: 将多个 FUSA default tag 合并为更少的 Job，减少 CI Job 数量和重复的环境初始化开销。

**合并规则**:

```
Category A (有 fusa_args):
  → 相同 (feature, mode) 可合并

Category B (无 fusa_args):
  有 scenario_file → 相同 scenario 可合并
  无 scenario_file → FFD (First Fit Decreasing) 按时间预算装箱
```

**时间约束**: 合并后每组不超过 `max_job_minutes`（默认 120 分钟），超出则拆分。

**输出**: `FusaMergeResult` 包含:
- `groups: List[FusaMergedGroup]` — 每组含 `marker_expression`（pytest 用）
- `original_count`, `merged_count`, `saved_jobs`

### csv_labeler — CSV 标签写入

> 文件: `csv_labeler.py`

**目的**: 将 TaskGrouper 的分组结果写回 CSV 的 `自动化标签` 列，格式为 `TaskLabel|original_tag`。

**两种模式**:
- `apply_scenario_labels`: scenario → label 映射；拆分的 scenario 用 `CapacityAssigner` 按容量分配
- `apply_simple_labels`: 按行序依次分配 label

**CapacityAssigner**: 内部状态机，维护 `(label, capacity)` 槽位列表，每次 `next_label()` 消耗一个容量。

### GroupingReport — 分组评估报告

> 文件: `grouping_report.py`

**目的**: 生成全局分组评估报告，展示各功能域的分组效果和 FUSA 合并节省。

- **Phase 1**: hmi/parking/driving/active_safety 的 `DomainGroupResult`（job 数、每 job 用例数、时间、CV 变异系数）
- **Phase 2**: FUSA 的 `FusaMergeRow`（合并前后 tag/job 数、节省数）

---

## 服务编排层 (`core/services/`)

### PipelineGenerator — 流水线生成

> 文件: `pipeline.py` + `pipeline_single.py` + `pipeline_batch.py`

由 Mixin 组合而成: `PipelineGenerator(SinglePipelineMixin, BatchPipelineMixin)`

#### 单流水线生成流程 (`SinglePipelineMixin.generate`)

```
PipelineConfig 输入
    │
    ├─ function_case == "fusa" 且无 tags？
    │   └─ _generate_fusa_merged_jobs()
    │       FusaTagMerger.merge() → FusaMergedGroup → TestJob
    │
    ├─ supports_smart_grouping 且无 tags？
    │   └─ CaseManager.collect_cases() → 临时 CSV
    │       TaskGrouper.apply_to_csv() → 分组标签
    │       tags = 分组标签列表
    │
    ├─ pipeline_mode == "smoke_test"？
    │   └─ _filter_tags_for_smoke_test()
    │       对每个 tag 检查 check_smoke_cases_exist()
    │
    └─ 仍无 tags？
        └─ _load_default_tags() 从配置文件加载
    
    _generate_test_jobs(config, tags) → List[TestJob]
    │  每个 tag 创建一个 TestJob，附加 scenario/FUSA 变量
    │
    └─ Jinja2 渲染 pipeline.yml.j2 → GitLab CI YAML
```

#### 批量流水线生成流程 (`BatchPipelineMixin.generate_batch`)

```
batch_mode ("daily_smoke" / "daily_full")
    │
    ├─ 飞书 Bitable 读取批量配置
    │   FeishuBitableService.get_batch_configs()
    │
    ├─ 构建 BatchTriggerJob 列表（去重 vehicle_id + function_case）
    │
    ├─ _sort_and_chain_trigger_jobs():
    │   1. 按 platform 分组
    │   2. 每个 platform 内按 version (driver_url + fota_url) 分组
    │   3. 小版本组优先（如 FUSA）
    │   4. 组内按 FUNCTION_CASE_PRIORITY_ORDER 排序
    │   5. 设置 needs_previous 实现同平台串行
    │
    ├─ 对每个 job 调用 self.generate(config) 生成单流水线 YAML
    │
    └─ Jinja2 渲染 batch_pipeline.yml.j2 → 批量触发 YAML
```

**串行策略**: 同一物理平台（Runner 机器）的 Job 通过 `needs_previous` 链式依赖，避免资源竞争。不同平台的 Job 可以并行。

### CaseManager — 用例管理

> 文件: `cases.py`

| 方法 | 功能 |
|------|------|
| `collect_cases(output, smoke_test_only)` | 合并 `test_cases/{function_case}/{platform}/` 下所有 CSV |
| `filter_by_tag(input, output, tag)` | 按 tag 过滤用例 |
| `filter_valid_cases(input, output)` | 过滤可运行用例（`get_runnable_mask`） |
| `count_cases(file, tag)` | 计数 |
| `check_smoke_cases_exist(input, tag)` | 检查 tag 是否有 smoke_test 用例 |
| `add_task_label(input, output, label)` | 在标签列前加 `label|` |

**路径规则**: `test_cases/{function_case}/{platform_name}/`，其中 `bsw_uds` 映射到 `bsw`。

### CaseSelector — 用例选择 + 分组

> 文件: `selection.py`

统一入口，组合 CaseManager 和 TaskGrouper:

1. 读取 CSV → 计算 runnable/skipped
2. `TaskGrouper.apply_to_csv()` → 分组 + 打标签
3. 构建 `SelectionResult`
4. 可选输出 baseline JSON（供后续 metrics 聚合使用）

便捷函数: `select_cases()`, `select_from_counts()`

### MetricsAggregator — 指标聚合

> 文件: `metrics.py`

| 方法 | 功能 |
|------|------|
| `summarize_csv(csv_path)` | 解析测试结果 CSV，统计 passed/failed/error |
| `aggregate_from_files(baseline, status_dir, results_dir)` | 合并 baseline + status_*.json + server_startup_stats.json |
| `check_pass_rate(threshold)` | 通过率是否达标（默认 90%） |
| `merge_csv_reports(input_dir, output_dir)` | 合并多个 test_results_*.csv → merged/failed/error CSV |

### ResultReporter — 报告发送

> 文件: `reporting.py`

负责将指标格式化为人可读文本并通过飞书 Webhook 发送。

**格式化方法**:
- `format_job_report` — 单 Job 报告
- `format_pipeline_report` — 流水线总报告（final 版含自动化率、稳定性、时间统计）
- `format_error_report` — 错误报告

**通知策略**: `should_send_notification(is_final, is_error, pass_rate)`:
- final 或 error → 必发
- 中间报告 → 通过率 < 90% 才发

---

## 配置体系 (`core/config/`)

### runners.yaml 结构

```yaml
platforms:                    # 硬件平台拓扑
  gwm_oriny_share:
    orin: {ip: "192.168.x.x", username: "deeproute"}
    x86: {ip: "10.x.x.x", username: "dr", password: "xxx"}
    fota_type: "gwm_oriny"

vehicles:                     # 车型 → 平台映射
  P03:
    platform: gwm_oriny_share
    orin_passwords: ["pass1", "pass2"]
  DE09:
    platform: gwm_oriny_share
    x86_override: {ip: "10.x.x.x"}  # 可选覆盖

runner_id_mapping:            # GitLab Runner ID → 逻辑名
  "9731": {config_name: "P03-1", machine_name: "gwm_oriny_1"}

runners:                      # Runner 定义
  "9731":
    description: "P03 HIL Runner"
    vehicles: ["P03"]
    platforms: ["gwm_oriny_share"]
    ip: "10.x.x.x"
```

**数据流**: `vehicle_id → vehicles[id].platform → platforms[platform] → IP/密码`

### function_cases.yaml 结构

定义各功能域（hmi, parking, driving, fusa, active_safety, chassis, bsw_uds）的:
- `timeout`: CI Job 超时
- `tags`: 默认 tag 文件引用
- `grouping`: smart grouping 参数（`avg_case_time_seconds`, `max_task_duration_seconds`）
- `supports_smart_grouping`: 是否启用智能分组

### 配置加载器

| 加载器 | 配置来源 | 输出 |
|--------|---------|------|
| `platforms.py` | runners.yaml | `PlatformConfig`, `get_platform()`, `list_supported_vehicles()` |
| `runners.py` | runners.yaml | Runner 数量/映射, `get_runner_count()` |
| `function_cases.py` | function_cases.yaml | `FunctionCaseConfig`, `get_function_case()`, `supports_smart_grouping()` |
| `grouping.py` | function_cases.yaml | `GroupingConfig`, `get_grouping_config(function_case, vehicle_id)` |
| `tags.py` | config/tags/*.txt | `load_default_tags()`, `load_fusa_args_mappings()`, `load_scenario_mappings()` |
| `settings.py` | settings.yaml | 全局设置 |
| `fota.py` | fota.yaml | FOTA 工具配置 |

---

## 外部集成 (`integrations/`)

### ADAS Farm

| 模块 | 功能 |
|------|------|
| `client.py` | HTTP 客户端，调用 ADAS Farm API（milestone/driver/artifact 查询） |
| `artifacts.py` | `ArtifactsFetcher` — 按 milestone 或 driver UUID 获取制品 |
| `models.py` | 制品数据模型（`CurrentVehicleArtifacts` 等） |

### 飞书

| 模块 | 功能 |
|------|------|
| `webhook.py` | `FeishuWebhook` — HMAC-SHA256 签名 + 发送消息 |
| `feishu_bitable.py` | `FeishuBitableService` — 读取飞书多维表格（批量测试配置），返回 `BatchTestConfig` |
| `spreadsheet.py` | 飞书电子表格 API（读写单元格） |
| `write_metrics.py` | 将指标 JSON 写入飞书电子表格指定行列 |

### GitLab

| 模块 | 功能 |
|------|------|
| `metrics.py` | `GitLabMetrics` — 从 GitLab CI API 计算流水线指标（持续时间、成功率等） |

### Runner Manager

| 模块 | 功能 |
|------|------|
| `progress_reporter.py` | `ProgressReporter` — 通过 Runner Manager API 上报 Job 进度和状态 |

---

## Jinja2 模板

### `pipeline.yml.j2` — 单流水线模板

生成包含 3 个 stage 的 GitLab CI YAML:

```
stages: [prepare, test, report]

prepare-and-collect:   # 用例收集 + 制品获取
  ↓
test-job-1..N:         # 并行测试 Job（每个 tag 一个）
  ↓
final-report:          # 结果汇总 + 飞书通知
```

**test job (`base_test_job`)** 的 `before_script` 执行流程:
1. 初始化环境（Python/ROS/进度上报）
2. 升级逻辑（FOTA + Driver / 仅 Driver / 跳过）
3. 配置字刷写（GWM/GL 平台）
4. 时间同步检查
5. 版本信息查看
6. 启动 HIL 服务器

**Runner 调度**: 通过 `tags` 指定 `platform` + `runner_hostname`/`smoke_test`/`prod`

### `batch_pipeline.yml.j2` — 批量触发模板

生成只含 `trigger` stage 的 YAML，每个 trigger job 通过 `remote` include 从 S3 加载对应的单流水线 YAML。`needs` 字段实现同平台串行。

---

## CLI 命令体系

```bash
python -m pipeline.cli <command> <subcommand> [options]
```

| 命令 | 子命令 | 功能 |
|------|--------|------|
| `cases` | `collect` | 收集测试用例 CSV |
| | `count` | 统计用例数 |
| | `filter-tag` | 按 tag 过滤 |
| | `apply-grouping` | 应用智能分组 |
| | `select` | 选择 + 分组 + baseline |
| | `select-from-counts` | 从已知数量选择 |
| `metrics` | `summarize` | 汇总 CSV 报告 |
| | `aggregate` | 聚合指标文件 |
| | `merge` | 合并多个 CSV 报告 |
| | `check-pass-rate` | 检查通过率 |
| `report` | `send` | 发送飞书报告 |
| | `error` | 发送错误报告 |
| `pipeline` | `generate` | 生成单流水线 YAML |
| | `generate-batch` | 生成批量触发 YAML |
| `artifacts` | `fetch` | 获取 ADAS Farm 制品 |
| `feishu` | `write-metrics` | 写入飞书电子表格 |
| `gitlab` | `calculate-metrics` | 计算 GitLab 指标 |
| `info` | `vehicles` | 列出支持的车型 |
| | `functions` | 列出功能域 |
| | `platform` | 查看平台信息 |

---

## 端到端流程

### 单流水线完整流程

```
┌─────────────────────────────────────────────────────────┐
│  1. 触发 (CLI / GitLab Schedule / Web)                   │
│     python -m pipeline.cli pipeline generate             │
│     --vehicle P03 --function parking --mode daily_full   │
├─────────────────────────────────────────────────────────┤
│  2. PipelineGenerator.generate(config)                   │
│     ├─ 检测是否需要 smart grouping / FUSA merge          │
│     ├─ CaseManager 收集用例                              │
│     ├─ TaskGrouper 分组 (LPT/Simple)                     │
│     └─ Jinja2 渲染 → generated-P03-parking.yml           │
├─────────────────────────────────────────────────────────┤
│  3. GitLab CI 执行                                       │
│     ├─ prepare-and-collect: 收集用例 + 获取制品          │
│     ├─ test-job-1..N: 并行执行测试（升级→配置→运行）     │
│     └─ final-report: 聚合结果 + 飞书通知                 │
├─────────────────────────────────────────────────────────┤
│  4. 指标流                                               │
│     ├─ CaseSelector → baseline.json (total/runnable)     │
│     ├─ 每个 job → status_*.json (passed/failed/error)    │
│     ├─ MetricsAggregator.aggregate() → metrics.json      │
│     └─ ResultReporter → 飞书 Webhook 通知                │
└─────────────────────────────────────────────────────────┘
```

### 批量流水线完整流程

```
┌─────────────────────────────────────────────────────────┐
│  1. 定时触发 (GitLab Schedule)                           │
│     python -m pipeline.cli pipeline generate-batch       │
│     --mode daily_smoke                                   │
├─────────────────────────────────────────────────────────┤
│  2. BatchPipelineMixin.generate_batch()                  │
│     ├─ 飞书 Bitable 读取批量配置                         │
│     │   (车型、功能域、driver_url、fota_url、是否启用)    │
│     ├─ 构建 BatchTriggerJob 列表                         │
│     ├─ 排序 + 串行链:                                    │
│     │   同平台 → needs_previous（串行）                   │
│     │   跨平台 → 并行                                    │
│     ├─ 每个组合调用 generate() → 单流水线 YAML           │
│     │   上传到 S3                                        │
│     └─ Jinja2 渲染 batch_pipeline.yml.j2                 │
├─────────────────────────────────────────────────────────┤
│  3. GitLab CI 执行批量触发 YAML                          │
│     trigger-P03-parking ─────┐                           │
│     trigger-P03-driving ─────┤  (串行: needs_previous)   │
│     trigger-P03-fusa   ──────┘                           │
│                                                          │
│     trigger-C01-parking ─────┐  (与 P03 组并行)          │
│     trigger-C01-driving ─────┘                           │
│                                                          │
│  每个 trigger → 子流水线 (从 S3 加载 YAML)               │
└─────────────────────────────────────────────────────────┘
```

---

## 关键设计决策

### 1. LPT 调度 + Runner 对齐

TaskGrouper 使用 LPT 算法均衡任务时间，同时将任务数对齐到 Runner 数量的整数倍，确保硬件资源不浪费。大 scenario 会被拆分以避免单点瓶颈。

### 2. FUSA Tag 合并

FusaTagMerger 通过约束分组（feature/mode/scenario）将大量 FUSA tag 合并为少量 Job，显著减少 CI 资源占用和环境初始化时间。使用 FFD 装箱算法处理无约束的 tag。

### 3. Mixin 架构

PipelineGenerator 通过 `SinglePipelineMixin` 和 `BatchPipelineMixin` 组合实现单/批量两种模式，避免大类耦合，batch 可以复用 single 的 `generate()` 方法。

### 4. 配置驱动

批量测试的车型、功能域、版本等配置存储在飞书多维表格中，非工程师也可编辑，CI 触发时自动读取。

### 5. 同平台串行

同一物理 Runner 机器上的多个 Job 通过 `needs_previous` 强制串行执行，避免 FOTA 升级和域控操作的资源竞争。

---

## 代码规模统计

| 类别 | 文件数 | 约行数 |
|------|--------|--------|
| 核心模型 (models) | 1 | ~470 |
| 领域逻辑 (domain) | 4 | ~1,050 |
| 服务编排 (services) | 7 | ~1,740 |
| 配置加载 (config) | 7 | ~930 |
| CLI | 9 | ~700 |
| 外部集成 (integrations) | 8 | ~2,700 |
| 工具函数 (utils) | 1 | ~270 |
| 测试 | 19 | ~4,300 |
| **Python 总计** | **~56** | **~12,160** |
| Shell 脚本 | ~25 | ~2,000+ |
| 模板 | 2 | ~390 |
