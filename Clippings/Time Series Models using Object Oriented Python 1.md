---
title: "Time Series Models using Object Oriented Python"
source: "https://www.quantstart.com/articles/time-series-models-using-object-oriented-python/"
author:
published:
created: 2026-04-26
description: "In this article we are going to continue designing and implementing an object oriented Python-based framework for generating realistic synthetic financial asset pricing series, by developing a framework for sampling from stochastic process based time series models."
tags:
  - "clippings"
---
在之前关于 [使用面向对象 Python 生成相关矩阵](https://www.quantstart.com/articles/correlation-matrix-generationg-using-object-oriented-python/) 的文章中，我们构建了一个 Python 面向对象类层次结构，以开发一个可扩展、模块化的工具，用于生成合成相关矩阵。此类矩阵可用于生成合成相关时间序列模型，进而可作为逼真的合成金融数据集的基础。

在本文中，我们将继续开发合成数据集生成工具，为时间序列生成器模型组件构建另一套面向对象的类层级结构。这些结构将构成相关合成资产定价数据的基础。

我们将考虑两种模型——即 [几何布朗运动](https://www.quantstart.com/articles/Geometric-Brownian-Motion/) （GBM）和 [跳跃-扩散](https://www.quantstart.com/articles/Jump-Diffusion-Models-for-European-Options-Pricing-in-C/) （JD）随机过程模型——并展示如何通过这个类层次结构实现它们。

在实现完这两个模型后，我们将编写一个基于 Matplotlib 的可视化脚本。我们会用它来对比多个路径实现下各模型的表现。

这是我们将在本文中开发的工具所生成结果的抢先预览：

![Example asset price paths from Geometric Brownian Motion and Jump Diffusion models](https://quantstartmedia.s3.us-east-1.amazonaws.com/images/article-images/articles/time-series-models-using-object-oriented-python/asset-price-path-visualization.png)

Example asset price paths from Geometric Brownian Motion and Jump Diffusion models

我们将首先开发定义时间序列模型类接口的抽象基类。然后实现GBM和JD这两个派生子类。接着我们将使用这些类生成一些样本路径。

## 抽象基类

第一个任务是定义类接口，方法与 [前文](https://www.quantstart.com/articles/correlation-matrix-generationg-using-object-oriented-python/) 类似。这需要导入合适的 Python ABC 机制以及第三方 NumPy 库，该库将用于存储价格路径。相关代码将存放在名为 `models.py` 的新文件中：

```python
# models.py

from abc import ABC, abstractmethod
from typing import Tuple, Optional

import numpy as np
```

下一个任务是创建一个 `TimeSeriesModel` 基类，该类将为所有后续继承自它的时间序列模型子类定义接口。

The `__init__` initialisation method takes in two arguments--the starting price $S_{0}$, `start_price`, and the time series model time step $\Delta t$, `dt`. The latter defaults to $1 / 252$, which accounts for the approximately 252 business days per year (since we are currently considering daily pricing models):`__init__` 初始化方法接收两个参数——起始价格 $S_{0}$ 、 `start_price` ，以及时间序列模型的时间步长 $\Delta t$ 、 `dt` 。后者默认值为 $1 / 252$ ，这对应每年约 252 个交易日（因为我们目前考虑的是日度定价模型）：

```python
# ..
# models.py
# ..

class TimeSeriesModel(ABC):
    """
    Abstract base class for time series models.
    """
    
    def __init__(
        self,
        start_price: float,
        dt: float = 1/252
    ):
        """
        Initialize the time series model.
        
        Args:
            start_price: Initial price of the asset
            dt: Time step (default: 1/252 for daily data)
        """
        self.start_price = start_price
        self.dt = dt
```

类接口暴露了一个单独的“公共”方法 `generate_path` 。该方法接收一个步数 `n` （本质上是用于生成定价的天数）和一个名为 `random_shocks` 的随机变量抽样NumPy数组。后者提供了相关的随机变量，将用于将时间序列模型的多个独立实现关联起来。该方法旨在返回一个包含模型单次实现价格的NumPy数组：

```python
# ..
# models.py
# ..

    @abstractmethod
    def generate_path(
        self,
        n_steps: int,
        random_shocks: np.ndarray
    ) -> np.ndarray:
        """
        Generate a price path given random shocks.
        
        Args:
            n_steps: Number of time steps
            random_shocks: Array of random shocks (already correlated)
        
        Returns:
            Array of prices
        """
        pass
```

既然我们已经为这些时间序列开发了类接口，现在可以从几何布朗运动开始，讨论实际的具体实现了。

## 几何布朗运动

我们已经在 QuantStart 上详细讨论过几何布朗运动（请参阅之前关于 [几何布朗运动](https://www.quantstart.com/articles/Geometric-Brownian-Motion/) 和 [使用 Python 进行几何布朗运动模拟](https://www.quantstart.com/articles/geometric-brownian-motion-simulation-with-python/) 的文章），但我们将在下方的信息框中对其进行数学回顾，以帮助你在许久未接触其数学细节时重新熟悉这一概念。

Geometric Brownian is a very common [Stochastic Differential Equation](https://www.quantstart.com/articles/Stochastic-Differential-Equations/) (SDE) model for the time-evolution of an asset price $S \left(\right. t \left.\right)$. The SDE for GBM is given by:几何布朗运动是一种非常常见的资产价格 \\(S(t)\\) 时间演化的随机微分方程（SDE）模型。几何布朗运动的随机微分方程如下所示：

$$
d S \left(\right. t \left.\right) = \mu S \left(\right. t \left.\right) d t + \sigma S \left(\right. t \left.\right) d B \left(\right. t \left.\right)
$$

Note that the coefficients $\mu$ and $\sigma$, representing the *drift* and *volatility* of the asset, respectively, are both constant in this model. In more sophisticated models they can be made to be functions of $t$, $S \left(\right. t \left.\right)$ and other stochastic processes (such as with [Stochastic Volality](https://www.quantstart.com/articles/Heston-Stochastic-Volatility-Model-with-Euler-Discretisation-in-C/) models).请注意，代表资产 $\mu$ 和 *波动率* 的系数μ与 $\sigma$ 在该模型中均为常数。在更复杂的模型中，它们可以被设定为 $t$ 、 $S \left(\right. t \left.\right)$ 以及其他随机过程的函数（例如在 [Stochastic Volality](https://www.quantstart.com/articles/Heston-Stochastic-Volatility-Model-with-Euler-Discretisation-in-C/) 模型中）。

The solution $S \left(\right. t \left.\right)$ can be found by the application of [Ito's Lemma](https://www.quantstart.com/articles/Itos-Lemma/) to the stochastic differential equation. We won't derive this in full here, but will simply present the result:通过将 $S \left(\right. t \left.\right)$ 应用于随机微分方程，可以求得解S(t)。我们在此不进行完整推导，仅给出结果：

$$
S \left(\right. t \left.\right) = S \left(\right. 0 \left.\right) exp ⁡ \left(\right. \left(\right. \mu - \frac{1}{2} \sigma^{2} \left.\right) t + \sigma B \left(\right. t \left.\right) \left.\right)
$$

我们现在将利用这些公式，结合欧拉-丸山离散化等合适的数值方法，编写一段Python代码来模拟该模型的单次实现。

要实现几何布朗运动模型，我们首先编写 `__init__` 初始化方法。我们提供构成基类 `TimeSeriesModel` 接口的两个参数，即 `start_price` 和 `dt` 。我们还提供两个额外的浮点型关键字参数 `drift` 和 `volatility` ，它们用于对模型行为进行参数化：

```python
# ..
# models.py
# ..

class GeometricBrownianMotion(TimeSeriesModel):
    """
    Geometric Brownian Motion model for asset prices.
    """
    
    def __init__(
        self, 
        start_price: float,
        dt: float,
        drift: float = 0.0, 
        volatility: float = 0.2,
    ):
        """
        Initialize the Geometric Brownian Motion model.

        Args:
            start_price: Initial price of the asset
            dt: Time step (default: 1/252 for daily data)
            drift: Annual drift parameter (mu)
            volatility: Annual volatility parameter (sigma)
        """
        super().__init__(start_price, dt)
        self.drift = drift
        self.volatility = volatility
```

下一步是编写 `generate_path` 方法的代码。如前所述，该方法需要两个参数， `n` 表示路径中的步数， `random_shocks` 用于从外部控制类接收相关随机变量，该控制类将在后续文章中开发。

The method initially creates a one-dimensional (1D) `prices` array and sets the first value equal to the provided starting price. We then precalculate the value of $\sqrt{\Delta t}$ to avoid calculating this unnecessarily within the loop.该方法首先创建一个一维（1D） `prices` 数组，并将第一个值设为提供的起始价格。随后我们预先计算 $\sqrt{\Delta t}$ 的值，以避免在循环中不必要地计算该值。

We now iterate over the number of steps and calculate both the drift and diffusion components of GBM. Importantly, note the usage of `random_shocks` within the diffusion term. Finally, the next price instance $S \left(\right. t + 1 \left.\right)$ is calculated as the multiple of the current price $S \left(\right. 0 \left.\right)$ and the exponential of the sum of the drift and the diffusion components.我们现在迭代步数，并计算几何布朗运动（GBM）的漂移项和扩散项。需要重点注意扩散项中 `random_shocks` 的使用方式。最后，下一个价格实例 $S \left(\right. t + 1 \left.\right)$ 的计算方式为当前价格 $S \left(\right. 0 \left.\right)$ 与漂移项和扩散项之和的指数的乘积。

我们不需要返回数组中的第一个价格，因为这将由外部类计算：

```python
# ..
# models.py
# ..

    def generate_path(
        self,
        n_steps: int,
        random_shocks: np.ndarray
    ) -> np.ndarray:
        """
        Generate a GBM price path.
        """
        prices = np.zeros(n_steps + 1)
        prices[0] = self.start_price
        
        # GBM formula: S(t+dt) = S(t) * exp((mu - 0.5*sigma^2)*dt + sigma*sqrt(dt)*Z)
        dt_sqrt = np.sqrt(self.dt)
        
        for t in range(n_steps):
            drift_component = (self.drift - 0.5 * self.volatility**2) * self.dt
            diffusion_component = self.volatility * dt_sqrt * random_shocks[t]
            prices[t + 1] = prices[t] * np.exp(drift_component + diffusion_component)
        
        return prices[1:]  # Return prices excluding the initial price
```

这就完成了 `GeometricBrownianMotion` 随机过程模型的实现。尽管该模型是模拟股票行为的一个实用起点（并且被应用于众多期权定价工具中），但它并未涵盖真实股票价格序列中存在的诸多“典型事实”。

这包括波动聚集行为以及随机跳跃（例如因夜间发生重大影响价格的新闻而引发的跳跃）。后一种效应可通过所谓的跳跃-扩散模型进行建模，该模型将在下一节中实现。

## 跳跃扩散

以下代码片段实现了 `JumpDiffusion` 时间序列模型，该模型纳入了随机价格跳变，用于模拟能够急剧且快速改变公司股票价格的信息所产生的影响。该模型本质上是一条几何布朗运动路径（包含所有相关参数），会周期性受到泊松模型分布的特定幅度的随机跳变（跳变幅度也具有随机性）。

For the initialization method `__init__` we add three new parameters compared to Geomtric Brownian Motion. The first is `jump_intensity`, which measures the average number of jumps per year ($\lambda$). The second is `jump_mean`, which is the mean average value of the jump. The final value is `jump_std`, which measures the standard deviation of the jump magnitude:与几何布朗运动相比，我们在初始化方法 `__init__` 中新增了三个参数。第一个是 `jump_intensity` ，用于衡量每年的平均跳跃次数（ $\lambda$ ）。第二个是 `jump_mean` ，即跳跃的平均值。最后一个参数是 `jump_std` ，用于衡量跳跃幅度的标准差：

```python
# ..
# models.py
# ..

class JumpDiffusion(TimeSeriesModel):
    """
    Jump-Diffusion model for asset prices.
    """
    
    def __init__(
        self,
        start_price: float,
        dt: float = 1/252,
        drift: float = 0.0,
        volatility: float = 0.2,
        jump_intensity: float = 0.1,
        jump_mean: float = 0.0,
        jump_std: float = 0.1,
    ):
        """
        Initialize the Jump-Diffusion model.
        
        Args:
            start_price: Initial price of the asset
            dt: Time step (default: 1/252 for daily data)
            drift: Annual drift parameter (mu)
            volatility: Annual volatility parameter (sigma)
            jump_intensity: Average number of jumps per year (lambda)
            jump_mean: Mean of jump size (log-normal)
            jump_std: Standard deviation of jump size (log-normal)
        """
        super().__init__(start_price, dt)
        self.drift = drift
        self.volatility = volatility
        self.jump_intensity = jump_intensity
        self.jump_mean = jump_mean
        self.jump_std = jump_std
```

由于以下 `generate_path` 方法包含了一些关于跳跃建模的相当复杂的概率和统计假设，我们添加了一个完整的信息框来描述模型背后的假设。如果你熟悉跳跃扩散模型的工作原理，就可以跳过这一部分，直接查看下面的代码。

The `generate_path` method implements the Jump-Diffusion model, which combines continuous Geometric Brownian Motion with discontinuous Poisson-distributed jumps. In our implementation below we actually utilise binomial distributions to represent Poisson jumps. This is because when $\Delta t$ (`dt`) is small (as it typically is for daily time steps like $\Delta t = 1 / 252$), the probability of multiple jumps occurring in a single time step becomes negligible.`generate_path` 方法实现了跳跃-扩散模型，该模型将连续的几何布朗运动与不连续的泊松分布跳跃相结合。在下方的实现中，我们实际使用二项分布来表示泊松跳跃。这是因为当 $\Delta t$ （ `dt` ）较小时（对于 $\Delta t = 1 / 252$ 这样的日度时间步长，情况通常如此），在单个时间步长内发生多次跳跃的概率可以忽略不计。

In this limit, a Poisson process with rate $\lambda \Delta t$ can be well-approximated by a Bernoulli (binomial with $n = 1$) random variable that takes value 1 with probability $\lambda \Delta t$ and 0 otherwise. This is why the code uses `np.random.binomial(1, jump_probs, n_steps)` where `jump_probs = self.jump_intensity * self.dt`. It is determining whether a jump occurs (1) or not (0) at each time step.在这一极限下，速率为 $\lambda \Delta t$ 的泊松过程可以用伯努利分布（ $n = 1$ 的二项分布）随机变量很好地近似，该变量以概率 $\lambda \Delta t$ 取值为1，否则取值为0。这就是代码中使用 `np.random.binomial(1, jump_probs, n_steps)` 的原因，其中 `jump_probs = self.jump_intensity * self.dt` 。该代码用于判断每个时间步是否发生跳变（1表示发生，0表示未发生）。

The method then generates jump sizes only for time steps where jumps occur. These jump sizes follow a log-normal distribution (controlled by `jump_mean` and `jump_std`), which ensures that prices remain positive after jumps. The expression `np.exp(np.random.normal(...)) - 1` converts the log-normal random variable into a returns (rather than price) format - if $J$ is log-normal, then $\left(\right. J - 1 \left.\right)$ represents the proportional change in price. The continuous component follows standard GBM dynamics with the drift and diffusion terms, where the drift includes the usual Itô correction term `(-0.5 * volatility^2)`.该方法仅为发生跳跃的时间步生成跳跃幅度。这些跳跃幅度遵循对数正态分布（由 `jump_mean` 和 `jump_std` 控制），可确保跳跃后价格仍保持为正值。表达式 `np.exp(np.random.normal(...)) - 1` 将对数正态随机变量转换为收益率（而非价格）格式——若 $J$ 服从对数正态分布，则 $\left(\right. J - 1 \left.\right)$ 表示价格的比例变动。连续部分遵循带漂移项和扩散项的标准几何布朗运动（GBM）动态模型，其中漂移项包含常规伊藤校正项 `(-0.5 * volatility^2)` 。

最后，价格演变通过乘法结合了两个组成部分： `prices[t + 1] = prices[t] * np.exp(drift_component + diffusion_component) * (1 + jump_component)` 。几何布朗运动（GBM）部分以指数形式应用（确保价格为正），而跳跃部分则以乘法因子 `(1 + jump_component)` 的形式应用。

这种设定确保了跳变会使价格产生比例变化而非绝对变化，这对金融资产而言更符合实际情况。该近似方法的优势在于，在典型的金融建模时间尺度上，它既计算高效又具备数学合理性，无需从泊松分布中显式抽样，也无需处理每个时间步出现多次跳变的罕见情况。

The code begins by generating a zero array `prices`, for which the first value is filled with the starting price. As with the GBM implementation, we precalculate $\sqrt{\Delta t}$. Subsequently the probabilities and actual occurence dates for the jumps are calculated using the approach outlined in the info box describing the model. The number of jumps is then calculated as the sum of the occurences of jumps (since each entry in `jumps_occur` is unity).代码首先生成一个零数组 `prices` ，并将其第一个值填充为起始价格。与GBM实现一样，我们预先计算 $\sqrt{\Delta t}$ 。随后，利用信息框中描述该模型的方法计算跳跃的概率和实际发生日期。接着计算跳跃次数，即跳跃发生次数之和（因为 `jumps_occur` 中的每个元素均为1）。

如果存在非零数量的跳跃，则 `jump_sizes` 数组中每个值为1的元素都会被设为随机对数正态跳跃值。该方法的其余部分与几何布朗运动的实现类似，区别在于需要将价格乘以 `1 + jump_component` ，以考虑乘性（比例）跳跃：

```python
# ..
# models.py
# ..

    def generate_path(
        self,
        n_steps: int,
        random_shocks: np.ndarray
    ) -> np.ndarray:
        """
        Generate a Jump-Diffusion price path.
        """
        prices = np.zeros(n_steps + 1)
        prices[0] = self.start_price
        
        dt_sqrt = np.sqrt(self.dt)
        
        # Generate jump occurrences
        jump_probs = self.jump_intensity * self.dt
        jumps_occur = np.random.binomial(1, jump_probs, n_steps)
        
        # Generate jump sizes
        jump_sizes = np.zeros(n_steps)
        n_jumps = jumps_occur.sum()
        if n_jumps > 0:
            # Log-normal jumps
            jump_sizes[jumps_occur == 1] = np.exp(
                np.random.normal(self.jump_mean, self.jump_std, n_jumps)
            ) - 1
        
        for t in range(n_steps):
            # GBM component
            drift_component = (self.drift - 0.5 * self.volatility**2) * self.dt
            diffusion_component = self.volatility * dt_sqrt * random_shocks[t]
            
            # Jump component
            jump_component = jump_sizes[t]
            
            # Combined price evolution
            prices[t + 1] = prices[t] * np.exp(drift_component + diffusion_component) * (1 + jump_component)
        
        return prices[1:]  # Return prices excluding the initial price
```

至此， `models.py` 文件编写完成。与上一篇文章中介绍的 `correlation.py` 模块一样，该模块没有入口点，仅包含时间序列模型的类定义与实现。接下来我们将采用与 [上一篇文章](https://www.quantstart.com/articles/correlation-matrix-generationg-using-object-oriented-python/) 可视化相关矩阵实例类似的方法，对从各几何布朗运动模型和跳跃扩散模型中生成的路径集进行可视化处理。

为了实现这一点，我们将在下一节中编写一个简短的可视化脚本，该脚本会并排显示每个时间序列模型的一组随机样本路径。

## 资产价格路径可视化

我们可以利用 NumPy 和 Matplotlib 来生成各时间序列模型样本的可视化结果。我们新建一个名为 `models_visualization.py` 的文件，并将其与 `models.py` 放在同一目录下。对于每个模型，我们可以使用 Matplotlib 的 `plot` 方法，以交易日索引为横轴、资产价格路径值为纵轴进行绘图。

我们首先导入必要的库以及从 `models.py` 中刚刚实现的类：

```python
# models_visualization.py

import matplotlib.pyplot as plt
import numpy as np

from models import (
    GeometricBrownianMotion,
    JumpDiffusion
)
```

要实现的第一个函数是 `generate_paths` 。它接收多个参数。第一个是时间序列模型实例 `model` ，在本示例中，该实例要么是几何布朗运动模型实例，要么是跳跃扩散模型实例。它需要步数 `n_steps` ，在本示例中其默认值为 252（一年）。还需要绘制的独立路径实现数量 `n_paths` 。最后，可通过 `seed` 提供一个可选随机种子，以确保能复现结果。

该函数首先会设置随机种子（如果提供了的话）。然后它会创建一个大小为 `(n_paths, n_steps)` 的空二维零矩阵，用于存储最终的路径实现值。接着，函数会遍历每一条路径并生成“随机冲击”数组，该数组用于存储每个模型中用到的随机变量。在后续的文章中，我们不会在此处简单使用标准正态（高斯）值，而是会通过一种被称为 [乔莱斯基分解](https://www.quantstart.com/articles/Cholesky-Decomposition-in-Python-and-NumPy/) 的技术，采用能够为每条路径实例提供相关性的数值。

最后，我们通过调用每个模型对应的 `generate_paths` 方法，并传入所需的步数以及随机变量组成的 `random_shocks` 数组，来创建每条路径本身：

```python
# ..
# models_visualization.py
# ..

def generate_paths(model, n_steps, n_paths, seed=None):
    """
    Generate multiple price paths for a given model.
    
    Args:
        model: TimeSeriesModel instance
        n_steps: Number of time steps per path
        n_paths: Number of paths to generate
        seed: Random seed for reproducibility
    
    Returns:
        Array of shape (n_paths, n_steps) containing all price paths
    """
    if seed is not None:
        np.random.seed(seed)
    
    paths = np.zeros((n_paths, n_steps))
    
    for i in range(n_paths):
        # Generate uncorrelated standard normal shocks
        random_shocks = np.random.standard_normal(n_steps)
        paths[i] = model.generate_path(n_steps, random_shocks)
    
    return paths
```

The next function to implement is `plot_model_paths`. This function takes in multiple parameters. Firstly, it requires a Matplotlib Axes object on which to produce the plots. It requires the `(n_paths, n_steps)` -sized 2D NumPy array that was generated in the previous function, called `paths`. It then requires the name of the time series model used (`model_name`) to name the model in the figure. It requires $\Delta t$ (`dt`) in order to calculate the correct number of time steps utilised. Finally, it takes in alpha transparency value (`alpha`) to add to the path plot lines.下一个要实现的函数是 `plot_model_paths` 。该函数包含多个参数。首先，它需要一个 Matplotlib Axes 对象，用于绘制图表。它需要在前一个函数中生成的、大小为 `(n_paths, n_steps)` 的二维 NumPy 数组 `paths` 。接着，它需要传入时间序列模型的名称 `model_name` ，以便在图表中对模型进行命名。它需要 $\Delta t$ （即 `dt` ）来计算所用的正确时间步数。最后，它接收一个 alpha 透明度值 `alpha` ，用于为路径绘图线条添加透明度。

该函数遍历路径数量，并使用 Matplotlib 折线图的 `plot` 方法，以指定的 alpha 透明度和预设的线宽，将计算出的时间步长（ `time_steps` ）与存储在二维 `paths` 数组中的各条路径行进行绘图。

它还以更深的黑色添加了平均路径，该路径是根据提供的所有路径实现计算得出的，以突出模型的样本平均行为。最后，添加了一些x轴和y轴标签，同时还有标题、网格和图例：

```python
# ..
# models_visualization.py
# ..

def plot_model_paths(ax, paths, model_name, dt, alpha=0.3):
    """
    Plot multiple paths on a given axes.
    
    Args:
        ax: Matplotlib axes object
        paths: Array of shape (n_paths, n_steps) containing price paths
        model_name: Name of the model for the title
        dt: Time step size
        alpha: Transparency level for the paths
    """
    n_paths, n_steps = paths.shape
    time_steps = np.arange(n_steps) * dt * 252  # Convert to trading days
    
    # Plot all paths with transparency
    for i in range(n_paths):
        ax.plot(time_steps, paths[i], alpha=alpha, linewidth=0.8)
    
    # Calculate and plot mean path in bold
    mean_path = np.mean(paths, axis=0)
    ax.plot(time_steps, mean_path, 'k-', linewidth=2, label='Mean', alpha=0.8)
    
    ax.set_xlabel('Time (trading days)')
    ax.set_ylabel('Price')
    ax.set_title(f'{model_name} - {n_paths} Path Realizations')
    ax.grid(True, alpha=0.8)
    ax.legend(loc='best')
```

创建好这两个函数后，现在就可以用 `main` 函数来实现入口点了。

该入口的第一部分设置了多个参数，包括路径数量、时间步数量、模型初始价格、每日时间步、各模型的漂移率和波动率，以及模型特定参数，最后还设置了用于可复现性的随机种子。每个参数都附带注释，以说明其与之前模型实现的关联方式：

```python
# ..
# models_visualization.py
# ..

def main():
    # Configuration parameters
    k = 50  # Number of path realizations
    n_steps = 252  # Number of time steps (1 year of daily data)
    
    # Model parameters
    start_price = 100.0
    dt = 1/252  # Daily time step
    
    # GBM parameters
    gbm_drift = 0.05  # 5% annual drift
    gbm_volatility = 0.2  # 20% annual volatility
    
    # Jump-Diffusion parameters
    jd_drift = 0.05  # 5% annual drift
    jd_volatility = 0.15  # 15% annual volatility (lower than GBM since jumps add volatility)
    jump_intensity = 5.0  # Average 5 jumps per year
    jump_mean = -0.03  # Average jump size (log-normal mean)
    jump_std = 0.06  # Jump size standard deviation
    
    # Random seed for reproducibility (set to None for random results)
    seed = 42
```

在 `main` 函数的下一部分，几何布朗运动模型 `gbm_model` 和跳跃扩散模型 `jd_model` 均使用上述定义的所有参数进行了实例化：

```python
# ..
# models_visualization.py
# ..

    # Initialize models
    gbm_model = GeometricBrownianMotion(
        start_price=start_price,
        dt=dt,
        drift=gbm_drift,
        volatility=gbm_volatility
    )
    
    jd_model = JumpDiffusion(
        start_price=start_price,
        dt=dt,
        drift=jd_drift,
        volatility=jd_volatility,
        jump_intensity=jump_intensity,
        jump_mean=jump_mean,
        jump_std=jump_std
    )
```

`main` 函数的最后一部分会通过各自的 `generate_paths` 方法，从每个模型中生成不同的路径实现。随后创建一个 Matplotlib 子图，该子图包含一行两列。利用之前定义的模型实例，将每个模型的路径分别绘制在独立的轴对象上。

最后，添加标题并将图形显示在屏幕上（也可选择保存为 PNG 格式到磁盘）：

```python
# ..
# models_visualization.py
# ..

    # Generate paths
    print("\nGenerating paths...")
    gbm_paths = generate_paths(gbm_model, n_steps, k, seed=seed)
    jd_paths = generate_paths(jd_model, n_steps, k, seed=seed if seed else None)
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot GBM paths
    plot_model_paths(ax1, gbm_paths, "Geometric Brownian Motion", dt, alpha=0.5)
    
    # Plot Jump-Diffusion paths
    plot_model_paths(ax2, jd_paths, "Jump-Diffusion", dt, alpha=0.5)
    
    # Add overall title
    fig.suptitle('Comparison of Time Series Models', fontsize=16)
    
    # Adjust layout
    plt.tight_layout()
    
    # Display the plot
    plt.show()

    # Optional: Save the figure
    # plt.savefig('asset_price_path_visualization.png', dpi=150, bbox_inches='tight')
```

最后，为了确保在命令行中通过 Python 调用该文件时能正确执行目标函数，有必要在入口点中调用 `main` 函数：

```python
# ..
# models_visualization.py
# ..

if __name__ == "__main__":
    main()
```

在合适的虚拟环境中，你可以在终端中运行以下命令：

```bash
python3 models_visualization.py
```

该脚本的结果可从下图中查看。左侧展示了几何布朗运动模型的50条样本路径节选，以及一条黑色的样本均值平均路径。右侧展示了跳跃-扩散模型的50条样本路径节选，以及另一条黑色的样本均值平均路径。

这里选择的跳跃次数与跳跃尺度均是为了突出两种模型的差异。显而易见，跳跃扩散路径在整个路径历史中包含多个明显的价格大幅涨跌跳跃。由于跳跃均值被设定为略负，由此可见，这一设定抵消了轻微的上行趋势，从而形成了样本均值呈下降趋势的平均路径。

![Example asset price paths from Geometric Brownian Motion and Jump Diffusion models](https://quantstartmedia.s3.us-east-1.amazonaws.com/images/article-images/articles/time-series-models-using-object-oriented-python/asset-price-path-visualization.png)

Example asset price paths from Geometric Brownian Motion and Jump Diffusion models

## 后续步骤

我们已经为合成数据生成工具开发出了两个组件，分别是相关矩阵生成器和时间序列模型类层次结构。在下一篇文章中，我们将开发一个组件，该组件将利用一种名为乔列斯基分解的技术生成相关随机变量，这一技术将用于生成相关价格路径。随后，我们将演示如何将这些路径以 CSV 格式持久化到磁盘中，以便在下游的量化交易系统中使用。

## 完整代码

```python
# models.py

from abc import ABC, abstractmethod
from typing import Tuple, Optional

import numpy as np

class TimeSeriesModel(ABC):
    """
    Abstract base class for time series models.
    """
    
    def __init__(
        self,
        start_price: float,
        dt: float = 1/252
    ):
        """
        Initialize the time series model.
        
        Args:
            start_price: Initial price of the asset
            dt: Time step (default: 1/252 for daily data)
        """
        self.start_price = start_price
        self.dt = dt

    @abstractmethod
    def generate_path(
        self,
        n_steps: int,
        random_shocks: np.ndarray
    ) -> np.ndarray:
        """
        Generate a price path given random shocks.
        
        Args:
            n_steps: Number of time steps
            random_shocks: Array of random shocks (already correlated)
        
        Returns:
            Array of prices
        """
        pass

class GeometricBrownianMotion(TimeSeriesModel):
    """
    Geometric Brownian Motion model for asset prices.
    """
    
    def __init__(
        self, 
        start_price: float,
        dt: float,
        drift: float = 0.0, 
        volatility: float = 0.2,
    ):
        """
        Initialize the Geometric Brownian Motion model.

        Args:
            start_price: Initial price of the asset
            dt: Time step (default: 1/252 for daily data)
            drift: Annual drift parameter (mu)
            volatility: Annual volatility parameter (sigma)
        """
        super().__init__(start_price, dt)
        self.drift = drift
        self.volatility = volatility

    def generate_path(
        self,
        n_steps: int,
        random_shocks: np.ndarray
    ) -> np.ndarray:
        """
        Generate a GBM price path.
        """
        prices = np.zeros(n_steps + 1)
        prices[0] = self.start_price
        
        # GBM formula: S(t+dt) = S(t) * exp((mu - 0.5*sigma^2)*dt + sigma*sqrt(dt)*Z)
        dt_sqrt = np.sqrt(self.dt)
        
        for t in range(n_steps):
            drift_component = (self.drift - 0.5 * self.volatility**2) * self.dt
            diffusion_component = self.volatility * dt_sqrt * random_shocks[t]
            prices[t + 1] = prices[t] * np.exp(drift_component + diffusion_component)
        
        return prices[1:]  # Return prices excluding the initial price

class JumpDiffusion(TimeSeriesModel):
    """
    Jump-Diffusion model for asset prices.
    """
    
    def __init__(
        self,
        start_price: float,
        dt: float = 1/252,
        drift: float = 0.0,
        volatility: float = 0.2,
        jump_intensity: float = 0.1,
        jump_mean: float = 0.0,
        jump_std: float = 0.1,
    ):
        """
        Initialize the Jump-Diffusion model.
        
        Args:
            start_price: Initial price of the asset
            dt: Time step (default: 1/252 for daily data)
            drift: Annual drift parameter (mu)
            volatility: Annual volatility parameter (sigma)
            jump_intensity: Average number of jumps per year (lambda)
            jump_mean: Mean of jump size (log-normal)
            jump_std: Standard deviation of jump size (log-normal)
        """
        super().__init__(start_price, dt)
        self.drift = drift
        self.volatility = volatility
        self.jump_intensity = jump_intensity
        self.jump_mean = jump_mean
        self.jump_std = jump_std

    def generate_path(
        self,
        n_steps: int,
        random_shocks: np.ndarray
    ) -> np.ndarray:
        """
        Generate a Jump-Diffusion price path.
        """
        prices = np.zeros(n_steps + 1)
        prices[0] = self.start_price
        
        dt_sqrt = np.sqrt(self.dt)
        
        # Generate jump occurrences
        jump_probs = self.jump_intensity * self.dt
        jumps_occur = np.random.binomial(1, jump_probs, n_steps)
        
        # Generate jump sizes
        jump_sizes = np.zeros(n_steps)
        n_jumps = jumps_occur.sum()
        if n_jumps > 0:
            # Log-normal jumps
            jump_sizes[jumps_occur == 1] = np.exp(
                np.random.normal(self.jump_mean, self.jump_std, n_jumps)
            ) - 1
        
        for t in range(n_steps):
            # GBM component
            drift_component = (self.drift - 0.5 * self.volatility**2) * self.dt
            diffusion_component = self.volatility * dt_sqrt * random_shocks[t]
            
            # Jump component
            jump_component = jump_sizes[t]
            
            # Combined price evolution
            prices[t + 1] = prices[t] * np.exp(drift_component + diffusion_component) * (1 + jump_component)
        
        return prices[1:]  # Return prices excluding the initial price
```

```python
# model_visualization.py

import matplotlib.pyplot as plt
import numpy as np

from models import GeometricBrownianMotion, JumpDiffusion

def generate_paths(model, n_steps, n_paths, seed=None):
    """
    Generate multiple price paths for a given model.
    
    Args:
        model: TimeSeriesModel instance
        n_steps: Number of time steps per path
        n_paths: Number of paths to generate
        seed: Random seed for reproducibility
    
    Returns:
        Array of shape (n_paths, n_steps) containing all price paths
    """
    if seed is not None:
        np.random.seed(seed)
    
    paths = np.zeros((n_paths, n_steps))
    
    for i in range(n_paths):
        # Generate uncorrelated standard normal shocks
        random_shocks = np.random.standard_normal(n_steps)
        paths[i] = model.generate_path(n_steps, random_shocks)
    
    return paths

def plot_model_paths(ax, paths, model_name, dt, alpha=0.3):
    """
    Plot multiple paths on a given axes.
    
    Args:
        ax: Matplotlib axes object
        paths: Array of shape (n_paths, n_steps) containing price paths
        model_name: Name of the model for the title
        dt: Time step size
        alpha: Transparency level for the paths
    """
    n_paths, n_steps = paths.shape
    time_steps = np.arange(n_steps) * dt * 252  # Convert to trading days
    
    # Plot all paths with transparency
    for i in range(n_paths):
        ax.plot(time_steps, paths[i], alpha=alpha, linewidth=0.8)
    
    # Calculate and plot mean path in bold
    mean_path = np.mean(paths, axis=0)
    ax.plot(time_steps, mean_path, 'k-', linewidth=2, label='Mean', alpha=0.8)
    
    ax.set_xlabel('Time (trading days)')
    ax.set_ylabel('Price')
    ax.set_title(f'{model_name} - {n_paths} Path Realizations')
    ax.grid(True, alpha=0.8)
    ax.legend(loc='best')

def main():
    # Configuration parameters
    k = 50  # Number of path realizations
    n_steps = 252  # Number of time steps (1 year of daily data)
    
    # Model parameters
    start_price = 100.0
    dt = 1/252  # Daily time step
    
    # GBM parameters
    gbm_drift = 0.05  # 5% annual drift
    gbm_volatility = 0.2  # 20% annual volatility
    
    # Jump-Diffusion parameters
    jd_drift = 0.05  # 5% annual drift
    jd_volatility = 0.15  # 15% annual volatility (lower than GBM since jumps add volatility)
    jump_intensity = 5.0  # Average 5 jumps per year
    jump_mean = -0.03  # Average jump size (log-normal mean)
    jump_std = 0.06  # Jump size standard deviation
    
    # Random seed for reproducibility (set to None for random results)
    seed = 42
    
    # Initialize models
    gbm_model = GeometricBrownianMotion(
        start_price=start_price,
        dt=dt,
        drift=gbm_drift,
        volatility=gbm_volatility
    )
    
    jd_model = JumpDiffusion(
        start_price=start_price,
        dt=dt,
        drift=jd_drift,
        volatility=jd_volatility,
        jump_intensity=jump_intensity,
        jump_mean=jump_mean,
        jump_std=jump_std
    )
    
    # Generate paths
    print("\nGenerating paths...")
    gbm_paths = generate_paths(gbm_model, n_steps, k, seed=seed)
    jd_paths = generate_paths(jd_model, n_steps, k, seed=seed if seed else None)
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot GBM paths
    plot_model_paths(ax1, gbm_paths, "Geometric Brownian Motion", dt, alpha=0.5)
    
    # Plot Jump-Diffusion paths
    plot_model_paths(ax2, jd_paths, "Jump-Diffusion", dt, alpha=0.5)
    
    # Add overall title
    fig.suptitle('Comparison of Time Series Models', fontsize=16)
    
    # Adjust layout
    plt.tight_layout()
    
    # Display the plot
    plt.show()

    # Optional: Save the figure
    # plt.savefig('asset_price_path_visualization.png', dpi=150, bbox_inches='tight')

if __name__ == "__main__":
    main()
```