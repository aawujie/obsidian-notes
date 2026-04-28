# ACP 协议与 CC 多Agent 调度

## 什么是ACP

**ACP = Agent Client Protocol**（Agent客户端协议），Anthropic 2025年底推出的开放标准。类比LSP让编辑器→语言服务器互通，ACP让AI Agent→编码Agent互通。

不是闭源方案，是开放协议，Google/OpenAI/Cursor/GitHub都已接入。

---

## 协议架构

```
调度Agent（OpenClaw / 你的主控）
    │
    ├── ACP 协议 ←→ acpx CLI（协议客户端）
    │                    │
    │                    ├── claude-agent-acp（适配器）→ Claude Code 进程
    │                    │
    │                    ├── codex-acp（适配器）→ Codex 进程
    │                    │
    │                    └── Gemini CLI 原生 --acp → Gemini 进程
    │
    └── 不需要 PTY 抓屏，不需要 --print 等输出
       所有通信走结构化消息（thinking / tool_call / text / done）
```

**核心创新**：编码Agent不再是黑盒进程，而是通过标准协议暴露为可调用的服务。调度方不需要关心Agent的内部实现，只发标准消息、收标准结果。

---

## 关键概念

### 适配器（Adapter）

协议和具体Agent之间的翻译层。比如 `claude-agent-acp` 启动CC进程，把ACP消息翻译成CC能理解的输入，把CC的输出翻译回ACP消息。

### 会话（Session）

持久化的对话上下文。一个会话 = 一个CC进程 + 完整对话历史。多Agent调度就是多个独立的会话并行。

### acpx

OpenClaw社区做的ACP CLI客户端，把协议细节包装成命令行工具。你的主Agent不需要自己实现ACP协议，通过acpx驱动任何ACP兼容的Agent。

---

## CC多Agent实战

### 环境配置

```json
// ~/.claude/settings.json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://ai-coding-ali.deeproute.cn",
    "ANTHROPIC_MODEL": "deepseek-v4-pro"
  },
  "model": "deepseek-v4-pro",  // 必须精确匹配API支持的模型名
  "permissions": { ... }
}
```

### 单次调用

```bash
npx acpx@latest --cwd ~/code/quant-factor claude exec "选出top 10股票"
→ deepseek-v4-pro 模型回复
```

### 创建持久化会话

```bash
# 三个Agent，三个独立会话
npx acpx --cwd ~/code/quant-factor claude sessions new --name 选股
npx acpx --cwd ~/code/quant-factor claude sessions new --name 择时
npx acpx --cwd ~/code/quant-factor claude sessions new --name 风控
```

会话存储在 `~/.acpx/sessions/quant-factor/选股/`，下次可接着聊。

### 多Agent并行调度

```bash
# OpenClaw主Agent 调度三个CC
exec bg → npx acpx --cwd ~/code/quant-factor claude -s 选股 \
  "从因子面板选出top 10，只回代码列表"

exec bg → npx acpx --cwd ~/code/quant-factor claude -s 择时 \
  "读取hs300日线，判断当前能否开仓。回'能/不能'+理由"

exec bg → npx acpx --cwd ~/code/quant-factor claude -s 风控 \
  "对持仓做风险评估。回'满仓/半仓/空仓'+理由"
```

三个Agent同时运行：
- 选股Agent看基本面因子
- 择时Agent看大盘环境
- 风控Agent看仓位安全
- 主Agent汇总三个结果拍板

### 会话管理

```bash
npx acpx claude sessions           # 列出所有会话
npx acpx claude -s 选股 status     # 查看会话状态
npx acpx claude -s 选股 history    # 查看对话历史
npx acpx claude -s 选股 close      # 关闭会话
npx acpx claude -s 选股 cancel     # 取消当前运行中的任务
```

---

## 与 --print 模式的对比

| 维度       | exec claude --print | acpx claude |
| :------- | :------------------ | :---------- |
| 通信方式     | 文本流（一次性输出）          | 结构化ACP消息    |
| 会话持久化    | ❌ 跑完进程死             | ✅ 会话存盘可续聊   |
| 并行多Agent | 需要文件传结果             | ✅ 独立会话天然隔离  |
| 错误处理     | 文本中找error           | 结构化error事件  |
| 适配器开销    | 无（直接调CC）            | 轻量（适配器中转）   |

---

## 架构全景

```
┌──────────────────────────────────────────────┐
│              主调度 Agent                      │
│         （OpenClaw / 手工 / Cron）              │
├──────────────────────────────────────────────┤
│              acpx CLI 客户端                    │
├──────────┬──────────┬──────────┬─────────────┤
│ claude   │  codex   │ gemini   │   cursor     │
│ 适配器    │  适配器   │ 原生ACP  │  原生ACP     │
├──────────┼──────────┼──────────┼─────────────┤
│Claude    │ Codex    │Gemini    │  Cursor      │
│Code      │ CLI      │ CLI      │  CLI         │
│(DSv4)    │          │          │              │
└──────────┴──────────┴──────────┴─────────────┘
        会话  会话  会话    各自独立的进程 + 上下文
```

---

## 实战教训

### 1. model 字段必须精确

`model: "sonnet[1m]"` → 适配器映射成 `claude-sonnet-4-6` → deeproute不认识 → 400
改 `model: "deepseek-v4-pro"` → 直接匹配 → 通过

### 2. 适配器不读 env 来覆盖 model

`ANTHROPIC_MODEL` 环境变量只影响CC自己的模型选择，但适配器可能用 settings.json 的 `model` 字段而非 `ANTHROPIC_MODEL`。两者保持一致最稳。

### 3. exec vs session

- `exec`：单次任务，跑完会话销毁
- `session`：持久化，适合需要多轮对话或保留上下文的场景
- 多Agent调度优先用 session 模式

---

## 应用场景

1. **量化多Agent**（本文案例）：选股+择时+风控各一个CC，独立判断汇总决策
2. **代码Review**：一个CC看后端改动、一个看前端，最后合并意见
3. **并行重构**：多个模块同时重构，各跑各的CC，最后统一合并
4. **数据管道**：一个CC清洗数据、一个算因子、一个跑回测，流水线并行

---

## 支持的Agent全表

| Agent       | 接入方式                  | 备注             |
| :---------- | :-------------------- | :------------- |
| Claude Code | claude-agent-acp 适配器  | 已实战验证 ✅        |
| Codex       | codex-acp 适配器         |                |
| Gemini CLI  | 原生 `--acp`            |                |
| Copilot     | 原生 `--acp --stdio`    |                |
| Cursor      | 原生 `cursor-agent acp` |                |
| Pi          | pi-acp 适配器            |                |
| OpenClaw    | 原生 `openclaw acp`     | 自身也是ACP Server |

---

*创建日期：2026-04-27*
*标签： #ACP #ClaudeCode #多Agent #acpx #协议 #量化 *
