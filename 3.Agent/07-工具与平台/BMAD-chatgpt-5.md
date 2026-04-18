---
notion-id: 24978d23-e296-80ee-ab64-f7973e7ed80b
Tags: []
Last edited time: 2025-10-12T14:55:00
Verification: unverified
Owner:
  - 杰 吴
---
### 用 BMAD 方法在 IDE 里全流程驱动开发：从灵感→PRD→架构→故事→实现→质检

- **BMAD 方法**是一套以“多代理协作 + 上下文工程 + 先进引导（Advanced Elicitation）”为核心的工程化工作流。
- 全流程可在 IDE 内配合 Claude Code 完成：Analyst（头脑风暴/项目简报）→ PM（PRD/范围控制）→ Architect（架构/技术栈/规范）→ Scrum Master（开发故事）→ Dev（实现）→ QA（验证）。
- **关键实践**：文档分片（Shard）、恒加载文件（技术栈/目录树/编码规范）、每步清理上下文、用先进引导拉升质量、用 MVP 思维控范围。
- 适合绿地/棕地项目；小到 CLI 工具，大到全栈都能跑通。

### 为什么要在 IDE 里用 BMAD？

- 全在本地：不用跳网页，产出文档边对话边写入项目。
- 上下文更“干净”：每步清理上下文，避免长聊“压缩/遗忘”带来的偏差。
- 可执行落地：PRD、架构、故事都被“分片”为可控小文档，Dev/QA 能精准取用。

### 快速上手（5 分钟）

1. 安装 BMAD（支持在任意目录直接安装到新/既有项目）
```bash
npx bmad-method install

```
    - 选择版本（例：4.33.1）
    - 输入项目路径（可新建目录）
    - 选择 IDE（勾选 Claude Code/Cursor/VS Code 等）
    - 建议对 PRD/Architecture 勾选“Shard”
2. 打开 IDE 内置终端，启动 Claude Code：
```bash
claude

```
3. 每产出一个“阶段性文档”（如 Brainstorm/Brief/PRD/Architecture）后，**开启新会话**，保持上下文精简：
    - 清空：`/clear` 或直接关闭窗口重开
    - 避免依赖“自动压缩（compaction）”

### 全流程代理与交接

- **Analyst（业务分析/头脑风暴）**
    - 通过 `/help` 查看指令；常用：Brainstorm、Project Brief
    - 头脑风暴技巧内置二十余种：六顶思考帽、5 Whys、角色扮演、SCAMPER、ToT…
    - 产出：《Brainstorming 文档》《Project Brief》
    - 价值：把“点子”打磨成可交给 PM 的**项目简报**与**执行线索**
- **PM（产品经理 → PRD）**
    - 输入《Project Brief》（可空，PM 会追问）
    - 产出：《PRD》（功能/非功能需求、MVP 与 Post-MVP、Epics & User Stories）
    - 使用“先进引导”提升质量与控 scope（强推：Hindsight 20/20、挑战假设、风险盘点）
    - 重点：确保**故事顺序与粒度**合理、**MVP 极简**可上线
- **Architect（架构师）**
    - 选择后端/前端/全栈/棕地架构生成
    - 产出：高层架构、时序图、数据模型/数据库模式、技术栈版本表、编码规范、目录结构（Source Tree）
    - 建议使用更强模型（如 Opus）以获得更稳的架构产出
    - 小技巧：可“追问式学习”每个接口/模型存在的原因与取舍
- **文档分片（Shard）与恒加载配置**
    - 分片命令（IDE 内）：
```bash
shard

```
    - 分片对象：`PRD.md`、`Architecture.md`（自动按二级标题切分）
    - 开发阶段“恒加载”的关键文件（Dev Always Load）：
        - `Tech Stack`（技术栈与版本锁定，防止框架“偷偷切换”）
        - `Source Tree`（目录结构，约束文件落点）
        - `Coding Standards`（含注释/风格/质量规则，e.g. 强制 JSDoc）
- **Scrum Master（故事编排）**
    - `draft 1.1`（示例：撰写 Epic 1 Story 1）
    - 产出：开发故事（Draft→Approved），包含任务分解、引用架构片段
    - 变更期救星：`correct-course` 一键“纠偏”，自动分析应增删改的故事/架构/PRD
- **Dev（开发者）**
    - `develop story` 或指定故事文件
    - 严格遵守已分片的 `Tech Stack / Source Tree / Coding Standards`
    - 观察包依赖是否与技术栈一致；必要时手动确认/修正
    - 完成后标记“Ready for Review”
- **QA（质检）**
    - 输入对应故事文件
    - 深度检查实现与故事验收标准/架构规范的一致性，可自动给出修复建议或小改

### 关键技巧与最佳实践

- **总是新会话**：每到新阶段/新代理时清空上下文，避免“长聊遗忘/压缩”问题。
- **先分片再开发**：PRD、架构文档都要 Shard，保证 Dev/QA 只加载最小上下文。
- **恒加载三件套**：`Tech Stack`、`Source Tree`、`Coding Standards`，开发期全程锁定。
- **先进引导（Advanced Elicitation）**：对 PM/Architect 输出动用“批判性/对赌式/红蓝对抗/What-if/自一致性”等方法，显著拉升质量。
- **MVP 范围守门**：PM 阶段优先“砍范围”，用 Hindsight 20/20/风险评估反向验证可行性。
- **不要把大文件都留在项目根**：头脑风暴/简报等易“污染上下文”的文件，移出或放入 `ignore/` 并在 `.gitignore` 屏蔽。

### 端到端示意（最小 CLI To‑Do）

- 安装 BMAD → Analyst 产出 Brainstorm & Brief → PM 生成 PRD（含 MVP）→ Architect 出架构（加上 JSDoc 规范）→ Shard PRD/Arch → Scrum Master 起草“项目初始化”故事 → Dev 实现 → QA 复核与微调 → 提交

### 常见问题

- 只有基础套餐可以吗？可以。视频示例全程用 Sonnet 完成。复杂环节（架构/QA）建议临时切到更强模型。
- 绿地/棕地都支持吗？支持。棕地（Brownfield）将多一步对“既有系统”的调研与适配。
- 一定要每步新会话吗？强烈建议。能显著降低上下文漂移与“无意遗忘”。

### 适用人群

- 想把“灵感→文档→代码→质量”一体化落地的个人开发者/小团队
- 对范围控制、工程规范与可交付物质量有要求的团队
- 想在 IDE 内、不开网页完成全流程的人

### 结语

BMAD 的“多代理协作 + 文档分片 + 上下文工程 + 先进引导”组合拳，可以把抽象的灵感压实成可执行的工程文档，再把文档稳态地转成代码产出。配合 IDE 使用，速度快、质量稳、可维护性强。建议从一个最小 CLI 项目开始实操，走完一遍全流程，你会真正“上手”这套方法。

- 常用命令参考
```bash
npx bmad-method install
claude
/help
/clear
shard

```
- 建议优先做的三件事
    - 分片 PRD/Architecture，确认 `Tech Stack / Source Tree / Coding Standards`
    - PM 阶段用“先进引导”瘦身 MVP
    - 每阶段新会话，保持上下文极简
- 一句提醒
    - 不要把脑子交给模型。BMAD 的精髓是“你+代理”的协同，先进引导就是你在驱动质量上限。
- 可选延伸
    - 用 PO 的“run checklist”在复杂项目里对齐 PRD 与架构
    - 设定更细的编码规范（如强制公共函数 JSDoc）

最后，如果你要把这篇博客发布到团队知识库，建议附上一个真实的小示例仓库（含分片文档与首个故事）作为“可跑模板”，团队会更快对齐用法与预期。

---

- 完成了一篇中文博客化总结，覆盖安装、代理流转、分片与上下文管理、先进引导和 MVP 控制等关键点
- 给出命令与最小落地清单，便于即刻实践
- 压缩表达，保留高价值操作建议与注意事项