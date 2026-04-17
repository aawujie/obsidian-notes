# LoRA 微调原理

> 制定日期：2026-03-29
> 参考：Hu et al. 2021 "LoRA: Low-Rank Adaptation of Large Language Models"

---

## 核心思想

大模型参数太多（7B、13B、70B），全量微调成本太高。

**LoRA 的 insight**：预训练模型的权重变化具有低秩特性。

即：$W = W_0 + \Delta W$，其中 $\Delta W$ 是低秩矩阵。

---

## 数学原理

### 原始微调
```
全量更新: W_new = W_old - lr * ∇L
需要存储: 7B 参数的梯度 + 优化器状态 ≈ 28GB+ (fp16)
```

### LoRA 方法
```
冻结原权重 W_0，只训练两个低秩矩阵 A 和 B

W = W_0 + B * A

其中:
- W_0: d × d (冻结)
- A: r × d (可训练, r << d)
- B: d × r (可训练)

参数量从 d×d 降到 r×(2d)
例如 d=4096, r=16: 16.7M → 131k (节省 99.2%)
```

---

## 为什么只加在 Attention？

论文发现：
- **Attention 的 Q、V 矩阵** 加 LoRA 效果最好
- FFN 层加 LoRA 收益较小
- 所以通常只给 `q_proj` 和 `v_proj` 加 LoRA

---

## 关键超参数

| 参数 | 含义 | 推荐值 |
|------|------|--------|
| `r` (rank) | 低秩维度 | 8, 16, 32, 64 |
| `lora_alpha` | 缩放系数 | 通常 = r 或 2r |
| `lora_dropout` | dropout 率 | 0.05 - 0.1 |
| `target_modules` | 应用层 | q_proj, v_proj |

### alpha 的作用
```
实际缩放 = alpha / r

例如: r=16, alpha=32 → 缩放=2
      r=64, alpha=16 → 缩放=0.25
```

---

## QLoRA = LoRA + 量化

进一步节省显存：

| 方法 | 模型精度 | 7B 模型显存 |
|------|----------|-------------|
| 全量微调 | fp16 | ~14GB |
| LoRA | fp16 | ~8GB |
| **QLoRA** | **4-bit** | **~4GB** |

### QLoRA 技术栈
```
1. 4-bit NormalFloat (NF4) 量化
2. Double Quantization (量化常数也量化)
3. Page Optimizer (分页优化器，防止梯度检查点 OOM)
```

---

## 训练流程

```
1. 加载预训练模型 (4-bit 量化)
2. 准备 LoRA 配置 (r, alpha, target_modules)
3. 使用 PEFT 包装模型
4. 准备指令数据 (Alpaca/ShareGPT 格式)
5. 训练 (只更新 A、B 矩阵)
6. 保存 LoRA 权重 (只有几 MB)
7. 推理时合并权重或动态加载
```

---

## 数据格式

### Alpaca 格式
```json
{
  "instruction": "请翻译这句话",
  "input": "Hello world",
  "output": "你好世界"
}
```

### ShareGPT 格式
```json
{
  "conversations": [
    {"from": "human", "value": "你好"},
    {"from": "gpt", "value": "你好！有什么可以帮你的？"}
  ]
}
```

---

## 实际效果

| 模型 | 任务 | LoRA r=16 效果 |
|------|------|----------------|
| LLaMA-2-7B | 中文对话 | 接近全量微调 |
| Qwen-7B | 代码生成 | 达到 SOTA |
| ChatGLM3-6B | 工具调用 | 显著提升 |

---

## 代码示例

```python
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM

# 1. 加载模型
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-7B-Instruct",
    load_in_4bit=True,  # QLoRA
    device_map="auto"
)

# 2. LoRA 配置
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# 3. 应用 LoRA
model = get_peft_model(model, lora_config)

# 4. 打印可训练参数
model.print_trainable_parameters()
# → trainable params: 20M || all params: 7B || trainable%: 0.28%
```

---

## 相关笔记

- [[Adam Optimizer]] — 优化器选择
- [[Transformer学习率调度]] — 学习率策略
- [[Transformer词汇表与BPE]] — 分词基础
