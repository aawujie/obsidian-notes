# AlphaGen 项目详细拆解

## 一、项目概览

AlphaGen 是一个**用强化学习（RL）自动挖掘量化因子**的框架。核心思路是：

- 将因子公式的构造建模为**序列生成问题**
- RL Agent 逐 token 输出因子表达式（后缀表示法）
- 生成的因子被送入**因子池（Alpha Pool）**进行线性加权组合
- 池的组合 IC 作为 reward 反馈给 Agent
- 可选地引入 LLM 与 RL 协作，周期性优化池中的因子

---

## 二、运行流程总览

```
scripts/rl.py  (入口)
  │
  ├─ 1. 数据准备
  │     ├─ 加载 Qlib 数据（csi300）
  │     ├─ 划分 4 段时间区间（1训练 + 3测试）
  │     └─ 构建 QLibStockDataCalculator（计算因子 IC）
  │
  ├─ 2. 初始化因子池
  │     ├─ 纯 RL：空池
  │     ├─ AlphaGPT Init：LLM 预生成因子填充
  │     └─ RL+LLM 协作：LLM 先生成初始池
  │
  ├─ 3. 构建 RL 环境
  │     ├─ AlphaEnvCore：核心逻辑（token→表达式→评估）
  │     └─ AlphaEnvWrapper：int↔Token 映射 + 动作掩码
  │
  ├─ 4. 训练
  │     ├─ MaskablePPO + LSTM 特征提取器
  │     └─ CustomCallback：日志、checkpoint、LLM 协作
  │
  └─ 5. 每个 rollout 结束
        ├─ 测试集评估（IC、Rank IC）
        ├─ 保存模型 + 池状态
        └─ 可选：调用 LLM 替换弱因子
```

---

## 三、动作空间详解

### 3.1 总体布局

RL Agent 的输出是一个离散整数，按区间映射到不同类型的 Token：

| 整数范围    | 类别       | 数量 | 映射方式                       |
| ----------- | ---------- | ---- | ------------------------------ |
| **0 ~ 19**  | Operator   | 20   | `OPERATORS[action]`            |
| **20 ~ 25** | Feature    | 6    | `FeatureType(action - 20)`     |
| **26 ~ 39** | Constant   | 14   | `CONSTANTS[action - 26]`       |
| **40 ~ 44** | DeltaTime  | 5    | `DELTA_TIMES[action - 40]`     |
| _(动态)_    | SubExpr    | 可选 | 外部传入的子表达式             |
| **45**      | SEP        | 1    | 结束符，触发评估               |

### 3.2 Operators（20 个，`config.py`）

实际训练使用的操作符，从 `expression.py` 的全集（27 个）中筛选：

```python
OPERATORS = [
    # 一元 (2个)
    Abs, Log,
    # 二元 (6个)
    Add, Sub, Mul, Div, Greater, Less,
    # 滚动 (10个)
    Ref, Mean, Sum, Std, Var, Max, Min, Med, Mad, Delta, WMA, EMA,
    # 双序列滚动 (2个)
    Cov, Corr
]
```

**被排除的 7 个**：`Sign`（信息量少）、`CSRank`（开销大）、`Pow`（数值爆炸）、`Skew/Kurt`（高阶矩不稳定）、`Rank`（与 CSRank 冗余）。

### 3.3 Features（6 个）

| 索引 | Token     | 含义           |
| ---- | --------- | -------------- |
| 0    | `$open`   | 开盘价         |
| 1    | `$close`  | 收盘价         |
| 2    | `$high`   | 最高价         |
| 3    | `$low`    | 最低价         |
| 4    | `$volume` | 成交量         |
| 5    | `$vwap`   | 成交量加权均价 |

### 3.4 Constants（14 个）

```python
[-30., -10., -5., -2., -1., -0.5, -0.01, 0.01, 0.5, 1., 2., 5., 10., 30.]
```

### 3.5 DeltaTimes（5 个）

```python
[1, 5, 10, 20, 40]  # 单位：交易日（约 1天、1周、2周、1月、2月）
```

---

## 四、Token 到表达式的三层映射

### 第 1 层：整数 → Token 对象（`AlphaEnvWrapper.action_to_token`）

分段减去偏移量定位类别，例如 `action=21`：
- `21 >= 20`（不是 Op）→ 减 20 → `action=1`
- `1 < 6`（是 Feature）→ `FeatureToken(FeatureType(1))` = `$close`

### 第 2 层：Token → 表达式树节点（`ExpressionBuilder.add_token`）

使用**后缀（逆波兰）表示法**，维护一个栈：

| Token 类型      | 行为                             |
| --------------- | -------------------------------- |
| `FeatureToken`  | 压入 `Feature(CLOSE)` 等         |
| `ConstantToken` | 压入 `Constant(1.0)` 等          |
| `DeltaTimeToken`| 压入 `DeltaTime(20)` 等          |
| `OperatorToken` | 弹出 n_args 个参数，构造节点压回 |
| `ExpressionToken`| 直接压入现成子树                |
| `SEP`           | 不入栈，触发 `_evaluate()`       |

### 第 3 层：表达式树 → 张量计算（`Expression.evaluate`）

每个节点递归计算，输出 `(days, stocks)` 的张量。

### 完整示例

构造因子 `Std($close, 20) / Mean($close, 20)`（变异系数）：

| 步骤 | 动作 | Token              | 栈状态                                       |
| ---- | ---- | ------------------ | -------------------------------------------- |
| 1    | 21   | `$close`           | `[$close]`                                   |
| 2    | 43   | `DeltaTime(20)`    | `[$close, 20]`                               |
| 3    | 11   | `Std`              | `[Std($close,20)]`                           |
| 4    | 21   | `$close`           | `[Std($close,20), $close]`                   |
| 5    | 43   | `DeltaTime(20)`    | `[Std($close,20), $close, 20]`               |
| 6    | 9    | `Mean`             | `[Std($close,20), Mean($close,20)]`          |
| 7    | 5    | `Div`              | `[Div(Std($close,20), Mean($close,20))]`     |
| 8    | 45   | `SEP`              | → 取出树 → `pool.try_new_expr()` → reward    |

---

## 五、RL 环境（`alphagen/rl/env/`）

### 5.1 `AlphaEnvCore`（Gymnasium 环境）

- **State**：已生成的 token 序列
- **Action**：Token 对象
- **Reward**：只有 episode 结束时才有，为池的目标函数值
- **Done**：输出 SEP / 达到最大长度（`MAX_EXPR_LENGTH=15`）

`step` 方法的三种情况：

| 情况       | 条件                | 处理                         |
| ---------- | ------------------- | ---------------------------- |
| 主动结束   | Agent 输出 SEP      | 评估表达式 → reward          |
| 继续生成   | token 数 < 15       | append token，reward = 0     |
| 强制截断   | 达到最大长度        | 合法则评估，否则 reward = -1 |

### 5.2 动作合法性掩码

`_valid_action_types()` 根据 `ExpressionBuilder` 的栈状态判断哪些 token 类型合法：
- 栈中只有 1 个元素 → 不允许二元操作符
- 栈顶不是 `DeltaTime` → 不允许滚动操作符
- 栈中恰好一个合法表达式 → 允许 SEP

`AlphaEnvWrapper.action_masks()` 将类型级掩码展开为完整的 bool 数组，供 `MaskablePPO` 使用，**保证只采样语法合法的 token**。

### 5.3 `AlphaEnvWrapper`（Wrapper 层）

- 将 Token 对象接口转为离散整数接口
- observation：`(MAX_EXPR_LENGTH,)` 的 uint8 数组，记录已输出的 action 整数
- `action_masks()`：返回 bool 掩码数组

---

## 六、因子池（`alphagen/models/linear_alpha_pool.py`）

### 6.1 核心思想

维护一个固定容量的因子池，通过线性加权组合多个 alpha 因子，不断优化权重使组合 IC 最优。

### 6.2 数据结构

```python
self.exprs          # 因子表达式列表，长度 capacity+1
self.single_ics     # 每个因子与收益的 IC
self._weights       # 线性组合权重
self._mutual_ics    # 因子间互相关矩阵（对称，对角线为1）
self._failure_cache # 被拒绝的因子缓存，避免重复评估
```

> **所有数组分配 `capacity + 1` 的空间**——"先加后删"策略：临时多放一个因子进去，优化权重后再踢掉最差的。

### 6.3 核心流程：`try_new_expr`

```
新表达式进来
  │
  ├─ 计算 IC（单因子 IC + 与池中每个因子的互相关）
  │
  ├─ 前置过滤（三重）
  │   ├─ IC 为 NaN → 拒绝
  │   ├─ 与已有因子相关性 > 0.99 → 拒绝（冗余）
  │   └─ IC < ic_lower_bound → 拒绝
  │
  ├─ 临时加入池（size → size+1）
  │
  ├─ 优化权重（子类实现）
  │
  ├─ 容量管理
  │   ├─ 超容量 → 踢掉权重绝对值最小的因子
  │   └─ 新加的就是最差的 → 回滚，放入 failure_cache
  │
  └─ 返回组合目标函数值（作为 RL reward）
```

### 6.4 两种子类实现

#### `MseAlphaPool`：最小化 MSE

损失函数：$\text{loss} = w^T M w - 2 w^T r + 1 + \alpha \|w\|_1$

- 无 L1 正则化时：直接最小二乘 `np.linalg.lstsq` 解析求解
- 有 L1 正则化时：Adam 梯度下降 + early stopping

#### `MeanStdAlphaPool`：优化 ICIR / LCB

同时考虑 IC 的均值和标准差，两种目标可选：

- **ICIR**（`lcb_beta=None`）：$\text{ICIR} = \frac{\mu_{IC}}{\sigma_{IC}}$
- **LCB**（`lcb_beta=β`）：$\text{LCB} = \mu_{IC} - \beta \cdot \sigma_{IC}$

缓存每个因子的逐日逐股原始值，优化更精确但内存开销更大。

---

## 七、训练入口（`scripts/rl.py`）

### 7.1 数据划分

| 段   | 用途     | 时间范围                |
| ---- | -------- | ----------------------- |
| 段 1 | 训练集   | 2012-01-01 ~ 2021-12-31 |
| 段 2 | 测试集 1 | 2022-01-01 ~ 2022-06-30 |
| 段 3 | 测试集 2 | 2022-07-01 ~ 2022-12-31 |
| 段 4 | 测试集 3 | 2023-01-01 ~ 2023-06-30 |

预测目标：未来 20 天收益率 `Ref($close, -20) / $close - 1`

### 7.2 三种初始化模式

| 模式           | 参数                  | 行为                                   |
| -------------- | --------------------- | -------------------------------------- |
| 纯 RL          | 默认                  | 空池，完全靠 RL 探索                   |
| AlphaGPT Init  | `alphagpt_init=True`  | LLM 预生成因子初始化池，之后纯 RL      |
| RL + LLM 协作  | `use_llm=True`        | LLM 生成初始池，训练中周期调用 LLM 优化 |

### 7.3 模型配置

```python
MaskablePPO(
    policy="MlpPolicy",
    features_extractor=LSTMSharedNet(n_layers=2, d_model=128, dropout=0.1),
    gamma=1.,        # 不折扣（只有 episode 结束有 reward）
    ent_coef=0.01,   # 适度探索
    batch_size=128
)
```

### 7.4 `CustomCallback`：训练回调

每个 rollout 结束时：
1. 记录池状态日志（size、权重显著因子数、best IC、评估次数）
2. 在 3 个测试集上评估组合 IC 和 Rank IC
3. 保存模型 checkpoint + 池 JSON
4. **LLM 协作**（可选）：每隔 N 步踢掉 `drop_rl_n` 个最弱 RL 因子，让 LLM 生成新因子填充

---

## 八、关键设计思想

| 维度           | 设计                                                    |
| -------------- | ------------------------------------------------------- |
| 表达式表示     | 后缀（逆波兰）序列，天然避免括号问题                    |
| 动作合法性     | `MaskablePPO` + 结构化掩码，100% 保证语法合法            |
| 因子池策略     | "先加后删"，容量 +1 的缓冲区设计                        |
| 三重过滤       | IC 下界 + 互相关阈值 + failure cache                    |
| 权重优化       | MSE 方式（快）或 ICIR/LCB 方式（稳）                    |
| RL + LLM 协作  | RL 负责精细搜索，LLM 负责跳出局部最优                    |
| 模块化         | `config.py` 控制动作空间，不动底层即可调整               |
