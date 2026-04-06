# Qwen3-8B 模型结构解析

通过 `torchinfo` 查看加载后的 Qwen3-8B（4bit 量化 + LoRA）模型结构。

## 整体架构

```
Qwen3ForCausalLM
├── Qwen3Model
│   ├── Embedding          # 词嵌入层
│   ├── ModuleList         # 36 个 Decoder 层
│   └── Qwen3RMSNorm       # 最终归一化
└── Linear                 # 语言模型头（lm_head）
```

## 参数统计

| 类型                | 参数量           |
| ----------------- | ------------- |
| 总参数（torchinfo 显示） | 51.9 亿（5.19B） |
| 实际参数              | **80 亿（8B）**  |
| 可训练参数             | 15.7 亿        |
| 冻结参数              | 36.2 亿        |

> **⚠️ torchinfo 的统计陷阱**：`torchinfo` 显示 5.19B 并非因为量化"压缩"了参数个数。4bit 量化的实现（bitsandbytes）会将两个 4bit 权重打包进一个 `uint8` 字节存储，`torchinfo` 通过 `.numel()` 统计 Tensor 元素个数时，看到的是打包后的字节数，因此显示为原始参数量的一半。模型实际仍是 8B 参数，只是每个参数从 16bit 压缩到了 4bit，**参数个数不变，每个参数的位宽减半**。

> **可训练参数 1.57B 的构成**：按 r=32 的纯 LoRA adapter 仅有约 87M 参数。剩余的 ~1.48B 来自 Unsloth 刻意保留为全精度（fp16）的 MLP 层——这些层没有被量化，因此作为可训练参数参与训练，是 Unsloth 提升训练稳定性的策略，而非意外解冻。

## 各层结构

### Embedding 层
- 词表大小：151,936（含特殊 token）
- 嵌入维度：4,096
- 参数量：622,329,856（约 6.2 亿，括号表示被冻结）

### Decoder 层（共 36 层）

torchinfo 显示两种参数量：

| 参数量（torchinfo） | 实际含义 |
|--------|------|
| 171,974,912 | MLP 保留为全精度 `Linear` 的层（可训练） |
| 96,477,440 | MLP 为 `Linear4bit` 的层（冻结） |

> Unsloth 在加载时会将部分 Decoder 层的 MLP 保留为 fp16 全精度而非量化，这些层的参数可训练，有助于维持训练稳定性。这不是 LoRA 的"选择性注入"——LoRA adapter 会均匀注入全部 36 层的目标模块。

每个 Decoder 层包含：
- **Self-Attention**：Q/K/V/O 四个线性层（4bit 量化）+ RMSNorm
- **MLP**：gate_proj / up_proj / down_proj + SiLU 激活
- **两个 RMSNorm**：attention 前、MLP 前

### lm_head
- 将 4096 维隐向量映射回词表（151,936 维）
- 参数量：622,329,856，与 Embedding 共享权重

## 分词器（Qwen2Tokenizer）

| 属性 | 值 |
|------|-----|
| 词表大小 | 151,643（基础） + 扩展特殊 token |
| 最大序列长度 | 40,960 |
| padding 方向 | 左侧（left） |
| truncation 方向 | 右侧（right） |
| EOS token | `<\|im_end\|>`（151645） |
| PAD token | `<\|PAD_TOKEN\|>`（151669，新增） |

### 特殊 Token 分类

**对话控制**
- `<|im_start|>` / `<|im_end|>`：对话轮次边界

**思维链**
- `<think>` / `</think>`：Qwen3 原生支持的 thinking mode，非 DeepSeek-R1 蒸馏

**工具调用**
- `<tool_call>` / `</tool_call>`：函数调用
- `<tool_response>` / `</tool_response>`：工具返回结果

**视觉多模态**（预留）
- `<|vision_start|>` / `<|vision_end|>` / `<|image_pad|>` 等

**代码补全（FIM）**
- `<|fim_prefix|>` / `<|fim_middle|>` / `<|fim_suffix|>`：Fill-in-the-Middle 代码补全

## 关键观察

1. **torchinfo 参数统计失真**：4bit 打包机制导致显示参数量减半，模型实际仍为 8B。

2. **4bit 量化降低的是显存，不是参数量**：`Linear4bit` 将每个参数从 16bit 压缩到 4bit，显存从约 16GB 降至约 5GB，参数个数不变。

3. **PAD token 是新增的**：原始 Qwen3 没有 PAD token，Unsloth 加载时自动添加了 `<|PAD_TOKEN|>`，用于批训练时的序列对齐。

---

## LoRA 注入后的模型结构

调用 `FastLanguageModel.get_peft_model()` 后，LoRA 适配器被注入到指定模块。

### LoRA 配置参数

```python
model = FastLanguageModel.get_peft_model(
    model,
    r = 32,                    # LoRA 秩
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj"],
    lora_alpha = 32,           # 缩放系数
    lora_dropout = 0,          # dropout（0 = 最优化）
    bias = "none",             # 不训练 bias
    use_gradient_checkpointing = "unsloth",  # 节省显存
    random_state = 3407,
)
```

| 参数 | 值 | 说明 |
|------|-----|------|
| r | 32 | 低秩矩阵的秩，越大表达能力越强，显存占用越多 |
| lora_alpha | 32 | 缩放系数，实际学习率缩放 = alpha/r = 1.0 |
| target_modules | 7 个模块 | Attention 的 Q/K/V/O + MLP 的三个投影层 |
| lora_dropout | 0 | 关闭 dropout，Unsloth 优化路径 |

### LoRA 原理

原始权重矩阵 $W$（冻结）被拆分为：

$$W' = W + \Delta W = W + BA$$

- $A$：形状 $(r, d_{in})$，随机初始化
- $B$：形状 $(d_{out}, r)$，零初始化（确保训练初始时 $\Delta W = 0$）
- 推理时只需计算 $Wx + BAx$，额外开销极小

### 每层 LoRA 参数量计算（r=32）

| 模块         | 输入维度  | 输出维度  | LoRA 参数量                     |
| ---------- | ----- | ----- | ---------------------------- |
| q_proj     | 4096  | 4096  | 32×4096 + 4096×32 = 262,144  |
| k_proj     | 4096  | 1024  | 32×4096 + 1024×32 = 163,840  |
| v_proj     | 4096  | 1024  | 32×4096 + 1024×32 = 163,840  |
| o_proj     | 4096  | 4096  | 32×4096 + 4096×32 = 262,144  |
| gate_proj  | 4096  | 12288 | 32×4096 + 12288×32 = 524,288 |
| up_proj    | 4096  | 12288 | 32×4096 + 12288×32 = 524,288 |
| down_proj  | 12288 | 4096  | 32×12288 + 4096×32 = 524,288 |
| **单层合计**   |       |       | **2,424,832**                |
| **36 层合计** |       |       | **87,293,952（约 8700 万）**     |

### torchinfo 的"看不见"问题

`torchinfo` 输出中看不到 LoRA 的 lora_A / lora_B 矩阵，原因是：

- LoRA 适配器被 PEFT 包装在 `Linear4bit` 内部，作为子模块存在
- depth=5 的层级恰好没有展开到 LoRA 矩阵那一层
- 实际上每个 `Linear4bit` 内部还有 `lora_A` 和 `lora_B` 两个小矩阵

### 注入后结构变化

对比注入前后，Layer 3-35 从 `Linear4bit` 变为 `Linear`，是 Unsloth 保留全精度的体现，并非 Bug。全精度层在 torchinfo 中参数量会显示为量化层的两倍（例如 q_proj 从 8,388,608 变为 16,777,216），这是 4bit 打包导致的统计差异，实际权重元素个数相同。

### Unsloth 的 Gradient Checkpointing

`use_gradient_checkpointing = "unsloth"` 开启后：

- 不保存中间激活值，反向传播时重新计算
- 显存减少约 30%
- **速度不会变慢**：Unsloth 用 Triton 内核优化了重计算过程，减少了显存读写带宽压力，实际速度与不开启相当甚至更快
- 对于 3090（24GB）跑 8B 模型微调是必要的
