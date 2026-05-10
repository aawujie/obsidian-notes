---
title: ML-Visualized 项目调研
type: research
created: 2026-05-11
updated: 2026-05-11
sources:
  - https://github.com/gavinkhung/machine-learning-visualized
  - https://ml-visualized.com/
tags: [ML, 可视化, 开源项目, Jupyter-Book, 调研]
---

# ML-Visualized 项目调研

> GitHub: [gavinkhung/machine-learning-visualized](https://github.com/gavinkhung/machine-learning-visualized)
> 在线书: https://ml-visualized.com/
> Stars: 1,253 · Forks: 106 · License: MIT · 作者: Gavin H (UMD)

---

## 一、项目概述

**Machine Learning Visualized** 是一本基于 Jupyter Book 构建的交互式 ML 在线书籍。作者 Gavin H（马里兰大学 CS 本科生）根据课堂讲义，用纯 NumPy 从第一性原理（first-principles）实现经典机器学习算法，每个 Notebook 的核心输出是一段训练过程的可视化动画——展示模型如何从随机初始化逐步收敛到最优参数。

项目仓库本身只包含 Jupyter Book 的配置和构建文件（Markdown、_toc.yml、Dockerfile），各算法的 .ipynb 文件存储在独立的 GitHub 仓库中，通过 `download_notebooks.sh` 脚本拉取后统一构建。

### 核心设计理念

1. **From Scratch**: 所有算法用纯 NumPy 手写实现，不使用 sklearn/pytorch 的现成模型（但部分章节有对比）
2. **数学推导 + 代码 + 可视化的三位一体**: Markdown 中嵌入 LaTeX 公式推导，代码块实现算法，最终输出 GIF/动画展示训练过程
3. **交互性**: 部分算法提供 Marimo Interactive Notebook，可拖动滑块调整超参数实时观察 loss 变化

---

## 二、功能清单

### Chapter 1. 优化 (Optimization)

| 算法 | 类型 | 交互版 | 说明 |
|------|------|--------|------|
| Gradient Descent | Notebook | - | 梯度下降优化过程可视化 |
| Linear Regression | Notebook | Marimo 交互版 | 含交互式线性回归，可调权重观察 loss 变化 |

### Chapter 2. 聚类与降维 (Clustering & Reduction)

| 算法 | 类型 | 交互版 | 说明 |
|------|------|--------|------|
| PCA (主成分分析) | Notebook | - | 数据压缩、主成分方向可视化 |
| K-Means 聚类 | Notebook | - | 聚类过程迭代可视化 |

### Chapter 3. 线性模型 (Linear Models)

| 算法 | 类型 | 交互版 | 说明 |
|------|------|--------|------|
| Perceptron | Notebook | Marimo 交互版 | 单层感知机决策边界演变 |
| Logistic Regression | Notebook | Marimo 交互版 | Sigmoid 激活 + BCE loss |

### Chapter 4. 神经网络 (Neural Networks)

| 算法 | 类型 | 交互版 | 说明 |
|------|------|--------|------|
| Neural Network (函数拟合) | Notebook | - | 用 3 层 NN 拟合双曲抛物面 |
| Neural Network (Loss Landscape) | Notebook | - | 训练过程中 loss 曲面可视化 |
| Neural Network (Transformations) | Notebook | - | 隐藏层输出变换的可视化 |

### 每个 Notebook 的结构（以 Neural Network 为例，55 个 cell）

1. **数学推导** (Markdown + LaTeX): Forward Propagation → Loss Function (MSE) → Backpropagation (链式法则) → 梯度公式
2. **从零实现**: DenseLayer 类、Tanh Activation、Gradient Descent Optimizer
3. **训练循环**: 逐 epoch 记录权重、loss、预测值，生成动画帧
4. **可视化输出**: GIF 动画展示模型拟合真值的过程
5. **PyTorch 对照**: 用 `nn.Module` 重写同一网络，对比训练结果

---

## 三、技术栈

| 层级 | 技术 | 用途 |
|------|------|------|
| **计算核心** | Python 3 + NumPy | 算法实现（矩阵运算） |
| **可视化** | Matplotlib + celluloid + scienceplots | 训练动画生成（celluloid 将 matplotlib 帧合成 GIF） |
| **文档系统** | Jupyter Book | 将 .ipynb + .md 构建为静态网站 |
| **交互式** | Marimo | 部分算法有交互式 Notebook |
| **数学排版** | LaTeX (nbconvert) | 公式渲染 + EPUB/PDF 导出 |
| **构建/部署** | Docker / GitHub Actions / GitHub Pages | CI 自动构建和部署到 ml-visualized.com |
| **单算法仓库** | 6 个独立 GitHub 仓库 | 每个算法独立维护 |

### 本地运行

```bash
# 方式 1: pip 直接构建
pip install -U jupyter-book
./download_notebooks.sh   # 拉取所有 .ipynb
jupyter-book build .
# 打开 _build/html/index.html

# 方式 2: Docker
docker compose run jupyter-book
```

依赖极简，核心只需 `numpy` + `matplotlib` + `jupyter-book`。

---

## 四、实用性评估

### ✅ 优点

1. **ML 入门教学的标杆级资源**: 数学推导 → 代码实现 → 可视化验证的闭环非常适合自学。对比吴恩达课程偏重理论、fast.ai 偏重工程，这个项目在"看见算法如何工作"上独树一帜。
2. **第一性原理实现**: 不用 sklearn，纯 NumPy 手写 forward/backward pass，真正理解算法内部机制。
3. **代码质量高**: 结构清晰，注释充分，数学公式与代码一一对应。
4. **部署友好**: Docker 一键构建，GitHub Pages 自动部署，本地可完整离线运行。
5. **社区潜力**: 作者设计了贡献流程（commit reference），鼓励社区提交新算法 Notebook。

### ⚠️ 局限性

1. **覆盖算法较少**: 仅 7 个基础算法，缺少 Decision Tree、Random Forest、SVM、XGBoost、Transformer、CNN 等。
2. **非生产工具**: 这是教学项目，不适合直接用于实际 ML 项目的可视化需求。算法实现也不是为了性能优化的。
3. **可视化维度有限**: 仅支持 2D/3D 可视化（matplotlib），无法处理高维数据的降维可视化（需 UMAP/t-SNE 等）。
4. **作者维护能力不确定**: 目前仅 1 个作者（本科生），长期维护存疑。最近更新在 2026-04-02。
5. **标注语言为 TeX**: GitHub 将其归类为 TeX 项目（因为 LaTeX 讲义文件多），可能影响搜索发现。

### 与现有工具对比

| 工具 | 定位 | 与本项目关系 |
|------|------|------------|
| **matplotlib / seaborn** | 通用数据可视化库 | 本项目基于 matplotlib，是底层依赖，不是竞品 |
| **scikit-learn** | 生产级 ML 库 | 本项目是教学实现，sklearn 是工业实现，互补 |
| **TensorBoard** | 训练监控仪表板 | 本项目是离线教学动画，TensorBoard 是实时训练监控 |
| **3Blue1Brown** | 数学动画讲解 | 理念相近（可视化理解），但 3B1B 是视频，本项目是可运行代码 |
| **Distill.pub** | 交互式 ML 文章 | 理念最接近，但 Distill 已停更，本项目更偏代码实现 |
| **d2l.ai (动手学深度学习)** | 交互式深度学习书籍 | 目标相似但规模更大，d2l 覆盖更多模型，本项目更偏可视化 |

---

## 五、投资/量化场景应用

### 能否直接用于投研可视化？

**结论: 基本不能直接用于投研，但部分模块可作为教学辅助。**

| 投研需求 | 本项目能否满足 | 替代方案 |
|----------|:---:|------|
| 因子分析可视化 (IC/ICIR 曲线) | ❌ | matplotlib/seaborn 自定义 + Jupyter |
| 回测曲线 (净值、回撤、夏普) | ❌ | pyfolio / quantstats / backtrader |
| 组合优化 (有效前沿、权重热力图) | ❌ | PyPortfolioOpt + matplotlib |
| ML 因子模型训练可视化 | ⚠️ 部分 | Gradient Descent / Linear Regression 章可作为理解优化过程的参考 |
| 策略信号分布可视化 | ❌ | plotly / seaborn |
| 深度学习策略 (RL/Transformer) 架构理解 | ⚠️ 部分 | Neural Network 章可帮助理解网络训练原理 |
| 时序预测模型可视化 | ❌ | statsmodels / prophet + 自定义 |

### 可能的借鉴方向

1. **教学参考**: 如果做量化策略的教学材料（如给团队讲解 ML 如何用于因子挖掘），这个项目的"推导+实现+可视化"三合一模式值得借鉴。
2. **Marimo 交互式**: Marimo 的交互式 Notebook 对回测参数调优（如滑动窗口、止损阈值）有参考价值——可以做一个类似的交互式回测可视化。
3. **训练过程可视化**: Neural Network loss landscape 的可视化方式，可以借鉴用于展示策略参数优化过程中的参数空间形态。
4. **celulloid 动画**: 生成 GIF 动画的技术可用于生成策略信号演变、投资组合权重变化的动图。

### 替代/补充工具推荐

- **Quant 常用可视化**: [QuantStats](https://github.com/ranaroussi/quantstats) — 一键生成回测报告含所有标准图表
- **ML 可解释性**: [SHAP](https://github.com/shap/shap) — 因子重要性、特征贡献分析
- **交互式仪表板**: [Panel](https://panel.holoviz.org/) + [HoloViews](https://holoviews.org/) — 可链接回测参数，实时更新图表

---

## 六、总结

`machine-learning-visualized` 是一个**高质量 ML 入门教学项目**，核心价值在于"看见算法如何学习"。对量化投研的**直接实用性很低**，但作为理解 ML 优化过程的教学参考、以及思考"如何把数学模型可视化"的灵感来源，仍有间接价值。

**推荐指数（面向量化投研）**: ⭐⭐☆☆☆ (2/5)
**推荐指数（面向 ML 初学者）**: ⭐⭐⭐⭐⭐ (5/5)

---

## 附录: 关键链接

- 项目主页: https://github.com/gavinkhung/machine-learning-visualized
- 在线书籍: https://ml-visualized.com/
- 作者 LinkedIn: https://www.linkedin.com/in/gavinkhung/
- 单算法仓库:
  - [Neural Network](https://github.com/gavinkhung/neural-network)
  - [Logistic Regression](https://github.com/gavinkhung/logistic-regression)
  - [Perceptron](https://github.com/gavinkhung/perceptron)
  - [PCA](https://github.com/gavinkhung/pca)
  - [K-Means](https://github.com/gavinkhung/k-means-clustering/)
  - [Gradient Descent](https://github.com/gavinkhung/gradient-descent)