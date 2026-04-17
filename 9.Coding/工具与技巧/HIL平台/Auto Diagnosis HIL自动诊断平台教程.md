# Auto Diagnosis — HIL 自动诊断平台教程

> 项目地址：`https://code.deeproute.ai/jiewu/auto_diagnosis`  
> 本地路径：`/home/dr/code/auto_diagnosis/`  
> 标签：#HIL #自动诊断 #CI/CD #飞书 #AI-Agent

---

## 1. 这是什么？

Auto Diagnosis 是一个 **HIL（Hardware-in-the-Loop）自动诊断平台**。它做三件事：

1. **收数据** — 从 Grafana/PostgreSQL 拉取 GitLab CI 失败和低执行率的 Job
2. **AI 分析** — 调用 Cursor Agent 或 OpenClaw Agent 拉取 Job 日志并分析失败根因
3. **推飞书** — 把诊断报告以 Interactive Card 或飞书文档的形式推送到群

整个流程是 **一条命令全自动**，也可以通过 **Web Dashboard** 可视化操作。

---

## 2. 架构概览

```
                ┌───────────────┐
                │   run.py      │  ← 统一入口
                └──────┬────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
  ┌──────────┐  ┌──────────┐  ┌──────────────┐
  │ Step 1   │  │ Step 2   │  │ Step 3       │
  │ 数据收集  │→│ Agent    │→│ 飞书通知      │
  │          │  │ AI 诊断   │  │              │
  └──────────┘  └──────────┘  └──────────────┘
       │              │              │
  Grafana SQL    cursor-agent    Webhook / 文档
  PostgreSQL     / openclaw      Interactive Card
```

### 目录结构

```
auto_diagnosis/
├── run.py                   # 主入口，串联三步流程
├── conf/
│   ├── config.yaml          # 全局配置（GitLab / Agent / 飞书）
│   ├── settings.py          # 配置加载（YAML → 环境变量 → CLI）
│   └── task_loader.py       # 任务配置加载与合并
├── lib/
│   ├── agent_runner.py      # Agent 统一调度（cursor / openclaw）
│   ├── backend_cursor.py    # Cursor Agent 后端
│   ├── backend_openclaw.py  # OpenClaw Agent 后端
│   ├── feishu_client.py     # 飞书 Interactive Card 发送
│   ├── feishu_doc.py        # 飞书文档创建模式
│   ├── prompt_loader.py     # 提示词 + 排除列表组装
│   ├── linkify.py           # Job ID 自动超链接
│   └── text.py              # 文本工具（截断、代码块切分）
├── steps/
│   ├── data_collect.py      # Step 1: 调用数据源脚本
│   ├── agent_run.py         # Step 2: 构建 prompt + 调用 Agent
│   └── feishu_notify.py     # Step 3: 构建卡片 + 发送
├── tasks/                   # 每个任务独立目录
│   ├── _template/           # 新任务模板
│   ├── hil_daily_failed/    # 每日失败 Job 诊断
│   ├── hil_daily_low_exec/  # 低执行率 Job 诊断
│   ├── watch_pipeline/      # Pipeline 实时监控
│   └── chat/                # 对话模式（手动输入）
├── scripts/
│   ├── dashboard.py         # Web 配置面板（HTTP Server）
│   ├── agent_cli.py         # 独立 Agent CLI
│   └── feishu_cli.py        # 独立飞书通知 CLI
└── instances.json           # 实例管理持久化
```

---

## 3. 快速开始

### 3.1 环境准备

```bash
# 依赖（很少）
pip install pyyaml requests

# 确保以下工具在 PATH 中
# cursor-agent（Cursor Agent 后端）
# openclaw（OpenClaw Agent 后端，二选一）
```

### 3.2 环境变量

```bash
# 必需
export PRIVATE_TOKEN="glpat-xxxxx"   # GitLab Personal Access Token

# 可选（也可以在 config.yaml 中配置）
export FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
export FEISHU_APP_ID="cli_xxx"       # 文档模式需要
export FEISHU_APP_SECRET="xxx"       # 文档模式需要
```

### 3.3 第一次运行

```bash
cd /home/dr/code/auto_diagnosis

# 查看所有可用任务
python3 run.py --list-tasks

# 运行每日失败诊断
python3 run.py --task hil_daily_failed

# 只看数据，不启动 AI 分析
python3 run.py --task hil_daily_failed --summary-only

# 不发飞书
python3 run.py --task hil_daily_failed --no-feishu
```

---

## 4. 预设任务详解

### 4.1 hil_daily_failed — 每日失败诊断

**用途**：汇总昨天 21:00 到现在的所有"真失败"Job（执行率为 NULL 且状态 failed），拉取日志，AI 分析根因。

**"真失败"的定义**：
```python
# 执行率无法计算（无 metrics）且状态是 failed
exec_rate IS NULL AND job_status = 'failed'
```

这意味着**低执行率**（<90%但有数据）的 Job 不包含在内，它们由另一个任务 `hil_daily_low_exec` 处理。

**常用命令**：
```bash
# 默认时间范围（昨天21:00 → 现在）
python3 run.py --task hil_daily_failed

# 自定义时间
python3 run.py --task hil_daily_failed --from now-48h --to now
python3 run.py --task hil_daily_failed --from "2026-03-25 10:00" --to "2026-03-26 10:00"

# 只看汇总
python3 run.py --task hil_daily_failed --summary-only
```

**飞书通知样式**：🔴 红色卡片（失败告警）

### 4.2 hil_daily_low_exec — 低执行率诊断

**用途**：汇总执行率 < 90% 的 Job，分析异常原因。

```bash
python3 run.py --task hil_daily_low_exec
python3 run.py --task hil_daily_low_exec --from now-48h
```

**飞书通知样式**：🟠 橙色卡片（警告）

### 4.3 watch_pipeline — Pipeline 实时监控

**用途**：轮询指定 Pipeline 的状态，发现新失败的 Job 立即触发 AI 分析并推送通知。

```bash
# 监控单个 Pipeline
python3 tasks/watch_pipeline/scripts/watch_pipeline.py --pipeline 33614805

# 监控多个
python3 tasks/watch_pipeline/scripts/watch_pipeline.py -p 12345 67890

# 自定义轮询间隔（60秒）
python3 tasks/watch_pipeline/scripts/watch_pipeline.py -p 12345 --poll-interval 60

# 只通知，不分析
python3 tasks/watch_pipeline/scripts/watch_pipeline.py -p 12345 --no-agent
```

**飞书通知样式**：🔵 蓝色卡片

### 4.4 chat — 对话模式

**用途**：手动输入内容，让 AI 分析后发送飞书通知。

```bash
# 交互式（终端输入，Ctrl+D 结束）
python3 run.py --task chat

# 管道输入
echo "分析一下这个问题..." | python3 run.py --task chat

# 不发飞书
python3 run.py --task chat --no-feishu
```

---

## 5. 配置系统

### 5.1 配置优先级

```
CLI 参数 > 环境变量 > task.yaml > config.yaml > Python 默认值
```

### 5.2 全局配置 `conf/config.yaml`

```yaml
gitlab:
  job_base: "https://code.deeproute.ai/hil/hil_auto_test/-/jobs/"

agent:
  backend: "cursor"          # cursor | openclaw
  workspace: "~/code/hil_auto_test"
  model: "auto"              # auto = 由 Agent 自动选择
  max_wait: 0                # 超时秒数，0=不限

feishu:
  webhook: "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
  template: "red"            # 卡片颜色：red / green / blue / orange
  notify_mode: "document"    # message = 群消息卡片, document = 飞书文档
  card_schema: 2             # 推荐 schema 2.0
```

### 5.3 任务级配置

每个任务在 `tasks/<name>/config/` 下维护独立配置，与全局 config.yaml **deep-merge**，任务级优先：

```
tasks/hil_daily_failed/
├── config/
│   ├── task.yaml        # 覆盖全局配置（数据源、模型、webhook 等）
│   ├── prompt.md        # AI 系统提示词
│   └── exclusions.md    # 已知可排除问题列表
└── scripts/
    └── hil_job_summary.py   # 数据收集脚本
```

### 5.4 提示词与排除列表

**prompt.md** — 控制 AI Agent 的行为：
- 输出格式要求（日志摘录 / 失败归纳 / 排查建议）
- 强制直接输出到 stdout（不写文件）
- 引用 gitlab-hil-ops Skill 拉取日志

**exclusions.md** — 已知非关键问题列表：
```markdown
- **`ujson` ModuleNotFoundError**：环境缺包，不是业务失败
- **`Initialize PTP time failed`**：PTP 未同步告警，非独立问题
- **`canceled` 状态的 Job**：不分析
```

AI 在分析时会**完全跳过**排除列表中的问题，不摘录、不提及。

---

## 6. 三步流程详解

### Step 1: 数据收集 (`steps/data_collect.py`)

调用任务配置的 `source_script`（如 `hil_job_summary.py`），该脚本：
1. 通过 Grafana SQL 查询 PostgreSQL 中的 HIL Job 数据
2. 按 Runner、功能域、阶段汇总
3. 输出格式化文本到 stdout

**核心 SQL 逻辑**：
```sql
-- "真失败"定义
WHERE exec_rate IS NULL AND job_status = 'failed'

-- "执行率"计算
(passed + failed) / executed_cases * 100
```

### Step 2: Agent 诊断 (`steps/agent_run.py`)

1. 用 `prompt_loader.py` 组装完整 prompt = 系统提示 + 排除列表 + 汇总数据
2. 调用 Agent 后端（cursor-agent CLI 或 openclaw agent CLI）
3. Agent 自动拉取 GitLab Job trace，摘录关键错误日志，生成诊断报告
4. 输出同时写到终端和日志文件

**双后端支持**：

| 后端 | CLI 命令 | 特点 |
|------|---------|------|
| cursor | `cursor-agent agent --print --trust --yolo ...` | Cursor IDE 内置，支持 MCP |
| openclaw | `openclaw agent --local -m ...` | 独立运行，不依赖 IDE |

通过 `--backend cursor` 或 `--backend openclaw` 切换。

### Step 3: 飞书通知 (`steps/feishu_notify.py`)

支持两种模式：

**消息模式** (`notify_mode: message`)：
- 读取 Agent 日志 → Job ID 自动加超链接 → 构建 Interactive Card → 发送到群

**文档模式** (`notify_mode: document`)：
- 创建飞书云文档 → 写入完整诊断报告 → 发送文档链接到群
- 优点：不受飞书卡片字数限制
- 需要配置 `FEISHU_APP_ID` / `FEISHU_APP_SECRET`

---

## 7. Web Dashboard

```bash
python3 scripts/dashboard.py --port 8080
# 浏览器打开 http://localhost:8080
```

**功能**：
- 📋 **任务浏览** — 左侧列表展示所有任务
- ⚙️ **配置编辑** — 在线编辑 task.yaml、prompt.md、exclusions.md
- 🆕 **创建任务** — 从模板创建新任务
- 📦 **实例管理** — 创建实例、配置 crontab 定时执行
- ▶️ **手动执行** — 一键运行任务，实时查看日志
- 📊 **执行历史** — 查看历史运行记录和退出码

Dashboard 运行在 `http://10.24.99.65:8888`（生产环境）。

---

## 8. 定时任务配置

### 方式一：crontab

```bash
# 每天 10:00 执行失败诊断
0 10 * * * cd /home/dr/code/auto_diagnosis && python3 run.py --task hil_daily_failed

# 每天 10:30 执行低执行率诊断
30 10 * * * cd /home/dr/code/auto_diagnosis && python3 run.py --task hil_daily_low_exec
```

### 方式二：Dashboard 实例

在 Web Dashboard 中创建实例，配置 `schedule_type` 为 `cron`，填入 cron 表达式。

---

## 9. 创建自定义任务

### 9.1 从模板创建

```bash
# 方式一：手动复制
cp -r tasks/_template tasks/my_new_task

# 方式二：通过 Dashboard 创建（点击"新建任务"按钮）
```

### 9.2 配置任务

编辑 `tasks/my_new_task/config/task.yaml`：

```yaml
name: "我的自定义任务"
description: "描述"

source:
  script: "tasks/my_new_task/scripts/my_script.py"
  args: []

agent:
  model: "auto"
  max_wait: 600

feishu:
  webhook: "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
  template: "blue"
  notify_mode: "message"
```

### 9.3 编写数据源脚本

脚本只需输出文本到 stdout，支持 `--from` / `--to` 参数：

```python
#!/usr/bin/env python3
"""自定义数据源脚本模板。"""
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from", dest="time_from", default="now-24h")
    parser.add_argument("--to", dest="time_to", default="now")
    args = parser.parse_args()
    
    # 你的数据收集逻辑
    report = collect_data(args.time_from, args.time_to)
    print(report)  # 输出到 stdout

if __name__ == "__main__":
    main()
```

### 9.4 编写提示词

编辑 `tasks/my_new_task/config/prompt.md`：

```markdown
【你的任务】
分析输入的数据，给出诊断报告。

【输出格式】
## 摘要
...
## 详细分析
...
## 建议
...
```

---

## 10. 独立工具

除了完整流程，每个模块也可单独使用：

```bash
# 单独发送飞书通知
python3 scripts/feishu_cli.py --title "测试" --body "Hello World"
python3 scripts/feishu_cli.py --title "报告" --body-file /tmp/report.md

# 单独运行 Agent 诊断
python3 scripts/agent_cli.py /tmp/hil_job_summary_last.txt

# 单独收集数据
python3 tasks/hil_daily_failed/scripts/hil_job_summary.py --from now-48h --to now
```

---

## 11. 飞书通知细节

### Card Schema 2.0

推荐使用 schema 2.0（默认），支持：
- Markdown 渲染
- 自动代码块分割（避免超过飞书单块字符限制）
- 卡片配色（header template）

### Job ID 自动超链接

报告中的 8-12 位数字会自动识别为 GitLab Job ID 并转为可点击链接：
- 数值范围：`[100000000, 999999999999]`
- 代码块内不处理
- 已经是链接的不重复处理
- 日期格式 `YYYYMMDD` 自动排除

### 飞书文档模式

当诊断报告很长（超过卡片限制）时，使用文档模式：
1. 调用飞书 API 创建云文档
2. 用 `markdown-to-feishu` 工具写入 Markdown
3. 设置文档权限（租户内可查看可编辑）
4. 发送文档链接到群

---

## 12. 常见问题

### Q: Agent 分析没有输出？
**A**: 检查 cursor-agent 或 openclaw 是否在 PATH 中。查看日志 `/var/tmp/hil_agent_output.log`。

### Q: 飞书发送失败？
**A**: 检查 webhook URL 是否正确，证书问题可设 `FEISHU_SSL_VERIFY=0`。

### Q: 怎么切换 Agent 后端？
**A**: `--backend openclaw` 或在 config.yaml 中设置 `agent.backend: openclaw`。

### Q: 时间范围怎么指定？
**A**: 支持以下格式：
```bash
--from now-48h            # 相对时间
--from "2026-03-25 10:00" # 绝对时间（自动追加 +08:00）
--from 2026-03-25T10:00:00+08:00  # 完整 ISO 格式
```

### Q: 怎么调整 AI 模型？
**A**: `--model sonnet-4` 或在 task.yaml 中设置。`auto` 表示由 Agent 自动选择。

### Q: 怎么看上次运行结果？
**A**: 
- 汇总数据：`/tmp/hil_job_summary_last.txt`
- Agent 输出：`/var/tmp/hil_agent_output.log`
- Dashboard 执行历史

---

## 13. 关键设计决策

| 决策 | 原因 |
|------|------|
| 三步分离（收集/分析/通知） | 每步可独立运行和调试 |
| 任务级配置 deep-merge | 不同任务可独立定制，同时继承全局默认 |
| 双 Agent 后端 | Cursor 适合有 IDE 环境，OpenClaw 适合无头服务器 |
| 飞书文档模式 | 解决卡片字数限制，长报告更友好 |
| Job ID 自动超链接 | 报告中的 Job ID 直接可点击跳转 GitLab |
| 排除列表机制 | 过滤已知非关键问题，减少噪声 |
| prompt 控制输出到 stdout | 确保下游能正确捕获 Agent 输出 |

---

*文档生成时间：2026-03-31*
