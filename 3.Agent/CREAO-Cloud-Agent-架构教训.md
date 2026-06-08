---
title: CREAO Cloud Agent 架构教训
date: 2026-06-06
tags: [Cloud Agent, 架构, 沙箱, 安全, CREAO, Peter Pang]
category: 投研日记
source: https://x.com/intuitiveml/status/2062699747224568212
---

# CREAO Cloud Agent 架构教训 — Peter Pang

> 原文: Peter Pang (@intuitiveml) 2026-06-05
> 翻译: 中英对照

---

## 原文

Most agent frameworks today assume a desktop. One user, one machine, one process. The agent runs while the laptop is open, writes to a local filesystem, holds API keys in environment variables, and dies when the terminal closes. When something breaks, the user retries. When the agent needs a package, pip install drops it into the user's Python. State, secrets, and lifecycle all sit inside one trusted boundary.

> 今天大多数 Agent 框架都假设桌面环境。一个用户、一台机器、一个进程。Agent 在笔记本开着的时候运行，写本地文件系统，把 API key 放在环境变量里，终端一关就死掉。出错了用户重试。需要包就 pip install 扔进用户的 Python 里。状态、密钥、生命周期全在一个可信边界内。

Cloud agent infrastructure has none of those luxuries.

> 云端 Agent 基础设施没有这些奢侈。

The agent runs on a sandbox that boots fresh, on hardware shared with strangers, triggered by callers the user never meets: a schedule, an HTTP request, another agent. The user is usually asleep when the run happens. The code inside the sandbox may be adversarial. The filesystem has to survive deployments. Credentials cannot live where the agent lives. Every guarantee the desktop gives you for free — persistence, identity, network trust, retry — has to be rebuilt as an explicit system.

> Agent 跑在一个每次重新启动的沙箱里，硬件跟陌生人共享，触发者用户从未见过：定时任务、HTTP 请求、另一个 Agent。运行时用户通常还在睡觉。沙箱里的代码可能是对抗性的。文件系统要经得起部署。凭证不能放在 Agent 住的地方。桌面端免费给你的每一个保证——持久化、身份、网络信任、重试——都必须重新构建为显式系统。

We spent the last few months tightening that layer at CREAO. Two lessons came out of it. If you have ever shipped a desktop agent and wondered what changes when it moves to the cloud, this is what changes.

> 我们在 CREAO 花了几个月加固这一层。得出两个教训。如果你曾交付过桌面 Agent，好奇它搬到云端会有什么变化，这就是变化。

---

## Lesson 1: Separate what changes slowly from what changes fast

> ## 教训一：把变得慢的和变得快的分开

On a desktop, the user's environment and the agent's runtime are the same thing, updated on the same cadence, by the same person. In the cloud, they are not.

> 桌面端，用户环境和 Agent 运行时是同一回事，由同一个人按同一节奏更新。云端不是。

An agent app accumulates state on the platform's side. A stock analyst installs matplotlib, downloads market data, writes charting scripts. That environment is the agent's muscle memory. We freeze it into a sandbox snapshot the moment the user is happy with it, and we hold that snapshot frozen until the user edits the environment again. Every run boots from the same image. Same packages, same files, same versions. Monday's run behaves like Friday's, because nothing underneath has moved.

> 一个 Agent 应用在平台侧积累状态。股票分析师装 matplotlib、下载市场数据、写绘图脚本。那个环境就是 Agent 的肌肉记忆。用户满意那一刻，我们把它冻结成沙箱快照，保持冻结直到用户再次编辑环境。每次运行从同一镜像启动。同样的包、同样的文件、同样的版本。周一的运行和周五一样，因为底层什么都没变。

This is the property that desktop frameworks cannot give you for free. A pip install six months ago resolves to different versions today. A cloud snapshot resolves to the same bytes forever. Reproducibility is something the platform owes the user, and a frozen snapshot is the cheapest way to deliver it.

> 这是桌面框架无法免费给你的属性。六个月前的 pip install 今天解析到不同版本。云端快照永远是同样的字节。可复现性是平台欠用户的，冻结快照是实现它的最便宜方式。

Then the coupling problem shows up.

> 然后耦合问题出现了。

The same image that freezes the user's environment also contains the runner code — the small harness library developed by us that manages the agent on each run. The user wants their environment to stay still. We want our runner to ship many times a day. One artifact, two opposite requirements.

> 冻结用户环境的同一镜像也包含了 runner 代码——我们开发的、管理每次 Agent 运行的小型框架库。用户希望环境不动。我们想一天发版多次。一个 artifact，两个相反的需求。

Our first fix was blunt. On boot, check whether the runner inside the snapshot matches the version we just deployed. If it doesn't, throw the snapshot away and boot from a clean template. It worked, and nobody complained. The damage only hit the first run after a deployment.

> 我们的第一个修复很粗暴。启动时检查快照里的 runner 是否匹配刚部署的版本。不匹配就扔掉快照，从干净模板启动。能用，没人抱怨。伤害只波及部署后的第一次运行。

Unattended runs killed that cover. A cron job at 9am Monday should not lose its environment because we deployed at 8:55. The contract we were quietly violating — "your environment is frozen until you change it"

> 无人值守运行摧毁了这个方案。周一早上 9 点的 cron 任务不应该因为我们 8:55 部署了而丢失环境。我们悄悄违背的契约——"你的环境在你改变它之前是冻结的"——暴露了。

The fix took us longer than it should have to see. The user's environment and the runner code change at completely different rates. The user edits their agent when they choose to. We deploy the platform many times a day. Treating them as one artifact forced a choice on every deployment: keep stale runner code, or destroy the frozen environment the user explicitly asked us to preserve.

> 这个修复我们花了比应该花的更久才想明白。用户环境和 runner 代码的变更速率完全不同。用户在自己选择的时候编辑 Agent。我们一天部署平台多次。把它们当成一个 artifact，每次部署都逼你二选一：保留过时的 runner 代码，还是毁掉用户明确要求我们保留的冻结环境。

The model we landed on borrows from how operating systems handle updates. The kernel changes. Your home directory does not. You do not wipe the disk to install a security patch.

> 我们最终采用的模型借鉴了操作系统处理更新的方式。内核变了。你的 home 目录不变。你不会为了装安全补丁而格式化硬盘。

We drew the same boundary. The sandbox boots from the user's frozen snapshot, untouched. Then we hot-swap only the runner. The sequence:

> 我们画了同样的边界。沙箱从用户冻结快照启动，不动它。然后只热替换 runner。步骤：

1. Stage the new runner in a temp directory inside the sandbox.
2. Validate it with node --check so any syntax error is caught before we touch anything live.
3. Atomically swap it in: unlock the immutable flag on the old runner, copy the new one over, re-lock with chattr +i, then hide the chattr binary itself so sandbox code cannot reverse the lock.
4. Purge V8's compile cache (/home/user/.cache/v8-compile-cache/*) so the new file actually loads instead of running stale bytecode.

> 1. 把新 runner 放到沙箱内的临时目录。
> 2. 用 `node --check` 校验，确保在触碰任何运行中代码之前捕获语法错误。
> 3. 原子替换：解锁旧 runner 的不可变标记，复制新的进去，用 `chattr +i` 重新锁定，然后把 `chattr` 二进制本身藏起来，防止沙箱代码反向解锁。
> 4. 清除 V8 编译缓存（`/home/user/.cache/v8-compile-cache/*`），确保新文件真正加载，而不是跑过时的字节码。

If any step fails, kill the sandbox and retry with a fresh one. No half-upgraded state ever runs an agent.

> 任何一步失败，杀沙箱，用新沙箱重试。从不给 Agent 跑半升级状态。

The whole swap takes about 300 milliseconds. We re-snapshot after a successful run only when the runner code was swapped, baking the updated code into the user's image so the next run skips the swap entirely. Platform deployments never discard the user's state; they fold the new runner into it. The user's packages, files, and customizations carry forward unchanged.

> 整个替换约 300 毫秒。只在 runner 代码被替换后才在成功运行后重新快照，把更新代码烤进用户镜像，下次运行直接跳过替换。平台部署从不丢弃用户状态；它们把新 runner 折叠进去。用户的包、文件、定制原封不动向前推进。

If you take one thing from this lesson, it is the diagnostic question. For anything you persist in a cloud platform, ask: who controls the cadence of change on this artifact? If the user and the platform both own it, you will eventually pay for the coupling. Split the artifact along the ownership boundary and let each side update on its own clock.

> 如果你从这课只带走一件事，就是那个诊断问题。对你在云平台上持久化的任何东西，问：谁控制这个 artifact 的变更节奏？如果用户和平台都拥有它，你迟早要为耦合付代价。沿着所有权边界拆分 artifact，让双方按自己的时钟更新。

---

## Lesson 2: Keep secrets out of the execution boundary

> ## 教训二：密钥永远不进入执行边界

This is the lesson that separates cloud agent infrastructure from everything else.

> 这是把云端 Agent 基础设施和所有其他东西区分开的教训。

A desktop agent runs as the user. It uses the user's keys, on the user's machine, against the user's network. A cloud agent runs as nobody, on shared hardware, against the open internet, executing code an LLM wrote from a prompt that may have been adversarial. The security model has to assume the code inside the sandbox is already compromised, not hope against it.

> 桌面 Agent 以用户身份运行。用用户的 key，在用户机器上，对着用户网络。云端 Agent 以 nobody 身份运行，在共享硬件上，对着公网，执行 LLM 根据可能对抗性的 prompt 写出的代码。安全模型必须假设沙箱内代码已经沦陷，而不是希望它没沦陷。

The rule we hold is simple. No long-lived credential ever lives inside the sandbox.

> 我们遵守的规则很简单。任何长期凭证永远不进入沙箱。

When an agent needs to call an authenticated service — Slack, GitHub, the user's own API — it does not hold the token. It sends a local HTTP request to an API bridge running outside the sandbox. The bridge attaches the OAuth token on the host side and forwards the call. The response comes back without the token ever entering the sandbox's memory or environment.

> 当 Agent 需要调用认证服务——Slack、GitHub、用户自己的 API——它不持有 token。它发一个本地 HTTP 请求到沙箱外的 API 桥接。桥接在宿主侧挂 OAuth token 并转发调用。响应回来，token 从未进入沙箱的内存或环境。

The interesting part is how the bridge knows the sandbox is allowed to ask. Two checks, layered on purpose.

> 有趣的部分是桥接如何知道沙箱有权限请求。两层检查，有意分层。

First, IP allowlist. The bridge only accepts connections from the internal network range our sandbox hosts live on. A call from anywhere else — a developer laptop, a leaked URL, the public internet — is dropped at the network layer before any application code runs. This pins the bridge to one piece of physical infrastructure and makes it useless to anyone outside it.

> 第一，IP 白名单。桥接只接受来自沙箱主机所在内网段的连接。任何其他来源的调用——开发者笔记本、泄露的 URL、公网——在网络层就被丢弃，任何应用代码都还没跑。这把桥接钉在一块物理基础设施上，对任何外部人员无意义。

Second, a short-lived JWT minted per run. When a sandbox boots, the platform signs a token scoped to that specific run: which user, which app, which session, with an expiry that covers the run window and nothing more. The sandbox presents it on every bridge call. The bridge verifies the signature, checks the expiry, and only then resolves the user's stored credentials and attaches them server-side. If a sandbox is hijacked, the attacker inherits a token that dies with the run and only authorizes calls scoped to that one session. There is no master credential to steal.

> 第二，每次运行签发的短生命周期 JWT。沙箱启动时，平台签发一个范围限定到该次运行的 token：哪个用户、哪个应用、哪个会话，过期时间覆盖运行窗口，绝不多给。沙箱每次桥接调用都出示它。桥接验证签名、检查过期，然后才解析用户存储的凭证并在服务端挂载。如果沙箱被劫持，攻击者继承的 token 随运行一起死亡，只授权那一个会话范围的调用。没有主凭证可偷。

The same bridge carries billing deductions, logs, and metrics out, so it is the one interface that crosses the sandbox boundary in either direction. Everything else inside the sandbox is treated as compromised by default.

> 同一个桥接承载计费扣减、日志和指标输出，所以它是跨越沙箱边界的唯一接口，双向皆如此。沙箱内所有其他东西默认视为已沦陷。

If a prompt injection convinces an agent to dump process.env to a webhook tomorrow, the attacker gets a short-lived JWT that only works from inside our network and expires with the run. That property is what lets us run untrusted user code on shared infrastructure without losing sleep.

> 如果明天 prompt injection 说服 Agent 把 `process.env` dump 到某个 webhook，攻击者拿到的是一个只在我们的内网有效、本次运行结束就过期的短生命 JWT。这个属性让我们能在共享基础设施上跑不受信任的用户代码，还能睡得着觉。

---

## The pattern underneath

> ## 底层的模式

Reliable, secure cloud agent infrastructure is not a novel system. It is a few properties held without exception:

> 可靠、安全的云端 Agent 基础设施不是什么新奇系统。它只是几条无例外坚守的属性：

- State lives in the sandbox, frozen until the user changes it.
- Code is hot-swappable, independent of state.
- Credentials live host-side, never inside the agent.
- One execution pipeline serves every caller, whether the trigger is a human, a scheduler, or another piece of software.

> - 状态住在沙箱里，冻结直到用户改变它。
> - 代码可热替换，与状态独立。
> - 凭证住在宿主侧，永远不进入 Agent。
> - 一条执行管道服务所有调用者，无论触发者是人、定时器、还是另一段软件。

That last property is the punchline of the whole design. One executeAgent function handles UI clicks, scheduled runs, and API calls. The billing system, the credit deduction logs, the observability signals — all identical regardless of whether a human clicked Run, a cron fired, or a script called the API. Adding a new trigger surface is a routing change, not an architecture change. The agent itself does not know or care who pulled the trigger.

> 最后一条属性是整个设计的 punchline。一个 `executeAgent` 函数处理 UI 点击、定时运行和 API 调用。计费系统、积分扣减日志、可观测信号——全部一致，不管是一个人点了 Run，还是 cron 触发了，还是脚本调了 API。新增一个触发表面是路由变更，不是架构变更。Agent 本身不知道也不在乎谁扣动了扳机。

That is what desktop frameworks cannot give you, and what makes the cloud version worth building. An agent on a laptop is bound to the laptop. An agent in the cloud is a function the rest of your stack can call. The user writes it once. The platform makes it survive deployments, run safely on shared hardware, and accept callers the user never anticipated.

> 这就是桌面框架给不了你的，也是云端版本值得构建的原因。笔记本上的 Agent 绑在笔记本上。云端的 Agent 是你整个技术栈其他部分可以调用的一个函数。用户写一次。平台让它活过部署、在共享硬件上安全运行、接受用户从未预料到的调用者。

An agent is a function with a natural language interface. Its implementation belongs to the user. Its trigger surface, its runtime, its security boundary belong to the platform. The discipline is to build the layers so each evolves on its own clock, and to spend the time finding the cracks between systems before someone else does.

> Agent 是一个自然语言界面的函数。它的实现属于用户。它的触发表面、运行时、安全边界属于平台。纪律是：把各层构建成各自按自己的时钟演进，并花时间在别人之前找到系统间的裂缝。

That is what makes the next surface cheap to ship, and safe to ship.

> 这就是让下一个触发表面既便宜、又安全上线的关键。