---
title: "Rahul 软件工厂蓝图 — 完整原文合集"
type: 技术笔记
created: 2026-05-27
updated: 2026-05-27
sources:
  - "https://x.com/sairahul1/status/2058832033628241931"
  - "https://hyperautomationlabs.co/software-factory-blueprint.pdf"
  - "https://www.freecodecamp.org/news/how-to-build-software-factory-with-claude-code"
  - "https://www.youtube.com/watch?v=djmbyJKlJ30"
tags:
  - Claude Code
  - Agent
  - 自动化开发
  - 软件工程
---

# 来源一：Hyperautomation Labs PDF 蓝图（全文）

### The Software Factory Blueprint
**5 Claude Code Agents That Ship Features While You Sleep**

**效果**：1 个 issue 进入 → 经过测试的 PR 出来 → 你早上审查。

| 指标 | 数值 |
|:---|:---|
| 站点数 | 5 |
| 运行时长 | 8 小时（夜间） |
| 早上审查 | 4 分钟 |
| 人工干预 | 0 |
| 吞吐量 | ∞ |

**适用人群**：独立创始人、独立黑客、小团队。

---

## 01 五站流水线架构

```
Issue Queue → Scout Agent → Builder Agent → QA Gate → Ship Agent
```

每个站点是独立的 Claude Code Agent，单一职责。Agent 之间不共享上下文，交接通过文件。

| 站 | 角色 | 触发 | 干什么 |
|:---|:---|:---|:---|
| **1. Issue Queue** | 任务队列 | 人工写入 | 结构化 issue，含验收标准、优先级标签。**唯一需要人碰的** |
| **2. Scout Agent** | 侦察兵 | 每 30 分钟 | 读 issue → grep 代码库 → git blame 查上下文 → 写 spec |
| **3. Builder Agent** | 施工队 | Scout 完成后 | 读 spec → 建 worktree → 写代码 → 最多 3 次测试-修复循环 → conventional commit |
| **4. QA Gate** | 质检 | Builder 完成后 | 全新上下文代理审查 diff → 4 项检查（验收标准/回归/密钥/注入）→ PASS/FAIL |
| **5. Ship Agent** | 发版 | QA PASS 后 | 组装 PR → 部署 staging → 早上 7 点发晨报 |

### 为什么是 5 个 Agent 而不是 1 个？

单个 Agent 超过 20 分钟就会漂移。分离 agent = 分离上下文窗口 = 分离故障模式 = 清晰的审计追踪。Builder 出问题，QA 抓住。QA 出错，你 4 分钟审查抓住。

---

## 02 Station 1：Issue Queue

模糊的 issue 产生模糊的代码。Agent 就绪的 issue 产生可合并的 PR。

### Agent 就绪 Issue 模板

```
TITLE: [P1] Add rate-limiting middleware to /api/chat

WHAT: Limit each authenticated user to 60 requests/min on the /api/chat endpoint.
Return 429 with retry-after header.

DONE WHEN:
- [ ] Middleware applied to /api/chat route only
- [ ] Rate limit: 60 req/min per user ID
- [ ] 429 response includes Retry-After header in seconds
- [ ] Unit test covers limit hit + reset
- [ ] No regressions in existing API test suite

LABELS: P1  SMALL  ready-for-factory
```

### 标签体系

| 维度 | 选项 | 含义 |
|:---|:---|:---|
| Priority | P1 / P2 / P3 | Ship today / this week / when free |
| Size | SMALL (<50行) / MEDIUM (50-200) / LARGE (200+) | |
| Gate | ready-for-factory | Scout 只取有这个标签的 issue |

### 前后对比

| | Before | After |
|:---|:---|:---|
| Issue | "Add rate limiting to the API" | 结构化标题 + 4 个 checkbox + 标签 |
| Agent 行为 | 猜测范围 → 碰 12 个文件 → 破坏 auth middleware | 限定 1 个文件 → 写 1 个测试 → 38 行 PR，90 秒合并 |

---

## 03 Station 2：Scout Agent

Scout 读 issue，写 Builder 可以直接执行的 spec。**从不写代码。**

### 4 步流程

1. **读 issue** — 解析标题、描述、验收标准、标签
2. **Grep 代码库** — 找到功能面涉及的所有文件（imports、routes、tests）
3. **Git blame** — 查每个相关文件最近 3 个 commit，获取上下文和代码风格
4. **写 spec** — 输出结构化 spec：要编辑的文件、要新增/修改的函数、测试计划

### Spec 输出模板

```
SPEC: rate-limit-middleware
ISSUE: #142

FILES:
- src/middleware/rateLimit.ts     (CREATE)
- src/routes/chat.ts              (MODIFY — add middleware)
- tests/rateLimit.test.ts         (CREATE)

APPROACH: Use sliding-window counter in Map<userId, {count, resetAt}>

TEST PLAN:
1) 60 requests pass
2) 61st returns 429
3) reset after 60s
```

### Scout 精确 Prompt

```
You are the Scout agent. Read the GitHub issue below. Grep the codebase
for every file related to the feature surface. Run git blame on each file
to understand recent changes and code style. Then write a spec to
.factory/specs/ISSUE_NUMBER.md with: files to create/modify, functions to
add, the approach in 2-3 sentences, and a test plan with 3 concrete
assertions. Do not write code. Do not open a PR. Output only the spec file.
```

### Cron 设置

Scout 每 30 分钟运行一次，监控 `ready-for-factory` 标签。

---

## 04 Station 3：Builder Agent

Builder 是**唯一写代码的 Agent**。在隔离的 worktree 中工作，永远不会损坏主分支。

### Worktree 隔离模式

```bash
git worktree add .factory/worktrees/issue-142 -b factory/issue-142
cd .factory/worktrees/issue-142
# Builder 在这里工作——main 分支保持干净
# 完成后：
git worktree remove .factory/worktrees/issue-142
```

### Builder 三大规则

| 规则 | 内容 |
|:---|:---|
| **Rule 1: Spec 进，代码出** | 读 spec 文件。严格实现 spec。不加功能。不重构邻居代码 |
| **Rule 2: 测试-修复-重试（最多 3 次）** | 每次文件修改后跑相关测试。失败就修。3 次后停止，写 .factory/failures/ISSUE.md |
| **Rule 3: Conventional Commits** | 每个 commit 遵循 `feat(scope): description` 或 `fix(scope): description`，一个逻辑变更一个 commit |

### Builder 精确 Prompt

```
You are the Builder agent. Read the spec at .factory/specs/ISSUE_NUMBER.md.
Create a worktree branch factory/issue-ISSUE_NUMBER.
Implement the spec exactly — no extra features, no unrelated refactors.
After each file change, run the relevant test suite.
If tests fail, fix and retry (max 3 attempts).
Commit with conventional commit format: feat(scope): description.
If all tests pass, mark .factory/status/ISSUE_NUMBER as "build-complete".
If 3 retries fail, write .factory/failures/ISSUE_NUMBER.md and stop.
```

---

## 05 Station 4：QA Gate

**全新上下文的独立 Agent**。它从未见过 Builder 的推理过程——这正是关键：新鲜眼光能看到 Builder 确认偏误漏掉的东西。

### QA 四项检查

| # | 检查项 | 内容 |
|:---|:---|:---|
| **1** | Acceptance Criteria | 逐条对照原始 issue 的 "done when" checkbox。每条都需要证据 |
| **2** | Regression Scan | 跑完整测试套件（不仅是新测试）。检查是否有已存在测试被破坏 |
| **3** | Secrets & Credentials | Grep：API keys、tokens、passwords、.env 值、包含凭证的硬编码 URL |
| **4** | Prompt Injection | 如果代码处理用户输入，检查传给 LLM、shell 命令、SQL 查询的未转义字符串 |

### PASS/FAIL 盖章格式

```
QA RESULT: PASS | FAIL
ISSUE: #142
CRITERIA: 4/4 met
REGRESSIONS: 0 found (148 tests pass)
SECRETS: Clean
INJECTION: N/A (no user input path)
NOTES: Rate limit resets correctly. Header format matches RFC 6585.
```

### QA Gate 精确 Prompt

```
You are the QA agent. You have not seen the Builder's work before.
Read the original issue. Read the diff on branch factory/issue-ISSUE_NUMBER.
Check: (1) every acceptance criterion is met with evidence, (2) run full
test suite and report regressions, (3) grep for secrets/credentials/API
keys, (4) check user-input paths for injection risks.
Write your report to .factory/qa/ISSUE_NUMBER.md with PASS or FAIL verdict.
If FAIL, list exactly what must change.
```

---

## 06 Station 5：Ship Agent

Ship Agent 只处理 QA-passed 的 issue。组装 PR、部署 staging、写晨报。

### PR 模板

```markdown
## [Factory] Rate-limit middleware for /api/chat (#142)

**What:** Sliding-window rate limiter, 60 req/min per user.
**Spec:** .factory/specs/142.md
**QA Report:** .factory/qa/142.md — PASS (4/4 criteria, 0 regressions)
**Tests:** 148 pass, 3 new, 0 skipped

### Changes
- src/middleware/rateLimit.ts (new, 42 lines)
- src/routes/chat.ts (+2 lines — middleware import + apply)
- tests/rateLimit.test.ts (new, 38 lines)
```

### 晨报格式

```
FACTORY OVERNIGHT REPORT — May 25, 2026
SHIPPED (ready to merge):
  PR #201 — Rate-limit middleware (#142) — QA PASS
  PR #202 — Fix avatar upload timeout (#138) — QA PASS
FAILED (needs human):
  Issue #140 — Builder failed 3x on DB migration
  → see .factory/failures/140.md
QUEUED (next run):
  Issue #143, #145 — ready-for-factory, waiting for Scout
```

### Ship Agent 精确 Prompt

```
You are the Ship agent. For each issue with status "qa-pass" in
.factory/status/: (1) Create a pull request with the title "[Factory]
ISSUE_TITLE (ISSUE_NUMBER)", body includes spec link, QA report, test count,
and file change summary. (2) Deploy the branch to staging. (3) After all PRs
are created, write a morning summary to .factory/reports/DATE.md listing
shipped PRs, failed issues, and queued issues. Format it for a 4-minute human
review.
```

---

## 07 夜间时间表

```
11:00 PM    你：给今晚的 issue 打上 ready-for-factory 标签，合上笔记本
11:30 PM    Scout Agent 取 issue → grep 代码库 → 写 spec 到 .factory/specs/
12:00 AM    Builder Agent 读 spec → 建 worktree → 写代码 → 测试-修复循环
 2:00 AM    Builder 完成。标记 build-complete
 2:30 AM    QA Gate 用新鲜上下文审查每个 build → PASS or FAIL
 4:00 AM    Ship Agent 为 passed issue 创建 PR → 部署 staging → 写晨报
 7:00 AM    你：咖啡。读晨报。合并或评论。4 分钟。
```

### Cron 配置

```bash
30 23 * * *  claude-routine scout     # 11:30 PM
0  0  * * *  claude-routine builder   # 12:00 AM
30 2  * * *  claude-routine qa        # 2:30 AM
0  4  * * *  claude-routine ship      # 4:00 AM
0  7  * * *  claude-routine summary   # 7:00 AM
```

### 早上审查流程（4 分钟）

1. **读晨报** — 30 秒
2. **点击每个 staging 链接，抽查 UI** — 2 分钟
3. **合并通过的 PR** — 1 分钟

---

## 08 参考：YouTube 视频章节

[I Built a Code Factory That Ships While I Sleep — 47 PRs Overnight](https://www.youtube.com/watch?v=djmbyJKlJ30)

```
00:00 The Receipt — 47 PRs overnight
00:33 The Problem — 1:1 ratio trap
01:20 The 5-Station Blueprint
02:38 Station 1: The Issue Queue
04:10 Station 2: The Scout Agent
05:20 Station 3: The Builder Agent
06:28 Station 4: The QA Gate
07:42 Station 5: The Ship Agent
08:43 The Overnight Run
09:55 Build Your First Factory Tonight
```

### 相关项目

- [Coppermind — I Built a Software Factory Using AI](https://www.youtube.com/watch?v=TgVXTVymr6E) — 30-40 features overnight, Claude + Gemini + ChatGPT Codex 联合审查

---

## 个人思考

待补充。