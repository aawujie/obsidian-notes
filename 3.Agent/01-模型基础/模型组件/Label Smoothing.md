# Label Smoothing —— 标签平滑正则化

> 防止模型对预测过于自信的正则化技术
> 整理日期：2026-03-28

---

## 一句话解释

**Label Smoothing** = 把 one-hot 标签"软化"，给其他类别留点概率，防止模型过拟合。

---

## 问题：模型太自信

### 标准交叉熵损失
```python
# 真实标签是 "猫"（one-hot: [1, 0, 0]）
# 模型预测: [0.99, 0.005, 0.005]

loss = -log(0.99) ≈ 0.01  # 损失很小，模型很满意
```

**问题**：
- 模型对 0.99 很满意，但对其他类别（狗、鸟）完全不学
- 容易过拟合
- 对新数据泛化差

---

## 解决方案：Label Smoothing

### 把 one-hot "软化"

| 类型 | 标签分布 |
|------|---------|
| **One-hot** | [1, 0, 0]（100% 确定是猫）|
| **Smoothed (ε=0.1)** | [0.9, 0.05, 0.05]（90% 猫，5% 狗，5% 鸟）|

### 公式

$$q'(k) = (1 - \varepsilon) \cdot \text{one\_hot}(k) + \frac{\varepsilon}{K}$$

- $\varepsilon$ = 0.1（平滑系数，原论文用的）
- $K$ = 类别数
- $(1-\varepsilon)$ = 0.9 给真实标签
- $\varepsilon/K$ = 0.1/3 ≈ 0.033 给其他每个标签

---

## 直观理解

**想象考试**：
- **One-hot**：标准答案说"选A"，你就坚信100%是A，其他选项完全不考虑
- **Label Smoothing**：标准答案说"选A"，但你也要想想"万一B也有点道理呢？"

这样模型不会"死记硬背"，而是学会"模糊的正确"。

---

## 代码实现

```python
class LabelSmoothingCrossEntropy(nn.Module):
    def __init__(self, vocab_size, smoothing=0.1, pad_idx=0):
        super().__init__()
        self.smoothing = smoothing
        self.confidence = 1.0 - smoothing  # 0.9
        self.vocab_size = vocab_size
        self.pad_idx = pad_idx

    def forward(self, pred, target):
        # 忽略 pad 位置
        mask = (target != self.pad_idx)
        pred = pred[mask]
        target = target[mask]

        if len(target) == 0:
            return torch.tensor(0.0, device=pred.device)

        log_probs = F.log_softmax(pred, dim=-1)

        # 构建平滑后的目标分布
        # 真实标签: [2]（类别2）
        # one-hot: [0, 0, 1, 0, 0]
        # 平滑后: [0.025, 0.025, 0.9, 0.025, 0.025]
        with torch.no_grad():
            true_dist = torch.full_like(
                log_probs, 
                self.smoothing / (self.vocab_size - 1)
            )
            true_dist.scatter_(1, target.unsqueeze(1), self.confidence)

        # KL 散度 = 交叉熵 - 熵（常数）
        loss = F.kl_div(log_probs, true_dist, reduction='batchmean')
        return loss
```

---

## 效果对比

| 场景 | 标准 CE | Label Smoothing |
|------|---------|-----------------|
| 预测 [0.99, 0.005, 0.005] | loss ≈ 0.01 ✅ | loss ≈ 0.15（更高，不能太自信）|
| 预测 [0.7, 0.2, 0.1] | loss ≈ 0.36 | loss ≈ 0.25 ✅（更好）|
| 泛化能力 | 容易过拟合 | 更好 |

---

## 为什么用 KL 散度？

$$KL(q' \| p) = \sum q'(x) \log\frac{q'(x)}{p(x)} = -H(q') + CE(q', p)$$

- $H(q')$ 是常数（平滑后的分布熵固定）
- 所以 **最小化 KL = 最小化交叉熵**

---

## 超参数选择

| ε 值 | 效果 |
|------|------|
| 0.0 | 标准交叉熵（无平滑）|
| 0.1 | 原论文推荐，平衡 |
| 0.2 | 更保守，更平滑 |

---

## 一句话总结

> **Label Smoothing = 别把话说太满，给其他选项留点余地，防止过拟合。**

---

## 相关笔记

- [[交叉熵损失]] —— 标准交叉熵详解
- [[Transformer训练篇]] —— Label Smoothing 在 Transformer 中的应用
- [[正则化技术]] —— Dropout、Weight Decay 等其他正则化方法
