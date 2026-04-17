---
share_link: https://share.note.sx/nacd7103#UHVarHGMRaciMV9es3QNDEspuvUtYtPxw0F+aizOlM0
share_updated: 2026-04-15T17:31:18+08:00
---
# 余弦退火 Cosine Annealing

> 一种学习率调度策略，名字来源于物理中的"退火"过程

---

## 名字的由来：物理退火

**物理退火（Annealing）**：
- 金属加热到高温 → 原子自由运动
- 缓慢降温 → 原子逐渐有序排列，达到能量最低的稳定状态
- **关键**：降温速度要慢，才能找到全局最优（而非局部最优）

**类比到优化算法**：
- **学习率高 → 随机探索（高温）**
- **学习率逐渐降低 → 精细调整（低温）**
- 目标：找到损失函数的全局最小值

---

## 数学公式

```
η_t = η_min + (η_max - η_min) × (1 + cos(π × T_cur / T_i)) / 2
```

**参数说明**：
- `η_max`：初始学习率（高温）
- `η_min`：最小学习率（低温）
- `T_cur`：当前 epoch
- `T_i`：一个周期的长度

---

## 学习率变化曲线

```
学习率
  ↑
η_max ┤╭─╮        ╭─╮        ╭─╮
      │ │ ╲      ╱ │ ╲      ╱ │
      │ │  ╲    ╱  │  ╲    ╱  │
      │ │   ╲──╱   │   ╲──╱   │
η_min ┤─╯          ╯          ╯
  └────────────────────────────→ epoch
      0    T_i   2T_i  3T_i
```

---

## 为什么用余弦函数？

| 特性 | 优势 |
|------|------|
| **平滑下降** | 初期缓慢降低，充分探索 |
| **快速收尾** | 后期快速降到最小值，精细收敛 |
| **周期性重启** | 可配合 Warm Restart，跳出局部最优 |

---

## 带热重启的余弦退火（SGDR）

```
学习率
  ↑
  │╭╮    ╭╮        ╭╮
  ││ ╲   │╲        │╲
  ││  ╲  │ ╲       │ ╲
  ││   ╲ │  ╲______│  ╲____
  └────────────────────────→ epoch
    T_0  T_1(=2×T_0)  T_2(=2×T_1)
```

**热重启（Warm Restart）**：
- **每个周期结束后，学习率突然跳回最大值**
- 相当于"重新加热"，**跳出当前局部最优**
- **周期长度逐渐倍增**（T_0, 2T_0, 4T_0...）

---

## PyTorch 实现

### 基本余弦退火

```python
from torch.optim.lr_scheduler import CosineAnnealingLR

scheduler = CosineAnnealingLR(
    optimizer, 
    T_max=100,    # 周期长度
    eta_min=0     # 最小学习率
)
```

### 带热重启

```python
from torch.optim.lr_scheduler import CosineAnnealingWarmRestarts

scheduler = CosineAnnealingWarmRestarts(
    optimizer, 
    T_0=10,       # 第一个周期长度
    T_mult=2,     # 周期倍增因子
    eta_min=1e-6  # 最小学习率
)
```

---

## 总结

| 概念 | 含义 |
|------|------|
| **退火** | 模拟物理降温过程，逐步降低学习率 |
| **余弦** | 用余弦函数控制下降曲线，平滑且可周期性重启 |
| **目的** | 平衡探索与利用，帮助找到更好的全局最优 |

---

## 参考

- 训练大模型（如 Transformer）时常用
- 配合热重启能有效提升收敛质量
- 来源：OpenClaw 会话 2026-04-15
