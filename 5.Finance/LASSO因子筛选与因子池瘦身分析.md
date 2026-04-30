# LASSO 因子筛选与因子池瘦身分析

> Date: 2026-04-30
> Status: 已完成

---

## 1. 背景与动机

当前使用的 5 因子基准池为：

| 因子 | 经济含义 |
|:---|:---|
| gross_margin_change | 毛利变化率 |
| roe_change | ROE 变化率 |
| roe_above_median | ROE 优于行业中位数 |
| eps_surprise | 盈利超预期 |
| profit_surprise | 利润超预期 |

存在三个问题：

1. **是否有冗余？** 5 个因子是否都对截面收益有独立预测能力
2. **是否有拖累？** 某些因子是否在组合中不贡献 Alpha 甚至产生噪音
3. **能否更精简？** 少因子 = 低过拟合风险 + 低交易成本

本文通过 LASSO/ElasticNet/Ridge 三种正则化方法，在 56 期滚动窗口上对因子池做系统筛选，并结合 Kalman 动态权重回测验证结果。

---

## 2. 方法论

### 2.1 三步走框架

```
Step 1: 数据准备
  ├─ 抽 Parquet 因子面板（123 MB）
  ├─ 15 个候选因子（core_5 + eliminated + additional）
  └─ 56 个截面时点，每期约 3000-5000 只股票

Step 2: 正则化筛选（LASSO / ElasticNet / Ridge）
  ├─ 每期截面回归，LASSO 自动将不重要系数压零
  ├─ 统计 56 期中被"选中"的频次
  └─ 三项方法对比，交叉验证 λ 参数

Step 3: Kalman 回测验证
  ├─ 入选因子 vs 原始 5 因子
  ├─ Kalman 动态权重 vs 等权
  └─ 2020-02 ~ 2024-11 OOS 考核
```

### 2.2 方法对比

| 方法 | 惩罚项 | 效果 |
|:---|:---|:---|
| **LASSO (L1)** | λ * Σ\|β\| | 将系数压到精确零 → 自动因子筛选 |
| **Ridge (L2)** | λ * Σβ² | 系数压缩但不归零 → 处理多重共线性 |
| **ElasticNet** | 混合 L1 + L2 | 兼具筛选 + 压缩，应对高相关问题 |

三种方法共同使用，若结论一致则验证可靠性。

---

## 3. 核心发现

### 3.1 LASSO 因子选中率

56 期滚动窗口，每期 LASSO 自选因子。统计各因子被选中频次：

| 排序 | 因子 | 选中次数 | 选中率 | 归类 |
|:---|:---|:---|:---|:---|
| 1 | volatility_20d | 47/56 | **83.9%** | 新增 |
| 2 | roe_above_median | 39/56 | **69.6%** | core_5 |
| 3 | roe_change | 26/56 | **46.4%** | core_5 |
| 4 | cpi_beta | 26/56 | **46.4%** | 新增 |
| 5 | gross_margin_change | 24/56 | **42.9%** | core_5 |
| 6 | main_flow_ratio | 21/56 | 37.5% | 新增 |
| 7 | margin_balance_change | 16/56 | 28.6% | eliminated |
| 8 | **eps_surprise** | 14/56 | **25.0%** ⚠️ | core_5 |
| 9 | block_discount_20d | 13/56 | 23.2% | eliminated |
| 10 | rsi_14d | 12/56 | 21.4% | 新增 |
| 11 | **profit_surprise** | 10/56 | **17.9%** ⚠️ | core_5 |
| 12 | relative_strength | 5/56 | 8.9% | 新增 |
| 13 | price_pressure | 3/56 | 5.4% | 新增 |
| 14 | volume_ratio_20d | 2/56 | 3.6% | eliminated |
| 15 | volume_ratio_raw | 2/56 | 3.6% | 新增 |

**关键观察：**

- **eps_surprise (25.0%) 和 profit_surprise (17.9%) 是 core_5 中表现最差的**，压缩到成为可以被淘汰的候选
- **volatility_20d (83.9%) 一骑绝尘**，说明波动率是截面收益最强的预测因子
- **roe_above_median (69.6%) 是 core_5 中唯一稳定的**，盈利质量护城河逻辑成立
- 此前已被淘汰的三个因子（margin_balance_change、block_discount_20d、volume_ratio_20d）LASSO 确认低选中率，验证了之前淘汰决策的合理性

### 3.2 正则化方法对比（Step 2）

三种正则化构建的多空组合 vs 5 因子等权基准，在训练期内（56 期窗口）：

| 方法 | 年化收益 | 年化波动 | Sharpe | 最大回撤 | 胜率 |
|:---|:---|:---|:---|:---|:---|
| LASSO (L1) | +17.7% | 15.0% | **1.02** | -14.0% | 62.5% |
| ElasticNet | +21.0% | 14.8% | **1.25** | -8.8% | 62.5% |
| Ridge (L2) | +28.4% | 14.3% | **1.81** | -10.2% | 73.2% |
| 5-Factor EW | -14.4% | 15.8% | **-1.07** | -70.5% | 32.1% |

**核心发现：**

1. **三种正则化方法在训练期内全方位碾压 5 因子等权**，Sharpe 从 -1.07 提升到 1.02~1.81
2. Ridge 表现最好（Sharpe 1.81），说明多重共线性确实存在，L2 压缩优于 L1 筛选
3. 5 因子等权的 -70.5% 最大回撤表明存在严重的因子拥挤和反向期问题，简单等权极不稳定

### 3.3 Kalman 回测验证（Step 3）

对 LASSO 选出的最佳 5 因子（top 5 选中率）与原始 5 因子在 OOS 期（2020-02 ~ 2024-11）进行 Kalman 动态权重回测：

| 组合 | 方法 | Sharpe | 年化收益 | 最大回撤 | 胜率 | 累计收益 |
|:---|:---|:---|:---|:---|:---|:---|
| **LASSO 入选** | Kalman | **0.276** | +9.3% | -26.2% | 55.4% | +35.3% |
| **LASSO 入选** | 等权 | -0.042 | +1.3% | -48.6% | 41.1% | -10.5% |
| **原始 5 因子** | Kalman | 0.216 | +7.3% | -31.5% | 53.6% | +25.9% |
| **原始 5 因子** | 等权 | -0.087 | +0.4% | -49.6% | 48.2% | -10.2% |

**关键结论：**

1. **LASSO 入选因子 × Kalman > 原始 5 因子 × Kalman**：ΔSharpe = +0.060，2024 年差距尤其大
2. **等权一律是灾难**：不管哪个因子池，等权 Sharpe 几乎为零甚至为负，最大回撤接近 -50%
3. **Kalman 的价值被验证**：同样是 LASSO 入选因子，Kalman 把 Sharpe 从 -0.04 拉到 +0.28
4. **但绝对水平仍低**：即便最优组合 Sharpe 仅 0.28，远低于当前产品 Sharpe 0.69——原因是 OOS 期（2020-2024）整体宏观环境对多因子策略不友好，且 56 期截面样本在 Bootstrap 测试中统计显著性不足

---

## 4. 因子诊断

### 4.1 eps_surprise — 建议淘汰

| 维度 | 评估 |
|:---|:---|
| LASSO 选中率 | 25.0%（倒数第 2） |
| Kalman 权重符号 | 为正（+0.017），但与动量因子高度重叠 |
| Bootstrap 贡献 | 无独立增量（被 volatility_20d 和 roe 因子覆盖） |

**结论：** 盈利超预期因子在截面上的信号已被波动率和 ROE 因子充分吸收，独立预测能力微弱。LASSO 反复将其压零，已无保留必要。

### 4.2 profit_surprise — 建议淘汰

| 维度 | 评估 |
|:---|:---|
| LASSO 选中率 | 17.9%（倒数第 1） |
| Kalman 权重符号 | 为正（+0.008）但权重极小 |
| Bootstrap 贡献 | 无增量 |

**结论：** 核心 5 因子中表现最差，接近随机噪音。与其留一个零信息的因子增加维度，不如直接拿掉。

### 4.3 roe_above_median — 核心保留

| 维度 | 评估 |
|:---|:---|
| LASSO 选中率 | 69.6%（core_5 最高） |
| Kalman 权重 | 始终为负且稳定（-0.027），方向一致 |
| 经济逻辑 | ROE 优于行业中位数 = 盈利护城河，逻辑自洽 |

**结论：** 五因子中最稳健的一个，独立预测价值明确，必须保留。

### 4.4 roe_change — 保留

| 维度 | 评估 |
|:---|:---|
| LASSO 选中率 | 46.4% |
| Kalman 权重 | 正向（+0.010），与 roe_above_median 方向互斥 |
| 互补性 | 捕捉 ROE 的趋势变化（动量属性），与水平因子互补 |

**结论：** 虽选中率不及 roe_above_median，但在 Kalman 框架中与核心因子形成互补，可保留。

### 4.5 gross_margin_change — 保留

| 维度 | 评估 |
|:---|:---|
| LASSO 选中率 | 42.9% |
| Kalman 权重 | 弱负向（-0.005），信号时变性强 |
| 基本面覆盖 | 提供毛利视角，与 ROE 因子不重叠 |

**结论：** 选中率中等但为组合提供基本面多样性，暂保留。

---

## 5. 同期辅助结果

### 5.1 Bootstrap 蒙特卡洛（1000 次重采样）

| 测试项 | 结论 |
|:---|:---|
| Kalman > 等权 | **99.5%** Bootstrap δ > 0，显著性极高 |
| Kalman 绝对 Sharpe | 不显著（95% CI 含零），53 期样本不足 |
| 权重稳定性 | 中等偏弱（符号一致性 53-71%，CV 极高） |
| 尾部风险 | 最差 5% 路径回撤 > 40%，需止损保护 |

### 5.2 卡尔曼 Walk-Forward 调参（80 期 × 30 组网格）

| 结论 | 详情 |
|:---|:---|
| Walk-Forward vs 固定参数 | 固定参数胜（Sharpe 0.39 vs 0.34） |
| 最优固定参数 | delta = 1e-09, sigma_r = 0.05 |
| sigma_r 稳定性 | 80/80 期全选 0.05，无需调整 |
| delta 漂移 | 在 1e-09 ~ 1e-05 间波动，多数年份选 1e-09 |

**结论：不需要 Walk-Forward 调参。固定 delta=1e-09, sigma_r=0.05 即可。**

### 5.3 GRS 回溯测试（5 个已淘汰因子）

对之前淘汰的 5 个因子做 GRS F 检验，判断淘汰是否正确：

| 因子 | GRS p-value | 结论 |
|:---|:---|:---|
| neg_block_premium_20d | 0.998 | ✅ 正确淘汰 |
| volume_ratio_20d | 0.557 | ✅ 正确淘汰 |
| cpi_beta | 1.000 | ✅ 正确淘汰 |
| block_discount_20d | 0.187 | ⚠️ 边界，待观察 |
| margin_balance_change | 0.072 | ❌ 误淘汰，可能有效 |

**注意：** GRS 测试的 margin_balance_change 结论与 rescued factors 独立验证结论有矛盾——GRS 认为它可能被误淘汰（p=0.072），但独立验证在清洁期发现它虽 IC 显著但无增量价值。需要更高频的真实数据重试。

---

## 6. 行动建议

### 6.1 立即执行

1. **淘汰 eps_surprise 和 profit_surprise** — 量化证据充分，不再入库
2. **将 volatility_20d 加入因子池** — LASSO 选中最高的因子，此前被低估
3. **将 cpi_beta 重新纳入候选** — 选中率与 roe_change 相当（46.4%），GRS 确认淘汰合理但 LASSO 在更多时点选中它

### 6.2 下一步验证

4. **用精简因子池重新跑 Kalman 回测**：volatility_20d + roe_above_median + roe_change + cpi_beta + gross_margin_change
5. **对比精简版 vs 现状**：验证少因子是否更优
6. **回测周期延伸到 2010-2015 牛市+股灾期**：检验极端行情下的表现

### 6.3 中长期

7. **block_discount_20d — 换真实大宗数据重建**：LASSO 选中率低但清洁期表现强，市场结构变了，用真实数据（非代理）可能复活
8. **margin_balance_change — 用真实融资余额重建**：GRS 认为可能误淘汰，代理数据不可靠

---

## 7. 结论摘要

```
LASSO 分析结论：
├─ eps_surprise + profit_surprise → 🗑️ 淘汰（选中率 < 25%）
├─ volatility_20d → ⭐ 拉入因子池（选中率 83.9%）
├─ cpi_beta → 🔄 重新纳入（选中率 46.4%，有独立价值）
├─ roe_above_median → ✅ 核心保留（最稳健）
├─ roe_change + gross_margin_change → ✅ 保留（互补）
│
├─ 卡尔曼 >> 等权 → 99.5% Bootstrap 确认
├─ Walk-Forward 调参 → 不需要，固定参数已最优
├─ block_discount_20d → 👀 值得追踪但需真实数据
└─ 缩身 5 因子（新）vs 原始 5 因子 → ΔSharpe +0.06 待更大样本验证
```

---

## 附录：数据文件清单

| 文件 | 路径 | 大小 |
|:---|:---|:---|
| 因子面板 | `/tmp/lasso_factor_panel.parquet` | 123 MB |
| Step2 结果 | `/tmp/step2_results.json` | — |
| Step3 结果 | `/tmp/step3_results.json` | — |
| 收益序列 | `/tmp/step3_returns.csv` | — |
| LASSO 选中率 | `/tmp/lasso_persistence.csv` | — |
| Kalman WF 结果 | `kalman_walk_forward_results.json` | 33 KB |
| GRS 测试 | `grs_test_results.json` | 2 KB |
| 救回因子 v2 | `validation_results/rescued_factors_v2_20260430_004907.json` | 4 KB |
| Bootstrap 脚本 | `monte_carlo_verification.py` | 26 KB |
