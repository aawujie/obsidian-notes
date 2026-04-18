---
notion-id: 2cc78d23-e296-8198-9ae7-cc340c6cf020
cover: "[[imgs/PPO连续动作空间实现细节（HalfCheetah示例）.jpeg]]"
Date: 2025-12-17
Last edited time: 2025-12-17T21:48:00
Tags: []
Link: https://youtu.be/BvZvx7ENZBw?si=0gGPAPnGxjAy2W3H
pic: https://img.youtube.com/vi/BvZvx7ENZBw/hqdefault.jpg
Verification: unverified
Owner:
  - AI generation
---
# 1. Metadata

- Title: PPO 在连续动作空间的实现细节（以 PyBullet 的 HalfCheetah 为例）
- Author: casa

# 2. Overview

本视频围绕如何将 PPO（Proximal Policy Optimization）从离散动作空间扩展到连续动作空间展开，重点讲述 8 个实现细节：用正态分布生成动作、如何生成与表示标准差、把动作分解为独立分量并累加概率与熵、对动作做裁剪（clip）、观测（observation）归一化、观测裁剪、奖励（reward）归一化与奖励裁剪等。视频演示基于 PyBullet 的 HalfCheetah 环境，最终展示加入归一化 wrappers（包装器）对训练初期表现的显著影响，并给出代码修改要点与实验观察。

# 3. 按照主题来梳理

## 3.1 从离散到连续：用正态分布生成动作

- 在离散动作空间（如 Atari）中，策略网络输出分类概率（categorical distribution），动作是整数标签（1, 2, 3...）。而在连续动作空间，策略要输出实数向量（例如 [-1.0, -0.8, 0.3, ...]），因此常用的方法是用正态分布（Normal distribution）来描述策略。
- 具体做法：策略网络对每个动作分量（action component）输出一个均值（mean），并配合一个标准差（standard deviation），二者定义一个一维正态分布；若动作有多维，就为每个维度建一组正态分布；最终的动作是在这些独立正态分布上采样得到的各个分量组合而成（即把分量拼接成动作向量）。
- 代码层面要点：
    - 从 PyTorch 导入 Normal 分布类（torch.distributions.Normal），用 mean 和 std 构造分布。
    - 把 actor 网络最后一层的输出特征数改为动作向量维度（action_space.shape 的乘积）；例如 HalfCheetah 的动作维度可能是 6，就把线性层输出改为 6。
    - 在 forward 中得到 mean 向量，再结合 std（见下一节如何生成）创建 Normal，然后调用 sample() 得到动作，同时计算 log_prob（用于优化）和 entropy（用于熵正则）。
- 为什么用正态分布合理：策略梯度方法需要策略概率的可微表示；正态分布在连续空间上是自然选择，而且 log_prob 与 entropy 的计算在优化中可直接使用。
- 保持可训练性：mean 来自网络输入状态（state-dependent），这样策略可以随状态改变而调整动作期望；std 也要可学习，但常见实现里它可以是状态无关的 learnable 参数（见下一节）。

## 3.2 标准差的表示：学 log_std（对数标准差）且与状态独立

- 视频指出一个“不太直观”的实现：不直接用网络输出标准差（std），而是学习对数标准差（log_std），并且让 log_std 成为不接收状态输入的可学习参数（parameter），即 state-independent（与状态无关）。
- 具体实现细节：
    - 在 actor 模块内部创建一个可训练的向量 log_std，维度等于动作维度（或与 mean 的首维匹配）。初始通常设为 0（即 std=exp(0)=1）。
    - 在 forward 时先从网络得到 mean（依赖状态）；然后把 log_std 扩展以匹配 mean 的 batch 维度（例如通过 repeat 或 expand），再对其做 exponentiation 得到 std = exp(log_std)。
    - 利用 mean 和 std 构造正态分布：Normal(mean, std)。
- 为什么用 log_std 有优势：
    - 数学稳定性：直接优化 std（要求正值）会有约束，优化 log_std 更自然（可以直接在实数域优化），exp 后自动保证正值。
    - 参数维度更少、更稳定：当 log_std 与状态无关时，训练时不需要网络学习复杂的方差结构，通常能加速训练并减少过拟合。不过这也意味着策略的探索强度在不同状态间不变，这既是简化也是潜在限制（视任务而定）。
- 代码注意：
    - log_std 初始为零向量，维度为动作维度（举例中 log_std 的第一个维度匹配 num_envs 或 num_actions 的首维，这里示例 num_envs=4）。
    - 当需要根据 batch 计算时，把 log_std 扩展为与 mean 相同的 shape，然后做 exp。
    - 由 mean 与 std 构造 distrib 后，可直接使用 distrib.sample()、distrib.log_prob(action) 和 distrib.entropy()。

## 3.3 假设动作分量之间独立：累加 log_prob 与 entropy

- 在多维连续动作空间（例如动作向量有若干分量）里，视频采用了独立分量（independent components）的假设：动作向量的联合概率等于各分量概率的乘积。对应到对数空间，则 log_prob( a ) = sum_i log_prob_i(a_i)。
- 实现上：
    - 使用 torch.distributions.Normal 为每个分量生成独立的一维正态分布，并对每个分量计算 log_prob（返回一个向量）；随后沿动作维度求和以得到该时间步动作的总 log_prob。
    - entropy 也同样按分量计算并求和（Total entropy = sum_i entropy_i）。
- 这样做的好处与含义：
    - 简化建模：不需要建协方差矩阵或输出协方差结构，降低参数复杂度与计算复杂度。
    - 当动作分量确实相对独立时，这是合适的近似；若动作分量高度耦合（某些机械臂任务），独立假设会限制策略表现。
- 类比：视频还提到多离散（multi-discrete）动作空间（多个独立离散分量联合表示动作）也可以用相同思想：为每个离散分量分别计算 categorical 的 log_prob 与 entropy，再求和。并强调在 multi-discrete 中常需对无效动作做 mask（遮蔽），以避免训练错误（这是个侧注，具体实现可参考论文）。
- 训练数据一致性提示：即使 agent 在交互时执行的是被 clip 过的动作（见下节），策略存储的原始（未裁剪）动作仍用于 forward 存储，以保证训练时的前向传播/后向传播一致性。

## 3.4 向环境发送动作前进行裁剪（clip action）但存储原始动作

- 在连续动作空间中，action_space 会给出每个分量的 lower bound 和 upper bound（下界和上界），例如每个分量范围 [-1, 1]。策略采样得到的动作可能越界，因此需要在发送给环境前将动作裁剪到合法区间。
- 裁剪的实现和注意事项：
    - 使用一个 ClipAction wrapper（裁剪包装器）或者在 step 前调用 np.clip(action, low, high)；在视频中查看了 clip action wrapper 的源码，核心就是按每个维度把动作限制在 action_space 的 lower 与 upper 之间。
    - 重要原则：即便在交互时发送给环境的是裁剪后的动作（clipped action），但在存储 buffer 或 trajectory 时仍保存原始采样的动作（未裁剪）。原因是保持训练前向传播时的数值一致性，否则会出现 policy log_prob 与 action 不一致导致训练问题。
    - 环境实际执行裁剪动作：环境因为只接受合法动作，会执行裁剪后的动作，但存储数据（例如用于计算 advantage）使用的是原始动作。
- 实践建议：在实现 replay / rollouts 的存储时明确区分存储的“采样动作”和实际送入 env 的“执行动作”。同时保持 log_prob 计算用的是采样动作对应的概率（即与生成动作的分布一致）。
- 断言/检查：视频演示中修改了 assert 语句以排除原本仅为离散动作空间设计的断言逻辑，确保在连续空间下不会触发不合理检查。

## 3.5 观测（Observation）归一化：用 RMS 跟踪均值与标准差并做标准化

- 视频介绍在原实现里对观测进行大量预处理，其中重要的一步是观测标准化（standardization）：使用一个运行时均值与标准差估计器（running mean and std，简称 rms）来将每个观测 x 变换为 (x - mean) / std，从而得到近似零均值、单位方差的输入。
- 实现要点：
    - 建立一个 RMS 类用于在线更新：每次 env 返回 observation 时调用 normalize()，该函数首先用新观测更新 running mean 和 running variance，然后用当前估计的 mean 与 std 对观测做标准化。
    - 公式与统计学依据：以增量方式维护均值与方差的估计，目的是在非平稳数据流中逐步跟踪统计特性，从而避免一次性读取大量数据来计算。
- 为何要做观测标准化：
    - 不同特征尺度差异会导致网络训练不稳定或收敛慢；归一化后能提升优化效果，使学习率、初始化更通用。
    - 对连续动作任务尤其有用，因为网络输出与状态尺度强相关，稳定的输入尺度减少了策略与价值网络之间的相互影响。
- 实践细节：
    - normalize 函数通常会返回归一化后的 tensor；在训练与推理阶段都使用相同的 normalize 步骤，保证数据一致性。
    - 需要小心初始阶段的 std 非常小（防止除以零），通常在计算时会加上 epsilon（小常数）以数值稳定。
- 视频结果对比：加入归一化的实验在训练初期能显著提高 episodic return 的上升速度，尽管最终收敛值可能类似，但归一化能减少训练震荡并显著缩小 value loss 的规模（这是因为 reward normalization 也会影响 value 估计尺度）。

## 3.6 观测裁剪（Observation Clipping）

- 在做完观测标准化后，视频继续对归一化后的观测做裁剪（clipping），以避免极端值对网络产生不良影响。
- 实现方式：
    - 在 make_env（环境创建函数）中使用 TransformObservation wrapper 或类似机制，通过 lambda 函数将 normalize(observation) 后的数值限制在某个区间，例如 [-10, 10]（视频取值）。
    - 这一层是最后一步的观测处理：normalize -> clip -> 返回给 agent。
- 为什么要裁剪：
    - 标准化过程中依赖运行统计量，在异常回报或突发事件下，观测可能产生极值，直接输入网络可能造成梯度爆炸或不稳定。
    - 裁剪能保证输入在一个受限范围内，减少 outlier 对模型训练造成的干扰，从而提高训练稳定性。
- 参数选择与注意：
    - 裁剪阈值不是绝对值，视频中使用 [-10, 10]，这个范围是经验性的，具体可根据任务调整。
    - 裁剪前务必做标准化，裁剪原始观测易丢失尺度信息；先标准化再裁剪可以保留统计标准并限制异常。

## 3.7 奖励（Reward）归一化：对折扣回报（returns）做 RMS 标准化

- 视频指出 reward normalization 的实现有一处“奇怪”的设计：不是对即时 reward 做 RMS， 而是对折扣回报（discounted returns）做 RMS 并用其标准差来缩放“奖励/返回”。
- 实现细节：
    - 在 wrapper 中维护一个 RMS 用于折扣回报：每次 env 返回 reward 时，先计算该时间步的折扣回报（return），这里需要 gamma（折扣因子）作为类的一个参数来累积折扣回报值。
    - 调用 normalize 时：先更新 RMS 的值（用当前折扣回报作为样本），然后把原始 reward 除以 RMS 的标准差（return std）来做归一化。视频强调“不是减去均值，只是除以标准差”。
- 为什么对 returns 做 RMS：
    - 折扣回报反映了未来回报总体规模，使用 returns 的标准差来缩放 reward 可以让不同阶段、不同策略下的 reward 尺度保持一致，从而减小 value loss 尺度并让更新更稳定。
    - 注意这是对 returns 的统计，而非对单步 reward 的统计，因而考虑了折扣累积的时间结构。
- 影响：
    - reward normalization 会显著影响 value network 的损失尺度（视频观察到 value loss 减少），也因此影响训练稳定性与学习率的敏感性。
    - 在某些情况下，归一化能使训练更快收敛，但也可能掩盖某些 reward 结构细节；不同任务效果可能不同，需要实验验证。
- 代码实现提示：
    - 在计算 advantage 等需要 returns 的地方，使用同一套归一化逻辑以保持一致性。
    - 当用归一化的 reward 去训练时，若也使用归一化后的观测，二者一起对训练行为产生复合影响，需注意监控训练曲线。

## 3.8 奖励裁剪（Reward Clipping）

- 与观测裁剪类似，视频在 make_env 中对归一化后的 reward 做了裁剪（clipping），将 reward 限在 [-10, 10] 的区间内。
- 实现点：
    - 使用 TransformReward wrapper 或 lambda 函数对 normalize(reward) 的结果应用 np.clip 或类似操作，得到裁剪后的 reward。
    - 先归一化再裁剪（normalize -> clip），可以避免异常大的归一化值继续导致数值稳定性问题。
- 作用与理由：
    - 裁剪 reward 可以控制训练更新中的梯度尺度，避免单条 episode 或极端情况造成参数更新过大。
    - 当 reward 尺度多变或返回分布 heavy-tailed（重尾）时，裁剪常被用于稳定训练，特别是在强化学习的 bootstrap 与策略梯度计算中。
- 综合效果：
    - 视频对比实验（有无 normalization wrappers）的曲线显示，加入归一化与裁剪的脚手架在训练早期能提升 agent 的 episodic return 增长速度；但在长期收敛值上二者可能趋于相同（具体受任务与超参影响）。
    - reward normalization 与 reward clipping 通常与观测归一化配合使用，以实现整体的尺度稳定化。

# 4. 框架 & 心智模型（Framework & Mindset）

- 框架摘要：把连续动作空间的 PPO 实现拆分为两类任务 ——（A）策略类别/分布的选择与网络输出结构调整；（B）环境输入/输出的数值预处理与包装（wrappers）。这两类任务相互独立但需要协同设计。
    - A 部分（策略分布与网络输出）包括：用参数化分布（Normal）来表示策略、网络输出 mean、log_std 作为可训练参数、为每个动作维度假设独立并求和 log_prob/entropy、确保 log_prob 与采样动作一致。实现步骤：
        1. 确认 action_space.shape，调整 actor 网络最后一层输出为动作维度（action_dim）。
        2. 在 actor 中定义一个可训练的 log_std 向量（维度 = action_dim），初值通常为 0。
        3. forward 时计算 mean（state-dependent），把 log_std 扩展为 batch 形状并做 exp 得到 std。
        4. 用 Normal(mean, std) 构造分布，sample 出动作，计算 log_prob（按维度求和）与 entropy（按维度求和）。
        5. 在交互与存储时区分原始采样动作与裁剪后执行动作，训练时用采样动作和其 log_prob。
    - B 部分（输入/输出预处理）包括：观测归一化、观测裁剪、reward returns 的归一化、reward 裁剪、动作裁剪。实现步骤：
        1. 实现或复用一个 RunningMeanStd（RMS）工具，用于在线更新均值和方差，分别用于观测与折扣回报。
        2. 在 make_env 中封装 wrappers，按顺序：记录 statistics/视频、观测 normalize、观测 clip（如 [-10,10]）、reward returns normalize（用 gamma）、reward clip（如 [-10,10]）、action clip（执行前）。
        3. 在 buffer/rollout 存储中保证一致性：存储策略采样的原始动作与对应的 log_prob、但在与环境交互时送入裁剪后的动作；在 advantage、return 计算上使用归一化规则一致的 reward 或 returns。
        4. 调整超参数（learning rate、num_steps、num_mini_batches、update_epochs、entropy_coef 等）以适配连续任务规模，视频示例里修改了 lr=3e-4、total_timesteps=2e6、num_envs=1、num_steps=2048、num_minibatches=32、update_epochs=10、entropy_coef=0。
- 心智模型（Mindset）：
    - 保持数据尺度一致性：策略输出、观测、回报这些信号的尺度直接影响优化过程，归一化与裁剪是工程上关键的稳定化手段。不要假设原始观测或奖励尺度就是合适的。
    - 简化但谨慎：为方差使用 state-independent log_std 是一种工程上简化（减少参数、加快训练）但并非总是最优的理论选择。设计时要权衡模型容量与训练稳定性，必要时可用更复杂（state-dependent）方差模型做对比试验。
    - 先可运行后调优：把实现先做通用且可运行（包括 wrappers 与合理超参），再做消融（ablation）与对比实验来判断哪些 design decisions 真正重要。视频建议阅读相关论文以获得更系统的消融结论（例如涉及 normalization 的论文）。
    - 数据一致性优先：在交互/存储/训练的各环节保证数值与定义的一致（例如用采样动作计算 log_prob，但送 clipped action 给 env 执行），任何不一致都会导致难以发现的 bug 或训练失败。
- 实践建议（进一步步骤）：
    - 在尝试新环境（例如 car_racing-v0，像素输入且连续动作）时，把两个方向（像素处理与连续动作 handling）结合起来：先复用已有的像素预处理（frame stack、灰度/resize/归一化等）再接入连续动作的 actor 变体与归一化 wrappers。
    - 做好实验记录：区分操作系统、随机种子、超参，这些都会影响复现结果（视频里作者在 macOS 与 Linux 机上分别跑实验来验证差异）。

# 总结

本视频系统地展示了将 PPO 从离散动作空间迁移到连续动作空间时具体的实现步骤与工程细节。核心要点包括：用正态分布参数化策略并输出 mean；用 learnable 的 state-independent log_std 来表示方差；将多维动作视作独立分量并累加 log_prob 与 entropy；在交互时对动作做裁剪但在存储/训练时保留原始采样动作；并通过观测归一化/裁剪与折扣回报归一化/裁剪来稳定训练。实验表明，加入 normalization wrappers 在训练初期能显著提升表现并降低 value loss 的尺度，但最终 episodic return 在该任务上可能与未加入归一化的实现相近。视频最后提出练习：把这些实现扩展到既有像素观测又有连续动作的 car_racing-v0 环境，作者将其参考解答放在视频描述中。