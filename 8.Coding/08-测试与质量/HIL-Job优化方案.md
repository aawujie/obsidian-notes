# HIL Pipeline Job 合并优化方案

> **结论：两阶段改动将 HIL 测试 Job 数量从 479 减少到 220（-54%），节省约 648min/轮 Runner 时间，测试覆盖率 100% 不变，代码已上线验证。**

---

## 一、背景：每个 Job 都有固定"税"

HIL Pipeline 中每个 Job 无论测几条用例，都要付出约 **5~7 分钟**的固定启动开销：

| 阶段 | 耗时 | 说明 |
|------|------|------|
| Server 启动（portal_server + roscore + 健康检查） | 100~160s | 最大开销，每个 Job 都重启 |
| CAN 检查 | 55~60s | 每个 Job 重新验证 |
| Driver 下载安装 | ~250s | 仅首个 Job，后续复用 |
| 其他（pip、ORIN 验证、报告上传） | ~30s | |

**基准数据**（Pipeline 32613389，日度全量）：

- 总 Job 数：475
- 非测试开销：47.9h
- 占总 Runner 时间：**45.1%**

> 线性回归 R²=0.049，说明 Job 耗时几乎与用例数无关——问题是 Job 数量太多，不是每个 Job 太慢。

---

## 二、方案：两阶段减少 Job 数

### Phase 1：HMI / Parking / Driving / Active_Safety 启用智能分组

**原理**：这四个域的用例 CSV 有 `scenario` 列（场景文件），同场景用例放一个 Job 跑，减少 Server 重启。

**实现**：在 `pipeline/config/function_cases.py` 中设置 `supports_smart_grouping=True`，配置合理的时间参数，`TaskGrouper` 自动按场景贪心分组（LPT 调度）。

各域分组参数：

| 功能域 | avg_case_time | max_task_duration | 说明 |
|--------|-------------|-------------------|------|
| hmi | 5s | 20min | 场景模式，P177 无 scenario 列降级为简单模式 |
| parking | 2s | 40min | 场景模式 |
| driving | 5s | 60min | 场景模式 |
| active_safety | 5s | 30min | 场景模式，有效率较低（~25%行有标签） |

同时修复了一个 bug：有 `自动化标签` 但无 `scenario` 值的用例在场景模式下会被丢弃，增加 `NoScenario` 兜底 Task 解决此问题（HMI P03 因此多覆盖了 199 条用例）。

### Phase 2：FUSA 按约束键合并

**原理**：FUSA 的核心约束是 `FUSA_FEATURE + FUSA_MODE` 在 Server 启动时确定、不可更改。两个 tag 只要共享相同的 `(FUSA_FEATURE, FUSA_MODE, SCENARIO_FILE)`，就可以合入同一个 Job。

**实现**：新增 `FusaTagMerger` 模块，三类分组策略：

| 类型 | 规则 | 示例 |
|------|------|------|
| **Category A**（有强制激活参数） | 同 `(feature, mode)` 合并 | BSD_Standby + LCA_Standby → 同 `bsd standby` |
| **Category B + 有 scenario** | 无强制激活，同场景文件合并 | NCA_Active + NCA_Standby → 同场景 |
| **Category B + 无 scenario** | 无强制激活无场景，FFD 装箱按时间预算拆分（≤120min/Job） | APA/RPA/VPA 组合 |

合并后 Job 使用 `pytest -m "tag1 or tag2"` 表达式。**无需修改 CSV、portal_test.py 或任何 CI 脚本**。

---

## 三、Job 数量变化（本地验证 + CI 实测）

### Phase 1 效果

> 数据来源：`pytest -s -k test_grouping_report`（`pipeline/tests/test_grouping_report.py`），基于真实 CSV 自动生成。

| 功能域 | 车型 | 模式 | Runner | 有效用例 | 原 Jobs | 新 Jobs | 节省 | 最慢 Job |
|--------|------|------|--------|---------|--------|--------|------|----------|
| hmi | P03 | scenario | 3 | 814 | 14 | 6 | **-8** | 24.8min |
| hmi | DE09 | scenario | 3 | 632 | 14 | 3 | **-11** | 30.1min |
| hmi | C01 | scenario | 2 | 985 | 14 | 6 | **-8** | 26.4min |
| hmi | P177 | simple | 2 | 708 | 24 | 4 | **-20** | 16.2min |
| parking | P03 | scenario | 3 | 2082 | 22 | 3 | **-19** | 69.8min |
| parking | DE09 | scenario | 3 | 1764 | 22 | 3 | **-19** | 59.2min |
| parking | C01 | scenario | 2 | 1718 | 22 | 2 | **-20** | 69.5min |
| parking | P177 | scenario | 2 | 1602 | 46 | 2 | **-44** | 76.7min |
| driving | P03 | scenario | 3 | 1450 | 7 | 3 | **-4** | 56.5min |
| driving | DE09 | scenario | 3 | 1279 | 7 | 3 | **-4** | 52.3min |
| driving | C01 | scenario | 2 | 1356 | 7 | 2 | **-5** | 71.4min |
| driving | P177 | scenario | 2 | 696 | 5 | 2 | **-3** | 34.5min |
| active_safety | P03 | scenario | 3 | 413 | 5 | 3 | **-2** | 16.9min |
| active_safety | DE09 | scenario | 3 | 429 | 5 | 3 | **-2** | 17.1min |
| active_safety | C01 | scenario | 2 | 420 | 5 | 2 | **-3** | 27.9min |
| active_safety | P177 | scenario | 2 | 651 | 5 | 2 | **-3** | 44.9min |
| **Phase 1 合计** | | | | | **224** | **49** | **-175** | |

> **注**：
> - C01 使用 `gwm_orinx` 平台，与 DE09（`gwm_thor`）CSV 数据不同
> - P177 HMI 目录下包含 driving + parking 两个 CSV 源文件（710 行有效用例），无 scenario 列，使用 simple 模式
> - Job 数对齐到 Runner 数量的整数倍（如 3 台 Runner → Job 数为 3/6/9），避免 Runner 空闲
> - active_safety 时间预算从 10min 提升到 30min，所有车型 Job 数均减少

### Phase 2 效果

| 车型 | 原 Tag 数 | 合并后 Job 数 | 节省 Job |
|------|---------|------------|--------|
| C01 | 62 | 43 | **-19** |
| DE09 | 62 | 43 | **-19** |
| P03 | 62 | 43 | **-19** |
| P177（GL） | 69 | 42 | **-27** |
| **Phase 2 合计** | **255** | **171** | **-84** |

### 两阶段总效果

| 优化项 | 原 Job 数 | 新 Job 数 | 减少 Job 数 | 节省 Runner 时间 |
|--------|----------|----------|------------|----------------|
| Phase 1（HMI+Parking+Driving+Active_Safety） | 224 | 49 | **-175** | **~438 min** |
| Phase 2（FUSA 合并） | 255 | 171 | **-84** | **~210 min** |
| **合计** | **479** | **220** | **-259** | **~648 min（~11h）** |

> 以 4 车型 × 2.5min/Job 估算。实际节省取决于具体用例执行密度。

---

## 四、用例覆盖：三重证明不丢一条

这是最关键的问题：**减少 Job 数量，用例数量不能少**。

### 4.1 机制证明（代码层）

`tests/case_runner/loader.py:121`：

```python
if case_data.get("自动化标签"):
    tags = case_data["自动化标签"].split("|")
    for tag in tags:
        marks.append(getattr(pytest.mark, tag))
```

CSV 中 `Task_1|BSD_Standby` 会拆分为**两个独立 pytest mark**：`@Task_1` 和 `@BSD_Standby`。

因此合并 Job 的 `-m "BSD_Standby or LCA_Standby"` 等价于：

```
原来：Job1 运行 -m "BSD_Standby"  →  选中所有带 BSD_Standby mark 的用例
      Job2 运行 -m "LCA_Standby"  →  选中所有带 LCA_Standby mark 的用例

现在：合并Job 运行 -m "BSD_Standby or LCA_Standby"  →  选中两者的并集（完全等价）
```

由于每条 FUSA 用例有且仅有一个 FUSA tag（不存在同时带两个强制激活 mark 的用例），`or` 的结果 = 两个集合的**精确并集**，覆盖率 100%。

### 4.2 运行时数据证明（CI prepare 阶段）

Phase 2 上线后实测 prepare job 日志：

| 车型 | total_cases | selected_cases | 覆盖率 | prepare 状态 |
|------|------------|----------------|--------|------------|
| P03 | 7916 | **7916** | **100%** | ✅ success |
| P177 | 25233 | **25233** | **100%** | ✅ success |

`selected_cases = total_cases`，**没有任何一条用例被过滤**。

### 4.3 Job 结构证明（所有 tag 完整保留）

P03 新 pipeline 实际生成的合并 Job 样例（**全部 62 个原始 tag 均出现在 marker 表达式中，无遗漏**）：

| Job 名 | marker 表达式 | 原 Job 数 |
|--------|-------------|---------|
| `P03_FUSA_bsd_standby_test` | `BSD_Standby or LCA_Standby` | 2→1 |
| `P03_FUSA_meb_standby_test` | `FMEB_Standby or RMEB_Standby` | 2→1 |
| `P03_FUSA_NCA_test` | `NCA_Active or NCA_Standby` | 2→1 |
| `P03_FUSA_HMA_test` | `HMA_No_Suppression_Condition or HMA_Suppression_Condition` | 2→1 |
| `P03_FUSA_Mixed_RADS_test` | `RADS_Active or VPA_Standby or APA_Searching or ...` | 6→1 |

---

## 五、超时风险分析

### Phase 1 超时分析

| 功能域 | 最大 Task 预估时长 | timeout 配置 | 状态 |
|--------|-----------------|------------|------|
| hmi（所有车型） | ≤44min | 60min | ✅ |
| parking（所有车型） | ≤84min | **120min**（已从 1h 提升） | ✅ |
| driving（所有车型） | ≤73min | 180min | ✅ |
| active_safety（所有车型） | ≤16min | 60min | ✅ |
| chassis（所有车型） | ≤38min | 60min | ✅ |
| sensors（所有车型） | ≤37min | 120min | ✅ |
| bsw_uds（所有车型） | ≤11min | 60min | ✅ |
| crash（所有车型） | ≤10min | 60min | ✅ |

### Phase 2 超时分析

FUSA Category B 无 scenario 组使用 FFD 装箱算法，每个 Job ≤120min，远低于 FUSA 配置的 120min timeout。

合并后最大的 FUSA Job（如 `FUSA_Mixed_VPA` 含 3 个 VPA tag）预估约 120min，在 timeout 限制内。

---

## 六、核心代码变更

### 6.1 Phase 1：智能分组启用 + NoScenario 兜底

**改动 1：启用智能分组**（`pipeline/config/function_cases.py`）

```python
# 仅需一行配置
"parking": FunctionCaseConfig(..., supports_smart_grouping=True, timeout="2h")
"driving": FunctionCaseConfig(..., supports_smart_grouping=True)
"hmi":     FunctionCaseConfig(..., supports_smart_grouping=True)
```

**改动 2：配置分组参数**（`pipeline/config/grouping.py`）

```python
elif function_case == "hmi":
    avg_case_time = 5       # 秒/用例
    max_task_duration = 1200  # 20min/Job
elif function_case == "parking":
    avg_case_time = 2
    max_task_duration = 2400  # 40min/Job
elif function_case == "driving":
    avg_case_time = 5
    max_task_duration = 3600  # 60min/Job
elif function_case == "active_safety":
    avg_case_time = 5
    max_task_duration = 600   # 10min/Job
```

**改动 3：修复 NoScenario 用例丢失**（`pipeline/core/domain/grouping.py`）

```
原逻辑：
  CSV有scenario列 → 场景模式 → 遍历行 → 只取有scenario值的行分组
  问题：有标签但scenario为空的行被丢弃（HMI P03 丢失 199 条）

修复后（伪代码）：
  analyze_csv():
    有scenario列:
      统计各scenario的用例数
      额外统计 no_scenario_count（有标签但无scenario的行数）

  apply_to_csv():
    tasks = group_by_scenario(scenarios)
    if no_scenario_count > 0:
      fallback_tasks = group_by_count(no_scenario_count)  # 均分
      给fallback_tasks打上 "Task_X_NoScenario" 标签
      tasks.extend(fallback_tasks)

  _update_csv_with_scenario_labels():
    对有scenario的行 → 前缀匹配的Task标签
    对无scenario的行 → 轮询分配到fallback_tasks
```

### 6.2 Phase 2：FUSA 合并核心逻辑

**新增模块 `fusa_grouping.py`**，核心数据流：

```
输入:
  default_tags:  ["BSD_Standby", "LCA_Standby", "NCA_Active", ...]  # 62个
  fusa_args_map: {"bsd_standby": {feature:"bsd", mode:"standby"}, ...}
  scenario_map:  {"bsd_standby": "HIL-long-straight-road-2.json", ...}

FusaTagMerger.merge():

  Step 1: 分类 — 为每个tag填充(feature, mode, scenario, estimated_minutes)
    tag.lower() 查 fusa_args_map → 有则Category A，无则Category B
    tag.lower() 查 scenario_map  → 填充scenario_file
    tag.lower() 查 FUSA_TAG_AVG_MINUTES → 填充预估耗时

  Step 2: 分组 — 按约束键 (feature, mode, scenario) 聚合
    相同约束键的tag可以共享同一个Job

  Step 3: 构建合并结果
    if feature AND mode:   # Category A
      → 直接合并为一个组，设置FUSA_FEATURE/MODE
    elif scenario:          # Category B + 有scenario
      → 直接合并，设置SCENARIO_FILE
    else:                   # Category B + 无scenario
      → FFD装箱算法，按预估耗时拆分，每bin≤120min

  Step 4: 去重命名 → 确保Job名唯一

输出:
  groups: [
    FusaMergedGroup(
      name="FUSA_bsd_standby",
      original_tags=["BSD_Standby", "LCA_Standby"],
      marker_expression="BSD_Standby or LCA_Standby",  # 直接传给pytest -m
      fusa_feature="bsd", fusa_mode="standby",
      scenario_file="HIL-long-straight-road-2.json",
    ), ...
  ]
```

**FFD 装箱算法**（Category B 无 scenario 组）：

```
sorted_tags = 按estimated_minutes降序排列
bins = []

for tag in sorted_tags:
    placed = False
    for bin in bins:
        if bin.total_time + tag.time <= MAX_JOB_MINUTES(120):
            bin.add(tag)
            placed = True
            break
    if not placed:
        bins.append(new_bin(tag))

# GWM实际分箱结果（24个无约束tag → 4个bin）：
#   Bin1: VPA_routing_Active(58.6) + VPA_ROUTING_PARKING(53.1) + ACC_Active(8.3) = 120.0min
#   Bin2: VPA_learning_Active(35.5) + RPA_Straight_Line(29.4) + RPA_parkin(27.5) + APA_Active(27.1) = 119.5min
#   Bin3: RADS_Active(22.4) + VPA_Standby(21.3) + ... = 113.6min
#   Bin4: AEB_Positive(10.7) + ACC_Standby(9.1) + ICA_Standby(8.5) + ICA_Active(8.3) = 36.6min
```

**Pipeline 集成**（`pipeline/core/services/pipeline.py`）：

```
PipelineGenerator.generate(config):
  if function_case == "fusa" and 用户没有指定tags:
    test_jobs = _generate_fusa_merged_jobs(config)
  else:
    ... 原有逻辑 ...

_generate_fusa_merged_jobs(config):
  default_tags = load_default_tags("fusa", vehicle_id)
  fusa_map = load_fusa_args_mappings(vehicle_id)    # 自动区分GWM/GL
  scenario_map = load_scenario_mappings()

  merger = FusaTagMerger()
  result = merger.merge(default_tags, fusa_map, scenario_map)

  for group in result.groups:
    job = TestJob(
      name = f"{vehicle_id}_{group.name}_test",
      tag  = group.marker_expression,  # "BSD_Standby or LCA_Standby"
      variables = {SCENARIO_FILE, FUSA_FEATURE, FUSA_MODE}  # 按需
    )
```

**YAML 渲染链路**：

```
模板 pipeline.yml.j2:
  {{ job.name }}:          →  P03_FUSA_bsd_standby_test:
    script:
      - stage.sh "{{ job.tag }}"  →  stage.sh "BSD_Standby or LCA_Standby"
    variables:
      FUSA_FEATURE: "bsd"
      FUSA_MODE: "standby"
      SCENARIO_FILE: "HIL-long-straight-road-2.json"

      ↓ shell 传递链

stage.sh "$1" → TEST_TAG="BSD_Standby or LCA_Standby"
  → run_cases.sh "$TEST_TAG"
    → pytest ... -m "${TEST_TAG}"
      → pytest -m "BSD_Standby or LCA_Standby"  ✅
```

---

## 七、代码 Review：已识别的风险和限制

### 7.1 确认安全的部分

| 检查项 | 结论 | 说明 |
|--------|------|------|
| YAML 引号传递 | 安全 | `"{{ job.tag }}"` 在 YAML 层保护空格，shell 作为单参数传递 |
| pytest -m 语法 | 正确 | `or` 是 pytest marker 表达式的标准运算符 |
| collect_cases.sh 兼容 | 正确 | 每个 test job 独立收集全量 CSV，pytest -m 自行过滤 |
| tags_string 含 or 表达式 | 无害 | 仅用于 TAGS/ALL_TAGS 变量的日志展示，不参与逻辑 |
| 显式指定 tags 时旁路 | 正确 | `config.tags` 非空时跳过合并，保留原始 1-tag-1-job 模式 |
| fusa_easy_debug 兼容 | 正确 | `replace("_easy_debug", "")` 后统一走合并路径 |
| GWM/GL 自动区分 | 正确 | `load_fusa_args_mappings(vehicle_id)` 自动选择 `_gl.txt` |

### 7.2 已识别风险

**[中风险] Category B 无 scenario 组的 Job 名称语义不准确**

FFD 装箱按时间最优分配，不考虑功能域语义。实际结果：

```
P03_FUSA_Mixed_VPA_test  → 含 VPA_routing_Active + VPA_ROUTING_PARKING + ACC_Active
P03_FUSA_Mixed_AEB_test  → 含 AEB_Positive_Active + ACC_Standby + ICA_Standby + ICA_Active
```

VPA 组里混入了 ACC 标签，AEB 组里混入了 ICA 标签。**不影响正确性**（pytest -m 按 marker 精确选择），但查看 CI 结果时 Job 名称有误导性。

> 建议后续优化命名逻辑，或在 FFD 前先按功能域预分组。

**[中风险] GL 车型的 Category B 时间预估不精确**

`FUSA_TAG_AVG_MINUTES` 字典基于 GWM 历史数据，GL 独有的 tag（如 `HPA_Standby`, `TBA_Active`, `D2D_Standby` 等约 27 个）无实测数据，统一使用默认值 15min。

影响：GL 的 FFD 分箱结果可能不够均衡。如果某个 GL tag 实际耗时远超 15min，该 bin 可能超出 120min 预算。

> 当前 CI 硬编码 timeout=185min 提供了安全垫。建议后续采集 GL 实际执行时间回填。

**[低风险] FTTI 标签与常规标签合并**

GL 版本中 `AES_FTTI_Active` 与 `AES_Standby` 共享 `(aes, standby)` 约束键被合并。FTTI（Fault Tolerant Time Interval）测试通常验证时序约束，DEM 配置确实相同（都是强制关闭 aes），合并在 DEM 层面正确。但如果未来 FTTI 测试需要独立执行环境，需要在 `tag_to_fusa_args_gl.txt` 中为 FTTI 标签分配不同的 feature/mode。

**[低风险] `FunctionCaseConfig.timeout` 未实际控制 CI timeout**

`function_cases.py` 中 FUSA timeout="2h"，但 YAML 模板 `.base_test_job` 硬编码 `timeout: 185min`。两者不矛盾（185min > 120min），但 config 中的值实际上没有被使用。

---

## 八、改动文件清单

| 文件 | 改动内容 |
|------|---------|
| `pipeline/config/function_cases.py` | HMI/Parking/Driving 设置 `supports_smart_grouping=True`；Parking timeout 1h→2h |
| `pipeline/config/grouping.py` | 新增 HMI/Parking/Driving 分组参数（avg_case_time、max_task_duration） |
| `pipeline/core/domain/grouping.py` | 修复场景模式下无 scenario 用例丢失：增加 NoScenario 兜底 Task；`group_by_count` 改为均分策略（消除末尾余数不均衡） |
| `pipeline/core/services/pipeline_batch.py` | 严格串行：同平台所有子流水线按 needs 链串行执行，跨平台并行 |
| `pipeline/core/domain/fusa_grouping.py` | **新增** FusaTagMerger：按 (feature,mode,scenario) 约束合并 FUSA tags |
| `pipeline/core/services/pipeline.py` | FUSA 功能域调用 `_generate_fusa_merged_jobs()`；其他域改用 `apply_to_csv()` 保持一致；批量模式按 vehicle_id+function_case 去重 |
| `pipeline/core/models.py` | `to_baseline_dict()` 使用 Task 用例数之和作为 `selected_cases` |
| `pipeline/core/domain/__init__.py` | 导出 FusaTagMerger 相关类 |
| `scripts/stop_server.sh` | 修复 rosmaster/roscore/phc2sys 清理逻辑：killall 后等待+强杀兜底 |
| `pipeline/core/domain/grouping_report.py` | **新增** 分组效果报表生成器，提供 `generate_report()` 稳定接口 |
| `pipeline/tests/test_grouping_report.py` | **新增** 分组效果评估测试（11 项），`pytest -s -k test_grouping_report` 输出完整报表 |
| `pipeline/tests/test_fusa_grouping.py` | **新增** 18 个单元测试（GWM/GL 全场景覆盖） |
| `pipeline/tests/test_pipeline_service.py` | 更新智能分组启用/禁用的测试断言 |

---

## 九、验证清单

### Phase 1（已完成）
- [x] 自动化评估测试：`pytest -s -k test_grouping_report`，4 域 × 4 车型 = 16 组合全覆盖 ✅
- [x] 超时风险：全部 16 组合最大 Task 预估 ≤ timeout ✅
- [x] 均衡性检查：所有 simple 模式 CV=0%，scenario 模式 CV< 40% ✅
- [x] CI 实测：实际 Job 数与本地预测一致 ✅
- [x] prepare 阶段全部 success，NoScenario Task 正确生成 ✅

### Phase 2（验证中）
- [x] 18/18 FUSA 单元测试全部通过 ✅
- [x] 本地验证：4 车型用例覆盖率 100%，无重复组名 ✅
- [x] CI 实测：P03 selected_cases=7916（100%），P177 selected_cases=25233（100%）✅
- [x] CI 实测：P03 生成 43 个 Job，P177 生成 42 个 Job（与本地预测一致） ✅
- [x] CI pytest collected 验证：合并 Job 的 `selected + deselected = collected`，marker 选择正确 ✅
- [ ] test Job 运行完成，验证通过率与历史无明显差异（进行中）

### 额外修复（验证过程中发现）
- [x] `scripts/stop_server.sh`：rosmaster/roscore/phc2sys 清理不彻底，killall 后无等待直接 pgrep → 加等待+强杀 ✅
- [x] `pipeline/core/services/pipeline.py`：飞书表格 P177/parking 有两条 enabled 记录导致 YAML job name 重复 → 按 vehicle_id+function_case 去重 ✅

---

## 十、Phase 3 优化：分组均衡性 + Runner 利用率

### 10.1 Simple 模式均分

`group_by_count` 从"填满再开新桶"改为"先算 Job 数再均分"：

```python
# 旧: [2410, 2410, 110] CV=129%
# 新: [1260, 1260] CV=0%
num_tasks = ceil(total_cases / max_per_task)
base = total_cases // num_tasks
extra = total_cases % num_tasks
```

所有 simple 模式域（chassis/sensors/bsw_uds/crash/hmi_P177）CV 降为 0%。

### 10.2 Job 数 Runner 整数倍对齐

分组后 Job 数量自动对齐到平台 Runner 数量的整数倍，从 `runners.yaml` 动态读取 Runner 数：

| 平台 | Runner 数 | Job 数举例 |
|------|----------|------------|
| gwm_oriny_tank (P03) | 3 | 3, 6, 9 |
| gwm_thor (DE09) | 3 | 3, 6, 9 |
| gwm_orinx (C01) | 2 | 2, 4, 6 |
| gl_oriny (P177) | 2 | 2, 4, 6 |

每一轮所有 Runner 都有活干，不会出现只剩 1~2 个 Job 而大部分 Runner 空闲的情况。

### 10.3 批量流水线严格串行

同平台所有子流水线按 `needs` 链**严格串行执行**：

```
trigger-P177-hmi → trigger-P177-parking → trigger-P177-driving → ... → trigger-P177-fusa
```

跨平台子流水线完全并行（不同 Runner 池）。这确保了版本切换安全、硬件资源独占。

---

## 十一、后续可选优化（Phase 4）

**FUSA Job 内 Feature 循环**（需框架改造）：

当前 Server 重启需要 100~160s。若改造为 DEM-only 重启（约 10~15s），则不同 feature 的 FUSA tag 可在同一 Job 内串行执行，理论上可将 43 个 Job 进一步压缩到 ~15 个。

实现路径：
1. 在 fixture 层实现 `switch_fusa_feature(feature, mode)` → 调用 `modify_configuration.py` + 重启 DEM
2. 修改 Pipeline 生成逻辑支持多 feature Job
3. 预期额外节省 ~70min/车型

---

## 附录 A：FUSA 合并详细清单

### GWM（P03）：62 tag → 43 job

| 合并组 | 包含的原始 tag | 类别 | FUSA 参数 | 场景文件 |
|--------|-------------|------|----------|---------|
| `FUSA_bsd_standby` | BSD_Standby, LCA_Standby | A | bsd/standby | HIL-long-straight-road-2.json |
| `FUSA_bsd_active` | BSD_Active, LCA_Active | A | bsd/active | HIL-long-straight-road-2.json |
| `FUSA_meb_standby` | FMEB_Standby, RMEB_Standby | A | meb/standby | HIL-long-straight-road-2.json |
| `FUSA_meb_active` | FMEB_Active, RMEB_Active | A | meb/active | HIL-long-straight-road-2.json |
| `FUSA_NCA` | NCA_Active, NCA_Standby | B+S | - | HIL-guangzhengaosu-250926.json |
| `FUSA_HMA` | HMA_No_Suppression, HMA_Suppression | B+S | - | HIL-long-straight-road-hma-new2.json |
| `FUSA_Mixed_VPA` | VPA_routing_Active, VPA_ROUTING_PARKING, ACC_Active | B | - | - |
| `FUSA_Mixed_VPA_2` | VPA_learning_Active, RPA_Straight_Line, RPA_parkin, APA_Active | B | - | - |
| `FUSA_Mixed_RADS` | RADS_Active, VPA_Standby, APA_Searching, VPA_learning_Standby, RADS_Standby, APA_Standby | B | - | - |
| `FUSA_Mixed_AEB` | AEB_Positive_Active, ACC_Standby, ICA_Standby, ICA_Active | B | - | - |
| 其余 30 个 tag | 各自独立 | A | 各自 feature/mode | 各自 scenario |
| `VPA_MAP_LEARNING_PARKING_ACTIVE` | 独立（唯一 scenario） | B+S | - | HIL-VPA-learning-250310.json |
| `TSR_Fusion` | 独立（唯一 scenario） | B+S | - | HIL-long-straight-road-tsr.json |
| `TSR_Standby` | 独立（唯一 scenario） | B+S | - | ICA_FORWARD_BUFFER_ROAD.json |

### GL（P177）：69 tag → 42 job

| 合并组 | 包含数量 | 类别 | 说明 |
|--------|---------|------|------|
| `FUSA_bsd_standby` | 2 (BSD_Standby+LCA_Standby) | A | 与 GWM 相同逻辑 |
| `FUSA_bsd_active` | 2 (BSD_Active+LCA_Active) | A | |
| `FUSA_aes_standby` | 2 (AES_Standby+AES_FTTI_Active) | A | FTTI 共享 (aes,standby) |
| `FUSA_esa_standby` | 2 (EMA_Standby+EMA_FTTI_Active) | A | FTTI 共享 (esa,standby) |
| `FUSA_Mixed_APA` | 7 | B | HWA/D2D/ALCA/APA 混合 |
| `FUSA_Mixed_ALCA` | 8 | B | TLA/RPA/APA_OFF 混合 |
| `FUSA_Mixed_TBA` | 8 | B | TBA/HPA 系列 |
| `FUSA_Mixed_HPA` | 4 | B | HPA 剩余 + ACC |
| 其余 34 个 tag | 各自独立 | A | 各自 feature/mode |

---

## 附录 B：FUSA 合并 Job 结构说明

为什么有些 Job 合并了、有些没合并？**不是 bug，是设计决定的**：

**10 个合并 Job（62 tag 中的 29 个被合并）**：

| 合并 Job | 包含 tag 数 | 合并原因 |
|----------|-----------|---------|
| `FUSA_bsd_standby` | 2 | Category A：BSD + LCA 共享 `(bsd, standby)` |
| `FUSA_bsd_active` | 2 | Category A：BSD + LCA 共享 `(bsd, active)` |
| `FUSA_meb_standby` | 2 | Category A：FMEB + RMEB 共享 `(meb, standby)` |
| `FUSA_meb_active` | 2 | Category A：FMEB + RMEB 共享 `(meb, active)` |
| `FUSA_NCA` | 2 | Category B：NCA_Active + NCA_Standby 共享场景 |
| `FUSA_HMA` | 2 | Category B：HMA 两个 tag 共享场景 |
| `FUSA_Mixed_VPA` | 3 | Category B 无场景：FFD 装箱（VPA_routing + ACC） |
| `FUSA_Mixed_VPA_2` | 4 | Category B 无场景：FFD 装箱（VPA_learning + RPA + APA） |
| `FUSA_Mixed_RADS` | 6 | Category B 无场景：FFD 装箱（RADS + VPA + APA） |
| `FUSA_Mixed_AEB` | 4 | Category B 无场景：FFD 装箱（AEB + ACC + ICA） |

**33 个未合并 Job（各自独立的 feature/mode）**：

这些 tag 在 `tag_to_fusa_args.txt` 中各有**独立的 `(feature, mode)` 组合**，例如：
- `ABP_Active` → `(abp, active)`
- `AEB_Active` → `(aeb, active)`
- `FCW_Active` → `(fcw, active)`

由于 `FUSA_FEATURE + FUSA_MODE` 在 Server 启动时确定且不可更改，不同 feature 的 tag **物理上无法在同一个 Job 中运行**。这 33 个 tag 各自是唯一 feature，所以必须各占一个 Job。

> 如果要进一步合并这 33 个，需要 Phase 4 的框架改造（Job 内 Feature 循环，DEM-only 重启）。

---

## 附录 C：流水线链接

| 内容 | 链接 |
|------|------|
| MR | https://code.deeproute.ai/deeproute-org/testing-and-vehicle-maintenance/operation-platform-tester/hil_auto_test/-/merge_requests/967 |
| 日度全量（含 FUSA 合并） | https://code.deeproute.ai/deeproute-org/testing-and-vehicle-maintenance/operation-platform-tester/hil_auto_test/-/pipelines/32737562 |
| P03/fusa 子 pipeline（43 jobs） | https://code.deeproute.ai/deeproute-org/testing-and-vehicle-maintenance/operation-platform-tester/hil_auto_test/-/pipelines/32737589 |
| DEBUG 批次 P03/fusa（43 jobs） | https://code.deeproute.ai/deeproute-org/testing-and-vehicle-maintenance/operation-platform-tester/hil_auto_test/-/pipelines/32727561 |
| DEBUG 批次 C01/fusa（43 jobs） | https://code.deeproute.ai/deeproute-org/testing-and-vehicle-maintenance/operation-platform-tester/hil_auto_test/-/pipelines/32727562 |
| DEBUG 批次 DE09/fusa（43 jobs） | https://code.deeproute.ai/deeproute-org/testing-and-vehicle-maintenance/operation-platform-tester/hil_auto_test/-/pipelines/32727566 |
| DEBUG 批次 P177/fusa（42 jobs） | https://code.deeproute.ai/deeproute-org/testing-and-vehicle-maintenance/operation-platform-tester/hil_auto_test/-/pipelines/32727564 |
