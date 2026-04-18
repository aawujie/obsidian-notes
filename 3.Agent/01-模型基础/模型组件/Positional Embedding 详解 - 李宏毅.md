# Positional Embedding 详解

> **视频来源：** [李宏毅 - Positional Embedding 课程](https://youtu.be/Ll-wk8x3G_g?si=uNDuxkEdNo_5QpSj)
> **提取时间：** 2026-04-01

---

## 1. 为什么需要 Positional Embedding？

### 1.1 Self-Attention 的问题

**核心问题：Self-Attention 本身没有位置信息**

Transformer 的输入处理流程：
1. Token → Embedding（变成向量）
2. Embedding 输入到 Layer
3. Layer 中的 Self-Attention 处理

**Self-Attention 计算过程（以第4个位置为例）：**
- XA, XB, XC, XD → QA, KA, VA, QB, KB, VB...
- QD 与 KA, KB, KC, KD 算 dot product → Attention Weights
- Softmax 归一化
- Weighted Sum of VA, VB, VC, VD → OD

**关键发现：**
> 交换 A 和 C 的位置（ABCD → CBAD），OD 的输出**完全一样**

因为 weighted sum 是加法，顺序不影响结果。

### 1.2 造成的严重问题

**示例：**
- "你打我" vs "我打你"
- 最后一个位置的 embedding 计算结果相同
- 模型**无法分辨**这两个句子的差异

**结论：** 必须给 Transformer 提供**位置信息**

---

## 2. Absolute Positional Embedding（绝对位置编码）

### 2.1 基本思想

为每个位置设计一个特殊的 Embedding，加到 Token Embedding 上：

$$\text{位置 } 0: \mathbf{P}_0, \quad \text{位置 } 1: \mathbf{P}_1, \quad \text{位置 } 2: \mathbf{P}_2, \ldots$$

**效果：**
- ABCD: A+P0, B+P1, C+P2, D+P3
- CBAD: C+P0, B+P1, A+P2, D+P3
- 同样的 Token 在不同位置 → 不同的输入 → 不同的输出

### 2.2 Sinusoidal Positional Embedding

**Transformer 原始论文使用的方法（2017年）**

**公式：**

对于位置 $k$ 的 Positional Embedding 的第 $i$ 个维度：

$$\text{PE}(k, 2i) = \sin\left(\frac{k}{10000^{2i/d}}\right)$$

$$\text{PE}(k, 2i+1) = \cos\left(\frac{k}{10000^{2i/d}}\right)$$

其中：
- $d$ = Embedding 维度（如 128, 256）
- $i = 0, 1, 2, \ldots, d/2-1$
- $k$ = 位置编号

### 2.3 Sinusoidal 的可视化理解

**每一对维度（2i, 2i+1）看作一个二维指针：**
- 偶数位：sin → y 坐标
- 奇数位：cos → x 坐标
- 合起来：二维平面上的旋转指针

**不同维度的旋转速度不同：**
- 前面的维度（i 小）：转得快（高频）
- 后面的维度（i 大）：转得慢（低频）

**示例（d=128）：**
- i=0: 周期 ≈ 6.3（转得最快）
- i=32: 周期 ≈ 628
- i=63: 周期 ≈ 54000（转得最慢）

**比喻：64个不同转速的指针（秒针、分针、时针...）**

### 2.4 Sinusoidal 的特殊性质

**核心性质：相对位置可计算**

$$\mathbf{P}(k+r) = \mathbf{M}_r \times \mathbf{P}(k)$$

<span style="color:rgb(255, 77, 77)"><b>$\mathbf{M}_r$ 只与相对距离 $r$ 有关，与绝对位置 $k$ 无关。</b></span>

**数学推导（使用三角函数合角公式）：**

$$\sin(A+B) = \sin A \cdot \cos B + \cos A \cdot \sin B$$

$$\cos(A+B) = \cos A \cdot \cos B - \sin A \cdot \sin B$$

因此：

$$\mathbf{P}(k+r) = \begin{bmatrix} \sin\frac{k+r}{Z} \\ \cos\frac{k+r}{Z} \end{bmatrix} = \begin{bmatrix} \sin\frac{k}{Z}\cos\frac{r}{Z} + \cos\frac{k}{Z}\sin\frac{r}{Z} \\ \cos\frac{k}{Z}\cos\frac{r}{Z} - \sin\frac{k}{Z}\sin\frac{r}{Z} \end{bmatrix} = \mathbf{R}(r) \cdot \mathbf{P}(k)$$

**对 Attention 的影响：**

Attention 计算可以分解为：

$$A = (\mathbf{x}_B + \mathbf{P}_N)^T \mathbf{W}_Q^T \mathbf{W}_K (\mathbf{x}_A + \mathbf{P}_M) = \text{内容项} + \text{位置-内容交叉项} + \text{位置项}$$

位置项通过 Sinusoidal 的性质，可以转化为只与相对位置有关的项。

---

## 3. Relative Positional Embedding（相对位置编码）

### 3.1 ALiBi (Attention with Linear Biases)

**2021年，非常简单但有效的方法**

**核心思想：**
> 直接在 Attention Score 上减去一个与距离成正比的偏置

$$A = \mathbf{Q} \cdot \mathbf{K}^T - B \times |m - n|$$

- $B$：手动设置的常数（如 0.5, 1）
- $|m-n|$：两个位置的相对距离
- 效果：距离越远，Attention 越小

**特点：**
- 不需要训练
- 可以外推到训练时没见过的长度
- 不同 Head 可以设置不同的 B

**实验结果：**
- 只在 512 token 上训练
- 可以处理更长的 sequence
- 全面碾压 Sinusoidal 方法

### 3.2 T5 的 Learnable Relative Bias

**2019年**

$$A = \mathbf{Q} \cdot \mathbf{K}^T - \text{Bias}(|m-n|)$$

- Bias 是通过训练学习得到的
- 将距离分段（0-5, 5-10, 10-20, >20...）
- 每段学习一个固定的 bias 值

**结果：** 不如 ALiBi

---

## 4. RoPE (Rotary Positional Embedding)

### 4.1 核心思想

**旋转位置编码**

在 Q 和 K 做 dot product **之前**，先把位置信息通过**旋转**加到 Q 和 K 上：

$$\mathbf{Q}^N = \text{RoPE}(\mathbf{Q}, N), \quad \mathbf{K}^M = \text{RoPE}(\mathbf{K}, M)$$

$$A = \mathbf{Q}^N \cdot \mathbf{K}^M$$

### 4.2 具体实现

**每两个维度一组，进行旋转：**

对于第 $(2i, 2i+1)$ 维：

$$\begin{bmatrix} x_{2i}' \\ x_{2i+1}' \end{bmatrix} = \begin{bmatrix} \cos(N \cdot \theta_i) & -\sin(N \cdot \theta_i) \\ \sin(N \cdot \theta_i) & \cos(N \cdot \theta_i) \end{bmatrix} \begin{bmatrix} x_{2i} \\ x_{2i+1} \end{bmatrix}$$

**旋转角度 $\theta_i$ 的设置（与 Sinusoidal 类似）：**

$$\theta_i = \frac{1}{10000^{2i/d}}$$

### 4.3 RoPE 的关键性质

**性质1：相对位置等价性**

$$\mathbf{Q}^N \cdot \mathbf{K}^M = \mathbf{Q} \cdot \mathbf{R}(M-N) \cdot \mathbf{K}$$

其中 $\mathbf{R}(M-N)$ 是只与相对距离有关的旋转矩阵。

**性质2：与 Flash Attention、KV Cache 兼容**
- 计算流程与标准 Attention 完全一致
- 只是 Q 和 K 被旋转了
- 可以直接套用各种 Attention 优化方法

**性质3：没有距离衰减保证**
- 不像 ALiBi 保证距离越远 Attention 越小
- 可以学习复杂的 Attention 模式（如跳过前一个 token，直接 attend 前两个）

### 4.4 RoPE vs ALiBi

| 特性 | RoPE | ALiBi |
|------|------|-------|
| 距离衰减 | ❌ 不保证 | ✅ 保证 |
| 复杂模式 | ✅ 可以学习 | ❌ 简单线性 |
| 训练稳定性 | 需要更多训练 | 简单直接 |
| 与优化兼容 | ✅ 完美兼容 | 需要修改 Attention |

**实际应用：**
- LLaMA、Qwen、Gemma 等主流模型都用 RoPE
- 历史选择了 RoPE（虽然 ALiBi 在某些实验上更好）

---

## 5. Train Short, Test Long

### 5.1 问题定义

**目标：**
- 训练时只看短 sequence（如 512 token）
- 测试时能处理长 sequence（如 2048, 4096...）

**为什么重要：**
- 训练长 sequence 成本高
- 实际应用需要处理长文本（如 AI Agent 持续运行）

### 5.2 不同方法的表现

| 方法 | Train Short Test Long |
|------|---------------------|
| Sinusoidal | ❌ 很快崩坏 |
| RoPE | ❌ 逐渐崩坏 |
| T5 Learnable | ❌ 逐渐崩坏 |
| **ALiBi** | ✅ **可以支撑** |

**ALiBi 的优势：** 人工设计的规则，对长度外推更 robust

### 5.3 RoPE 的扩展方法

#### 方法1：Position Interpolation（位置插值）

**思想：**
- 训练时最大位置 N
- 测试时 sequence 长度 L×N
- 把位置编号除以 L：1, 2, 3... → 0.5, 1, 1.5...

**问题：**
- 需要 fine-tune 才能适应小数位置
- 不 fine-tune 表现不好

#### 方法2：NTK-aware Scaling（频率感知缩放）

**来源：** Reddit 帖子（没有正式论文）

**核心思想：**
- 不同频率的维度，做不同的缩放
- 高频维度（转得快）：不缩放（scale=1）
- 低频维度（转得慢）：用 Position Interpolation（scale=1/L）

**公式：**

$$\text{scale}(i) = L^{-2i/d}$$

**效果：**
- 不需要 fine-tune 也有不错效果
- 可以处理 2-4 倍长度的 sequence

#### 方法3：YARN

**Yet Another RoPE Extension Method**

**改进 NTK-aware：**
- 保留更多高频维度不变
- 保留更多低频维度用插值
- 比 NTK-aware 效果更好

#### 方法4：Dynamic Scaling（动态缩放）

**思想：**
- 根据输入长度动态决定缩放方式
- 短 sequence：用原位置
- 长 sequence：做 interpolation

**问题：**
- 会破坏 KV Cache（不同长度用不同位置编码，缓存失效）
- 实际使用较少

#### 方法5：LongRoPE

**当前最强方法**

**特点：**
- 结合 frequency-based + dynamic scaling
- 用 evolutionary search 搜索最佳参数
- 可以处理 2M（200万）token
- 可以读完整套哈利波特还有剩

**流程：**
1. 先 fine-tune 扩展到某长度
2. 再用 LongRoPE 扩展一次
3. 再扩展一次
4. 最终达到 2M

---

## 6. 真的需要 Positional Embedding 吗？

### 6.1 NoPE (No Positional Embedding)

**2023年的论文**

**核心发现：**
> 多层 Self-Attention 本身就有位置信息！

**示例：**
- "猫吃鱼" vs "鱼吃猫"
- 第一层：没有位置信息，确实无法区分
- 第二层：
  - 位置2的 embedding 综合了"猫+吃"
  - 位置3的 embedding 综合了"吃+鱼"
  - 即使交换，第二层的输入已经不同

**实验结果（Toy Task）：**
- Copy 任务：NoPE 表现最好
- 可以外推到训练时没见过的长度

### 6.2 为什么主流模型还用 RoPE？

**关键区别：训练过程**

实验对比（训练时的 Loss）：
- RoPE：Loss 低
- NoPE：Loss 高

**结论：**
- Self-Attention 本身确实有位置信息
- 但**训练时需要**显式的 Positional Embedding 来帮助学习
- 训练收敛后，位置信息已经内化

### 6.3 DroPE (Drop Positional Embedding)

**思想：**
> 训练时用 RoPE，训练快结束时丢掉

**流程：**
1. 前 90% 训练：用 RoPE
2. 最后 10% 训练：去掉 RoPE
3. 推理时：没有 Positional Embedding

**效果：**
- 可以处理更长的 sequence
- 不受 Positional Embedding 的长度限制

**佛经比喻：**
> "如筏喻者，法尚应舍，何况非法"
> 
> Positional Embedding 就像渡河的船，到了对岸就要放下。

---

## 7. 方法总结对比

| 方法 | 类型 | 核心思想 | 优点 | 缺点 | 代表模型 |
|------|------|---------|------|------|---------|
| **Sinusoidal** | Absolute | 正弦函数编码 | 有相对位置性质 | 长序列崩坏 | 原始 Transformer |
| **ALiBi** | Relative | Attention 减距离偏置 | 简单、外推好 | 过于简单 | 部分实验模型 |
| **T5 Bias** | Relative | 学习距离偏置 | 可学习 | 不如 ALiBi | T5 |
| **RoPE** | Rotary | 旋转编码 | 与优化兼容、效果好 | 需要扩展方法 | LLaMA, Qwen, Gemma |
| **NoPE** | None | 不用位置编码 | 无长度限制 | 训练困难 | 实验性 |
| **DroPE** | Hybrid | 训练时用，结束丢掉 | 两全其美 | 训练复杂 | 实验性 |

### RoPE 扩展方法对比

| 方法 | 核心思想 | 需要 Fine-tune | 效果 |
|------|---------|----------------|------|
| Position Interpolation | 统一缩放位置 | ✅ 需要 | 一般 |
| NTK-aware | 频率感知缩放 | ❌ 不需要 | 好 |
| YARN | 改进 NTK | ❌ 不需要 | 更好 |
| Dynamic Scaling | 根据长度动态调整 | ❌ 不需要 | 好，但破坏 KV Cache |
| LongRoPE | 综合优化 | ✅ 需要 | 最好（2M）|

---

## 8. 关键洞察

### 8.1 相对位置 vs 绝对位置

**绝对位置：** 知道"我在第100个位置"
**相对位置：** 知道"我距离某个 token 有5个位置"

**实际更重要的是相对位置！**
- "猫吃了鱼"中，"猫"和"鱼"的关系不因前面加1000个 token 而改变
- 但距离太远时，Attention 应该变小

### 8.2 高频 vs 低频维度

**高频（转得快）：**
- 训练时已经看过各种角度
- 外推时不怕新角度

**低频（转得慢）：**
- 训练时只看过小范围角度
- 外推时容易遇到没见过的角度 → 崩坏

**扩展策略：** 主要保护低频维度

### 8.3 训练 vs 推理的区别

**训练时需要 Positional Embedding：**
- 帮助模型更快学习
- 提供明确的位置信号

**推理时可能不需要：**
- 多层 Attention 已经学到位置信息
- 去掉后可以处理任意长度

---

## 9. 参考资料

- Transformer 原始论文 (2017)
- ALiBi 论文 (2021)
- RoPE 论文 (2021)
- NoPE 论文 (2023)
- LongRoPE 论文 (2024)
- NTK-aware Scaling (Reddit)
- YARN 论文

---

*本笔记完整记录了李宏毅教授 Positional Embedding 课程的所有内容，包括数学推导、可视化解释、方法对比和代码实现思路。*
