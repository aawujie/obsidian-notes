---
notion-id: 2cc78d23-e296-8169-9af0-fa770d93ca56
cover: "[[imgs/从零实现PPO：11个关键工程化细节与实践指南.jpeg]]"
Date: 2025-12-17
Last edited time: 2025-12-17T21:47:00
Tags: []
Link: https://youtu.be/MEt6rrxH8W4?si=m_swexP80gJjUVGa
pic: https://img.youtube.com/vi/MEt6rrxH8W4/hqdefault.jpg
Verification: unverified
Owner:
  - AI generation
---
# 1. Metadata

- Title: 从零实现 PPO（Proximal Policy Optimization）——11 个实现细节与工程化建议
- Author: Costa（机器学习工程师实习生、Drexel University 第四年博士生，专攻强化学习）

# 2. Overview

本视频介绍了如何用 PyTorch 从头实现 OpenAI 在 2017 年提出的深度强化学习算法 Proximal Policy Optimization（PPO）。作者在讲解过程中覆盖了实际工程中常遇到的 11 个关键实现细节，并辅以开发工具（如 argparse、TensorBoard、Weights & Biases）与复现实验的配置方法。结论是：通过合理的环境封装（vector environments）、网络初始化、优化器参数设置、存储与批处理策略、优势估计（GAE）、目标与裁剪（clipping）、熵正则化、梯度裁剪与可选的早停机制，可以得到与开源实现行为接近且更稳定的 PPO 实现；并且这些实现细节在不同任务间通常只需少量修改即可复用。

# 3. 按照主题来梳理

## 3.1 开发环境与实验追踪（argparse、TensorBoard、Weights & Biases）

- 本节详细讲述了作者搭建开发环境和配置实验追踪的工作流与实践细节。作者个人偏好使用 pipx/pipenv/poetry（视频中用的是 poetry）来创建虚拟环境并安装依赖。实际代码入口为一个 Python 脚本，第一步用 argparse（作者说的是 arc parts，即 argparse）来定义一系列可通过命令行调整的超参数或运行配置。作者把每个参数定义为三部分：名称、类型与默认值，并为其添加帮助文本用于文档说明。常见的 hyper 参数示例包括：experiment name（默认脚本名）、gym id（默认 CartPole-v1）、learning rate（默认 2.5e-4）、random seed（默认 1）、total timesteps（环境步数，默认 25000）、torch deterministic（用于复现）、cuda（是否使用 GPU）等。作者强调，把这些配置放在命令行参数中可以在不改代码的情况下快速改变实验设置，对日常调试极其方便。
- TensorBoard：作者示范如何用 torch.utils.tensorboard.SummaryWriter 创建一个带有 run name 的目录来保存标量、文本等指标。具体实践包括把 args（超参数字典）序列化为文本并通过 add_text 保存；演示使用 add_scalar 添加用于监控的标量（如训练损失、episodic return）。作者提示可以启动 tensorboard 并通过 web 界面观察曲线（可调平滑参数）、查看超参数文本等，帮助调试与可视化训练过程。
- Weights & Biases（W&B）：视频展示如何在代码中加入一个 track 标志来决定是否向 W&B 上传数据；包括设置默认 project（作者用了 cleanrl）与 entity（可为 None 以使用默认用户名）。当开启时，W&B 会：自动与 TensorBoard 同步、记录 args 配置、上传 gym 的视频（需要在 env monitor/record 配合）、保存代码副本。作者强调这种按开关启动 cloud 追踪的方法既能保持本地运行的简洁，又能在需要时获得云端可视化与日志备份。示例命令如 python ppltrack 会快速运行并给出一个 W&B 链接，通过这个链接可以查看训练视频、loss 曲线、超参数元数据、文件列表和代码快照。
- 随机种子与设备设置：在完成追踪工具配置后，作者清理示例代码并设定随机数种子（random、numpy、torch），确保实验可复现。同时使用 torch.device 来选择 CPU 或 GPU（基于 cuda flag），并在使用 CUDA 时设置 torch 的确定性选项（torch_deterministic）以尽量复现。同样强调这些只是工程上常用的实践，目的是减少跑实验时的非确定性和便于结果比对。

## 3.2 环境封装与向量化（Vector Environments、Gym Wrapper）

- 本节重点解释 PPO 常用的“向量环境”（vector environments）概念及其工程化实现。传统使用 gym 的基本流程为：env = gym.make(...); obs = env.reset(); action = sample(); next_obs, reward, done, info = env.step(action)；当 done 为 True 时需手动调用 reset。作者指出在训练时经常会维护 episodic return 的统计，一种简单实现是代码里显式累积 reward 并在 done 时打印或存储。但更简洁的工程做法是使用 gym 提供的 wrapper（如 RecordEpisodeStatistics），它会在 episode 结束时把 episode 的 return 信息放入 info 中，从而免去了你自己维护统计的代码。再者使用 RecordVideo wrapper 可以在需要时录制 agent 的视频用于调试。
- 向量环境（VectorEnv）：PPO 实际上是对多个并行独立环境进行采样并拼接数据后再训练。作者构建了一个“make_env”工厂函数（返回创建单个 gym 环境的函数），然后使用 gym.vector.SyncVectorEnv 或类似 API 创建多个并行副本。向量环境依然使用 env.reset() 和 env.step(actions) 接口，但差异在于：当一个子环境结束（done），vector env 会自动在内部 reset 该子环境，并在 step 的返回中用下一 episode 的初始 observation 替换本次返回（即丢弃 terminal observation，返回的是新 episode 的 first observation）。因此处理返回值时不能再直接用单环境的 done/obs 处理方式，需要注意 info 里可能包含 episodic stats 来记录 episode 返回。
- 工程化细节：作者在创建 make_env 时加入了 capture_video 标志以便只对第一个子环境录视频，且在 make_env 中注入随机种子参数以便在不同子环境间使用不同 seed，从而提高训练数据的多样性。Num_envs（文中称 num_m）为向量化子环境数量，num_steps 则为每个子环境在一次 rollout 中采集的步数。最终每次 rollout 会得到 num_envs * num_steps 个 transition 数据点，作者称之为 batch size。作者还提示，如果使用 W&B 的 gym monitor（monitor_gym=True）可以自动上传视频到 W&B 控制台，便于观察 agent 在训练不同阶段的行为。最后作者在代码里加了断言确保环境为离散动作空间（Discrete），并打印 observation space 与 action space 的形状（以 CartPole 为例 observation 维度为 4，action 数为 2），用于后续网络维度设置与调试。

## 3.3 Agent 架构、参数初始化与网络细节（Actor-Critic、Orthogonal Init）

- 在实现 agent 时，作者创建了一个 Agent 类，其内部包含 actor（策略网络）与 critic（价值网络）。实现依赖 PyTorch 的 nn.Module、torch.optim 以及分布类（Categorical）来处理离散动作。关于网络结构，作者详细说明了两个网络的层级与激活：critic 为三层线性（Linear）层，激活函数使用 tanh（双曲正切），最后一层输出维度为 1（标量 value）；actor 结构类似，但最后一层输出维度等于动作空间大小（比如 CartPole 的 2），输出为 logits（未归一化的分数），随后通过 Categorical 分布进行 sample 或计算 log_prob。
- 参数初始化（关键实现细节 2）：作者强调不要使用 PyTorch 默认初始化，而应使用 PPO 原始实现中常用的“正交初始化”（orthogonal initialization）结合常量偏置（bias 常置为 0），以保持网络初始行为和梯度尺度一致性。具体实现是写一个 layer_init 函数：对 layer.weight 使用 nn.init.orthogonal_，并传入 gain 参数（标准差/增益）。常见的做法是隐藏层使用 gain = sqrt(2)（即隐层非线性激活的推荐值），最后一层（输出层）对 critic 使用 gain = 1，对于 actor 的最后一层使用 gain = 0.01（较小的初始化尺度以保证初始策略概率分布较为平滑）。作者说明这样做的目的是使得不同层参数的标量幅度相近，从而避免一开始策略过于偏向某些动作或 value 估计过大。
- 输入与输出形状：第一个线性层的输入维度为 observation_space.shape 的乘积（例如 CartPole 的 observation 是 (4,) 则输入为 4）。actor 的输出为 logits（长度等于动作数），critic 的输出为单个标量。作者还建议把 actor 和 critic 的前向推理（get_action_and_value）打包到一起执行，以减少重复计算：先算 actor logits、构建 Categorical、sample actions（rollout 阶段）并计算 log_probs 与 entropy，再用 critic 计算 values，最终将 actions/log_probs/entropies/values 一并返回以存储到 rollout buffer。

## 3.4 优化器、epsilon 与学习率退火（Adam eps、Annealing）

- Adam 优化器的 eps（epsilon）参数：PyTorch 默认的 Adam epsilon 是 1e-8，但原始 PPO 实现（以及很多开源实现）使用的是 1e-5。作者指出该细节看似微小，但会影响数值稳定性和训练行为，因此在实现中显式将 eps 设为 1e-5 来匹配原始实现。具体创建方式为 torch.optim.Adam(agent.parameters(), lr=learning_rate, eps=1e-5)。
- 学习率退火（关键实现细节 4）：作者在训练循环外计算总的 update 次数 num_updates（total_timesteps / batch_size）。引入 anneal_lr 标志，如果为真，则在第 u 次更新时将学习率设为 initial_lr * fraction，其中 fraction = 1 - (current_update / total_updates)。也就是线性衰减学习率，让 training 趋势更稳定并能在训练后期使用较小的步长进行微调。实际通过 PyTorch 的 param_groups 修改 optimizer 中的 lr 来实现。
- 全局步骤与计数：在 rollout 内部，作者每次对向量环境调用 step 时，将 global_step 增加 num_envs（因为每次 step 实际上是为所有子环境推进一步），并把 next_obs / next_done 存入对应的 storage 变量。storage 的形状通常是 (num_steps, num_envs, ...) 以便后续在切平（flatten）时得到 (batch_size, ...)。作者强调在 rollout 期间禁用梯度计算（torch.no_grad）来避免不必要的内存占用和计算负担。

## 3.5 Rollout 存储、批次划分与训练循环（num_steps、batch_size、minibatches）

- Rollout 与 batch size 的定义：作者定义 num_steps（每子环境收集的步数）和 num_envs（向量环境数量），因此一次 rollout 的 batch_size = num_steps * num_envs（例如 num_steps=128，num_envs=4 则 batch_size=512）。total_timesteps 除以 batch_size 得到 total_updates（训练更新次数）。这是训练循环的外层迭代次数；每次外层迭代会完成一次完整的 rollout 收集与若干次参数更新。
- Storage 变量：在 rollout 阶段，代码会依序把每步的 obs, actions, log_probs, rewards, dones, values 等信息保存在预先分配好的 tensor（shape 根据 num_steps x num_envs）中。rollout 结束后要对这些数组做 flatten（通常按先时间后环境或先环境后时间的顺序）得到一维索引 batch，以便做随机抽样小批量训练。
- 小批训练策略（关键实现细节 6）：PPO 的做法是将一个 batch（例如 512）划分为若干个 mini-batch（例如 4 个），每个 mini-batch 的大小为 batch_size / n_minibatches（例子中为 128）。同时设置 update_epochs（例如 4），表示对整个 batch 做若干个 epoch 的更新。在每个 epoch 内，会随机打乱 batch indices 并按 mini-batch 大小切分索引，然后对每个 mini-batch 进行前向计算与损失回传。这样的做法与公开实现一致：使用多次 epoch 与小批梯度来提高样本效率并稳定训练。
- 前向计算注意事项：在小批训练时，需要将 old log_probs 与 old values（rollout 中记录的）作为常量传入模型，以便计算新的 log_probs 与 value 并与旧值比较（用于计算 ratio、value_clip 等）。因此在 agent 的 forward/get_action_and_value 中应提供 actions 参数以便输出对应动作下的新 log_prob 与 value，而不是重新采样动作（sample）从而破坏旧动作的对比关系。
- 随机打乱与索引抽样：作者示范用 numpy.arange(batch_size) 生成索引并在每个 epoch 时 shuffle。随后按步长 minibatch_size 选取索引子集，从而构成 mini-batch 的训练数据。这样保证了数据在多个 epoch 中会以不同的顺序进入训练，从而减小过拟合。

## 3.6 优势估计（GAE）与返回计算（advantages、returns）

- GAE（Generalized Advantage Estimation，关键实现细节 5）：作者建议在实现中加入 gae 标志来选择是否使用 GAE。若启用，则需要定义 gamma（折扣因子，如 0.99）和 gae_lambda（如 0.95）。GAE 通过对 temporal-difference residuals（δ_t = r_t + γ V_{t+1} - V_t）做衰减加权累加来得到 advantage。作者从原始仓库中复制了一个较为复杂但更接近真实实现的 GAE 计算代码，强调其实现较公式更复杂，阅读时可以在纸上推导几个项来帮助理解。
- 引导（bootstrap）处理：当 rollout 在中途结束时（即某些环境并未完成 episode），PPO 会对末端的 next_value 做引导估计（bootstrap）。也就是说在计算 GAE 时，如果 environment 在 rollout 末端未 done，则用 critic 对 next_obs 的估计值作为 V_{T} 来计算 δ_{T-1}。作者指出这与纯粹用 sum of discounted rewards 的 returns 不同，GAE 的 returns（用于 value function 回归）是 advantages + values（即 empirical returns = advantages + values），而不是直接的 discounted cumulative reward。作者用 IDE 查看变量以对比 GAEs 的 returns 与普通 returns 的差异，保证实现正确。
- 扁平化存储：在计算完 advantages 与 returns 后，作者会将所有存储的变量 flatten（batch_size 大小）以便后续的 mini-batch 抽样与训练。通常 advantages 会被标准化（见下一节）以改善训练稳定性。

## 3.7 优化目标与正则化（剪切目标、价值裁剪、熵正则化、梯度裁剪、额外指标）

- 剪切的策略目标（Clipped Policy Objective，关键实现细节 8）：PPO 的核心是通过对概率比率 r_t(θ) = π_θ(a_t|s_t) / π_{θ_old}(a_t|s_t) 进行裁剪来限制策略更新幅度。作者实现中设置 clip_coef（默认 0.2），并计算两项：unclipped = r_t * adv_t，clipped = clamp(r_t, 1 - clip_coef, 1 + clip_coef) * adv_t。策略损失取这两者的最小值（或说取负数后取最大），最后取平均。作者指出实现方式与论文等价，但在代码上用 max/min 的写法有些实现差异。
- 价值函数裁剪（Value Loss Clipping，关键实现细节 9）：为避免 value 网络发生剧烈更新，原始实现也对 value 的变化做了裁剪（类似于对 r_t 做裁剪）。实现方式为计算 value_pred 与 value_pred_clipped（value_old + clip(value_pred - value_old, -clip_coef, clip_coef)），然后分别与 returns 计算 MSE，取二者的最大作为 value_loss。作者同时提供 val_clip flag 来控制是否启用该项。
- 熵损失（Entropy Bonus，关键实现细节 10）：为了鼓励策略探索，PPO 在总损失中会加入 -entropy * entropy_coef（因为我们最小化损失而想最大化熵）。作者默认 entropy_coef = 0.01，value_loss_coef = 0.5。总损失 = policy_loss + value_loss_coef * value_loss - entropy_coef * entropy（注意符号）。解释上，增加熵会使行动分布更加平滑与多样，从而防止过早收敛到确定性策略。
- 梯度裁剪（Global Gradient Clipping，关键实现细节 11）：在反向传播前计算总损失并调用 loss.backward()，随后使用 torch.nn.utils.clip_grad_norm_(agent.parameters(), max_grad_norm) 对梯度进行裁剪（默认 max_grad_norm=0.5）。这样可以防止梯度爆炸并使参数更新更稳定。作者强调这是生产级实现的常见做法。
- 额外诊断指标：作者提到原实现中还会计算 approx_kl（近似 KL 散度，原实现用 -mean(log_ratio)），以及 clipped_fraction（衡量多少比例的样本触发了 clipping），还有 explained_variance（用于评估 value function 预测 return 的能力）。作者还提到 John Schulman 的一篇博客中提出了更好的 KL 近似计算方式，暗示这些诊断指标有助于理解更新激进程度与价值网络的解释性。

## 3.8 早停（Early Stopping based on KL）与实验记录

- 早停的思想（Bonus Implementation）：作者介绍了 Joshua Achiam 在 OpenAI Spinning Up 推荐的一个实现细节：在每次更新 epoch 中监测 approximate KL，如果超过 target_kl（例如 0.015），则提前停止当前 update 的更多 epochs（即早停）。这样可以在局部避免策略更新过度，保持训练的稳定性。作者在实现中将 target_kl 设置为 None（默认不启用），但提供了可选参数以便实验时打开。
- 实验记录回顾：训练结束后，作者演示如何在 W&B 控制台中查看上传的视频、loss 分解（policy_loss、value_loss、entropy）、episodic returns/lengths、超参数、代码快照、requirements.txt 以及系统资源使用情况。作者也提到在本次示例中训练很快（18s），因此系统指标数据点较少，但示例说明了从代码到云端观测整个流程的闭环。

# 4. 框架 & 心智模型（Framework & Mindset）

- 框架与心智模型总览：作者在视频中呈现出一种面向工程化与可复现性的实现心智模型，适用于将论文算法转化为可运行代码并在现实实验中稳定复现。这一心智模型可以整理为若干步骤和原则，便于在实现任何强化学习算法（不仅限 PPO）时作为行动指南。以下将这些原则展开为清晰步骤与 rationale，每项不少于 500 字。
1. 明确可配置化与命令行优先（Configuration-first）
    - 思路：所有可调节的超参数与运行配置都应通过命令行参数或配置文件暴露，而不是硬编码在代码里。这使得实验可复现、可追溯，并便于通过自动化工具（如脚本或 CI）批量跑不同配置的实验。作者的实践是使用 argparse 为每个变量设置名字、类型、默认值与帮助文本。重要参数包括环境 id、学习率、随机种子、总步数、num_envs、num_steps、clip 相关参数、优化器 eps、是否启用 GAE、是否启用学习率退火、是否上传到 W&B 等。
    - 原因：当在 tuning 或 debug 时频繁调整参数，命令行参数能极大缩短迭代周期，同时记录下每次实验真实使用的参数便于复现和比较。
    - 实践建议：保存 args 至 TensorBoard 文本与 W&B 配置（config），并在云端保存代码快照（W&B 提供此能力）。在日志系统中包含启动命令（完整的 python 命令行），确保别人或日后自己能按同样命令重现实验。
2. 从小处验证并逐步扩大（Small-to-large testing）
    - 思路：先在简单环境（如 CartPole）或小的 total_timesteps 下调试实现细节（网络维度、rollout 存储、优化更新逻辑、梯度流、shape 错配等），待实现与小规模实验通过后再放大训练量或换复杂环境（Atari、MuJoCo）。
    - 原因：强化学习实现复杂且容易出现 subtle 的 bug（shape mismatch、done/reset 的处理、向量环境的 terminal observation 行为等）。在小规模上快速验证能节省大量调试时间，且更容易对比梯度/loss 曲线与行为视频。
    - 实践建议：配合 TensorBoard/W&B 上传短时运行的 trace、视频、以及打印出的检查点（如第一步 rollouts 的 obs/action/logprob/value 的分布）来确认实现正确。
3. 严格处理环境边界与并行化细节（VectorEnv-as-primitive）
    - 思路：将并行环境（vector env）视为一个基本构件，理解其 step/reset 的语义差异（如 terminal observation 被替换为 next episode initial observation），并且在设计 rollouts buffer、done 处理和 value bootstrap 时按 vector semantics 编写代码。
    - 原因：向量环境能显著提高数据采样效率，但也引入复杂的边界情况（某些子环境在不同时间结束），错误处理会导致无效的存储数据或不正确的 advantage 计算。
    - 实践建议：为每个子环境设置独立 seed，使用 monitor/wrapper 来自动收集 episodic stats，利用同步向量环境（SyncVectorEnv）在 CPU 上更易于调试，必要时用单环境跑通逻辑后再扩展 num_envs。
4. 精确复现论文/参考实现中的“微细节”（Init/eps/clip）
    - 思路：很多强化学习算法的表现受一系列“微小但关键”的实现选择影响，如网络初始化方式（orthogonal 与 gain 的选择）、Adam 的 epsilon、value clipping 是否启用、actor 输出层的初始化尺度、梯度裁剪阈值等。实现时尽可能匹配论文或开源基线（例如 OpenAI baselines、Stable Baselines、cleanrl）的设定，除非有充分理由改动。
    - 原因：这些细节会影响训练稳定性、策略探索性与收敛速度。忽略它们会导致实验结果与论文报导不一致，且难以调试。
    - 实践建议：把这些细节作为默认配置显式写入代码（而不是默默使用框架默认），并把重要细节加入日志与代码注释，便于团队共享与复现。
5. 分层损失设计与可解释化指标（Loss Decomposition & Diagnostics）
    - 思路：将总损失拆分为 policy loss、value loss、entropy bonus，并为每一项单独记录与监测。同时记录辅助诊断指标：approx_kl、clipped_fraction、explained_variance、grad_norm 等。对这些指标的变化要有对应的解释或阈值（例如若 approx_kl 远大于预期则考虑减小 lr 或启用早停）。
    - 原因：当训练发散或策略退化到随机行为时，仅靠 total loss 很难定位问题；细分损失与诊断指标能帮助理解是策略更新过激、value 网络欠拟合还是探索不足。
    - 实践建议：在每次更新时将这些指标写到 TensorBoard/W&B，并在初期训练中关注这些曲线的趋势；把 approximate KL 或 clipped_fraction 作为早停或 lr 调整策略的依据。
6. 保守更新与早停策略（Clipping & Early Stopping）
    - 思路：优先使用剪切（clipped objective）与梯度裁剪来保证更新保守；如有需要再在 epoch 层面上监控 KL 并提前停止（target_kl）。此外使用线性学习率退火以在训练后期减少更新步长。
    - 原因：PPO 的设计目标就是避免策略更新太大导致性能崩溃，具体实现时通过 clip_coef、value_clip、grad_clip 以及 target_kl 可以从多方面控制更新幅度以获得稳定性。
    - 实践建议：把 early stopping 作为可选功能而非默认，先观察 clipped_fraction / approx_kl 的分布再决定是否开启。
7. 自动化追踪与可视化闭环（TB/W&B）
    - 思路：在代码中内建对 TensorBoard/W&B 的支持（开关控制），并在每次实验中保存超参数、代码快照与环境视频。确保线上追踪与本地运行模式共存，便于开发时保持轻量运行，实验验证时开启云端记录。
    - 原因：可视化与自动化记录极大提升调试效率、实验复现性与团队协作能力。视频可以直观发现 agent 行为异常，参数/日志可用于后续对比分析。
    - 实践建议：在提交 PR 或分享结果时附上 W&B 链接，保证他人能复现并查看训练曲线与代码快照。
8. 小结：心智模型的核心是“可配置化 + 分层验证 + 保守更新 + 可解释化指标 + 自动记录”。在实现算法时优先保证正确性与稳定性，再追求性能；在调参时以诊断指标为依据而不是盲目搜索超参数空间。这个心智模型在作者的示例中贯穿始终，从 argparse 到 W&B，从向量环境的封装到 GAE 的细节实现，再到 clipping/entropy/grad_clip 的组合，形成一套可复用的强化学习工程实践指导。

# 总结

本视频以从零实现 PPO（PyTorch）为线索，系统地阐述了 11 个关键实现细节以及若干工程化建议：包括开发环境与实验追踪（argparse、TensorBoard、W&B）、向量环境的正确使用、actor-critic 网络与正交初始化、Adam 的 eps 设置与学习率退火、rollout 存储与 batch/minibatch 策略、GAE 的实现与 returns 计算、PPO 的剪切策略与 value 裁剪、熵正则化、全局梯度裁剪和可选的基于 KL 的早停。作者强调这些细节对训练的稳定性和复现性至关重要，并提供了完整的工程化流程与调试手段（视频观察、loss 分解、诊断指标）。视频链接与源码在描述中给出，可用于将此实现拓展至更多环境和任务。