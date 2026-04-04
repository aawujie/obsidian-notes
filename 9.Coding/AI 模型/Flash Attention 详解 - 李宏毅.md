---
share_link: https://share.note.sx/wcr7t1ig#hhGA2sJKflmSlOMLNwBv8sfDAhUYafT/eeF+xkSZqm0
share_updated: 2026-04-01T22:50:25+08:00
---
# Flash Attention 详解

> **视频来源：** [李宏毅 - Flash Attention 课程](https://youtu.be/vXb2QYOUzl4?si=ZJajE1NmTeu0NNn7)
> **提取时间：** 2026-04-01

---

## 1. 课程概述

### 1.1 目标
- 加快语言模型的**生成速度**（Inference/推論阶段）
- 假设已经清楚 Transformer 内部运作原理
- 不是讲训练过程，而是讲**已训练好的模型如何加速生成**

### 1.2 加速方法的代价
任何加速方法都有代价，通常是用**不关心的资源**换取速度：

| 代价类型                | 说明                 |
| ------------------- | ------------------ |
| **改变 Attention 计算** | 结果是近似值，与原来不一样      |
| **模型绑定**            | 必须训练特定模型才能使用，非随插即用 |
| **其他代价**            | 如额外计算、内存等          |

### 1.3 课程安排
- **第一部分：** Flash Attention（最详细）
- **第二部分：** KV Cache 相关方法（快速带过）
- **不讲：** Speculative Decoding（2024年第16讲已讲过）

---

## 2. Transformer 基础回顾

### 2.1 语言模型 = 文字接龙
- 给未完成的句子，预测下一个 token
- 主流架构：**Transformer**

### 2.2 Transformer 结构
- 多层 Layer
- 每层有 **Self-Attention** 机制
- Self-Attention 让 Transformer 考虑整个输入 Sequence 的所有信息

### 2.3 Self-Attention 计算流程

**输入：** X1 到 X5（一排向量）

**Step 1：生成 QKV**
- X1 → V1, K1, Q1
- X2 → V2, K2, Q2
- ...以此类推

**Step 2：计算 Attention（以第4个位置为例）**
1. Q4 与 K1-K4 做 dot product → a1-a4（attention weight）
2. 过 softmax 归一化 → â1-â4（0-1之间，和为1）
3. 每个 â 乘对应 V，做 weighted sum → O4（输出）

**公式：**
```
âi = exp(ai - amax) / Σ exp(aj - amax)
Oi = Σ âi × Vi
```

> 注：实际计算会减 amax（最大 dot product 值）防止指数爆炸

---

## 3. GPU 运算的底层逻辑

### 3.1 核心概念：工作台 vs 仓库

| 概念 | 名称 | 特点 |
|------|------|------|
| **工作台** | SRAM (on-chip) | 小、快、运算瞬间完成 |
| **仓库** | HBM | 大、慢、搬数据花时间 |

**比喻：**
- GPU 有很多 **Execution Unit**（小精灵，三头六臂代表多分身）
- 它们运算很快，但**工作台太小**
- 大数据必须放在**仓库**，需要时搬到工作台

### 3.2 瓶颈：搬数据
- 工作台上的运算：**瞬间完成**
- 搬数据（仓库 ↔ 工作台）：**花时间，是瓶颈**

**Flash Attention 的核心思想：**
> 改变计算顺序，**减少搬数据次数**，结果不变

---

## 4. 标准 Attention 的计算流程（多次读写）

### 4.1 问题设定
- Query 要与 L 个 Key 算 dot product
- L = sequence 长度（可能 10万、100万）
- 工作台放不下所有 Key，必须切成 **chunk**（每块 N 个）

### 4.2 计算 A（dot product）
```
第1个 chunk：读 N 个 Key → 与 Q 算 dot → 得 A1-AN → 存回仓库
第2个 chunk：读 N 个 Key → 与 Q 算 dot → 得 AN+1-A2N → 存回仓库
...
共 B = L/N 次
```

### 4.3 计算 Â（softmax 归一化）

**需要：** Amax（所有 A 的最大值）和分母（Σ exp(Ai - Amax)）

**问题：** 工作台不能放与 L 有关的东西（如 100万个数值）

**找 Amax 的方法：**
```
读 chunk 1 → 找最大值 D1 → 存 D1
读 chunk 2 → 与 D1 比 → 更新最大值 D2 → 存 D2
...
读 chunk B → 得 DB = Amax
```

**找分母的方法：**
```
读 chunk 1 → Σ exp(Ai - Amax) → 存 S1
读 chunk 2 → 加总 → 存 S2
...
得 SB = 分母
```

**计算 Â：**
```
读 chunk 1 → exp(Ai - Amax) / SB → 存 Â1-N
读 chunk 2 → exp(Ai - Amax) / SB → 存 ÂN+1-2N
...
```

### 4.4 计算 O（Weighted Sum）
```
读 chunk 1 的 V 和 Â → weighted sum → 得 O1
读 chunk 2 的 V 和 Â → weighted sum → 加 O1 → 得 O2
...
得最终 OB = Attention Layer 输出
```

### 4.5 问题：多次读写仓库
- 计算 A：B 次读写
- 找 Amax：B 次读写
- 找分母：B 次读写
- 计算 Â：B 次读写
- 计算 O：B 次读写

**总共：多次来回搬数据！**

---

## 5. Flash Attention 简化版：减少 softmax 的读写

### 5.1 核心技巧：同时找 Amax 和分母

**观察：** 找 Amax 和分母可以**一次完成**

**流程：**
```
读 chunk 1：
  - 找最大值 D1
  - 假设 D1 = Amax
  - 算 S1 = Σ exp(Ai - D1)
  
读 chunk 2：
  - 找 D2（与 D1 比）
  - 如果 D2 > D1：
    - S1 需要修正：S1 × exp(D1 - D2)
    - 这样 S1 就变成 "以 D2 为 Amax" 的值
  - 算新 chunk 的 Σ exp(Ai - D2)
  - S2 = 修正后的 S1 + 新 chunk 的和
  
继续...
```

**关键公式（修正）：**
```
S_new = S_old × exp(D_old - D_new) + Σ exp(Ai - D_new)
```

这样，**读一次 chunk 就能更新 Amax 和分母**，不需要多次读写！

### 5.2 结果
- 从 **多次读写** 变成 **2次读写**
- 第1次：找 Amax 和分母
- 第2次：计算 Â

---

## 6. 真正的 Flash Attention：一步到位

### 6.1 灵魂拷问
> 一定要算出 attention weight Â 才能计算 weighted sum O 吗？

**Flash Attention 的答案：不需要！可以直接得到 O！**

### 6.2 核心思想
Q、K、V 放到工作台后，**一次运算得到最终结果 O**

### 6.3 计算流程

**第1个 chunk：**
```
读 Q, K1-N, V1-N
算 dot product → 找 D1（最大值）
算 S1 = Σ exp(Ai - D1)
直接算 O1 = Σ [exp(Ai - D1) / S1] × Vi   ← 注意：这是错的 attention weight！
```

> O1 是用错误的 weight 算的（D1 不是真正的 Amax，S1 不是真正的分母）

**第2个 chunk：**
```
读 K_{N+1}-K_{2N}, V_{N+1}-V_{2N}
找 D2（与 D1 比）
修正 S1：S1 × exp(D1 - D2)
算新 chunk 的 Σ exp(Ai - D2)
S2 = 修正后的 S1 + 新 chunk 的和

修正 O1：
  O1_new = O1 × (S1/S2) × exp(D1 - D2)
  
算新 chunk 的 weighted sum：
  O2_chunk = Σ [exp(Ai - D2) / S2] × Vi
  
O2 = O1_new + O2_chunk
```

**第 k 个 chunk：**
```
读 K, V
找 Dk（与 D_{k-1} 比）
修正 S_{k-1}：S_{k-1} × exp(D_{k-1} - Dk)
算新 chunk 的和
Sk = 修正后的 S_{k-1} + 新 chunk

修正 O_{k-1}：
  O_{k-1}_new = O_{k-1} × (S_{k-1}/Sk) × exp(D_{k-1} - Dk)
  
算新 chunk 的 weighted sum
Ok = O_{k-1}_new + 新 chunk 的 sum
```

### 6.4 最终结果
- 经过 B 个 chunk 后，得到 OB
- **OB = Σ (正确的 attention weight) × Vi**
- **Â 从未被真正计算出来！**

**神奇之处：**
- 中间过程一直在"犯错"（用错误的 Amax 和分母）
- 但每次都在**修正前面的错误**
- 最终结果是**完全正确的**

### 6.5 特性
- 用 Hugging Face 时，如果选 Flash Attention，**读不出 attention weight**
- 因为 Â 从未被显式计算

---

## 7. 实验对比

### 7.1 Toy Example（假 QKV）

**环境：** A100 80GB（仓库 80GB，工作台只有十几 MB）

**结果：**

| Sequence 长度 | Naive Attention | Flash Attention | 加速比 |
|-------------|-----------------|-----------------|-------|
| 64-4096 | - | - | **最高 9 倍** |

**数值精度：**
- Flash Attention 与 Naive Attention 结果差异：~10^-7
- 几乎一样，差异来自不同运算机制

### 7.2 真实模型（Yi-34B）

**短 sequence（7300 tokens）：**
- Naive: 0.15 秒
- Flash: 没快多少
- 原因：sequence 太短，Flash Attention 优势不明显；模型还有其他部分（FFN、embedding 等）也花时间

**长 sequence（7万 tokens）：**
- Naive: 2 秒
- Flash: 1.3 秒
- **明显加速**

**超长 sequence（73万 tokens）：**
- Naive: **CUDA Out of Memory**
- 原因：仓库被撑爆
- 这就是下一堂课 KV Cache 要解决的问题

---

## 8. Flash Attention 总结

| 特性 | 说明 |
|------|------|
| **不改变结果** | 计算结果与标准 Attention 理论上一致 |
| **随插即用** | 可套用到任何 Transformer 模型 |
| **核心思想** | 减少数据搬运次数（HBM ↔ SRAM） |
| **代价** | 算法复杂、额外计算（修正项） |
| **实际效果** | sequence 越长，加速越明显（最高 9 倍） |
| **副作用** | 读不出 attention weight（Â 从未被显式计算） |

### 8.1 关键技巧回顾

1. **Softmax 修正：**
   ```
   S_new = S_old × exp(D_old - D_new) + Σ exp(Ai - D_new)
   ```

2. **Output 修正：**
   ```
   O_new = O_old × (S_old/S_new) × exp(D_old - D_new) + 新 chunk 的 weighted sum
   ```

3. **一步到位：**
   - 不需要显式计算 Â
   - 直接得到正确的 O

### 8.2 使用方式

**PyTorch：**
```python
# 使用 Flash Attention（默认）
torch.nn.functional.scaled_dot_product_attention(Q, K, V)

# 禁用 Flash Attention（用 eager/naive）
torch.nn.functional.scaled_dot_product_attention(Q, K, V, attn_mask=None, dropout_p=0.0, is_causal=True, enable_math=True)
```

**Hugging Face：**
```python
# 不用 Flash Attention
model = pipeline("text-generation", model="model_name", attn_implementation="eager")

# 用 Flash Attention（默认）
model = pipeline("text-generation", model="model_name", attn_implementation="sdpa")
```

---

## 9. 与其他加速方法的对比

| 方法 | 是否改变 Attention | 是否需要训练 | 额外代价 |
|------|-------------------|------------|---------|
| **Flash Attention** | 否 | 否 | 算法复杂、少量额外计算 |
| **KV Cache** | 否 | 否 | 占用内存 |
| **GQA/MQA** | 是 | 是 | 可能降低模型能力 |
| **Sliding Window** | 是 | 可选 | 看的范围减少 |
| **Speculative Decoding** | 否 | 否 | 需要额外小模型 |

---

## 10. 关键洞察

### 10.1 为什么 Flash Attention 快？
- 不是减少了计算量
- 而是**减少了数据搬运**（HBM ↔ SRAM）
- 数据搬运是 GPU 运算的瓶颈

### 10.2 为什么需要修正？
- 每次假设当前 chunk 的最大值就是 Amax（是错的）
- 但发现更大的值时，**修正前面的错误**
- 通过指数项的乘法，把"旧 Amax"的痕迹抹掉，换成"新 Amax"

### 10.3 数学原理
```
exp(Ai - D_old) × exp(D_old - D_new) = exp(Ai - D_new)
```
- 分子分母同时调整，保持比例不变
- 最终结果是正确的

---

## 11. 参考资料

- Flash Attention 原始论文（2022）
- 助教讲解和作业中有更详细的说明
- PyTorch 文档：`torch.nn.functional.scaled_dot_product_attention`

---

*本笔记完整记录了李宏毅教授 Flash Attention 课程的所有细节，包括算法流程、数学推导、代码示例和实验结果。*
