# PEFT 参数高效微调概览

> Parameter-Efficient Fine-Tuning

## 一、为什么需要 PEFT

全量微调（Full Fine-Tuning）的问题：

| 问题 | 说明 |
|------|------|
| 显存要求高 | 7B 模型全量微调需要 ~80GB 显存 |
| 训练慢 | 所有参数都要计算梯度 |
| 存储笨重 | 每个任务保存一份完整模型 |
| 灾难性遗忘 | 微调后可能丢失原有能力 |

PEFT 目标：**只训练 <1% 的参数，效果接近全量微调。**

---

## 二、方法全景

```
PEFT
├── 加法类（Additive）     → 在模型上插入新模块
│   ├── Adapter
│   └── Prefix / Prompt Tuning
│
├── 重参数化类（Reparameterization）  → 低秩近似原有权重
│   └── LoRA 系列
│
└── 选择类（Selective）    → 只解冻原模型的部分参数
    └── BitFit 等
```

---

## 三、各方法详解

### 3.1 Adapter

**原理**：在 Transformer 每层内部插入小型 MLP 瓶颈模块。

```
原始层输出
    ↓
 下投影 (d → r)   ← 可训练
    ↓
 非线性激活
    ↓
 上投影 (r → d)   ← 可训练
    ↓
 残差连接
    ↓
下一层输入
```

- 推理时模块**无法消除**，有额外延迟
- 参数量：约 $2 \times d \times r$ 每层

---

### 3.2 Prefix Tuning

**原理**：在每一层的 Key、Value 前拼接可训练的**虚拟 token 向量**。

```
原始输入:  [token₁, token₂, ..., tokenₙ]
加前缀后:  [P₁, P₂, ..., Pₖ, token₁, token₂, ..., tokenₙ]
           ←  可训练前缀  →  ← 原始输入（冻结）→
```

- 前缀向量直接注入每层 Attention 的 KV
- 不修改模型结构，但推理时序列变长
- 对**生成任务**效果好

---

### 3.3 Prompt Tuning

**原理**：只在**输入层**加可训练的软提示向量，比 Prefix Tuning 更轻量。

```
输入 = [软提示向量（可训练）] + [原始文本 token（冻结）]
```

- 模型参数完全冻结
- 随模型规模增大，效果越来越接近全量微调
- 10B 以上模型效果才明显，小模型效果差

---

### 3.4 LoRA

**原理**：在原始权重矩阵旁并联一个低秩矩阵对，只训练低秩部分。

```
原始前向:  h = W x          (W 冻结)
LoRA 前向: h = W x + BA x   (B, A 可训练，r << d)
```

其中 $A \in \mathbb{R}^{r \times d}$，$B \in \mathbb{R}^{d \times r}$，$r$ 为 rank。

**推理时**直接 merge：$W' = W + BA$，零额外开销。

→ 详见 [[LoRA 原理可视化详解]]

---

### 3.5 QLoRA

**原理**：LoRA + 4-bit 量化原始模型。

```
原始模型权重  →  NF4 量化（4-bit）→  冻结
LoRA 矩阵    →  bfloat16         →  训练
```

- 将 65B 模型微调的显存需求压缩到单张 48GB GPU 可承受
- 引入 Double Quantization（对量化常数再次量化）
- 引入 Paged Optimizer（防止显存峰值 OOM）

---

### 3.6 DoRA

**原理**：将权重分解为**幅度**（magnitude）和**方向**（direction）分别微调。

$$W = m \cdot \frac{V}{\|V\|}$$

- 幅度 $m$：标量，控制整体大小
- 方向 $V/\|V\|$：用 LoRA 更新
- 效果优于 LoRA，参数量相近

---

### 3.7 IA³

**原理**：学习对激活值的**缩放向量**，而非加法增量。

```
h' = l ⊙ h    (l 是可训练的缩放向量，⊙ 逐元素乘)
```

- 参数量极少（比 LoRA 还少）
- 推理时可 merge，零额外开销
- 适合 few-shot 场景

---

### 3.8 BitFit

**原理**：只训练原模型的**偏置项**（bias），其余参数冻结。

- 参数量极少（<0.1%）
- 效果有限，适合资源极度受限场景

---

## 四、方法对比

| 方法 | 可训练参数量 | 推理开销 | 适用场景 |
|------|------------|---------|---------|
| Full FT | 100% | 无 | 资源充足 |
| Adapter | ~1% | 有延迟 | 多任务切换 |
| Prefix Tuning | ~0.1% | 序列变长 | 生成任务 |
| Prompt Tuning | ~0.01% | 序列变长 | 超大模型 |
| LoRA | ~0.1-1% | **零**（merge 后） | 通用首选 |
| QLoRA | ~0.1-1% | 量化解码开销 | 消费级 GPU |
| IA³ | ~0.01% | **零**（merge 后） | 极轻量场景 |
| BitFit | <0.1% | 无 | 极简场景 |

---

## 五、如何选择

```
显存 < 16GB？
    └─ 是 → QLoRA（4-bit 量化 + LoRA）
    └─ 否 ↓

需要同时挂多个任务适配器？
    └─ 是 → Adapter 或 LoRA（不 merge，按需切换）
    └─ 否 ↓

模型 > 10B？
    └─ 是 → Prompt Tuning 也可考虑
    └─ 否 ↓

默认选择 → LoRA（效果、开销、灵活性最均衡）
```

---

## 六、Hugging Face PEFT 库

```python
from peft import get_peft_model, LoraConfig, TaskType

config = LoraConfig(
    r=8,                        # rank
    lora_alpha=32,              # 缩放系数
    target_modules=["q_proj", "v_proj"],  # 应用到哪些层
    lora_dropout=0.1,
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(base_model, config)
model.print_trainable_parameters()
# trainable params: 4,194,304 || all params: 6,742,609,920 || trainable%: 0.06%
```

---

## 七、核心思想总结

所有 PEFT 方法本质都在回答同一个问题：

> **微调时改变的信息量（delta）是低维的**，不需要动原始高维权重。

- LoRA：delta 是低秩矩阵
- Adapter：delta 是瓶颈模块的输出
- Prefix：delta 是 KV 空间中的偏移
- Prompt：delta 是输入空间的软提示

---

## 相关概念

- [[LoRA 原理可视化详解]] — LoRA 的数学原理与可视化
- [[正定矩阵与优化]] — 微调背后的优化理论
- 量化（Quantization）— QLoRA 的基础
- Transformer 架构 — PEFT 方法的作用对象
