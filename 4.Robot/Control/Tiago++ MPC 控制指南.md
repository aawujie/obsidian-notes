---
notion-id: 2f278d23-e296-80ec-b47b-c90f490f219f
---
使用模型预测控制（MPC）控制 Tiago++ 差速驱动机器人。

## 🎯 MPC 简介

**MPC（Model Predictive Control）模型预测控制** 是一种先进的控制方法：

1. **预测未来**：使用机器人运动学模型，预测未来 N 步的状态
2. **优化控制**：找到最优的控制序列，使机器人尽可能接近目标
3. **滚动执行**：只执行第一步控制，然后重新规划

### 为什么用 MPC？

✅ **处理约束**：可以限制速度、加速度等

✅ **预测性**：考虑未来轨迹，避免短视决策

✅ **最优性**：通过优化获得最优控制

✅ **通用性**：适用于导航、路径跟踪等多种任务

## 🚀 快速开始

### 基础使用

```python
from src.envs.tiago_env import TiagoEnv
from src.mpc.tiago_mpc import TiagoMPC
import numpy as np

# 创建环境
env = TiagoEnv(render_mode="human", control_mode='velocity')

# 创建 MPC 控制器
mpc = TiagoMPC(
    horizon=20,      # 预测 20 步（1秒）
    dt=0.05,         # 时间步长 50ms
    Q=np.diag([10.0, 10.0, 1.0]),  # 状态权重 [x, y, θ]
    R=np.diag([0.1, 0.1]),         # 控制权重 [v, ω]
)

# 设置目标点
goal = np.array([2.0, 1.5])

# 重置环境
obs, _ = env.reset()

# 控制循环
for _ in range(500):
    # 当前状态 [x, y, θ]
    current_state = obs[[0, 1, 2]]

    # 生成参考轨迹
    reference = mpc.generate_straight_line_reference(current_state, goal)

    # MPC 求解
    control, success = mpc.solve(current_state, reference)

    # 执行控制
    obs, _, _, _, _ = env.step(control)
    env.render()

    # 检查是否到达
    if np.linalg.norm(obs[:2] - goal) < 0.1:
        print("到达目标！")
        break

env.close()

```

## 📦 运行演示

### 方式 1: 交互式脚本

```bash
# 运行所有演示（带可视化）
uv run python test/mpc_test/tiago_mpc_demo.py --demo all --render

# 只运行点到点导航
uv run python test/mpc_test/tiago_mpc_demo.py --demo point --render

# 圆形路径跟踪
uv run python test/mpc_test/tiago_mpc_demo.py --demo circle --render

# 8字形路径
uv run python test/mpc_test/tiago_mpc_demo.py --demo eight --render

# 正方形路径
uv run python test/mpc_test/tiago_mpc_demo.py --demo square --render

```

### 方式 2: 无渲染（更快）

```bash
# 测试性能，不显示窗口
uv run python test/mpc_test/tiago_mpc_demo.py --demo all

```

## 🎮 MPC 参数说明

### TiagoMPC 参数

```python
mpc = TiagoMPC(
    horizon=20,          # 预测时域（步数）
    dt=0.05,             # 时间步长（秒）
    Q=np.diag([...]),    # 状态权重矩阵
    R=np.diag([...]),    # 控制权重矩阵
    v_max=1.0,           # 最大线速度
    omega_max=2.0,       # 最大角速度
)

```

### 权重矩阵调优

### Q: 状态权重 (3×3)

```python
Q = np.diag([q_x, q_y, q_theta])

```

- `**q_x, q_y**`: 位置误差权重
    - 越大 → 更精确跟踪位置
    - 推荐：10-20
- `**q_theta**`: 朝向误差权重
    - 越大 → 更关注朝向对齐
    - 推荐：1-5

**示例配置**：

```python
# 精确定位（导航到点）
Q = np.diag([15.0, 15.0, 2.0])

# 路径跟踪
Q = np.diag([20.0, 20.0, 3.0])

# 宽松控制
Q = np.diag([5.0, 5.0, 0.5])

```

### R: 控制权重 (2×2)

```python
R = np.diag([r_v, r_omega])

```

- `**r_v**`: 线速度惩罚
    - 越大 → 控制越平滑（但可能反应慢）
    - 推荐：0.05-0.2
- `**r_omega**`: 角速度惩罚
    - 越大 → 转向更平滑
    - 推荐：0.05-0.2

**示例配置**：

```python
# 平滑控制
R = np.diag([0.1, 0.1])

# 激进控制（快速响应）
R = np.diag([0.05, 0.05])

# 保守控制（省能量）
R = np.diag([0.5, 0.5])

```

### 时域参数

- `**horizon**`: 预测步数
    - 太小 → 短视，可能陷入局部最优
    - 太大 → 计算慢
    - 推荐：15-25 步
- `**dt**`: 时间步长
    - 与环境的 `frame_skip` 和仿真步长对应
    - Tiago 默认：0.05s (20 Hz)

## 🔧 差速驱动运动学

### 运动学方程

```plain text
ẋ = v * cos(θ)
ẏ = v * sin(θ)
θ̇ = ω

```

**关键约束**：

- ❌ 不能横向移动（非完整约束）
- ✅ 可以原地旋转
- ✅ 可以前进/后退

### 控制输入

```python
control = [v, ω]

```

- `v`: 线速度 (m/s)，沿朝向方向
- `ω`: 角速度 (rad/s)，绕中心旋转

### 状态空间

```python
state = [x, y, θ]

```

- `x, y`: 位置 (m)，世界坐标系
- `θ`: 朝向 (rad)

## 📊 应用场景

### 1. 点到点导航

```python
# 生成参考轨迹
goal = np.array([2.0, 1.5])
reference = mpc.generate_straight_line_reference(current_state, goal)

# 求解并执行
control, success = mpc.solve(current_state, reference)

```

**适用于**：

- 移动到指定位置
- 导航任务
- 目标跟踪

### 2. 路径跟踪

```python
# 生成路径
from src.mpc.tiago_mpc import generate_circle_path
path_x, path_y = generate_circle_path(center=(1, 1), radius=0.8)

# 跟踪路径
reference, next_idx = mpc.generate_path_tracking_reference(
    current_state, path_x, path_y, current_idx
)
control, success = mpc.solve(current_state, reference)

```

**适用于**：

- 巡逻路线
- 预定义路径
- 轨迹跟踪

### 3. 动态避障（待实现）

可以在代价函数中添加障碍物惩罚项。

## 🆚 MPC vs 其他方法

| 方法 | 优点 | 缺点 | 适用场景 |
| --- | --- | --- | --- |
| **MPC** | 最优、处理约束、预测性 | 计算量大 | 导航、路径跟踪 |
| **PID** | 简单、实时 | 无预测、难调参 | 简单跟踪 |
| **纯跟踪** | 快速、几何直观 | 无优化 | 路径跟踪 |
| **强化学习** | 学习最优策略 | 需要大量数据 | 复杂任务 |

## 🎓 技术细节

### 优化问题

MPC 求解以下优化问题：

```plain text
minimize: ∑(state_error^T * Q * state_error + control^T * R * control)

subject to:
    state[k+1] = f(state[k], control[k])  # 运动学约束
    -v_max ≤ v ≤ v_max                    # 速度限制
    -ω_max ≤ ω ≤ ω_max                    # 角速度限制
    state[0] = current_state              # 初始状态

```

### 求解器

使用 **IPOPT**（Interior Point Optimizer）求解非线性规划问题：

- 基于梯度的优化
- 支持约束
- Warm start 加速

### 离散化

使用**欧拉法**离散化连续时间模型：

```plain text
x[k+1] = x[k] + v * cos(θ) * dt
y[k+1] = y[k] + v * sin(θ) * dt
θ[k+1] = θ[k] + ω * dt

```

## 🐛 故障排除

### 问题 1: MPC 求解失败

**现象**：输出 "MPC 求解失败"

**可能原因**：

4. 参考轨迹不可行
5. 权重设置不当
6. 约束冲突

**解决**：

- 增加迭代次数
- 调整权重矩阵
- 检查速度限制是否合理

### 问题 2: 机器人抖动

**原因**：权重 R 太小，控制变化剧烈

**解决**：增加 R 的值，例如 `R = np.diag([0.5, 0.5])`

### 问题 3: 反应太慢

**原因**：

- 预测时域太长
- 权重 R 太大

**解决**：

- 减小 horizon
- 减小 R 的值

### 问题 4: 到不了目标

**原因**：

- Q 太小，不够重视位置误差
- v_max 或 omega_max 太小

**解决**：

- 增加 Q[0], Q[1]
- 增加速度限制

## 📈 性能指标

在 M1 Mac 上的测试结果：

| 任务 | MPC 求解时间 | 总用时 | 精度 |
| --- | --- | --- | --- |
| 点到点导航 (2m) | ~8ms | ~8秒 | ±5cm |
| 圆形路径 (r=0.8m) | ~10ms | ~15秒 | ±8cm |
| 8字形路径 | ~12ms | ~18秒 | ±10cm |
| 正方形路径 (2m) | ~9ms | ~20秒 | ±8cm |

## 🔗 相关资料

- [CasADi 文档](https://web.casadi.org/)
- [IPOPT 求解器](https://coin-or.github.io/Ipopt/)
- [差速驱动运动学](https://en.wikipedia.org/wiki/Differential_wheeled_robot)
- [MPC 理论](https://en.wikipedia.org/wiki/Model_predictive_control)

## 🎯 下一步

### 扩展功能

7. **动态避障**
    - 在代价函数中添加障碍物距离惩罚
    - 实时更新障碍物位置
8. **速度规划**
    - 根据路径曲率调整速度
    - 平滑加减速
9. **鲁棒性**
    - 添加状态估计器
    - 处理模型误差

### 与强化学习结合

MPC 可以作为：

- **策略初始化**：为 RL 提供好的初始策略
- **安全约束**：确保 RL 策略满足约束
- **基准对比**：评估 RL 策略性能

---

**祝使用愉快！** 🚀