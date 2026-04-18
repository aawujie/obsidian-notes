---
notion-id: 26f78d23-e296-81b0-8fb6-cc4130629c13
cover: "[[imgs/Spellbook使用与贡献全流程指南.jpeg]]"
Date: 2025-09-15
Last edited time: 2025-09-16T19:58:00
Tags: []
Link: https://youtu.be/yGkcV6speaM?si=cgLCiJcbJi9fPCvE
pic: https://img.youtube.com/vi/yGkcV6speaM/hqdefault.jpg
Verification: unverified
Owner:
  - AI generation
---
# 1. Metadata

- Title: 如何阅读与贡献 Spellbook（Dune 的社区 DBT 平台）
- Author: 视频主持人（转写整理）

# 2. Overview

本视频介绍了 Spellbook（Dune 的社区驱动 DBT 平台）的定位、核心概念与日常使用方法，包含如何在 Spellbook 里理解数据**血缘（lineage）**、查找与阅读已有模型、以及如何在本地搭建、修改并通过 PR（Pull Request）把修复或新模型贡献回 Spellbook。作者通过一个实操示例（为 L2 Mantle 添加 gas fees 数据并修复 rollup 收入展示的缺失）演示了从问题发现、定位血缘、在仓库中新建模型、提交分支、等待 CI（持续集成）测试并请求代码评审的一整套流程。结论是：掌握 Spellbook 能使你快速成为链上数据领域的高级从业者，理解和贡献其模型可以让你接触到 Dune/Spellbook 那“冰山下”的复杂数据工程工作流。

# 3. 按照主题来梳理

## 3.1 Spellbook 是什么，以及 DBT 在其中的作用

- Spellbook 是什么（定位与用途）
    - Spellbook 是 Dune 提供的一个“社区构建的 DBT 平台”。它是一个公共仓库，保存了大量用于链上数据处理的模型（tables）、宏（macros）与子项目（subprojects）。
    - 在 Dune 的应用中，像 Dex trades（去中心化交易）、lending labels（借贷地址标签）等被展示的数据，很多是由 Spellbook 提供的表（tables）构建而成。换句话说，Dune 的可视化/仪表盘层面很多数据来源于 Spellbook 里的模型定义。
    - 通过社区协作的方式，工程师与数据分析师可以共同维护、修复与扩展这些模型，使得整个生态的数据层越来越完整、可靠。
- DBT（Data Build Tool）概念简介与在 Spellbook 的角色
    - DBT 是一种管理 SQL 查询、模型之间“顺序执行”和“血缘关系（lineage）”的工具。它允许把复杂的数据转换流程拆成模块化的模型、宏与脚本，从而构造出 DAG（Directed Acyclic Graph，有向无环图）形式的血缘树。
    - 在 DBT 里，每个模型通常是一个可以执行的 SQL 查询；模型之间通过 ref（引用）或 source（来源）建立依赖关系。执行时，DBT 能按依赖顺序逐个构建这些模型，保证下游模型在其上游模型准备好后再运行。
    - Spellbook 基于 DBT 的组织方式：模型被组织在 subprojects、models、macros 等目录里，整体呈现为一个包含许多互相引用与组合的大型数据工程系统。理解 DBT 的工作方式，是高效使用 Spellbook 的前提。
- 为什么要把模型做成 DBT 的形式（好处）
    - 可复用性：公共宏（macros）能把重复逻辑抽象出来，多个链或平台可以复用同一套转换逻辑，只需在参数或少量文件上做适配。
    - 可追溯性：通过血缘图（lineage），可以准确追踪一个最终表是如何由一系列中间模型、源表组合而成，便于排查数据异常。
    - 代码审查与 CI：把表定义放到 Git 仓库里可以通过 PR 流程进行审查，结合 CI 自动运行测试与编译，减少错误进入生产。
    - 增量构建（incremental）：DBT 支持增量更新，避免每次全量重建，提升效率并降低成本。
- DBT 中的一些关键词（保留原文并说明）
    - macro（宏）：可以理解为函数（function），用于在多个模型中复用复杂的 SQL 逻辑或模板化操作。视频中反复提到宏（macro）和类似的“unisoft v2 compatible trades”类型的宏。
    - ref：DBT 的内部引用，用于引用同一子项目中的其他模型文件，表明依赖关系。
    - source（来源）：用于引用仓库以外的源表（例如原始链上表或别的 subproject 中声明的表），在 schemas 或 sources 文件中声明。
    - YAML：DBT 用来声明模型元数据的文件格式（tests、columns、描述、作者等）。
    - incremental（增量）：一种构建策略，模型每次只处理一段新数据（例如过去 x 天或自上次构建之后的区块区间），避免重复计算全量数据。
    - DAG / Lineage（血缘）：模型之间的依赖关系结构，通常以图形（DAG）展示，帮助理解数据如何由源头一步步变换、聚合成最终表。
- 对初学者的建议（摘自视频的态度）
    - 如果你对 DBT 不熟，Spellbook 的文档（docs）是第一站，里面会讲 macros、models、subprojects 的使用方式。虽然一开始可能看起来像“mumbo jumbo（晦涩难懂）”，但很多概念可以通过阅读和实际跟随一个模型的 lineage 来学习。
    - 先从能产出你关心的最终表（例如 Dex trades）出发，沿着 ref/source 向上追溯每一层模型，会比从抽象理论开始更快上手。

## 3.2 在 Spellbook 中如何导航、阅读数据血缘（Lineage）与查找模型

- 从最终表出发的查找策略（实践路线）
    - 如果你知道目标表的名字（例如 Dex trades），推荐直接在 Spellbook 的 DBT subprojects 搜索栏里输入表名，快速定位相关模型。视频中主持人展示了直接搜索 "Dex trades" 并进入对应子项目查看 SQL。
    - 在找到某个表后，你会看到该模型引用了其它子查询或宏。DBT 的常见写法会用 ref() 来表示引用模型，用 source() 或直接引用来表示原始来源表。识别这些关键字可以帮助你沿依赖链往上追溯。
    - 有时模型使用了宏（macro），这些宏通常在 macros 目录里定义。宏本质是函数式的模板，可以把多个链或平台的逻辑统一起来。要理解宏的实现，需要打开相应的宏定义文件（通常是以 .sql 或 .jinja2 风格的模板文件）。
- 理解常见目录与命名约定
    - subprojects：大的项目模块划分，比如针对交易（trades）、token、dex 等不同主题会有不同子项目。每个 subproject 下包含 models、macros、schemas、sources 等文件夹。
    - models：具体的 SQL 模型定义（最终会产表）。
    - macros：宏定义，用于复用复杂逻辑。
    - schemas / yml：元数据与测试声明文件，描述模型列、测试、以及谁是作者等。
    - sources：声明外部来源或原始表的文件，帮助 DBT 知道在哪里拉数据。
- 用搜索与代码搜索两种方式定位代码
    - 简单名称搜索：当你知道目标表名或 model 名称时，使用普通搜索能很快找到文件路径与 SQL 定义。
    - 代码搜索（code search）：如果表名分散或嵌套在宏/条件中，使用全局代码搜索能找到引用、宏调用或更隐晦的匹配项。视频中提到有时候需要切换到 code search 才能定位某些定义。
- 如何读懂一个模型的逻辑（循序渐进）
    - 先看模型的 SQL 定义，注意最顶层的 select / with / union 逻辑。很多模型实际上是“Union all” 多个链或平台的子查询的组合，体现了“对多链循环并合并”的设计模式。
    - 识别引用（ref）与来源（source）：每一个 ref 指向另一个模型文件，继续点开该文件你会看到更下游或更原始的逻辑，逐层追溯直到看到原始 source 表（例如 base transactions、traces、blocks）。
    - 查阅对应的 schema（YAML）文件：这里有字段定义、测试（例如 unique、not_null）与分区信息，能帮助你理解该表的预期结构和约束。
    - 如果模型用了宏：打开宏文件，理解宏的输入参数与输出 SQL 模板。宏往往把跨链差异、平台差异封装起来，参数化后可以在多处复用。
- 血缘（lineage）示例说明（从视频里的示例）
    - 视频展示了一个 orders 表作为顶层表，下面依赖 customer order history、order payments 等中间表，最底层是 stg orders（stage 原始订单表）。这就是典型的 DBT lineage：最终表由若干中间表合成，中间表又由更基础的 stage/源表生成。
    - 在 Spellbook 里，这些关系在 DBT subprojects 页面上可以以树或 DAG 形式查看，也可以通过文件引用关系手动追溯。
- 实用提示（调试与验证模型）
    - 使用 Spellbook 的 Issues 页面：如果你在使用某个表时发现问题或需求（例如某字段缺失或数据异常），可以在 Issues 里创建 issue 描述问题，协助维护者发现与修复。
    - Discussions 与周报：Spellbook 会有讨论区和每周的 GPT 摘要，用来汇总新增/修改的表。这是跟进仓库动态、了解新变更的好方式。
    - 直接在 Dune 中试查询：定位到你刚修改或关注的表后，可以在 Dune 新建查询直接 select 该表来检查输出是否符合预期，这能快速验证模型变更效果。

## 3.3 本地设置与贡献工作流（Fork、Branch、PR、CI、测试）

- 本地准备与仓库流程概述
    - Fork（派生仓库）：首先在 GitHub 上 Fork Spellbook 主仓库到自己的账户，得到一份独立的副本用于开发。
    - Clone（克隆）：把你的 Fork 克隆到本地（例如使用 GitHub Desktop 或 git 命令），在本地进行修改。
    - 新建分支（Branch）：为每次改动新建一个 feature/bugfix 分支（例如 mantlegas_fix），避免直接在 main 上提交。
    - 开发与提交（Commit）：在本地编辑模型、添加 SQL 与 YAML，按常规 git 提交并 push 到你的 Fork 分支。
    - 打 PR（Pull Request）：在 GitHub 上从你的分支对主仓库发起 PR，填写变更描述并关联对应的 issue（如果你在 Issues 里先创建了问题），这样维护者可以看到上下文。
- 在本地编辑 DBT 模型的注意事项
    - 文件结构遵守现有约定：把模型放在对应的 subproject 和 models 目录下，名字、meta 与 schema 文件尽量参照现有实例，保持一致性。
    - 增量（incremental）模型配置：如果模型被声明为 incremental，需要在 SQL 中提供增量判断的 predicate（例如基于时间的 block_day、block_month 等）。这确保模型在运行时只处理新增部分而不是全量重建。
    - YAML metadata（schemas）要补全：在对应的 schema 文件中声明新的模型名称、列名、测试（tests）、分区策略（partition by）与作者/贡献者信息等。这不仅用于文档，也会被 CI 用来检测。
    - sources 声明：如果你的模型依赖某些 source 表（在另一个 subproject 或外部数据源），需要在 sources 文件中确认相应的 source 已被声明。如果源表不存在，可能还需要新增 source 声明。
- 运行 CI 与调试常见错误
    - PR 触发 CI：提交 PR 后，Spellbook 的 CI 会自动运行。它通常会先运行被编辑或新增的模型的编译（DBT compile）和测试（DBT test）。
    - 注意观察 CI 日志：CI 会列出失败的步骤（常见为 SQL 语法错误、缺少引用、测试未通过等）。第一步要看的是“running initial models”和“testing”两类步骤。
    - 本地调试技巧：可以在本地安装 python 和 DBT 环境，使用 dbt compile 指定某个模型生成 SQL（如果项目使用 Jinja/宏），这样能在离线环境复现 SQL 并快速修复语法或模板错误。
    - 更新分支（rebase 或 merge main）：如果你的 PR 持续时间较长，其他 PR 合并可能会让主分支产生变化。CI 会尝试把你的变更与现有最新更改合并，若出现冲突或新问题，需要你把分支从 main 更新（merge 或 rebase）并重新推送。
- 提交评审（PR）与合并后的验证
    - 标注与分配审阅者：在 PR 中添加标签（例如 ready for review）并指定合作者/维护者（视频中提到要把 PR 指派给 Jeff），不要自评审合并（管理员权限可能被限制）。
    - 维护者审查：维护者会查看你的变更、CI 结果，并提出建议或直接批准。如果有需要改进的地方，他们会在 PR 下评论要求你调整。
    - 合并后结果：一旦 PR 合并，新的模型会在主仓库生效，并被用于生成的最终表。Dune 的 dashboard 则会反映这些更新（例如之前缺失的 Revenue 现在被填上）。
    - 跟踪变更：可以通过 Spellbook 的 Discussions 或每周汇总跟进其他人对仓库的改动，保持对依赖模型变化的感知。
- 常见问题与实践建议
    - 很可能第一次提交会遇到错误，这是正常的。数据工程与 ETL 建设本质上需要多次迭代。
    - 多查看类似平台与链的现有实现：很多时候，只需复制体类似实现并替换平台名（如将 zora 替换为 mantle）就能快速生成初稿模型。
    - 注重 schema 的 tests：DBT 的测试（unique、not_null、relationships 等）能及早发现数据质量问题。为新模型补充合理的测试是必要步骤。
    - 与团队沟通：在 Issues 里描述清楚问题与修复思路，配合维护者能加速审查与合并。

## 3.4 实操示例：定位并修复 Mantle 的 gas fees 缺失（完整复盘）

- 问题发现（现象）
    - 在某个 rollup economics（rollup 经济学）仪表盘中，作者发现图表显示“有成本（cost）但没有收入（revenue）”。这触发了调查原因：为什么有成本但没有对应的收入数据？
    - 该仪表盘所用的数据来源为 Spellbook 中的多个表，初步判断是某个 Spellbook 表（可能是 revenue 相关）没有包含 Mantle 链的数据。
- 初步假设与血缘追溯
    - 作者先确认这个仪表盘使用的是 Spellbook 的表（因为不符合其它 raw/decoded/upload/map/view/query view 的命名模式）。
    - 进入 Spellbook 的 DBT subprojects，搜索可能相关的模型（例如 L2 revenue、gas fees 等）。
    - 通过打开相关模型，作者发现有 L1 data fees（费用）表包含成本信息，而收入表（例如 L2 Revenue 模型）存在但其上游依赖的 gas fees 模型并没有把 Mantle 纳入。
- 具体诊断（找到根因）
    - 作者观察到：Mantle 已经在某些模型（例如 mantle 在 L2 revenue 的某处）出现在代码中，但 gas fees 的总体模型并未对 Mantle 做 union/加入，导致 L2 revenue 在依赖 gas fees 时没有 Mantle 的相关数据，从而使得最终的 rollup economics 仪表盘缺失 Mantle 的收入数据。
    - 换句话说，L2 Revenue 模型本身可能包含 Mantle 的逻辑，但它依赖的 gas fees（或 gas fee 的上游源）没有包含 Mantle，造成数据链路断裂。
- 解决方案思路（高层）
    - 在 Spellbook 的相应 subproject 下新增一份与其他链类似的 gas fees 模型文件（例如 gas_mantle.fees），并在相应的组合模型（总的 gas fees 聚合处）中把这一新模型加入 union 的集合里。
    - 确认 Mantle 所需的源表是否已在 sources 中声明（例如 mantle.transactions、mantle.blocks 等）；如果没有，则需先新增 source 声明。
    - 更新 schema YAML（metadata）以包含新的模型、列描述与测试项，确保 CI 能通过测试。
- 实际操作步骤（作者的动手流程）
    - Fork 并 clone：作者已经有 Spellbook 的 fork，拉取到本地。
    - 新建 branch：创建名为 mantlegas_fix 的新分支并推送到 GitHub。
    - 定位模板：在 gas fees 的目录中找到一个已有链（例如 zora）的实现作为模板。通常这些模板包括 SQL 文件与对应的 schema（YAML）。
    - 复制并替换：把 zora 模型复制一份，替换文件名与文件内部的标识（把 zora 替换为 mantle，调整可能的协议差异如 op-stack、optimistic/zk 等若必要）。
        - 注意：有时不同链的命名或结构有差异（例如是 OP Stack、Optimistic 或 Modular），需要在复制时确认源表路径（source）是否存在并可用。
    - 核对 sources：检查 repo 的 sources yaml 是否已有 mantle 的 transactions、blocks、traces、logs 等，如果已经声明，则无需新增源声明；若缺失则需要补充。
    - 增量配置与 schema：在新模型的 YAML 中配置 partition by、incremental 策略、unique key 以及 tests（例如确保字段不为空、唯一性等）。作者保留了原有的 column 定义与测试，并只添加作者信息。
    - 在聚合表中添加引用：除了新增 gas_mantle 模型外，必须在总的 gas fees 聚合模型中把 gas_mantle.fees 加入到 union 列表，确保其会被合并到总表。
    - 提交并推送：把变更 commit 并 push 到 Fork 的分支。
- CI 运行与调试
    - 提交 PR：从自己的分支向主仓库发起 PR，并在说明中写清修复目的，例如 “fixing mantle missing gas related to L2 revenues”，并关联事先创建的 Issue。
    - CI 触发：主仓库的 CI 会运行，仅构建和测试被修改或新增的模型（以提高效率）。主要关注两项：构建（initial models）和测试（testing）。
    - 可能的错误：
        - 语法错误或宏模板错误：如果你在 SQL 模板中写错 Jinja/宏语法，编译会失败。解决方法是在本地用 dbt compile 先行检查生成的 SQL。
        - 引用缺失：如果某个 source 或 ref 指向不存在的表，测试会失败，需要补充 source 或修正引用路径。
        - 测试不通过：比如 unique 或 not_null 测试失败，CI 会给出具体的 select 语句来定位具体哪些值触发了失败。
    - 作者幸运地因为复制并小幅修改他人模板而一次性通过了 CI（视频中说明只有一次 commit 并通过）。
- 合并前后的协作流程
    - 在 PR 中标注“ready for review”并指派给维护者（比如 Jeff），不要自己合并（管理员或审阅者来合并以保持流程规范）。
    - 维护者审查、可能提出小修改请求或直接批准后合并。合并后，Spellbook 的主仓库更新，相关的 Dune 仪表盘或查询会开始使用更新后的模型，从而在 rollup economics 图表中呈现出之前缺失的 Mantle 收入数据。
    - 最终验证：作者回到 Dune，并对修复前的查询（现在引用主仓库更新后的表）进行 select 验证，确认 Revenue（收入）列不再为空并且符合预期。
- 从这个示例学到的要点（总结式提炼）
    - 找问题要沿血缘追溯：不要只看最终表，逐层向上看依赖，找到缺失节点。
    - 常用技巧是复制已有链的实现并替换名词：很多链的处理逻辑类似，复用模板能极快产出初稿。
    - CI 与测试是保障：通过 dbt 的编译和测试能提前发现语法/逻辑/数据质量问题。
    - 社区工作流需遵守：Fork、Branch、PR、Assign、等待 Review 的流程是标准操作；把变更与 Issue 关联并写清说明能加速审查。
    - 贡献是学习捷径：通过修复与扩展 Spellbook，你会迅速掌握链上数据工程的核心实践，成为领域内的高级从业者。

# 4. 框架 & 心智模型（Framework & Mindset）

- 框架一：以血缘（Lineage）为中心的问题定位与修复流程（步骤化心智模型）
    - 步骤 1 — 观察现象并确认来源：当某个仪表盘或查询显示异常（如收入为 0 或字段异常），首先确认该数据是否来自 Spellbook 的某个模型或是别的原始表。判断依据是表名、命名风格或直接查看 Dune 查询引用的表名。
    - 步骤 2 — 沿血缘向上追溯：打开目标表的 DBT 模型，识别 ref() 和 source() 的使用，逐层打开被引用的模型，直到找到最底层的 source（比如 transactions、blocks、traces）。重点是寻找“在哪个节点开始出现缺口或丢失链的数据”。
    - 步骤 3 — 定位差异/缺失的链：在合并/union 的节点上检查是否有漏掉某个链（如 Mantle 没被包含）。如果上游模型或 source 中没有包含该链，就会导致下游聚合缺数据。
    - 步骤 4 — 评估改动边界与影响：确认是否仅需新增一个链的模板模型并把它加入聚合，还是需要在更上游修改 source 或更改宏逻辑。评估改动可能影响的其它模型，判断是否需要同时更新 tests 或 schema。
    - 步骤 5 — 在本地实现修改并补充元数据：复制近似链实现、替换标识并补齐 YAML 中的 schema、tests、partitioning、incremental 策略等，保证新模型在 CI 中能顺利通过。
    - 步骤 6 — PR 与 CI 迭代：发起 PR，观察 CI 的构建/测试结果，按需修复错误。CI 通常会列出失败的测试或编译错误，按照提示逐一解决。
    - 步骤 7 — 合并后验证：待 PR 合并后，在 Dune 或目标环境中重新运行最终查询，确认问题已被解决。必要时补充文档或在 Issue/Discussion 中说明修复细节。
    - 这种以血缘为中心的思路能把复杂的 ETL 问题拆解成可定位与可治理的若干节点，使问题排查与修复更高效且可追溯。
- 框架二：模块化复用与模板优先策略（工程心态）
    - 原则 1 — 先找现成模板再造轮子：很多链或平台在结构上高度相似（例如交易表、gas fee 计算逻辑等）。优先在现有模型中找一个相近的实现，复制并替换具体平台的标识，有助于快速验证与降低出错率。
    - 原则 2 — 抽象为宏（macros）：把跨链的通用逻辑抽象成宏，参数化差异（比如 chain_name、protocol specifics），优点是后续新增链只需传入参数而无需重复逻辑，实现一次维护、处处生效。
    - 原则 3 — 增量策略优先：对大体量数据建表时，优先选择 incremental（增量）构建策略，指定合适的分区（按日期、区块时间等）与增量谓词。这样在 CI 或定时运行时可以减少 compute 成本并加快反馈。
    - 原则 4 — 强化元数据测试：在 schema YAML 中为每个模型增加合适的 tests（例如 unique、not_null、accepted_values），通过测试机制保护数据质量。这不仅是工程实践，也是对协作者的一种合同式保证。
    - 原则 5 — 小步迭代与及时合