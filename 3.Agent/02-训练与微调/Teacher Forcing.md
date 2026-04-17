# Teacher Forcing —— 序列生成训练技巧

> Transformer 等序列模型训练时的关键技术
> 整理日期：2026-03-28

---

## 一句话解释

**Teacher Forcing** = 训练时用**真实标签**作为下一步输入，而不是模型自己的预测。

---

## 直观对比

### 正常生成（推理时）
```
输入: "I am" → 预测 "a" → 输入 "I am a" → 预测 "student"
     ↑___________________________________________↓
     用模型自己上一轮的预测，作为下一步的输入
```

### Teacher Forcing（训练时）
```
输入: "I am" + 真实标签 "a" → 预测 "student"
     ↑________________________↓
     直接用真实的标签，而不是模型的预测
```

---

## 为什么叫 "Teacher"？

| 术语 | 含义 |
|------|------|
| **Teacher** | 真实的标签（正确答案） |
| **Forcing** | 强制把正确答案喂给模型 |

就像老师手把手教学生：不管学生猜什么，直接告诉他正确答案，让他继续学下一个。

---

## 代码示例

```python
# 目标序列: [<bos>, Je, suis, un, étudiant, <eos>]

# Teacher Forcing: 输入是真实标签的前半部分
decoder_input = tgt[:-1]   # [<bos>, Je, suis, un, étudiant]
target_output = tgt[1:]    # [Je, suis, un, étudiant, <eos>]

# 前向传播
output = model(src, decoder_input)  # 用真实标签作为输入
loss = criterion(output, target_output)  # 和真实标签比较
```

---

## 优缺点

| 优点 | 缺点 |
|------|------|
| ✅ 训练稳定，不会把错误传播下去 | ❌ 训练和推理不一致（Exposure Bias）|
| ✅ 收敛快 | ❌ 推理时模型没见过自己的错误 |
| ✅ 实现简单 | ❌ 可能产生不自然的输出 |

---

## 问题：Exposure Bias

**现象**：训练时模型总是看到正确答案，推理时却看到自己的错误 → 性能下降。

**解决方案：Scheduled Sampling**

训练初期用 Teacher Forcing，后期逐渐用模型自己的预测：

```python
# 以概率 p 使用真实标签，(1-p) 使用模型预测
if random.random() < teacher_forcing_ratio:
    decoder_input = true_label
else:
    decoder_input = model_prediction
```

---

## 在 Transformer 中的实现

```python
# transformer_training_marimo.py 中的 Teacher Forcing
tgt_input = tgt_batch[:, :-1]   # 去掉最后一个 <eos>，作为输入
tgt_output = tgt_batch[:, 1:]   # 去掉第一个 <bos>，作为目标

output = model(src_batch, tgt_input, ...)  # 用 tgt_input 而不是上一轮预测
```

---

## 相关笔记

- [[Transformer架构从零理解]] —— Transformer 架构详解
- [[transformer_training_marimo]] —— 训练篇，包含 Teacher Forcing 实践
