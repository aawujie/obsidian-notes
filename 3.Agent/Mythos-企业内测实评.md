---
title: "Anthropic Mythos 企业内测实评"
type: reference
created: 2026-06-10
updated: 2026-06-10
sources:
  - "https://x.com/zekramu/status/2064131568495677490"
tags:
  - agent
  - mythos
  - anthropic
  - security
  - model-review
---

## 原文信息

- 作者：zek (@zekramu) - 验证用户
- 时间：2026-06-08
- 点赞：2,631 | 转发：213 | 浏览：677,679

> **Anthropic Mythos 安全模型的企业试点用户一手测评。**

---

## 1. 成本

单个企业试点预期花费超 **100 万美元**。对比：作者公司上个月全公司所有推理费用才 200 万。

提供了一些免费 API token，但远不够覆盖实际使用。

## 2. Harness（安全笼套）

- **不是 Claude Code**，是一个独立的 harness，看起来像是 AI 生成的代码
- 重点在于"防止 Mythos 逃逸"，带一些简陋的安全 skills
- 一半护栏不生效
- 这就是传说中的 **Project Glasswing**
- 不确定公开发布时是否附带这个 harness
- 作者成功绕过了 harness 直接运行模型（"他们不太想让人这么干"）

## 3. 模型本身

### 优势
- 安全研究任务**远超 Opus / GPT-5.5 xhigh**
- 感觉是为安全任务专门微调的
- 通用编码一般，不是特别惊艳

### 局限
- 连他们的 Bazel 自定义构建工具都搞不定，需要人工先构建
- 不是"人类威胁"——但有钱 + 懂 harness 绕过 + 安全工程技能的人确实能做恶意的事

## 4. 实战结果

在他们多款产品中发现约 **800 个重大漏洞**。

> "产品是几乎这个 app 上每个人都间接用过的，可能少数人直接用过。"

足以重新考虑安全策略。

## 5. 结论

> "好模型。不是 Anthropic 想让你们相信的人类生存威胁，但确实是好模型。"
>
> 想跟 GPT-5.5 xhigh 做公平对比但拿不出 100 万美元。

---

## 与 Fable 5 对比

| 维度 | Mythos | Fable 5 |
|:---|:---|:---|
| 定位 | 安全审计 | 通用长任务 |
| Harness | 独立 Project Glasswing | CMA（托管沙箱） |
| 成本 | 企业百万级 | API 价格 |
| 强项 | 漏洞发现（800+ 重大漏洞） | 自纠正循环 + Memory |
| 编码 | 一般 | 结构性能提升 6x |