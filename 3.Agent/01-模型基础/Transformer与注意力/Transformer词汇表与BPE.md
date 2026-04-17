# Transformer 词汇表与 BPE 分词

> Transformer 原论文的词汇表设置和 BPE 子词分词方法
> 整理日期：2026-03-28

---

## 一句话

**Transformer 用 37k 词汇表 + BPE 子词分词，从 WMT 2014 数据集自动学习得到。**

---

## 原论文设置

| 配置 | 值 | 说明 |
|------|-----|------|
| **源语言词汇表（英语）** | **37,000** | WMT 2014 英德翻译 |
| **目标语言词汇表（德语）** | **32,000** | 德语略小 |
| **分词方法** | **Byte Pair Encoding (BPE)** | 子词级分词 |
| **数据集** | WMT 2014 | 约 450 万句对 |

---

## 为什么用 BPE？

### 传统分词的问题

```
单词级分词：
  "unhappiness" → 不在 5 万词表里 → <unk>（未知词）
  "ChatGPT" → 新词 → <unk>
  "covid-19" → 没见过 → <unk>

问题：
- OOV（Out of Vocabulary）太多
- 无法处理新词、罕见词
- 词汇表需要非常大
```

### BPE 解决方案

```
BPE 子词分词：
  "unhappiness" → "un" + "happiness"
  "ChatGPT" → "Chat" + "GPT"
  "covid-19" → "covid" + "-19"

好处：
- 任何词都能拆成子词
- 词汇表大小可控（30k-50k）
- 新词也能处理
```

---

## BPE 学习过程

### 算法步骤

```python
# 1. 初始化：每个字符是一个词
词汇表: {'l', 'o', 'w', 'e', 'r', 'n', 's', 't', 'i', 'd'}

# 2. 统计频率最高的字符对
"es" 出现了 100 次 → 合并为 "es"
"st" 出现了 90 次 → 合并为 "st"
"est" 出现了 80 次 → 合并为 "est"
...

# 3. 重复合并，直到达到目标词汇表大小
最终词汇表: 37,000 个子词单元
```

### 实际例子

```python
# 训练前（字符级）
"low" → ['l', 'o', 'w']
"lower" → ['l', 'o', 'w', 'e', 'r']
"lowest" → ['l', 'o', 'w', 'e', 's', 't']

# 训练后（子词级）
"low" → ['low']
"lower" → ['low', 'er']
"lowest" → ['low', 'est']

# 新词也能处理
"lowering" → ['low', 'er', 'ing']  # 用已学的子词组合
```

---

## 词表来源

### 官方来源

| 来源 | 链接/方式 | 说明 |
|------|----------|------|
| **原论文代码** | tensor2tensor GitHub | Google 官方实现 |
| **WMT 2014 数据集** | statmt.org | 原始训练数据 |
| **Hugging Face** | `transformers` 库 | 预训练模型词表 |

### 下载预训练词表

```python
# 方法1: Hugging Face Transformers
from transformers import AutoTokenizer

# BERT 词表（30k WordPiece）
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
print(f"BERT 词表大小: {len(tokenizer.vocab)}")  # 30522

# GPT-2 词表（50k BPE）
tokenizer = AutoTokenizer.from_pretrained("gpt2")
print(f"GPT-2 词表大小: {len(tokenizer.vocab)}")  # 50257

# 查看词表内容
print(list(tokenizer.vocab.items())[:10])
# [('the', 1996), ('a', 1037), ('to', 1010), ...]
```

```python
# 方法2: 直接下载词表文件
# BERT: https://huggingface.co/bert-base-uncased/raw/main/vocab.txt
# GPT-2: https://huggingface.co/gpt2/raw/main/vocab.json

import json

# 加载 GPT-2 词表
with open('vocab.json', 'r') as f:
    vocab = json.load(f)
print(f"词表大小: {len(vocab)}")
print(f"示例: {list(vocab.items())[:5]}")
```

---

## 不同模型的词表对比

| 模型 | 年份 | 词表大小 | 分词方法 | 特点 |
|------|------|---------|---------|------|
| **Transformer** | 2017 | 37k | BPE | 英德翻译 |
| **BERT** | 2018 | 30k | WordPiece | 双向编码 |
| **GPT** | 2018 | 40k | BPE | 单向生成 |
| **GPT-2** | 2019 | 50k | BPE | 更大词表 |
| **RoBERTa** | 2019 | 50k | BPE | 优化版 BERT |
| **GPT-3** | 2020 | 50k | BPE | 超大模型 |
| **LLaMA** | 2023 | 32k | SentencePiece | 多语言 |
| **LLaMA-2** | 2023 | 32k | SentencePiece | 多语言优化 |

---

## 词表内容示例

### BERT WordPiece 词表（前20个）

```
[PAD]    → 0      # 填充符
[UNK]    → 100    # 未知词
[CLS]    → 101    # 分类标记
[SEP]    → 102    # 分隔标记
[MASK]   → 103    # 掩码标记
the      → 1996   # 最常见词
a        → 1037
to       → 1010
of       → 1997
and      → 1998
in       → 1999
...
```

### BPE 子词示例

```python
# GPT-2 BPE 词表中的子词
'Ġthe'      →  518   # Ġ 表示空格开头
'Ġa'        →  257
'ing'       →  1207  # 常见后缀
'ed'        →  1183  # 常见后缀
'Ġun'       →  489   # 常见前缀
'Ġre'       →  412
'Ġlow'      →  12345 # 完整词
'er'        →  339   # 子词
'est'       →  402   # 子词
...
```

---

## 如何构建自己的 BPE 词表

```python
from tokenizers import Tokenizer, models, trainers, pre_tokenizers

# 1. 创建 BPE 分词器
tokenizer = Tokenizer(models.BPE())

# 2. 设置预分词器（按空格和标点分割）
tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()

# 3. 训练
trainer = trainers.BpeTrainer(
    vocab_size=37000,           # 目标词汇表大小
    special_tokens=["<pad>", "<unk>", "<bos>", "<eos>"]
)

files = ["train.txt"]  # 训练语料
tokenizer.train(files, trainer)

# 4. 保存
tokenizer.save("my_bpe_tokenizer.json")

# 5. 使用
encoded = tokenizer.encode("Hello world")
print(encoded.tokens)  # ['Hello', 'world']
print(encoded.ids)     # [1234, 5678]
```

---

## 玩具数据集 vs 真实词表

| 对比项 | 你的玩具数据 | 真实词表（Transformer） |
|--------|-------------|----------------------|
| **词汇量** | 12 个词 | 37,000 个子词 |
| **来源** | 人工定义 | BPE 自动学习 |
| **覆盖范围** | 几个简单句子 | 数百万句子 |
| **OOV 处理** | 容易遇到未知词 | 子词覆盖，很少 OOV |
| **新词处理** | 无法处理 | 可拆分为子词 |
| **多语言** | 单一语言 | 可支持多语言 |

---

## 常见问题

### Q: 为什么原论文英语 37k，德语 32k？
**A:** 英语语料更多，词汇更丰富；德语有复合词，BPE 拆分后子词更少。

### Q: 词表越大越好吗？
**A:** 不是。太大增加计算量，太小 OOV 多。30k-100k 是 sweet spot。

### Q: 中文怎么处理？
**A:** 中文用字级或子词。BERT 中文版用 21k 个字，现代模型用 BPE/SentencePiece 学子词。

### Q: 不同语言的词表可以共享吗？
**A:** 可以。多语言模型（如 mBERT、XLM-R）用共享词表，通常 100k-250k。

---

## 一句话总结

> **Transformer 词表是 BPE 从 WMT 数据集自动学习的 37k 子词，现代模型词表可在 Hugging Face 下载，大小通常在 30k-100k 之间。**

---

## 相关笔记

- [[Transformer词汇表与BPE]] —— BPE 算法详细原理
- [[WordPiece分词]] —— BERT 使用的分词方法
- [[SentencePiece]] —— 另一种子词分词方法
- [[词汇表Vocabulary构建]] —— 如何构建自己的词汇表
