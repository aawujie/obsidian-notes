# BLEU Score —— 机器翻译自动评估指标

> Bilingual Evaluation Understudy，比较机器翻译和人工参考翻译的相似度
> 整理日期：2026-03-28

---

## 一句话

**BLEU = 看机器翻译和人工翻译有多像，n-gram 精确率的几何平均。**

---

## 核心思想

### 直观理解

```
人工翻译（参考答案）：
  "The cat sat on the mat."

机器翻译（待评估）：
  "The cat sat on the mat."  ← 完全一样，BLEU = 100%
  "The cat is on the mat."   ← 有点不同，BLEU = 中等
  "A dog runs in the park."  ← 完全不同，BLEU ≈ 0
```

### 为什么需要 BLEU？

| 评估方式 | 优点 | 缺点 |
|---------|------|------|
| **人工评估** | 准确，考虑语义 | 慢，贵，不可复现 |
| **BLEU** | 快，免费，可复现 | 只看表面匹配 |

**BLEU 是人工评估的"廉价替代品"**

---

## 计算步骤

### 1. n-gram 精确率

#### 1-gram（单个词匹配）

```python
机器翻译: "the cat sat on the mat"
参考翻译: "the cat sat on the mat"

匹配统计:
  the: 机器2次，参考2次 → min(2,2) = 2
  cat: 机器1次，参考1次 → min(1,1) = 1
  sat: 机器1次，参考1次 → min(1,1) = 1
  on:  机器1次，参考1次 → min(1,1) = 1
  mat: 机器1次，参考1次 → min(1,1) = 1

匹配数 = 6
机器总词数 = 6
1-gram 精确率 = 6/6 = 100%
```

#### 2-gram（两个连续词）

```python
机器翻译 2-grams: "the cat", "cat sat", "sat on", "on the", "the mat"
参考翻译 2-grams: "the cat", "cat sat", "sat on", "on the", "the mat"

匹配: 5/5 = 100%
```

#### 3-gram 和 4-gram

```python
3-grams: "the cat sat", "cat sat on", "sat on the", "on the mat"
匹配: 4/4 = 100%

4-grams: "the cat sat on", "cat sat on the", "sat on the mat"
匹配: 3/3 = 100%
```

### 2. 简短惩罚（Brevity Penalty）

#### 问题：机器翻译会"作弊"

```python
参考: "The cat sat on the mat"
机器: "The cat"  ← 只翻译了部分

1-gram 精确率 = 2/2 = 100%  ← 作弊成功！
```

#### 解决方案

```python
如果机器翻译长度 ≥ 参考长度:
    BP = 1  （无惩罚）

如果机器翻译长度 < 参考长度:
    BP = exp(1 - 参考长度 / 机器长度)

示例:
  参考长度 = 6
  机器长度 = 2
  BP = exp(1 - 6/2) = exp(-2) ≈ 0.135  ← 大幅惩罚！
```

### 3. 最终 BLEU 公式

```python
BLEU = BP × exp(Σ w_n × log(p_n))

其中:
  p_n = n-gram 精确率（通常 n=1,2,3,4）
  w_n = 权重（通常平均，各 1/4）
  BP = 简短惩罚
  exp(log(...)) = 几何平均
```

---

## 代码实现

### 使用 NLTK

```python
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

# 参考翻译（可以有多个参考答案）
references = [
    ['The', 'cat', 'sat', 'on', 'the', 'mat'],
    ['The', 'cat', 'is', 'sitting', 'on', 'the', 'mat']  # 另一个参考
]

# 机器翻译（候选）
candidate = ['The', 'cat', 'sat', 'on', 'the', 'mat']

# 计算 BLEU（默认 4-gram）
score = sentence_bleu(references, candidate)
print(f"BLEU: {score:.4f}")  # 1.0 = 完美匹配

# 不同质量的翻译
candidate2 = ['The', 'cat', 'is', 'on', 'the', 'mat']
score2 = sentence_bleu(references, candidate2)
print(f"BLEU: {score2:.4f}")  # 约 0.6-0.8

candidate3 = ['A', 'dog', 'runs', 'in', 'the', 'park']
score3 = sentence_bleu(references, candidate3)
print(f"BLEU: {score3:.4f}")  # 接近 0
```

### 手动实现（简化版）

```python
import math
from collections import Counter

def get_ngrams(tokens, n):
    """获取 n-gram 列表"""
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def bleu_score(candidate, references, max_n=4):
    """简化版 BLEU 计算"""
    
    # 计算各阶 n-gram 精确率
    precisions = []
    for n in range(1, max_n + 1):
        candidate_ngrams = Counter(get_ngrams(candidate, n))
        
        # 统计匹配数（取 min(候选出现次数, 参考出现次数)）
        matches = 0
        total = sum(candidate_ngrams.values())
        
        for ref in references:
            ref_ngrams = Counter(get_ngrams(ref, n))
            for ngram, count in candidate_ngrams.items():
                matches += min(count, ref_ngrams[ngram])
        
        # 避免除0
        if total == 0:
            precisions.append(0)
        else:
            precisions.append(matches / total)
    
    # 几何平均（取 log 后平均，再 exp）
    if min(precisions) > 0:
        geo_mean = math.exp(sum(math.log(p) for p in precisions) / max_n)
    else:
        geo_mean = 0
    
    # 简短惩罚
    c = len(candidate)
    r = min(len(ref) for ref in references)  # 最短参考长度
    
    if c > r:
        bp = 1
    else:
        bp = math.exp(1 - r / c)
    
    return bp * geo_mean

# 测试
candidate = ['The', 'cat', 'sat', 'on', 'the', 'mat']
reference = [['The', 'cat', 'sat', 'on', 'the', 'mat']]

print(bleu_score(candidate, reference))  # 1.0
```

---

## BLEU 的优缺点

### 优点

| 优点 | 说明 |
|------|------|
| ✅ **自动评估** | 快速，无需人工 |
| ✅ **可复现** | 相同输入，相同输出 |
| ✅ **语言无关** | 适用于任何语言对 |
| ✅ **和人工评价相关** | 研究表明 BLEU 和人工评分有一定相关性 |
| ✅ **行业标准** | 机器翻译论文标配 |

### 缺点

| 缺点 | 说明 | 示例 |
|------|------|------|
| ❌ **不考虑语义** | 只看词匹配 | "cat" 和 "feline" 算不同 |
| ❌ **同义词问题** | 同义词算错误 | "big" ≠ "large" |
| ❌ **语序不敏感** | 词顺序影响小 | "cat the sat" 可能 BLEU 不低 |
| ❌ **短句不稳定** | 短句波动大 | 单句 BLEU 不可靠 |
| ❌ **需要参考翻译** | 没有参考无法计算 | 新领域困难 |

---

## 评分标准

| BLEU 分数 | 质量评价 | 说明 |
|-----------|---------|------|
| **< 10** | 很差 | 几乎无法理解 |
| **10-20** | 差 | 有很多错误 |
| **20-30** | 一般 | 能理解大意 |
| **30-40** | 可接受 | 基本可读 |
| **40-50** | 好 | 比较流畅 |
| **50-60** | 很好 | 接近人工 |
| **> 60** | 优秀 | 难以区分机器/人工 |

### 实际系统表现

| 系统 | 年份 | 英德翻译 BLEU |
|------|------|--------------|
| 传统 SMT | 2014 | ~20 |
| Transformer | 2017 | **28.4** |
| GPT-3 | 2020 | ~40 |
| 人工翻译 | - | ~50-60 |

---

## BLEU 的变体

| 变体 | 改进点 | 适用场景 |
|------|--------|---------|
| **BLEU-1** | 只看 1-gram | 快速评估 |
| **BLEU-4** | 标准 4-gram | 机器翻译标配 |
| **Sentence-BLEU** | 单句 BLEU | 句子级评估 |
| **Corpus-BLEU** | 语料级 BLEU | 更稳定 |
| **Smoothing** | 平滑处理 | 避免 0 值 |

### 平滑方法

```python
from nltk.translate.bleu_score import SmoothingFunction

# 当某些 n-gram 没有匹配时，避免 log(0)
smoothing = SmoothingFunction().method1
score = sentence_bleu(references, candidate, smoothing_function=smoothing)
```

---

## 其他评估指标

| 指标 | 特点 | 与 BLEU 对比 |
|------|------|-------------|
| **METEOR** | 考虑同义词、词干 | 比 BLEU 更接近人工评价 |
| **ROUGE** | 面向召回率 | 摘要任务常用 |
| **CIDEr** | 基于 TF-IDF | 图像描述任务 |
| **BERTScore** | 用 BERT 计算语义相似度 | 考虑语义，更准但更慢 |
| **COMET** | 神经网络评估 | 目前 SOTA |

---

## 一句话总结

> **BLEU = 机器翻译和人工翻译的 n-gram 相似度，快速但只看表面匹配，是人工评估的廉价替代品。**

---

## 相关笔记

- [[机器翻译评估]] —— 翻译质量评估方法综述
- [[METEOR]] —— 考虑同义词的评估指标
- [[BERTScore]] —— 基于语义相似度的评估
- [[Transformer]] —— BLEU 28.4 的翻译模型
