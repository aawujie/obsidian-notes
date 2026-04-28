---
title: Demis Hassabis 诺奖访谈笔记
type: summary
created: 2026-04-28
updated: 2026-04-28
sources: [Lex Friedman Podcast, Demis Hassabis second appearance]
tags: [AI, DeepMind, 访谈笔记, DemisHassabis, AlphaFold, AlphaGo, AGI, 蛋白质折叠, 虚拟细胞, 科学研究方法]
---

# Demis Hassabis 诺奖访谈笔记

> 来源：Lex Friedman Podcast，Demis Hassabis 第二次做客。
> Demis Hassabis 是 Google DeepMind 的领导者、诺贝尔化学奖得主。

---

## 一、诺奖猜想：经典学习算法的边界

### 1.1 核心猜想

在诺贝尔奖演讲中，Demis 提出了一个 provocative 的猜想：

> "Any pattern that can be generated or found in nature can be efficiently discovered and modeled by a classical learning algorithm."
>
> "任何可以在自然中被生成或发现的模式，都可以被经典学习算法高效地发现和建模。"

Demis 解释说，诺奖演讲传统上就应该有一点挑衅性。他的思考源于回顾 AlphaGo、AlphaFold 等 Alpha X 项目——这些项目本质上是在极高维度、组合爆炸的空间中构建模型。

- 围棋的可能局面数：$10^{170}$
- 蛋白质的可能结构数：$10^{300}$
- 两者都远超宇宙中的原子数

如果暴力枚举，宇宙的时间都不够用。但他们通过**构建环境的模型来智能地引导搜索**，使问题变得可解。

### 1.2 "适者生存"与可学习性

Demis 提出了更深层的直觉：

> "I sometimes call it survival of the stablest... If you think about geological times, the shape of mountains being shaped by weathering processes... the orbits of planets, the shapes of asteroids — these have all survived processes that have acted on them many, many times. So if that's true, then there should be some sort of pattern that you can reverse learn."
>
> "我有时称之为'最稳定者生存'……如果你思考地质时间尺度，山脉的形状被风化过程塑造……行星的轨道、小行星的形状——这些都经历了反复作用于它们的生存过程。如果这是真的，那么应该存在某种可以被反向学习的模式。"

**核心逻辑链**：
1. 自然界中的系统不是随机的——它们经历过选择压力（进化、地质、宇宙学）
2. 因为有结构，所以存在一个低维流形（lower dimensional manifold）
3. 神经网络擅长跟随梯度——如果存在一个可跟随的梯度，你就不需要处理全部复杂性
4. 因此，自然系统可以被经典学习算法高效发现或恢复

**反例**：人造的抽象问题（如大数分解），如果没有潜在结构，就只能暴力搜索，可能需要量子计算机。

### 1.3 新的复杂度类？

Demis 正在与同事探索一个理论计算机科学问题：

> "What is modelable by classical systems, by non-quantum systems, Turing machines in effect... Maybe a new class of problem that is solvable by this type of neural network process and kind of mapped onto these natural systems."
>
> "什么可以被经典系统、非量子系统——本质上是图灵机——所建模……也许存在一类新问题，可以通过这类神经网络过程求解，并映射到这些自然系统上。"

Lex 戏称为 **LNS（Learnable Natural Systems）**——"可学习的自然系统"类。

### 1.4 信息是宇宙的基本单位

> "Information is the most fundamental unit of the universe, more fundamental than energy and matter. I think they can all be converted into each other, but I think of the universe as a kind of informational system."
>
> "信息是宇宙最基本的单位，比能量和物质更基本。我认为它们都可以互相转换，但我把宇宙看作一种信息系统。"

在这个观点下，**P=NP 问题本质上是一个物理学问题**。

---

## 二、AlphaFold 与 AlphaGo 的方法论

### 2.1 搜索 + 模型的范式

Demis 将 AlphaFold 和 AlphaGo 的共性提炼为同一范式：

1. **学习环境的动态模型**（蛋白质折叠的物理规律 / 围棋的棋局动态）
2. **用该模型引导搜索**（使搜索从指数级变为多项式时间）
3. **目标函数优化**（能量最小化 / 赢棋概率最大化）

> "We're building models of very combinatorially, high-dimensional spaces... if you try to brute force a solution, there wouldn't be enough time in the time of the universe. So you have to do something much smarter. And what we did in both cases was build models of those environments and that guided the search in a smart way."
>
> "我们在极高维度、组合爆炸的空间中构建模型……如果尝试暴力求解，宇宙的时间都不够用。所以你必须做更聪明的事。我们在两种情况下都是构建环境的模型，以智能的方式引导搜索。"

### 2.2 AlphaFold 3：从静态到动态

- **AlphaFold 2**：解决蛋白质的静态 3D 结构
- **AlphaFold 3**：建模蛋白质-蛋白质、蛋白质-RNA、蛋白质-DNA 的**相互作用**（动态视角）
- **AlphaGenome**：预测单点突变如何链接到实际功能

### 2.3 超越已知：创造力与搜索

> "The model can model everything that you currently know about... but then how do you go beyond that? So that starts to speak about the ideas of creativity."
>
> "模型可以建模你目前已知的一切……但如何超越已知？这开始涉及创造力的概念。"

- **Move 37**：AlphaGo 通过蒙特卡洛树搜索找到了围棋中前所未见的策略
- 要在模型之上叠加**搜索过程**，才能进入搜索空间中**新的区域**
- 目标函数必须正确设定，引导搜索走向有意义的方向

---

## 三、蛋白质折叠：物理学如何做到？

### 3.1 自然自己就解决了这个问题

> "Proteins fold in milliseconds in our bodies. So somehow physics solves this problem that we've now also solved computationally. And I think the reason that's possible is that, in nature, natural systems have structure because they were subject to evolutionary processes that shaped them."
>
> "蛋白质在我们体内以毫秒级折叠。所以物理学以某种方式解决了这个问题，而我们现在也用计算解决了。我认为这是可能的，因为自然系统具有结构——它们受到进化过程的塑造。"

### 3.2 能量景观与梯度

- 蛋白质折叠存在一个**能量景观**（energy landscape），其中有可跟随的梯度
- 神经网络最擅长的就是跟随梯度
- 只要目标函数正确设定，就不需要应对全部组合复杂性

---

## 四、从视频学习物理：Veo 3 的启示

### 4.1 被动观察足以理解物理？

> "If you were to ask me five, 10 years ago, I would've said... you probably need to understand intuitive physics... there's a lot of theories in neuroscience, it's called action in perception where you need to act in the world to really, truly perceive it in a deep way... But it seems like you can understand it through passive observation, which is pretty surprising to me."
>
> "如果你在五到十年前问我，我会说……你可能需要理解直觉物理……神经科学中有很多理论，叫做'行动中的知觉'——你需要在世界中行动才能真正深度感知它……但现在看起来，你可以通过被动观察来理解它，这让我相当惊讶。"

### 4.2 Veo 3 的物理能力

- 流体动力学（液体、材料行为）
- 镜面光照（specular lighting）
- 直觉物理：像人类儿童那样理解"东西应该怎样运作"

> "I used to write physics engines and graphics engines in my early days in gaming, and I know it's just so painstakingly hard to build programs that can do that. And yet somehow these systems are reverse engineering from just watching YouTube videos."
>
> "我早年在游戏行业写物理引擎和图形引擎，我知道构建能实现这些的程序有多困难。然而这些系统仅仅通过观看 YouTube 视频，就在反向工程这些能力。"

### 4.3 这对理解现实本质意味着什么

> "Presumably what's happening is it's extracting some underlying structure around how these materials behave. So perhaps there is some kind of lower dimensional manifold that can be learned if we actually fully understood what's going on under the hood. That's maybe true of most of reality."
>
> "推测它是在提取关于这些材料如何行为的某种底层结构。所以也许存在某种可学习的低维流形——如果我们完全理解底层发生了什么。这也许对大部分现实都是成立的。"

### 4.4 理解的定义

> "I think to the extent that it can predict the next frames in a coherent way. That is a form of understanding, right? Not in the anthropomorphic version... They certainly have modeled enough of the dynamics... It's more of an intuitive physics understanding."
>
> "我认为，在它能连贯地预测下一帧的程度上，那是一种理解的形式——不是人类学意义上的深层次哲学理解……它们确实建模了足够的动力学……更像是一种直觉物理的理解。"

这直接挑战了"只有具身 AI（机器人）才能真正理解物理世界"的观点。

---

## 五、虚拟细胞（Virtual Cell）

### 5.1 25 年的梦想

> "Virtual cell, which is what I call the project of modeling a cell, I've had this idea of wanting to do that for maybe more like 25 years. And I used to talk with Paul Nurse, who is a bit of a mentor of mine in biology."
>
> "虚拟细胞——我称之为建模一个细胞的项目——我想做这件事已经有大概 25 年了。我过去经常和 Paul Nurse 讨论，他是我在生物学方面的mentor，Crick 研究所的创始人，2001 年诺贝尔奖得主。"

### 5.2 渐进路线图

Demis 的战略：将宏大梦想分解为可管理的中间步骤。

1. **AlphaFold 2**：蛋白质静态 3D 结构
2. **AlphaFold 3**：蛋白质-蛋白质、蛋白质-RNA/DNA 的双向交互
3. **下一步**：建模整个通路（pathway），如 TOR 通路（涉及癌症）
4. **最终**：全细胞模拟

### 5.3 从酵母细胞开始

> "I'd probably start with a yeast cell... the yeast cell is like a full organism that's a single cell... Yeast is very well understood. So that would be a good candidate for a kind of full simulated model."
>
> "我可能会从酵母细胞开始……酵母细胞既是一个完整的生物体，又是一个单细胞……酵母被研究得非常透彻。所以它是一个很好的全模拟模型的候选。"

### 5.4 梦想：100 倍加速实验

- 大部分实验在**计算机模拟**中进行
- 最终验证步骤才在**湿实验室**中进行
- 生物学实验速度提高 100 倍

### 5.5 建模的粒度选择

> "You got to make a decision when you're modeling any natural system, what is the cutoff level of the granularity that you're gonna model it to... Probably for a cell, I would hope that would be the protein level and that one wouldn't have to go down to the atomic level."
>
> "在建模任何自然系统时，你必须决定建模的粒度截止水平……对于细胞来说，我希望是蛋白质水平，不需要下到原子水平。"

不同的时间尺度也是一个挑战——蛋白质折叠极快，但某些生物过程很慢，可能需要多个不同时间动态的模拟系统协同工作。

### 5.6 生命的起源

Demis 认为在虚拟细胞之后，下一步可以探索：
- 从化学"原始汤"开始，设定初始条件
- 能否生成看起来像细胞的东西？
- 这是一个通过组合空间的搜索过程

> "Perhaps that would be a next stage after the virtual cell project is, well, how could you actually something like that emerge from the chemical soup?"
>
> "也许在虚拟细胞项目之后的下一阶段是：如何让类似的东西从化学汤中涌现出来？"

Lex 说希望生命起源也有一个 "Move 37"。

### 5.7 生命与非生命的连续体

> "I think ultimately what we'll figure out is there's a continuum. There's no such thing as a line between non-living and living... That it's not a line that it's a continuum, that connects physics and chemistry and biology."
>
> "我认为最终我们会发现的是一个连续体。不存在非生命与生命之间的界线……它不是一条线，而是一个连续体，连接了物理学、化学和生物学。"

---

## 六、研究品味与假设二分法

### 6.1 研究品味（Research Taste）

> "I think that's gonna be one of the hardest things to mimic or model is this idea of taste or judgment. I think that's what separates the great scientists from the good scientists."
>
> "我认为最难模仿或建模的事情之一就是品味或判断力的概念。我认为这是区分伟大科学家和优秀科学家的东西。"

- 所有职业科学家在技术上都是好的，否则无法在学术界走那么远
- 但**品味**——嗅出正确的方向、正确的实验、正确的问题——是区分因素

### 6.2 提出 conjecture 比解决 conjecture 更难

> "It's harder to come up with a conjecture, a really good conjecture than it is to solve it."
>
> "提出一个好的猜想比解决它更难。"

- AlphaProof 已经在数学奥林匹克中获得银牌
- 也许最终能解决 Millennium Prize 级别的问题
- 但能否提出一个 Terence Tao 都觉得深刻的新猜想？这是完全不同级别的创造力

### 6.3 假设二分法（Splitting the Hypothesis Space）

> "There's no such thing as failure really as long as you are picking experiments and hypotheses that meaningfully split the hypothesis space."
>
> "只要你选择的实验和假设能有意义地将假设空间一分为二，就其实不存在失败这回事。"

- 精心设计的实验，**无论成功还是失败都同样有价值**
- 失败告诉你该往哪里走——这在本质上是一次二分搜索
- 这是一种高度创造性的过程，单纯的"模型上的搜索"无法做到

### 6.4 "像爱因斯坦那样的想象力跳跃"

> "This kind of leap of imagination, like Einstein had when he came up with special relativity and then general relativity with the knowledge you had at the time."
>
> "这种想象力的跳跃，就像爱因斯坦凭借当时的知识提出狭义相对论和广义相对论那样。"

当前的 AI 系统显然做不到这一点，我们也不确定需要怎样的机制。

---

## 七、AlphaEvolve：进化算法 + LLM

### 7.1 混合系统的潜力

> "LLMs are kind of proposing some possible solutions and then you use evolutionary computing on top to find some novel part of the search space."
>
> "LLM 提出一些可能的解决方案，然后在上面使用进化计算来找到搜索空间中的一些新颖部分。"

这是一个非常有前景的方向：**将基础模型与其他计算技术结合**。

可能的组合：
- LLM + 蒙特卡洛树搜索
- LLM + 进化算法
- 各种搜索/推理算法叠加在基础模型之上

### 7.2 传统进化计算的局限与突破

> "The problem with naive traditional evolutionary computing methods... they could never work out how to evolve new properties, new emergent properties. You always had a subset of the properties that you put into the system. But maybe if we combine them with these foundation models, perhaps we can overcome that limitation."
>
> "传统进化计算方法的问题是……它们从来没能找到如何进化出新属性、新涌现属性的方法。你得到的总是你放入系统的属性的子集。但也许如果我们将它们与基础模型结合，就能克服这个限制。"

自然界中进化确实演化出了新能力（从细菌到人类），所以原理上必须是可能的。

### 7.3 递归自我改进

Lex 提出 AlphaEvolve 可能实现递归自我改进。

Demis 的回应：
- 当前系统更适合**增量改进**（如更快的矩阵乘法），给定非常具体的指令
- 做大跨度的飞跃（如发明 Transformer 架构）则完全不同
- 能否从现在起只需要增量改进，还是还需要一到两个大突破？这是开放问题

---

## 八、AGI 的定义与时间线

### 8.1 时间估计

> "My estimate is sort of 50% chance by in the next five years. So by 2030 let's say."
>
> "我的估计是未来五年内大约 50% 的概率，也就是到 2030 年左右。"

### 8.2 Demis 的 AGI 高标准

> "Mine's quite a high bar and always has been of like, can we match the cognitive functions that the brain has? Right, so we know our brains are pretty much general Turing machines, approximate. And of course we created incredible modern civilization with our minds. So that also speaks to how general the brain is."
>
> "我的标准一直很高：我们能否匹配大脑所拥有的认知功能？我们知道我们的大脑差不多是通用的图灵机——近似地。当然，我们用我们的心智创造了不可思议的现代文明。这也说明大脑有多么通用。"

AGI 必须满足：
- **不是锯齿状智能**（jagged intelligence）——在所有领域保持一致性
- 不能有些地方极好（如今天的系统）、有些地方极差
- 必须具备**真正的发明能力和创造力**

### 8.3 如何测试 AGI？

两种方式：

1. **广度测试**：数万个认知任务（人类能做的所有事情）
2. **深度测试**：让几百个世界顶级专家（各领域的 "Terence Tao"）使用一两个月，看能否找到明显缺陷

### 8.4 "灯塔时刻"：Move 37 级别的事件

> "There are the sort of lighthouse moments like the move 37 that I would be looking for."
>
> "有些像 Move 37 那样的'灯塔时刻'是我会寻找的。"

Demis 给出的具体测试：

1. **提出新猜想**：将知识截止在 1900 年，给系统所有 1900 年前的文献，看它能否独立提出狭义和广义相对论
2. **发明像围棋一样深刻的游戏**：不仅是新策略，而是发明一个审美上美丽、深度上不亚于围棋的新游戏
3. 不只是一个领域——**多个领域**都能做到才真正通用

### 8.5 人类会不会"错过"AGI 的突破？

> "The analogy I give there is... if I was to talk to Garry Kasparov or Magnus Carlsen and play a game with them and they make a brilliant move, I might not be able to come up with that move, but they could explain why afterwards that move made sense."
>
> "我给出的类比是……如果我和 Garry Kasparov 或 Magnus Carlsen 下棋，他们走了一步绝妙的棋，我可能自己想不出那步棋，但他们事后可以解释为什么那步棋是合理的。"

- AGI 的发现不会被最好的科学家完全无法理解
- 但可能需要 AI **解释其推理过程**——这本身就是智能的一部分

---

## 九、天气预测：非线性动力系统的可建模性

### 9.1 WeatherNext 系统

> "We've created the best weather prediction systems in the world and they're better than traditional fluid dynamics sort of systems that usually calculated on massive supercomputers, takes days to calculate it."
>
> "我们创造了世界上最好的天气预测系统，它们比传统的流体动力学系统更好——后者通常在大型超级计算机上计算，需要数天时间。"

- 流体动力学、Navier-Stokes 方程传统上被认为极难在经典系统上处理
- 但神经网络系统已经可以建模天气动力学的大部分有趣方面
- 包括最近的飓风路径预测

---

## 十、Scaling Laws 与 AI 进步的瓶颈

### 10.1 三个并行的 Scaling

> "We certainly feel there's a lot more room just in the scaling. So actually all steps, pre-training, post-training, and inference time. So there's sort of three scalings that are happening concurrently."
>
> "我们确实觉得仅在 scaling 方面还有很大空间。实际上所有步骤——预训练、后训练和推理时间——这三种 scaling 正在同时进行。"

### 10.2 是否需要新突破？50/50

> "I would say it's kind of 50/50 whether new things are needed or whether the scaling of the existing stuff is gonna be enough."
>
> "我会说大约是 50/50——是需要新东西，还是现有方法的 scaling 就足够了。"

DeepMind 的策略：**两条路同时全力推进**
- 一半资源投入全新的蓝天想法
- 一半资源投入当前能力最大化的 scaling

### 10.3 当"地形变难"的时候

> "I'm actually quite like it when the terrain gets harder. Because then it veers more from just engineering to true research."
>
> "我其实很喜欢当地形变难的时候。因为那时它从单纯的工程转向真正的研究。"

### 10.4 数据问题

> "I'm not very worried about that, partly because I think there's enough data... Do you have enough data to make simulations so that you can create more synthetic data that are from the right distribution."
>
> "我不太担心这个问题，部分因为我认为有足够的数据……你是否有足够的数据来制作模拟，从而生成来自正确分布的合成数据。"

关键是：需要**足够的真实世界数据来创建数据生成器**，然后合成数据就能接管。

---

## 十一、计算力、能源与文明未来

### 11.1 计算力的持续需求

- **训练计算**：需要协同定位，有带宽约束
- **推理计算**：AI 产品被数十亿人使用
- **思考系统**（thinking systems）：推理时间越长越聪明

> "The training side actually is only just one part of that, it may even become the smaller part of what's needed."
>
> "训练方面实际上只是其中一部分，甚至可能成为所需总量中较小的一部分。"

### 11.2 未来能源：聚变 + 太阳能

> "I think fusion and solar are the two that I would bet on."
>
> "我认为聚变和太阳能是我会押注的两个方向。"

- 太阳能："天空中的聚变反应堆"——关键是电池和传输
- 聚变：如果有正确的反应堆设计和足够快的等离子体控制，是肯定可行的
- AI 已经在帮助：等离子体约束（与 Commonwealth Fusion 合作）、反应堆设计、新型太阳能材料、室温超导体、最优电池

### 11.3 100 年内达到 Type I 文明？

> "I would not be that surprised if there was a like a 100-year time scale from here."
>
> "如果从现在的 100 年时间尺度来看，我不会太惊讶。"

- 能源免费 → 水问题解决（海水淡化不再昂贵）
- 无限火箭燃料 → 太空像公交服务
- 小行星采矿成为现实
- Carl Sagan 的愿景：将意识带到宇宙，唤醒宇宙

### 11.4 激进丰裕时代

> "For the first time in human history, we wouldn't be resource constrained. And I think that could be amazing new era for humanity where it's not zero sum."
>
> "人类历史上第一次，我们不再受资源约束。我认为这对人类而言可能是一个了不起的新时代——不再是零和博弈。"

---

## 十二、Gemini 的逆袭：从落后到领先

### 12.1 一年内的巨变

Lex 指出 Google 一年前在 LLM 产品上落后，现在 Gemini 2.5 领先。

> "It's absolutely incredible team that we have... led by Koray and Jeff Dean and Oriol and the amazing team we have on Gemini, absolutely world class."
>
> "我们拥有绝对不可思议的团队……由 Koray、Jeff Dean、Oriol 领导，以及 Gemini 的优秀团队，绝对是世界级的。"

关键要素：
- 最好的**人才**
- 充足的**计算资源**
- **研究文化**：将 Google Brain 和 DeepMind 的人才与思想汇聚
- **"无情的进步"+"无情的交付"**

### 12.2 大公司的官僚主义挑战

> "I still operate and I was always operating with old DeepMind as a startup still... And acting with decisiveness and the energy that you get from the best smaller organizations."
>
> "我仍然以创业公司的方式运作 DeepMind……以果断和来自最优小组织的能量行事。"

- 最佳组合：世界级研究 + 数十亿用户的产品表面
- "持续砍掉官僚主义"

### 12.3 AI 产品设计哲学

> "You've got to design not for what the thing can do today, the technology can do today, but in a year's time."
>
> "你必须设计的不是技术今天能做什么，而是一年后能做什么。"

- 模型列车正在飞速前进——产品需要**拦截**即将到来的能力
- 当前文本框聊天 UI 可能在几年后看起来很原始
- 未来方向：AI 生成的、个性化界面（适应你的审美、大脑工作方式）

### 12.4 版本号的含义

- **大版本**（2.5 → 3.0）：新的完整"英雄训练运行"（hero run），收集 6 个月的架构/数据创新
- **小版本**：基于同一架构的后训练补丁或思路
- **不同尺寸**（Pro、Flash、Flash-Lite）：从最大模型蒸馏而来
- 目标：定义 **Pareto 前沿**（性能 vs. 速度/成本的权衡）

---

## 十三、基准测试的问题

> "You need them, but it's important that you don't over fit to them."
>
> "你需要它们，但重要的是不要过度拟合。"

- 多目标优化：不能只在 coding 上好
- "无悔改进"（no regret improvements）：在某方面改进但不降低其他方面
- 产品中的**终端用户信号**越来越重要
- 人格风格（简洁 vs. 详细、幽默程度）也变成了产品空间的新问题

---

## 十四、人才战争与经济变革

### 14.1 Meta 的高薪策略

> "Meta right now are not at the frontier. Maybe they'll manage to get back on there... There's more important things than just money."
>
> "Meta 现在不在前沿。也许他们会设法回来……有比金钱更重要的事情。"

- 真正信仰 AGI 使命的人，更关心的是**在前沿影响技术走向、安全地管理它**
- 回忆起 2010 年 DeepMind 创立时，Demis 几年不给自己发工资
- 现在实习生的薪酬相当于当年的整个种子轮

### 14.2 程序员的工作

> "I think for the next era, like the next five, 10 years, I think what we're gonna find is people who embrace these technologies become almost at one with them... become sort of superhumanly productive."
>
> "我认为在未来五到十年，我们会发现拥抱这些技术的人几乎与它们合为一体……变得超级高产。"

- 顶级程序员将 10 倍于现在的高产
- 编程变得更易得 → 更多创意人士可以参与
- 人类的价值在于：**指定架构应该是什么、提出正确问题、评估 AI 生成的代码**

### 14.3 比工业革命快 10 倍的影响

> "I think what we're gonna see is something like probably 10 times the impact the industrial revolution had but 10 times faster as well."
>
> "我认为我们将看到的影响力大概是工业革命的 10 倍，但速度也快 10 倍。"

- 不是 100 年，而是 10 年
- 这意味着**社会适应难度极大**
- 需要顶级经济学家和哲学家开始思考：全民基本供给（universal basic provision）

---

## 十五、AI 安全与地缘政治

### 15.1 P(doom)

> "I don't have a p doom number. The reason I don't is because I think it would imply a level of precision that is not there... What I would say is it's definitely non-zero and it's probably non-negligible."
>
> "我没有 p(doom) 数字。原因是这暗示了一种不存在的精确度……我会说它绝对不是零，而且可能不是可忽略的。"

在高度不确定性 + 双向巨大赌注的条件下，**唯一合理的态度是谨慎乐观（cautious optimism）**。

### 15.2 双重风险

1. **坏行为体**使用通用技术作恶（个人或流氓国家）
2. **系统本身**越来越自主、越来越接近 AGI——如何确保受控

### 15.3 开放科学的困境

> "How does one restrict bad actors access to these powerful systems... but enable access at the same time to good actors to maximally build on top of. It's a pretty tricky problem."
>
> "如何限制坏行为体访问这些强大系统……同时又能让好行为体最大程度地在其上构建？这是一个相当棘手的问题。"

### 15.4 希望：类似 CERN 而非 Manhattan Project

> "I hope we'll end up with something more collaborative if needed. Like more like a CERN project... where it's research focused and the best minds in the world come together to carefully complete the final steps."
>
> "我希望我们最终得到的是更具协作性的东西——更像一个 CERN 项目……以研究为重点，世界上最优秀的头脑汇聚在一起，小心地完成最后步骤。"

- 科学一直是协作性事业，可以作为合作的向量
- 研究人员之间保持沟通至关重要

---

## 十六、John von Neumann 与《The Maniac》

### 16.1 如果 von Neumann 看到今天

> "I think he would've loved where we are today. And he would've really enjoyed AlphaGo being a game... I'm not sure how even maybe he wouldn't even be that surprised. There's the fruition of what I think he already foresaw in the 1950s."
>
> "我认为他会喜欢我们今天的成就。他会非常享受 AlphaGo 作为一个游戏……我不确定他会不会那么惊讶——这也许正是他在 1950 年代已经预见的事情的实现。"

- von Neumann 架构 → 所有现代计算机的基础
- 他称之为"生长而非编程"的学习机器
- 博弈论 + 人工智能 = AlphaGo 的天然交汇

### 16.2 纯粹的理性不够

> "Mad dreams of reason — it's not enough for guiding humanity as we build these super powerful technology."
>
> "理性的疯狂梦想——在构建这些超强技术时，仅凭理性不足以引导人类。"

- 需要**精神维度/人文维度**
- 科学和艺术是同伴——Feynman 的花的例子
- Spinoza 的哲学：理解宇宙 + 理解我们在其中的位置
- 文艺复兴时期的人（如 Da Vinci）不会区分科学、艺术和宗教

---

## 十七、意识：碳基 vs. 硅基

### 17.1 经典计算还是量子计算？

> "Penrose is amazing thinker, one of the greatest of the modern era. And we've had a lot of discussions about this. Of course we cordially disagree... To my knowledge, they haven't found anything convincing yet. So my betting is that it's mostly just classical computing that's going on in the brain."
>
> "Penrose 是了不起的思想家，现代最伟大的思想家之一。我们对此有过很多讨论。当然，我们友好地保持分歧……据我所知，他们还没有找到任何令人信服的证据。所以我押注大脑中主要是经典计算。"

### 17.2 意识 = 信息被处理时的感觉？

> "One of the best definitions I like of consciousness is it's the way information feels when we process it."
>
> "我喜欢的一个关于意识的最佳定义是：它是信息在被我们处理时的感觉方式。"

### 17.3 不同基底的同理心

> "With an AI that's on silicon, we won't be able to rely on the second part. Even if it exhibits the first part, that behavior looks like a behavior of a conscious being... But we wouldn't know how it actually felt."
>
> "对于硅基的 AI，我们无法依赖第二部分（相同基底）。即使它表现出第一部分（相同行为）——行为看起来像一个有意识的存在……但我们不知道它实际感受如何。"

- 人类认为彼此有意识基于两点：(1) 相同行为，(2) 相同基底
- AI 只有 (1) 没有 (2)
- 也许通过 Neuralink 等神经接口，我们最终能感受硅基上的计算

### 17.4 构建 AI 是为了理解人脑

> "I always imagined that building AI, a kind of intelligent artifact, and then comparing that to the human mind and seeing what the differences were would be the best way to uncover what's special about the human mind, if indeed there is anything special."
>
> "我一直想象，构建 AI——一种智能人工制品——然后将其与人类心智比较，观察差异，将是揭示人类心智有什么特殊之处的最佳方式，如果确有什么特殊之处的话。"

- Demis 的神经科学博士研究海马体（记忆与想象力）
- "What I cannot create, I do not understand." — Richard Feynman

---

## 十八、游戏：作为宇宙的模拟

### 18.1 游戏的深层意义

> "Games are great little microcosm simulations of the world. They're simulations of the world too. They're simplified versions of some real world situation... It allows you to practice at them too."
>
> "游戏是世界的微缩模拟。它们也是世界的模拟——真实世界情境的简化版本……它让你能在其中练习。"

- 一生中只有十几次重大决策机会
- 游戏提供**安全、可重复的环境**来改进决策过程

### 18.2 输赢的哲学

> "Don't get carried away with victory and think you're just the best in the world. And the losses keep you humble and always knowing there's always something more to learn."
>
> "不要因胜利而得意忘形，认为自己就是世界第一。失败让你保持谦逊，始终知道总有更多可以学习的东西。"

- 本质上关乎**自我认知、自我改进**——不是打败别人
- 将挫折感转化为建设性的改进动力
- 真正的满足来自 mastery：以前做不到的事现在能做到了

### 18.3 未来的 AI 游戏

> "Maybe we are on the cusp in the next few years, five, 10 years of having AI systems that can truly create around your imagination, can sort of dynamically change the story and storytell the narrative around and make it dramatic no matter what you end up choosing."
>
> "也许在未来几年、五到十年内，我们将拥有能真正围绕你的想象力创造的 AI 系统——能动态改变故事、叙述叙事，无论你选择什么都能让它变得戏剧化。"

- 终极的"选择你自己的冒险"
- 互动版的 Veo，5-10 年后
- 玩家真正**共创**游戏（不是选择幻觉）

### 18.4 文明（Civilization）——Demis 最喜欢的游戏

- Civilization I 和 II 是他最喜欢的所有游戏
- 太花时间——必须小心不要沉迷

### 18.5 游戏塑造了 Demis 的思维

- Commodore Amiga 500 → 学会所有编程
- 90 年代游戏行业 = GPU、图形、物理引擎、AI 的前沿
- 技术 + 艺术 + 音乐 + 故事叙述 = 多学科融合
- 这种多学科融合贯穿了他的一生

### 18.6 Demis 的"后 AGI 项目"

1. 创建一款视频游戏（回到最初的热情）
2. 研究物理学大统一理论

也可能通过 vibe coding 在空闲时间做游戏。

---

## 十九、协作、希望与人性

### 19.1 不把 AI 竞赛看作"输赢"

> "I try not to view it like a game or competition, even though that's a lot of my mindset. It's about... steward this unbelievable technology... safely into the world for the benefit of humanity."
>
> "我尽量不将其视为游戏或竞赛，尽管那是我思维模式的一大部分。关键在于……将这项不可思议的技术安全地管理到世界上，为人类的利益服务。"

### 19.2 与其他 AI 实验室领导人的关系

- 保持良好关系，与所有人（几乎）都有沟通渠道
- 情况更严峻时，这些沟通渠道将至关重要
- 希望看到更多实验室从事科学研究——更容易在科学问题上合作

### 19.3 希望之源

> "What gives me hope is that I think our almost limitless ingenuity... the best human minds are incredible... And then the other thing is our extreme adaptability."
>
> "给我希望的是我认为我们几乎无限的创造力……最优秀的人类心智令人难以置信……另一个是我们极强的适应性。"

- 狩猎采集者的大脑能应对现代世界（飞机、播客、AI 聊天机器人）——已经令人震惊
- 这只是下一步

---

## 附录：Lex 的结束独白 —— David Foster Wallace "This is Water"

（以下是 Lex 在访谈后的个人反思，Demis 未参与此部分。）

### "这就是水"寓言

> "There are these two young fish swimming along and they happen to meet an older fish swimming the other way, who nods at them and says, 'Morning, boys. How's the water?' And the two young fish swim on for a bit, and then eventually, one of them looks over at the other and goes, 'What the hell is water?'"
>
> "两条小鱼在水里游，碰巧遇到一条老鱼朝相反方向游来。老鱼朝他们点点头说：'早上好，小伙子们。水怎么样？'两条小鱼继续游了一会儿，最终其中一条看着另一条问：'水到底是什么鬼？'"

核心启示：
- 最明显、最重要的事实往往最难被看到和谈论
- 生命的精神战斗不在山顶修行——在**日常生活的平凡时刻**
- 每个瞬间都蕴含无限的丰富性——关键是 **"不被无聊打败"（be unborable）**

### Feynman 的花

> "I could imagine the cells in there, the complicated actions inside which also have beauty... It only adds."
>
> "我可以想象里面的细胞，内部的复杂活动——它们也有美……科学知识只会增加兴奋、神秘和敬畏，不会减少。"

---

*原始文案：/tmp/youtube_transcript.txt（148KB）*
*整理日期：2026-04-28*
