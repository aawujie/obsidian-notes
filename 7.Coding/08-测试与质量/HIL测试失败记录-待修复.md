# HIL 测试失败记录（待修复）

> 发现时间：2026-03-17
> 分支：fixed-use-high-speed-gateway
> 改动前已存在的失败，与配置重构无关

## 第 1 类：get_runnable_mask 返回全 False（8 个）

**涉及测试**：
- `test_csv_utils.py` — test_count_cases_basic, test_count_cases_all, test_get_runnable_mask_basic, test_get_runnable_mask_case_insensitive
- `test_selection.py` — test_select_excludes_unimplemented, test_select_all_valid, test_select_with_empty_tags, test_select_case_insensitive_unimplemented
- `test_case_manager.py` — test_count_cases

**根因**：`is_valid_case_row()`（来自 `auto_common.case_filter`）现在要求同时满足 5 个条件：
1. 标签非空
2. 不含 `unimplemented`
3. `"自动化输入输出"` 字段非空
4. 能解析为 JSON
5. 包含 `case_id`

但测试用的 CSV 只有 `用例ID,用例名称,自动化标签` 三列，**没有 `自动化输入输出` 列**，条件 3-5 不满足。

**修复方向**：测试 CSV 补上 `自动化输入输出` 列，填入合法 JSON（如 `{"case_id": "TC001"}`）。

## 第 2 类：smoke_test 用例数变化（2 个）

**涉及测试**：
- `test_cli_cases.py` — test_filter_smoke_test
- `test_cli_integration.py` — test_full_smoke_test_workflow

**根因**：断言 `assert 20 <= count <= 50`，但实际 CSV 里 smoke_test 标签的用例只剩 12 条。上游用例表数据变了，测试硬编码的范围过时。

**修复方向**：更新断言范围为 `10 <= count <= 50`，或改为不硬编码具体数量。

## 第 3 类：stdout vs stderr（2 个）

**涉及测试**：
- `test_runner_manager.py` — test_update_stage_without_job_id, test_update_stage_success

**根因**：`ProgressReporter` 输出改为写 stderr，但测试检查 `captured.out`，实际内容在 `captured.err`。

**修复方向**：测试改为检查 `captured.err`。
