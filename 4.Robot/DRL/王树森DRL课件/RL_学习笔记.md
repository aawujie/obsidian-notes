# RL学习笔记

## 1. 回报的符号表示

**为什么用 U 表示回报？** U 代表 Utility(效用)，来源于经济学的效用理论。虽然 Sutton & Barto 教材用 G 更常见，但 U 强调了回报作为"效用"的含义，两者数学定义相同：$U_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k}$。

## 2. 观测值 vs 随机变量

**观测值**($s_t, a_t$)是已经发生的确定值，作为已知条件。**随机变量**($S_{t+1}, A_{t+1}, \ldots$)是未来尚未发生的状态和动作，具有不确定性，需要用概率分布描述和求期望。

## 3. 状态价值函数：一个"期望套期望"的理解

### 3.1 核心公式

$$V_\pi(s) = \mathbb{E}_\pi[G_t \mid S_t = s]$$

**人话翻译**：从状态 $s$ 出发，按策略 $\pi$ 行动，**未来能拿到的平均总分**。

### 3.2 为什么是期望？

因为有两种不确定性：
1. **策略的随机性**：在同一个状态，可能选择不同的动作
2. **环境的随机性**：执行同一个动作，可能到达不同的下一状态

所以要对所有可能的"未来路径"求平均，这就是期望！

### 3.3 状态价值 vs 动作价值

$$V_\pi(s_t) = \mathbb{E}_A [Q_\pi(s_t, A)]$$

**通俗理解**：
- $Q_\pi(s_t, a)$：在状态 $s_t$ 选择具体动作 $a$ 的价值
- $V_\pi(s_t)$：把所有可能动作的价值按概率加权平均

**类比**：就像选专业，每个专业有个期望收入（Q值），你的整体期望收入（V值）= 各专业期望收入 × 你选它的概率。

### 3.4 对状态价值再求期望是什么？

$$J(\pi) = \mathbb{E}_{s_0 \sim d_0}[V_\pi(s_0)]$$

这是"**期望的期望**"，用来评估整个策略的性能。

**两层含义**：
1. **第一层期望** $V_\pi(s)$：假设我从状态 $s$ 开始，期望能得到的总回报
2. **第二层期望** $\mathbb{E}_s$：我不知道会从哪个状态开始，对所有可能的起始状态再求平均

**生活例子**：
- 第一层：从北京出发旅行，平均花费 5000 元
- 第一层：从上海出发旅行，平均花费 4000 元  
- 第一层：从深圳出发旅行，平均花费 4500 元
- **第二层**：如果你有 50% 概率在北京，30% 在上海，20% 在深圳，那你的**总体平均花费** = 0.5×5000 + 0.3×4000 + 0.2×4500 = **4600 元**

这个 4600 元就是 $\mathbb{E}_s[V_\pi(s)]$，也就是策略 $\pi$ 的整体性能 $J(\pi)$！

### 3.5 快速记忆

| 符号 | 含义 | 白话 |
|------|------|------|
| $V_\pi(s)$ | 状态价值函数 | 从某个状态出发的平均总回报 |
| $\mathbb{E}_A[Q_\pi(s,A)]$ | 对动作求期望 | 各动作价值的加权平均 |
| $\mathbb{E}_s[V_\pi(s)]$ | 对状态求期望 | 策略的整体表现 |

## 4. 深度强化学习中的动作选择公式

### 4.1 核心公式

$$a_t = \argmax_a Q(s_t, a; \mathbf{w})$$

**人话翻译**：在时刻 $t$，用神经网络算出每个动作的Q值，选Q值最大的那个动作去执行。

### 4.2 公式详解

#### 等号右边：$Q(s_t, a; \mathbf{w})$

| 符号 | 分隔符 | 含义 | 举例 |
|------|--------|------|------|
| $s_t$ | 逗号 , | 当前状态（输入） | 游戏画面、机器人位置 |
| $a$ | 逗号 , | 候选动作（输入） | 上/下/左/右 |
| $\mathbf{w}$ | 分号 ; | 神经网络参数 | CNN的权重和偏置 |

**关键点**：
- $s_t, a$ 是**输入变量**（逗号分隔）
- $\mathbf{w}$ 是**模型参数**（分号分隔，训练时更新）

#### 等号左边：$a_t$

- **时刻 $t$ 实际执行的动作**
- 是 argmax 运算的结果
- 从所有候选动作中选出来的最优动作

### 4.3 执行过程示例

假设玩游戏，当前时刻 $t$：

1. **输入状态** $s_t$（当前画面）到神经网络
2. **遍历所有动作**，计算Q值：
   - $Q(s_t, 上; \mathbf{w}) = 0.3$
   - $Q(s_t, 下; \mathbf{w}) = 0.8$ ← 最大！
   - $Q(s_t, 左; \mathbf{w}) = 0.2$
   - $Q(s_t, 右; \mathbf{w}) = 0.5$
3. **选择最大**：$a_t = 下$（因为 0.8 最大）
4. **执行动作**：智能体执行"下"这个动作

### 4.4 与理论最优的区别

| 公式 | 含义 | 应用场景 |
|------|------|----------|
| $a^* = \argmax_a Q^*(s, a)$ | 理论最优动作 | 理论分析 |
| $a_t = \argmax_a Q(s_t, a; \mathbf{w})$ | 神经网络近似的最优动作 | DQN、DDQN等深度RL算法 |

**区别**：
- $Q^*$ 是真正的最优Q函数（往往无法得到）
- $Q(\cdot; \mathbf{w})$ 是用神经网络学习的近似Q函数

### 4.5 代码理解

```python
def select_action(state, q_network):
    """
    state: 当前状态 s_t
    q_network: 带参数 w 的神经网络
    """
    # 计算所有动作的Q值
    q_values = q_network(state)  # [0.3, 0.8, 0.2, 0.5]
    
    # argmax：选择Q值最大的动作
    action = q_values.argmax()  # 返回索引 1（对应"下"）
    
    return action  # a_t = "下"
```

### 4.6 快速记忆

> **右边的 $a$**：遍历所有候选动作（占位符）  
> **左边的 $a_t$**：最终选定的动作（结果）  
> **$\mathbf{w}$**：神经网络的参数（训练学来的）

这是**DQN算法的核心**：用深度学习近似Q函数 + 贪心选择动作！

## 5. DQN训练：Loss、梯度和梯度下降

### 5.1 三个核心公式

#### 公式1：Loss（损失函数）

$$L = \frac{1}{2}(q - y)^2$$

**含义**：
- **$q$**：神经网络**预测的Q值**（当前预测）
- **$y$**：**目标Q值**（希望预测成的值，通常由Bellman方程计算）
- **$L$**：预测值和目标值之间的**平方误差**

**人话**：我预测错了多少？差得越大，损失越大。

**例子**：
- 神经网络预测：$q = 5$
- 目标值：$y = 8$（根据TD目标计算）
- 损失：$L = \frac{1}{2}(5-8)^2 = 4.5$

#### 公式2：Gradient（梯度）

$$\frac{\partial L}{\partial \mathbf{w}} = \frac{\partial q}{\partial \mathbf{w}} \cdot \frac{\partial L}{\partial q} = (q - y) \cdot \frac{\partial Q(\mathbf{w})}{\partial \mathbf{w}}$$

**含义**：
- 计算**损失函数对网络参数 $\mathbf{w}$ 的梯度**
- 用**链式法则**分解成两部分
- $(q - y)$：预测误差
- $\frac{\partial Q(\mathbf{w})}{\partial \mathbf{w}}$：Q值对参数的敏感度

**人话**：参数往哪个方向调整才能减少误差？

**直观理解**：
- 如果 $q > y$（预测太大）：梯度为正 → 需要减小参数
- 如果 $q < y$（预测太小）：梯度为负 → 需要增大参数

#### 公式3：Gradient Descent（梯度下降）

$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \cdot \frac{\partial L}{\partial \mathbf{w}} \bigg|_{\mathbf{w}=\mathbf{w}_t}$$

**含义**：
- **$\mathbf{w}_t$**：当前的网络参数
- **$\mathbf{w}_{t+1}$**：更新后的网络参数
- **$\alpha$**：学习率（步长，控制每次更新的幅度）
- **减号**：沿着梯度的**反方向**移动（下山）

**人话**：根据梯度，小步小步地调整参数，让预测越来越准。

**例子**：
- 当前参数某个值：$w = 2.0$
- 计算出梯度：$\frac{\partial L}{\partial w} = 0.5$（正数，说明损失在增大）
- 学习率：$\alpha = 0.1$
- 更新：$w_{新} = 2.0 - 0.1 \times 0.5 = 1.95$

### 5.2 训练流程

这三个公式构成了神经网络训练的完整循环：

```
1. 【Loss】计算预测值 q 和目标值 y 的差距
          ↓
2. 【Gradient】计算如何调整参数 w 才能减小差距
          ↓
3. 【Gradient Descent】实际更新参数 w
          ↓
重复以上步骤，直到 q ≈ y（预测越来越准）
```

### 5.3 在DQN中的具体应用

在DQN训练一个transition $(s_t, a_t, r_t, s_{t+1})$ 时：

1. **预测值** $q$：
   $$q = Q(s_t, a_t; \mathbf{w})$$
   当前网络对该状态-动作对的预测

2. **目标值** $y$：
   $$y = r_t + \gamma \max_{a'} Q(s_{t+1}, a'; \mathbf{w}^-)$$
   TD目标（Temporal Difference Target）

3. **计算损失**：
   $$L = \frac{1}{2}(q - y)^2$$

4. **反向传播计算梯度**：
   $$\frac{\partial L}{\partial \mathbf{w}}$$

5. **更新参数**：
   $$\mathbf{w} \leftarrow \mathbf{w} - \alpha \cdot \frac{\partial L}{\partial \mathbf{w}}$$

### 5.4 代码实现示例

```python
# 1. 前向传播：计算预测Q值
q_pred = q_network(state, action)  # 预测值 q

# 2. 计算TD目标
with torch.no_grad():
    next_q_values = target_network(next_state)
    y_target = reward + gamma * next_q_values.max()  # 目标值 y

# 3. 计算Loss
loss = 0.5 * (q_pred - y_target) ** 2  # 或使用 MSELoss

# 4. 反向传播计算梯度
loss.backward()  # 自动计算 ∂L/∂w

# 5. 梯度下降更新参数
optimizer.step()  # w_new = w_old - α * ∂L/∂w
```

### 5.5 生活类比

想象你在练习投篮：

1. **Loss**：你投偏了多少？（实际落点 vs 篮筐位置）
2. **Gradient**：你应该往哪个方向调整力度和角度？调多少？
3. **Gradient Descent**：根据偏差，一点点调整你的投篮动作

重复这个过程，你的投篮会越来越准！DQN训练也是同样的道理。

### 5.6 关键点总结

| 概念 | 作用 | 白话 |
|------|------|------|
| Loss | 衡量预测误差 | 我错了多少？ |
| Gradient | 指出优化方向 | 往哪儿改？ |
| Gradient Descent | 执行参数更新 | 开始改！ |

**核心思想**：通过不断地"预测 → 计算误差 → 调整参数"这个循环，让Q网络的预测越来越接近真实的Q值！

### 5.7 梯度 vs 梯度下降：关键区别

#### 两者对比

| 维度 | 梯度 | 梯度下降 |
|------|------|----------|
| **性质** | 计算/分析 | 执行/行动 |
| **公式** | $\frac{\partial L}{\partial \mathbf{w}}$ | $\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \cdot \frac{\partial L}{\partial \mathbf{w}}$ |
| **输出** | 方向向量（导数） | 新的参数值 |
| **作用** | "上坡在哪？" | "往下坡走！" |
| **代码** | `loss.backward()` | `optimizer.step()` |

#### 形象类比

想象你在雾中的山上，想下山：

1. **梯度**：你用手摸地面，感受哪边是上坡
   - 输出：一个指向上坡的箭头
   
2. **梯度下降**：你根据上坡方向，往**反方向**迈一小步
   - 输出：你的新位置

#### 为什么要分开？

- **梯度**是数学上的分析工具，只管"计算方向"
- **梯度下降**是优化算法，要决定：
  - 往哪走？（梯度的反方向，因为有负号）
  - 走多远？（学习率 $\alpha$）
  - 什么时候走？（每次迭代）

#### 关键记忆 🎯

> **梯度** = 罗盘（指方向）  
> **梯度下降** = 迈步（走路）

你需要先有罗盘知道方向，再迈步往那个方向走！

## 6. 策略梯度中的随机采样与无偏估计

### 6.1 核心问题

**问题**：为什么从策略中随机采样动作 $a \sim \pi(\cdot|s_t; \boldsymbol{\theta}_t)$，就能保证梯度估计 $\mathbf{g}(a, \boldsymbol{\theta})$ 是无偏的？

### 6.2 什么是无偏估计？

**定义**：估计量的期望值等于真实值

$$\mathbb{E}[\text{估计量}] = \text{真实值}$$

**例子**：
- 真实平均身高：170cm
- 如果抽样方法的期望身高 = 170cm → 无偏 ✅
- 如果抽样方法的期望身高 = 175cm → 有偏 ❌

### 6.3 策略梯度的真实值

在策略梯度方法中，**真实的策略梯度**是：

$$\nabla_{\boldsymbol{\theta}} J(\boldsymbol{\theta}) = \mathbb{E}_{a \sim \pi(\cdot|s_t;\boldsymbol{\theta}_t)} [\mathbf{g}(a, \boldsymbol{\theta}_t)]$$

**含义**：对所有可能的动作 $a$，按照策略 $\pi$ 的概率分布，计算梯度 $\mathbf{g}(a, \boldsymbol{\theta})$ 的期望。

**展开形式**：

$$\nabla_{\boldsymbol{\theta}} J(\boldsymbol{\theta}) = \sum_a \pi(a|s;\boldsymbol{\theta}) \cdot \mathbf{g}(a, \boldsymbol{\theta})$$

### 6.4 随机采样的估计

实际中，我们不可能遍历所有动作计算期望（动作空间可能很大或连续），所以：

1. **从策略中随机采样**：$a \sim \pi(\cdot | s_t; \boldsymbol{\theta}_t)$
2. **用这个样本计算梯度**：$\mathbf{g}(a, \boldsymbol{\theta}_t)$

### 6.5 为什么是无偏的？

**关键原因**：我们从什么分布采样，就用什么分布计算期望！

$$\mathbb{E}_{a \sim \pi} [\mathbf{g}(a, \boldsymbol{\theta})] = \sum_a \pi(a|s;\boldsymbol{\theta}) \cdot \mathbf{g}(a, \boldsymbol{\theta}) = \nabla_{\boldsymbol{\theta}} J(\boldsymbol{\theta})$$

**验证无偏性**：
- 采样分布 = $\pi(\cdot|s;\boldsymbol{\theta})$ ✅
- 期望分布 = $\pi(\cdot|s;\boldsymbol{\theta})$ ✅
- 两者**完全一致**！

所以单个样本 $\mathbf{g}(a, \boldsymbol{\theta})$ 虽然有噪声（方差大），但它的**期望**正好等于真实梯度 → **无偏** ✅

### 6.6 反例：什么情况下会有偏？

#### 反例1：贪心选择（总是选最大概率动作）

如果我们用：
$$a = \argmax_{a'} \pi(a'|s;\boldsymbol{\theta})$$

- 只看到了"最优动作"的梯度
- 忽略了其他动作的梯度贡献
- 采样分布 ≠ 期望分布 → **有偏** ❌

#### 反例2：从均匀分布采样

如果我们从均匀分布采样：
$$a \sim \text{Uniform}(\mathcal{A})$$

但计算的期望是：
$$\mathbb{E}_{a \sim \pi} [\mathbf{g}(a, \boldsymbol{\theta})]$$

- 采样分布（均匀分布）≠ 期望分布（策略分布）
- → **有偏** ❌

### 6.7 直观类比

**估计中国人的平均身高**：

| 方法 | 采样方式 | 结果 |
|------|----------|------|
| ✅ 无偏 | 按人口比例随机抽样 | 期望 = 真实平均身高 |
| ❌ 有偏 | 只在篮球队里抽样 | 期望 > 真实平均身高（高个子被过度采样） |
| ❌ 有偏 | 只抽最高的人 | 期望 >> 真实平均身高 |

**在策略梯度中**：

| 方法 | 采样方式 | 结果 |
|------|----------|------|
| ✅ 无偏 | $a \sim \pi(a\|s)$ | 梯度期望 = 真实梯度 |
| ❌ 有偏 | $a = \argmax \pi(a\|s)$ | 梯度期望 ≠ 真实梯度 |
| ❌ 有偏 | $a \sim \text{Uniform}$ | 梯度期望 ≠ 真实梯度 |

### 6.8 无偏 vs 低方差

**重要区分**：

| 特性 | 无偏估计 | 低方差估计 |
|------|----------|------------|
| 含义 | 期望等于真实值 | 估计值集中、波动小 |
| 随机采样 | ✅ 无偏 | ❌ 方差大（单次采样噪声大） |
| 多次采样平均 | ✅ 无偏 | ✅ 方差降低 |

**结论**：
- 随机采样虽然**无偏**，但**方差大**（单次估计不准）
- 通过多次采样或使用baseline可以**降低方差**
- 无偏性保证了"长期来看是对的"

### 6.9 数学证明（简化版）

设真实梯度为：
$$g_{\text{true}} = \sum_a \pi(a|s) \cdot \mathbf{g}(a, \boldsymbol{\theta})$$

用随机采样估计：
$$\mathbb{E}_{a \sim \pi}[\mathbf{g}(a, \boldsymbol{\theta})] = \sum_a \pi(a|s) \cdot \mathbf{g}(a, \boldsymbol{\theta}) = g_{\text{true}}$$

因为根据期望的定义：
$$\mathbb{E}_{X \sim p}[f(X)] = \sum_x p(x) f(x)$$

当 $X = a$，$p = \pi$，$f = \mathbf{g}$ 时，正好得到真实梯度！

### 6.10 关键记忆 🎯

> **从谁采样，就能无偏估计谁的期望！**

- 采样分布 = 期望分布 → **无偏** ✅
- 采样分布 ≠ 期望分布 → **有偏** ❌

**策略梯度的无偏性**：
- 从策略 $\pi$ 采样动作 $a$
- 估计对策略 $\pi$ 的期望
- 采样和期望一致 → 无偏！

虽然单次采样有噪声（**方差大**），但多次采样的平均值会收敛到真实梯度（**期望正确**）！

## 7. Actor-Critic算法详解

### 7.1 算法概览

**Actor-Critic**是经典的强化学习算法，包含两个核心组件：

- **Actor（演员/策略网络）**：参数 $\boldsymbol{\theta}$，负责选择动作
- **Critic（评委/价值网络）**：参数 $\mathbf{w}$，负责评估动作价值

### 7.2 核心概念：价值网络与价值函数的关系

#### 三个概念

1. **动作价值函数 $Q(s,a)$（理论）**
   $$Q^\pi(s,a) = \mathbb{E}_\pi[G_t \mid S_t=s, A_t=a]$$
   在状态 $s$ 下执行动作 $a$，然后按策略 $\pi$ 行动的期望回报

2. **状态价值函数 $V(s)$（理论）**
   $$V^\pi(s) = \mathbb{E}_\pi[G_t \mid S_t=s] = \mathbb{E}_{a \sim \pi}[Q^\pi(s,a)]$$
   在状态 $s$ 下按策略 $\pi$ 行动的期望回报

3. **价值网络 $q(s,a;\mathbf{w})$（实际）**
   $$q(s,a;\mathbf{w}) \approx Q^\pi(s,a)$$
   用神经网络（参数 $\mathbf{w}$）近似真实的动作价值函数

#### 核心关系

$$V^\pi(s) = \sum_a \pi(a|s) \cdot Q^\pi(s,a) \quad \text{或} \quad V(s) = \mathbb{E}_{a \sim \pi}[Q(s,a)]$$

**含义**：
- **$Q(s,a)$**：选择**具体动作** $a$ 的价值
- **$V(s)$**：对所有动作按策略概率**加权平均**
- **$q(s,a;\mathbf{w})$**：神经网络**近似** $Q(s,a)$

**快速记忆**：价值网络 $q$ 近似动作价值 $Q$，状态价值 $V$ 是动作价值 $Q$ 的期望。

### 7.3 完整算法流程

#### 步骤1-3：环境交互与采样

1. **观察状态并采样动作**
   $$a_t \sim \pi(\cdot | s_t; \boldsymbol{\theta}_t)$$
   从Actor采样实际要执行的动作

2. **执行动作，获得反馈**
   $$\text{Perform } a_t \rightarrow (s_{t+1}, r_t)$$
   获得新状态和奖励

3. **采样下一个动作（不执行！）**
   $$\tilde{a}_{t+1} \sim \pi(\cdot | s_{t+1}; \boldsymbol{\theta}_t)$$
   用于估计下一状态的价值，**只采样不执行**

#### 步骤4-7：更新Critic（价值网络）

4. **评估Q值**
   $$q_t = q(s_t, a_t; \mathbf{w}_t), \quad q_{t+1} = q(s_{t+1}, \tilde{a}_{t+1}; \mathbf{w}_t)$$
   预测当前和下一个状态-动作对的Q值

5. **计算TD误差**
   $$\delta_t = q_t - (r_t + \gamma \cdot q_{t+1})$$
   TD error = 预测值 - TD目标

6. **计算Critic梯度**
   $$\mathbf{d}_{\mathbf{w}, t} = \frac{\partial q(s_t, a_t; \mathbf{w})}{\partial \mathbf{w}} \bigg|_{\mathbf{w}=\mathbf{w}_t}$$

7. **更新Critic（梯度下降）**
   $$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \cdot \delta_t \cdot \mathbf{d}_{\mathbf{w}, t}$$

#### 步骤8-9：更新Actor（策略网络）

8. **计算策略梯度**
   $$\mathbf{d}_{\boldsymbol{\theta}, t} = \frac{\partial \log \pi(a_t | s_t; \boldsymbol{\theta})}{\partial \boldsymbol{\theta}} \bigg|_{\boldsymbol{\theta}=\boldsymbol{\theta}_t}$$

9. **更新Actor（梯度上升）**
   $$\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t + \beta \cdot q_t \cdot \mathbf{d}_{\boldsymbol{\theta}, t}$$

### 7.4 训练目标

#### Actor的目标：最大化状态价值

**目标函数**：
$$V(s; \boldsymbol{\theta}, \mathbf{w}) = \sum_a \pi(a|s; \boldsymbol{\theta}) \cdot q(s, a; \mathbf{w})$$

**策略梯度**：
$$\frac{\partial V(s; \boldsymbol{\theta})}{\partial \boldsymbol{\theta}} = \mathbb{E}_A \left[ \frac{\partial \log \pi(A|s; \boldsymbol{\theta})}{\partial \boldsymbol{\theta}} \cdot q(s, A; \mathbf{w}) \right]$$

**更新方式**：梯度**上升**（增加好动作的概率）

#### Critic的目标：最小化TD误差

**损失函数**：
$$L = \frac{1}{2}(q_t - y_t)^2$$

其中TD目标：
$$y_t = r_t + \gamma \cdot q(s_{t+1}, \tilde{a}_{t+1}; \mathbf{w})$$

**梯度**：
$$\frac{\partial L}{\partial \mathbf{w}} = (q_t - y_t) \cdot \frac{\partial q(s_t, a_t; \mathbf{w})}{\partial \mathbf{w}}$$

**更新方式**：梯度**下降**（减少预测误差）

#### 梯度上升 vs 梯度下降：何时用哪个？

**核心原则**：
- **梯度下降（-）**：最小化损失/误差 → Critic用
- **梯度上升（+）**：最大化目标/回报 → Actor用

**直观理解**：

| 方法 | 符号 | 目标 | 类比 | 应用 |
|------|------|------|------|------|
| **梯度下降** | - | 找最低点 | 下山 | Critic（最小化TD误差） |
| **梯度上升** | + | 找最高点 | 爬山 | Actor（最大化回报） |

**梯度**总是指向函数值**增大**的方向：
- 想变小（最小化）→ 往梯度**反方向**走 → 用**减号**
- 想变大（最大化）→ 往梯度**方向**走 → 用**加号**

**在Actor-Critic中**：
- **Critic下降**：$\mathbf{w} \leftarrow \mathbf{w} - \alpha \cdot \nabla L$ （预测要准，误差要小）
- **Actor上升**：$\boldsymbol{\theta} \leftarrow \boldsymbol{\theta} + \beta \cdot \nabla J$ （策略要优，回报要大）

### 7.5 Actor-Critic的分工与协作

#### 两者的角色

| 组件 | 作用 | 输入 | 输出 | 类比 |
|------|------|------|------|------|
| **Actor** $\pi(\cdot\|s; \boldsymbol{\theta})$ | 做决策（选动作） | 状态 $s$ | 动作 $a$ | 演员表演 |
| **Critic** $q(s,a; \mathbf{w})$ | 评价决策（打分） | 状态-动作 $(s,a)$ | Q值 | 评委打分 |

#### 协同工作流程

```
1. Actor选择动作 a_t
         ↓
2. 与环境交互，获得 (s_{t+1}, r_t)
         ↓
3. Critic评估：q_t = q(s_t, a_t)  → "这个动作值多少分"
         ↓
4. Critic学习：通过TD learning改进评分准确性
         ↓
5. Actor改进：
   - 如果 q_t > 0（好动作）→ 增加 π(a_t|s_t) 的概率
   - 如果 q_t < 0（坏动作）→ 减少 π(a_t|s_t) 的概率
```

### 7.6 关键特点

#### 1. On-policy算法

- 用当前策略 $\pi$ 采样动作
- 评估和改进的是**同一个策略**
- 采样 $\tilde{a}_{t+1} \sim \pi$ 保证无偏估计

#### 2. Bootstrap（自举）

- 用Critic的估计 $q_{t+1}$ 来更新 $q_t$
- 不需要等到episode结束
- 可以在线学习

#### 3. 两个学习率

- **$\alpha$**：Critic的学习率（价值网络更新步长）
- **$\beta$**：Actor的学习率（策略网络更新步长）
- 通常 $\alpha > \beta$（Critic学得快一些）

#### 4. Q值作为权重

步骤9中，$q_t$ 作为权重指导策略更新：
- $q_t$ 大（好动作）→ 大幅增加概率
- $q_t$ 小（坏动作）→ 小幅或减少概率

**$q_t$ 的详细含义**：

$$q_t = q(s_t, a_t; \mathbf{w}_t)$$

这是Critic对动作 $a_t$ 的**打分/评估**，在Actor更新公式中充当**权重**：

$$\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t + \beta \cdot \underbrace{q_t}_{\text{权重}} \cdot \underbrace{\mathbf{d}_{\boldsymbol{\theta}, t}}_{\text{方向}}$$

| $q_t$ 的值 | 含义 | Actor的反应 |
|-----------|------|-------------|
| $q_t > 0$ 且很大 | 很好的动作 | **大幅增加** $\pi(a_t\|s_t)$ |
| $q_t > 0$ 且较小 | 还行的动作 | **小幅增加** $\pi(a_t\|s_t)$ |
| $q_t \approx 0$ | 一般般的动作 | 几乎不改变 |
| $q_t < 0$ | 不好的动作 | **减少** $\pi(a_t\|s_t)$ |

**一句话总结**：$q_t$ = Critic的评分，决定"往这个方向走多远"——好动作多走，坏动作反着走。

### 7.7 为什么采样 $\tilde{a}_{t+1}$ 但不执行？

#### 目的：估计期望价值

我们需要估计：
$$V(s_{t+1}) = \mathbb{E}_{a \sim \pi(\cdot|s_{t+1})}[q(s_{t+1}, a)]$$

**方法**：
- 从策略 $\pi$ 采样 $\tilde{a}_{t+1}$
- 用 $q(s_{t+1}, \tilde{a}_{t+1})$ 近似期望
- 根据第6章结论：这是**无偏估计**！

#### 为什么不执行？

| 时刻 | 动作 | 是否执行 | 用途 |
|------|------|----------|------|
| $t$ | $a_t$ | ✅ 执行 | 环境交互，获取经验 |
| $t+1$ | $\tilde{a}_{t+1}$ | ❌ 不执行 | 估计 $V(s_{t+1})$，算完丢弃 |
| $t+1$ | $a_{t+1}$（重新采样） | ✅ 执行 | 下一时刻的真实动作 |

**原因**：
- $\tilde{a}_{t+1}$ 只是计算TD目标的工具
- 下一时刻会用更新后的策略 $\pi(\cdot; \boldsymbol{\theta}_{t+1})$ 重新采样

### 7.8 优缺点分析

#### ✅ 优点

1. **样本效率高（Sample Efficient）**：每步都可以学习，不需要完整episode
   - **含义**：用更少的样本（数据）达到相同的学习效果
   - **优势**：减少与环境交互的次数，训练更快、更实用

   **算法对比**：

   | 算法类型 | 样本效率 | 说明 |
   |----------|----------|------|
   | **REINFORCE** | ❌ 低 | 需要完整 episode 才能更新一次 |
   | **Actor-Critic** | ✅ 高 | 每步都可以学习，不需要等 episode 结束 |
   | **TRPO** | ✅ 更高 | 通过信任域约束，更稳定地利用样本 |

   **具体例子**：

   **低样本效率（REINFORCE）**：
   ```
   玩完一局游戏（100步）→ 才能更新一次策略
   需要玩 1000 局 → 才能更新 1000 次
   
   ```

   **高样本效率（Actor-Critic）**：
   ```
   每走一步 → 就能更新一次策略
   走 100 步 → 就能更新 100 次
   ```

   低效率：必须开完一整圈才能总结一次经验；高效率：每开一段路就能总结并改进
2. **低方差**：用Critic估计代替MC return，方差更小
3. **在线学习**：适用于连续任务
4. **可扩展性强**：A3C、PPO、SAC等都基于此架构

#### ❌ 缺点

1. **有偏估计**：Critic估计不准时会传递误差（bootstrap代价）
2. **难调参**：需要平衡两个学习率
3. **可能不稳定**：策略和价值相互影响，容易振荡
4. **收敛性**：理论保证较弱

### 7.9 与其他算法的对比

| 算法 | Actor | Critic | Policy | 特点 |
|------|-------|--------|--------|------|
| **REINFORCE** | ✅ | ❌ | On-policy | 高方差，无偏 |
| **Q-learning** | ❌ | ✅ | Off-policy | 只学Q值，贪心选动作 |
| **SARSA** | ❌ | ✅ | On-policy | TD学习Q值 |
| **Actor-Critic** | ✅ | ✅ | On-policy | 低方差，有偏但高效 |

### 7.10 关键记忆 🎯

> **Critic**：评价动作 → "这个动作值 $q_t$ 分"  
> **Actor**：根据评价改进 → "值高就多做，值低就少做"

**核心思想**：
- Critic教Actor什么是好动作
- Actor根据Critic的反馈改进策略
- 两者协同进化，共同提升

**一句话总结**：Actor-Critic = 策略梯度（Actor）+ 价值估计（Critic）的完美结合！

## 8. TRPO 中的邻域和范数符号说明

本文档基于 `5_TRPO.pdf` 提取的文本内容，总结 TRPO 算法中使用的邻域和范数的数学符号表示。

### 8.1 邻域的数学符号

#### 基本表示

在 TRPO 中，邻域（neighborhood）用符号 $\mathcal{N}$ 表示：

- **$\mathcal{N}(\theta_{k-1})$**：以 $\theta_{k-1}$ 为中心的邻域

#### 邻域的定义

根据 PDF 第 8 页的内容，邻域的定义为：

$$\mathcal{N}(\theta_{k-1}) = \{ \theta \mid \|\theta - \theta_{k-1}\| \leq \Delta \}$$

**符号说明**：
- **$\mathcal{N}$**：花体字母 N，表示邻域（neighborhood）
- **$\theta_{k-1}$**：当前迭代的参数
- **$\theta$**：邻域内的参数
- **$\|\cdot\|$**：范数符号
- **$\Delta$**：邻域的半径（delta，希腊字母）

#### 信任域（Trust Region）

当邻域内的近似函数 $L(\theta|\theta_{k-1})$ 能够很好地近似目标函数 $J(\theta)$ 时，这个邻域被称为**信任域**（trust region）。

#### 函数符号说明

| 符号 | 英文全称 | 中文名称 | 含义 |
|------|----------|----------|------|
| **$J(\theta)$** | Objective Function | 目标函数 | 策略参数 $\theta$ 下的期望回报 |
| **$L(\theta\|\theta_{k-1})$** | Surrogate Objective Function | 代理目标函数 | 在 $\theta_{k-1}$ 附近对 $J(\theta)$ 的近似函数 |
| **$\tilde{L}$** | L tilde | L 波浪号 | 代理目标函数的另一种表示，$\tilde{L}$ 读作 "L tilde" 或 "L 波浪号" |

### 8.2 范数的表示符号

#### 基本范数符号

在 TRPO 中，范数使用双竖线表示：

- **$\|\theta - \theta_{k-1}\|$**：参数差的范数
- **$\|\theta - \theta_{k-1}\| \leq \Delta$**：范数约束

#### TRPO 中的两种约束方式

根据 PDF 第 45-46 页，TRPO 提供了两种定义信任域的方式：

**Option 1: 参数范数约束**

$$\|\theta - \theta_{k-1}\| < \Delta$$

**Option 2: KL 散度约束**

$$\frac{1}{n} \sum_{i=1}^{n} \text{KL}(\pi(\cdot|s_i; \theta_{k-1}) \| \pi(\cdot|s_i; \theta)) < \Delta$$

其中：
- **KL**：KL 散度（Kullback-Leibler divergence），衡量两个概率分布的差异
- **$\pi(\cdot|s_i; \theta)$**：策略函数
- **$\|$**：KL 散度中使用单竖线分隔两个分布（注意：在 LaTeX 中 KL 散度用单竖线）

#### KL 散度说明

**定义**：
- **离散分布**：$\text{KL}(P \| Q) = \sum_x P(x) \log \frac{P(x)}{Q(x)}$
- **连续分布**：$\text{KL}(P \| Q) = \int p(x) \log \frac{p(x)}{q(x)} dx$

**性质**：
- 非对称：$\text{KL}(P \| Q) \neq \text{KL}(Q \| P)$
- 非负：$\text{KL}(P \| Q) \geq 0$，当且仅当 $P = Q$ 时为 0
- 不是距离度量（不满足三角不等式）

**在 TRPO 中的作用**：限制新旧策略之间的差异，保证策略更新的稳定性。

#### 范数类型

虽然 PDF 中没有明确说明范数的类型，但在实际应用中：
- 通常使用 **L2 范数**（欧几里得范数）：$\|x\|_2$
- 有时也使用 **L∞ 范数**（最大范数）：$\|x\|_\infty$

### 8.3 完整算法中的符号使用

#### 信任域算法步骤

根据 PDF 第 33 页，TRPO 的完整步骤：

1. **近似**：给定 $\theta_{k-1}$，构造 $L(\theta|\theta_{k-1})$，在邻域 $\mathcal{N}(\theta_{k-1})$ 内近似 $J(\theta)$

2. **最大化**：在信任域 $\mathcal{N}(\theta_{k-1})$ 内找到 $\theta_{\text{new}}$：

   $$\theta_{\text{new}} \leftarrow \argmax_{\theta \in \mathcal{N}(\theta_{k-1})} L(\theta|\theta_{k-1})$$

#### 为什么是最大化而不是最小化？

**核心原因**：$J(\theta)$ 和 $L(\theta|\theta_{k-1})$ 表示**期望回报**，回报越大越好。

| 类型 | 目标 | 优化方向 | 例子 |
|------|------|----------|------|
| **目标函数** | 越大越好 | **最大化** | $J(\theta)$ = 期望回报 |
| **损失函数** | 越小越好 | **最小化** | $L = \frac{1}{2}(q-y)^2$ = 预测误差 |

- $J(\theta)$ 表示策略的期望回报，我们希望回报**越大越好**，所以需要**最大化**
- $L(\theta|\theta_{k-1})$ 是 $J(\theta)$ 的近似，所以也要**最大化**
- 如果是损失函数（误差），才需要**最小化**

**类比**：
- **最大化回报** = 找最高点（爬山）→ TRPO 的目标
- **最小化损失** = 找最低点（下山）→ Critic 的目标

#### 最大化的目的

1. **间接优化真实目标函数**：
   - 直接优化 $J(\theta)$ 很困难（需要完整轨迹、计算量大）
   - 在信任域内，$L(\theta|\theta_{k-1})$ 能很好地近似 $J(\theta)$
   - 最大化 $L(\theta|\theta_{k-1})$ 可以间接改进 $J(\theta)$

2. **找到更好的策略参数**：
   - 在信任域内找到使代理函数最大的 $\theta_{\text{new}}$
   - 期望 $J(\theta_{\text{new}}) > J(\theta_{k-1})$，即策略性能提升

3. **保证策略改进的稳定性**：
   - 约束在信任域内：$\|\theta - \theta_{k-1}\| \leq \Delta$
   - 避免参数更新过大导致策略崩溃
   - 确保每次更新都是"小幅改进"，而非"大幅跳跃"

**优化流程**：
```
真实目标：max J(θ)  ← 太难直接优化
         ↓
近似替代：max L(θ|θ_{k-1})  ← 在信任域内近似
         ↓
约束保证：θ ∈ 𝒩(θ_{k-1})  ← 保证近似有效
         ↓
结果：J(θ_new) ≈ L(θ_new|θ_{k-1}) > J(θ_{k-1})
```

#### 约束条件

在最大化步骤中，约束条件可以写成：

$$\text{s.t. } \theta \in \mathcal{N}(\theta_{k-1})$$

或者等价地：

$$\text{s.t. } \|\theta - \theta_{k-1}\| \leq \Delta$$

**符号说明**：
- **s.t.**：Subject To（约束条件 / 使得）

### 8.4 符号总结表

| 符号 | 含义 | 示例 |
|------|------|------|
| **$\mathcal{N}(\theta)$** | 以 $\theta$ 为中心的邻域 | $\mathcal{N}(\theta_{k-1})$ |
| **$\|\cdot\|$** | 范数 | $\|\theta - \theta_{k-1}\|$ |
| **$\Delta$** | 邻域半径（delta） | $\Delta = 0.01$ |
| **$\theta$** | 策略参数向量 | $\theta \in \mathbb{R}^d$ |
| **$\text{KL}(\cdot\|\cdot)$** | KL 散度 | $\text{KL}(\pi_{\text{old}} \| \pi_{\text{new}})$ |

### 8.5 注意事项

1. **范数符号**：使用双竖线 `$\|\cdot\|$` 表示范数，不是单竖线 `$|$`
2. **邻域符号**：使用花体字母 $\mathcal{N}$（`\mathcal{N}`），不是普通 N
3. **KL 散度**：在 LaTeX 中使用单竖线 `$\|$` 分隔两个分布，这是 KL 散度的标准表示
4. **约束方向**：通常使用 $\leq$ 或 $<$，取决于具体实现

### 8.6 关键记忆 🎯

> **邻域** = 以当前参数为中心的一个"安全区域"  
> **范数** = 衡量参数变化大小的"尺子"  
> **信任域** = 在这个区域内，近似函数是可信的

**TRPO 的核心思想**：
- 在信任域内最大化近似函数
- 避免参数更新过大导致策略崩溃
- 通过约束保证策略改进的稳定性

---
*创建日期: 2025-12-12*

