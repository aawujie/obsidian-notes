---
title: flyai-skill调研
type: concept
created: 2026-06-10
updated: 2026-06-10
tags: [flyai, skill, 调研, MCP, 飞猪, OpenClaw, Claude Code, 旅行搜索]
---

## 结论摘要

**flyai-skill** 是阿里飞猪团队开源的 AI Agent 旅行搜索技能，通过 CLI + MCP 协议连接飞猪旅行平台，支持在 Claude Code / OpenClaw 等 agent 内用自然语言搜索机票、酒店、火车票、景点、演出、签证等。**免费体验模式可直接使用**（无需注册），付费 API Key 解锁完整结果。

**核心价值**：8 个 MCP tool、一套 SKILL.md 定义、跨平台兼容（Claude Code + OpenClaw）、零配置开箱即用。

**风险点**：硬编码内置 API Key、CLI 代码混淆、设备指纹采集。

---

## 一、项目概况

| 项 | 值 |
|---|-----|
| **仓库** | https://github.com/alibaba-flyai/flyai-skill |
| **许可证** | MIT |
| **当前版本** | v1.0.14 (skill) / v1.0.16 (CLI) |
| **首次发布** | 2026-03-17 (CLI) |
| **维护方** | alibaba-flyai (飞猪 AI 开放平台) |
| **Homepage** | https://open.fly.ai/ |
| **Stars** | ~40+ |
| **CLI 周下载** | ~500+ |

## 二、架构总览

```
用户自然语言 → Agent (Claude Code / OpenClaw)
                    ↓ 意图匹配 (SKILL.md patterns, priority=90)
              /flyai <command> --params
                    ↓
              flyai-cli (Node.js, Commander)
                    ↓ MCP jsonrpc 2.0, tools/call
         https://flyai.open.fliggy.com/mcp
                    ↓
              飞猪旅行数据平台
                    ↓
              JSON 响应 → Agent 格式化 Markdown → 用户
```

**核心组件**：
- `skills/flyai/SKILL.md` — 技能定义文件（意图匹配、显示规则、使用说明）
- `skills/flyai/references/` — 8 个命令的参数参考文档
- `@fly-ai/flyai-cli` — Node.js CLI，通过 MCP 协议调用飞猪 API
- `.claude-plugin/` — Claude Code 插件元信息
- `.claude-plugin/marketplace.json` — ClawHub 市场注册

## 三、功能清单

### 8 个 MCP Tool

| Tool 名称 | CLI 命令 | 功能 | 必填参数 |
|-----------|---------|------|---------|
| `fliggy_fast_search` | `keyword-search` | 全类目关键词搜索（酒店/机票/门票/签证/邮轮等） | `--query` |
| `fliggy_ai_search` | `ai-search` | AI 语义搜索，理解复杂意图 | `--query` |
| `search_flight` | `search-flight` | 结构化机票搜索（含直飞/中转/价格/时间段等 20+ 过滤） | `--origin` |
| `search_hotels` | `search-hotel` | 结构化酒店搜索（星级/床型/价格/POI 等过滤） | `--dest-name` |
| `search_poi` | `search-poi` | 景点/活动搜索（35 个分类） | `--city-name` |
| `search_domestic_train` | `search-train` | 火车票搜索（国内） | `--origin` |
| `search_marriott_hotels` | `search-marriott-hotel` | 万豪集团酒店搜索 | `--dest-name` |
| `search_marriott_packages` | `search-marriott-package` | 万豪套餐产品搜索 | `--keyword` |

### 搜索覆盖场景

| 大类 | 具体场景 |
|------|---------|
| **交通** | 国内/国际机票、火车票、接送机、租车、包车 |
| **住宿** | 酒店、民宿、客栈、机酒套餐 |
| **体验** | 景点门票、一日游、向导、定制游 |
| **活动** | 演唱会、体育赛事、演出、动漫展 |
| **服务** | 签证、旅行保险、SIM 卡、WiFi 租赁 |
| **旅行** | 邮轮、周末游、蜜月、亲子游、研学 |

### 显示能力

- Markdown 表格对比
- 图片展示（`![]({picUrl})`）
- 预订链接（`[Click to book]({jumpUrl})`）
- 平台提示（`systemMessage`）

## 四、技术评估

### CLI 实现 (@fly-ai/flyai-cli)

| 项目 | 详情 |
|------|------|
| **语言** | TypeScript |
| **运行时** | Node.js >= 18 |
| **入口** | `dist/flyai-bundle.cjs` (esbuild 打包混淆) |
| **唯一运行时依赖** | commander ^12.1.0 |
| **包大小** | ~68KB (解压 ~74KB) |
| **混淆** | JavaScript Obfuscator |

### API 通信

| 项目 | 详情 |
|------|------|
| **端点** | `https://flyai.open.fliggy.com/mcp` |
| **协议** | MCP (jsonrpc 2.0)，`tools/call` method |
| **Content-Type** | `application/json`, 也支持 `text/event-stream` (SSE) |
| **认证层** | HMAC-SHA256 签名 (ver=7) |
| **签名头** | `x-flyai-sign-ver`, `x-flyai-sign-alg`, `x-flyai-nonce`, `x-flyai-sign`, `x-flyai-ts` |
| **API Key** | `Authorization: Bearer <key>` |
| **设备指纹** | `x-ff-ctx` (gzip+加密的 base64，含 CPU/内存/平台/语言/deviceId) |
| **追踪** | `x-ttid: ai2c(sk.clawhub)`, `User-Agent: flyai-cli/1.0.6` |
| **超时** | 180 秒 |

### 认证机制

```
优先级：
1. FLYAI_API_KEY 环境变量
2. DEBUG_FLYAI_API_KEY 环境变量（调试用）
3. flyai config set FLYAI_API_KEY 写入本地 (~/.flyai/config.json)
4. 内置默认 API Key (sk-faRn8K...) → 体验模式
```

**体验模式特征**：返回结果完整但 `systemMessage` 提示 `"*当前为体验模式，部分搜索结果可能受限..."`。

**签名密钥**：`FLYAI_SIGN_SECRET` 环境变量控制，默认值硬编码在 CLI 中。

### 设备指纹

CLI 首次运行时在 `~/.flyai/device-id`（或系统临时目录）生成 UUID，SHA256 哈希后作为设备标识。每次请求附带加密的机器信息（CPU 核数、内存、平台、Node 版本、语言、时区等）。

## 五、OpenClaw 兼容性评估

### Skill 格式兼容性

| 特性 | 兼容 | 说明 |
|------|-----|------|
| SKILL.md 格式 | ✅ | 标准 frontmatter + Markdown body |
| `openclaw.priority` (90) | ✅ | 意图路由优先级 |
| `openclaw.intents` | ✅ | 8 种意图类型 |
| `openclaw.patterns` | ✅ | 18 组正则（含中文），意图匹配 |
| `openclaw.emoji` | ✅ | ✈ |
| `openclaw.requires.bins` | ✅ | node |
| ClawHub marketplace | ✅ | `clawhub install flyai` |
| `npx skills add` | ✅ | 标准安装方式 |
| Slash command | ✅ | `/flyai <command>` |

### 意图匹配模式（18 组，覆盖中英文）

- 英文：hotel/flight/attraction/visa/car rental/cruise/ticket/concert/trip plan/budget 搜索等
- 中文：`(搜索|查找|推荐|比较|预订|查询).*(酒店|机票|航班|景点|门票|签证|邮轮|租车|民宿)` 等
- 旅行场景：`(旅游|旅行|出行|度假|出差|蜜月|亲子游).*(规划|计划|攻略|推荐|搜索|安排)`

### 执行模型

- `agent.type: tool` — 作为工具型技能
- `agent.runtime: node` — Node.js 运行时
- `agent.context_isolation: execution` — 每次命令独立执行上下文
- `agent.parent_context_access: read-only` — 只读父上下文

## 六、实测结果

### 环境

- Node.js 24.11.1, npm 11.6.2
- 安装: `npm i -g @fly-ai/flyai-cli` (2 packages, 3s)

### 测试结果

#### 1. keyword-search（关键词搜索）

```bash
flyai keyword-search --query "Tokyo attractions"
```

✅ **成功**。返回 10 条东京景点（三丽鸥彩虹乐园、歌舞伎座、晴空塔等），含 `jumpUrl`、`picUrl`、`title`。systemMessage 提示体验模式。

#### 2. search-flight（机票搜索）

```bash
flyai search-flight --origin "Beijing" --destination "Shanghai" --dep-date 2026-06-15
```

✅ **成功**。返回 10 条航班（国航、厦航、中联航、吉祥、南航、东航、山航），票价 ¥330-¥600，含直飞和中转。

#### 3. search-hotel（酒店搜索）

```bash
flyai search-hotel --dest-name "杭州" --check-in-date 2026-06-15 --check-out-date 2026-06-17
```

✅ **成功**。返回杭州酒店列表（如家、索菲特等），含 `mainPic`、`detailUrl`、评分、价格。

Tokyo 酒店搜索返回 `"message": "empty"` — 体验模式国际酒店数据受限。

#### 4. search-train（火车票搜索）

```bash
flyai search-train --origin "北京" --destination "上海" --dep-date 2026-06-15
```

✅ **成功**。返回 G 字头高铁列车信息，含车次、座位等级、行程时间。

#### 5. ai-search（AI 语义搜索）

```bash
flyai ai-search --query "Tokyo best hotels near Shibuya"
```

✅ **成功**。返回 AI 生成的 Markdown 推荐文本，分豪华/高档/舒适三档，含预订链接和详细分析。

### 性能

| 命令 | 响应时间 |
|------|---------|
| keyword-search | ~1.5s |
| search-flight | ~1.2s |
| search-hotel | ~1.0s |
| search-train | ~1.3s |
| ai-search | ~12s (流式 SSE) |

### 免费额度

- **不需要注册**，内置 API Key 即可使用
- 体验模式 `systemMessage` 提示"部分搜索结果可能受限"
- 未发现明确的调用次数限制（测试期间连续 5 次调用均成功）
- 国际酒店搜索可能为空（东京酒店返回 empty，杭州正常）

## 七、安全性评估

| 风险 | 等级 | 说明 |
|------|------|------|
| 硬编码 API Key | MEDIUM | CLI bundle 内嵌默认 key，源码混淆但可通过 strings 提取 |
| 硬编码签名密钥 | MEDIUM | 同上 |
| 设备指纹采集 | LOW | 收集 CPU/内存/平台/语言/时区，用于反滥用，非 PII |
| 代码混淆 | LOW | 闭源保护，不影响使用 |
| MCP URL 可覆盖 | INFO | `DEBUG_FLYAI_MCP_URL` 环境变量可重定向端点 |

**建议**：如需正式使用，注册飞猪 AI 开放平台获取专属 API Key，通过 `FLYAI_API_KEY` 环境变量配置。

## 八、建议

### 适合场景

1. **国内旅行规划 Agent** — 机票/酒店/火车票/景点数据完整
2. **Claude Code 内快速差旅查询** — `/flyai keyword-search` 无需切换应用
3. **OpenClaw 自动化旅行助手** — 意图匹配自动触发
4. **MCP 技能开发参考** — 结构清晰的 MCP + CLI + Skill 三层架构

### 不适合场景

1. **国际旅行** — 体验模式国际数据不完整，需正式 API Key
2. **批量数据采集** — MCP 协议设计为单次查询，不适合大规模爬取
3. **实时库存预订** — 提供的是搜索和跳转链接，非直接下单

### 对知识库的价值

- 可作为 MCP Skill 开发的参考模板
- `skills/flyai/SKILL.md` 是 skill frontmatter 定义的优秀示例
- 意图匹配的正则表达式设计方法论值得提取

---

> 调研日期：2026-06-10 | CLI 版本：v1.0.16 | Skill 版本：v1.0.14