---
title: "论文报告：TPR Probes Reveal Shared Structure Across Linear Directions"
type: paper-report
created: 2026-05-19
source: "arXiv:2605.09967"
authors: "Andrew Lee, Fernanda Viégas, Martin Wattenberg (Harvard / Google DeepMind)"
tags:
  - mechanistic-interpretability
  - linear-representation-hypothesis
  - tensor-product-representation
  - probing
  - othello-gpt
  - representation-learning
---

# TPR Probes 揭示线性方向背后的共享结构

> **论文**：*Tensor Product Representation Probes Reveal Shared Structure Across Linear Directions*
> **作者**：Andrew Lee, Fernanda Viégas, Martin Wattenberg — Harvard University / Google DeepMind
> **日期**：2026-05-11 | **代码**：[github.com/ajyl/tpr_othello](https://github.com/ajyl/tpr_othello)

---

## 一、核心问题

**线性表示假说**认为 Transformer 将概念编码为激活空间中的线性方向（如情感、毒性、拒绝等），已得到大量实证支持。但一个根本问题被忽视了：

> 一堆孤立的线性方向（bag of linear directions）无法捕捉**关系结构**——而真实世界中的概念是由关系组织起来的。

这篇论文的核心问题是：**线性方向是否只是更丰富、更具组合性的底层结构的投影？**

---

## 二、实验平台：OthelloGPT

选用 **OthelloGPT**（Li et al., 2022）作为研究对象：

- 8 层 Transformer，仅在 2000 万局黑白棋（Othello）走子序列上训练
- 输入如 `["D3", "E3", ...]`，预测下一个合法走法
- **关键特性**：模型从未被告知棋盘的存在，但内部激活中自发涌现了棋盘状态的表征
- Nanda et al. (2023) 证明：棋盘状态可通过**线性探针**（192 个独立线性方向 = 64 格 × 3 种颜色）从激活中解码

棋盘具有天然结构：格子（squares）和棋子颜色（colors）是两类不同的概念，通过"占据"关系组合成棋盘状态。线性探针能解码，但不回答"这些方向是否来自共享的结构化因素"。

---

## 三、方法：张量积表示探针

### 3.1 TPR 框架（Smolensky, 1990）

张量积表示（Tensor Product Representation, TPR）通过**角色-填充物绑定**（role-filler binding）将结构化对象表示为各组件外积的叠加：

$$\mathbf{B} = \sum_{i=1}^{k} \mathbf{r}_i \otimes \mathbf{f}_{y(i)} \in \mathbb{R}^{d_r \times d_f}$$

- $\mathbf{r}_i$：角色向量（如棋盘的格子）
- $\mathbf{f}_{y(i)}$：填充物向量（如格子的颜色）
- $\mathbf{B}$：绑定矩阵

棋盘状态天然适配此框架——64 个格子是角色，3 种颜色（Empty/Current/Opponent）是填充物。

### 3.2 双线性 TPR 探针

探针学习三组权重：

1. **角色嵌入** $\mathbf{R} \in \mathbb{R}^{64 \times d_r}$：每个格子的向量表示
2. **填充嵌入** $\mathbf{F} \in \mathbb{R}^{3 \times d_f}$：每种颜色的向量表示
3. **映射矩阵** $\mathbf{M} \in \mathbb{R}^{d_r \times d_f \times d_{model}}$：将隐藏状态映射到绑定空间

解码过程：
$$\mathbf{B} = \mathbf{M}(\mathbf{h}_t^l), \quad \ell_{s,c} = \mathbf{r}_s^\top \mathbf{B} \,\mathbf{f}_c$$

### 3.3 三线性 TPR 探针

更细粒度的分解：棋盘本身也是结构化的（8 行 × 8 列），引入第三个维度：

$$\ell_{ij,c} = \langle \mathbf{T},\ \mathbf{u}_i \otimes \mathbf{v}_j \otimes \mathbf{f}_c \rangle$$

- $\mathbf{U} \in \mathbb{R}^{8 \times d_u}$：行嵌入
- $\mathbf{V} \in \mathbb{R}^{8 \times d_v}$：列嵌入
- $\mathbf{F} \in \mathbb{R}^{3 \times d_f}$：颜色嵌入

---

## 四、核心发现

### 4.1 TPR 探针的高效性

- 线性探针：$192 \times 512 = 98,304$ 参数
- 双线性 TPR（$d_r=52$, $d_f=2$）：$56,582$ 参数（仅 **57.5%**）
- 三线性 TPR（$d_u=d_v=8$, $d_f=2$）：$65,670$ 参数
- **两者均达 99% 准确率**，参数更少且结构约束更强

关键：**仅需低秩角色/填充嵌入即可完美解码**（$d_f=2$ 足够，因为 3 类 softmax 只有 2 个自由度）。

### 4.2 嵌入的可视化结构

- **格子嵌入** (Isomap)：呈现鞍形流形，上曲线对应行 A-H，下曲线对应列 1-8
- **颜色嵌入** (PCA)：PC1 分离 Empty vs. 被占据，PC2 分离 Current vs. Opponent
- **绑定矩阵** (PCA)：64 个格子形成与颜色嵌入结构镜像的聚类
- D4-D5-E4-E5 四格是异常值——根据 Othello 规则，起始四格永远不空

### 4.3 因果干预验证

对模型内部棋盘表征进行干预（翻转某格颜色或置空），验证模型的下步预测是否相应改变：

- 线性探针干预：$\hat{\mathbf{h}} = \mathbf{h} + \alpha \frac{\mathbf{w}_{s,c}}{\|\mathbf{w}_{s,c}\|}$
- TPR 干预：替换绑定矩阵中的外积项 $\mathbf{r}_s \mathbf{f}_{y(s)}^\top \to \mathbf{r}_s \mathbf{f}_{\hat{y}(s)}^\top$，再通过 $\mathbf{M}$ 的伪逆映射回隐藏空间

**结果**（Figure 3）：所有干预（线性、双线性 TPR、三线性 TPR）均达到近乎零误差，即使同时干预多个格子。**TPR 探针不仅捕捉了有效结构，还捕捉了因果机制。**

### 4.4 ⭐ 线性探针可从 TPR 参数中恢复

这是论文最重要的发现：

从 TPR 参数可推导"有效线性探针方向"：
$$\tilde{\mathbf{w}}_{s,c} = \mathbf{M}_{\text{flat}}^\top \text{vec}(\mathbf{r}_s \mathbf{f}_c^\top)$$

与独立训练的线性探针计算余弦相似度：
- **满维情况**（$d_r=64$）：几乎完美对齐（余弦相似度 >0.95）
- **压缩情况**（$d_r=56$）：仍保持高相似度（多数 >0.85），中心四格因"永不为空"约束而略低

**结论：线性方向是更结构化 TPR 探针的投影。** 满维时 TPR 仅是线性探针的重新参数化（Appendix C 给出数学证明）；压缩时 TPR 通过瓶颈形成分布式编码（叠加），但仍能恢复线性方向。

### 4.5 不仅是低秩分解

与 SVD 截断对比：
- 当参数相当时，TPR 达 99% 准确率，而 rank-$k$ SVD 仅 85%
- SVD 需 $k=120$（1.5 倍参数）才能达到 TPR 的 99%
- **TPR 学到的是结构化分解，超越了简单的低秩分解**

### 4.6 ⭐ 格子嵌入恢复棋盘几何

定量分析格子嵌入的几何结构：

**局部邻域分析**（Figure 6）：
- 每个格子的 $k$-近邻中，约 **60%** 是真实棋盘邻居
- 其余主要在同一行/列/对角线
- 两个基线模型（随机棋盘状态训练、随机编码训练）均表现差得多

**成对棋盘几何**（Figure 7）：
- 计算所有 2016 对格子嵌入的余弦相似度，按行列间距 $(\Delta i, \Delta j)$ 分组
- 同一行（$\Delta i=0$）、同一列（$\Delta j=0$）、同一对角线（$\Delta i=\Delta j$）的格子对相似度显著更高
- $R^2=0.54$（OthelloGPT）vs $R^2=0.24$（随机编码）vs $R^2=0.03$（OOD）

**TPR 探针从 OthelloGPT 中恢复的格子嵌入自发反映了棋盘几何结构，远超 TPR 架构本身或数据分布所能解释的程度。**

### 4.7 局部编码 vs. 分布式编码

Appendix C 揭示了一个优雅的性质：

- **满维 TPR**（$d_u=d_v=8$, $d_f=2$）：行列嵌入构成近似标准正交基（Gram 矩阵接近单位矩阵，奇异值接近 1），本质是**局部编码**——每个格子-颜色对有独立维度
- **压缩 TPR**（$d_u<8$ 或 $d_r<64$）：必须通过**分布式编码（叠加）**来表示信息

---

## 五、相关工作定位

| 方向 | 代表性工作 | 与本工作的关系 |
|:---|:---|:---|
| 线性表示假说 | Park et al. 2023, Tigges et al. 2023, Arditi et al. 2024 | 本工作揭示线性方向背后的结构化分解 |
| 非线性/流形特征 | Engels et al. 2024, Kantamneni & Tegmark 2025 | 特征可能不是 rank-1 的，而是低维流形 |
| 因子化表征 | Shai et al. 2026 | Transformers 可学习潜在变量的因子化表示 |
| 特征场 | Yocum et al. 2025, Sarfati et al. 2026 | 线性探针可能从结构化的"特征场"中恢复局部读数 |
| 乘法 Transformer | Bai et al. 2025 | 数字在乘法模型中形成五棱柱结构（Figure 8）→ 线性方向是聚类的投影 |
| 结构化 SAE | Hindupur et al. 2025, Costa et al. 2025 | 现有 SAE 缺乏对组件间交互（绑定）的建模 |
| TPR 传统 | Smolensky 1990, McCoy et al. 2018 | TPR 框架用于编码组合/关系结构 |

---

## 六、局限性与讨论

1. **需先验知识**：TPR 探针需要预先知道要寻找什么结构（棋盘格子、颜色），不适用于未知领域
2. **不声称模型本身做张量积**：TPR 探针恢复的是可分解共享结构的参数化，不意味着模型内部原生使用 TPR
3. **未与机制对接**：未研究恢复的结构如何与 OthelloGPT 的具体计算机制关联
4. **单一绑定层**：只有一层 role-filler 绑定，未来可扩展到多层级的层次化结构

**开放问题**：
- 线性方向是否普遍是更丰富结构化表示的投影？
- SAE 恢复的 latent 中，是否有部分对应组件间的交互（绑定）？如何解释它们？
- 能否发展既不需要先验结构知识又能恢复绑定的无监督方法？

---

## 七、个人评注

**为什么这篇论文重要？**

1. **桥接了机械可解释性两大流派**：线性探测（简单但无结构）和 TPR/组合表征（有结构但较少实证验证）。证明两者不是竞争关系，而是投影关系。

2. **方法论贡献**：TPR 探针是一种轻量级的结构化解码器，比线性探针参数更少、产出更丰富（可分解的角色/填充嵌入 + 绑定矩阵 + 几何洞察），可以直接嫁接到任何有结构先验的领域。

3. **启发性类比**（Figure 8）：乘法 Transformer 中数字形成五棱柱结构，线性方向只是到每个簇质心的向量。**这个类比暗示：许多已发现的"线性特征"可能只是冰山一角**——底下藏着更丰富的几何/组合结构。

4. **对 SAE 研究的启示**：当前 SAE 以 bag of directions 的方式分解激活，但可能忽略了特征间的**交互（绑定）**。TPR 框架提供了一种考虑交互的方式。

**值得关注的后续方向**：
- 将 TPR 探针应用到自然语言领域（句法树？语义角色？）
- 与 SAE 结合，发展"绑定感知"的稀疏自编码器
- 在更大模型中验证线性方向 = 结构化底层投影的假说

---

*报告基于 arXiv:2605.09967 v1 (2026-05-11)，原文 12 页 + 附录*