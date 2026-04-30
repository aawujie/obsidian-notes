# Cursor SDK Pipeline 方案：GitLab Runner 空白环境部署

> 场景：公共 Runner，每次 Pipeline 从零构建。拉 skill 仓库 → 拉目标项目 → SDK 执行 → 输出结果。
> SDK 版本：`@cursor/sdk` v1.0.7（2026-04）

---

## 一、整体流程

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────┐
│ 装 Node +    │ ──▶ │ clone skill  │ ──▶ │ clone 目标   │ ──▶ │ SDK      │
│ @cursor/sdk  │     │ 仓库到本地   │     │ 项目到本地   │     │ 执行任务 │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────┘
```

每阶段都是干净的，不依赖 Runner 上预装任何东西。

---

## 二、Runner 上的目录结构

```
/runner/
├── skills/                   # ← 从 skill 仓库 clone
│   └── .cursor/skills/
│       ├── security-review/
│       │   └── SKILL.md
│       ├── cpp-review/
│       │   └── SKILL.md
│       └── ...
├── workspace/                # ← 目标项目（要 review 的代码）
│   └── src/...
├── package.json              # ← 放 runner 根目录，只装 SDK
├── pnpm-lock.yaml
└── run.ts                    # ← 入口脚本
```

---

## 三、代码

### package.json

```json
{
  "name": "cursor-pipeline",
  "private": true,
  "type": "module",
  "dependencies": {
    "@cursor/sdk": "^1.0.7"
  },
  "devDependencies": {
    "tsx": "^4.21.0"
  }
}
```

### run.ts — 入口脚本

```typescript
import { Agent } from "@cursor/sdk";
import { readdirSync, readFileSync, existsSync } from "node:fs";
import { join, resolve } from "node:path";

// ============================================
// 配置 - 从环境变量读取
// ============================================
const API_KEY = process.env.CURSOR_API_KEY!;
const SKILLS_DIR = resolve(process.env.SKILLS_DIR ?? "./skills");
const WORKSPACE = resolve(process.env.WORKSPACE_DIR ?? "./workspace");
const TASK = process.env.AGENT_TASK ?? "Summarize this project";
const MODEL = process.env.AGENT_MODEL ?? "gpt-5.4-nano";
const SKILL_FILTER = process.env.AGENT_SKILLS?.trim(); // 逗号分隔，可选

// ============================================
// 扫描 skill 目录
// ============================================
function scanSkills(root: string): { name: string; content: string }[] {
  const skillsDir = join(root, ".cursor", "skills");
  if (!existsSync(skillsDir)) return [];

  const skills: { name: string; content: string }[] = [];
  for (const entry of readdirSync(skillsDir, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const f = join(skillsDir, entry.name, "SKILL.md");
    if (existsSync(f)) {
      skills.push({ name: entry.name, content: readFileSync(f, "utf8") });
    }
  }
  return skills;
}

// ============================================
// 构造 prompt = skills 指令 + 用户任务
// ============================================
function buildPrompt(skills: { name: string; content: string }[], task: string) {
  const skillBlock = skills.length === 0
    ? ""
    : [
        "You have access to the following specialized skills.",
        "When relevant, follow the skill's methodology and output format.",
        "",
        ...skills.flatMap(s => [
          `### Skill: ${s.name}`,
          s.content,
          "",
        ]),
        "---",
        "",
      ].join("\n");

  return skillBlock + "## Task\n\n" + task;
}

// ============================================
// 主流程
// ============================================
async function main() {
  // 1. 加载 skill
  let skills = scanSkills(SKILLS_DIR);
  console.log(`[setup] skills dir: ${SKILLS_DIR}`);
  console.log(`[setup] loaded ${skills.length} skills: ${skills.map(s => s.name).join(", ") || "(none)"}`);

  if (SKILL_FILTER) {
    const names = new Set(SKILL_FILTER.split(",").map(s => s.trim()));
    skills = skills.filter(s => names.has(s.name));
    console.log(`[setup] filtered to: ${skills.map(s => s.name).join(", ")}`);
  }

  // 2. 构造 prompt
  const prompt = buildPrompt(skills, TASK);

  // 3. 创建 agent（local 模式，cwd 指向目标项目）
  console.log(`[setup] workspace: ${WORKSPACE}`);
  console.log(`[setup] model: ${MODEL}`);
  console.log(`[run] executing...\n`);

  const agent = await Agent.create({
    apiKey: API_KEY,
    model: { id: MODEL },
    local: { cwd: WORKSPACE },
  });

  const run = await agent.send(prompt);
  let output = "";

  for await (const event of run.stream()) {
    switch (event.type) {
      case "assistant":
        for (const block of event.message.content) {
          if (block.type === "text") {
            process.stdout.write(block.text);
            output += block.text;
          }
        }
        break;
      case "tool_call":
        process.stderr.write(`[${event.status}] ${event.name}\n`);
        break;
      case "thinking":
        process.stderr.write(`[thinking] ${event.text.slice(0, 120)}...\n`);
        break;
      case "status":
        if (event.status !== "FINISHED") {
          process.stderr.write(`[status] ${event.status}\n`);
        }
        break;
    }
  }

  const result = await run.wait();
  await agent.close();

  console.log(`\n[done] status=${result.status}`);
  if (result.status !== "finished") process.exit(1);
}

main().catch(e => { console.error(`[fatal] ${e.message}`); process.exit(1); });
```

---

## 四、GitLab CI 配置

```yaml
# .gitlab-ci.yml
variables:
  SKILLS_REPO: "gitlab.com/your-team/cursor-skills.git"
  SKILLS_BRANCH: "main"

agent-review:
  image: node:22
  stage: review
  variables:
    AGENT_TASK: "Review the code changes in this MR. Find bugs, security issues, and code quality problems. Write a structured report."
    AGENT_MODEL: "gpt-5.4"
    AGENT_SKILLS: "security-review,code-quality"  # 空 = 加载全部 skill
  before_script:
    # 1. 装 SDK（每次 pipeline 都重新装）
    - corepack enable
    - pnpm install
    # 2. clone skill 仓库
    - git clone --depth 1 --branch $SKILLS_BRANCH https://oauth2:$SKILLS_REPO_TOKEN@$SKILLS_REPO ./skills
    # 3. 目标项目已在 $CI_PROJECT_DIR，链接到 workspace
    - ln -sf $CI_PROJECT_DIR ./workspace
  script:
    - npx tsx run.ts
  artifacts:
    when: always
    paths:
      - agent-output.md
    expire_in: 7 days
```

环境变量在 GitLab → Settings → CI/CD → Variables 里配：

| 变量 | 说明 |
|------|------|
| `CURSOR_API_KEY` | Cursor API key，masked |
| `SKILLS_REPO_TOKEN` | skill 仓库的 access token（私有库才需要） |

---

## 五、文件关系图

```
                    GitLab Runner（空白）
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   pnpm install     git clone         $CI_PROJECT_DIR
   @cursor/sdk      skills 仓库         （MR 代码）
        │                │                │
        │           .cursor/skills/       │
        │           ├── sec/SKILL.md      │
        │           └── cpp/SKILL.md      │
        │                │                │
        └────────┬───────┘                │
                 ▼                        │
              run.ts ◄────────────────────┘
                 │
            Agent.create({
              local: { cwd: "./workspace" }
            })
                 │
                 ▼
            agent.send(prompt)
            ├── skill 内容注入
            └── 用户任务
                 │
                 ▼
            输出结果 + artifacts
```

---

## 六、关键决策

### 为什么不把 skills 放目标项目里

- 目标项目的 `.cursor/skills/` 是项目专属的（跟代码一起维护）
- 公共 skills（安全审查/代码风格/测试规范）放独立仓库，多个项目复用
- Skill 仓库可以独立更新，不影响任何目标项目

### 为什么选 local 不选 cloud

| | local | cloud |
|---|---|---|
| 私密仓库 | ✅ 直接可见（Runner 已有权限） | ❌ 需要另外授权 |
| MR diff 上下文 | ✅ `$CI_PROJECT_DIR` 天然可用 | ❌ 需手动传 branch/repo |
| 依赖 | 0（node 就够了） | 0 |
| 并发 | Runner 数量限制 | 服务端限制 |

### 为什么每次 pnpm install

- 公共 Runner 不缓存 `node_modules`，每次都是全新的
- `@cursor/sdk` 体积 ~40MB，安装时间 ~5s，可接受
- 避免了缓存污染和版本漂移

---

## 七、扩展

### 多 stage pipeline

```yaml
stages:
  - review
  - fix          # agent 的修改自动提交

agent-fix:
  image: node:22
  stage: fix
  variables:
    AGENT_TASK: "Apply the fixes suggested in the review stage. Edit files as needed."
    AGENT_MODEL: "claude-opus-4-6"
  before_script:
    - corepack enable
    - pnpm install
    - git clone --depth 1 https://oauth2:$SKILLS_REPO_TOKEN@$SKILLS_REPO ./skills
    - ln -sf $CI_PROJECT_DIR ./workspace
  script:
    - npx tsx run.ts
    # agent 修改了文件，commit 回分支
    - cd $CI_PROJECT_DIR
    - git add -A
    - git diff --staged --quiet || git commit -m "fix: auto fixes from Cursor agent [skip ci]"
    - git push origin $CI_COMMIT_BRANCH
  only:
    - merge_requests
```

### 自定义 skill 示例 (放到 skill 仓库里)

```
skills/.cursor/skills/mr-review/SKILL.md
```

```markdown
# MR Review Skill

You are a code reviewer in a GitLab CI pipeline.

## Methodology
1. Read the git diff first (use `git diff origin/main...HEAD`)
2. Check: security → bugs → style → performance
3. Output a structured report:

### Format
- **Security** (critical first)
- **Bugs**
- **Style**
- **Performance**
- **Summary**: 1-3 sentence verdict

## When to block
- Hardcoded credentials
- SQL injection
- Missing error handling on external calls
```

Pipeline 里用：

```yaml
variables:
  AGENT_SKILLS: "mr-review"
  AGENT_TASK: "Review this MR"
```

---

## 相关笔记

- [[Cursor Cookbook 项目拆解]] — cookbook 源码拆解
- [[CLI-Anything 让软件 Agent 化]] — Agent 嵌入工具通用思路
