# 词汇表（Vocabulary）构建

> NLP 中词到数字 ID 的映射方法
> 整理日期：2026-03-28

---

## 一句话解释

**词汇表** = 词 → 数字 ID 的映射表，ID 只是索引，语义靠 Embedding 学习。

---

## 示例

```python
SRC_VOCAB = {
    "<pad>": 0,     # 填充符
    "<unk>": 1,     # 未知词
    "<bos>": 2,     # 句子开始
    "<eos>": 3,     # 句子结束
    "I": 4,
    "am": 5,
    "a": 6,
    "student": 7,
    # ... 其他词
}
```

---

## 特殊 Token 的固定 ID

| Token | ID | 说明 |
|-------|----|------|
| `<pad>` | **0** | 必须固定为0，PyTorch Embedding 默认填充值 |
| `<unk>` | **1** | 未知词，通常固定为1 |
| `<bos>` | **2** | 句子开始（Begin of Sentence）|
| `<eos>` | **3** | 句子结束（End of Sentence）|
| 其他词 | **4+** | 随便排 |

---

## 普通词的分配方法

### 方法1：按频率排序（推荐）

```python
from collections import Counter

# 统计训练集中所有词的频率
word_counts = Counter(all_words)

# 按频率从高到低排序
vocab = {"<pad>": 0, "<unk>": 1, "<bos>": 2, "<eos>": 3}
for idx, (word, count) in enumerate(word_counts.most_common(), start=4):
    vocab[word] = idx
```

**好处**：
- 高频词 ID 小，Embedding 矩阵前面存常用词
- 可能有点缓存优势（访问更快）
- 低频词 ID 大，方便后续裁剪词汇表

### 方法2：按字母顺序

```python
unique_words = sorted(set(all_words))
vocab = {"<pad>": 0, "<unk>": 1, "<bos>": 2, "<eos>": 3}
for idx, word in enumerate(unique_words, start=4):
    vocab[word] = idx
```

**好处**：
- 简单直观
- 确定性强，可复现

### 方法3：随机分配

```python
import random

unique_words = list(set(all_words))
random.shuffle(unique_words)

vocab = {"<pad>": 0, "<unk>": 1, "<bos>": 2, "<eos>": 3}
for idx, word in enumerate(unique_words, start=4):
    vocab[word] = idx
```

**好处**：
- 没有偏见
- 缺点：不可复现（除非设随机种子）

---

## 关键理解：ID 只是索引，没有语义

```python
# 这些数字只是内存地址
"I": 4, "am": 5, "student": 7

# 4、5、7 不代表 "I"、"am"、"student" 有任何关系
# 语义是通过 Embedding 学习的
```

**Embedding 层**：
```python
nn.Embedding(vocab_size, d_model)
# 每个 ID 对应一个 d_model 维的向量
# 训练时自动学习这些向量
```

**可视化**：
```
词汇表:        Embedding 矩阵:
"I" → 4  →   [0.2, -0.5, 0.8, ...]  (d_model 维)
"am" → 5 →   [-0.3, 0.7, 0.1, ...]
"student" → 7 → [0.1, 0.2, -0.4, ...]
```

---

## 词汇表大小选择

| 场景 | 词汇表大小 | 说明 |
|------|-----------|------|
| 英文 | 32k-50k | BPE/WordPiece 子词 |
| 中文 | 50k-100k | 字级别或 BPE |
| 多语言 | 100k-250k | mBERT、XLM-R |
| 小玩具 | 100-1000 | 演示用 |

**BPE（Byte Pair Encoding）**：
- 不是用完整词，而是用子词（subword）
- "student" → ["stud", "ent"] 或 ["st", "udent"]
- 优势：减少 OOV（Out of Vocabulary）

---

## 代码示例：完整词汇表构建

```python
from collections import Counter
import json

def build_vocab(texts, min_freq=1, specials=None):
    """
    从文本列表构建词汇表
    
    Args:
        texts: 文本列表，如 ["I am a student", "you are good"]
        min_freq: 最小词频，低于此阈值的词忽略
        specials: 特殊token列表
    
    Returns:
        vocab: 词到ID的映射
        id2word: ID到词的映射
    """
    if specials is None:
        specials = ["<pad>", "<unk>", "<bos>", "<eos>"]
    
    # 分词并统计词频
    word_counts = Counter()
    for text in texts:
        words = text.split()  # 简单空格分词，实际用 tokenizer
        word_counts.update(words)
    
    # 过滤低频词
    word_counts = {w: c for w, c in word_counts.items() if c >= min_freq}
    
    # 构建词汇表
    vocab = {special: idx for idx, special in enumerate(specials)}
    
    # 按频率排序添加普通词
    for idx, (word, _) in enumerate(word_counts.most_common(), start=len(specials)):
        vocab[word] = idx
    
    # 反向映射
    id2word = {idx: word for word, idx in vocab.items()}
    
    return vocab, id2word


# 使用示例
texts = [
    "I am a student",
    "you are a good student",
    "I like apples",
]

vocab, id2word = build_vocab(texts, min_freq=1)

print(f"词汇表大小: {len(vocab)}")
print(f"词汇表: {vocab}")

# 保存
with open("vocab.json", "w") as f:
    json.dump(vocab, f, ensure_ascii=False, indent=2)
```

---

## 常见问题

### Q: ID 顺序影响模型效果吗？
**A:** 不影响。ID 只是索引，Embedding 层会学习每个 ID 对应的向量。顺序只影响初始化时的随机值。

### Q: 为什么 `<pad>` 必须是 0？
**A:** PyTorch 的 `nn.Embedding` 默认 `padding_idx=0`，这样 pad 位置的 Embedding 不会被更新（始终为0）。

### Q: 训练好的模型能改词汇表吗？
**A:** 不能。Embedding 矩阵的行数和词汇表大小绑定，改了 ID 就对应不上向量了。

### Q: OOV（Out of Vocabulary）怎么办？
**A:** 用 `<unk>` token 代替，或者使用 BPE 子词减少 OOV。

### Q: 中英文混合怎么办？
**A:** 统一用一个词汇表，或者分别构建 src_vocab 和 tgt_vocab（翻译任务）。

---

## 一句话总结

> **词汇表是词的身份证，ID 只是编号，语义靠 Embedding 学，顺序不重要，特殊 token 要固定。**

---

## 相关笔记

- [[Transformer训练篇]] —— 词汇表在训练中的使用
- [[BPE分词]] —— 子词分词方法
- [[Embedding层]] —— ID 如何变成向量
