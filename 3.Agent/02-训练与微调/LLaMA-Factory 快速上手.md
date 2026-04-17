# LLaMA-Factory 快速上手

> 环境已准备：llmtuner 0.7.1 + PyTorch 2.4.1 + CUDA 12.2

---

## 1. 验证安装

```bash
python3 -c "import llmtuner; print('OK')"
```

---

## 2. 准备数据

创建 `data/alpaca_zh.json`：

```json
[
  {
    "instruction": "请介绍一下自己",
    "input": "",
    "output": "我是由深度求索开发的AI助手，专门用于帮助用户解答问题。"
  },
  {
    "instruction": "翻译这句话",
    "input": "Machine learning is fascinating",
    "output": "机器学习非常迷人"
  }
]
```

创建 `data/dataset_info.json`：

```json
{
  "alpaca_zh": {
    "file_name": "alpaca_zh.json",
    "formatting": "alpaca"
  }
}
```

---

## 3. 单卡 QLoRA 训练

```bash
llmtuner-cli train \
  --model_name_or_path Qwen/Qwen2.5-7B-Instruct \
  --dataset alpaca_zh \
  --template qwen \
  --finetuning_type lora \
  --lora_target q_proj,v_proj \
  --lora_rank 16 \
  --lora_alpha 32 \
  --quantization_bit 4 \
  --output_dir ./qwen_lora \
  --per_device_train_batch_size 1 \
  --gradient_accumulation_steps 4 \
  --learning_rate 5e-5 \
  --num_train_epochs 3 \
  --max_samples 1000 \
  --logging_steps 10 \
  --save_steps 100 \
  --plot_loss
```

---

## 4. 关键参数解释

| 参数 | 说明 |
|------|------|
| `quantization_bit 4` | 4-bit 量化 (QLoRA) |
| `lora_rank 16` | 低秩维度 r=16 |
| `lora_alpha 32` | 缩放系数 (alpha/r=2) |
| `lora_target` | 应用 LoRA 的层 |
| `gradient_accumulation_steps` | 梯度累积，模拟大 batch |

---

## 5. 合并 LoRA 权重

训练完成后合并为完整模型：

```bash
llmtuner-cli export \
  --model_name_or_path Qwen/Qwen2.5-7B-Instruct \
  --adapter_path ./qwen_lora \
  --template qwen \
  --finetuning_type lora \
  --export_dir ./qwen_finetuned \
  --export_size 2 \
  --export_device cpu \
  --export_legacy_format False
```

---

## 6. 启动 Web UI（可选）

```bash
llmtuner-cli webui
```

浏览器打开 `http://localhost:7860`

---

## 7. 显存估算

| 模型 | 精度 | 显存需求 |
|------|------|----------|
| Qwen2.5-7B | 4-bit + LoRA | ~6GB |
| Qwen2.5-14B | 4-bit + LoRA | ~10GB |
| Qwen2.5-72B | 4-bit + LoRA | ~48GB |

你的 RTX 3090 (24GB) 可以微调 14B 甚至 32B 模型。

---

## 下一步

1. 准备自己的领域数据
2. 调整 `lora_rank` 和 `learning_rate`
3. 尝试多轮对话格式 (ShareGPT)
