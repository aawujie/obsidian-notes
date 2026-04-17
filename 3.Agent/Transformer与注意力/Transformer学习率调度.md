# Transformer 学习率调度 —— Warmup + Decay

> Transformer 原论文使用的学习率调度策略
> 整理日期：2026-03-28

---

## 一句话解释

**Warmup**（预热）：训练初期小学习率慢慢升温，防止梯度爆炸  
**Decay**（衰减）：后期按 $1/\sqrt{\text{step}}$ 逐渐降低，精细收敛

---

## 公式

$$\text{lr} = d_{\text{model}}^{-0.5} \cdot \min\left(\text{step}^{-0.5}, \text{step} \cdot \text{warmup\_steps}^{-1.5}\right)$$

---

## 分阶段解析

| 阶段 | 条件 | 公式 | 曲线 | 目的 |
|------|------|------|------|------|
| **Warmup** | step < warmup_steps | $\text{step} \cdot \text{warmup}^{-1.5}$ | ↗ 线性上升 | 初期梯度不稳定，小步慢走 |
| **Decay** | step ≥ warmup_steps | $\text{step}^{-0.5}$ | ↘ 平滑下降 | 后期精细调整，收敛最优 |

---

## 直观图示

```
学习率
  ↑
  │      ╭─╮
  │     ╱   ╲
  │    ╱     ╲
  │   ╱       ╲____
  │  ╱              ＼
  │ ╱                ＼
  └────────────────→ step
    ↑
   Warmup结束 (比如 4000 步)
```

---

## 代码实现

```python
class TransformerLRScheduler:
    def __init__(self, optimizer, d_model, warmup_steps=4000):
        self.optimizer = optimizer
        self.d_model = d_model
        self.warmup_steps = warmup_steps
        self.step_num = 0

    def step(self):
        self.step_num += 1
        lr = self._get_lr()
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = lr
        return lr

    def _get_lr(self):
        step = self.step_num
        d = self.d_model
        # 取 min 实现分段：小值是 Warmup，大值是 Decay
        lr = (d ** -0.5) * min(
            step ** -0.5,                    # Decay: 1/sqrt(step)
            step * (self.warmup_steps ** -1.5)  # Warmup: 线性上升
        )
        return lr
```

**关键点：** 用 `min()` 自动选择两个阶段中较小的学习率，实现平滑过渡。

---

## 超参数选择

| 参数 | 原论文 | 说明 |
|------|--------|------|
| d_model | 512 | 模型维度，影响初始学习率大小 |
| warmup_steps | 4000 | 预热步数，通常占总步数的 5-10% |

**学习率曲线数据（d_model=512, warmup=4000）：**

| Step | 阶段 | 学习率 |
|------|------|--------|
| 1 | Warmup | 1.25e-7 |
| 1000 | Warmup | 1.25e-4 |
| 4000 | 转折点 | 5.0e-4 |
| 8000 | Decay | 3.5e-4 |
| 40000 | Decay | 1.6e-4 |

---

## 为什么要这样设计？

### Warmup 的必要性

**问题：** Transformer 训练初期梯度不稳定

```
Step 1: 梯度很大 → 参数更新很大 → 模型崩溃
Step 2: 梯度爆炸 → NaN
```

**解决：** 小学习率起步，慢慢升温

```
Step 1: lr=1e-7 → 小更新 → 稳定
Step 1000: lr=1e-4 → 中等更新 → 学习
Step 4000: lr=5e-4 → 正常更新 → 收敛
```

### Decay 的必要性

**问题：** 固定学习率后期震荡，无法精细收敛

**解决：** 逐渐降低学习率，让步长越来越小

```
初期：大步走，快速接近最优区域
后期：小步走，精细调整找到最优解
```

---

## 对比其他调度方式

| 方式 | 公式 | 特点 | 适用场景 |
|------|------|------|---------|
| **Transformer** | $1/\sqrt{\text{step}}$ | 平滑衰减，无需调参 | 大模型、长训练 |
| Step Decay | 每 N 步 ×0.1 | 阶梯式，需要调 N | CV 传统方法 |
| Cosine Annealing | 余弦曲线 | 周期性，有重启 | 小数据集、微调 |
| Exponential | $e^{-\text{step}}$ | 衰减太快 | 不推荐 |
| Constant | 固定 | 最简单 | Baseline |

---

## 可视化代码

```python
import matplotlib.pyplot as plt
import numpy as np

def transformer_lr(step, d_model=512, warmup=4000):
    return (d_model ** -0.5) * min(step ** -0.5, step * (warmup ** -1.5))

steps = np.arange(1, 50000)
lrs = [transformer_lr(s) for s in steps]

plt.figure(figsize=(10, 4))
plt.plot(steps, lrs)
plt.axvline(x=4000, color='r', linestyle='--', label='Warmup end')
plt.xlabel('Step')
plt.ylabel('Learning Rate')
plt.title('Transformer LR Schedule')
plt.legend()
plt.show()
```

---

## 常见问题

### Q: Warmup 步数怎么选？
**A:** 通常占总步数的 5-10%，比如训练 100k 步，Warmup 4k-10k。

### Q: 可以用更大的 Warmup 吗？
**A:** 可以，但 Warmup 太长会浪费训练时间。

### Q: 没有 Warmup 会怎样？
**A:** 初期梯度爆炸，Loss 变成 NaN，训练失败。

### Q: 学习率峰值是多少？
**A:** 在 Warmup 结束点：$\text{peak\_lr} = d_{\text{model}}^{-0.5} \cdot \text{warmup}^{-0.5}$

---

## 一句话总结

> **Warmup 防爆炸，Decay 精细调，min 函数自动切，Transformer 训练稳。**

---

## 相关笔记

- [[Transformer训练篇]] —— 完整训练代码实现
- [[Adam优化器]] —— 优化器参数设置
- [[学习率调度比较]] —— 各种调度策略对比
