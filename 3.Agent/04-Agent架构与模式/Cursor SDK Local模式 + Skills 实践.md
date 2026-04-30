# Cursor SDK Local 模式 + 调用本地 Skills

> 目标：在无桌面环境的服务器（GitLab Runner / CI / VPS）上用 Cursor SDK local 模式执行任务，自动加载本地 skill 文件。

---

## 最小环境

```bash
node >= 22
CURSOR_API_KEY="crsr_..."
```

`package.json` 只需要一个依赖：

```json
{
  "type": "module",
  "dependencies": {
    "@cursor/sdk": "^1.0.7"
  },
  "devDependencies": {
    "tsx": "^4.21.0"
  }
}
```

**不需要 Cursor IDE，不需要桌面环境，不需要额外二进制。**

---

## 基础用法：local 模式执行任务

```typescript
import { Agent } from "@cursor/sdk";

const agent = await Agent.create({
  apiKey: process.env.CURSOR_API_KEY,
  model: { id: "gpt-5.4-nano" },  // 可选 models: default, gpt-5.4, claude-opus-4-6, ...
  local: { cwd: "/path/to/workspace" },
});

const run = await agent.send("分析这个项目的认证模块，找出安全漏洞");

for await (const event of run.stream()) {
  // 处理事件: assistant_delta / tool_call / thinking / status
}

const result = await run.wait();
agent.close();
```

---

## 核心：自动加载本地 Skills

Cloud 模式看不到本地 `.cursor/skills/`，local 模式虽然 Agent 能扫项目文件，但**不会自动识别 skill 文件**。需要手动把 skill 内容注入 prompt。

### 方案：SkillLoader 工具

在 workspace 根目录放一个 `skill_loader.ts`，它会扫描 `.cursor/skills/` 并注入到 prompt：

```typescript
// skill_loader.ts
import { readdirSync, readFileSync, existsSync } from "node:fs";
import { join, basename } from "node:path";
import type { Agent } from "@cursor/sdk";

export type Skill = {
  name: string;
  path: string;
  content: string;
};

/**
 * 扫描 .cursor/skills/ 目录，读取所有 SKILL.md 文件
 */
export function loadSkills(cwd: string): Skill[] {
  const skillsDir = join(cwd, ".cursor", "skills");
  if (!existsSync(skillsDir)) return [];

  const skills: Skill[] = [];
  const entries = readdirSync(skillsDir, { withFileTypes: true });
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    const skillFile = join(skillsDir, entry.name, "SKILL.md");
    if (existsSync(skillFile)) {
      skills.push({
        name: entry.name,
        path: skillFile,
        content: readFileSync(skillFile, "utf8"),
      });
    }
  }
  return skills;
}

/**
 * 用 skill 列表构造 system prompt 附加内容
 */
export function buildSkillPrompt(skills: Skill[]): string {
  if (skills.length === 0) return "";
  return [
    "---",
    "## Available Skills",
    "The following skills are defined in .cursor/skills/. When a user task matches a skill's description, follow the skill's instructions.",
    "",
    ...skills.map(s =>
      `### Skill: ${s.name}\n\n${s.content}`
    ),
    "---",
  ].join("\n");
}

/**
 * 构造最终 prompt: skill 指令 + 用户任务
 */
export function buildPrompt(
  cwd: string,
  userTask: string,
  options?: {
    /** 只要指定 skill 名（逗号分隔），如 "security-review,cpp-review" */
    only?: string;
  }
): string {
  let allSkills = loadSkills(cwd);

  if (options?.only) {
    const names = new Set(options.only.split(",").map(s => s.trim()));
    allSkills = allSkills.filter(s => names.has(s.name));
  }

  const skillBlock = buildSkillPrompt(allSkills);
  return [skillBlock, "", "## User Task", userTask].filter(Boolean).join("\n");
}
```

### 使用示例

```typescript
// run_with_skills.ts
import { Agent } from "@cursor/sdk";
import { buildPrompt } from "./skill_loader.js";

const CWD = process.env.WORKSPACE ?? process.cwd();

const prompt = buildPrompt(CWD, process.argv[2] ?? "Summarize this project", {
  // only: "security-review",  // 可选：只用特定 skill
});

console.log(`Loaded ${prompt.match(/### Skill:/g)?.length ?? 0} skills`);

const agent = await Agent.create({
  apiKey: process.env.CURSOR_API_KEY,
  model: { id: "gpt-5.4" },
  local: { cwd: CWD },
});

const run = await agent.send(prompt);

for await (const event of run.stream()) {
  if (event.type === "assistant") {
    for (const block of event.message.content) {
      if (block.type === "text") process.stdout.write(block.text);
    }
  } else if (event.type === "tool_call") {
    console.log(`[${event.status}] ${event.name}`);
  }
}

const result = await run.wait();
console.log(`\nDone: ${result.status}`);
await agent.close();
```

```bash
# 终端执行
export CURSOR_API_KEY="crsr_..."
npx tsx run_with_skills.ts "分析这个项目的安全漏洞"
```

---

## 进阶：带 skill 结果的 CI 集成

```typescript
// ci_agent.ts — GitLab Runner / GitHub Actions 通用
import { Agent } from "@cursor/sdk";
import { buildPrompt } from "./skill_loader.js";
import { writeFileSync } from "node:fs";

async function runCI() {
  const task = process.env.AGENT_TASK ?? "Review recent changes for issues";
  const model = process.env.AGENT_MODEL ?? "gpt-5.4-nano";
  const cwd = process.env.CI_PROJECT_DIR ?? process.cwd();

  const prompt = buildPrompt(cwd, task);

  const agent = await Agent.create({
    apiKey: process.env.CURSOR_API_KEY,
    model: { id: model },
    local: { cwd },
  });

  const run = await agent.send(prompt);
  let output = "";

  for await (const event of run.stream()) {
    if (event.type === "assistant") {
      for (const block of event.message.content) {
        if (block.type === "text") output += block.text;
      }
    } else if (event.type === "thinking") {
      process.stderr.write(`[thinking] ${event.text.slice(0, 100)}...\n`);
    } else if (event.type === "tool_call") {
      process.stderr.write(`[${event.status}] ${event.name}\n`);
    }
  }

  const result = await run.wait();
  await agent.close();

  // 写入 CI artifacts
  writeFileSync("agent-output.md", output);
  console.log(output);

  if (result.status !== "finished") process.exit(1);
}

runCI().catch(e => { console.error(e); process.exit(1); });
```

### GitLab CI 配置

```yaml
# .gitlab-ci.yml
agent-review:
  image: node:22
  stage: review
  variables:
    AGENT_TASK: "Review MR changes for bugs, security issues, and code quality. Report in markdown."
    AGENT_MODEL: "gpt-5.4"
  script:
    - pnpm install
    - npx tsx ci_agent.ts
  artifacts:
    paths:
      - agent-output.md
    expire_in: 7 days
```

---

## 关键区别

| | Local 模式 | Cloud 模式 |
|---|---|---|
| 运行位置 | 本机 (Runner/服务器) | Cursor 云端 |
| 文件访问 | 本地文件系统 (cwd) | Git repo (克隆后) |
| Skills 支持 | 手动注入 prompt | 手动注入 prompt |
| 额外依赖 | **无** (node + npm 足够) | 无 |
| 适用场景 | CI/本地开发/私密项目 | PR/批量/公开 repo |

**两种模式都需要手动把 skill 内容注入 prompt**——SDK 没有原生的 skill 发现机制。

---

## 相关笔记

- [[Cursor Cookbook 项目拆解]] — cookbook 4 个示例详细拆解
- [[CLI-Anything 让软件 Agent 化]] — Agent 嵌入工具的通用思路
