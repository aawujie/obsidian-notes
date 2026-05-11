---
title: "层次化可导航小世界图 (HNSW)"
source: "https://www.pinecone.io/learn/series/faiss/hnsw/"
author:
  - "[[James Briggs]]"
published:
created: 2026-05-11
description: "层次化可导航小世界（HNSW）图是向量相似性搜索中性能最优的索引之一。HNSW 是一项极为流行的技术，屡次在超快搜索速度和出色的召回率方面产出最先进的性能。"
tags:
  - "clippings"
  - "translation"
  - "中文"
translated: true
---

层次化可导航小世界（HNSW）图是[向量相似性搜索](https://www.pinecone.io/learn/what-is-similarity-search/)中性能最优的索引之一\[1\]。HNSW 是一项极为流行的技术，屡次在超快搜索速度和出色的召回率方面产出最先进的性能。

然而，尽管 HNSW 是近似最近邻（ANN）搜索中流行且健壮的算法，理解它的工作原理却远非易事。

---

**注意：**[**Pinecone**](https://www.pinecone.io/) **让你无需了解 HNSW 或向量索引库的任何知识，就能在应用中构建可扩展、高性能的向量搜索。但我们知道你希望了解事物的运作原理，所以请享受这篇指南！**

---

本文将揭开 HNSW 的神秘面纱，以易于理解的方式解释这个智能算法。在文章后半部分，我们将探讨如何使用 [Faiss](https://www.pinecone.io/learn/series/faiss/) 实现 HNSW，以及哪些参数设置能带来我们所需的性能。

## HNSW 的基础

我们可以将 [ANN 算法](https://www.pinecone.io/learn/what-is-similarity-search/)分为三个不同的类别：树、哈希和图。HNSW 属于*图*这个类别。更具体地说，它是一种*邻近图*，其中两个顶点基于它们的邻近程度（更近的顶点被链接）被连接起来——通常以欧几里得距离定义。

从一个*"邻近"图*到一个*"层次化可导航小世界"图*，复杂性有显著的跃升。我们将描述对 HNSW 贡献最大的两项基础技术：概率跳表（probability skip list）和可导航小世界图（navigable small world graph）。

### 概率跳表

概率跳表最早由 *William Pugh* 于 1990 年提出\[2\]。它像有序数组一样允许快速搜索，同时使用链表结构来轻松（且快速地）插入新元素（这是有序数组做不到的）。

跳表通过构建多层链表来工作。在第一层，我们找到*跳过*许多中间节点/顶点的链接。随着向下的层级移动，每条链接*"跳过"*的数量逐渐减少。

要搜索跳表，我们从具有最长 *"跳跃"* 的最高层开始，沿着边向右移动（如下图）。如果我们发现当前节点的"键"*大于*我们要搜索的键——我们知道已经越过了目标，于是向下移动到*下一个*层级的前一个节点。

![概率跳表结构，我们从最顶层开始。如果当前键大于我们要搜索的键（或到达末尾），则下降到下一层。](https://www.pinecone.io/_next/image/?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fvr8gru94%2Fproduction%2F9065d31e1b2e33ca697a56082f0ece7eff1c2d9b-1920x500.png&w=3840&q=75)

概率跳表结构，我们从最顶层开始。如果当前键大于我们要搜索的键（或到达末尾），则下降到下一层。

HNSW 继承了相同的分层格式：最高层有较长的边（用于快速搜索），较低层有较短的边（用于精确搜索）。

### 可导航小世界图

使用*可导航小世界*（NSW）图进行向量搜索是在 2011-14 年的几篇论文中引入的\[4, 5, 6\]。其核心思想是：如果我们构建一个邻近图，同时具有长程和短程链接，那么搜索时间可以降低到（多）对数复杂度。

图中的每个顶点连接到若干个其他顶点。我们称这些连接的顶点为*朋友*，每个顶点维护一个*朋友列表*，从而构成我们的图。

在搜索 NSW 图时，我们从一个预定义的*入口点*开始。该入口点连接到几个附近的顶点。我们识别出这些顶点中哪个最接近我们的查询向量，然后移动到那里。

![NSW 图的搜索过程。从预定义的入口点开始，算法贪婪地遍历到更接近查询向量的连接顶点。](https://www.pinecone.io/_next/image/?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fvr8gru94%2Fproduction%2F5ca4fca27b2a9bf89b06748b39b7b6238fd4548c-1920x1080.png&w=3840&q=75)

NSW 图的搜索过程。从预定义的入口点开始，算法贪婪地遍历到更接近查询向量的连接顶点。

我们重复这个*贪婪路由搜索*过程——通过在每个朋友列表中识别最近的邻近顶点，从一个顶点移动到另一个顶点。最终，我们会发现没有比当前顶点更近的顶点——这就是局部最小值，作为我们的停止条件。

---

*可导航小世界模型定义为使用贪婪路由具有（多）对数复杂度的任何网络。当图不可导航时，贪婪路由的效率对于较大网络（1-10K+ 顶点）会下降* *\[7\]。*

---

*路由*（即我们在图中穿行的实际路径）由两个阶段组成。我们从 "zoom-out"（缩小）阶段开始，经过低度数顶点（度数是一个顶点拥有的链接数量）——然后是后期的 "zoom-in"（放大）阶段，经过高度数顶点\[8\]。

![高度数顶点有许多链接，而低度数顶点只有很少的链接。](https://www.pinecone.io/_next/image/?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fvr8gru94%2Fproduction%2Fd65da887accc1d8d577f236459b16946c9f71a96-1920x960.png&w=3840&q=75)

高度数顶点有许多链接，而低度数顶点只有很少的链接。

我们的*停止条件*是在当前顶点的朋友列表中找不到更近的顶点。因此，在 *zoom-out* 阶段（链接更少，不太可能找到更近的顶点），我们更容易遇到局部最小值而过早停止。

为了最小化过早停止的概率（并提高召回率），我们可以增加顶点的平均度数，但这会增加网络复杂度（和搜索时间）。因此我们需要在召回率和搜索速度之间平衡顶点的平均度数。

另一种方法是从高度数顶点开始搜索（先进行 *zoom-in*）。对于 NSW，这*确实*能改善低维数据的性能。我们将看到，这也是 HNSW 结构中的一个重要因素。

### 创建 HNSW

HNSW 是 NSW 的自然演进，借鉴了 Pugh 概率跳表结构中的层次化多层思想。

为 NSW 添加层次结构产生了一个链接按不同层级分离的图。在最顶层，我们有最长的链接，在最底层，我们有最短的链接。

![HNSW 的分层图，最顶层是我们的入口点，只包含最长的链接，随着向下移动，链接长度变短且数量增多。](https://www.pinecone.io/_next/image/?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fvr8gru94%2Fproduction%2F42d4a3ffc43e5dc2758ba8e5d2ef29d4c4d78254-1920x1040.png&w=3840&q=75)

HNSW 的分层图，最顶层是我们的入口点，只包含最长的链接，随着向下移动，链接长度变短且数量增多。

在搜索过程中，我们进入最顶层，在那里找到最长的链接。这些顶点往往具有较高度数（链接分布在多个层级），这意味着我们默认从 NSW 中描述的 *zoom-in* 阶段开始。

我们在每一层中像 NSW 一样遍历边，贪婪地移动到最近的顶点，直到找到局部最小值。与 NSW 不同的是，此时我们会转移到下一层中的当前顶点并重新开始搜索。我们重复这个过程，直到找到最底层——*第 0 层*的局部最小值。

![通过 HNSW 图的多层结构进行搜索的过程。](https://www.pinecone.io/_next/image/?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fvr8gru94%2Fproduction%2Fe63ca5c638bc3cd61cc1cd2ab33b101d82170426-1920x1080.png&w=3840&q=75)

通过 HNSW 图的多层结构进行搜索的过程。

## 图的构建

在图的构建过程中，向量被逐个迭代插入。层数由参数 *L* 表示。向量在给定层插入的概率由一个概率函数给出，该函数由*"层级乘数" m\_L* 归一化，其中 *m\_L = ~0* 意味着向量仅在*第 0 层*插入。

![概率函数对每一层（除第 0 层外）重复执行。向量被添加到其插入层及其下方的每一层。](https://www.pinecone.io/_next/image/?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fvr8gru94%2Fproduction%2Ff105cb148aae44f77fa7e3df7b7f8c0256bcbec4-1920x980.png&w=3840&q=75)

概率函数对每一层（除第 0 层外）重复执行。向量被添加到其插入层及其下方的每一层。

HNSW 的创建者发现，当最小化各层之间共享邻居的重叠时，可以达到最佳性能。*降低 m\_L* 有助于最小化重叠（将更多向量推到*第 0 层*），但这会增加搜索期间的平均遍历次数。因此，我们使用一个平衡两者的 *m\_L* 值。*这个最优值的经验法则是* *`1/ln(M)`* *\[1\]*。

图的构建从最顶层开始。进入图后，算法贪婪地遍历边，找到与插入向量 *q* 最接近的 *ef* 个最近邻——此时 *ef = 1*。

找到局部最小值后，它向下移动到下一层（就像搜索时一样）。重复此过程，直到到达我们选择的*插入层*。这里开始构建的第二阶段。

*ef* 值增加到 `efConstruction`（我们设定的参数），意味着将返回更多的最近邻。在第二阶段，这些最近邻既是新插入元素 *q* 的链接候选，也是进入下一层的入口点。

从这些候选中添加 *M* 个邻居作为链接——最直接的选择标准是选择最近的向量。

经过多次迭代，在添加链接时还需要考虑另外两个参数。*M\_max* 定义了一个顶点可以拥有的最大链接数，*M\_max0* 定义了同样的但针对*第 0 层*的顶点。

![解释分配给每个顶点的链接数量，以及 M、M\_max 和 M\_max0 的影响。](https://www.pinecone.io/_next/image/?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fvr8gru94%2Fproduction%2Fdc5cb11ea197ceb4e1f18214066c8c51526b9af5-1920x1080.png&w=3840&q=75)

解释分配给每个顶点的链接数量，以及 M、M\_max 和 M\_max0 的影响。

插入的停止条件是到达*第 0 层*的局部最小值。

## HNSW 的实现

我们将使用 Facebook AI Similarity Search（Faiss）库来实现 HNSW，并测试不同的构建和搜索参数，看看它们如何影响索引性能。

要初始化 HNSW 索引，我们编写：

```python
# 设置 HNSW 参数
d = 128  # 向量维度
M = 32

index = faiss.IndexHNSWFlat(d, M)
print(index.hnsw)
```

```
<faiss.swigfaiss.HNSW; proxy of <Swig Object of type 'faiss::HNSW *' at 0x7f91183ef120> >
```

这样，我们设置了 `M` 参数——插入时添加到每个顶点的邻居数量，但我们还缺少 *M\_max* 和 *M\_max0*。

在 Faiss 中，这两个参数在 `set_default_probas` 方法中自动设置，该方法在索引初始化时调用。*M\_max* 值设置为 `M`，*M\_max0* 设置为 `M*2`（详见[notebook](https://github.com/pinecone-io/examples/blob/master/learn/search/faiss-ebook/hnsw-faiss/hnsw_faiss.ipynb)）。

在用 `index.add(xb)` 构建索引前，我们会发现层数（Faiss 中称为 *levels*）尚未设置：

```python
# HNSW 索引开始时没有层级
index.hnsw.max_level
```

```
-1
```

```python
# levels（或 layers）也是空的
levels = faiss.vector_to_array(index.hnsw.levels)
np.bincount(levels)
```

```
array([], dtype=int64)
```

如果我们继续构建索引，会发现这两个参数现在都被设置了。

```python
index.add(xb)
```

```python
# 添加数据后，我们发现 level
# 已被自动设置
index.hnsw.max_level
```

```
4
```

```python
# levels（或 layers）现在已填充
levels = faiss.vector_to_array(index.hnsw.levels)
np.bincount(levels)
```

```
array([     0, 968746,  30276,    951,     26,      1], dtype=int64)
```

这里我们有了图中的层级数量，从 *0* 到 *4*，由 `max_level` 描述。还有 `levels`，它显示了从 *0* 到 *4* 每个层级上顶点的分布（忽略第一个 `0` 值）。我们甚至可以找到哪个向量是我们的入口点：

```python
index.hnsw.entry_point
```

```
118295
```

这就是我们 Faiss 风格 HNSW 图的高层视图。在测试索引之前，让我们更深入地了解 Faiss 是如何构建这个结构的。

#### 图的结构

初始化索引时，我们传入向量维度 `d` 和每个顶点的邻居数 `M`。这会调用 `set_default_probas` 方法，传入 `M` 和 `1 / log(M)` 作为 `levelMult`（等价于上面的 *m\_L*）。该方法的 Python 等价实现如下：

```python
def set_default_probas(M: int, m_L: float):
    nn = 0  # 设置最近邻计数 = 0
    cum_nneighbor_per_level = []
    level = 0  # 从第 0 层开始
    assign_probas = []
    while True:
        # 计算当前层的概率
        proba = np.exp(-level / m_L) * (1 - np.exp(-1 / m_L))
        # 一旦达到低概率阈值，我们已经创建了足够多的层
        if proba < 1e-9: break
        assign_probas.append(proba)
        # 邻居数在每一层都 == M，除了第 0 层 == M*2
        nn += M*2 if level == 0 else M
        cum_nneighbor_per_level.append(nn)
        level += 1
    return assign_probas, cum_nneighbor_per_level
```

这里我们构建了两个向量——`assign_probas`，即向量在给定层的*插入概率*，以及 `cum_nneighbor_per_level`，即向量在不同插入层分配的最近邻累计总数。

```python
assign_probas, cum_nneighbor_per_level = set_default_probas(
    32, 1/np.log(32)
)
assign_probas, cum_nneighbor_per_level
```

```
([0.96875,
  0.030273437499999986,
  0.0009460449218749991,
  2.956390380859371e-05,
  9.23871994018553e-07,
  2.887099981307982e-08],
 [64, 96, 128, 160, 192, 224])
```

从中我们可以看到，向量在*第 0 层*插入的概率显著高于更高层（不过如下所述，实际概率与这里定义的略有不同）。这个函数意味着更高层更稀疏，降低了"陷入困境"的可能性，并确保我们从较长距离的遍历开始。

`assign_probas` 向量被另一个名为 `random_level` 的方法使用——在这个函数中，每个顶点被分配一个插入层。

```python
def random_level(assign_probas: list, rng):
    # 从随机数生成器获取随机浮点数
    f = rng.uniform() 
    for level in range(len(assign_probas)):
        # 如果随机浮点数小于该层的概率...
        if f < assign_probas[level]:
            # ...我们在该层确认插入
            return level
        # 否则减去该层概率并重试
        f -= assign_probas[level]
    # 以下情况以极低概率发生
    return len(assign_probas) - 1
```

我们使用 Numpy 的随机数生成器 `rng`（在下方初始化）生成一个随机浮点数 `f`。对于每个 `level`，检查 `f` 是否小于 `assign_probas` 中该层的分配概率——如果是，那就是我们的插入层。

如果 `f` 太大，我们从 `f` 中减去 `assign_probas` 的值，然后对下一层重试。这个逻辑的结果是，向量*最可能在*第 0 层插入，但如果不在第 0 层，则每增加一层，插入的概率递减。

最后，如果没有层级满足概率条件，我们使用 `return len(assign_probas) - 1` 在最高层插入向量。如果比较 Python 实现和 Faiss 的分布，我们会看到非常相似的结果：

```python
chosen_levels = []
rng = np.random.default_rng(12345)
for _ in range(1_000_000):
    chosen_levels.append(random_level(assign_probas, rng))
```

```python
np.bincount(chosen_levels)
```

```
array([968821,  30170,    985,     23,       1],
      dtype=int64)
```

![Faiss 实现（左）和 Python 实现（右）中各层顶点的分布对比。](https://www.pinecone.io/_next/image/?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fvr8gru94%2Fproduction%2F75658a08c25dabc1405f769c76fd2929c051853b-1920x930.png&w=3840&q=75)

Faiss 实现（左）和 Python 实现（右）中各层顶点的分布对比。

Faiss 实现还确保我们*始终*在最高层至少有一个顶点，作为图的入口点。

### HNSW 性能

现在我们已经探索了 HNSW 背后的所有理论以及如何在 Faiss 中实现——让我们看看不同参数对召回率、搜索和构建时间以及各索引内存使用的影响。

我们将修改三个参数：`M`、`efSearch` 和 `efConstruction`。我们将对 Sift1M 数据集进行索引，你可以使用[此脚本](https://gist.github.com/jamescalam/a09a16c17b677f2cf9c019114711f3bf)下载和准备数据。

像之前一样，我们这样初始化索引：

```python
index = faiss.IndexHNSWFlat(d, M)
```

另外两个参数 `efConstruction` 和 `efSearch` 可以在初始化 `index`*之后*修改。

```python
index.hnsw.efConstruction = efConstruction
index.add(xb)  # 构建索引
index.hnsw.efSearch = efSearch
# 现在可以搜索了
index.search(xq[:1000], k=1)
```

`efConstruction` 值*必须*在通过 `index.add(xb)` 构建索引之前设置，但 `efSearch` 可以在搜索前的任何时候设置。

先来看一下召回率性能。

![不同 M、efConstruction 和 efSearch 参数的 Recall@1 性能。](https://www.pinecone.io/_next/image/?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fvr8gru94%2Fproduction%2Fe8c281c3626226a76389fa344a71eb57f70cf879-1920x980.png&w=3840&q=75)

不同 M、efConstruction 和 efSearch 参数的 Recall@1 性能。

高 `M` 和 `efSearch` 值可以大幅提升召回率性能——同时也明显需要一个合理的 `efConstruction` 值。我们也可以增加 `efConstruction` 以在较低的 `M` 和 `efSearch` 值下获得更高的召回率。

然而，这种性能并非免费的。一如既往，我们需要在召回率和搜索时间之间取得平衡——让我们看看。

![搜索 1000 个查询时，不同 M、efConstruction 和 efSearch 参数下的搜索时间（微秒）。注意 y 轴使用对数刻度。](https://www.pinecone.io/_next/image/?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fvr8gru94%2Fproduction%2F876bf66aba408959042888efe72c55db4d6b3b41-1920x980.png&w=3840&q=75)

搜索 1000 个查询时，不同 M、efConstruction 和 efSearch 参数下的搜索时间（微秒）。注意 y 轴使用对数刻度。

虽然更高的参数值给我们带来了更好的召回率，但对搜索时间的影响可能是巨大的。这里我们搜索 `1000` 个相似向量（`xq[:1000]`），召回率/搜索时间可以从 80%-1ms 变化到 100%-50ms。如果我们能接受相当糟糕的召回率，搜索时间甚至可以降到 0.1ms。

如果你一直在关注我们的[向量相似性搜索系列文章](https://www.pinecone.io/learn/)，你可能记得 `efConstruction` 对[搜索时间的影响可以忽略不计](https://www.pinecone.io/learn/series/faiss/vector-indexes/)——但这里并非如此……

当搜索少量查询时，`efConstruction` 对搜索时间的影响*确实*很小。但这里使用了 `1000` 个查询，`efConstruction` 的微小影响变得非常显著。

如果你认为你的查询大多是低容量的，`efConstruction` 是一个很好的增加参数。它可以提高召回率而几乎不影响*搜索时间*，特别是在使用较低 `M` 值时。

![仅搜索一个查询时，efConstruction 与搜索时间的关系。当使用较低 M 值时，不同 efConstruction 值的搜索时间几乎不变。](https://www.pinecone.io/_next/image/?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fvr8gru94%2Fproduction%2Fef1a2edd25adb202c0a98a1f33a0e72d1295b554-1720x1080.png&w=3840&q=75)

仅搜索一个查询时，efConstruction 与搜索时间的关系。当使用较低 M 值时，不同 efConstruction 值的搜索时间几乎不变。

这一切看起来不错，但 HNSW 索引的内存使用呢？这里的情况可能稍显*不太*吸引人。

![使用 Sift1M 数据集，随着 M 值增加的内存使用。efSearch 和 efConstruction 对内存使用没有影响。](https://www.pinecone.io/_next/image/?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Fvr8gru94%2Fproduction%2Fe04d23ccd76d8bdc568542bebe75a75e7d36a21e-1480x1050.png&w=3840&q=75)

使用 Sift1M 数据集，随着 M 值增加的内存使用。efSearch 和 efConstruction 对内存使用没有影响。

`efConstruction` 和 `efSearch` 都不影响索引内存使用，我们只需考虑 `M`。即使 `M` 取较低的 `2`，索引大小也已超过 0.5GB，当 `M` 为 `512` 时几乎达到 5GB。

因此，虽然 HNSW 产生了令人难以置信的性能，但我们需要在高内存使用和由此可能产生的高基础设施成本之间进行权衡。

#### 改善内存使用和搜索速度

HNSW 在内存利用率方面并非最佳索引。然而，如果这一点很重要，并且改用[其他索引](https://www.pinecone.io/learn/series/faiss/vector-indexes/)不可行，我们可以通过使用[乘积量化（PQ）](https://www.pinecone.io/learn/series/faiss/product-quantization/)压缩向量来改善。使用 PQ 会降低召回率并增加搜索时间——但与往常一样，ANN 的很多工作就是在三者之间进行权衡。

如果我们想提高搜索速度——也可以！只需向索引添加一个 IVF 组件即可。在向索引添加 IVF 或 PQ 方面有很多内容可讨论，因此我们写了一篇[关于混合搭配索引的完整文章](https://www.pinecone.io/learn/series/faiss/composite-indexes/)。

以上就是关于用于向量相似性搜索的层次化可导航小世界图的文章！现在你已经了解了 HNSW 背后的直觉以及在 Faiss 中如何实现它，可以开始在你自己向量搜索应用中测试 HNSW 索引了，或者使用像 [Pinecone](https://www.pinecone.io/) 或 OpenSearch 这样已内置向量搜索功能的托管解决方案！

如果你想继续学习更多关于向量搜索以及如何利用它来增强你的应用，我们有一整套[学习材料](https://www.pinecone.io/learn/)，旨在帮你快速掌握向量搜索领域。

## 参考文献

\[1\] E. Bernhardsson, [ANN Benchmarks](https://github.com/erikbern/ann-benchmarks) (2021), GitHub

\[2\] W. Pugh, [Skip lists: a probabilistic alternative to balanced trees](https://15721.courses.cs.cmu.edu/spring2018/papers/08-oltpindexes1/pugh-skiplists-cacm1990.pdf) (1990), Communications of the ACM, vol. 33, no.6, pp. 668-676

\[3\] Y. Malkov, D. Yashunin, [Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs](https://arxiv.org/abs/1603.09320) (2016), IEEE Transactions on Pattern Analysis and Machine Intelligence

\[4\] Y. Malkov et al., [Approximate Nearest Neighbor Search Small World Approach](https://www.iiis.org/CDs2011/CD2011IDI/ICTA_2011/PapersPdf/CT175ON.pdf) (2011), International Conference on Information and Communication Technologies & Applications

\[5\] Y. Malkov et al., [Scalable Distributed Algorithm for Approximate Nearest Neighbor Search Problem in High Dimensional General Metric Spaces](https://www.researchgate.net/publication/262334462_Scalable_Distributed_Algorithm_for_Approximate_Nearest_Neighbor_Search_Problem_in_High_Dimensional_General_Metric_Spaces) (2012), Similarity Search and Applications, pp. 132-147

\[6\] Y. Malkov et al., [Approximate nearest neighbor algorithm based on navigable small world graphs](https://publications.hse.ru/mirror/pubs/share/folder/x5p6h7thif/direct/128296059) (2014), Information Systems, vol. 45, pp. 61-68

\[7\] M. Boguna et al., [Navigability of complex networks](https://arxiv.org/abs/0709.0303) (2009), Nature Physics, vol. 5, no. 1, pp. 74-80

\[8\] Y. Malkov, A. Ponomarenko, [Growing homophilic networks are natural navigable small worlds](https://arxiv.org/abs/1507.06529) (2015), PloS one

Facebook Research, [Faiss HNSW Implementation](https://github.com/facebookresearch/faiss/blob/main/faiss/impl/HNSW.cpp), GitHub