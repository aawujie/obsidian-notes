---
notion-id: 24f78d23-e296-81f7-b045-eb4e2e91609a
cover: "[[imgs/在Amazon Bedrock上用Claude及Strands Agent构建AI Agent实战全解.jpeg]]"
Date: 2025-08-15
Last edited time: 2025-08-15T00:49:00
Tags: []
Link: https://youtu.be/8gTpgWru0Wg?si=QPpLNUjU6F1LThAG
pic: https://img.youtube.com/vi/8gTpgWru0Wg/sddefault.jpg
Verification: unverified
Owner:
  - AI generation
---
# 1. Metadata

- Title: 在 Amazon Bedrock 上用 Claude 构建 AI Agent 的实战演示
- Author: Dwan Lightoot / Banjo / Suman DNA（演讲者与演示者合集转写）

# 2. Overview

本视频展示如何在 Amazon Bedrock（亚马逊 Bedrock）上利用 Claude 系列模型和 AWS 新发布的开源 SDK Strands Agent 构建“agentic”（自治）AI 系统。内容从概念讲解（什么是 agent）、介绍 Bedrock 提供的模型与安全保障，到现场动手 workshop：配置预置环境、安装 Strands、使用示例（天气查询 + 计词工具）、MCP（Model Connector/Plugin，视频中称 MCP server）集成用于生成 AWS 架构图、再到借助 Cloud Code 在 VS Code 内自动生成并修改 CDK（Cloud Development Kit）Agent。结论是：借助 Bedrock、Claude 与 Strands，开发者可以用极少的样板代码快速构建多步骤推理、计划与执行的自治工作流，并能通过 MCP 提供外部知识或工具能力以扩展模型能力。

# 3. 按照主题来梳理

## 3.1 什么是 Amazon Bedrock、Agent 与本次目标

- Amazon Bedrock 是一个“fully managed service”（全托管服务），通过统一 API 暴露多款基础模型（foundational models），并提供模型选择、guard rails（防护/约束）、以及“enterprise-grade”安全性（企业级安全性）作为默认配置。视频强调 Bedrock 的目标是让开发者不仅能“构建”AI 应用，也能“在全球范围内扩展”这些应用。
- 在 AWS 的定义中，agent 是一种“autonomous system”（自治系统），能够像人类那样进行推理（reason）、制定计划（plan）、并分多步执行以完成目标。具体流程包括：接受一个任务、识别高层目标、将目标拆解成步骤、对每个步骤采取行动、评估步骤结果并据此决定下一步，直至完成目标。视频反复以此定义来说明后续 Strands Agent 的设计理念和 demo 的行为预期。
- 本次 workshop 的目标与结构：先通过若干幻灯片让参与者在概念上就位，然后进入一个“hands-on keyboard event”（实操工作坊）。AWS 提供了预配置的 AWS 账户与 VS Code server，使参与者能在浏览器里直接操作而无需本地安装。演示者将先讲解 Bedrock 的模型启用方式与基本概念，再展示 Strands Agent 的安装与示例，随后演示如何把 MCP servers（模型连接器/插件）整合进 agent 来获取外部文档或工具能力，最后示范如何用 Cloud Code 在 VS Code 中生成或改写基于 Strands 的 CDK Agent。视频多次强调该套开放源码项目刚发布（只有几天），鼓励社区贡献（star、PR、issue 等）。

## 3.2 Strands Agent：开源 SDK 的理念与架构

- Strands Agent（视频称 strands agent）是 AWS 开源的一套用于构建 agentic 应用的 SDK，其设计哲学是“简洁”：只需要三样东西——models（模型）、tools（工具）、prompt（提示词），没有多余的脚手架或复杂的守护机制（no heavy scaffolding）。开发者负责提供必要的系统背景（system prompt）、希望使用的模型（例如视频中默认使用 Claude 3.7 / 3.5），以及工具集合；其余由模型在运行时负责推理和决定细节。这个设计假设“当下的 LLM 已经足够强大”，可以信任模型来做较多的推理与接口调用决策。
- 架构层面是直观的三要素流程：用户 craft 一个 prompt（或问题/目标）并交给 Strands Agent；Agent 根据 system prompt 与可用 tools 与模型生成一个执行计划；在执行时，Agent 通过内置或自定义工具（例如 HTTP request、word count）来完成各步骤，并对中间结果进行评估与迭代。Strands 提供了内置工具（HTTP 请求工具等）并允许用简单的装饰器（tool decorator）来定义自定义工具，使开发者仅需撰写函数并返回结果即可暴露为可被 agent 使用的工具。
- 部署与集成：Strands 支持在本地测试环境以及在 AWS 生产环境（EC2、Lambda、ECS 等）中部署。与 Bedrock 的集成使得在使用 Claude（或 Bedrock 中其他模型）时，无需额外的第三方密钥管理，模型调用可直接通过 Bedrock 的配置（如设置 CLOUD_CODE 环境变量）进行。

## 3.3 现场工作坊准备与 Bedrock 模型启用步骤

- AWS 提供预配置账户与 VS Code server：参加者无需使用自己的 AWS 账户，主办方已提前为每位参与者配置好资源（包括 Workstation participant role 和 VS Code server），参与者通过浏览器打开指定 URL、使用一次性密码登录后即可进入预置环境。演示者解释“这是本次 workshop 最难的部分”，建议遇到问题随时提问。
- 在 Bedrock 控制台中启用模型：进入 Amazon Bedrock 控制台后，需要在“model access”或“modify model access”处选择并启用希望使用的模型。演示中提到想用 Claude v7、3.5 hiq 与 3.5 sonnet，但某些账号尚未启用新模型，只能回退使用较旧模型。强调该操作需要等待批准或确认（submit request），并说明 workshop 的代码开源，参与者可在会后按相同步骤在自己的环境中执行。
- 安装 Strands 与配置 Cloud Code：在工作区的终端执行 pip install strands_agent 与 strands_agent_tools（视频中用 pip install strand agents 与 strand agent tools 的口语表述），即可安装 Strands 核心 SDK 及工具集。若使用 Claude via Bedrock（cloud code），可以通过导出环境变量（export CLOUD_CODE=...，视频中略去具体值）使 Strands 在调用模型时通过 Bedrock 的集成路径进行认证与请求，从而省去单独签名或 API 密钥的管理。演示者还在 VS Code 中打开 Cloud Code 插件并用“research preview”或推荐设置来快速开始。

## 3.4 示例一：天气查询 + 词数统计（weather + word count agent）详解

- 目标与思路：第一个实作性练习是构建一个简单 agent，任务是“获取某地天气并统计返回文本的词数”。该示例旨在演示如何把内置的 HTTP 请求工具和自定义的 word count 工具组合，展示 Strands 通过工具调用完成多步骤任务的能力。系统 prompt 明确指示 agent 去特定 API（示例中直接给出 gov 的天气 API URL，且不需要 API key）抓取天气数据，并以人类可读的方式呈现。
- 代码结构与关键点：核心文件有 system prompt（用来约束 agent 行为）、模型选择（示例中切换为 Claude 3.5 以提速）、tools 定义（内置 HTTP request 与一个用 @tool 装饰器简单暴露的 word_count 函数）。演示者强调“tool decorator”把一个普通函数变为 agent 的可调用工具，减少开发者在工具包装上的样板代码。整个 agent 流程由 Strands 框架处理：模型能理解如何解析“San Francisco”的经纬度/邮编并将其传入天气 API，说明模型在理解 API 参数填充方面承担了部分工作，而不是开发者手工构造每个字段。
- 运行与输出：运行后，agent 首先通过 HTTP 请求工具获取 San Francisco 的天气摘要（示例结果包含温度、晴天、风向等），随后调用 word count 工具返回文本长度（示例中 110 words）。整个实现仅用约 40 行代码，展示了 Strands 在组合多工具、进行跨步骤执行与评估时的简洁性与高效性。演示中也回答了关于“如何传递经纬度/邮编”与“自定义工具数量”的提问，说明模型会决定如何使用工具提供的接口，而 Strands 支持既有内置工具也可用极少代码定义任意自定义工具。

## 3.5 示例二：MCP servers（文档与图表）集成与生成 AWS 架构图

- MCP servers 的概念与用途：视频中以“MCP server”（有时称为 documentation MCP、diagram MCP 等）为术语，指一类为模型提供结构化外部上下文或能力的插件/端点。MCP 可以为模型提供文档检索、示例、图标列表、或者将模型生成的结构化描述转成可视化产物（例如架构图）。核心价值是“把外部信息（documentation、icons、knowledge base 等）以结构化方式提供给模型，使其能在 agent 执行中读取文档、产生可操作的输出（例如 Cloud architecture diagram）”。
- 演示流程：演示者下载并引入两个 MCP server：一个用于查询 AWS 文档（docs client），一个用于绘制图表（diagram client）。通过一行命令（示例用 UVX 或类似工具）就可以把 MCP server 的 Python material 拉到本地，然后在 Strands 的 agent 中把这些 MCP client 注册为工具集合的一部分。在 agent 的 system prompt 中，给定一个“你是认证的解决方案架构师（extra certified solutions architect）”的角色约束（role prompt），并指示其去“获取 Lambda 文档并生成静态网站使用 Lambda 与 S3 的架构图”，作为任务输入。
- Agent 执行细节与错误处理：运行后 agent 会分解任务为子步骤（search documentation → read docs → create diagram），并通过 HTTP 调用或 MCP 接口检索 Lambda 文档，解析哪些图标可用，然后生成 diagram 描述并尝试创建可下载的图像文件。演示中模型在首次生成图标时发生错误（图标选择导致失败），agent 自主检测失败并修正（修正 cloud icon），再次生成成功并保存图表。整套流程用约 40 行代码完成，展示了通过 MCP 将外部知识与图形渲染能力融入 agent，使其能在多步骤任务中既检索权威文档又输出可视化成果。
- 部署与扩展：关于如何把 MCP server 部署在云端（例如在 Lambda 中以 Server-Sent Events 做 HTTP streaming），演示者回答说 MCP 支持 HTTP streaming/Server-Sent Events，可以把 MCP 部署为 Lambda + API Gateway 等架构，但需要调整 setup。总之，MCP 是连接 LLM 与外部世界（文档、数据库、渲染服务、第三方 API）的“USB-C（类比）”，为 agent 提供额外能力与上下文。

## 3.6 Cloud Code 与自动生成 CDK Agent：用模型改写代码的演示

- 目标：示范如何在 VS Code 内使用 Cloud Code（与 Bedrock 集成）让 Claude（通过 Cloud Code）“理解仓库中的现有代码并自动生成/修改另一个 agent 文件”，例如从现有示例生成一个新的 CDK（Cloud Development Kit）agent，并将其连接到 MCP server。这里的重点不是传统的手写代码，而是展示 Claude（cloud code）如何作为“代码助手 / 自动化编写者”在上下文中查阅仓库文件、生成模板、并应用更改。
- 过程细节：演示者在仓库中新建一个空文件，随后在 VS Code 使用 Cloud Code 的交互功能向 Claude 提问：“请更新 CDK agent，使其成为一个连接到 MCP server 的 Strands agent，参考仓库中其他示例”。Cloud Code 会读取仓库文件、列出计划（plan of attack）、逐步生成并插入代码修改，最后询问用户是否应用这些变更。工具还会给出变更的元信息（模型调用成本、耗时、使用了哪些模型等），从而帮助开发者理解自动化编辑的影响。
- 结果与价值：Claude 能成功生成 TypeScript 或 Python 的 CDK 代码示例（演示中显示生成了 TypeScript 的例子并加入必要的安全/配置项、以及对 CDK 约束的说明），并能加上注释或最佳实践（例如安全性建议或 cdk-nag 规则）。这体现出一种开发者工作流：把繁琐的样板（infrastructure as code）交由模型在受控上下文中生成，再由人工审阅与部署，从而大幅降低开发初期的摩擦。演示者还强调 Cloud Code 的可视化反馈（cost estimate、API 请求详情），让用户在使用模型自动化改写仓库时更有把控。

# 4. 框架 & 心智模型（Framework & Mindset）

- 简化三要素（models + tools + prompt）作为 agent 构建心智模型：视频反复强调 Strands 的核心心法是“足够而简洁”，即构建 agent 仅需三要素：选择合适的模型（models）、提供可调用工具集合（tools）、并用明确的系统 prompt（prompt）定义目标与约束。作为开发者的思路应当从这三点出发：先确定 agent 的高层目标与边界（prompt），再列出 agent 需要的外部能力（tools，例如 HTTP 请求、数据库查询、绘图服务或 MCP servers），最后选取在 Bedrock 可用且成本/延迟合适的模型变体（例如 Claude 3.5、3.7、v7 等）。此心智模型的优势在于把复杂的 agent 行为分解为可管理的维度，使设计与测试更可控。
- 以模型为中心的决策下放：Strands 的设计假设当代 LLM（如 Claude）在推理与接口调用决策上已非常强大，因此把一部分细粒度的决策（如如何从“San Francisco”推断出经纬度或使用哪个查询参数）交给模型，实现更少的硬编码。心态上，这要求开发者信任模型的通用推理能力，同时在系统 prompt 与工具接口上设定足够的保护（例如明确规定允许调用的 endpoint、返回格式、或对失败的回退策略）。换言之，开发者把“协议”与“能力声明”暴露给模型，而不是把所有路径硬编码在框架中。
- MCP 作为“能力扩展层”的心智模型：把 MCP servers 看作给模型“安装插件”的方式。原始 LLM 可能缺乏最新或者专属领域知识、特定的 API 接口行为描述或特定的渲染能力，而 MCP 提供了一个结构化且可复用的方式把这些外部能力接入 agent。在设计 agent 时，应把 MCP 视为一种“能力声明”：如果任务需要查阅特定文档、绘制特定样式的图表、或访问内部数据库，就为模型提供对应的 MCP，使其在执行中既能检索权威信息，也能调用外部服务完成实际动作。
- 自动化与人工审查结合的工作流：Cloud Code + Bedrock 的演示体现了一种“模型辅助开发”（model-assisted development）心态：让模型自动生成或修改代码（例如生成 CDK stacks、配置 agent 等），但在生产化之前由工程师进行审查与部署。核心步骤可总结为：定义修改意图 → 通过 Cloud Code 让模型读取上下文并生成修改建议 → 人工审阅与测试 → 部署到受控环境（例如使用既有的 CI/CD、CDK 流程）。这种心智模型能显著加速从概念到可运行原型的过程，但也强调在关键决策处保留人为把关。
- 最后，成本与治理并行的思维：尽管视频主要聚焦技术实现，但 Cloud Code 的回馈（总成本、API 调用数、模型选择）提醒开发者在设计 agent 时需同步考虑成本与合规治理。实践中需要建立监控、使用模型版本控制策略、以及对 agent 的权限（例如哪些工具可调用、能否访问外部系统）进行严格限定，以平衡创新速度与企业风险管理。

# 总结

本视频以概念讲解加实操工作坊的方式，展示了在 Amazon Bedrock 环境下结合 Claude 系列模型与 Strands Agent SDK 构建自治 agent 的完整路径。关键结论包括：Strands 通过“models + tools + prompt”的极简接口快速上手；MCP servers 为模型提供外部知识与能力，使 agent 能读取文档、调用服务并输出图表等复杂成果；Cloud Code 与 Bedrock 的集成可让模型在 IDE 内读取仓库并自动生成或修改 agent 代码，从而显著提升开发效率。总体上，演示表明利用 Bedrock + Claude + Strands，可以用少量样板代码构建强大的多步骤自治工作流，并通过 MCP 与云服务无缝对接以扩展能力。