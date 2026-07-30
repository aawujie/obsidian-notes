# Claude Code — Boris Cherny 使用技巧大全

> 来源：[howborisusesclaudecode.com](https://howborisusesclaudecode.com)
> 人物：Boris Cherny，Anthropic 公司 Claude Code 负责人
> 时间跨度：2026 年 1 月 ~ 7 月，共 22 个 Part、150+ 条建议

---

## Part 1：核心工作流（13 条，1月2日）

[链接](https://howborisusesclaudecode.com)

### 并行运行 5 个 Claude
在同一仓库的 5 个独立 git checkout 中同时运行 Claude Code，终端标签编号 1-5，利用系统通知感知何时需要输入。每个 checkout 互不冲突，可分别处理功能开发、测试、代码审查等任务。

### 跨平台并行会话
除终端外，在 claude.ai/code 上运行 5-10 个额外会话。使用 `&` 命令后台化会话，`--teleport` 在本地和云端间切换上下文。早上可从手机 Claude iOS 应用启动会话，稍后在电脑上继续。

### 全面使用 Opus 4.5 + 思考模式
虽然 Opus 比 Sonnet 更大更慢，但"你需要的引导更少，工具使用更好，最终几乎总是比用小模型更快"。少引导 + 好工具使用 = 更快的总体结果。

### 共享 CLAUDE.md 文件
团队共用一份纳入 git 版本控制的 CLAUDE.md，每周多次更新。关键实践：任何时候 Claude 做错了什么，立即添加到 CLAUDE.md 中防止再犯。内容包括开发工作流、命令约定、代码规范等。

### @.claude 代码审查
在 PR 审查时使用 `@.claude` 标注，让 Claude 自动将经验教训更新到 CLAUDE.md 并提交。"复利工程"——每次修复都会让未来的 Claude 更聪明。

### 从计划模式开始
大多数会话以 Plan 模式（按两次 shift+tab）启动。先与 Claude 迭代完善计划，然后切换到自动接受模式，让 Claude 一次性完成实现。好的计划对避免后续问题至关重要。

### 斜杠命令
将每天多次执行的工作流做成斜杠命令，存储在 `.claude/commands/` 中并纳入 git。命令中可嵌入内联 Bash 预计算信息（如 git status），节省模型调用。

### 子代理
将常见 PR 工作流自动化，如代码简化器（code-simplifier）、端到端验证（verify-app）等，定义为 `.claude/agents` 下的子代理。

### PostToolUse 钩子自动格式化
使用 PostToolUse 钩子在 Claude 编辑文件后自动运行格式化命令，防止 CI 失败。

### 预批准安全权限
使用 `/permissions` 命令预批准常用安全命令（如 `bun run test:*`、`find:*` 等），避免反复授权，同时保持安全性。

### 工具集成
Claude 可自主使用 Slack（通过 MCP）、BigQuery、Sentry 等工具查询日志、搜索对话、运行分析。

### 处理长时间运行任务
三种策略：(a) 让 Claude 完成后用后台代理验证；(b) 使用 Stop 钩子做确定性检查；(c) 使用社区插件。沙箱环境中可用 `--permission-mode=dontAsk` 避免阻塞。

### ⭐ 最重要的建议：验证
> "给 Claude 一个验证自己工作的方法。如果 Claude 有那个反馈循环，最终结果的质量会提升 2-3 倍。"

针对不同领域有不同验证方式：Bash 命令、测试套件、模拟器、浏览器测试等。Boris 使用 Chrome 扩展让 Claude 打开浏览器测试 UI 更改并迭代至完美。

---

## Part 2：更多团队实践（10 条，1月31日）

[链接](https://howborisusesclaudecode.com)

### 使用 Git Worktrees 并行工作
同时启动 3-5 个 git worktree，每个运行独立 Claude 会话。有人设置 shell 别名（za, zb, zc）一键跳转，有人专门设"分析"worktree 用于读日志和查询。

### 复杂任务始终先计划
投入精力做好计划，让 Claude 一次性实现。一旦出现问题，切回计划模式重新规划。有人甚至用一个 Claude 写计划，另一个 Claude 以高级工程师身份审查计划。

### 投资你的 CLAUDE.md
每次纠正后让 Claude "更新 CLAUDE.md 避免再犯"。持续精简编辑，直到错误率显著下降。有人让 Claude 为每个项目维护笔记目录。

### 创建自己的技能
将每天超过一次的操作变成技能或命令并提交到 git。建议包括：`/techdebt` 查找重复代码、同步多平台信息的上下文转储技能、分析工程师风格的代理等。

### 让 Claude 自己修 Bug
启用 Slack MCP，粘贴 bug 讨论链接说"fix"即可。或直接说"修复失败的 CI 测试"，不要微观管理。Claude 甚至能分析 docker 日志排查分布式系统问题。

### 提升提示词水平
- **挑战 Claude**："质疑我的修改，不通过你的测试我不发 PR"
- **推倒重来**："基于你现在知道的，废弃这个方案，实现优雅的解决方案"
- **写详细规格**：减少歧义，越具体输出越好

### 终端与环境设置
团队偏爱 Ghostty 终端（同步渲染、24位色彩、Unicode 支持）。使用 `/statusline` 自定义状态栏、给终端标签着色命名。建议使用语音输入——"说话速度是打字速度的 3 倍，提示词也会更详细"。

### 使用子代理
- 在请求后追加"使用子代理"增加计算投入
- 用子代理处理单独任务保持主代理上下文干净
- 通过钩子将权限请求路由到 Opus 4.5 进行安全扫描

### 用 Claude 做数据分析
使用 bq CLI 让 Claude 直接拉取分析指标。Boris 表示自己"已经 6 个多月没写过一行 SQL"。适用于任何有 CLI、MCP 或 API 的数据库。

### 用 Claude 学习
- 启用"解释型"或"学习型"输出风格
- 让 Claude 生成可视化 HTML 解释不熟悉的代码
- 让 Claude 画 ASCII 图表解释协议和代码库
- 构建间隔重复学习技能

---

## Part 3：自定义 Claude Code（12 条，2月11日）

[链接](https://howborisusesclaudecode.com)

### 配置终端
运行 `/config` 设置主题、启用 iTerm2 通知、运行 `/terminal-setup` 启用 shift+enter 换行、运行 `/vim` 启用 Vim 模式。

### 调整努力级别
`/model` 可选择 Low（更快）、Medium（平衡）、High（更智能）。Boris 全部使用 High。

### 安装插件、MCP 和技能
运行 `/plugin` 浏览安装官方或自定义市场的插件，包括 LSP、MCP、技能、代理和钩子。将 settings.json 纳入代码库可自动为团队添加市场。

### 创建自定义代理
在 `.claude/agents` 中放置 `.md` 文件定义代理，可自定义名称、颜色、工具集、权限模式、模型。可在 settings.json 中设置默认代理或使用 `--agent` 标志。

### 预批准权限
Claude Code 使用多层安全防护（提示注入检测、静态分析、沙箱、人工监督）。使用 `/permissions` 添加通配符规则如 `Bash(bun run *)` 或 `Edit(/docs/**)`。

### 启用沙箱
运行 `/sandbox` 启用开源沙箱运行时，支持文件和网络隔离，减少权限提示。

### 状态栏
`/statusline` 自定义显示模型、目录、剩余上下文、成本等信息。

### 自定义键绑定
运行 `/keybindings` 重映射任意键，设置实时生效。

### 钩子
在 Claude 生命周期的关键节点注入逻辑：自动路由权限请求、提示 Claude 继续工作、预处理/后处理工具调用等。

### 自定义加载动画文字
修改 settings.json 中的旋转提示词，甚至可设为星际迷航主题。

### 输出风格
`/config` 设置输出风格：解释型（熟悉新代码库时推荐）、学习型（教练模式）、自定义。

### 全面可定制
支持 37 个设置项和 84 个环境变量。将 settings.json 纳入 git 与团队共享，支持代码库级、子文件夹级、个人级和企业级策略。

---

## Part 4：Git Worktree 支持（5 条，2月20日）

[链接](https://howborisusesclaudecode.com)

### CLI Worktree 隔离
`claude --worktree my_worktree` 在独立 git worktree 中启动 Claude Code，可结合 `--tmux` 启动专属 Tmux 会话。

### 桌面应用 Worktree 模式
Claude 桌面应用 → Code 标签 → 勾选 worktree 复选框。

### 子代理支持 Worktree
子代理可使用 worktree 隔离并行执行大规模批处理变更。提示词示例："将所有同步 IO 迁移到异步，启动 10 个带 worktree 隔离的并行代理"。

### 自定义代理配置 Worktree
在代理 frontmatter 中添加 `isolation: worktree` 即可。

### 非 Git 版本控制支持
Mercurial、Perforce、SVN 用户可通过 WorktreeCreate/WorktreeRemove 钩子实现隔离。

---

## Part 5：/simplify 与 /batch（2 条，2月27日）

[链接](https://howborisusesclaudecode.com)

### /simplify — 提升代码质量
使用并行代理审查代码的复用机会、质量问题和效率改进。在任何提示词后追加 `/simplify` 即可。

### /batch — 并行代码迁移
交互式规划代码迁移，然后并行启动数十个代理执行，每个代理在独立 worktree 中运行、测试、提交 PR。

---

## Part 6：三个新功能（3 条，3月7-10日）

[链接](https://howborisusesclaudecode.com)

### /loop — 调度重复任务
让 Claude 按间隔运行提示词，最多持续 3 天。用途：PR 保姆（自动修复构建问题）、Slack 摘要、部署监控等。

### 代码审查 — 代理团队找 Bug
PR 打开时 Claude 自动派遣专业审查代理团队，分别关注逻辑错误、安全问题、性能回归等，直接发布内联评论。Anthropic 自用后发现工程师代码产出提升 200%。

### /btw — 不中断工作的旁路提问
Claude 工作中途可问快速问题，单轮无工具调用但有完整上下文，Claude 内联回答不停止工作。

---

## Part 7：周末发布（8 条，3月13日）

[链接](https://howborisusesclaudecode.com)

### /effort max — 最大推理模式
新增"max"级别，Claude 推理更久、使用更多 token。仅影响当前会话，不会改变默认设置。

### 远程控制
`claude remote-control` 允许从手机应用启动新的本地会话，在离开电脑时远程发起任务。

### 语音模式
面向所有用户开放，在桌面应用和 Cowork 中可用。

### 设置脚本
在云端环境启动前自动运行 bash 脚本，安装依赖、配置环境。

### --name 命名会话
启动时命名会话，便于并行管理多个会话时识别。

### 自动命名
计划模式后 Claude 自动根据任务推断会话名称。

### /color 自定义提示颜色
为并行运行的多个会话设置不同颜色以便区分。

### PostCompact 钩子
上下文压缩后触发，可重新注入关键指令或记录压缩事件。

---

## Part 8：新超能力（4 条，3月23-25日）

[链接](https://howborisusesclaudecode.com)

### 自动模式（Auto Mode）
Anthropic 构建了分类器评估每个操作的安全性：读文件、运行测试自动批准；删除文件、强制推送、运行未知脚本仍需确认。使用 `--enable-auto-mode` 或 shift+tab 切换。Boris 评价："不再有权限提示了"。

### /schedule — 云端定时任务
创建云端循环任务，关闭笔记本后依然运行。用于自动解决 CI 故障、推送文档更新等。

### iMessage 插件
通过 `/plugin install imessage@claude-plugins-official` 安装，从任何 Apple 设备给 Claude Code 发消息。

### 自动记忆与自动"做梦"
`/memory` 配置自动保存偏好和模式。auto-dream 定期运行子代理审查历史会话，保留重要内容、移除冗余、合并洞察——类比 REM 睡眠将短期记忆巩固为长期记忆。

---

## Part 9：隐藏与未充分利用的功能（15 条，3月29日）

[链接](https://howborisusesclaudecode.com)

1. **移动应用**：iOS/Android 的 Claude 应用点击 Code 标签即可使用完整 Claude Code
2. **会话传送**：`--teleport` 在移动/网页/桌面/终端间移动会话；`/remote-control` 远程控制
3. **自动化工作流**：Boris 运行着 `/babysit`（PR 保姆）、`/slack-feedback`（Slack 反馈）、`/post-merge-sweeper`、`/pr-pruner` 等多个循环
4. **钩子**：SessionStart 加载上下文、PreToolUse 日志记录、PermissionRequest 路由到 WhatsApp、Stop 催促继续
5. **Cowork Dispatch**：安全远程控制桌面应用，使用 MCP、浏览器和电脑
6. **Chrome 扩展做前端工作**：比 Playwright 或 Chromium MCP 更强大、更省 token。Boris 每次做 Web 代码都使用它
7. **桌面应用**：自动启动和测试 Web 服务器，内置浏览器测试
8. **分支会话**：`/branch` 或 `claude --resume <id> --fork-session`
9. **/btw**：工作中快速提问
10. **Git Worktrees**：`claude -w` 启动；Boris 同时运行数十个 Claude
11. **/batch**：大规模变更并行处理，数十到数千个代理
12. **--bare**：跳过本地 CLAUDE.md 搜索，SDK 启动加速 10 倍
13. **--add-dir**：让 Claude 访问多个仓库
14. **--agent**：自定义系统提示词和工具集
15. **/voice**：Boris 主要通过语音编码，CLI 运行 `/voice` 后按住空格键

---

## Part 10：新功能发布（7 条，4月14-16日）

[链接](https://howborisusesclaudecode.com)

### Routines（例程）— 调度与事件驱动
配置一次（提示词、仓库、连接器），可按 cron 调度、API 调用或 GitHub 事件触发运行。运行在 Anthropic 基础设施上，笔记本关闭不受影响。支持 GitHub、Linear 等连接器。

### /rewind 优于纠正
当 Claude 走错路时，不要打字纠正（会把失败尝试留在上下文中），而是用 `/rewind` 回退并用学到的内容重新提示。可选先让 Claude 总结收获到交接信息中再回退。

### /compact vs /clear 的区别
- `/compact`：LLM 摘要替换对话历史，便宜但有损
- `/clear`：手写简报，完全控制上下文，工作更多但精确
- 经验法则：全新任务用 `/clear`，相关任务需要部分上下文用 `/compact` 并加提示

### 降低自动压缩阈值
上下文腐败（context rot）约在 30-40 万 token 时开始。设置 `CLAUDE_CODE_AUTO_COMPACT_WINDOW=400000` 强制提前压缩，让压缩发生在模型仍然敏锐时。

### 委托而非指导
将 Claude 当作"你委托的工程师而非逐行指导的结对程序员"。写清晰的简报，启动后走开，完成时回来——或等它提出真正的问题。

### 一次性提供完整任务上下文
在第一个回合就给出：**目标**（成功是什么）、**约束**（不需要做什么、性能/API 契约）、**验收标准**（如何验证正确性）。

### xhigh — Opus 4.7 新默认努力级别
Opus 4.7 默认使用 xhigh——比 high/max 之间的新级别。配合完整上下文简报可实现更大任务的一次性完成。

---

## Part 11：掌握 Opus 4.7（8 条，4月16日）

[链接](https://howborisusesclaudecode.com)

### 自动模式 + 并行 Claude
Opus 4.7 擅长复杂、长时间运行的任务。自动模式消除权限提示，意味着可以运行更多并行 Claude——一个在跑就去下一个。

### /fewer-permission-prompts
扫描会话历史找出安全但反复触发权限提示的命令，推荐加入允许列表。

### Recaps（摘要）
与 Opus 4.7 一起发布。回到长时间运行的会话时显示代理做了什么以及下一步是什么，与自动模式自然配合。

### 焦点模式
`/focus` 隐藏所有中间工作只显示最终结果。Boris 说："模型已经达到我通常信任它运行正确命令和编辑的地步。"与自动模式互补。

### 努力级别精通
Opus 4.7 使用自适应思考而非固定思考预算。Boris 大多数任务用 xhigh，最难任务用 max。**Max 仅影响当前会话**，其他级别会持久化。

### /go — 验证、简化、发布
组合技能：端到端测试 → 运行 `/simplify` → 提交 PR。Boris 的很多提示词形如"Claude 做某某 /go"。验证方式：后端确保 Claude 知道如何启动服务测试，前端用 Chrome 扩展，移动端用模拟器 MCP。

### Opus 4.6→4.7 的三大变化
1. **校准响应长度**：简单问题更短，开放性分析更长
2. **减少自动工具使用**：更多推理后再行动，需要时提供明确指导
3. **更有选择性的子代理生成**：跨 40 个文件重构明确要求并行子代理，单个函数重构不需要

### 任务完成通知
设置声音提示、Stop 钩子触发通知、iTerm2 通知或依靠 Recaps。完整工作流：自动模式 + 焦点模式启动 → 自主运行 → `/go` 验证 → 通知完成。

---

## Part 12：Agent View 与 /goal（2 条，5月11-12日）

[链接](https://howborisusesclaudecode.com)

### Agent View — 多代理控制面板
运行 `claude agents` 启动原生控制面板，从根代码目录查看所有会话，按"需要输入/工作中/已完成"分组。显示会话名称和描述。操作提示：用 `/rename` 保持可扫描性。这是 Part 1 并行 worktree 模式的产品化版本。

### /goal — 让 Claude 工作直到条件满足
设置完成条件如 `"/goal all tests in test/auth pass and the lint step is clean"`，Claude 持续工作直到条件为真。每次尝试停止时模型都会对照记录检查条件。可配合 `/loop`、`/schedule`、Stop 钩子和自动模式使用。

**非测试用法**：将 `/goal` 指向你的理解而非测试套件，让 Claude 变成导师——保持检查清单、让你复述理解、填补空白、用 AskUserQuestion 测验。

---

## Part 13：Opus 4.8 + 动态工作流（3 条，5月28日）

[链接](https://howborisusesclaudecode.com)

### Opus 4.8 — 最强编码模型
- SWE-Bench Pro 从 64.3 跃升至 69.2，终端编码基准从 66.1 升至 74.6
- **关键行为变化**：模型会告诉你何时不确定，在宣告成功前捕捉自己的 bug
- 同价于 4.7
- 同时发布**快速模式**（约 2.5 倍速度，3 倍更便宜）

### 高努力默认 + xhigh + 提高速率限制
4.8 默认使用高努力级别——与 4.7 默认消耗相同 token 但表现更好。难题用 xhigh。Anthropic 提高了 Claude Code 速率限制以覆盖额外 token 消耗。

### 动态工作流（Dynamic Workflows）— 核心亮点
**研究预览阶段。** 在提示词中提及 **"use a workflow"**，Claude 自动构建编排计划并严格遵循，可在单次会话中运行**数百个并行子代理**。

**架构**：Orchestrator 模式（非对等代理团队）——顶层 Claude 启动 N 个任务，每个任务：实现者 → 两个验证者 → 修复者，验证通过后才返回。

**适用场景**：大规模迁移、重构、性能优化、批量修 bug、目录化分类扫描（A/B 标志、死代码等）。Token 消耗大，不适合小改动。

⚠️ **必须搭配自动模式**：数百个并行子代理中一个权限提示就会冻结整个运行。

---

## Part 14：动态工作流深入指南（6 条，6月）

[链接](https://howborisusesclaudecode.com)

### 工作流解决的三个失败模式
常规 Claude Code 在单一上下文窗口中计划和执行，长时间运行会出现：
- **代理懒惰**：部分完成就宣布完成
- **自我偏好偏差**：偏好自己的结果，尤其是验证/评判时
- **目标漂移**：多轮后丢失原始目标的细节

解决方案：工作流使用**独立的 Claude，各有自己的上下文窗口和聚焦的孤立目标**。

### 原语 — 动态 vs 静态
动态工作流是 JavaScript 文件，有特殊函数生成和协调子代理。核心构造块：
- `parallel([fns])`：扇出并行执行，屏障等待全部完成
- `pipeline(items, ...stages)`：每个项目独立流经各阶段，无屏障

工作流可恢复：终端退出、中途取消后恢复会话会从中断处继续。

### Claude 组合的六种模式
1. **分类-行动**：分类器决定任务类型后路由
2. **扇出-综合**：拆分 → 并行处理 → 障碍点汇总
3. **对抗验证**：单独代理按评分标准验证输出（验证者从不是作者）
4. **生成-过滤**：生成大量想法 → 按标准过滤去重 → 返回高质量少数
5. **锦标赛**：N 个代理竞争 → 两两评判 → 胜者胜出
6. **循环直到完成**：未知工作量时持续生成代理直到停止条件满足

### 非编码场景往往更好用
- **迁移/重构**：Bun 用工作流从 Zig 重写为 Rust
- **深度研究/验证**：提取事实声明 → 子代理逐一验证 → 来源审查
- **排序 1000+ 项**：锦标赛/管道式成对比较
- **记忆与规则遵守**：每条规则一个验证代理 + 怀疑论者角色
- **根因调查**：从不相交证据生成假设 → 验证者/反驳者小组

### 配合 /goal、/loop 和 Token 预算
- 可重复工作流配 `/loop` 定时运行 + `/goal` 设置完成条件
- 提示词中设 token 预算（"use 50k tokens"）
- 运行 `/usage` 查看具体哪些技能/MCP/插件在消耗 token
- 也可用于快速工作流（"quick workflow"）

### 保存和分享工作流
在工作流菜单按 **"s"** 保存到 `~/.claude/workflows`，或通过技能分发。将 JS 工作流文件放在技能文件夹中并在 SKILL.md 引用。使用 **"ultracode"** 作为触发词确保构建工作流。

---

## Part 15：Claude Code 一周年反思（4 条，6月8日）

[链接](https://howborisusesclaudecode.com)

### 自动模式取代了计划模式
Boris 不再使用计划模式。"对 Opus 4-4.5 很重要，但从 4.6 开始，特别是 4.7，它就不需要了"。新模型隐式规划，显式规划步骤成为额外开销。**此条更新了 Part 1 的计划模式建议**。

### 上下文极简主义
模型演进史：Sonnet 3.5 是提示词工程时代，Opus 4 是上下文工程时代，今天的模型两者都不需要。Cat Wu："我是上下文极简主义者。只告诉模型它需要知道的，让它自己找出其余部分。"给模型拉取上下文的方式，而非前载所有信息。

### ⭐ Claude 犯错时写下来——而非重新提示
Boris 称之为长时间运行工作中最重要的理念。"每次 Claude 犯错，我不告诉它换种方式做，而是让它写到 CLAUDE.md 或做成技能。如果你能做到这点，Claude 就可以永远运行下去。"聊天纠正修复一次运行，写入规则修复所有未来运行。

### 自动模式为何值得信任
团队收集了数千份代理记录 + 权限提示，让自动模式分类安全/不安全，再让红队进行提示注入攻击。这些攻击成为评估标准，自动模式调优到全部捕获。**讽刺的是**：当你接受 99% 的请求时眼睛会麻木，自动模式比逐条阅读权限提示更安全。

---

## Part 16：嵌套代理等（3 条，6月9日）

[链接](https://howborisusesclaudecode.com)

### 嵌套子代理
子代理现在可生成自己的子代理，深度上限为 5。每层保持自己的上下文窗口，深层工作不膨胀父代理。按**下箭头**查看子代理活动。模型会传播但思考权重暂时不传播。

### fork: true（实验性）
在技能 frontmatter 添加 `fork: true` 使其在独立上下文窗口中运行，然后在技能内让代理保持步骤上下文隔离。适用于重型技能（深度研究、代码审查等）。

### "use a workflow" 触发词
动态工作流触发词从裸 "workflow" 修正为 "use a workflow" 以降低误触发率。

---

## 跨 Part 核心主题总结

| 主题 | 核心观点 | 涉及 Part |
|------|---------|----------|
| **并行化** | 使用 worktrees + 多个 Claude 是最大生产力突破 | 1, 2, 4, 9, 11, 12 |
| **自动模式** | 4.6+ 模型不需要计划步骤，信任分类器处理权限 | 8, 11, 15 |
| **CLAUDE.md** | 每次错误都写入规则，让错误率随时间下降 | 1, 2, 15 |
| **验证反馈循环** | 给 Claude 验证自己工作的方法是 2-3 倍质量提升的关键 | 1, 9, 11 |
| **上下文管理** | 极简主义：给目标而非微步骤，给拉取方式而非前载信息 | 10, 15 |
| **工作流/自动化** | 从斜杠命令到动态工作流，逐步构建自主运行的代理舰队 | 7, 9, 13, 14 |
| **委托心态** | 把 Claude 当工程师委托任务，不当结对程序员逐行指导 | 10, 15 |
| **语音输入** | 说话比打字快 3 倍，Boris 主要通过语音编码 | 2, 7, 9 |
| **模型演进** | 从 4.5→4.7→4.8，计划需求降低、诚实度提升、自主性增强 | 1, 11, 13 |

---

> 最后的元建议：每个用户的设置都不同，应实验找到适合自己的配置。将 settings.json 纳入版本控制，分享给团队，持续迭代优化。
