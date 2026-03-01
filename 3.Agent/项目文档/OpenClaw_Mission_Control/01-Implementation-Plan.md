# OpenClaw Mission Control - 实现方案

> **创建日期**: 2026-02-21  
> **标签**: #OpenClaw #实现方案 #NextJS #Convex

---

## 📋 总览

**技术栈**: Next.js + Convex + Vercel  
**预计时间**: 9-13 天（完整版本）  
**推荐 MVP**: 3-4 天（Memory + Tasks）

---

## 一、项目初始化

### 1.1 创建 Next.js 项目

```bash
npx create-next-app@latest mission-control --typescript --tailwind --app
cd mission-control
```

### 1.2 初始化 Convex

```bash
npm install convex
npx convex dev
```

### 1.3 部署配置

```bash
# 安装 Vercel CLI
npm i -g vercel

# 部署到 Vercel
vercel --prod
```

---

## 二、数据库设计

### 2.1 Convex Schema

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  // 任务看板
  tasks: defineTable({
    title: v.string(),
    description: v.optional(v.string()),
    status: v.union(
      v.literal("todo"),
      v.literal("in_progress"),
      v.literal("done")
    ),
    assignee: v.union(
      v.literal("user"),
      v.literal("agent")
    ),
    priority: v.optional(v.union(
      v.literal("low"),
      v.literal("medium"),
      v.literal("high")
    )),
    tags: v.optional(v.array(v.string())),
    createdAt: v.number(),
    updatedAt: v.number(),
    completedAt: v.optional(v.number()),
  }),
  
  // 记忆库
  memories: defineTable({
    content: v.string(),
    category: v.string(), // daily, decision, preference, context
    date: v.string(), // YYYY-MM-DD
    tags: v.optional(v.array(v.string())),
    createdAt: v.number(),
  }).index("by_date", ["date"])
    .index("by_category", ["category"]),
  
  // 日历任务
  scheduledTasks: defineTable({
    jobId: v.string(),
    name: v.string(),
    schedule: v.string(), // cron expression
    nextRun: v.number(),
    lastRun: v.optional(v.number()),
    status: v.union(
      v.literal("active"),
      v.literal("paused"),
      v.literal("failed")
    ),
    payload: v.optional(v.string()), // JSON string
  }).index("by_nextRun", ["nextRun"]),
  
  // 团队成员（sub-agents）
  agents: defineTable({
    name: v.string(),
    role: v.string(), // developer, writer, designer, researcher
    status: v.union(
      v.literal("idle"),
      v.literal("working"),
      v.literal("busy")
    ),
    currentTask: v.optional(v.string()),
    avatar: v.optional(v.string()), // emoji or URL
    createdAt: v.number(),
  }),
  
  // 内容流水线
  contentPipeline: defineTable({
    title: v.string(),
    stage: v.union(
      v.literal("idea"),
      v.literal("script"),
      v.literal("thumbnail"),
      v.literal("filming"),
      v.literal("publish")
    ),
    content: v.optional(v.string()),
    attachments: v.optional(v.array(v.string())), // URLs
    dueDate: v.optional(v.number()),
    createdAt: v.number(),
    updatedAt: v.number(),
  }).index("by_stage", ["stage"]),
});
```

---

## 三、阶段规划

### 阶段 1：基础架构（1-2 天）

**目标**: 完成项目初始化和基础 CRUD

```
✅ Day 1:
- [ ] Next.js + Convex 项目搭建
- [ ] 部署到 Vercel + Convex Cloud
- [ ] 基础布局（Sidebar + Main Content）
- [ ] 认证（可选，用 Clerk 或 NextAuth）

✅ Day 2:
- [ ] Tasks 表的 CRUD API
- [ ] Memories 表的 CRUD API
- [ ] 基础 UI 组件库（Button, Input, Card）
```

**交付物**: 可访问的空白应用 + 数据库可读写

---

### 阶段 2：Tasks Board（2-3 天）

**目标**: 可拖拽的任务看板

```
✅ Day 3:
- [ ] 看板视图（三列：Todo / In Progress / Done）
- [ ] 任务卡片组件
- [ ] 创建任务表单

✅ Day 4:
- [ ] 拖拽功能（@dnd-kit/core）
- [ ] 状态实时更新（Convex useQuery）
- [ ] 任务详情弹窗

✅ Day 5（可选）:
- [ ] 任务筛选（按 assignee、priority）
- [ ] 任务搜索
- [ ] 完成动画
```

**关键代码**:

```typescript
// app/tasks/page.tsx
import { useQuery, useMutation } from "convex/react";
import { api } from "../../convex/_generated/api";

export default function TasksPage() {
  const tasks = useQuery(api.tasks.list);
  const updateStatus = useMutation(api.tasks.updateStatus);
  
  return (
    <div className="grid grid-cols-3 gap-4">
      {['todo', 'in_progress', 'done'].map(status => (
        <TaskColumn 
          key={status} 
          status={status}
          tasks={tasks?.filter(t => t.status === status)}
          onDrop={(taskId) => updateStatus({ id: taskId, status })}
        />
      ))}
    </div>
  );
}
```

---

### 阶段 3：Memory 记忆库（2 天）

**目标**: 可搜索的记忆文档

```
✅ Day 6:
- [ ] 记忆列表视图（按日期分组）
- [ ] 记忆详情组件（Markdown 渲染）
- [ ] 搜索框（fuse.js 前端搜索）

✅ Day 7:
- [ ] 分类筛选（daily / decision / preference）
- [ ] 标签系统
- [ ] OpenClaw 同步 Action（HTTP Webhook）
```

**OpenClaw 同步方案**:

```typescript
// convex/memories.ts
export const syncMemory = action({
  args: { 
    content: v.string(), 
    date: v.string(),
    category: v.string()
  },
  handler: async (ctx, args) => {
    await ctx.db.insert("memories", {
      content: args.content,
      category: args.category,
      date: args.date,
      createdAt: Date.now(),
    });
  },
});

// OpenClaw 调用（技能中）
async function syncToConvex(memory: string, date: string) {
  await fetch('https://your-app.convex.cloud/api/memories/syncMemory', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      content: memory,
      date: date,
      category: 'daily'
    })
  });
}
```

---

### 阶段 4：Calendar 日历（1-2 天）

**目标**: cron 任务可视化

```
✅ Day 8:
- [ ] 日历视图（@fullcalendar/react）
- [ ] 显示 cron 任务（下次执行时间）
- [ ] 任务状态标记（成功/失败）

✅ Day 9（可选）:
- [ ] 手动触发任务
- [ ] 执行历史记录
- [ ] 创建新 cron 任务表单
```

**数据同步脚本**:

```bash
#!/bin/bash
# scripts/sync-cron.sh

# 从 OpenClaw 获取 cron 列表
openclaw cron list --json > /tmp/crons.json

# 同步到 Convex
curl -X POST https://your-app.convex.cloud/api/sync-crons \
  -H "Content-Type: application/json" \
  -d @/tmp/crons.json
```

---

### 阶段 5：Team + Office（3-4 天）

**目标**: 团队状态仪表盘

```
✅ Day 10:
- [ ] Team 页面（组织结构图）
- [ ] Agent 角色配置（developer/writer/designer）
- [ ] 职责描述

✅ Day 11:
- [ ] Office 页面（工位视图）
- [ ] Agent 头像/状态展示
- [ ] CSS 动画（工作中效果）

✅ Day 12:
- [ ] 状态轮询 API（每 10 秒）
- [ ] OpenClaw 状态上报集成
- [ ] 实时任务进度显示

✅ Day 13（可选）:
- [ ] 效率统计（完成任务数、工作时长）
- [ ] 成就系统
- [ ] 团队聊天室（可选）
```

**状态轮询实现**:

```typescript
// hooks/useAgentStatus.ts
export function useAgentStatus() {
  const [agents, setAgents] = useState([]);
  
  useEffect(() => {
    const poll = async () => {
      const res = await fetch('/api/agents/status');
      const data = await res.json();
      setAgents(data);
    };
    
    poll();
    const interval = setInterval(poll, 10000); // 10 秒
    return () => clearInterval(interval);
  }, []);
  
  return agents;
}
```

---

## 四、OpenClaw 深度集成

### 4.1 需要开发的 OpenClaw 技能

```typescript
// ~/clawd/skills/mission-control/
// 功能：同步数据到 Convex

1. task-sync.ts
   - 创建任务时自动写入 Convex
   - 完成任务时更新状态

2. memory-sync.ts
   - 写入 memory/ 文件时同步到 Convex

3. cron-sync.ts
   - 定期同步 cron 状态

4. agent-status.ts
   - 上报 sub-agent 状态变化
```

### 4.2 新增 OpenClaw 命令

```bash
# 查看任务看板
/mission tasks

# 创建任务
/mission add task "整理 DRL 笔记" --assignee agent

# 查看记忆
/mission memory search "DRL"

# 查看团队状态
/mission team status

# 查看日历
/mission calendar
```

---

## 五、项目结构

```
mission-control/
├── app/
│   ├── layout.tsx
│   ├── page.tsx              # Dashboard
│   ├── tasks/
│   │   └── page.tsx          # 任务看板
│   ├── memory/
│   │   └── page.tsx          # 记忆库
│   ├── calendar/
│   │   └── page.tsx          # 日历
│   ├── team/
│   │   └── page.tsx          # 团队结构
│   └── office/
│       └── page.tsx          # 数字办公室
├── components/
│   ├── TaskBoard.tsx
│   ├── TaskCard.tsx
│   ├── MemoryList.tsx
│   ├── Calendar.tsx
│   ├── AgentCard.tsx
│   └── ui/                   # 基础组件
├── convex/
│   ├── schema.ts
│   ├── tasks.ts
│   ├── memories.ts
│   ├── scheduledTasks.ts
│   └── agents.ts
├── hooks/
│   ├── useAgentStatus.ts
│   └── useTasks.ts
└── scripts/
    └── sync-cron.sh
```

---

## 六、时间估算

| 阶段 | 内容 | 时间 | 优先级 |
|------|------|------|--------|
| 1 | 基础架构 + Schema | 1-2 天 | ⭐⭐⭐⭐⭐ |
| 2 | Tasks Board | 2-3 天 | ⭐⭐⭐⭐⭐ |
| 3 | Memory 记忆库 | 2 天 | ⭐⭐⭐⭐⭐ |
| 4 | Calendar 日历 | 1-2 天 | ⭐⭐⭐ |
| 5 | Team + Office | 3-4 天 | ⭐⭐ |
| 6 | OpenClaw 集成 | 持续 | ⭐⭐⭐⭐⭐ |
| **总计** | | **9-13 天** | |

### MVP 方案（3-4 天）

如果时间有限，先做核心功能：

```
Day 1: 基础架构 + Tasks CRUD
Day 2: Tasks Board UI + 拖拽
Day 3: Memory 列表 + 搜索
Day 4: OpenClaw 同步集成
```

---

## 七、风险与应对

| 风险 | 影响 | 应对措施 |
|------|------|----------|
| **数据同步复杂** | 高 | 先用简单 Webhook，后续优化 |
| **实时性不足** | 中 | 轮询 + 推送结合 |
| **过度工程化** | 高 | 严格 MVP 优先，验证后再扩展 |
| **维护成本高** | 中 | 用 Convex/Vercel 减少运维 |
| **OpenClaw 集成困难** | 中 | 先用独立脚本，再开发技能 |

---

## 八、下一步行动

### 立即可做

1. [ ] 创建 Next.js + Convex 项目
2. [ ] 部署到 Vercel
3. [ ] 定义 Convex Schema
4. [ ] 实现 Tasks CRUD

### 参考资源

- [Next.js 文档](https://nextjs.org/docs)
- [Convex 文档](https://docs.convex.dev)
- [@dnd-kit 文档](https://docs.dndkit.com)
- [Vercel 部署指南](https://vercel.com/docs)

---

**标签**: #OpenClaw #实现方案 #NextJS #Convex #开发计划
