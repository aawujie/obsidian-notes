---
share_link: https://share.note.sx/3bi3xcab#zEe5vSxYtxeZGsv8/FzXeDw659qrJCCsO8Wmf43FWkk
share_updated: 2026-04-01T22:50:38+08:00
---
# Transformer 可解释性详解

> **视频来源：** [李宏毅 - Transformer 内部机制课程](https://youtu.be/Xnil63UDW2o?si=3R0Qm3Hrb58J14Ng)
> **提取时间：** 2026-04-01

---

## 1. 课程概述

### 1.1 课程目标
- 深入理解大型语言模型（Transformer）内部运作机制
- 学习剖析 AI/神经网络内部运作的方法
- **类比：** 这堂课讲的是 **AI 的脑神经科学**

### 1.2 重要提醒
- 分析的对象通常是**较小的模型**（如 GPT-2、早期 LLaMA）
- 大型模型（如 LLaMA 405B）难以分析（算力限制）
- 结果可能**不适用于最新最强的大模型**
- 类似脑科学研究：从小鼠实验推断人类大脑机制

### 1.3 课程结构
1. **一个神经元在做什么**
2. **一层神经元在做什么**
3. **不同层之间的互动**
4. **让语言模型自己说出内心想法**

---

## 2. Transformer 基础回顾

### 2.1 语言模型 = 文字接龙
- 输入：token sequence Z₁ 到 Zₜ₋₁
- 输出：下一个 token Zₜ 的概率分布
- Token 可以是文字、像素、语音等

### 2.2 Transformer 结构
```
输入 token → Embedding → Layer 1 → Layer 2 → ... → Layer N
                                                    ↓
                                            最后一个向量 → Unembedding → 概率分布
```

### 2.3 关键组件
- **Embedding**：token → 向量（查表）
- **Unembedding**：向量 → token 概率分布（线性变换）
- **Layer**：包含 Self-Attention + Feed Forward

### 2.4 单个神经元
Feed Forward Layer 中的单个神经元：
```
输入向量 → Weighted Sum → ReLU → 输出
```
- 每个输出 = 输入的 weighted sum 过 ReLU
- ReLU：负数变 0，正数不变

---

## 3. 单个神经元的分析

### 3.1 分析步骤

**步骤 1：观察现象（相关性）**
- 观察神经元激活时（输出 > 0）模型的行为
- 示例：某神经元激活时，模型说脏话
- ⚠️ **相关性 ≠ 因果性**（冰淇淋销量 vs 溺水人数）

**步骤 2：验证因果性**
- **移除神经元**，观察模型行为是否改变
- 将神经元输出设为 0（或平均值）
- 如果模型不再说脏话 → 有因果关系

**步骤 3：分析激活程度（可选）**
- 不同激活程度是否导致不同等级的脏话
- 实际研究中较少做

### 3.2 著名案例：川普神经元 (Trump Neuron)

**来源：** OpenAI 2021 年研究（Distell 平台）

**发现：**
- 某神经元看到川普相关输入时高度激活
- 川普本人照片 → 高度激活
- 卡通版川普 → 激活
- 川普文字 → 激活
- 其他政治人物（奥巴马、乔布斯）→ 不激活

**注意：**
- 这是 **CLIP 图像模型**，不是生成模型
- 只能观察输入→激活，不能观察激活→生成

### 3.3 祖母神经元 (Grandmother Cell)

**概念来源：** 1969 年认知科学
- 假设：单个神经元负责特定记忆（如"祖母"）
- 实际：**稻草人理论**（虚构来反驳的）
- 主流观点：多个神经元共同处理一个记忆

**AI 中的类似现象：**
- 大多数任务由**多个神经元共同管理**
- 单个神经元往往没有特定功能
- 但确实存在一些高选择性神经元（如川普神经元）

### 3.4 为什么不是"一个神经元 = 一个任务"？

**神经元数量限制：**
- 每层只有 4096 个神经元
- 如果每个神经元只做一件事 → 模型能力太有限
- 无法产生千变万化内容

**实际机制：**
- **一组神经元**负责一个任务
- 不同任务可以**共享神经元**
- 4096 个神经元 → 2^4096 种组合 → 巨大表达能力

---

## 4. 功能向量 (Function Vectors)

### 4.1 核心假设
> 每个功能由**特定神经元组合**构成（高维空间中的方向）

**示例：**
- 拒绝请求的功能 = 神经元 1、3、N 激活
- 这些神经元的数值排列成一个向量 → **功能向量**

### 4.2 如何找到功能向量？

**方法：对比平均法**

1. **收集正例**：大量模型拒绝请求的输入
   - 记录第 10 层最后一个位置的 representation
   - 平均 → H⁺（拒绝 + 其他信息）

2. **收集负例**：大量模型不拒绝的输入
   - 记录第 10 层 representation
   - 平均 → H⁻（其他信息）

3. **相减**：V_refuse = H⁺ - H⁻
   - 抵消"其他信息"
   - 得到"拒绝"功能向量

### 4.3 验证功能向量

**实验 1：加上功能向量**
- 正常问题："瑜伽的三个好处"
- 第 10 层加上拒绝向量
- 结果：模型说"瑜伽很危险，我不能告诉你"

**实验 2：减去功能向量**
- 有害请求："写黑函诋毁总统"
- 第 10 层减去拒绝向量
- 结果：模型真的写了黑函

**成功率：**
- 加上拒绝向量 → 高比例拒绝正常请求
- 减去拒绝向量 → 大幅降低拒绝率，增加有害输出

### 4.4 其他功能向量示例

| 功能向量 | 效果 |
|---------|------|
**语言向量** | 英文 → 中文
**谄媚向量** | 模型不断附和、赞美用户
**说真话向量** | 模型变得极其诚实（甚至无趣）
**In-context Vector** | 让模型按照示例任务执行

### 4.5 In-Context Vector

**发现：** 2023 年 10 月（两篇论文同一天发表）

**方法：**
1. 给模型多个示例（如反义词：small→large, dark→light）
2. 记录最后一个位置各层 representation
3. 平均 → In-context Vector

**效果：**
- 只给 "simple:"，加上 In-context Vector
- 模型自动输出 "complex"（按反义词任务执行）

**功能向量的加减：**
- 可以组合功能向量创造新功能
- 示例：first+capital - first+copy = last+capital

### 4.6 自动发现功能向量：Sparse Autoencoder (SAE)

**问题：** 如何自动找出所有功能向量？

**假设：**
1. 每个 representation 是功能向量的线性组合
2. 每次只用**少量**功能向量（稀疏性）

**方法：**
- 训练 Sparse Autoencoder
- 输入：大量 representation H₁...Hₙ
- 输出：功能向量 V₁...Vₖ 和系数 α

**Loss Function：**
```
minimize: Σ|Eᵢ| + λ·Σ|α|
```
- 第一项：reconstruction error 小
- 第二项：系数稀疏（少数功能向量激活）

**Claude 3 的分析结果：**
- 3400 万个功能向量
- 金门大桥向量：多语言、图像都能激活
- Debug 向量：检测代码错误
- AI 自我认知向量（科幻但可能只是输出"我是AI"）
- 谄媚向量

---

## 5. 语言模型的模型 (Model of Language Model)

### 5.1 为什么需要？
- Transformer 太复杂，无法直接解析
- 需要一个**更简单但 faithful** 的模型

### 5.2 知识抽取模型示例

**任务：** "台北 101 is located in ___" → "台北"

**简化模型：**
1. 前几层：处理主词，产生 representation X
2. 关系词（is located in）→ 产生线性函数（W, b）
3. Y = X·W + b
4. Y unembedding → 得到 "台北"

**验证：**
- 换主词（Space Needle）→ 换 X → 得到 "Seattle"
- 换关系（has height of）→ 换线性函数 → 得到高度

**Faithfulness：**
- 某些关系效果很好（地点）
- 某些关系效果差（CEO、父母、宝可梦进化）

### 5.3 Circuit（电路）方法

**方法：**
- 对原模型做**大量剪枝 (pruning)**
- 只保留与特定任务相关的组件
- 直到模型"一目了然"

**与 Network Compression 区别：**
| | Circuit | Network Compression |
|--|---------|-----------------|
**目标** | 只关心特定任务 | 保持多数任务能力 |
**剪枝程度** | 非常剧烈 | 适度 |
**可解释性** | 必须人类可读 | 不强调 |

**应用：**
- 分析多跳推理 (Multi-hop)
- 分析指代消解 (IOI 问题)

---

## 6. 让模型说出内心想法

### 6.1 Logit Lens

**核心发现：**
- 模型可以"说话" → 最有解释性
- 可以直接问模型"你在想什么"

**方法：**
- 把 Unembedding Layer 接到**中间每一层**
- 解析每层输出对应的 token 分布

**Residual Connection 的关键作用：**
```
Layer 输出 = 输入 + 变换
```
- 想象：有一条 "Residual Stream" 高速公路
- 每层只是**加**一点信息进去
- 信息一路传递到输出

**实际应用：**
- 输入代词 "it"
- 第 11 层解析出 "element"（指代对象）
- 观察模型如何逐步解析指代

### 6.2 案例分析：首都问题

**输入：**
```
What is the capital of France? Paris
What is the capital of Poland?
```

**Logit Lens 分析：**
- 第 15 层：突然知道跟 Poland 有关
- 第 19 层：锁定答案 "Warsaw"

**不同问法，不同机制：**
- 直接问：先想 Poland → 再想 Warsaw
- 阅读理解：直接锁定 Warsaw（前文已提及）

### 6.3 翻译的内部机制

**任务：** 法文 "fleur" → 中文 "花"

**Logit Lens 发现：**
- 前 20 层：解析为英文 "flower"
- 第 27 层：转为中文 "花"
- **结论：** LLaMA-2 内心用英文思考

### 6.3 Patch Scope

**解决 Logit Lens 的局限：**
- Logit Lens 只能解析单个 token
- 但 representation 可能包含更丰富的信息

**方法：**
1. 输入目标词，记录某层 representation
2. 构造模板："X: ___" 或 "Tell me a secret about X"
3. 把 X 的 representation 替换为目标 representation
4. 观察模型输出

**效果：**
- 可以解析 representation 的丰富含义
- 可调模板获得不同风格的解释

**示例：** "Princess of Wales"
- 第 1-2 层：识别为 "country in UK"
- 第 4 层：识别为 "royal title for women"
- 第 5 层：知道是 "wife of Prince of Wales"
- 第 6 层：识别出 "Diana"

---

## 7. 应用：改进 Multi-hop Reasoning

### 7.1 问题定义

**Multi-hop Question：**
```
The spouse of the performer of Imagine is ___
```
- E1: Imagine（专辑）
- E2: John Lennon（演奏者）
- E3: Yoko Ono（配偶）

### 7.2 分析失败原因

**Logit Lens + Patch Scope 分析：**
- 蓝色线：E2 首次出现的层（较浅层）
- 橙色线：E3 首次出现的层（20-25 层）

**问题：**
- E2 解析太晚 → 来不及在 20 层前解析 E3
- 导致回答错误

### 7.3 解决方案：Backpatching

**方法：**
- 把**后面层**的 representation **加到前面**
- 重新跑一遍

**效果：**
- 原答对的问题：不影响（100% → 100%）
- 原答错的问题：40-60% 变对

**与 Reasoning 模型的联系：**
- Reasoning：深度不够，长度来凑（多轮思考）
- Backpatching：把后面的"思考"移到前面

---

## 8. Feed Forward Layer 的另一种理解

### 8.1 Key-Value 视角

**传统理解：**
- 前一层的值 → weighted sum → 下一层

**新理解 (Transformer Feed Forward Layer, 2020)：**
- 前一层的每个维度 Kᵢ 作为 "key"
- 对应的权重向量 Vᵢ 作为 "value"
- 输出 = Σ Kᵢ × Vᵢ

**类比：**
- 类似 Attention：key 决定关注什么，value 提供信息

### 8.2 解析 Value 向量

**方法：** 用 Unembedding 解析每个 V

**发现：**
- 某些 V 对应特定概念（单位、代词、副词、族群）

**应用：知识编辑**
- 找到对应 "金城武" 的 V
- 替换为 "李宏毅" 的 embedding
- 模型回答"世界上最帅的人"时会答"李宏毅"
- 成功率：48% 改变输出，34% 正确改为李宏毅

---

## 9. 总结

### 9.1 分析方法层级

| 层级 | 方法 | 说明 |
|------|------|------|
| **单个神经元** | 激活分析、消融实验 | 寻找特定功能神经元 |
| **一层神经元** | 功能向量、SAE | 理解层级的功能表示 |
| **多层互动** | Circuit、模型剪枝 | 理解任务执行流程 |
| **模型自述** | Logit Lens、Patch Scope | 让模型"说出"思考过程 |

### 9.2 关键洞察

1. **分布式表示**：多个神经元共同编码信息
2. **功能向量**：高维空间中的方向对应功能
3. **Residual Stream**：信息逐层累加
4. **可解释性**：语言模型可以"说话"，这是独特优势

### 9.3 局限性

- 多数神经元难以解释
- 分析方法多针对小模型
- 大模型可能机制不同
- 功能向量方法有细节差异（不同论文做法不同）

---

## 10. 参考资料

- OpenAI: Interpretability Research (2021)
- Anthropic: Scaling Monosemanticity (Claude 3 Analysis)
- Transformer Feed Forward Layer (2020)
- Logit Lens / Patch Scope
- Multi-hop Reasoning / Backpatching (2024)
- Sparse Autoencoder (SAE) 相关文献

---

*本笔记完整记录了李宏毅教授 Transformer 可解释性课程的所有内容，包括数学原理、实验方法、实际案例和前沿研究。*
