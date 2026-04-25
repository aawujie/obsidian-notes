---
title: OpenClaw 微信 Markdown 渲染配置教程
type: concept
created: 2026-04-25
updated: 2026-04-25
tags: [openclaw, weixin, markdown, 配置]
---

# OpenClaw 微信 Markdown 渲染配置教程

## 问题

微信 iLink 私聊中，机器人回复的表格和代码块有时能正确显示，有时变成纯文本。

## 微信 iLink 的 Markdown 渲染能力

微信 iLink 协议**没有 "markdown" 消息类型**——所有文本都是纯文本（`item_list: [{ type: 1, text_item: { text } }]`）。但客户端**会就地渲染一部分 markdown 语法**：

| 语法                       | 微信是否渲染 | StreamingMarkdownFilter 行为 |           |
| :----------------------- | :----- | :------------------------- | --------- |
| ` ``` ` 代码块              | ✅      | **保留**围栏，逐字符透传             |           |
| ` ` ` 行内代码               | ✅      | **保留**反引号                  |           |
| `                        | ` 表格   | ✅                          | **保留**管道符 |
| `**粗体**`                 | ✅      | **保留**双星号                  |           |
| `*italic*`（英文）           | ✅      | **保留**单星号                  |           |
| `*中文斜体*`                 | ❌      | **脱掉**星号                   |           |
| `##### H5` / `###### H6` | ❌      | **脱掉** `#####`             |           |
| `![alt](url)` 图片         | ❌      | **整段删除**                   |           |
| `---` 水平线                | ✅      | **保留**                     |           |

## 根因

之前安装的 `openclaw-weixin` 版本是 **2.0.1**，`src/messaging/` 下的源码被手动修改过：

- **删除**了官方的 `markdown-filter.ts`（`StreamingMarkdownFilter` 流式状态机）
- **添加**了 `markdownToPlainText` 函数，用简单正则无条件拆掉代码块围栏和表格管道符

```typescript
// 2.0.1 被改过的 send.ts — 拆掉所有格式
result = result.replace(/```[^\n]*\n?([\s\S]*?)```/g, (_, code) => code.trim());  // 代码块围栏去掉
result = result.replace(/^\|[\s:|-]+\|$/gm, "");  // 表格分隔行去掉
result = result.replace(/^\|(.+)\|$/gm, (_, inner) =>
  inner.split("|").map(cell => cell.trim()).join("  "),  // 管道符变成空格
);
```

结果：微信收到的是纯文本，客户端无法渲染代码块和表格样式。

## 解决方案：升级到官方 v2.1.10

官方 v2.1.10 用 `StreamingMarkdownFilter` 处理回复文本——一个字符级流式状态机，**保留**微信能渲染的格式（代码块、表格、粗体等），**只剥离**微信不渲染的（中文斜体、H5/H6、图片）。无需任何额外配置。

### 升级步骤

```bash
cd ~/.openclaw/extensions/openclaw-weixin

# 1. 安装最新包
npm install @tencent-weixin/openclaw-weixin@2.1.10 --force

# 2. 用官方源码覆盖被改过的本地文件
cp -r node_modules/@tencent-weixin/openclaw-weixin/src/* src/

# 3. 清除 jiti 缓存（否则可能加载旧编译结果）
rm -rf node_modules/.cache/jiti/

# 4. 重启 Gateway
systemctl --user restart openclaw-gateway
```

### 清理 openclaw.json

升级后不需要 `markdown` 配置项，`StreamingMarkdownFilter` 默认保留所有微信能渲染的格式。把之前的配置清掉：

```json
// 之前（不需要了）
"channels": {
  "openclaw-weixin": {
    "accounts": {},
    "markdown": { "tables": "on", "codeBlocks": "on" }
  }
}

// 之后（干净）
"channels": {
  "openclaw-weixin": {
    "accounts": {}
  }
}
```

## 原理说明

微信的消息发送流程：

```
模型输出 → reply pipeline → payload.text → StreamingMarkdownFilter → 过滤后文本 → 微信API
```

`StreamingMarkdownFilter` 是最后一道处理，决定了微信实际收到的文本。它逐字符扫描，用状态机（`sol` / `body` / `fence` / `inline` 四个状态）判断当前处于什么语法结构，**保留**代码块围栏和表格管道符，**脱掉**中文斜体星号和图片标签。

### 为什么自建插件没用

之前调试过 OpenClaw 的各种 plugin hook：

| Hook | 对微信格式显示有用？ | 原因 |
|:-----|:-------------------|:-----|
| `before_message_write` | 否 | 只改 session transcript，微信发送读的是 payload.text，不走 session |
| `before_dispatch` | 否 | 只对 inbound（用户发的消息）触发，不对 agent 回复触发 |
| `message_sending` | 否 | 微信 agent 回复不走这个 hook |
| `reply_dispatch` | 否 | body 只有 2 字节，不是实际消息内容 |
| `llm_output` | 否 | 只读 hook（返回 void），无法修改内容 |

所以自建的 `formatted-message` 插件对微信格式显示没有贡献——插件改的是 session transcript，微信发送读的是 reply payload，两个独立的数据流。

### v2.1.10 新增的 outbound-hooks

v2.1.10 新增了 `outbound-hooks.ts`，提供了 `applyWeixinMessageSendingHook` 和 `emitWeixinMessageSent`。这意味着 v2.1.10 **支持 `message_sending` hook** 了——如果以后需要拦截或修改发送内容，这个 hook 现在能生效。

## 版本对比

| 版本 | Markdown 处理 | 代码块 | 表格 | 行内代码 | message_sending hook |
|:-----|:------------|:------|:----|:-------|:-------------------|
| 2.0.1（被改过） | `markdownToPlainText` 正则 | ❌ 拆掉围栏 | ❌ 拆掉管道符 | ❌ 去掉反引号 | ❌ |
| 2.1.10（官方） | `StreamingMarkdownFilter` 状态机 | ✅ 保留 | ✅ 保留 | ✅ 保留 | ✅ 新增支持 |

## 验证

从微信发消息让机器人回复：
1. 带表格的内容 → 确认表格有管道符、显示正常
2. 带代码块的内容 → 确认代码块有围栏、有代码块样式
3. 带行内代码的内容 → 确认反引号显示、有行内代码样式
4. 带中文斜体 `*中文*` → 确认星号被脱掉，只显示文字