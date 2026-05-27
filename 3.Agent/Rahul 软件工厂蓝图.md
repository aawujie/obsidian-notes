---
title: "Rahul 软件工厂蓝图 — Claude Code 自动化开发流水线"
type: 技术笔记
created: 2026-05-27
updated: 2026-05-27
sources:
  - "https://x.com/sairahul1/status/2058832033628241931"
  - "https://www.youtube.com/watch?v=djmbyJKlJ30"
  - "https://hyperautomationlabs.co/software-factory-blueprint.pdf"
tags:
  - Claude Code
  - Agent
  - 自动化开发
  - 软件工程
---

## 来源

- **作者**：Rahul（@sairahul1）
- **推文**：[How to Build a Software Factory with Claude Code That Ships Features While You Sleep](https://x.com/sairahul1/status/2058832033628241931)
- **YouTube**：[I Built a Code Factory That Ships While I Sleep — 47 Features in One Night](https://www.youtube.com/watch?v=djmbyJKlJ30)
- **免费 PDF**：[software-factory-blueprint.pdf](https://hyperautomationlabs.co/software-factory-blueprint.pdf)

## 效果

睡一觉醒来，47 个合并 PR，一行代码没写。

## 5 站流水线

```
Issue Queue → Scout Agent → Builder Agent → QA Gate → Ship Agent
```

| 站 | 角色 | 干什么 |
|:---|:---|:---|
| **1. Issue Queue** | 任务队列 | 把需求写成 agent 可消费的结构化 prompt |
| **2. Scout Agent** | 侦察兵 | 读 issue → grep 代码库 → 写实现方案 spec |
| **3. Builder Agent** | 施工队 | 拿 spec → 建 worktree → 写代码 + 跑单元测试 |
| **4. QA Gate** | 质检 | 独立 agent 审查 diff → 核对验收标准 → 打 pass/fail |
| **5. Ship Agent** | 发版 | 提 PR → 部署 staging → 发晨报总结 |

## 更精细的 7 Agent 架构（推文版本）

更深层的拆法，把 Builder 拆成后端+前端，前面加了三层分析：

**链路**：research → story → brief → build → verify → validate

| Agent | 职责 | 权限 |
|:---|:---|:---|
| **Researcher** | 先扫代码库，理解现状 | 只读 |
| **Story Writer** | 需求转用户故事 + 验收标准 | 只读 |
| **Spec Writer** | 用户故事转技术方案 | 只读 |
| **Backend Builder** | 写 API/Service/Job/单测 | 仅后端目录 |
| **Frontend Builder** | 写组件/页面/Hook/UI 测试 | 仅前端目录 |
| **Test Verifier** | 对用户故事写验收测试 | 仅测试文件 |
| **Validator** | 对比实现 vs 故事 vs 技术方案，报告缺口 | 只读 |

## 核心原则

- **每个 agent 只有干净上下文窗口**——只看自己需要的，不污染
- **错误假设在 brief 阶段就拦截**——不是写了 10 个文件后才改
- **一个工程师发一个完整垂直切片**：后端+前端+测试+验证
- **团队最优知识活在 agent 里**——不锁在人的脑子里
- **结构化链式传递**：上游输出 = 下游输入，无信息丢失

---

## 同类项目参考

- [I Built a Software Factory That Ships Features While I Sleep (Using AI)](https://www.youtube.com/watch?v=TgVXTVymr6E) — Coppermind，30-40 个 features overnight，多模型联合审查（Claude + Gemini + ChatGPT Codex）
- [The AI Coding Workflow That Ships Features While You Sleep](https://www.youtube.com/watch?v=lbRggFJWhn4) — Matt Pocock 在 AI Engineer 的 90 分钟工作坊

## 个人思考

待补充。