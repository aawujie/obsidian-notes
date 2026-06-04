---
title: How To Be A World-Class Agentic Engineer
type: reading-note
created: 2026-06-01
updated: 2026-06-01
sources:
  - https://x.com/systematicls/status/2028814227004395561
tags:
  - Agentic Engineering
  - Claude Code
  - AI Agent
  - 工程方法论
---

> 来源：sysls (@systematicls)，2026-03-03
> 8771赞 1001转 376万查看
> 核心观点：**少即是多。你不需要任何外部依赖，理解几个基本原则就够了。**

---

## 引言：为什么你感觉到瓶颈

你每天都在用 Claude 和 Codex CLI，偶尔看到它做一些极其愚蠢的事，你无法理解为什么有人能造出虚拟火箭而你连两块石头都叠不起来。

你以为问题出在 harness、插件、终端。你用了 beads、opencode、zep，CLAUDE.md 写了 26000 行。但无论怎么努力，你始终无法接近天堂，而别人却在和天使嬉戏。

**答案：你不理解 Agentic Engineering 的基本原则。**

> 作者背景：从 agent 还几乎不会写代码的时代就开始用，试过所有包、所有 harness、所有范式。做过生产级的 agentic 工厂（信号系统、基础设施、数据管道）。现在只用最基本的 CLI，却做出了最突破性的工作。

---

## 核心原则 1：少即是多

### 前沿公司正在飞奔

基础模型公司在一代代狂奔，每一代 agent 智能的提升都会改变你的工作方式。几代之前，你在 CLAUDE.md 里写"先读 READ_THIS_BEFORE_DOING_ANYTHING.md"，它有 50% 概率直接无视你。现在，复杂嵌套指令都能遵循。

**这意味着：每一代新 agent 都会迫使你重新思考什么是"最优"。所以少即是多。**

### 依赖越多，锁死越深

<span style="color:rgb(255, 77, 77)">当你使用大量第三方库和 harness，你把自己锁死在了一个"解决方案"里——而这个解决方案解决的问题，可能在下一代模型里根本不存在。</span>

### 最重要的事实

> 前沿公司员工是 agent 的最大用户，无限 token 预算，最新模型。如果真有一个问题存在且有好的解决方案，前沿公司会是那解决方案的最大用户。然后他们会把那解决方案**直接整合进产品**。

看看 skills、memory harness、subagents——它们都始于<span style="color:rgb(255, 77, 77)">"对真实问题的解决方案"</span>，<span style="color:rgb(255, 77, 77)">被验证有效后，被整合进了基础产品。</span>

> 所以，<span style="color:rgb(195, 117, 255)">如果某个东西真的是突破性的，它迟早会被整合进基础产品。<b>你不需要安装任何外部依赖来做最好的工作。</b></span>

---

## 核心原则 2：Context Is Everything

> 上下文就是一切。你引入一千个插件和外部依赖，就会遭遇**上下文膨胀**——你的 agent 被太多信息淹没了。

**例子：**
"帮我写个 Python 猜词游戏"——简单。
但 agent 在读什么？"管理内存"的笔记，71 个 session 前的挂起屏幕，无数条"记得写笔记"的规则。这和猜词游戏有什么关系？

<span style="color:rgb(255, 77, 77)"><b>你要给 agent 恰好完成任务所需的信息，仅此而已。</b></span>

<span style="color:rgb(195, 117, 255)">你对上下文的控制越好，agent 表现越好。一旦引入花里胡哨的记忆系统、插件、命名糟糕的 skills</span>，你就是在让 agent 同时学习造炸弹和烤蛋糕，而你想要它写的只是一首关于红杉林的小诗。

---

## 核心原则 3：精准描述实现

### 分离研究与实现

<span style="color:rgb(255, 77, 77)"><b>模糊指令：</b></span> "去建一个认证系统"
→ agent 需要研究什么是认证系统？有哪些选项？优劣？<span style="color:rgb(255, 77, 77)">搜遍网络，上下文被各种实现细节填满。到真正实现时，已经混淆了，开始幻觉。<br></span>
<span style="color:rgb(255, 77, 77)"><b>精准指令：</b></span> "实现 JWT 认证，bcrypt-12 密码哈希，refresh token 轮换，7天过期"
→ agent 不需要研究其他方案，上下文全是实现细节。

### 如果你<span style="color:rgb(255, 77, 77)">不知道实现细节</span>？

1. 创建一个<span style="color:rgb(255, 77, 77)"><b>研究任务</b></span>，让 agent 研究各种实现方案
2. 你自己决定（或让 agent 决定）<span style="color:rgb(255, 77, 77)">用哪个方案</span>
3. 用一个<span style="color:rgb(255, 77, 77)"><b>全新上下文</b></span>的 agent 去实现

> 一旦你开始这样思考，你会发现工作流中 agent 被不必要的上下文污染的地方。你可以在 agentic 工作流中设置"墙"，只让 agent 看到完成任务所需的具体上下文。

记住：你有一个非常聪明、知识渊博的团队成员，知道宇宙中所有类型的球。但除非你告诉它你要设计一个舞池，它会一直跟你讲球形物体的各种好处。

---

## 核心原则 4：理解谄媚（Sycophancy）的设计局限

> 没人会用一款天天骂你、告诉你你错了、完全无视你指令的产品。所以<span style="color:rgb(255, 77, 77)">这些 agent 被设计成尽可能同意你、做你想让它做的事。</span>

### 问题

你说"帮我在代码库里找个 bug"——它一定会找到 bug，**哪怕它需要自己造一个**。因为它极度想遵循你的指令。

大多数人抱怨 LLM 幻觉，却没意识到<b>自己才是问题</b>。你问什么，它就会给什么——哪怕需要稍微扭曲一下事实。

### 解决方案：<span style="color:rgb(255, 77, 77)">中性 Prompt<br></span>
不要说"找 bug"，说：
> "搜索数据库，追踪每个组件的逻辑，报告所有发现。"

<span style="color:rgb(255, 77, 77)">中性 prompt 有时会发现 bug</span>，<span style="color:rgb(255, 77, 77)">有时只是如实陈述代码如何运行</span>。但它<span style="color:rgb(255, 77, 77)">不会把 agent 偏向"一定存在 bug"的方向。</span>

### 进阶：利用谄媚

<span style="color:rgb(195, 117, 255)">用三个 agent 互相制衡：</span>

| Agent       | 角色    | 指令                           | 产出                                                               |
| :---------- | :---- | :--------------------------- | :--------------------------------------------------------------- |
| Bug-Finder  | 找 bug | +1低影响/+5中等/+10严重             | 所有可能 bug 的超集（<span style="color:rgb(195, 117, 255)">包括误报</span>） |
| Adversarial | 反驳    | 驳倒一个 bug 得该 bug 的分数，冤假错案扣 2x | 真实 bug 的子集                                                       |
| Referee     | 裁判    | "我有正确答案"，答对+1 答错-1           | 高保真最终判断                                                          |

> 这利用了每个 agent 被硬编码的欲望——**想要取悦你**。

---

## 核心原则 5：<span style="color:rgb(255, 77, 77)">如何判断什么有用</span>

> <span style="color:rgb(195, 117, 255)">如果 OpenAI 和 Claude 都实现了它</span>，或者收购了实现它的公司——<span style="color:rgb(195, 117, 255)">那它大概率有用。</span>

例子：
- Skills → 现在到处都有，已是官方文档
- Memory、Voices、Remote Work → Claude 直接加了
- Planning → 从社区发现有效 → 变成核心功能
- Stop-hooks → 曾经超级有用 → Codex 5.2 一出就消失了

> 你不需要"保持更新"。<span style="color:rgb(195, 117, 255)"><b>只需要偶尔更新你的 CLI 工具，读一下新增了什么功能。</b></span> 这就够了。

---

## 核心原则 6：Compaction、上下文与假设

agent 有时像世界上最聪明的东西，有时又蠢得令人发指。区别在于：<span style="color:rgb(255, 77, 77)"><b>agent 是否被迫做了假设或 "填补空白"</b></span>。

> 截至目前，<span style="color:rgb(255, 77, 77)">agent 在"连接点"、"填补空白"、"做假设"方面仍然糟糕透顶。</span>一旦它们开始假设，立刻就能看出它们走上了歧途。

**最重要的 CLAUDE.md 规则：**
- <span style="color:rgb(195, 117, 255)">告诉 agent 在 compaction 后重读任务计划</span>
- 重读与任务相关的文件
- 在继续之前重新建立上下文

---

## 核心原则 7：让 agent 知道任务何时结束

人类对"任务完成"有很强的直觉。agent 最大的问题是：<span style="color:rgb(255, 77, 77)"><b>知道怎么开始，不知道怎么结束。</b></span> 这导致 agent 实现一堆 stub 然后交差。

### 解决方案：<span style="color:rgb(255, 77, 77)">测试 + 合约<br></span>
> 测试是 agent 的极好里程碑——它们是确定性的，你可以设定清晰的期望。

**"{TASK}_CONTRACT.md"**：<span style="color:rgb(255, 77, 77)">规定任务可以结束之前必须完成什么</span>。
- 测试必须全部通过
- 不允许修改测试
- 截图 + 验证（设计或行为）

> 当 agent 可以通过截图验证"设计是否符合预期"，它就可以迭代，直到达到你想要的视觉效果，而不是第一次尝试就停下。

---

## 核心原则 8：长期运行的 Agent

> 24 小时连续运行的 agent 并不可取——<span style="color:rgb(255, 77, 77)">它强制引入了上下文膨胀</span>，无关的合同内容会污染 session。

**更好的方式：一个合同 = 一个 session。**

```
编排层 → 创建新合同 → 创建新 session → 执行合同 → 验证 → 完成
```

> 这会彻底改变你的 agentic 体验。

---

## 核心原则 9：迭代，迭代，迭代

### Rules

如果不想让 agent 做某件事，写成规则。在 CLAUDE.md 里告诉 agent 读规则。

```
CLAUDE.md 应该是逻辑嵌套的目录，只包含 IF-ELSE：
- 如果编程 → 读 coding-rules.MD
- 如果写测试 → 读 coding-test-rules.MD
- 如果测试失败 → 读 coding-test-failing-rules.MD
```

> 看到 agent 做了你不认可的事 → 加到规则里 → 告诉 agent 下次做之前先读规则 → 它就不会再犯了。

### Skills

Skills 像规则，但更适合编码"配方"——做某件事的具体方法。

> 如果你不知道 agent 会怎么解决一个问题，让它先研究，然后**写成 skill**。你可以在它真正遇到那个问题之前审查和修正。

### Rules 和 Skills 的维护

你会不断添加 rules 和 skills。这是给 agent 注入个性、记忆和偏好的方式。**除此之外几乎都是过度设计。**

然后 agent 会感觉像魔法——"按你的方式做事"。

然后性能又下降了。

**为什么？** rules 和 skills 越来越多，开始互相矛盾，或者上下文膨胀。

**解决方案：** 清理。让 agent 去做一次"spa day"，合并 rules 和 skills，消除矛盾，询问你更新后的偏好。

> 就这么简单。保持简单，用 rules 和 skills，把 CLAUDE.md 当作目录，**对上下文和设计限制保持宗教般的警惕**。

---

## 结论：Own The Outcome

> 今天没有完美的 agent。你可以把大部分设计和实现交给 agent，但**你必须对结果负责**。

从裸 CLI 开始，忘记复杂的结构和 harness。不断迭代，用 rules 和 skills 编码偏好，保持上下文干净。

**然后享受和未来的玩具玩耍（同时用它们做正经事）。**