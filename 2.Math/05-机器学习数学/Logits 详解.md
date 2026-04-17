# Logits 详解

> 创建时间：2026-04-11
> 标签： #深度学习 #机器学习 #分类 #softmax

---

## 一句话定义

<span style="color:rgb(255, 77, 77)"><b>Logits</b> 是神经网络最后一层（分类层）的<b>原始输出值</b>，<b>未经任何激活函数处理</b>。</span>

---

## 直观理解

```
输入 → 神经网络 → Logits → Softmax/Sigmoid → 概率
                    ↑
                 原始分数
```

---

## 数学定义

对于 $K$ 分类问题：

$$\text{Logits} = z = [z_1, z_2, ..., z_K]$$

<span style="color:rgb(255, 77, 77)">其中 $z_i$ 可以是<b>任意实数</b>（正数、负数、很大、很小）<br></span>
---

## 为什么叫 Logits？

名字来源于 <span style="color:rgb(255, 77, 77)"><b>log-odds（对数几率）</b></span>：

$$\text{logit}(p) = \log\left(\frac{p}{1-p}\right)$$

但在深度学习中，这个词被泛化为<span style="color:rgb(255, 77, 77)"><b>分类前的原始分数</b></span>。

---

## Logits vs 概率

|           | Logits                                           | 概率       |
| --------- | ------------------------------------------------ | -------- |
| **范围**    | $(-\infty, +\infty)$                             | $[0, 1]$ |
| **和为1**   | ❌ 否                                              | ✅ 是      |
| **可解释性**  | <span style="color:rgb(255, 77, 77)">相对大小</span> | 直观百分比    |
| **计算稳定性** | <span style="color:rgb(255, 77, 77)">可能溢出</span> | 归一化后稳定   |

**转换关系（Softmax）：**

$$P(y=i) = \frac{e^{z_i}}{\sum_{j=1}^K e^{z_j}}$$

---

## 代码示例

```python
import torch
import torch.nn.functional as F

# 神经网络输出 (3分类)
logits = torch.tensor([[2.0, 1.0, 0.1]])  # 原始分数

# 转成概率 (Softmax)
probs = F.softmax(logits, dim=1)
# probs = [[0.659, 0.242, 0.098]]

# 预测类别
predicted = torch.argmax(logits, dim=1)  # 取最大值的索引
# predicted = [0]  (第0类)
```

---

## 为什么要用 Logits？

### 1️⃣ 数值稳定性

<span style="color:rgb(255, 77, 77)">直接算 Softmax 可能溢出</span>：
```python
z = [1000, 1000, 1000]
exp(z) = [inf, inf, inf]  # 溢出！
```

**技巧**：<span style="color:rgb(255, 77, 77)">减去最大值</span>
```python
z_stable = z - max(z)  # [0, 0, 0]
```

### 2️⃣ 损失函数计算

交叉熵损失直接用 logits（更稳定）：
```python
# 推荐 ✅
loss = F.cross_entropy(logits, labels)  # 内部自动做 softmax

# 不推荐 ❌
probs = F.softmax(logits, dim=1)
loss = F.nll_loss(torch.log(probs), labels)  # 数值不稳定
```

### 3️⃣ 温度缩放 (Temperature Scaling)

调节 logits 可以控制预测置信度：
```python
T = 2.0  # 温度
soft_logits = logits / T  # 分布更"软"（更均匀）
```

---

## 常见误区

| ❌ 错误理解             | ✅ 正确理解                                                                       |
| ------------------ | ---------------------------------------------------------------------------- |
| Logits 是概率         | Logits 是**原始分数**，不是概率                                                        |
| Logits 必须在 [0,1]   | Logits 可以是**任意实数**                                                           |
| Softmax 输出叫 logits | <span style="color:rgb(255, 77, 77)">Softmax 输出叫 <b>probabilities</b></span> |

---

## 总结

> <span style="color:rgb(255, 77, 77)"><b>Logits = 神经网络分类前的原始输出，范围无限制，需经 Softmax/Sigmoid 转成概率。</b></span>

---

## 相关概念

- [[Softmax 函数]]
- [[Entropy_CrossEntropy_KLDivergence]]
- [[温度缩放]]
- [[神经网络输出层]]
