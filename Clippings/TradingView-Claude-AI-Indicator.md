---
title: 用Claude AI在10分钟内构建自定义TradingView指标
type: clipping
created: 2026-05-20
source: https://x.com/AlphaCartell/status/2051742600575463849
tags: [TradingView, Claude, Pine Script, AI交易, MCP]
---

## Build Your First Custom TradingView Indicator with Claude AI in Under 10 Minutes

> 原文作者：AlphaCartel · 2026-05-05 · 73.8万阅读 · 380赞 · 1068收藏

### 背景

作者的朋友之前花$300找开发者定制Pine Script指标。每次有新想法都要解释、等三天、拿到半对吗的东西、再解释、祈祷。然后作者给他展示了这个工作流——他11分钟就自己建好了第一个OI动量指标，免费。

### 为什么现在能行

过去的瓶颈：
- 学Pine Script本身（花几周）
- 付费找开发者（贵、慢、痛苦）
- 用别人的公开脚本（不匹配自己的交易优势）
- 放弃，用默认指标

AI辅助写代码时依然痛苦的"复制粘贴循环"：在ChatGPT生成代码→复制→粘贴到TradingView→编译报错→复制错误→粘贴回去→又报错→重复45分钟

### 突破点：AI原生工作流

三件事改变了游戏：
1. **TradingView Desktop** 可直接在Pine Editor中打开本地文件
2. **Claude Code** 可直接读写你电脑上的文件
3. **MCP协议** Claude通过Chrome DevTools Protocol直连你的TradingView Desktop

实际效果：Claude写代码→保存文件→TradingView即时编译→有错就读错误→修复→重新编译。你在图表上实时看到一切发生。**无复制粘贴，无摩擦。想法→图表。**

### 今天要构建的指标：Open Interest动量指标

- 9周期快EMA + 21周期慢EMA（Open Interest数据）
- 动态颜色：OI动量加速看涨→绿色，衰减/反转→红色
- 柱状图显示逐棒OI增量（新资金进入 vs 资金退出）
- 内置EMA交叉预警条件
- 完全可自定义输入

> 这不是玩具指标，这是机构级分析，由你自己在15分钟内构建完成。

### 一次性设置（5分钟）

**需要的工具：**
- TradingView Desktop（免费，必须是桌面版不是网页版）
- Claude Code（Anthropic CLI工具，需Pro或Max订阅）
- Node.js 18+（免费）
- Git（免费）

> 桌面版是Electron框架构建，底层跑Chromium，有内置调试通道让Claude直连你的实时图表。网页版不行。

**Step 1：安装TradingView MCP Server**
```bash
git clone https://github.com/anthropics/tradingview-mcp-server
```

**Step 2：配置Claude使用MCP Server**
编辑 `~/.claude/.mcp.json`，添加MCP server配置。

**Step 3：以调试模式启动TradingView**
必须用仓库脚本启动，不能用桌面快捷方式：
- Windows: `.\scripts\launch_tv_debug.bat`
- macOS: `./scripts/launch_tv_debug_mac.sh`

**Step 4：启动Claude Code**
在包含MCP配置的目录启动Claude Code，打开要用的图表，说："Build me..."

### 构建指标的提示词

（原文包含完整prompt模板）

### Verdict

> 如果你在TradingView上交易，不理解为什么这个工作流是突破，你还没有理解AI真正改变的是什么。
> 这不是"AI帮你写代码"——这是AI直接操作你的交易工具，消除工具与结果之间的每一秒延迟。你不需要成为开发者才能拥有定制交易优势了。
> 如果你今天不做这个设置，有人会做。他们会在你点击Web界面的图标时实时分析Open Interest数据。
> 这不是未来。这就是现在。