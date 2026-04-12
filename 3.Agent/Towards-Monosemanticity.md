# Towards Monosemanticity: Decomposing Language Models With Dictionary Learning

**来源**: Anthropic Transformer Circuits Thread  
**发表日期**: 2023 年 10 月 4 日  
**作者**: Trenton Bricken, Adly Templeton, Joshua Batson, Brian Chen, Adam Jermyn, Tom Conerly, Nick Turner, Cem Anil, Carson Denison, Amanda Askell, Robert Lasenby, Yifan Wu, Shauna Kravec, Nicholas Schiefer, Tim Maxwell, Nicholas Joseph, Alex Tamkin, Karina Nguyen, Brayden McLean, Josiah E Burke, Tristan Hume, Shan Carter, Tom Henighan, Chris Olah  
**链接**: https://transformer-circuits.pub/2023/monosemantic-features/index.html  
**最后更新**: 2026-04-12

---

## 📋 核心摘要

这篇论文使用**稀疏自编码器（Sparse Autoencoder）** 从单层 Transformer 中提取了大量可解释的特征。研究团队训练了 90 个不同规模的字典学习模型，从 512 个特征（1×扩展）到 131,072 个特征（256×扩展），重点分析了 A/1 运行中的 4,096 个特征。

**核心发现**：
- ✅ 特征比神经元更具可解释性（中位数评分 12 vs 0）
- ✅ 发现了跨模型的**普遍性特征**（如 base64、阿拉伯语、DNA 特征）
- ✅ 观察到**特征分裂**现象：更细粒度的字典学习会揭示更具体的特征
- ✅ 特征可以形成**有限状态自动机**式的系统，实现复杂行为
- ✅ 79% 的 MLP 层损失贡献可由特征解释（A/1 运行）

---

## 🔬 研究背景

### 问题：多语义性（Polysemanticity）

神经元通常是多语义的——单个神经元对看似无关的输入混合物产生响应。例如：
- 在 Inception v1 中，单个神经元同时响应**猫脸**和**汽车前部**
- 在研究的一层模型中，单个神经元响应**学术引用、英语对话、HTTP 请求、韩语文本**的混合

### 原因：叠加状态（Superposition）

叠加状态假说认为，神经网络通过为每个特征分配神经元的线性组合，来表示比神经元数量更多的独立 "特征"。

**三个解决策略**（来自 Toy Models of Superposition）：
1. 创建无叠加状态的模型（如鼓励激活稀疏性）
2. 使用字典学习在显示叠加状态的模型中找到过完备特征基
3. 混合方法

本研究采用**策略 2**——稀疏自编码器作为弱字典学习算法。

---

## 🧪 实验设置

### 模型架构

| 组件         | Transformer           | 稀疏自编码器                    |
| ---------- | --------------------- | ------------------------- |
| **层数**     | 1 注意力层 + 1 MLP 层      | 1 隐藏层（ReLU）               |
| **MLP 大小** | 512 神经元               | 512（1×）~ 131,072（256×）    |
| **数据集**    | The Pile（100B tokens） | Transformer MLP 激活（8B 样本） |
| **损失函数**   | 自回归对数似然               | L2 重建 + L1 隐藏层激活惩罚        |

### 特征表示

特征分解公式：
$$\mathbf{x}^j \approx \mathbf{b} + \sum_i f_i(\mathbf{x}^j) \mathbf{d}_i$$

- $\mathbf{x}^j$：数据点 $j$ 的激活向量（长度 $d_{\text{MLP}}$）
- $f_i(\mathbf{x}^j)$：特征 $i$ 的激活值
- $\mathbf{d}_i$：特征方向（单位向量）
- $\mathbf{b}$：偏置

### 特征命名约定

例如 "A/1/2357"：
- **A**：模型 A（另有模型 B 用于普遍性研究）
- **1**：字典学习运行编号（A/0~A/5 形成固定 L1 系数、递增字典大小的序列）
- **2357**：该运行中的具体特征编号

---

## 🔍 详细特征分析

### 1️⃣ 阿拉伯脚本特征（A/1/3450）

**激活特性**：
- 响应阿拉伯语、波斯语、乌尔都语等使用阿拉伯脚本的文本
- 训练数据中阿拉伯文本仅占 0.13%，但占特征激活 token 的 81%
- 与阿拉伯脚本代理的 Pearson 相关性为 0.74

**下游效应**：
- 激活时增加阿拉伯字符 token 的预测概率
- 消融实验显示：关闭特征会伤害阿拉伯脚本 token 的预测

**非神经元对齐**：
- 最相关的神经元（A/neurons/489）响应多种非英语语言的混合
- 特征在神经元基中有 27 个系数≥0.1，且最大的 3 个系数为负

**普遍性**：
- 在模型 B 中找到高度相似的特征 B/1/1334（相关性 0.91）

---

### 2️⃣ DNA 特征（A/1/2937）

**激活特性**：
- 响应由 A/T/C/G 组成的大写 DNA 序列
- 与二值化 DNA 代理的 Pearson 相关性为 0.8
- 是建模 DNA 上下文的唯一特征

**下游效应**：
- Top logit 权重为 AGT、GCC 等核苷酸组合

**普遍性**：
- 模型 B 中的对应特征：B/1/3680（相关性 0.92）

---

### 3️⃣ Base64 特征（A/1/2357）

**激活特性**：
- 响应 base64 字符串（字符集 [a-zA-Z0-9+/]）
- 与代理的相关性为 0.38（代理过于宽泛）

**特征分裂现象**：
- A/0 中只有 1 个 base64 特征（A/0/45）
- A/1 中分裂为 3 个特征：
  - **A/1/2357**：优先响应 base64 字母
  - **A/1/2364**：优先响应 base64 数字
  - **A/1/1544**：响应编码 ASCII 文本的 base64 字符串

**普遍性**：
- 模型 B 中的对应特征：B/1/2165（相关性 0.85）
- 此前在 SoLU 模型中也观察到 base64 神经元

---

### 4️⃣ 希伯来语特征（A/1/416）

**激活特性**：
- 响应希伯来语文本（基于 Unicode 块识别）
- 与希伯来脚本代理的相关性为 0.55

**非神经元对齐**：
- 模型 A 中没有响应希伯来语的神经元

**普遍性**：
- 模型 B 中的对应特征：B/1/1901（相关性 0.92）

---

## 📊 全局分析

### 可解释性评估

#### 人工分析

**评分标准**（满分 14 分）：
- 置信度（0-3）
- 高激活 token 一致性（0-5）
- Logit 效应一致性（0-3）
- 效应大小分离度（0-1）
- 特异性（0-3）

**结果**：
- **特征中位数得分**：12 分（ confident, specific, consistent）
- **神经元中位数得分**：0 分（无法形成假设）
- 评估样本：412 个特征激活区间（162 个特征/神经元）

#### 自动化可解释性（Claude）

**激活预测**：
- 使用 60 个样本（9 tokens 每个）计算 Spearman 相关性
- 特征显著优于神经元

**Logit 权重预测**：
- 任务：判断未见过的 logit token 是否是特征预测的下一个 token
- **特征准确率**：74%
- **神经元准确率**：58%
- **随机猜测**：50%

---

### 模型解释度

**A/1 运行**：
- **79%** 的 MLP 层对数似然损失还原由特征解释
- 替换 MLP 激活为自编码器输出的额外损失仅为零消融 MLP 损失的 21%

**A/5 运行**（131,072 特征，L1=0.004）：
- **94.5%** 的对数似然损失还原

---

### 特征 vs 数据

**验证特征反映模型而非仅数据**：
1. **随机权重模型**：对随机权重模型进行字典学习，发现特征可解释性显著降低
2. **Logit 权重检查**：特征激活与下游效应一致
3. **特征消融**：关闭特征会降低相应 token 的预测
4. **固定特征采样**：人工设置高激活值会生成符合特征解释的文本

---

## 🎭 现象学（Phenomenology）

### 特征主题（Motifs）

1. **上下文特征**（Context Features）：如 DNA、base64
2. **上下文中的 Token 特征**（Token-in-Context）：如数学中的"the"（A/0/341）、HTML 中的"<"（A/0/20）
3. **Trigram 特征**：如预测 COVID-**19** 中的 19（A/2/12310）
4. **动作特征**（Action Features）：同时作为输入检测器和输出生成器

---

### 特征分裂（Feature Splitting）

**现象**：随着字典规模增大，特征会分裂成更细粒度的版本

**示例**：
- A/0（512 特征）→ A/1（4,096 特征）→ A/2（16,384 特征）
- Base64 特征：1 → 3 → 更多
- 数学/物理特征从粗粒度（"the"在数学文本）分裂为细粒度（"the"在机器学习 vs 抽象代数 vs 引力理论）

**几何解释**：
- 相似特征在字典空间中的向量夹角很小
- UMAP 可视化显示紧密聚类（base64、阿拉伯脚本等）

**猜想**：
- 存在理想化的"真实特征"集合
- 受限字典返回覆盖相似领域的近似特征
- 随着字典增大，观察到更细粒度的"真实特征"

---

### 看似 Bug 的特征

#### Bug 1：单 Token 特征

**现象**：某些特征仅激活单个 token（如字母 P）

**解释**：
- 实际是多个上下文特定的 P 特征在粗粒度字典中无法区分
- 细粒度字典中分裂为不同上下文的 P 特征（如 P 在 Pattern、P 在 Python 等）

#### Bug 2：单上下文的多个特征

**现象**：多个特征覆盖相似概念（如 3 个 base64 特征）

**解释**：
- 特征分裂的体现
- 不同特征处理 base64 的不同子类型（字母、数字、ASCII 编码文本）

---

### 有限状态自动机（Finite State Automata）

**现象**：特征通过 token 流相互作用，形成状态机式的系统

#### 示例 1：单节点自循环

Base64 特征增加 base64 合理 continuation（如 Qg、zA）的概率，这些 token 继续激活该特征。

#### 示例 2：双节点系统（All Caps Snake Case）

- **A/0/207**：激活于全大写文本 token
- **A/0/358**：激活于下划线
- 交替激活生成 `ARRAY_MAX_VALUE` 等变量名

#### 示例 3：Unicode 字符处理

Tamil Unicode 字符通常分裂为两个 token：
- 前缀特征（\xe0\xae 或 \xe0\xaf）：指定 Unicode 块
- 后缀特征（\xa3）：指定块内字符
- 两特征交替激活

#### 示例 4：HTML 状态机

- **A/0/20**：激活于开放标签，预测标签名
- **A/0/0**：激活于标签名，预测标签闭合
- **A/0/30**：激活于标签闭合，预测空白
- **A/0/494**：激活于空白，预测新标签开放

生成示例：`<div>\n\t\t<span>`

#### 示例 5：记忆特定短语

在特征数较多的运行中（如 A/4），观察到特征序列记忆标准法律语言：
`MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE`

---

### 普遍性（Universality）

#### 模型间比较（A vs B）

**激活相似性**：
- A/1 特征与 B/1 最相似特征的中位数激活相关性：**0.72**
- 神经元间中位数激活相关性：**0.46**

**Logit 权重相似性**：
- 通常低于激活相关性（由于"干扰权重"）
- 归因相似性（结合激活和效应）与激活相似性高度一致

#### 与文献比较

**相似特征**：
- **SoLU 模型**：base64 神经元、十六进制神经元、全大写神经元
- **Smith 等人**：德语检测器、标题大小写检测器、单 token 特征
- **Gurnee 等人**：质因数特征（A/4/22414）、法语特征（A/0/14）
- **Goh 等人**（多模态模型）：澳大利亚、加拿大、非洲、以色列 - 巴勒斯坦地区特征

---

## 💡 理论讨论

### 叠加状态理论的扩展

**各向同性叠加状态模型**（Toy Models）：
- 特征是离散的一维对象
- 特征方向大致均匀分布

**本研究的新发现**：
- 特征在高密度相关特征组中**聚类**
- 特征可能产生相似的"动作"（输出效应）
- 可能存在高维**特征流形**而非一维特征

### Token-in-Context 特征的真实性

**问题**：为何观察到数百个不同的"the"特征（如物理中的"the"vs 数学中的"the"）？

**两种假设**：
1. **字典学习偏差**：底层 Transformer 使用组合编码，字典学习产生局部编码
2. **真实局部编码**：Transformer 确实部分使用局部编码

**支持假设 2 的理由**：
- 局部编码允许更"锐利"的预测
- 组合编码会强制 logits 为独立特征的和

---

## 🔮 未来工作

1. **扩展稀疏自编码器**：
   - 应用到前沿模型的工程挑战
   - 100×扩展因子、10,000 宽度 MLP → 约 200 亿参数

2. **字典学习缩放定律**：
   - 理想扩展因子如何随模型增大而变化？
   - 所需数据量如何变化？

3. **识别好特征**：
   - 自动化可解释性的改进
   - 超越 MMCS、激活相似性、归因相似性的指标

4. **分析可扩展性**：
   - 从微观洞察到宏观理解
   - 发现更大规模结构

5. **算法改进**：
   - 变分自编码器
   - 超越 L1 的稀疏性促进技术
   - 注意力层的叠加状态研究

---

## 📈 关键指标

| 指标 | A/1（4,096 特征） | A/5（131,072 特征） |
|------|------------------|---------------------|
| **损失还原** | 79% | 94.5% |
| **人工可解释性中位数** | 12/14 | - |
| **自动化激活预测** | 显著优于神经元 | - |
| **Logit 预测准确率** | 74% | - |
| **死特征** | 168（4.1%） | - |
| **超低密度特征** | 292（7.1%） | - |

---

## 🎯 核心贡献

1. **存在性证明**：至少某些特征比神经元更具单语义性
2. **全局分析**：典型特征是可解释的，解释了 MLP 层的非平凡部分
3. **现象学发现**：特征分裂、普遍性、有限状态自动机
4. **工具与可视化**：发布 90 个字典的特征探索界面

---

## 🔗 相关资源

- **论文全文**: https://transformer-circuits.pub/2023/monosemantic-features/index.html
- **特征可视化**: https://transformer-circuits.pub/2023/monosemantic-features/vis/a1.html
- **Neel Nanda 复现**: https://www.alignmentforum.org/posts/fKuugaxt2XLTkASkk/open-source-replication-and-commentary-on-anthropic-s
- **Colab 教程**: https://colab.research.google.com/drive/1u8larhpxy8w4mMsJiSBddNOzFGj7_RTn

---

## 📝 引用

```bibtex
@article{bricken2023monosemanticity,
  title={Towards Monosemanticity: Decomposing Language Models With Dictionary Learning},
  author={Bricken, Trenton and Templeton, Adly and Batson, Joshua and Chen, Brian and Jermyn, Adam and Conerly, Tom and Turner, Nick and Anil, Cem and Denison, Carson and Askell, Amanda and Lasenby, Robert and Wu, Yifan and Kravec, Shauna and Schiefer, Nicholas and Maxwell, Tim and Joseph, Nicholas and Hatfield-Dodds, Zac and Tamkin, Alex and Nguyen, Karina and McLean, Brayden and Burke, Josiah E and Hume, Tristan and Carter, Shan and Henighan, Tom and Olah, Christopher},
  year={2023},
  journal={Transformer Circuits Thread},
  note={https://transformer-circuits.pub/2023/monosemantic-features/index.html}
}
```

---

*笔记整理：2026-04-12*  
*图片来源：/Users/apple/Documents/MyBrain/3.Agent/monosemantic-features-images/*
