# Kronos：金融市场语言的基础模型

![[logo.png|100]]

> **项目地址**：[GitHub - shiyu-coder/Kronos](https://github.com/shiyu-coder/Kronos)
> **论文**：[arXiv:2508.02739](https://arxiv.org/abs/2508.02739)
> **实时演示**：[BTC/USDT 24h 预测](https://shiyu-coder.github.io/Kronos-demo/)
> **许可证**：MIT
> **状态**：已被 **AAAI 2026** 接收

---

## 1. 这是什么？

Kronos 是**首个面向金融K线图的开源基础模型**，基于全球超过 **45 家交易所**的数据训练而成。

与通用时间序列预测模型（TSFM）不同，Kronos **专门设计用于处理金融数据独特的高噪声特性**。它的核心思路是：把 K 线序列当作一种"语言"来理解。

---

## 2. 核心架构：两阶段框架

![[overview.png]]

```
K线数据 (OHLCV) → [专用分词器] → 分层离散令牌 → [自回归 Transformer] → 预测
```

1. **分词器（Tokenizer）**：将连续的多维K线数据（开盘、最高、最低、收盘、成交量）量化为**分层离散令牌**。
2. **Decoder-only Transformer**：基于这些令牌进行预训练，成为适用于多种量化任务的统一模型。

**关键设计**：不是直接拿价格数值做回归，而是先"翻译"成离散 token，再用语言模型的方式做自回归预测。

---

## 3. 模型库

| 模型 | 分词器 | 上下文长度 | 参数量 | 开源 |
| :--- | :--- | :--- | :--- | :--- |
| Kronos-mini | Kronos-Tokenizer-2k | 2048 | 4.1M | ✅ |
| Kronos-small | Kronos-Tokenizer-base | 512 | 24.7M | ✅ |
| Kronos-base | Kronos-Tokenizer-base | 512 | 102.3M | ✅ |
| Kronos-large | Kronos-Tokenizer-base | 512 | 499.2M | ❌ |

所有开源模型均可从 [Hugging Face Hub](https://huggingface.co/NeoQuasar) 获取。

---

## 4. 快速上手

### 环境

```bash
# Python 3.10+
pip install -r requirements.txt
```

### 预测代码（核心 4 步）

```python
from model import Kronos, KronosTokenizer, KronosPredictor
import pandas as pd

# 1. 加载模型
tokenizer = KronosTokenizer.from_pretrained("NeoQuasar/Kronos-Tokenizer-base")
model = Kronos.from_pretrained("NeoQuasar/Kronos-small")

# 2. 实例化预测器
predictor = KronosPredictor(model, tokenizer, max_context=512)

# 3. 准备数据
df = pd.read_csv("./data/XSHG_5min_600977.csv")
df['timestamps'] = pd.to_datetime(df['timestamps'])
lookback = 400
pred_len = 120
x_df = df.loc[:lookback-1, ['open', 'high', 'low', 'close', 'volume', 'amount']]
x_timestamp = df.loc[:lookback-1, 'timestamps']
y_timestamp = df.loc[lookback:lookback+pred_len-1, 'timestamps']

# 4. 生成预测
pred_df = predictor.predict(
    df=x_df,
    x_timestamp=x_timestamp,
    y_timestamp=y_timestamp,
    pred_len=pred_len,
    T=1.0,           # 采样温度
    top_p=0.9,        # Nucleus sampling
    sample_count=1    # 预测路径数量
)
```

**输入要求**：DataFrame 必须包含 `['open', 'high', 'low', 'close']`，`volume` 和 `amount` 可选。

**批量预测**：支持 `predict_batch` 方法，利用 GPU 并行对多个资产同时预测。

### 预测效果示例

![[prediction_example.png]]

---

## 5. 微调流程（A 股示例）

项目提供了基于 [Qlib](https://github.com/microsoft/qlib) 的完整微调流程：

### 四步走

| 步骤 | 操作 | 命令 |
| :--- | :--- | :--- |
| **1. 配置** | 修改 `finetune/config.py` 中的路径和超参数 | - |
| **2. 数据准备** | 用 Qlib 处理 A 股数据，拆分训练/验证/测试集 | `python finetune/qlib_data_preprocess.py` |
| **3a. 微调分词器** | 让分词器适应 A 股数据分布 | `torchrun --nproc_per_node=N finetune/train_tokenizer.py` |
| **3b. 微调预测器** | 微调主模型 | `torchrun --nproc_per_node=N finetune/train_predictor.py` |
| **4. 回测评估** | Top-K 策略回测 | `python finetune/qlib_test.py --device cuda:0` |

### 回测效果示例

![[backtest_result_example.png]]

### 依赖

```bash
pip install pyqlib
```

---

## 6. 从演示到生产的注意事项

> ⚠️ 项目提供的微调+回测是**简化示例**，不是生产就绪的量化系统。

*   **原始信号 vs 纯 Alpha**：模型输出的是原始预测信号。实际量化中需要通过投资组合优化对冲风险因子（市场 Beta、规模、价值等），分离出"纯 Alpha"。
*   **策略复杂性**：简单的 Top-K 策略只是起点。生产级策略需要动态仓位管理、止盈止损、交易成本/滑点模拟等。
*   **数据适配**：`QlibDataset` 是示例，不同数据源需要自行调整预处理逻辑。

---

## 7. 个人思考与笔记

### 亮点

- **把 K 线当语言**：将金融时序数据离散化为 token，用 NLP 范式处理，思路新颖
- **全球 45+ 交易所预训练**：跨市场、跨资产类别的泛化能力
- **完整的微调流程**：提供了 A 股 + Qlib 的端到端示例，落地门槛低
- **AAAI 2026 接收**：学术认可度高

### 待观察

- 模型最大上下文 512（除 mini 版 2048），对长周期分析是否够用？
- 金融市场的非平稳性（regime change）如何应对？
- 实盘中预测精度和延迟表现如何？
- Kronos-large（499M）未开源，最强版本无法使用

### 与因子投资的关联

- 模型预测信号可以作为一个**新的 Alpha 因子**输入多因子模型
- 微调流程中的"风险因子中性化"与《因子投资》第二章的截面回归思想一脉相承
- 回测框架中的 Qlib 是微软出品的量化研究平台，值得单独学习

---

## 引用

```bibtex
@misc{shi2025kronos,
    title={Kronos: A Foundation Model for the Language of Financial Markets},
    author={Yu Shi and Zongliang Fu and Shuo Chen and Bohan Zhao
            and Wei Xu and Changshui Zhang and Jian Li},
    year={2025},
    eprint={2508.02739},
    archivePrefix={arXiv},
    primaryClass={q-fin.ST},
    url={https://arxiv.org/abs/2508.02739},
}
```
