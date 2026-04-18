---
notion-id: 28478d23-e296-8114-be4b-eb9d35ac4fdc
cover: "[[imgs/ICT订单流策略详解与操作指南.jpeg]]"
Date: 2025-10-06
Last edited time: 2025-10-06T12:19:00
Tags: []
Link: https://youtu.be/ofQ--jkHTm4?si=4_iMR5f2BGj8QQvN
pic: https://img.youtube.com/vi/ofQ--jkHTm4/hqdefault.jpg
Verification: unverified
Owner:
  - AI generation
---
# 1. Metadata

- Title: OrderflowStrategy（ICT 的一种交易系统）详解与操作指南
- Author: Alan（视频讲述者）

# 2. Overview

这段视频介绍并示范了 ICT 社群内常见的一个交易系统 OrderflowStrategy（订单流策略）。核心论点是：通过识别趋势结构（Higher High / Higher Low 或 Lower Low / Lower High）、观察结构破坏（Break of Structure，BOS/结构破坏）、标记买方/卖方流动性区域（Buy-Side / Sell-Side Liquidity）以及等待动能累积形态（Accumulation / 动能累积）并在关键兴趣点（Point of Interest，POI：包含 FVG/失衡区域 与 Order Block/订单块）处进行挂单或市价跟进，就能按照趋势安全且高效地建立仓位。结论是：OrderflowStrategy 与作者原先使用的 Structured Breakout（结构突破）和 Request（请求位）非常相似，关键在于理解每一步的逻辑与等待合适的累积时机再入场，从而提高胜率与盈亏比。

# 3. 按照主题来梳理

## 3.1 什么是 OrderflowStrategy 与趋势判定

- OrderflowStrategy 本质是“跟随趋势”的策略。讲者先用最基本的趋势定义来铺垫：上涨趋势由连续的 Higher High（更高高点）和 Higher Low（更高低点）构成；上涨趋势的一个关键条件是价格不能把最近的 Higher Low 打掉（若被打掉，上涨趋势结束且下跌趋势尚未确立）。相反，下跌趋势由 Lower Low（更低低点）和 Lower High（更低高点）构成，且下跌趋势同样不能被打掉其最近的 Lower High。
- 对交易者而言，趋势判断的实务应用是：当市场处于上涨趋势（Higher High + Higher Low），优先考虑做多（买入）；当市场处于下跌趋势（Lower Low + Lower High），优先考虑做空（卖出）。但“在何处做多/做空”并不是盲目追随，而是依赖 OrderflowStrategy 的后续流程：识别结构破坏（Break of Structure，简称 BOS/结构破坏）、确定流动性区域（Buy-Side / Sell-Side Liquidity）、等待动能累积（Accumulation/动能累积）以及在 POI（Point of Interest，关键兴趣点）处执行。
- 讲者强调趋势判断并非瞬间判断，而是通过高、低点的演变来确认走势方向。此外，作者指出：不能在动能极强、无回撤的阶段硬进场（即“catching the falling knife/接住下落的刀”类比），因为那样容易被快速的冲击造成止损。因此策略强调等待回撤与累积——即在结构已经被破坏、主力留下的流动性区域形成后，等待价格在该区域出现累积（减速、盘整或小范围消耗），再于 POI 做单。通过这种方式可以兼顾顺势与风险控制。

## 3.2 四个关键概念：BOS、Buy/Sell-Side Liquidity、Accumulation、POI（FVG 与 Order Block）

- 第一个关键概念：Break of Structure（BOS/结构破坏）。BOS 是指当价格穿破并建立了新的高位或低位，从而改变了原先的结构。例如上涨趋势里形成新的 Higher High，并穿破前高，这个穿破区域被视为结构破坏（讲者也称之为 VOS 或结构破坏区域）。BOS 的确认意味着主力的动能已经释放，接下来会形成一个回撤，该回撤通常会回到主力留下的流动性区域。
- 第二个关键概念：Buy-Side Liquidity（买方流动性）与 Sell-Side Liquidity（卖方流动性）。这些区域是主力在突破或结构破坏后，价格回撤时会寻找并消费的流动性区。Buy-Side Liquidity 一般出现在上涨趋势的回撤区，作为支撑；Sell-Side Liquidity 出现在下跌趋势的回撤区，作为阻力。作者把这些称为“主力区域”或 ICT 的 Bid/Ask Liquidity（视频中也叫 Bite-Side-Aquity/Buy-Side Liquidity 和 Sell-Side Liquidity）。
- 第三个关键概念：Accumulation（动能累积）。这是价格回撤到流动性区域后出现的“减速或整固”形态。Accumulation 可以表现为横盘、缓慢下跌、趋势线收敛等不同形态。其作用是消耗短期交易者的动能或让主力逐步建仓，从而为下一段有力的趋势做准备。讲者强调：只有在看到 Accumulation 形态时才去交易；若价格没有任何累积、只是快速下坠或冲高，则不交易，以免在强势的动能冲击下被止损。
- 第四个关键概念：Point of Interest（POI，兴趣点），包含两种常见子类型：
    - FVG（Fair Value Gap/失衡区域，视频称为 FEG）。FVG 是在快速动能释放阶段形成的“空位”：通常由第三根 K 线与第一根 K 线之间的缺口产生（讲者说只要三根 K 线，第一根低位与第三根高位之间的距离就构成 FVG）。ICT 体系认为价格很可能回补这一空位后再反转，所以 FVG 是重要的 POI。
    - Order Block（订单块）。Order Block 是导致 FVG 形成的那一整根 K 线（即那根促成快速动能的 K 线本身）。无论 K 线为多头或空头、颜色如何，只要它是形成那波不平衡的起始烛线，它就是 Order Block。ICT 认为大型订单往往藏在 Order Block 处，价格通常会回到这里再发生反转。
- 这四个要素合在一起就是 OrderflowStrategy 的核心：先识别 BOS（结构破坏）标志趋势方向，再标记 Buy/Sell-Side Liquidity 区域，观察回撤处的 Accumulation（动能累积），最后在 POI（FVG 或 Order Block）处下单或挂单。每个步骤都要有明确的确认信号（例如累积形态、触及 POI）才能执行，避免盲目追单。

## 3.3 交易流程与下单规则（一步一步的操作流程）

- 总体流程（分步说明）：
    1. 确认趋势与结构：在较短或中等时间框架内识别市场是否处于明显的上涨（Higher High + Higher Low）或下跌（Lower Low + Lower High）趋势。观察是否有 Break of Structure（BOS/结构破坏），例如新高突破或新低突破，作为主力动能释放的标志。
    2. 标记流动性区域：在确认 BOS 后，标注对应的 Buy-Side Liquidity（若上升）或 Sell-Side Liquidity（若下降）。这个区域通常是突破前后价格回撤会触及的区域，是主力可能回补或搜集对手方订单的地方。
    3. 等待动能累积（Accumulation）：当价格回撤到流动性区域时，不直接进场，而是等待出现累积形态。累积形态可表现为横盘、缓慢收敛或小规模下跌/上升等任何“动能减弱并消耗”的结构。只有在看到累积后，才视为进场的前置条件。
    4. 确定 POI（FVG 或 Order Block）：在流动性区域及累积形态内部或边缘，寻找 POI。FVG（失衡）通常是三根 K 线形成的空位；Order Block 是导致失衡的那根整烛线。讲者建议可把 FVG 与 Order Block 结合使用，双重验证。
    5. 挂单或等触及后下单：有两种常用执行方式：
        - 激进方式：在 Accumulation 形成后直接挂单（即预先在 POI 附近挂买/卖单）。风险是有时会先被止损（被打掉）然后价格再回去，但若位置设置合理，仍可接受；
        - 保守方式（讲者较偏好）：等待价格先回到 POI 并触及后再下单或以警报提醒进场。这样可以避免无意义的提前止损，提高交易安全性。
    6. 止损与目标设定：止损通常设置在 POI 的外侧或累积区域之外（避免被常见的“假突破”清掉）。盈利目标按风险收益比设定，讲者常提到希望至少达到 1:2 的盈亏比，若能拉到 1:3+ 更佳。也可以把部分仓位以较近目标锁利，剩余部分放到 Accumulation 的起点或更高位（或更低位，取决方向）。
    7. 纪律与复盘：若没达到累积或 POI 条件则不交易；交易后要回顾每笔单的质量（quality），包括是否出现合格的 accumulation、POI 是否真实到位、止损是否合理等。
- 风险管理与执行细节：
    - 不在强动能（无累积）阶段贸然进场。
    - 若结构被“假突破”（价格只用一根 K 线突破然后滞留、回撤），应识别为可能的假突破，流动性仍可能在突破区域附近。假突破情形下，原先判断的 LowerLow/LowerHigh 或 HigherHigh/HigherLow 需要重新判定位置，不要轻易更改方向。
    - 当多个 accumulation 区出现时（例如连续多个小累积区），可以结合这些区域形成更强的 supply/demand zone（供应/需求区），作为更扎实的入场或止损参考。
    - 讲者示范用 5 分钟图在数小时内达到 1:3.82 的盈亏比案例，强调耐心等待累积与 POI 能带来更高的盈利潜力，但也指出某些 setup 因价格花费较长时间回溯，会降低设定的 quality。

## 3.4 案例解析（视频中的三个示例与分解）

- 示例一（上涨趋势突破与回撤做多）：
    - 市场先形成连续的 Higher High 与 Higher Low，随后出现一根具有强烈动能的上涨烛线，价格突破前高（形成 BOS/结构破坏）。讲者把这个突破区域标为 VOS（或结构破坏区域），并认定突破后会有回撤回到主力区域（Buy-Side Liquidity）。
    - 价格回撤到该区域后出现 Accumulation（作者举例包括横盘或缓慢回调的形态），这时候寻找 POI：既可以是 FVG（失衡区），也可以是前面导致失衡的 Order Block（订单块）。讲者指出两者结合使用能提高信号质量。
    - 在 Accumulation 出现后，作者有两个选择：直接在累积区挂单或等待价格触及 POI 再进场（作者更倾向后者以避免被无意义的止损）。案例里，当价格触及 POI 并满足止盈设置后，达成了大约 1:2 的盈亏比（可进一步调整以获得更高的收益）。
    - 要点：必须见到 Accumulation 才开仓；POI 可作为触发点；止损要设在区域以外以避免假突破误伤。
- 示例二（下跌趋势中的假突破与做空）：
    - 市场中出现了新的 Lower High（更低高点）和随后形成的 Lower Low（更低低点），这构成 BOS，表明下跌动能存在。讲者在 BOS 区域标示 Sell-Side Liquidity（供给区）。
    - 有时候突破看似很短促（仅一根 K 线突破后滞留），这种情况可能是“假突破”。即便如此，价格在该区域的流动性仍旧是有效的卖方流动性区域，交易者仍可在合理的 POI 找寻做空机会，但需要判定该区域是否为极限（作者强调极限位置更优）。
    - 在这个示例中，作者选择了一个 supply zone（供应区）作为潜在入场点，因为它更接近极限且累积形成后更具可靠性。之后价格做出了多次 accumulation，最终在合适的 POI 处入场，但由于价格花了较长时间才回到目标，setup 的“quality”被认为不如第一个例子好。
    - 要点：识别假突破并不等于放弃该区域；要关注是否为极限位置与 accumulation 的质量；若止损距离较大，可能需要更谨慎或放弃该 setup。
- 示例三（再次确认结构破坏并高质量入场）：
    - 这是一个相对明确的上涨结构破坏（新高后回撤）。讲者找到了明显的 FVG 与对应的 Order Block，并且回撤形成了清晰的 accumulation。此时同时出现 Buy-Side Liquidity 与 POI 的重合，使得入场信号强度大幅提升。
    - 作者示范两种入场方法（挂单或待触及后市价进场），并讨论不同止损设定的风险/回报：较保守的止损设置在区域外侧能避开假突破，但会降低风险收益比；激进的止损设在更近位置可提高收益但增加被止损概率。举例中若将止盈设在 accumulation 起点，能实现 1:3.82 的盈亏比，且该次交易从 5 分钟图视角花费约 5 小时达到目标。
    - 要点：当 FVG 与 Order Block 同时出现且 accumulation 清晰时，setup 的质量很高；时间尺度会影响回报实现时间，但不影响信号本身的有效性。

# 4. 框架 & 心智模型（Framework & Mindset）

- OrderflowStrategy 的框架要点（可当作一套可复用的操作心智流程）：
    1. 趋势优先（Trend First）：在任何时间框架内，先判断趋势方向（Higher High/Higher Low 或 Lower Low/Lower High）。这一步将决定主要操作方向（做多或做空），避免与主趋势对着干。
    2. 结构破坏作为信号（Structure Break as Trigger）：不要凭感觉乱进场，先等结构破坏（Break of Structure/BOS）出现，它代表主力进行了动能释放并且可能已改变短中期的力道。BOS 提供“为什么会有回撤与流动性存在”的因。
    3. 寻找主力流动性区（Identify Liquidity Pools）：在 BOS 后，标出 Buy-Side 或 Sell-Side Liquidity 区。把这些区域视为主力回补或聚集订单的“猎场”。从心态上，要相信大型订单会回到这些区域并留下可交易的机会。
    4. 等待动能累积（Wait for Accumulation）：市场不会在每次回撤就给出可交易信号；真正值得交易的是那些在流动性区出现了累积/消化的回撤。心态上要耐心，不强行追涨杀跌，避免在高动能阶段接刀。
    5. POI 优先级（POI as Entry Focus）：在流动性区和 accumulation 内查找 POI（FVG 与 Order Block）。当 POI 与累积相结合，入场信号强度最高。心态上把 POI 当成“主战场”，在其附近设置警报或挂单。
    6. 风险控制与位置管理（Risk Management）：始终设置止损，止损位置依据 POI/Order Block 边界或 accumulation 的最低/最高位来设。目标按照风险收益比（至少 1:2）来设定，优先长期稳定胜率而非追求一次性高回报。
    7. 复盘与系统化（Review & Systemize）：每笔交易要有记录并复盘，关注是否每一步（BOS、liquidity、accumulation、POI）都被严格执行。通过复盘提升执行力，将策略变为“可重复的系统”而非临时直觉。
- 心智模型补充（如何在情绪与决策中应用）：
    - 耐心优先：交易不是在每次回撤都要参与。等待 accumulation 是保护资本的关键。把每次等待视为筛选最优机会的过程，而不是浪费时间。
    - 证据驱动（Evidence-Based）：每一步都需证据支持（结构已破坏、流动性区明确、accumulation 清晰、POI 到位）。不要凭单一指标或主观直觉下重注。
    - 适应性而非顽固（Adapt, Don’t Force）：若某个区域变成“假突破”或累积未形成，应迅速放弃该设定，寻找下一个高质量 setup。坚持策略的原则但对具体情景保持灵活。
    - 风险优先于收益（Risk Before Reward）：先定义最大可承受风险（止损大小），再确定仓位大小与盈亏比目标。即使策略成功率高，也要严格仓位管理以避免单次爆仓。
    - 分级入场与分段获利（Layering）：可以采用分批入场（部分挂单、部分触及后进场）和分段平仓（先获利一部分，剩余跟随趋势），以平衡胜率与收益。
- 为什么这个框架可行（理论上的合理性）：
    - OrderflowStrategy 的逻辑基于市场参与者行为学：机构在形成大行情前会先发起突破（BOS），随后回撤以收集对手方订单（liquidity），并在回搜区做仓位调整（accumulation）。FVG 与 Order Block 是技术上观察到主力活动的“印记”。因此在实际交易中利用这些痕迹，可以提高与机构行为同步的概率，从而获得更有利的入场点与盈亏比。
    - 该框架兼顾了顺势（在趋势方向上交易）与安全（等待累积与 POI），同时提供明确的入场/出场逻辑，使交易从直觉行为转向可量化、可复盘的系统化流程。

# 总结

OrderflowStrategy 是一套以结构与流动性为核心的顺势交易方法：先判定趋势并等待结构破坏（BOS），标定买卖双方流动性区，等待动能累积（Accumulation），在 FVG（失衡区域）或 Order Block（订单块）等 POI 附近执行挂单或触及后进场。关键在于耐心等待累积、以 POI 为触发、并严格设置止损与盈亏比。无论采用激进挂单或保守触及后进场，都应遵循证据驱动和风险优先的心态，并通过复盘把该方法变成可重复的交易系统。