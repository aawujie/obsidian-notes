# panda_factor 因子库完整分析 & 下一步规划

> 分析日期：2026-05-03  
> 代码分支：feature/unify-quant-factor  
> 分析范围：架构、25个因子、23个研究脚本、30+验证结果文件

---

## 1. 代码架构全景

### 1.1 Monorepo 结构

```
panda_factor/                         # Git 仓库根
├── panda_common/                     # 公共层：config, MongoDB, 日志, Pydantic模型
├── panda_data/                       # 数据层：MongoDB行情读取
├── panda_data_hub/                   # 数据源适配：Tushare/TQ/XT
├── panda_factor/panda_factor/        # ★ 核心因子引擎 (14个子包)
│   ├── generate/                     # Factor基类 + DSL算子 (RANK/RETURNS/STDDEV等9个)
│   ├── factors/                      # [NEW] 25个经典因子子类库
│   ├── analysis/                     # IC分析 + 分组回测workflow
│   ├── backtest/                     # [NEW] 真实约束回测引擎
│   ├── signal/                       # [NEW] 因子合成 + 组合构建
│   ├── risk/                         # [NEW] 风控管理器
│   ├── mining/                       # [NEW] ML因子发现 (XGBoost/Kalman)
│   ├── pipeline/                     # [NEW] YAML Pipeline编排器
│   ├── strategy/                     # [NEW] 策略框架
│   ├── evaluation/                   # [NEW] 鲁棒性评估 (Monte Carlo等)
│   ├── regime/                       # [NEW] 市场状态分类 (HMM/DualGrid)
│   ├── data/                         # 数据适配器
│   ├── models/                       # 因子模型定义
│   └── utils/                        # 工具函数
├── panda_factor_server/              # FastAPI后端
├── panda_web/                        # Vue前端
├── panda_llm/                        # LLM辅助因子生成
├── examples/                         # 23个研究脚本
└── docs/                             # ARCHITECTURE.md + RESEARCH_ROADMAP.md
```

### 1.2 架构设计原则

| 原则 | 说明 |
|------|------|
| 纯增量 | 新模块以子目录添加，不修改原有模块接口 |
| 数据源无关 | 新模块接受 DataFrame/Series，不绑定特定数据源 |
| 可选依赖 | ML依赖通过 extras_require 管理（mining/deep） |
| Factor 子类化 | 所有因子继承 Factor 基类，复用 DSL 算子 |
| 注册表模式 | FACTOR_REGISTRY 统一管理因子名→类映射 |

### 1.3 DSL 算子能力

Factor 基类提供 9 个 DSL 算子：
`RANK`, `RETURNS`, `STDDEV`, `CORRELATION`, `IF`, `DELAY`, `SUM`, `MEAN`, `EMA`

均基于 (date, symbol) MultiIndex Series，自动处理截面/时序操作。

---

## 2. 已有因子全量分析

### 2.1 因子列表（共25个，按类别）

#### 动量类 (Momentum) — 4个
| # | 因子名 | 描述 | 窗口 |
|---|--------|------|------|
| 1 | momentum_20d | 20日价格动量 | 20d |
| 2 | momentum_60d | 60日价格动量 | 60d |
| 3 | momentum_120d | 半年价格动量 | 120d |
| 4 | momentum_250d | 年度价格动量 | 250d |

#### 反转类 (Reversal) — 2个
| # | 因子名 | 描述 |
|---|--------|------|
| 5 | reversal_5d | 5日反转（短期反转效应） |
| 6 | reversal_10d | 10日反转（中期反转效应） |

#### 波动率类 (Volatility) — 3个
| # | 因子名 | 描述 |
|---|--------|------|
| 7 | volatility_20d | 20日收益率标准差 |
| 8 | volatility_60d | 60日收益率标准差 |
| 9 | idio_volatility | 20日特质波动率（个股-市场） |

#### 流动性类 (Liquidity) — 3个
| # | 因子名 | 描述 |
|---|--------|------|
| 10 | turnover_rate | 20日平均成交量（换手率代理） |
| 11 | volume_ratio | 量比：当日量/20日均量 |
| 12 | amihud_illiq | Amihud非流动性：\|收益\|/成交量 |

#### 量价关系 (Volume-Price) — 3个
| # | 因子名 | 描述 |
|---|--------|------|
| 13 | vol_price_corr | 20日收盘价与成交量相关系数 |
| 14 | vol_return_corr | 20日成交量与收益率相关系数 |
| 15 | price_pressure | 收盘价偏离日内均价程度 |

#### 技术指标 (Technical) — 3个
| # | 因子名 | 描述 |
|---|--------|------|
| 16 | rsi | 14日相对强弱指标 |
| 17 | macd_signal | MACD信号线（12/26/9） |
| 18 | bollinger_pos | 布林带相对位置（20d, 2σ） |

#### 相对强弱 (Relative Strength) — 2个
| # | 因子名 | 描述 |
|---|--------|------|
| 19 | rel_strength | 相对强度指数（个股-市场20日均值） |
| 20 | beta | 60日滚动Beta（个股对市场敏感度） |

#### 组合因子 (Composite) — 3个
| # | 因子名 | 描述 |
|---|--------|------|
| 21 | mom_vol_combo | 动量-波动组合：高动量+低波动 |
| 22 | quality_momentum | 质量-动量：相对强度+低波动 |
| 23 | multi_factor | 多因子综合：动量40%+反转30%+流动性30% |

#### 宏观与资金流 (Macro) — 2个
| # | 因子名 | 描述 |
|---|--------|------|
| 24 | cpi_beta | CPI Beta：个股对通胀敏感度（24月滚动） |
| 25 | main_flow_ratio | 主力资金流向比：量价配合度 |

### 2.2 因子 IC 表现矩阵（FM-Shanken 双检验）

> 基于 quant-factor 侧 756 期、10 组合的 FM-Shanken 检验

| 因子 | Rank IC | IC IR | IC t-stat | Shanken SE% | Shanken t | IC Pass | Shanken Pass |
|------|---------|-------|-----------|-------------|-----------|---------|--------------|
| volume_ratio | -0.122 | -1.166 | -32.1 | 0.196 | 18.30 | ✅ | ✅ |
| momentum_20d | -0.126 | -0.776 | -21.3 | 0.292 | 14.21 | ✅ | ✅ |
| rel_strength | -0.119 | -0.801 | -22.0 | 0.236 | 13.45 | ✅ | ✅ |
| volatility_20d | -0.104 | -0.894 | -24.6 | 0.195 | 15.30 | ✅ | ✅ |
| amplitude_20d* | -0.023 | -0.735 | -20.2 | 0.058 | 11.88 | ✅ | ✅ |
| rsi_14d | -0.074 | -0.548 | -15.1 | 0.195 | 10.25 | ✅ | ✅ |
| reversal_5d | 0.062 | 0.455 | 12.5 | 0.200 | -9.98 | ✅ | ✅ |
| price_pressure | -0.006 | -0.145 | -4.0 | 0.062 | 3.37 | ✅ | ✅ |
| beta_60d | 0.010 | 0.089 | 2.4 | 0.143 | -4.27 | ✅ | ✅ |
| vol_breakout* | -0.011 | -0.271 | -7.4 | 0.061 | 6.38 | ✅ | ✅ |
| vol_price_corr | -0.001 | -0.036 | -1.0 | 0.037 | 5.90 | ❌ | ✅ |
| cpi_beta | -0.0003 | -0.013 | -0.3 | 0.038 | 1.94 | ❌ | ❌ |

> *amplitude_20d, vol_breakout 是 quant-factor 的因子，未纳入 panda_factor 的 FACTOR_REGISTRY

**关键发现：**
- strongest IC: volume_ratio, momentum_20d, rel_strength, volatility_20d（|IC| > 0.10）
- vol_price_corr 在 FM-Shanken 中 IC 不显著，与 rescued factors 验证结论一致
- cpi_beta 在日频 IC 检验中不显著，但在月频策略中表现出色（T_half=77d，衰减最慢）

### 2.3 信息衰减分析

| 因子 | IC₀ | λ(day⁻¹) | T_half | 月频存活 |
|------|-----|-----------|--------|----------|
| reversal_5d | -0.085 | 0.60 | 1.2d | ❌ |
| reversal_10d | -0.062 | 0.28 | 2.5d | ❌ |
| momentum_20d | 0.045 | 0.15 | 4.6d | ❌ |
| volume_ratio | -0.038 | 0.32 | 2.2d | ❌ |
| momentum_60d | 0.058 | 0.058 | 12.0d | ⚠️ 边界 |
| volatility_20d | -0.072 | 0.035 | 19.8d | ⚠️ 边界 |
| turnover_rate | -0.065 | 0.028 | 24.8d | ✅ |
| momentum_250d | 0.052 | 0.012 | 57.8d | ✅ |
| cpi_beta | -0.095 | 0.009 | 77.0d | ✅ |

**核心结论：** 只有半衰期 ≥ 调仓周期的因子才能在策略中存活。这是因子筛选的前置硬规则。

---

## 3. 高级方法论验证结果

### 3.1 Kalman 动态权重（核心策略引擎）

**Factor Timing 对比（OOS 2020-01 ~ 2024-11，57期）：**

| 方法 | Sharpe | 年化收益 | 最大回撤 | Calmar |
|------|--------|---------|---------|--------|
| 等权基准 | -0.180 | -2.2% | -57.8% | -0.04 |
| **Kalman OLS** | **0.264** | **9.0%** | **-30.7%** | **0.29** |
| Kalman + Linear Pred | 0.165 | 6.6% | -34.4% | 0.19 |
| Kalman + LightGBM Pred | 0.185 | 7.1% | -34.8% | 0.20 |

**结论：Kalman-smoothed 历史 lambda > 预测 lambda。** 因子收益方向预测准确率仅 55-57%，相当于随机，预测带来的 tilt 反而引入噪声。

**Walk-Forward 参数稳定性（2018-05 ~ 2025-03，80期）：**
- 判定：FIXED WINS（固定参数优于动态参数选择）
- Fixed Sharpe: 0.387，Walk-Forward Sharpe: 0.343
- 最优参数极其稳定：delta=1e-09, sigma_r=0.05 在 50% 的滚动窗口中是最优的
- sigma_r 几乎不变（始终 0.05），delta 在 1e-09 ~ 1e-05 间漂移但不影响 core 表现

### 3.2 精简因子池策略（最新成果）

**5F Kalman + 情绪减仓（2017-02 ~ 2025-02，94期）：**

因子池：volatility_20d, roe_above_median, roe_change, cpi_beta, gross_margin_change

| 方法 | Sharpe | 年化收益 | 最大回撤 | Calmar |
|------|--------|---------|---------|--------|
| 等权 | -0.322 | -4.5% | -58.5% | -0.08 |
| **Kalman + Sentiment** | **0.500** | **14.4%** | **-44.9%** | **0.32** |
| Δ | +0.822 | +18.9% | +13.6% | +0.40 |

年度分解：
| 年份 | 收益 | Sharpe |
|------|------|--------|
| 2017 | -12.6% | -1.02 |
| 2018 | -27.8% | -1.00 |
| 2019 | +61.9% | +1.95 |
| 2020 | +39.5% | +1.83 |
| 2021 | +21.3% | +1.26 |
| 2022 | +13.0% | +0.54 |
| 2023 | -12.5% | -0.63 |
| 2024 | +28.5% | +0.96 |

**Bootstrap 稳健性：** 1000次 Bootstrap 95% CI 跨零 → 统计上不够稳健，需要更多数据或更强的 alpha 源。

### 3.3 Regime Rotation（市场状态自适应）

**6 Regime HMM 分类器（训练 2017-2019，测试 2020-2024）：**

6状态：Bear/Bull × LowVol/NormalVol/HighVol

| 方法 | Sharpe | 最大回撤 | 累积收益 |
|------|--------|---------|---------|
| EW Fixed (14因子) | -0.303 | -67.7% | -34.8% |
| Kalman Fixed (14因子) | -0.303 | -67.7% | -34.8% |
| Rotation Hard | -0.285 | -63.7% | -31.5% |
| **Rotation Kalman** | **0.034** | **-37.2%** | **+1.8%** |

**关键发现：**
- 14因子池表现差（太多噪声因子），因子质量 > 因子数量
- Regime Rotation 能大幅降低回撤（-67.7% → -37.2%），但 Sharpe 仍为负
- 因子在不同 regime 下的 IC 确实有显著分化（见下方映射表）

**各 Regime 最强因子（|IC| > 0.10）：**
| Regime | 最强因子 | Rank IC |
|--------|---------|---------|
| Bear_LowVol | block_discount_20d | +0.111 |
| Bear_LowVol | turnover_rate | +0.094 |
| Bear_NormalVol | volatility_20d | -0.140 |
| Bear_HighVol | roe_change | -0.142 |
| Bear_HighVol | gross_margin_change | -0.134 |
| Bear_HighVol | momentum_20d | -0.134 |
| Bull_NormalVol | volatility_20d | -0.113 |
| Bull_HighVol | momentum_20d | -0.106 |
| Bull_HighVol | momentum_60d | -0.101 |

### 3.4 GRS 增量因子检验

基准5因子 vs 5个候选因子，53期 OOS：

| 候选因子 | ΔSharpe | GRS p-value | 判定 |
|---------|---------|-------------|------|
| margin_balance_change | +0.88 | 0.072 | **MISCLASSIFIED — 应回纳** |
| block_discount_20d | +0.67 | 0.187 | BORDERLINE — 值得进一步调查 |
| volume_ratio_20d | +0.36 | 0.557 | 正确淘汰 |
| cpi_beta | +0.00 | 1.000 | 正确淘汰 |
| neg_block_premium_20d | +0.03 | 0.998 | 正确淘汰 |

### 3.5 其他方法论速览

| 方法 | 脚本 | 核心结论 |
|------|------|---------|
| Lasso/EN/Ridge 因子选择 | lasso_factor_selection.py | 15因子 walk-forward CV，正则化可自动筛选 |
| GARCH 动态杠杆 | garch_leverage.py | DCC-GARCH + HMM，杠杆范围[0.5, 3.0]，可降回撤 |
| 信息衰减模型 | decay_model.py | T_half ≥ T_rebalance 是存活必要条件 |
| Monte Carlo 验证 | monte_carlo_verification.py | 4步 bootstrap：收益/权重/最差情况/Kalman vs EW |
| 北上资金 IV 分析 | northbound_iv_analysis.py | Bartik IV 剥离因子收益中的内生性成分 |
| 投资者方差分解 | investor_variance_decomp.py | Shapley R² 分解因子收益到外资/机构/散户 |

---

## 4. 当前状态总结

### 4.1 优势
- 完整的工程化架构：从数据→因子→IC→回测→风控→策略→前端全链路
- 25个可生产的 Factor 子类，统一注册表，API 可调用
- Kalman 动态权重方法验证有效（vs 等权提升 0.8+ Sharpe）
- Regime/Evaluation/Mining 模块提供丰富的分析工具箱
- 23个研究脚本提供方法论弹药库

### 4.2 瓶颈
| 瓶颈 | 严重度 | 细节 |
|------|--------|------|
| **Alpha 不足** | 🔴 CRITICAL | 最优 Sharpe 0.50，距可实盘阈值(≥0.8)还有距离 |
| **因子同质化** | 🟠 HIGH | 现有因子主要是 OHLCV 变体，信息源单一 |
| **回撤过大** | 🟠 HIGH | -44.9% 对资管产品不可接受 |
| **基本面因子低频** | 🟡 MEDIUM | 季报驱动，信号更新慢 |
| **Bootstrap 不稳健** | 🟡 MEDIUM | 95% CI 跨零，统计显著性不足 |
| **因子择时效果弱** | 🟡 MEDIUM | 预测准确率仅 55-57% |

---

## 5. 下一步方向建议

### 🥇 P0 — Quick Wins（1-2周，Sharpe 0.50 → 0.60+）

#### 5.1 回纳 margin_balance_change（1天）
- GRS p=0.072，ΔSharpe=+0.88，是最明确的遗漏因子
- 加入 FACTOR_REGISTRY，将 5F Kalman 池扩至 6F
- 预期 Sharpe: 0.50 → 0.55+

#### 5.2 IC Decay 多期信号叠加（2-3天）
- 利用 decay_model.py 的发现：lag 3-5 仍有残余预测力
- 指数衰减权重 w = exp(-λ × lag) 或从 IC decay 经验权重
- 预期 IC IR 提升 15-25%

#### 5.3 日内微观结构因子（2-3天）
当前仅用 OHLCV 的 close，忽略了日内信息。MongoDB 已有完整数据：
- `overnight_gap`: 开盘/昨收 - 1（隔夜信息冲击）
- `close_strength`: 20日 (close-low)/(high-low) 均值（主力尾盘建仓）
- `intraday_reversal`: (open-low)/(high-low)（日内反转强度）
- `high_low_range`: 20日 high/low 均值（日内波幅）

预期：2-4个独立 alpha 源，各 IC 0.03-0.05

#### 5.4 风险预算组合（3天）
- 替代等权/IC加权，用 Risk Parity 让每个因子对组合风险贡献相等
- 降低对高波动因子的过度暴露
- 预期：回撤降低 20-30%

### 🥈 P1 — 体系提升（3-4周，Sharpe 0.60 → 0.70+）

#### 5.5 Regime 分类完善 + 因子映射（1周）
- 训练数据延长至 2010-2019，测试 2020-2024
- 加入成交量状态（萎缩/放量）
- 基于 factor_by_regime 映射表，每状态选 top-3 因子动态切换
- 仓位联动：Bull_LowVol=满仓，Bear_HighVol=空仓

#### 5.6 新增因子类型（1-2周）

**资金流因子：**
- 北向资金 5日动量（当前5d vs 前20d均值）
- 大单净流入占比 - 散户净流入占比（smart money indicator）
- 融资余额变化率（已有 margin_balance_change）

**波动率微观结构因子：**
- realized_vs_parkinson：已实现波动率 / Parkinson波动率 - 1
- upside_vol_ratio：上行波动率 / 总波动率（看涨情绪）
- vol_of_vol：波动率的波动率（稳定性）

**换手率派生因子：**
- turnover_decay_ratio: turnover_5d / turnover_20d
- abnormal_volume_zscore: 标准化异常成交量
- volume_price_divergence: 量价背离（rank(vol_change) - rank(price_change)）

#### 5.7 Paper Trading 系统搭建（3-5天）
- 每日收盘后自动计算因子 → 合成信号 → 输出 target_portfolio.csv
- 次日对比实际涨跌，记录模拟盈亏
- 验证信号在实际交易约束下的可行性

### 🥉 P2 — Alpha 突破（1-2月，Sharpe 0.70 → 0.80+）

#### 5.8 换手率约束优化（2天）
- 在目标函数中加入换手惩罚：max E[r] - λ×Var(r) - γ×|w_new - w_old|
- γ 反映实际交易成本（约 30bp 单边）

#### 5.9 LSTM Embedding 因子（2-3周）
- quant-factor 中初步验证 IR > 0.5（最强单因子之一），但未正式迁入
- 输入：过去60日 OHLCV + 20维技术特征
- 架构：2-layer LSTM → 128-dim embedding → rank 预测头
- 关键风险控制：rolling 3y train / 1y val / 1y OOS，防 look-ahead bias

#### 5.10 Transformer Attention 截面因子（3-4周）
- 将截面（所有股票某日）作为一个序列
- Self-attention 捕捉股票间关系
- 可解释性：attention 权重 → 行业轮动信号

### 🔮 P3 — 前沿探索（持续）

#### 5.11 新数据源接入
| 数据 | 来源 | 用途 |
|------|------|------|
| 资金流分级 | Tushare moneyflow | 主力/散户行为因子 |
| 大宗交易 | Tushare block_trade | 大股东增减持信号 |
| 北向资金个股 | Tushare hsgt_top10 | 外资 smart money 信号 |
| 分析师预期 | Tushare forecast | 预期修正因子 |
| 龙虎榜 | Tushare top_list | 游资行为模式 |
| 股东户数 | Tushare stk_holdernumber | 筹码集中度因子 |

#### 5.12 另类数据 Alpha
- 新闻情绪 NLP → 个股舆情因子
- 供应链关系图 → 产业链联动因子
- 搜索量/关注度 → 投资者注意力因子
- 期权隐含波动率 → 前瞻性波动率因子（如有期权数据）

#### 5.13 方法论扩展
- Bayesian 动态因子模型（替代 Kalman 的点估计）
- 强化学习组合优化（替代静态优化）
- 图神经网络行业轮动（替代传统截面回归）
- Causal Forest 异质性处理效应（识别因子在哪些股票上有效）

---

## 6. 优先级矩阵

```
                   低难度                    高难度
            ┌─────────────────────┬─────────────────────┐
 高收益     │ 5.1 回纳因子         │ 5.4 风险预算         │
            │ 5.2 IC Decay 叠加    │ 5.5 Regime 完善      │
            │ 5.3 日内微观结构因子  │ 5.9 LSTM Embedding   │
            ├─────────────────────┼─────────────────────┤
 中收益     │ 5.6 新增派生因子     │ 5.10 Transformer     │
            │ 5.7 Paper Trading   │ 5.13 方法论扩展       │
            ├─────────────────────┼─────────────────────┤
 长期布局   │ 5.8 换手约束        │ 5.11 新数据源         │
            │                     │ 5.12 另类数据         │
            └─────────────────────┴─────────────────────┘
```

---

## 7. 推荐执行路线图

### Phase 1：夯实基础（5月第1-2周）
```
5.1 回纳 margin_balance_change  ──── Sharpe 0.50 → 0.55
5.2 IC Decay 多期叠加           ──── IR +15-25%
5.3 日内微观结构因子 (4个)       ──── 新增 alpha 源
```
**目标：Sharpe 0.60+, 8-10因子池**

### Phase 2：体系优化（5月第3-4周）
```
5.4 风险预算组合                ──── 回撤 -45% → -30%
5.5 Regime 分类完善 + 因子映射   ──── 动态因子选择
5.6 新增派生因子 (6-8个)        ──── IC 0.03-0.06
5.7 Paper Trading 系统           ──── 实盘验证准备
```
**目标：Sharpe 0.70+, 最大回撤 < 30%**

### Phase 3：Alpha 突破（6月-7月）
```
5.8 换手约束优化                ──── 净 Sharpe 提升
5.9 LSTM Embedding 因子         ──── IR > 0.5 独立 alpha
5.11 新数据源接入               ──── 资金流/大宗交易/分析师预期
```
**目标：Sharpe 0.80+, 可实盘状态**

---

## 8. 关键成功指标

| 指标 | 当前基线 | Phase 1 | Phase 2 | Phase 3 | 可实盘阈值 |
|------|---------|---------|---------|---------|-----------|
| Sharpe | 0.50 | ≥0.60 | ≥0.70 | ≥0.80 | ≥0.80 |
| 年化收益 | 14.4% | ≥16% | ≥18% | ≥20% | ≥20% |
| 最大回撤 | -44.9% | ≤-35% | ≤-30% | ≤-20% | ≤-20% |
| Calmar | 0.32 | ≥0.45 | ≥0.60 | ≥1.0 | ≥1.0 |
| 因子数 | 5 | 8-10 | 12-15 | 15-20 | - |
| Bootstrap CI跨零 | 是 | 待改善 | 否 | 否 | 否 |

---

## 9. 附录：文件清单

### 因子定义文件
```
panda_factor/panda_factor/factors/
├── __init__.py          # FACTOR_REGISTRY (25因子)
├── momentum.py          # 4个动量因子
├── reversal.py          # 2个反转因子
├── volatility.py        # 3个波动率因子
├── liquidity.py         # 3个流动性因子
├── volume_price.py      # 3个量价关系因子
├── technical.py         # 3个技术指标因子
├── relative_strength.py # 2个相对强弱因子
├── composite.py         # 3个组合因子
└── macro.py             # 2个宏观因子
```

### 关键研究脚本
```
examples/
├── kalman_reduced_backtest.py      # 精简因子池 Kalman 回测（核心）
├── regime_rotation_backtest.py     # Regime 轮动回测
├── factor_timing.py                # 因子择时预测
├── kalman_walk_forward.py          # Kalman 参数稳定性
├── kalman_factor_optimization.py   # Kalman 因子优化
├── lasso_factor_selection.py       # Lasso 因子筛选
├── decay_model.py                  # 信息衰减建模
├── garch_leverage.py               # GARCH 动态杠杆
├── monte_carlo_verification.py     # Monte Carlo 鲁棒性
├── grs_test_retrospective.py       # GRS 增量检验
├── fm_shanken_validation.py        # FM-Shanken 双检验
├── northbound_iv_analysis.py       # 北上资金 IV 分析
├── investor_variance_decomp.py     # 投资者方差分解
└── validate_rescued_factors.py     # 被淘汰因子复审
```

### 关键结果文件
```
validation_results/
├── kalman_reduced_backtest_20260430_195225.json  # 精简池回测
├── regime_rotation_20260501_144222.json           # Regime 轮动
├── rescued_factors_v2_20260430_004907.json        # 因子复审
├── fm_shanken_20260429_175748.csv                 # FM-Shanken
factor_timing_results.json                          # 因子择时
grs_test_results.json                               # GRS 检验
kalman_walk_forward_results.json                    # Walk-Forward
strategy/strategy_summary_20260430_184813.json      # 产品化策略
```
