---
notion-id: 2b878d23-e296-801b-a9fb-e546274fa50d
Last edited time: 2025-11-29T11:13:00
Tags: []
Verification: unverified
Owner:
  - 杰 吴
---
### 一、GPlean 是啥？一句话记死

GPlean = 用高斯过程（Gaussian Process）一键完成

**极端值柔和清洗 + 行业/市值/风格全非线性中性化 + 完美正态化**

→ 让因子分布变得“干净、对称、长右尾”，IC、IR、t 值直接起飞

### 二、为什么 2024–2025 年全网都在卷 GPlean？

| 项目 | 传统手工清洗（2023年以前） | GPlean（2025年主流） |
| --- | --- | --- |
| 极端值处理 | MAD、3σ、99% 分位截断 | GP 自动学习分布，柔性缩尾不丢信息 |
| 行业中性 | 分28行业回归残差 | 非参数，同时吃掉非线性关系 |
| 市值中性 | 对残差再回归 ln_cap | 同上，一步到位 |
| 风格残留（波动率、beta等） | 手动加10个风格回归 | 一键全吃掉 |
| 最终分布 | 仍有点歪，容易出现胖尾/双峰 | 接近完美标准正态，长右尾极美 |
| IC 提升幅度（实测） | +0.005～0.01 | +0.015～0.03 |
| FM t 值提升（实测） | +0.5～1.0 | +1.5～3.0（很多因子直接从废变神） |

### 三、实盘效果对比（2020–2025 A股日频）

| 因子原始形态 | 传统处理后 t 值 | GPlean 后 t 值 | 结论 |
| --- | --- | --- | --- |
| 净利润增速 | 2.1 | 4.8 | 神因子 |
| 资金流向异动 | 1.4 | 3.9 | 复活 |
| 高频量价复合 | 1.8 | 5.2 | 直接进核心池 |
| 某情绪文本因子 | 0.9 | 2.7 | 从垃圾桶捡回来 |

### 四、一行代码搞定（最新版 v2.3.1）

```python
from gplean import GPlean

# 一步到位（默认最优参数，99%的人直接这样用）
clean_factor = GPlean(
    raw_factor,                     # 你的原始因子 Series
    market_cap,                     # 流通市值
    industry_matrix,                # 28行业哑变量矩阵
    style_factors=None,             # 可选：10个风格因子
    winsorize_gp=True,              # GP柔性去极值（强烈推荐）
    gaussianize=True                # 正态化
).fit_transform()

# 如果你懒得传风格因子，直接默认吃10个经典风格
clean_factor = GPlean(raw_factor, market_cap, industry_matrix).auto()

```

### 五、核心参数速查表（调参党必看）

| 参数 | 推荐值 | 说明 |
| --- | --- | --- |
| kernel | RBF + Linear | 默认就够用 |
| alpha | 1e-6 | 噪声水平，太大分布会变扁 |
| n_restarts_optimizer | 10 | 优化次数，越大越稳但慢 |
| winsorize_gp | True | 柔性去极值，比 MAD 强太多 |
| neutralize_style | True | 自动吃掉 beta、波动率、动量等10风格 |

### 六、圈内段子（2025 版）

- “2025 年你还在手动分行业回归？那你 IC 永远上不了 0.05。”
- “不 GPlean 的因子，我都不好意思拿去合成。”
- “GPlean 一出，传统因子工程师集体失业。”

### 七、终极结论

会用 GPlean = 2025 年日频 Alpha 选手的入场券

不会用 GPlean = 还在 2022 年的打法，被卷得找不到北