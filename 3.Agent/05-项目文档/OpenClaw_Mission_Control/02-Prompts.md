# OpenClaw Mission Control - 可执行指令

> **创建日期**: 2026-02-21（基于原笔记整理）  
> **标签**: #OpenClaw #Prompts #可执行指令

---

## 📋 使用说明

**直接复制**下方的英文指令发送给 OpenClaw，它会自动开始构建对应的模块。

**建议顺序**: Tasks Board → Memory → Calendar → Team → Office → Content Pipeline

---

## 1. Tasks Board｜任务看板

**用途**: 让你和 OpenClaw 的工作都透明化——谁在做什么、做到哪一步、卡在哪里一眼看清；它也能看见你在忙什么，从而主动接走任务并更新状态。

**核心功能**:
- 任务状态追踪（Todo / In Progress / Done）
- 任务分配（User vs Agent）
- 实时更新

**指令（直接复制给 OpenClaw）**:

```
Please build a task board for us that tracks all the tasks we are working on. I should be able to see the status of every task and who the task is assigned to, me or you. Moving forward please put all tasks you work on into this board and update it in real time. Build it as a Next.js app with a Convex database.
```

**补充说明（可选）**:

```
Additional requirements:
- Drag and drop to change task status
- Filter by assignee (me/agent)
- Show task creation date and completion date
- Add priority levels (low/medium/high)
```

---

## 2. Content Pipeline｜内容流水线

**用途**: 把内容创作拆成流水线：**Idea → Script → Thumbnail → Filming → Publish**。你丢灵感，它每天固定时间写脚本、生成缩略图、把卡片推进到下一列，减少「重复启动」的成本。

**核心功能**:
- 内容创作阶段管理
- 支持富文本（脚本）+ 图片附件
- 自动化推进（定时任务）

**指令**:

```
Please build me a content pipeline tool. I want it to have every stage of content creation in it. I should be able to edit ideas and put full scripts in it and attach images if need be. I want you to manage this pipeline with me and add wherever you can. Build it as a Next.js app with a Convex database.
```

**阶段建议**:

```
Stages should include:
1. Idea（灵感）
2. Script（脚本）
3. Thumbnail（缩略图）
4. Filming（拍摄/制作）
5. Publish（发布）
```

---

## 3. Calendar｜日历

**用途**: 很多人觉得 Claw 不够主动，实际问题常常是「没有可见的排程」。日历就是你对它的 **cron jobs / scheduled tasks** 的审计面板：有没有排进来、什么时候跑、是否执行成功。

**核心功能**:
- cron 任务可视化
- 下次执行时间显示
- 执行历史追踪

**指令**:

```
Please build a calendar for us in the mission control. All your scheduled tasks and cron jobs should live here. Anytime I have you schedule a task, put it in the calendar so I can ensure you are doing them correctly. Build it as a Next.js app with a Convex database.
```

**补充说明（可选）**:

```
Features needed:
- Show next run time for each cron job
- Display execution history (success/failed)
- Allow manual trigger
- Show task payload/details
```

---

## 4. Memory｜记忆库

**用途**: 把它产生的每一条 memory 变成 UI 里的**文档集合**，并做**全局搜索**。你不再靠「想起来去翻文件」，而是像查资料一样检索过去的决定、偏好、策略、上下文。

**核心功能**:
- 记忆文档列表
- 全文搜索
- 分类/标签

**指令**:

```
Please build a memory screen in our mission control. It should list all your memories in beautiful documents. We should also have a search component so I can quickly search through all our memories. Build it as a Next.js app with a Convex database.
```

**补充说明（可选）**:

```
Requirements:
- Sync with existing memory/ files
- Categorize memories (daily, decision, preference, context)
- Tag support
- Full-text search
- Show memory date and category
```

---

## 5. Team｜团队结构

**用途**: 你会反复用到开发 / 写作 / 设计 / 研究等不同能力。Team 页面把这些常用 **sub-agents** 固化成组织结构：角色、职责、正在做的事、对应的记忆与工具，方便管理，也让「该叫谁出来做事」更确定。

**核心功能**:
- sub-agents 列表
- 角色与职责
- 当前任务状态

**指令**:

```
Please build me a team structure screen. It should show you, plus all the subagents you regularly spin up to do work. If you haven't thought about which sub agents you spin up, please create them and organize them by roles and responsibilities. This should be developers, writers, and designers as examples. Build it as a Next.js app with a Convex database.
```

**角色建议**:

```
Suggested roles:
- Developer（开发）- 写代码、调试、部署
- Writer（写作）- 写脚本、文章、笔记
- Designer（设计）- 做图、视觉、排版
- Researcher（研究）- 查资料、整理信息
- Analyst（分析）- 数据分析、报告
```

---

## 6. Office｜数字办公室

**用途**: 偏氛围，但能提升运营感。实时状态总览 + 组织效率仪表板：用头像/工位展示每个 agent 的当前状态与任务进度；谁空闲、谁卡住、谁在跑流程，一眼可见。

**核心功能**:
- Agent 实时状态
- 工位/头像可视化
- 任务进度显示

**指令**:

```
Please build me a digital office screen where I can view each agent working. They should be represented by individual avatars and have their own work areas and computers. When they are working they should be at their computer. I should be able to quickly view the status of every team member. Build it as a Next.js app with a Convex database.
```

**补充说明（可选）**:

```
Features:
- Avatar for each agent (emoji or image)
- Status indicator (idle/working/busy)
- Current task display
- Animation when working (typing effect, progress bar)
- Last active time
```

---

## 🚀 完整 Mission Control 指令

如果想一次性让 OpenClaw 规划整个系统：

```
I want to build a Mission Control system for us. It's a dashboard where I can see and manage all your work, memories, scheduled tasks, and sub-agents.

The tech stack is: Next.js + Convex database, deployed on Vercel.

Please help me build these modules one by one:
1. Tasks Board - track all tasks and their status
2. Memory Library - searchable memory documents
3. Calendar - show all cron jobs and scheduled tasks
4. Team Structure - organize sub-agents by roles
5. Digital Office - real-time agent status dashboard
6. Content Pipeline - content creation workflow

Start with the Tasks Board first. Build it as a Next.js app with Convex backend, and deploy it on Vercel. Make sure it has drag-and-drop functionality and real-time updates.
```

---

## 📝 实施建议

### 优先级

1. **优先做**: Tasks Board + Memory → 立刻感觉从「对话助手」变成「可运营的系统」
2. **其次**: Calendar → 建立信任，看到它有没有按时做事
3. **再次**: Team → 固化常用 sub-agents
4. **最后**: Office + Content Pipeline → 氛围和进阶功能

### 开发模式

**方式 1: 完全由 OpenClaw 生成**
- 优点：快速、无需手写代码
- 缺点：定制化受限

**方式 2: 手动搭建框架 + OpenClaw 填充**
- 优点：可控性强、架构清晰
- 缺点：需要前端基础

**推荐**: 先用方式 1 快速出 MVP，再用方式 2 重构优化

---

## 🔗 相关文档

- [00-Overview.md](./00-Overview.md) - 深度分析：目的、思路、设计哲学
- [01-Implementation-Plan.md](./01-Implementation-Plan.md) - 实现方案：技术栈、阶段规划、时间估算

---

**标签**: #OpenClaw #Prompts #MissionControl #可执行指令
