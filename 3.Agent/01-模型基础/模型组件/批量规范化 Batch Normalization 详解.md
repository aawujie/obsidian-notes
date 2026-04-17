# 批量规范化 Batch Normalization 详解

> 创建日期：2026-03-09
> 来源：[动手学深度学习 7.5 节](https://zh.d2l.ai/chapter_convolutional-modern/batch-norm.html)
> 标签：#深度学习 #批量规范化 #BatchNorm #神经网络 #模型训练

---

## 一、核心结论

**批量规范化（Batch Normalization，BN）** 是一种流行且有效的技术，可**持续加速深层网络的收敛速度**。

**核心价值**：
- ✅ 加速深层网络训练收敛
- ✅ 允许使用更大的学习率
- ✅ 具有一定的正则化效果，减少过拟合
- ✅ 使得训练 100 层以上的网络成为可能（结合残差块）

> 💡 一句话理解：BN 通过在每次训练迭代中规范化中间层的输入分布，使网络各层的输出更加稳定，从而加速训练。

---

## 二、为什么需要批量规范化？

### 1. 数据预处理的重要性

训练神经网络时，数据预处理方式对最终结果产生巨大影响：
- 标准化输入特征（均值=0，方差=1）
- 使参数的量级统一，与优化器更好配合

### 2. 中间层变量分布偏移问题

**问题描述**：
- 训练过程中，中间层变量的变化范围可能很广
- 沿着从输入到输出的层，分布发生变化
- 跨同一层中的单元，分布不一致
- 随时间推移，模型参数更新导致分布变幻莫测

**影响**：
- 变量分布的偏移可能阻碍网络收敛
- 如果一个层的可变值是另一层的 100 倍，需要对学习率进行补偿调整

### 3. 深层网络容易过拟合

- 更深层的网络复杂度更高
- 正则化变得更加重要

---

## 三、批量规范化的原理

### 3.1 核心思想

批量规范化应用于单个可选层（也可以应用到所有层），其原理如下：

1. **规范化输入**：减去均值并除以标准差（基于当前小批量）
2. **应用比例系数和偏移**：学习拉伸参数 γ 和偏移参数 β

> **名称由来**：基于批量统计的标准化 → 批量规范化

### 3.2 数学公式

**批量规范化变换**：

$$\mathrm{BN}(\mathbf{x}) = \boldsymbol{\gamma} \odot \frac{\mathbf{x} - \hat{\boldsymbol{\mu}}_\mathcal{B}}{\hat{\boldsymbol{\sigma}}_\mathcal{B}} + \boldsymbol{\beta}$$

其中：
- $\mathbf{x} \in \mathcal{B}$：来自小批量 $\mathcal{B}$ 的输入
- $\hat{\boldsymbol{\mu}}_\mathcal{B}$：小批量 $\mathcal{B}$ 的样本均值
- $\hat{\boldsymbol{\sigma}}_\mathcal{B}$：小批量 $\mathcal{B}$ 的样本标准差
- $\boldsymbol{\gamma}$：拉伸参数（scale），可学习
- $\boldsymbol{\beta}$：偏移参数（shift），可学习

**均值和方差计算**：

$$\begin{aligned}
\hat{\boldsymbol{\mu}}_\mathcal{B} &= \frac{1}{|\mathcal{B}|} \sum_{\mathbf{x} \in \mathcal{B}} \mathbf{x} \\
\hat{\boldsymbol{\sigma}}_\mathcal{B}^2 &= \frac{1}{|\mathcal{B}|} \sum_{\mathbf{x} \in \mathcal{B}} (\mathbf{x} - \hat{\boldsymbol{\mu}}_{\mathcal{B}})^2 + \epsilon
\end{aligned}$$

**注意事项**：
- 添加小常量 $\epsilon > 0$，避免除以零
- $\boldsymbol{\gamma}$ 和 $\boldsymbol{\beta}$ 是需要与其他模型参数一起学习的参数
- 标准化后的小批量平均值为 0，单位方差为 1

### 3.3 批量大小的影响

- **小批量大小不能为 1**：减去均值后每个隐藏单元为 0，无法学习
- **有效且稳定的批量大小**：50~100 范围中的中等批量大小
- 批量规范化时，批量大小的选择比没有 BN 时更重要

### 3.4 噪声的正则化效应

估计值 $\hat{\boldsymbol{\mu}}_\mathcal{B}$ 和 $\hat{\boldsymbol{\sigma}}_\mathcal{B}$ 使用噪声估计来抵消缩放问题：
- 这种噪声是有益的
- 优化中的各种噪声源通常会导致更快的训练和较少的过拟合
- 噪声似乎是正则化的一种形式

---

## 四、批量规范化层

### 4.1 全连接层中的 BN

**位置**：仿射变换和激活函数之间

**计算流程**：
$$\mathbf{h} = \phi(\mathrm{BN}(\mathbf{W}\mathbf{x} + \mathbf{b}))$$

其中：
- $\mathbf{x}$：全连接层输入
- $\mathbf{W}$、$\mathbf{b}$：权重和偏置参数
- $\phi$：激活函数
- $\mathrm{BN}$：批量规范化运算符

### 4.2 卷积层中的 BN

**位置**：卷积层之后、非线性激活函数之前

**特殊处理**：
- 对**每个输出通道**执行批量规范化
- 每个通道有自己的拉伸参数 γ 和偏移参数 β（标量）
- 在小批量的 $m \cdot p \cdot q$ 个元素上同时执行 BN
  - $m$：样本数
  - $p$：高度
  - $q$：宽度

**计算方式**：
- 收集所有空间位置的值
- 在给定通道内应用相同的均值和方差
- 在每个空间位置对值进行规范化

### 4.3 训练模式 vs 预测模式

| 模式 | 均值和方差来源 | 用途 |
|------|---------------|------|
| **训练模式** | 当前小批量的统计量 | 通过小批量统计数据规范化 |
| **预测模式** | 整个数据集的统计量（移动平均） | 通过数据集统计规范化 |

**预测时的处理**：
- 使用移动平均估算整个训练数据集的样本均值和方差
- 在预测时使用它们得到确定的输出
- 可以逐个样本进行预测

---

## 五、从零实现 BatchNorm

### 5.1 PyTorch 实现

```python
import torch
from torch import nn
from d2l import torch as d2l

def batch_norm(X, gamma, beta, moving_mean, moving_var, eps, momentum):
    # 通过 is_grad_enabled() 来判断当前模式是训练模式还是预测模式
    if not torch.is_grad_enabled():
        # 预测模式：直接使用传入的移动平均所得的均值和方差
        X_hat = (X - moving_mean) / torch.sqrt(moving_var + eps)
    else:
        assert len(X.shape) in (2, 4)
        if len(X.shape) == 2:
            # 全连接层：计算特征维上的均值和方差
            mean = X.mean(dim=0)
            var = ((X - mean) ** 2).mean(dim=0)
        else:
            # 二维卷积层：计算通道维上（axis=1）的均值和方差
            # 保持 X 的形状以便后面可以做广播运算
            mean = X.mean(dim=(0, 2, 3), keepdim=True)
            var = ((X - mean) ** 2).mean(dim=(0, 2, 3), keepdim=True)
        
        # 训练模式：用当前的均值和方差做标准化
        X_hat = (X - mean) / torch.sqrt(var + eps)
        
        # 更新移动平均的均值和方差
        moving_mean = momentum * moving_mean + (1.0 - momentum) * mean
        moving_var = momentum * moving_var + (1.0 - momentum) * var
    
    Y = gamma * X_hat + beta  # 缩放和移位
    return Y, moving_mean.data, moving_var.data
```

### 5.2 BatchNorm 层类

```python
class BatchNorm(nn.Module):
    # num_features：完全连接层的输出数量或卷积层的输出通道数
    # num_dims：2 表示完全连接层，4 表示卷积层
    def __init__(self, num_features, num_dims):
        super().__init__()
        if num_dims == 2:
            shape = (1, num_features)
        else:
            shape = (1, num_features, 1, 1)
        
        # 参与求梯度和迭代的拉伸和偏移参数，分别初始化成 1 和 0
        self.gamma = nn.Parameter(torch.ones(shape))
        self.beta = nn.Parameter(torch.zeros(shape))
        
        # 非模型参数的变量初始化为 0 和 1
        self.moving_mean = torch.zeros(shape)
        self.moving_var = torch.ones(shape)

    def forward(self, X):
        # 如果 X 不在内存上，将 moving_mean 和 moving_var 复制到 X 所在显存上
        if self.moving_mean.device != X.device:
            self.moving_mean = self.moving_mean.to(X.device)
            self.moving_var = self.moving_var.to(X.device)
        
        # 保存更新过的 moving_mean 和 moving_var
        Y, self.moving_mean, self.moving_var = batch_norm(
            X, self.gamma, self.beta, self.moving_mean,
            self.moving_var, eps=1e-5, momentum=0.9)
        return Y
```

### 5.3 关键参数说明

| 参数 | 含义 | 典型值 |
|------|------|--------|
| `eps` | 方差估计值的小常量，避免除零 | 1e-5 或 1e-12 |
| `momentum` | 移动平均的动量 | 0.9 |
| `gamma` | 拉伸参数，初始化为 1 | 可学习 |
| `beta` | 偏移参数，初始化为 0 | 可学习 |

---

## 六、使用 BatchNorm 的 LeNet 示例

### 6.1 网络结构

```python
import torch
from torch import nn

net = nn.Sequential(
    nn.Conv2d(1, 6, kernel_size=5), 
    BatchNorm(6, num_dims=4),  # 卷积层后
    nn.Sigmoid(),
    
    nn.AvgPool2d(kernel_size=2, stride=2),
    
    nn.Conv2d(6, 16, kernel_size=5), 
    BatchNorm(16, num_dims=4),  # 卷积层后
    nn.Sigmoid(),
    
    nn.AvgPool2d(kernel_size=2, stride=2), 
    nn.Flatten(),
    
    nn.Linear(16*4*4, 120), 
    BatchNorm(120, num_dims=2),  # 全连接层后
    nn.Sigmoid(),
    
    nn.Linear(120, 84), 
    BatchNorm(84, num_dims=2),  # 全连接层后
    nn.Sigmoid(),
    
    nn.Linear(84, 10)
)
```

### 6.2 训练配置

```python
lr, num_epochs, batch_size = 1.0, 10, 256
train_iter, test_iter = d2l.load_data_fashion_mnist(batch_size)
d2l.train_ch6(net, train_iter, test_iter, num_epochs, lr, d2l.try_gpu())
```

**训练结果**：
```
loss 0.273, train acc 0.899, test acc 0.807
32293.9 examples/sec on cuda:0
```

> 💡 注意：使用 BN 后，学习率可以设置得更大（如 1.0），而传统 LeNet 通常需要更小的学习率。

### 6.3 查看学习到的参数

```python
# 查看第一个 BN 层的 gamma 和 beta
net[1].gamma.reshape((-1,)), net[1].beta.reshape((-1,))
```

**示例输出**：
```
gamma: tensor([0.4863, 2.8573, 2.3190, 4.3188, 3.8588, 1.7942])
beta: tensor([-0.0124, 1.4839, -1.7753, 2.3564, -3.8801, -2.1589])
```

---

## 七、深度学习框架的简明实现

### 7.1 PyTorch

```python
net = nn.Sequential(
    nn.Conv2d(1, 6, kernel_size=5), 
    nn.BatchNorm2d(6),  # 卷积层用 BatchNorm2d
    nn.Sigmoid(),
    nn.AvgPool2d(kernel_size=2, stride=2),
    
    nn.Conv2d(6, 16, kernel_size=5), 
    nn.BatchNorm2d(16),
    nn.Sigmoid(),
    nn.AvgPool2d(kernel_size=2, stride=2), 
    nn.Flatten(),
    
    nn.Linear(256, 120), 
    nn.BatchNorm1d(120),  # 全连接层用 BatchNorm1d
    nn.Sigmoid(),
    
    nn.Linear(120, 84), 
    nn.BatchNorm1d(84),
    nn.Sigmoid(),
    
    nn.Linear(84, 10)
)
```

### 7.2 TensorFlow/Keras

```python
def net():
    return tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(filters=6, kernel_size=5, input_shape=(28, 28, 1)),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Activation('sigmoid'),
        tf.keras.layers.AvgPool2D(pool_size=2, strides=2),
        
        tf.keras.layers.Conv2D(filters=16, kernel_size=5),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Activation('sigmoid'),
        tf.keras.layers.AvgPool2D(pool_size=2, strides=2),
        
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(120),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Activation('sigmoid'),
        
        tf.keras.layers.Dense(84),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Activation('sigmoid'),
        
        tf.keras.layers.Dense(10),
    ])
```

---

## 八、争议与讨论

### 8.1 原始解释：内部协变量偏移

批量规范化的提出者 Ioffe and Szegedy (2015) 解释其原理为：
- **减少内部协变量偏移（internal covariate shift）**
- 变量值的分布在训练过程中发生变化，BN 可以稳定这种分布

### 8.2 对原始解释的质疑

**两个问题**：
1. **用词不当**：这种偏移与严格定义的协变量偏移（covariate shift）非常不同
2. **解释模糊**：只提供了一种不明确的直觉，没有解释为什么技术如此有效

**学术辩论**：
- Ali Rahimi 在 2017 年 NeurIPS 演讲中将"内部协变量转移"作为焦点
- 将现代深度学习的实践比作"炼金术"
- Santurkar et al. (2018) 提出 BN 的成功解释与原始论文声称的行为相反

### 8.3 更合理的解释

尽管存在争议，BN 的实际效果已被广泛验证：
- 具有**正则化效果**（类似 Dropout）
- 使优化 landscape 更平滑
- 允许使用更大的学习率
- 减少对参数初始化的敏感性

> 📌 **重要提醒**：将这些指导性直觉与既定的科学事实区分开来。在撰写研究论文时，清楚地区分技术和直觉。

---

## 九、小结

| 要点 | 说明 |
|------|------|
| **核心机制** | 利用小批量的均值和标准差，不断调整神经网络的中间输出 |
| **效果** | 使整个神经网络各层的中间输出值更加稳定 |
| **全连接 vs 卷积** | 使用略有不同（卷积需要对每个通道单独处理） |
| **训练 vs 预测** | 计算方式不同（训练用小批量统计，预测用移动平均） |
| **副作用** | 主要是正则化效果 |
| **原始动机** | "减少内部协变量偏移"的解释可能不是有效的解释 |

---

## 十、练习与思考

1. **偏置参数**：在使用 BN 之前，是否可以从全连接层或卷积层中删除偏置参数？为什么？

2. **学习率对比**：比较 LeNet 在使用和不使用 BN 情况下的学习率，绘制训练和测试准确度的提高。

3. **BN 的位置**：是否需要在每个层中进行 BN？尝试不同的配置。

4. **BN vs Dropout**：可以通过 BN 来替换 Dropout 吗？行为会如何改变？

5. **参数分析**：确定参数 β 和 γ，并观察和分析结果。

6. **其他应用**：查看高级 API 中有关 BatchNorm 的在线文档，了解其他应用场景。

7. **研究思路**：
   - 可以应用的其他"规范化"转换？
   - 可以应用概率积分变换吗？
   - 全秩协方差估计可以吗？

---

## 十一、相关笔记

- [[卷积神经网络基础]]
- [[1×1 卷积通道降维原理（Inception 核心）]]
- [[ResNet 残差结构与瓶颈块]]
- [[Dropout 正则化技术]]
- [[深度学习优化方法]]
- [[模型压缩与加速技术]]

---

## 十二、参考资料

1. **原始论文**：Ioffe, S., & Szegedy, C. (2015). "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift". ICML 2015.

2. **质疑研究**：Santurkar, S., et al. (2018). "How Does Batch Normalization Help?". NeurIPS 2018.

3. **学术讨论**：Lipton, Z. C., & Steinhardt, J. (2018). "Troubling Trends in Machine Learning Scholarship".

4. **动手学深度学习**：[7.5 批量规范化](https://zh.d2l.ai/chapter_convolutional-modern/batch-norm.html)

---

*最后更新：2026-03-09*
