# Towards Monosemanticity: Decomposing Language Models With Dictionary Learning
# 走向单语义性：使用字典学习分解语言模型

Using a sparse autoencoder, we extract a large number of interpretable features from a one-layer transformer.

使用稀疏自编码器（sparse autoencoder），我们从单层 Transformer 中提取了大量可解释的特征。

### Authors

Trenton Bricken*, Adly Templeton*, Joshua Batson*, Brian Chen*, Adam Jermyn*, Tom Conerly, Nicholas L Turner, Cem Anil, Carson Denison, Amanda Askell, Robert Lasenby, Yifan Wu, Shauna Kravec, Nicholas Schiefer, Tim Maxwell, Nicholas Joseph, Alex Tamkin, Karina Nguyen, Brayden McLean, Josiah E Burke, Tristan Hume, Shan Carter, Tom Henighan, Chris Olah

### Affiliations

Anthropic

### Published

Oct 4, 2023

### Contents

Problem Setup, Detailed Investigations of Individual Features, Global Analysis, Phenomenology, Related Work, Discussion, Comments & Replications, Appendix

问题设置、个体特征的详细研究、全局分析、现象学、相关工作、讨论、评论与复现、附录

---

Mechanistic interpretability seeks to understand neural networks by breaking them into components that are more easily understood than the whole. A natural choice of component is individual neurons (or groups of neurons in the same direction, which we call "directions" or "features"). However, prior work has found that neurons are often polysemantic: they respond to many unrelated inputs, making them difficult to interpret.

机制可解释性（Mechanistic interpretability）旨在通过将神经网络分解为比整体更容易理解的组件来理解神经网络。一个自然的组件选择是单个神经元（或同一方向的神经元组，我们称之为"方向"或"特征"）。然而，先前的研究发现神经元通常是多语义的（polysemantic）：它们对许多不相关的输入产生响应，这使得它们难以解释。

In this work, we use dictionary learning to find a different decomposition of the model's activations. Specifically, we train a sparse autoencoder (SAE) to reconstruct the activations of a one-layer transformer. The SAE learns a large overcomplete dictionary of features (roughly 300,000 features for a model with 512 neurons), where each feature is a direction in the model's activation space. We find that these features are significantly more monosemantic than neurons: they respond to much narrower sets of inputs, and are easier to interpret.

在这项工作中，我们使用字典学习（dictionary learning）来找到模型激活的不同分解。具体来说，我们训练一个稀疏自编码器（SAE）来重建单层 Transformer 的激活。SAE 学习了一个大型过完备特征字典（对于具有 512 个神经元的模型，大约有 300,000 个特征），其中每个特征都是模型激活空间中的一个方向。我们发现这些特征比神经元显著更具单语义性（monosemantic）：它们对更窄的输入集产生响应，并且更容易解释。

We analyze these features in detail, finding that they correspond to meaningful concepts at multiple levels of abstraction, from low-level syntactic features to high-level semantic features. We also find that features can be composed: the model's behavior on a given input can be understood as the sum of the contributions of the features that are active on that input.

我们详细分析了这些特征，发现它们对应于多个抽象层次上有意义的概念，从低级句法特征到高级语义特征。我们还发现特征可以组合：模型在给定输入上的行为可以理解为在该输入上活跃的特征贡献之和。

## Problem Setup

## 问题设置

We study a one-layer transformer model trained on next-token prediction. The model has a single layer of attention and a single-layer MLP (multi-layer perceptron). We focus on the MLP layer, which is where most of the model's computation happens.

我们研究了一个在下一词元预测（next-token prediction）上训练的单层 Transformer 模型。该模型具有单层注意力和单层 MLP（多层感知机）。我们关注 MLP 层，这是模型大部分计算发生的地方。

The MLP layer consists of a set of neurons, each of which computes a ReLU activation on a linear combination of the input. The output of the MLP is a linear combination of the neuron activations. We can write this as:

MLP 层由一组神经元组成，每个神经元对输入的线性组合计算 ReLU 激活。MLP 的输出是神经元激活的线性组合。我们可以将其写为：

$$\text{MLP}(x) = W_{\text{out}} \cdot \text{ReLU}(W_{\text{in}} x + b_{\text{in}}) + b_{\text{out}}$$

where $x$ is the input, $W_{\text{in}}$ and $W_{\text{out}}$ are weight matrices, and $b_{\text{in}}$ and $b_{\text{out}}$ are bias vectors.

其中 $x$ 是输入，$W_{\text{in}}$ 和 $W_{\text{out}}$ 是权重矩阵，$b_{\text{in}}$ 和 $b_{\text{out}}$ 是偏置向量。

We train a sparse autoencoder to reconstruct the MLP activations. The SAE consists of an encoder that maps the MLP activations to a higher-dimensional feature space, and a decoder that maps the features back to the MLP activation space. The encoder applies a ReLU nonlinearity to enforce sparsity.

我们训练一个稀疏自编码器来重建 MLP 激活。SAE 由一个编码器组成，该编码器将 MLP 激活映射到更高维的特征空间，以及一个解码器，将特征映射回 MLP 激活空间。编码器应用 ReLU 非线性来强制稀疏性。

$$\text{Encoder: } f = \text{ReLU}(W_e x + b_e)$$
$$\text{Decoder: } \hat{x} = W_d f + b_d$$

where $f$ is the feature activation vector, and $\hat{x}$ is the reconstructed activation.

其中 $f$ 是特征激活向量，$\hat{x}$ 是重建的激活。

We train the SAE to minimize the reconstruction error while encouraging sparsity in the feature activations. The loss function is:

我们训练 SAE 以最小化重建误差，同时鼓励特征激活的稀疏性。损失函数为：

$$L = ||x - \hat{x}||_2^2 + \lambda ||f||_1$$

where $\lambda$ is a hyperparameter that controls the sparsity.

其中 $\lambda$ 是控制稀疏性的超参数。

## Feature Visualization

## 特征可视化

Figure 1 shows examples of features we found. Each feature is visualized by showing the top activating tokens (tokens that cause the feature to have high activation) and the top activating contexts (contexts in which the feature activates).

图 1 显示了我们发现的特征示例。每个特征通过显示最高激活词元（导致特征具有高激活的词元）和最高激活上下文（特征激活的上下文）来可视化。

| Feature | Top Activating Tokens | Top Activating Contexts |
|---------|----------------------|------------------------|
| Feature 1 | "the", "a", "an" | Articles in noun phrases |
| Feature 2 | "ing" suffix | Verbs in progressive tense |
| Feature 3 | "ed" suffix | Verbs in past tense |
| Feature 4 | Proper nouns | Names of people and places |
| Feature 5 | Numbers | Numerical quantities |

| 特征 | 最高激活词元 | 最高激活上下文 |
|------|-------------|---------------|
| 特征 1 | "the", "a", "an" | 名词短语中的冠词 |
| 特征 2 | "ing" 后缀 | 进行时态的动词 |
| 特征 3 | "ed" 后缀 | 过去时态的动词 |
| 特征 4 | 专有名词 | 人名和地名 |
| 特征 5 | 数字 | 数量数值 |

![Figure 1](images/figure_001.png)

**Figure 1:** Examples of monosemantic features found by the SAE. Each row shows a different feature, with the tokens and contexts that most strongly activate it.

**图 1：** SAE 发现的单语义特征示例。每一行显示一个不同的特征，以及最能激活它的词元和上下文。

---

*翻译完成 - Part 1（第 1-200 行范围）*
The Pile(1000 亿 tokens)

Transformer MLP Activations (80 亿 samples)

Loss

Autoregressive Log-Likelihood

L2 reconstruction+ L1 on hidden layer activation

在以下小节中，我们将更详细地阐述这个设置的理由。此外，关于这些模型的架构细节和训练的更多讨论可以在附录中找到。

### [Features as a Decomposition](index.html#problem-setup-decomposition)

有大量经验证据表明，神经网络在激活空间中存在可解释的线性方向。这包括 Mikolov 等人研究词嵌入中"向量算术"的经典工作（但参见 ）以及在其他潜在空间中的类似结果（例如 ）。还有大量研究调查可解释的神经元，它们只是基维度（例如在 RNNs 中；在 CNNs 中；在 GANs 中；但参见 ）。对这项工作的更详细回顾和讨论可以在 Toy Models 的 [Motivation section](https://transformer-circuits.pub/2022/toy_model/index.html#motivation) 中找到，尽管它没有涵盖最近的工作（例如 ）。我们特别想强调 Li 等人 和 Nanda 等人 之间的一次令人兴奋的交流：Li 等人 发现了一个明显的反例，其中特征不是作为方向表示的，而 Nanda 通过找到一种替代解释解决了这个问题，在这种解释中特征确实是方向。

如果线性方向是可解释的，很自然地会认为存在某个"基本集合"的有意义方向，更复杂的方向可以由这些方向创建。我们将这些方向称为特征（features），这就是我们想要将模型分解成的东西。有时，由于幸运的环境，单个神经元似乎是这些基本的可解释单元（参见上面的例子）。但很多时候，情况并非如此。

相反，我们将激活向量 \mathbf{x}^j 分解为更一般特征的组合，这些特征可以是任何方向：

\mathbf{x}^j \approx \mathbf{b} + \sum_i f_i(\mathbf{x}^j) \mathbf{d}_i
(1)**

其中 \mathbf{x}^j 是数据点 j 的长度为 d_{\rm MLP} 的激活向量，f_i(\mathbf{x}^j) 是特征 i 的激活，每个 \mathbf{d}_i 是激活空间中的单位向量，我们称之为特征 i 的方向（direction），\mathbf{b} 是偏置。虽然这不是本文的重点，我们也可以想象以这种方式分解模型潜在状态或激活的其他部分。例如，我们可以将此分解应用于残差流（residual stream）（参见例如 ），或注意力头的 keys 和 queries，或它们的输出。注意这个分解并不新鲜：它只是字典学习中常见的线性矩阵分解。

在我们的稀疏自编码器设置中，特征激活是编码器的输出

f_i(x) = \text{ReLU}( W_e (\mathbf{x} - \mathbf{b}_d) + \mathbf{b}_e )_i,

其中 W_e 是编码器的权重矩阵，\mathbf{b}_d, \mathbf{b}_e 是预编码器偏置和编码器偏置。特征方向是解码器权重矩阵 W_d 的列。（参见 [appendix](index.html#appendix-autoencoder) 了解完整符号。）

如果存在这样的稀疏分解，它提出了一个重要问题：模型在某种意义上是由特征组成的，还是特征只是一种方便的事后描述？在本文中，我们采取不可知论的立场，尽管我们关于特征普遍性（feature universality）的 [results](index.html#phenomenology-universality) 表明，特征的存在超越了单个模型。

#### Superposition Hypothesis

要看看这个分解与叠加（superposition）的关系，回想一下叠加假设假设神经网络"想要表示的特征比它们拥有的神经元更多"。我们认为这是通过一种"噪声模拟"（noisy simulation）发生的，其中小型神经网络利用特征稀疏性和高维空间的性质来近似模拟更大、更稀疏的神经网络。

![Figure 2](images/figure_002.png)

这意味着我们应该期望特征方向形成一个过完备基（overcomplete basis）。也就是说，我们的分解应该比神经元有更多的方向 \mathbf{d}_i。此外，特征激活应该是稀疏的，因为稀疏性使得这种噪声模拟成为可能。这在数学上等同于经典的字典学习问题。

### [What makes a good decomposition?](index.html#problem-setup-good-decomposition)

假设存在一个字典，使得每个数据点的 MLP 激活实际上可以很好地近似为方程 1 中的特征的稀疏加权和。如果满足以下条件，该分解将对解释神经网络有用：

- 我们可以解释每个特征激活的条件。也就是说，我们有一个关于哪些数据点 j 导致特征激活（即哪些 f_i(\mathbf{x}^j) 较大）的描述，这个描述在多样化数据集上有意义（包括可能用于测试假设的合成或离分布样本）。这个性质与 Cammarata 等人 讨论的 Causality、Generality 和 Purity 的期望密切相关，这些提供了一个如何在特定实例中使这个性质具体化的例子。
- 我们可以解释每个特征的下游效应，即改变 f_i 的值对后续层的影响。这应该与 (1) 中的解释一致。
- 这些特征解释了 MLP 层功能的很大一部分（通过 loss 衡量；参见 [How much of the model does our interpretation explain](index.html#global-analysis-how-much)？）。

满足这些标准的特征分解将使我们能够：

- 确定特征在特定示例上对层输出和下一层激活的贡献。
- 监控网络以检测特定特征的激活（参见例如关于 [safety-relevant features](../july-update/index.html#safety-features) 的推测）。
- 通过改变某些特征的值，以可预测的方式改变网络的行为。在多层模型中，这看起来像是通过改变早期层中的特征激活来可预测地影响某一层。
- 证明网络已经学习了数据的某些属性。
- 证明网络在特定示例上产生输出时使用了数据的给定属性。这与 influence functions 提供的证据在精神上是相似的。
- 设计用于激活给定特征并引发特定输出的输入。

当然，将模型分解为组件只是机械可解释性工作的开始！它为我们提供了模型内部运作的立足点，使我们能够认真开始解开电路（circuits）并建立对模型更大规模的理解。

### [Why not use architectural approaches?](index.html#why-not-architectures)

在 [Toy Models of Superposition](https://transformer-circuits.pub/2022/toy_model/index.html) 中，我们强调了几种解决叠加问题的不同方法。其中一种方法是设计模型，使其一开始就不存在叠加。

最初，我们认为这可能是可行的，但会带来很大的性能损失（即产生具有更大 loss 的模型）。即使这种性能损失太大，在实践中无法用于真实模型，我们也觉得成功创建 monosemantic 模型对研究非常有用，而且在很多方面，这感觉是下游分析"最干净"的方法。

不幸的是，在花费了大量时间研究这种方法后，我们最终得出结论，它在根本上是不可行的。

特别是，我们多次尝试在训练过程中诱导激活稀疏性（activation sparsity），以产生没有叠加的模型，甚至训练具有 1-hot 激活的模型。这确实消除了叠加，但它未能产生清晰可解释的神经元！具体来说，我们发现即使在没有叠加的情况下，单个神经元也可能是多义的（polysemantic）。这是因为在许多情况下，模型通过多义地表示多个特征（在一个多义神经元中）比单义地表示单个特征而忽略其他特征能达到更低的 loss。

要理解这一点，考虑一个具有单个神经元的玩具模型，在具有四个互斥特征（A/B/C/D）的数据集上训练，每个特征对下一个 token 做出不同的（正确的）预测，以相同的方式标记。进一步假设这个神经元的输出是二元的：它要么激发，要么不激发。当它激发时，它产生一个表示不同可能的下一个 token 概率的输出向量。

我们可以计算这个模型在几种情况下的交叉熵 loss：

- 假设神经元只在特征 A 上激发，并且在激发时正确预测 token A。模型忽略所有其他特征，当特征 A 不存在时，预测 token B/C/D 上的均匀分布。在这种情况下，loss 是 \frac{3}{4}\ln 3 \approx 0.8。
- 相反，假设神经元在特征 A 和 B 上都激发，预测 A 和 B token 上的均匀分布。当 A 和 B 特征不存在时，模型预测 C 和 D token 上的均匀分布。在这种情况下，loss 是 \ln 2 \approx 0.7。

因为情况 (2) 的 loss 低于情况 (1)，所以模型通过使其唯一的神经元多义来获得更好的性能，即使没有叠加。

这个例子最初可能看起来无趣，因为它只涉及一个神经元，但它实际上指向了高度稀疏网络的一个普遍问题。如果我们将激活稀疏性推到极限，每次只有一个神经元激活。我们现在可以考虑那个单个神经元以及它激发的情况。如前所述，该神经元仍然可以是多义的。

基于这个推理和我们的实验结果，我们认为在交叉熵 loss 上训练的模型通常会更倾向于多义地表示更多特征，而不是单义地表示更少的"真实特征"，即使在稀疏性约束使叠加不可能的情况下也是如此。

在其他 loss 函数下训练的模型不一定存在这个问题。例如，在均方误差 loss (MSE) 下训练的模型对于多义和单义表示可能达到相同的 loss（例如 ），并且对于某些特征重要性曲线，它们可能更倾向于单义解。但语言模型不是用 MSE 训练的，因此我们不认为架构改变可以用来创建完全 monosemantic 的语言模型。

然而，注意在训练后学习分解模型时，我们确实使用了 MSE loss（在激活和它们在字典中的表示之间），所以稀疏性可以抑制叠加在所学字典中形成。（否则，我们可能会有"一直到底"的叠加。）

### [Using Sparse Autoencoders To Find Good Decompositions](index.html#setup-autoencoder-motivation)

有一个长期存在的假设，即世界上的许多自然潜在变量都是稀疏的（参见 ，"Why Sparseness?"部分）。虽然我们对语言模型中存在的特征理解有限，但我们确实有的例子（例如 ）暗示了高度稀疏的变量。我们在 Toy Models of Superposition 上的工作 表明，一大组稀疏特征可以用低维空间中的方向来表示。

因此，我们寻求一个稀疏且过完备的分解。这本质上是 [sparse dictionary learning](https://en.wikipedia.org/wiki/Sparse_dictionary_learning) 的问题。（注意，由于我们只要求激活的稀疏分解，我们不使用 \mathbf{d}_i 对模型输出的下游效应。这意味着我们将在后面的部分中使用这些下游效应作为对所发现特征的一种验证。）

理解为什么使问题过完备——这最初听起来可能是一个微不足道的改变——实际上使这个设置与文献中寻求稀疏解缠的类似方法非常不同，这一点很重要。这与为什么字典学习是一个如此不平凡的操作密切相关；事实上，正如我们将看到的，这完全是可能的，这有点令人惊讶。字典学习的核心是一个内部问题：给定特征方向 \mathbf{d}_i，为每个数据点 \mathbf{x} 计算特征激活 f_i(\mathbf{x})。从表面上看，这个问题似乎是不可能的：我们要求从低维投影确定高维向量。换句话说，我们试图反转一个非常矩形的矩阵。唯一使之可能的是我们正在寻找一个稀疏的高维向量！这是著名的且经过充分研究的 [compressed sensing](https://en.wikipedia.org/wiki/Compressed_sensing) 问题，其精确形式是 NP-hard 的。可以将高维稀疏结构存储在低维空间中，但恢复它很困难。

尽管困难，还是有一系列复杂的字典学习方法（例如 ）。这些方法通常涉及优化松弛问题或进行贪婪搜索。我们尝试了几种这些经典方法，但最终决定专注于一种更简单的字典学习的稀疏自编码器近似（类似于 Sharkey 等人 ）。这有两个原因。首先，稀疏自编码器可以轻松扩展到非常大的数据集，我们认为这对于表征在大型多样化语料库上训练的模型中存在的特征是必要的。对于本文中讨论的模型，我们在 80 亿数据点上训练了自编码器。其次，我们担心迭代字典学习方法可能 ["too strong"](../may-update/index.html#dictionary-worries)，在某种意义上能够从激活中恢复模型本身无法访问的特征。精确的压缩感知是 NP-hard 的，神经网络肯定没有这样做。相比之下，稀疏自编码器在架构上与语言模型中的 MLP 层非常相似，因此从叠加中恢复特征的能力应该相似。

### [Sparse Autoencoder Setup](index.html#setup-autoencoder)

我们在这里简要概述稀疏自编码器的架构和训练，并在 [Basic Autoencoder Training](index.html#appendix-autoencoder) 中提供更多细节。我们的稀疏自编码器是一个模型，在输入处有偏置，编码器是带有偏置和 ReLU 的线性层，然后解码器是另一个线性层和偏置。在玩具模型中，我们发现偏置项对自编码器的性能非常重要。我们将输入和输出中应用的偏置绑定，因此结果相当于从所有激活中减去固定偏置，然后使用仅在编码器激活前具有偏置的自编码器。

我们使用 Adam 优化器训练这个自编码器，以重建我们 transformer 模型的 MLP 激活，使用 MSE 注意，使用 MSE loss 避免了我们在上面 [Why Not Architectural Approaches?](index.html#why-not-architectures) 中讨论的多义性挑战 loss 加上 L1 惩罚以鼓励稀疏性。

在训练自编码器时，我们发现一些原则非常重要。首先，规模真的很重要。我们发现在更多数据上训练自编码器使特征主观上更"锐利"和更可解释。最后，我们决定对自编码器使用 80 亿训练点（参见 [Autoencoder Dataset](index.html#appendix-autoencoder-dataset)）。

其次，我们发现在训练过程中，一些神经元停止激活，即使在大量数据点上也是如此。我们发现在训练过程中"重采样"（resampling）这些死亡神经元可以给出更好的结果，允许模型为给定的自编码器隐藏层维度表示更多特征。我们的重采样过程在 [Neuron Resampling](index.html#appendix-autoencoder-resampling) 中详细说明，但简而言之，我们定期检查在大量步骤中没有激发的神经元，并将死亡神经元上的编码器权重重置为匹配自编码器当前表示不佳的数据点。

对于希望应用此方法的读者，我们提供了一个附录，其中包含 [Advice for Training Sparse Autoencoders](index.html#appendix-autoencoder)。

#### How can we tell if the autoencoder is working?

通常在机器学习中，我们可以通过查看易于测量的量（如测试 loss）来很容易地判断方法是否有效。我们花了很多时间寻找一个等效的度量来指导我们的努力，不幸的是还没有找到任何令人满意的东西。

我们开始寻找 [an information-based metric](../may-update/index.html#simple-factorization)，以便在某种意义上说，最好的分解是使自编码器和数据的总信息最小化的那个。不幸的是，这个总信息通常与主观特征可解释性或激活稀疏性不相关。（特征激活的平均 L0 范数为数百但重建误差较低的运行，可能比平均 L0 范数较小但重建误差较高的运行具有更低的总信息。）

因此，我们最终使用几个额外度量的组合来指导我们的研究：

- 手动检查：特征看起来可解释吗？
- 特征密度：我们发现"活跃"特征的数量和它们激发的 token 百分比是一个非常有用的指导。（参见附录了解 [details](index.html#appendix-feature-density)。）
- 重建 loss：自编码器重建 MLP 激活的效果如何？我们的目标最终是解释 MLP 层的功能，所以 MSE loss 应该很低。
- 玩具模型：拥有我们知道真实情况的玩具模型，因此可以清晰地评估自编码器的性能，这对我们早期的进展至关重要。

解释或测量其中一些信号可能很困难。例如，在某些时候，我们认为我们看到了一些最初没有任何意义的特征，但经过更深入的检查，我们 [could understand](index.html#features-seem-like-bugs)。同样，虽然我们已经确定了特征密度分布的一些期望，但仍有很多我们不理解的地方，这使得这不能提供清晰的进展信号。

我们认为，如果我们能够为从 transformer 上训练的稀疏自编码器的字典学习解决方案识别更好的度量，将会非常有帮助。

### [The (one-layer) model we're studying](index.html#setup-transformer)

我们选择研究一个单层 transformer 模型。我们将这个模型视为字典学习的试验台，在这个角色中，它带来了三个关键优势：

- 因为单层模型很小，它们可能比更大的模型有更少的"真实特征"，这意味着较小字典学到的特征可能覆盖它们的所有"真实特征"。较小的字典训练成本更低，允许快速的超参数优化和实验。
- 我们可以非常便宜地过度训练单层 transformer。我们假设非常高数量的训练 tokens 可能允许我们的模型在叠加中学习更清晰的表示。
- 我们可以轻松分析特征对 logit 输出的影响，因为这些在特征激活中近似线性。注意，这种线性结构使得特征应该是线性的可能性更大。一方面，这意味着线性表示假设对这个模型更可能成立。另一方面，它可能意味着我们的结果不太可能推广到多层模型。幸运的是，其他人已经用稀疏自编码器研究了多层 transformer 并发现了可解释的线性特征，这让我们更有信心，我们在单层模型中看到的东西确实可以推广。这提供了有益的确证，即我们发现的特征不仅仅告诉我们数据分布，实际上 [reflect the functionality of the model](index.html#global-analysis-about-model)。

我们训练了两个具有相同超参数和数据集的单层 transformer，仅在初始化时使用的随机种子不同。然后我们在两个 transformer 上学习了许多不同大小的字典，对每对匹配的字典使用相同的超参数，但在每个 transformer 的不同 token 激活上训练。

我们将本文中研究的主要 transformer 称为"A"transformer。我们主要使用另一个 transformer（"B"）来研究 [feature universality](index.html#phenomenology-universality)，因为我们可以例如比较从"A"和"B"transformer 学到的特征，看看它们有多相似。

### [Notation for Features](index.html#setup-notation)

在整个草稿中，我们将使用像"A/1/2357"这样的字符串来表示特征。第一部分"A"或"B"表示特征来自哪个模型。第二部分（例如"A/1"中的"1"）表示字典学习运行。这些在学习因子的数量和使用的 L1 系数上有所不同。所有运行的表格可以在 [here](vis/index.html) 找到。值得注意的是，A/0...A/5 形成一个序列，具有固定的 L1 系数和递增的字典大小。最后一部分（例如"A/1/2357"中的"2357"）对应于运行中的特定特征。

有时，我们想表示 transformer 中的神经元，而不是稀疏自编码器学到的特征。在这种情况下，我们使用符号"A/neurons/32"。

### [Interface for Exploring Features](index.html#setup-interface)

我们提供了一个接口来探索所有字典学习运行中的所有特征。每个运行的可视化链接可以在 [here](vis/index.html) 找到。我们建议从 [interface for A/1](vis/a1.html) 开始，我们讨论得最多。

这些接口为每个特征提供大量信息。这包括它们何时激活的示例，当它们激活时对 logits 有什么影响，如果特征被消融（ablated），它们如何影响 token 概率的示例，等等：

![Figure 3](images/figure_003.png)

我们的接口还允许用户搜索特征：

![Figure 4](images/figure_004.png)

此外，我们提供了 [second ](vis/index.html#example-texts)[interface](vis/index.html#example-texts)，显示给定数据集示例上激活的所有特征。这适用于一组示例文本。

![Figure 5](images/figure_005.png)

## [Detailed Investigations of Individual Features](index.html#feature-analysis)

我们论文最重要的声明是，字典学习可以提取比神经元显著更 monosemantic 的特征。在本节中，我们对一小部分在高度特定上下文中激活的特征给出了这个声明的详细演示。

我们研究的特征响应以下内容：

- 用阿拉伯字母书写的文本（如"الكتاب المختصر في حساب الجبر والمقابلة"）
- DNA 序列（如"CCTGGTACTGTACGAACGAACGAACGTAGCCTTGG"）
- base64 字符串（如"https://www.youtube.com/watch?v=dQw4w9WgXcQ"中的最后字符）
- 用希伯来字母书写的文本（如"בראשית ברא אלהים את השמים ואת הארץ"）

对于每个学到的特征，我们尝试建立以下声明：

- 学到的特征对假设的上下文具有高特异性（specificity）激活。（当特征开启时，上下文通常存在。）
- 学到的特征对假设的上下文具有高敏感性（sensitivity）激活。（当上下文存在时，特征通常开启。）
- 学到的特征引起适当的下游行为。
- 学到的特征不对应于任何神经元。
- 学到的特征是普遍的（universal）——通过对不同模型应用字典学习发现相似的特征。

为了证明声明 1-3，我们为每个上下文设计了计算代理（computational proxies），即数值分数，估计字符串（或 token）来自特定上下文的（对数）可能性。上面选择的上下文很容易基于所涉及的 Unicode 字符的定义集来建模。我们将 DNA 序列建模为来自 [ATCG] 的字符的随机字符串，将 base64 字符串建模为来自 [a-zA-Z0-9+/] 的字符的随机序列。对于阿拉伯字母和希伯来字母特征，我们利用每种语言都是用具有明确定义的 Unicode 块的字母书写的事实。每个计算代理然后是对 \log(P(s|\text{context}) / P(s)) 的估计，在假设下与在数据集的完整经验分布下的比率。关于如何为每个特征假设估计这个比率的完整描述在 [appendix section on proxies](index.html#appendix-proxies) 中给出。

在本节中，我们主要研究在每个上下文中最活跃的学到的特征。通常还有其他特征也对那个上下文建模，我们发现主要特征敏感性的罕见"空白"通常由另一个特征的活动解释。我们在关于 [Activation Sensitivity](index.html#feature-arabic-sensitivity) 和 [Feature Splitting](index.html#phenomenology-feature-splitting) 的部分中详细讨论了这个现象。

我们努力证明每个特征的特异性，因为我们认为这对于排除多义性更为重要。多义性通常涉及神经元对明显不相关的概念激活。例如，我们 transformer 模型中的 [one neuron](vis/a-neurons.html%3Fordering=index.html#feature-83) 响应学术引用、英语对话、HTTP 请求和韩语文本的混合。在视觉模型中，有一个经典例子，一个神经元响应猫脸和汽车前部。如果我们的代理显示特征只在一些相对罕见和特定的上下文中激活，这将排除典型形式的多义性。

![Figure 6](images/figure_006.png)

我们最后注意到，本节中的特征是经过精心挑选的，以便更容易分析。定义简单计算代理对于我们发现的大多数特征（例如关于 [fantasy games](vis/a1.html%3Fsearch_target_mode=index_name&amp;search_mode=case_insensitive.html#feature-129) 的文本）会很困难，我们在 [following section](index.html#global-analysis) 中以其他方式分析它们。

### [Arabic Script Feature](index.html#feature-arabic)

我们要考虑的第一个特征是阿拉伯字母特征，[A/1/3450](vis/a1.html#feature-3450)。它响应阿拉伯语、波斯语、乌尔都语（可能还有其他语言）的文本激活，这些语言使用阿拉伯字母。这个特征非常具体，对阿拉伯字母相对敏感，如果我们从单个神经元的角度查看模型，它实际上是看不见的。

#### [Activation Specificity](index.html#feature-arabic-activations)

我们的第一步是表明这个特征几乎只在阿拉伯字母文本上激发。我们使用估计的可能性比率 \log(P(s|\text{Arabic Script}) / P(s)) 给每个 token 一个"阿拉伯字母"分数，并按该分数分解特征激活的直方图。阿拉伯语文本在我们的整体数据分布中相当罕见——仅占训练 tokens 的 0.13%——但它占我们特征激活的 tokens 的 81%。这个百分比随特征活动水平而变化，从特征 barely active 时的 25% 到特征激活高于 5 时的 98%。

![Figure 7](images/figure_007.png)
我们还展示了数据集示例，展示了不同级别的特征活动。在解释它们时，重要的是要注意阿拉伯语 Unicode 字符通常被分割成多个 tokens。例如，字符 ث ([U+062B](https://www.compart.com/en/unicode/U+062B)) 被分词为 \xd8 后跟 \xab。这种分割分词对于拉丁字母以外的 Unicode 字符和其他 Unicode 块中最常见的字符很常见。当这种情况发生时，A/1/3450 通常只在 Unicode 字符的最后一个 token 上触发。

激活谱的上部，高于约 5 的活动水平，清楚地显示出对阿拉伯脚本的高特异性响应。我们应该如何看待较低的部分？我们有三个假设：

- 代理不完美。它有假阴性，因为常见字符在其他 Unicode 块中（例如，空格、标点符号），也由于分词产生奇怪行为的地方。例如，在上图中，有一个换行符 ⏎ 我们的特征会触发，但我们的代理分配的低分数，因为它在 Unicode 块之外。
- 模型可能不完美（但仍然校准）。如果特征激活与它们对某些属性存在的"置信度"成比例，那么我们应该期望它们在弱激活时有时会出错。虽然未能识别文本是哪种语言看起来很愚蠢，但这是一个非常弱的单层 transformer 模型，而且字符经常被分割成多个 tokens 增加了额外的难度。
- 自编码器可能不完美：如果自编码器的宽度小于模型使用的"真实特征"数量，那么未恢复的特征可能会作为低激活出现在许多学习特征中。

无论如何，大特征激活对模型预测有更大的影响，为什么我们相信大激活有更大的影响？在我们本文中考虑的单层 transformer 的情况下，我们可以为此提供一个强有力的论据：特征对 logits 有线性影响（通过对层归一化重新缩放），因此特征的更大激活对 logits 有更大的影响。在更大模型的情况下，这遵循许多猜想和启发式论证（例如模型中大量线性路径和每层线性特征的想法），并且通过连续性对于足够小的激活必须为真，但没有无懈可击的论证。所以正确理解它们最重要。评估低激活水平假阳性影响的一个有用工具是 Cammarata 等人的"期望值图"。我们绘制了按激活水平加权的特征激活分布。该特征提供的大部分激活幅度来自阿拉伯脚本中的数据集示例。

![Figure 8](images/figure_008.png)

#### [激活敏感性](index.html#feature-arabic-sensitivity)

在上面的特征激活分布中，很明显 A/1/3450 对阿拉伯脚本中的所有 tokens 都不敏感。在随机数据集示例中，它未能在五个前缀"ال"示例上触发，音译为"al-"，相当于英语中的定冠词"the"。然而，恰恰在这些地方，另一个特定于阿拉伯脚本的特征 [A/1/3134](vis/a1.html#feature-3134) 触发。还有几个额外的特征在阿拉伯语和相关脚本上触发（例如 [A/1/1466](vis/a1.html#feature-1466)、[A/1/3134](vis/a1.html#feature-3134)、[A/1/3399](vis/a1.html#feature-3399)），有助于表示阿拉伯脚本。另一个例子涉及 Unicode 分词：当阿拉伯字符被分割成多个 tokens 时，我们这里分析的特征仅在构成字符的最后一个 token 上激活，而 [A/1/3399](vis/a1.html#feature-3399) 在构成字符的第一个 token 上激活。要查看这些特征如何协作，我们提供了一个 [替代可视化](vis/a1-ar.html)，显示在一段阿拉伯文本上激活的所有特征。我们在下面的 [现象学](index.html#phenomenology) 部分更多地考虑这种交互。

尽管如此，我们在 4000 万个 token 的数据集上发现，我们的特征活动与阿拉伯脚本代理的活动（阈值设为 0）之间的 Pearson 相关性为 0.74。相关性提供了考虑幅度的敏感性和特异性的联合度量，0.74 是一个相当大的相关性。

#### [特征下游效应](index.html#feature-arabic-effect)

因为自编码器是在模型激活上训练的，理论上它学习的特征可能仅代表训练数据中的结构，与网络的功能无关。我们反而表明，学习的特征对模型输出有可解释的因果效应，这些效应在特征激活的背景下是有意义的。注意，这些下游效应不是字典学习过程的输入，后者只看到 MLP 层的激活。如果由此产生的特征也介导重要的下游行为效应，那么我们可以确信特征真正连接到 MLP 在网络中的功能角色，而不仅仅是底层数据的属性。

我们从每个特征对模型 logits 影响的线性近似开始。我们按照 的路径展开方法计算 logit 权重（也称为"logit 归因"，参见类似工作例如 ），将每个特征方向乘以 MLP 输出权重，层归一化操作的近似值结合了去除均值的投影和对角矩阵近似缩放项，以及 unembedding 矩阵 (d_iW_{down}\pi L W_{unembed})。因为 softmax 函数是平移不变的，logit 权重没有绝对尺度；我们平移这些，使每个特征的中位数 logit 权重为零。

每个特征在激活时，使一些输出 token 更可能，一些输出 token 更不可能。我们绘制了 logit 权重的分布。我们排除了对应于极其罕见或从未使用过的词汇元素的权重。这些可能类似于 Rumbelow & Watkins 的"异常 tokens"（例如，"SolidGoldMagikarp"）。在零处有一个大的主模式，在最右侧有一个小得多的第二模式，当我们的特征开启时，其可能性最增加的 tokens。这个第二模式似乎对应于阿拉伯字符，以及有助于表示阿拉伯脚本字符的 tokens（尤其是 \xd8 和 \xd9，它们通常是 [基本阿拉伯语 Unicode 块](https://www.compart.com/en/unicode/block/U+0600) 中阿拉伯语 Unicode 字符的 UTF-8 编码的前半部分）。

![Figure 9](images/figure_009.png)

这表明激活此特征会增加网络预测阿拉伯脚本 tokens 的概率。理论上有几种方法 logit 权重可能高估模型对特征的实际使用：1. 可能这些输出权重足够小，当乘以激活时，它们对模型的输出没有明显影响。2. 特征可能只在其他特征使这些 tokens 极不可能的情况下激活，因此特征实际上几乎没有影响。3. 我们线性化层归一化的近似（见 Framework）可能很差。基于随后的分析，证实了 logit 权重效应，我们不认为这些问题在实践中出现。

为了可视化这些效应对实际数据的影响，我们 [因果地](index.html#appendix-feature-ablations)[消融](index.html#appendix-feature-ablations)[特征](index.html#appendix-feature-ablations)。对于给定的数据集示例，我们将上下文运行到模型直到 MLP 层，将激活解码为特征，然后减去 [A/1/3450](vis/a1.html#feature-3450) 的激活，人为地将其在整个上下文中设为零，然后再应用模型的其余部分。我们使用下划线可视化消融特征的效果；预测被特征帮助的 tokens（消融降低可能性）用蓝色下划线，预测被特征损害的 tokens（消融增加可能性）用红色下划线。

在右侧的示例中，我们看到 [A/1/3450](vis/a1.html#feature-3450) 在短上下文中的每个 token 上都激活（橙色背景）。消融它损害了阿拉伯脚本中所有 tokens 的预测（紫色下划线），但帮助了句号 . 的预测（橙色下划线）。图的其余部分显示了来自两个不同特征激活水平范围的上下文。（右侧示例中间 token 的特征激活（"子样本间隔 5"）大约是左侧示例中间 token（"子样本间隔 0"）的一半。）我们看到特征在整个范围内因果地帮助模型对阿拉伯脚本的预测，特征唯一使可能性降低的 tokens 是与其他脚本共享的标点符号。当特征更活跃时，影响的幅度更大。

![Figure 10](images/figure_010.png)

我们鼓励感兴趣的读者查看 [A/1](vis/a1.html) 的特征可视化，以查看此效应和其他效应。

我们还通过将特征活动"固定"在高值从模型采样，验证特征的下游效应与我们的阿拉伯脚本特征解释一致。为此，我们从前缀 1,2,3,4,5,6,7,8,9,10 开始，模型有一个预期的延续（请记住，这是一个非常弱的单层模型！）。然后我们将 [A/1/3450](vis/a1.html#feature-3450) 设置为其最大观察值，看看这如何改变样本：

![Figure 11](images/figure_011.png)

#### [特征不是神经元](index.html#feature-arabic-neuron)

这个特征看起来相当 monosemantic，但一些模型有相对 monosemantic 的神经元，我们想检查字典学习是否只是给了我们一个特别好的神经元。当然，一些特征可能真的是神经元对齐的。但我们想知道至少字典学习发现的一些特征不是平凡的。我们首先注意到，当我们 [搜索](vis/a-neurons.html%3Fsearch_mode=regex_case_sensitive&amp;ordering=count&amp;search_text=[\u0600-\u06FF]+.html) 神经元在其 top 20 个数据集示例中有阿拉伯脚本时，只有一个神经元出现，有一个阿拉伯脚本示例。（其余 18 个示例是英语，一个是西里尔文。）

然后我们查看特征在神经元基中的系数，发现按幅度最大的三个系数都是负的 (!)，总共有 27 个神经元的系数幅度至少为 0.1。

![Figure 12](images/figure_012.png)

当然，这些神经元可能参与微妙的抵消游戏，导致一个特定神经元的主要激活被锐化。为了检查这一点，我们找到在约 4000 万个数据集示例上与特征激活最相关的神经元。我们还尝试查看对特征字典向量贡献最大的神经元。然而，我们发现查看最相关的神经元更可靠——在早期实验中，我们发现罕见情况下相关方法找到看似相似的神经元，而字典方法没有。这可能是因为神经元可以有不同的激活尺度。最相关的神经元 ([A/neurons/489](vis/a-neurons.html#feature-489)) 响应不同非英语语言的混合。这作为 superposition 策略是有意义的：因为语言本质上是互斥的，它们自然可以相互放在 superposition 中。我们可以通过可视化神经元的激活分布来看出这一点——数据集示例都是其他语言，阿拉伯脚本只存在一小部分。

![Figure 13](images/figure_013.png)

Logit 权重分析也与这个神经元响应语言混合一致。例如，在下图中，许多 top logit 权重似乎包括俄语和韩语 tokens。细心的读者会观察到分布中对应于罕见阿拉伯脚本 tokens 的薄红色条。这些阿拉伯脚本 tokens 的权重值总体上略微偏向正，但有些是负的。

![Figure 14](images/figure_014.png)

最后，散点图和相关性表明 [A/1/3450](vis/a1.html#feature-3450) 和神经元之间的相似性非零，但非常小。通过类比，这也适用于 [B/1/1334](vis/b1.html#feature-1334)。特别是，注意 logit 权重散点图的 y 轴（对应于特征）如何清晰地分离阿拉伯脚本 token logits，而 x 轴没有。更一般地说，注意 y 边缘都清楚地表现出特异性，但 x 边缘没有。

![Figure 15](images/figure_015.png)

我们得出结论，我们研究的特征不简单地对应于单个神经元。如果我们只根据神经元分析模型，阿拉伯脚本特征将有效地不可见。

#### [普遍性](index.html#feature-arabic-universality)

我们现在将询问 A/1/3450 是否是一个 universal 特征，在其他模型中形成，并可以被字典学习一致地发现。这将表明我们正在发现关于单层 transformer 如何学习数据集表示的更一般的东西。

我们在 [B/1](vis/b1.html) 中搜索类似特征，这是在相同数据集上训练但具有不同随机种子的 transformer 上的字典学习运行。我们搜索具有最高激活相关性的特征，"激活相关性"定义为在 40,960,000 个 tokens 上的激活与 [A/1/3450](vis/a1.html#feature-3450) 具有最高 Pearson 相关性的特征，找到 [B/1/1334](vis/b1.html#feature-1334) (corr=0.91)，它惊人地相似：

![Figure 16](images/figure_016.png)

这个特征也清楚地响应阿拉伯脚本。如果有的话，它比我们的原始特征更好——它在 0-1 范围内更特异。logit 权重讲述了类似的故事：

![Figure 17](images/figure_017.png)

消融这个特征的效果也与此一致（参见 [B/1/1334](vis/b1.html#feature-1334) 的可视化）。

为了更系统地分析 A 和 B 之间的相似性，我们查看散点图比较激活或 logit 权重：

![Figure 18](images/figure_018.png)

激活强烈相关（Pearson 相关性为 0.91），特别是在主阿拉伯模式中。

Logit 权重揭示了我们在 A/1 的直方图中看到的双峰性的二维版本，阿拉伯 tokens 的 logit 权重聚集在右上角。相关性比激活的相关性更适度，因为分布由中心相对不相关的模式主导。我们假设这个中心模式对应于"权重干扰"，共享的离群模式是重要的观察结果——也就是说，模型理想情况下可能希望所有这些权重为零，但由于与其他特征及其权重的 superposition，这是不可能的。

### [DNA 特征](index.html#feature-dna)

我们现在考虑一个 DNA 特征，[A/1/2937](vis/a1.html#feature-2937)。它响应由 A、T、C 和 G 组成的长大写字符串而激活，通常用于表示核苷酸序列。我们密切遵循上面阿拉伯脚本特征的分析，以显示特征的激活特异性和敏感性、合理的下游效应、缺乏神经元对齐以及模型之间的普遍性。主要区别将是 (1) [A/1/2937](vis/a1.html#feature-2937) 是专门用于建模 DNA 上下文的唯一特征，(2) 我们的代理对 DNA 的敏感性不如我们的特征，错过包含标点符号、空格和缺失碱基的字符串。

#### [激活特异性和敏感性](index.html#feature-dna-activations)

我们从"是 DNA 序列"的计算代理开始，\log(P(s|\text{DNA}) / P(s))。因为有一些词汇 tokens，例如 CAT，可能出现在 DNA 中，但也出现在其他上下文中，我们在评估代理时总是查看至少两个 tokens 的组。log 概率结果是非常双峰的，所以我们将代理二值化（基于其符号）。这个二值化代理与特征激活的 Pearson 相关性为 0.8。

![Figure 19](images/figure_019.png)

虽然特征在特征的较高区域看起来相当 monosemantic（所有 10 个约 6.0 激活的随机数据集示例都是 DNA 序列），但有大量蓝色表示 DNA 代理在较低区域未触发。下面我们在四个激活水平（包括特征关闭）显示随机示例网格，代理触发和不触发。

![Figure 20](images/figure_020.png)

我们注意到，在特征和代理不同意的所有但两个案例中，特征确实指示 DNA 序列，只是在我们代理严格的 ATCG 词汇之外。例如，三联体 TGG AGT 中存在的空格使代理未能触发。该特征还在字符串 5'-TCT 中的'-上有效地触发，因为该前缀之后应该是 DNA，即使前缀本身不是 DNA。（因果消融显示关闭 DNA 特征会损害后续字符串的预测。）因此我们相信 [A/1/2937](vis/a1.html#feature-2937) 对 DNA 非常敏感和特异。代理触发而特征未触发的情况确实是 DNA 序列，尽管特征在下一个 token 上开始触发。我们观察到 DNA 特征可能不会在 DNA 序列的前几个 tokens 上触发，[但在长 DNA 序列结束时](vis/a1-dna.html)，它是唯一激活的特征。

#### [特征下游效应](index.html#feature-dna-effect)

DNA 特征激活的下游效应，通过 logit 权重测量，是有意义的，所有 top tokens 都是核苷酸的组合，如 AGT 和 GCC。

![Figure 21](images/figure_021.png)

#### [特征不是神经元](index.html#feature-dna-neuron)

与 [A/1/2937](vis/a1.html#feature-2937) 最相似的神经元，通过激活相关性测量，是 [A/neurons/67](vis/a-neurons.html#feature-67)。DNA 上下文形成该神经元激活示例的一小部分。我们特征向量中系数最高的神经元，[A/neurons/227](vis/a-neurons.html#feature-227)，在其 top 激活示例中也没有 DNA 序列。

![Figure 22](images/figure_022.png)

#### [普遍性](index.html#feature-dna-universality)

[A/1/2937](vis/a1.html#feature-2937) 在运行 B/1 中有一个相关特征 (corr=0.92)，[B/1/3680](vis/b1.html#feature-3680)。它们的 top logit 权重一致，都是 DNA tokens（例如 AGT），形成一个单独的模式（右侧圈出），而不是两者的 logit 权重主体。

![Figure 23](images/figure_023.png)

### [Base64 特征](index.html#feature-base64)

我们现在考虑一个 [base64](https://en.wikipedia.org/wiki/Base64) 特征，[A/1/2357](vis/a1.html#feature-2357)。我们对这个特征特别兴奋，因为我们在 SoLU 论文中发现了一个 base64 神经元，表明 base64 可能非常 universal——甚至在不同数据集和不同架构训练的模型之间。我们将 base64 字符串建模为来自 [a-zA-Z0-9+/] 的字符的随机序列。按相应计算代理着色的激活分布，以及来自每个激活水平的随机数据集示例，显示这个特征对 base64 非常特异。

![Figure 24](images/figure_024.png)

这不是在 base64 上下文中激活的唯一特征，在下面 [部分](index.html#features-seem-like-bugs-2) 我们讨论了另外两个，其中一个在 base64 上下文中的单个数字上触发（如上面的图中 A/1/2357 未激活的 2、4、7 和 9），利用 BPE 分词器的属性做出更好的预测。

转向 logit 权重，它们有第二个模式，由高 base64 特异性 tokens 组成。主模式似乎主要是干扰，但右侧偏向 base64 中性或略微 base64 倾向的 tokens。（如果我们在下面查看条件，我们看到向 base64 特异性 tokens 的更连续过渡。）

![Figure 25](images/figure_025.png)

非 base64 和 base64 tokens 之间有比我们在阿拉伯脚本示例中看到的更连续的过渡。这种差异可能出现，因为 token 在阿拉伯脚本中出现的频率是否高于其他文本是一个相对二元的区别，而 token 在 base64 或其他文本中出现的频率变化更连续。例如，fr 既是法语的常见缩写，也是 base64 token，所以模型对上调 fr 谨慎是有意义的，因为它可能已经由于在法语中的使用而有更高的先验。确实，任何由英文字母表中的字母组成的 token 都有一些非平凡的出现在 base64 字符串中的概率。

计算代理与 [A/1/2357](vis/a1.html#feature-2357) 活动之间的 Pearson 相关性仅为 0.38。我们认为这主要是因为代理太宽。例如，十六进制字符串（由 [0-9A-F] 组成）激活代理，因为它们与整体数据分布非常不同，但实际上由它们自己的特征预测，[A/1/3817](vis/a1.html#feature-3817)。

#### [普遍性](index.html#feature-base64-universality)

[A/1/2357](vis/a1.html#feature-2357) 在运行 B/1 中有一个相关特征 (corr=0.85)，[B/1/2165](vis/b1.html#feature-2165)。它对 base64 字符串也有高激活特异性：

![Figure 26](images/figure_026.png)

像 [A/1/2357](vis/a1.html#feature-2357) 一样，[B/1/2165](vis/b1.html#feature-2165) 的 logit 权重有第二个模式对应于 base64 token：

![Figure 27](images/figure_027.png)

相关性和散点图也与它们是非常相似的特征一致：

![Figure 28](images/figure_028.png)

注意，我们期望干扰和 base64 token logit 权重之间的重叠来自上述 base64 token 在许多其他上下文中的使用。

#### [特征不是神经元](index.html#feature-base64-neuron)

查看模型 A 中与这个特征最相关的神经元：[A/neurons/470](vis/a-neurons.html#feature-470) (corr=0.18)，我们发现虽然它确实显著响应 base64 字符串，但它也激活许多其他东西，包括代码、HTML 标签、URL 部分等：

![Figure 29](images/figure_029.png)

Logit 权重表明它略微增加 base64 tokens，但更专注于上调其他 tokens，例如文件名结尾。

![Figure 30](images/figure_030.png)

激活和 logit 相关性与这个神经元帮助表示相同特征一致，但主要做其他事情。

![Figure 31](images/figure_031.png)

### [希伯来特征](index.html#feature-hebrew)

另一个有趣的例子是希伯来特征 [A/1/416](vis/a1.html#feature-416)。像阿拉伯特征一样，基于 Unicode 块很容易通过计算识别希伯来文本。

[A/1/416](vis/a1.html#feature-416) 在上部谱中有高激活特异性。它确实对其他事情弱激活（特别是其他具有 Unicode 脚本的语言）。在强激活中也有一些蓝色；这似乎显著地在"常见字符"上，例如空格或标点符号，来自其他 unicode 块（在 [阿拉伯特征部分](index.html#feature-arabic-activations) 中查看更多类似问题的讨论）。

![Figure 32](images/figure_032.png)

它的 logit 权重有一个显著的第二模式，对应于希伯来字符和相关的未完成 Unicode 字符。注意 \xd7 是 [基本希伯来 Unicode 块](https://www.compart.com/en/unicode/block/U+0590) 中大多数字符的 UTF-8 编码中的第一个 token。

![Figure 33](images/figure_033.png)

希伯来脚本代理与 [A/1/416](vis/a1.html#feature-416) 的 Pearson 相关性为 0.55。一些敏感性失败可能是由于互补特征 [A/1/1016](vis/a1.html#feature-1016)，它在 \xd7 上触发并预测完成希伯来字符码点的字节。

#### [特征不是神经元](index.html#feature-hebrew-neuron)

似乎没有类似的神经元。模型 A 中最相关的神经元是 [A/neurons/489](vis/a-neurons.html%3Fordering=index.html#feature-489) (corr=0.1)，具有低激活和 logit 特异性。考虑以下激活和 logit 相关性图：

![Figure 34](images/figure_034.png)

为了交叉验证这一点，我们还 [搜索](vis/a-neurons.html%3Fsearch_mode=regex_case_sensitive&amp;ordering=count&amp;search_text=[\u0590-\u05FF].html) 了任何神经元，其中主希伯来 Unicode 块出现在 top 数据集示例中。我们没有找到任何。

#### [普遍性](index.html#feature-hebrew-universality)

[A/1/416](vis/a1.html#feature-416) 在 B/1 运行中有一个相关特征，[B/1/1901](vis/b1.html#feature-1901) (corr=0.92)，具有显著的激活特异性：

![Figure 35](images/figure_035.png)

Logit 权重有第二个模式，如前所述：

![Figure 36](images/figure_036.png)

激活和 logit 权重相关性再次一致：
![Figure 37](images/figure_037.png)

## [全局分析](index.html#global-analysis)

如果前一节已经说服你，至少有一些特征是真正可解释的，并且反映了底层模型机制，那么很自然会想知道这在那些精心挑选的特征之外有多大程度上成立。本节的主要重点是回答这个问题："其余特征的可解释性如何？"我们表明，人类和大型语言模型都认为我们的特征比神经元具有显著更高的可解释性，并且绝对意义上也相当可解释。

人们可能还会问一些其他问题。我们的字典学习方法在多大程度上发现了理解 MLP 层所需的所有特征？整体而言，MLP 层的机制有多少已经被变得可解释？我们还不能完全满意地回答这些问题，但将在本节末尾提供一些初步的推测。

我们注意到，在 A/1 自编码器的 4,096 个学习特征中，有 168 个是"死的"（在 1 亿个数据集中都没有激活），292 个是"超低密度"的，在少于百万分之一的数据集样本上激活，并表现出[其他非典型属性](index.html#appendix-feature-density)。我们在进一步分析中排除了这两组特征。

### [典型特征的可解释性如何？](index.html#global-analysis-interp)

在本节中，我们使用三种不同的方法来分析典型特征的可解释性，以及与神经元相比如何：人工分析，以及两种形式的自动化可解释性。所有三种方法都发现特征比神经元可解释得多。

#### [人工手动分析](index.html#global-analysis-interp-manual)

目前，我们没有任何比人类对可解释性的判断更值得信赖的指标。因此，我们让一位盲法标注者（作者之一，Adam Jermyn）根据可解释性对特征和神经元进行评分。评分标准可以在[附录](index.html#appendix-rubric)中找到，考虑了对解释的信心、激活与该解释的一致性、logit 输出权重与该解释的一致性，以及特异性。

在进行此评估时，我们想要避免我们在先前工作（例如）中感知到的一个弱点，即评估主要集中于最大数据集示例，而对激活谱的其余部分关注较少。许多多义神经元如果只看顶级数据集示例，看起来是单义的，但如果查看激活谱的较低部分，就会被揭示为多义的。为了避免这种情况，我们在特征激活谱上均匀采样，为了在特征激活谱上均匀采样，我们将激活谱分为 11 个"激活区间"，在 0 激活和最大激活之间均匀分布。我们从这些区间均匀采样。并针对该特征暗示的整体假设，分别对每个区间进行评分。

不幸的是，这种方法劳动密集，因此评分样本数量很小。总共在 162 个特征和神经元上评分了 412 个特征激活区间。

![Figure 38](images/figure_038.png)

我们看到特征比神经元可解释得多。非常主观地说，我们发现如果特征的标准值高于 8，它们就相当可解释。中位数神经元在我们的标准上得分为 0，表明我们的标注者甚至无法形成该神经元可能代表什么的假设！而中位数特征区间得分为 12，表明标注者有一个自信的、具体的、一致的假设，该假设在 logit 输出权重方面是有意义的。

#### [自动化可解释性 – 激活](index.html#global-analysis-interp-auto-acts)

为了在更大规模上分析特征，我们转向自动化可解释性。遵循 Bills 等人的方法，我们让一个大型语言模型（Anthropic 的 Claude）使用特征激活的 token 示例来生成特征解释。接下来，我们让模型使用该解释来预测先前未见过的 token 上的新激活。值得明确说明的是，我们的自动化可解释性设置旨在确保没有关于激活模式的信息泄露，除了解释本身。例如，在预测新激活时，模型看不到该特征的任何真实激活。

与人工分析一样，我们使用整个激活区间范围的样本来评估单义性。这与 Bills 等人的评估策略不同，他们在预测和真实激活的相关性计算中使用了最大数据集示例和随机样本的混合。对于稀疏特征（在大多数随机样本上不触发），这实际上测试了模型区分特征大激活和零激活的能力。具体来说，对于每个特征，我们计算了预测激活和 60 个数据集示例（每个示例由 9 个 token 组成）的真实激活之间的 Spearman 相关系数，每个特征产生 540 个预测。虽然只使用完全随机的序列是最原则性的评分方法，但一半的示例来自特征区间，以获得更准确的相关性。参见[附录](index.html#appendix-automated)获取更多信息，包括使用重要性评分来精确抵消提供特征触发 token 的偏差。

与人工分析一致，Claude 能够比神经元更好地解释和预测特征的激活。在 Claude 预测常数分数（通常是全 0）的情况下，无法计算相关性，我们分配零分，这解释了那里的上升。

![Figure 39](images/figure_039.png)

#### [自动化可解释性 – Logit 权重](index.html#global-analysis-interp-auto-logits)

在我们 earlier 的单个特征分析中，我们发现查看 logits 是交叉验证特征可解释性的强大工具。我们也可以在自动化可解释性中采用这种方法。使用在前一次分析中生成的特征解释，我们让语言模型预测一个先前未见过的 logit token 是否是该特征应该预测为可能下一个出现的 token。然后针对顶级 positive logit token 和随机其他 logit token 的 50/50 混合进行评分。随机猜测会给出 50% 的准确率，但模型在特征上实现了 74% 的平均准确率，而神经元的平均准确率为 58%。这里的失败是指 Claude 未能以正确的格式回复以进行评分的情况。

![Figure 40](images/figure_040.png)

#### [激活区间分析](index.html#global-analysis-interp-intervals)

除了整体研究特征外，在我们的手动分析中，我们可以使用特征区间放大特征激活谱的部分。如前所述，特征区间是激活最接近特定均匀分布的最大激活分数的示例集。因此，我们不是问一个特征是否看起来可解释，而是问一个激活范围是否与特征整个激活谱暗示的整体假设一致。这使我们能够询问可解释性如何随特征激活强度变化。

![Figure 41](images/figure_041.png)

较高激活的特征区间比较低激活的区间与我们的解释更一致。特别是：

- 许多特征在整个激活谱上显示一致的激活。
- 一些特征在激活谱的顶部约 60% 上显示一致的激活，然后当我们看向越来越小的激活时迅速变得不那么可解释。

这可能是我们的特征不太正确的信号。例如，如果我们的一个特征与我们真正想要学习的特征略有角度，这可能会在较低激活区间中表现为不一致的行为。

#### [注意事项](index.html#global-analysis-interp-caveats)

我们的手动和自动化可解释性实验有一些注意事项：

- 特征激活偏向较低区间。大多数特征激活相当小，因此落在较低（且较不可解释的）特征区间中。尽管如此，正如我们在详细分析中发现的，特征的大部分效果（关于它对模型输出的效果，参见例如 [Arabic Feature's Activations Specificity Analysis](index.html#feature-arabic-activations) 中的激活期望值图）是由于其较高激活，这些是相当可解释的。
- 评估的特征是从所有特征集中均匀采样的，可解释性可能与重要性相关。人们可以想象评估具有最大激活幅度或最大消融效果的特征。我们的感觉是，这些会比我们考虑的随机采样特征更可解释。人们可以想象一种情况，其中最重要的特征在某种意义上系统地较不可解释，尽管对[最活跃特征](vis/a1.html%3Fordering=max_dense.html)的检查表明情况相反。

基于我们对可视化中许多特征的检查，我们认为这些注意事项不会影响实验结果。我们鼓励感兴趣的读者打开 [A/1](vis/a1.html) 的可视化和[相应的神经元](vis/a-neurons.html)。你可以按"random"排序以获得无偏样本，并进行上述实验的自己的版本，或者按重要性指标（如最大激活和最大密度）对特征排序，以评估上面的最后一个注意事项。

### [我们的解释解释了模型的多少？](index.html#global-analysis-how-much)

我们现在转向我们最无法回答的问题——这些看似可解释的特征在多大程度上代表了 MLP 的"全部故事"？人们可以用多种方式提出这个问题。我们已经使可解释的 MLP 损失贡献的比例是多少？我们能理解多少模型行为？如果确实存在某个离散的"真实特征"集合，我们已经发现了多少比例？

部分解决这个问题的一种方法是询问我们的特征解释了多少损失。对于 [A/1](vis/a1.html)（我们在本文中最关注的运行），79% 的 MLP 层提供的对数似然损失减少由我们的特征恢复。也就是说，用自编码器的输出替换 MLP 激活所产生的额外损失，仅占零消融 MLP 所产生的损失的 21%。通过使用更多特征或使用较低的 L1 系数，可以减少此损失惩罚。作为一个极端示例，[A/5](vis/a5.html)（n_learned_sparse=131,072，l1_coefficient=0.004）恢复了 94.5% 的对数似然损失。

这些数字应该带有很大的保留。最大的问题是，用损失比例来构建这个问题可能会产生误导——我们预计会有一个长尾特征，使得随着解释损失比例的增加，需要越来越多的特征来解释残差。另一个问题是我们不相信我们的特征完全是单义的（一些多义性可能隐藏在低激活中），也不是所有特征都一定是清晰可解释的。尽管如此，我们 earlier 对单个特征的[分析](index.html#feature-analysis)（例如 Arabic 特征、base64 特征等）确实表明，特定的可解释特征以可解释的方式被模型使用——消融它们会以适当的方式降低概率，人为激活它们会引起相应的行为。这似乎证实了恢复的 79% 损失正在测量一些真实的东西，尽管有这些注意事项。

原则上，人们可以使用自动化可解释性来产生更好的衡量标准：用从解释预测的激活替换激活。（我们相信社区中的其他人最近一直在考虑这个！）这个方法的朴素版本计算成本会相当高，朴素地说，用 100k 特征模拟一个层的成本将是采样像 Claude 2 或 GPT-4 这样的大型语言模型的 100,000 倍（我们需要为每个 token 的每个特征采样解释大型模型一次）。按当前价格，这表明在单个 4096 token 上下文上模拟 100k 特征将花费 12,500–25,000 美元，并且人们可能需要在许多上下文上进行评估。尽管可能有近似方法。更一般地说，这里有更广泛的可能性空间。也许有一种原则性的方法可以就单个特征进行此分析——存在重大的概念问题，但人们可能能够将 earlier 的"特征重要性"概念形式化为特征做出的独立损失贡献，然后分析该特定特征可以恢复多少。

总的来说，我们认为衡量基于特征的解释在多大程度上解释模型的问题是一个重要的开放问题，需要在定义指标和寻找有效计算方法方面进行大量工作。

### [特征告诉我们关于模型还是数据的信息？](index.html#global-analysis-about-model)

模型的激活反映了两件事：数据集的分布以及该分布被模型转换的方式。因此，对激活的字典学习混合了数据和模型属性，学习特征的有趣属性可能归因于其中一个或两个来源。数据中的相关性在应用模型的第一部分后（直到 MLP）可能会持续存在，理论上我们看到的那些有趣特征可能只是数据集相关性投影到不同空间中的产物。然而，这些特征被模型的第二部分使用（MLP 下投影和 unembedding）不是字典学习的输入，因此这些特征的下游效果的可解释性必须是模型的属性。

为了评估数据集相关性对特征激活可解释性的影响，我们在具有随机权重的 one-layer 模型版本上运行字典学习。我们通过随机打乱在 Run A 中使用的训练 transformer 的每个权重矩阵的条目来生成具有随机权重的模型。这保证了单个权重的分布匹配，差异是由于结构造成的。结果特征在[这里](vis/random1.html)，包含许多单 token 特征（如"span"、"file"、"."和"nature"）以及一些在其他广泛可识别的上下文的不同看似任意子集上触发的特征（如 [LaTeX](vis/random1.html#feature-1143) 或 [code](vis/random1.html#feature-3050)）。然而，我们无法为非单 token 特征构建有意义的解释，并邀请读者检查具有随机权重模型的特征可视化以自行确认这一点。我们得出结论，模型的学习过程在其激活中创造了比数据集中 token 分布本身更丰富的结构。

为了评估下游特征效果的可解释性，我们再次使用前一节的三种主要方法：

- Logit 权重检查。Logit 权重表示每个特征对 logits 的影响，正如我们在 earlier 对单个特征的[调查](index.html#feature-analysis)中所证明的，它们与 base64、Arabic 和 Hebrew 特征的特征激活一致。邀请读者在可视化中检查所有特征的 logit 权重。
- 特征消融。我们将特征的值在上下文中设置为零，并记录每个 token 的损失如何变化。可视化中提供了所有特征的消融。
- 固定特征采样。我们人为地将特征的值固定为高数字，然后从模型采样。我们发现生成的文本与特征的解释相匹配。

![Figure 42](images/figure_042.png)

在所有这些指标中，特征激活与其下游效果的经验一致性提供了证据，表明发现的特征正被模型使用。

## [现象学](index.html#phenomenology)

最终，我们工作的目标是理解神经网络。将模型分解为特征只是达到这一目的的手段，人们可能会非常合理地想知道它是否真正推进了我们的整体目标。因此，在本节中，我们将注意力转向这些特征可以教给我们关于神经网络的教训。（我们已经开始将这种利用我们的理论理解来推理模型属性称为现象学，类比于 [物理学中的现象学](https://en.wikipedia.org/wiki/Phenomenology_(physics)) 和 [2019 ICML workshop](https://deep-phenomena.org/) 关于深度学习中的现象。）

做到这一点的一种方式是给出我们发现的特征的详细讨论（类似于），但我们认为了解我们发现特征的最佳方式只是[浏览界面](vis/a1.html)，这是我们随本文发布的用于探索特征的工具。我们发现的特征变化巨大，没有简洁的总结能捕捉到它们的广度。相反，我们将主要关注我们注意到的更抽象的属性和模式。这些抽象属性将能够告知——尽管绝不能回答——像"这些是真实特征吗？"和"one-layer 模型中实际发生了什么？"这样的问题。

我们首先讨论一些关于特征的基本主题和观察。然后我们将讨论我们相关的特征如何与其他字典学习运行和其他模型中的特征进行比较。这将表明特征是普遍的，字典学习可以理解为特征分裂的过程，反映了叠加几何的深层内容。最后，我们将探索特征如何连接成"有限状态自动机"，作为实现更复杂行为的系统。

### [特征主题](index.html#phenomenology-feature-motifs)

我们在模型中发现了什么样的特征？

一个强烈的主题是上下文特征（例如 DNA、base64）和上下文中的 token 特征（例如数学中的 the – [A/0/341](vis/a0.html#feature-341)，HTML 中的 < – [A/0/20](vis/a0.html#feature-20)）的普遍存在。从纯粹的理论角度来看，注意力头主要可以实现"三点函数"（有两个输入和一个输出）。MLP 层更适合实现 N-token 连接，其中最极端的可能是上下文特征或上下文中的 token 特征。因此，我们看到许多这些特征也许是自然的。这些在先前工作中已被观察到（上下文特征例如；上下文中的 token 特征例如；先前的观察），但上下文中的 token 特征的巨大数量让我们感到震惊。例如，在 [A/4](vis/a4.html) 中，有超过一百个特征主要在不同上下文中响应 token "the"。上下文中的 token 特征可能为简化模型分析提供重要机会——正如 Elhage 等人指出的，可能可以将这些特征理解为由上下文和 token 参数化的二维特征族。通常这些特征通过特征分裂（在下一节讨论）连接，在具有较少学习特征的字典中表现为纯上下文特征或 token 特征，但随着学习更多特征，分裂成上下文中的 token 特征。

另一个有趣的模式是看似"trigram"特征的实现，例如预测 COVID-19 中 19 的特征（[A/2/12310](vis/a2.html#feature-9143)）。这样的特征原则上可以仅用注意力实现，但实际上模型也使用 MLP 层。我们还看到似乎响应特定、更长 token 序列的特征。这些特别引人注目，因为它们可能实现类似"记忆"的行为——我们稍后将更多地讨论这个。

最后，值得注意的是，我们在 one-layer 模型中发现的所有特征除了作为"输入特征"的角色外，还可以解释为"动作特征"。例如，base64 特征既可以理解为响应 base64 字符串激活，也可以理解为作用于增加 base64 字符串的概率。"动作"观点可以澄清一些上下文中的 token 特征：特征 [A/0/341](vis/a0.html#feature-341) 预测数学文本中的名词短语，上调名词如 denominator 和形容词如 latter。因此，虽然它在 the 上激活最强，但它也在形容词如 special 和 this 上激活，这些后面也跟随名词短语。特征的这种双重解释可以通过浏览我们的界面来探索。几篇论文先前已经探索了将神经元解释为动作（例如），而 one-layer 模型特别适合这一点，因为这是理解最后一个 MLP 层的特别原则性的方式，而 one-layer 模型中唯一的 MLP 就是最后一层。

### [特征分裂](index.html#phenomenology-feature-splitting)

我们发现的特征的一个显著特点是它们以簇的形式出现。例如，我们上面观察到多个 base64 特征、多个 Arabic 脚本特征等等。随着我们增加学习稀疏特征的总数，我们看到更多这些特征，我们将这种现象称为特征分裂。随着我们从 A/0 中的 512 个特征到 A/1 中的 4,096 个特征再到 A/2 中的 16,384 个特征，特定于 base64 上下文的特征数量从 1 个到 3 个再到更多。

为了理解字典元素的几何如何对应这些定性簇，我们对来自 A/0、A/1 和 A/2 的特征方向的组合集进行 2-D UMAP。

![Figure 43](images/figure_043.png)

我们看到对应于 base64 和 Arabic 脚本特征的簇，以及来自特定上下文的许多其他紧密簇和其他特征的各种有趣几何结构。这证实了定性簇反映在字典的几何中：相似特征在其字典向量之间具有小角度。

![Figure 44](images/figure_044.png)

我们推测，如果我们为字典学习提供无限的字典大小，它会返回某个理想化的特征集。通常，这些"真实特征"被聚集成相似特征的集合，模型将其置于非常紧密的叠加中。由于特征数量受到限制，字典学习返回的特征大致覆盖了与理想化特征相同的领域，代价是特异性稍低。

在这个图景中，概念上相似特征的字典向量相似的原因是，它们可能在模型中产生相似的行为，因此应该对神经元激活中的相似效果负责。例如，一个在句号上触发的特征预测带有前导空格后跟大写字母的 token 是很自然的。如果有多个特征在句号上触发，也许在略有不同的上下文中，这些可能都预测带有前导空格的 token，这些预测可能很好地涉及产生相似的神经元激活。特征高度相关且具有相似"输出动作"的组合，导致真实模型比我们之前在 toy models 工作中观察到的具有更密集和更有结构的叠加。Toy Models 考虑了相关特征（特别是参见 [相关特征的组织](https://transformer-circuits.pub/2022/toy_model/index.html#geometry-organization) 和 [相关特征的折叠](https://transformer-circuits.pub/2022/toy_model/index.html#geometry-collapsing)），但仅考虑了在是否激活上相关的特征（而不是如果激活的值），并且没有类似于这里描述的相似"输出动作"的东西。尽管如此，Toy Models 的实验可能是一个有用的直觉泵，特别是在注意叠加中的相似特征与特征折叠成单个更广泛特征之间的区别。

如果这个图景是真的，它将因许多原因而重要。这表明确定字典学习的"正确特征数量"不如最初看起来那么重要。它还表明，具有较少特征的字典学习可以提供模型特征的"摘要"，这在研究大型模型时可能非常重要。此外，它将解释我们在字典学习过程中观察到的一些更奇怪的特征，表明这些要么是如果进一步分裂就有意义的"折叠"特征（参见 ["Bug" 1: 单 Token 特征](index.html#features-seem-like-bugs-1)），要么是如果仔细分析确实有意义的超高特异性"分裂"特征（参见 ["Bug" 2: 单个上下文的多个特征](index.html#features-seem-like-bugs-2)）。最后，这表明我们的 toy models 叠加基本理论错过了问题的一个重要维度，因为没有充分研究高度相关和"动作共享"特征。

#### 示例：数学和物理特征

在这个示例中，我们最粗略的运行（具有 512 个学习稀疏特征）有三个特征描述不同技术设置中的 token。使用特征激活之间的 masked cosine similarity，对于每对特征，我们计算它们在其中一个触发的 token 子集上的激活之间的 cosine similarity。我们重复此操作，限制在另一个触发的子集上，并取两者中较大的一个。如果此度量超过约 0.4，我们在特征之间绘制连接。选择此阈值是为了平衡产生足够小的图以进行可视化，同时也显示特征分裂的一些丰富性。我们在此分析中省略超低密度特征。我们能够识别这些特征如何在具有更多学习稀疏特征的运行中细化和分裂。

我们看到的是，更精细的运行揭示了例如技术写作中概念之间更细粒度的区别，并区分了冠词 the 和 a，它们后面跟随略有不同的名词短语集。我们还看到，这种细化的结构比树更复杂：相反，我们在一个级别发现的特征可能同时分裂和合并以在下一个级别形成细化特征。但总的来说，我们看到具有更多学习稀疏特征的运行往往比较少的运行更具体。

![Figure 45](images/figure_045.png)

值得注意的是，这些更精确的特征反映了模型预测以及激活的差异。数学散文中的一般 the 特征（[A/0/341](vis/a0.html#feature-341)）具有高度通用的数学 token 作为其顶级 positive logits（例如支持 denominator、remainder、theorem），而更精细分裂的机器学习版本（[A/2/15021](vis/a2.html#feature-15021)）具有更具体的主题预测（例如 the dataset、the classifier）。同样，我们的抽象代数和拓扑特征（[A/2/4878](vis/a2.html#feature-4878)）支持 the quotient 和 the subgroup，引力和场论特征（[A/2/2609](vis/a2.html#feature-2609)）支持 the gauge、the Lagrangian 和 the spacetime。

#### [看似 Bug 的特征](index.html#features-seem-like-bugs)

["Bug" 1: 单 Token 特征](index.html#features-seem-like-bugs-1)
当我们限制字典学习使用非常少的学习稀疏特征时，出现的特征有时看起来相当奇怪。特别是，有大量高激活幅度的特征，每个特征仅在一个 token 上触发，并且似乎在每个该 token 的实例上触发。这样的特征很奇怪，因为模型可以通过学习不同的 bigram 统计完全实现相同的效果，因此没有理由将 MLP 容量用于这些。Smith 最近的报告中也观察到了类似的特征。

我们认为特征分裂解释了这种现象：模型没有学习一个在字母 P 上触发的单一特征，这些特征在 token " P"上触发，在它作为第一个 token 出现的单词中，例如 [ P][attern]。相反，它学习了许多在不同上下文中在 P 上触发的特征，在这种情况下，我们通过手动检查而不是 cosine similarity 发现了细化的 P 特征。对神经元激活和输出 logits 有相应不同的影响（见下文）。在足够粗略的级别上，字典学习无法区分这些，但当我们允许它使用更多学习稀疏特征时，特征分裂并细化为在不同上下文中触发的各种 P 特征的动物园。

![Figure 46](images/figure_046.png)

["Bug" 2: 单个上下文的多个特征](index.html#features-seem-like-bugs-2)
我们还观察到了相反的情况，其中多个特征似乎覆盖了大致相同的概念或上下文。例如，在 [A/1](vis/a1.html) 中有三个特征在（子集）base64 字符串上触发，并预测合理的 base64 token，如 zf、mF 和 Gp。其中一个特征在 earlier [详细讨论过](index.html#feature-base64)，我们展示了它在 base64 字符串上触发。但我们也观察到它并非在所有 base64 字符串上触发——为什么？其他两个特征在做什么？为什么有三个？

在 [A/0](vis/a0.html)（具有 512 个特征）中，故事很简单。只有一个 base64 相关特征，[A/0/45](vis/a0.html#feature-45)，它似乎在 base64 编码字符串的所有 token 上激活。但在 [A/1](vis/a1.html) 中，该特征分裂成三个不同的特征，它们的激活似乎共同覆盖了 [A/0/45](vis/a0.html#feature-45) 的激活：

![Figure 47](images/figure_047.png)

其中两个特征看起来相对简单。[A/1/2357](vis/a1.html#feature-2357) 似乎在 base64 中的字母上优先触发，而 [A/1/2364](vis/a1.html#feature-2364) 似乎在数字上优先触发。

比较这些特征的 logit 权重显示，它们预测大致相同的 token 集，有一个显著差异：在数字上触发的特征对预测数字的 logit 权重低得多。换句话说，如果当前 token 由数字组成，模型将预测下一个 token 是非数字 base64 token。

![Figure 48](images/figure_048.png)

我们认为这很可能是 tokenization 的产物！如果单个数字后跟另一个数字，它们会被一起 tokenized 为单个 token；[Bq][8][9][mp] 永远不会出现，因为它会被 tokenized 为 [Bq][89][mp]。因此，即使在随机 base64 字符串中，当前 token 是单个数字的事实也提供了关于下一个 token 的信息。

但第三个特征 [A/1/1544](vis/a1.html#feature-1544) 呢？乍一看，没有明显的规则说明它何时触发。但如果我们更仔细地观察，我们注意到它似乎响应编码 ASCII 文本的 base64 字符串。我们最初的线索是 [A/1/1544](vis/a1.html#feature-1544) 可能响应编码 ASCII 文本的 base64 字符串，是该特征特别响应的 token ICAgICAg，对应六个连续空格。如果我们查看每个特征的顶级数据集示例，我们发现 [A/1/1544](vis/a1.html#feature-1544) 的示例包含解码为 ASCII 的子字符串，而 [A/1/2357](vis/a1.html#feature-2357) 或 [A/1/2364](vis/a1.html#feature-2364) 的顶级激活示例都没有：确定数据集示例何时编码 ASCII 文本有些微妙，因为 base64 只能以四个字符组解码为 ASCII，因为四个 base64 字符 [encode triples](https://en.wikipedia.org/wiki/Base64#Examples) 的 ASCII 字符。因此，我们选择子字符串——当使用 python base64 库解码时——包含最大数量的可打印 ASCII 字符。

![Figure 49](images/figure_049.png)

这种调查模式，即查看较粗的特征集以理解模型行为的类别，然后查看更精细的特征集以调查该行为的微妙之处，可能证明非常适合预期特征集相当大的大型模型。

还值得注意的是，字典学习特征在这里能够让我们感到惊讶。许多可解释性方法是自上而下的，寻找我们期望的东西。但谁会知道模型不仅有 base64 特征，而且它们区分不同种类的 base64 字符串？这让我们想起了高频 - 低频检测器或多模态神经元等案例，在视觉模型中发现了令人惊讶和意想不到的特征。

### [普遍性](index.html#phenomenology-universality)

关于特征的最大"元问题"之一是它们是否是 [普遍的](https://distill.pub/2020/circuits/zoom-in/#claim-3)——相同的特征是否在不同模型中形成？这个问题通常很重要，因为它关系到从一个模型研究中学到的来之不易的经验是否会推广到其他模型。但在尝试从叠加中提取特征的背景下尤其重要，因为普遍性可以提供重要证据，证明我们提取的特征是"真实的"，或者至少是可重复的。在什么意义上普遍性表明特征是"真实的"？一个基本观察是，它们表明我们发现的特征不仅仅是字典学习过程的产物——或者至少，如果它们来自字典学习过程，它是以某种一致的方式。但也有几种更深层次的方式，它是启发性的。这意味着，无论特征的来源是什么，我们可以将特征谈论为可复制的、可靠的、重复出现的分析单元。这也只是一个令人惊讶的观察，如果叠加中特征的强版本假说是真的，并且模型字面上表示某个有限的、离散的特征集在叠加中，人们会期望这一点。

Earlier，我们看到我们执行详细分析的所有特征（例如 Arabic 特征或 base64 特征）在两个 one-layer 模型之间都是普遍的。但这对我们模型中的典型特征也是如此吗？它的范围有多广——我们是否只有在相同架构的模型在相同数据集上训练时才观察到相同的特征，或者这些特征也出现在更多不同的模型中？本节将寻求解决这两个问题。第一个子节将定量分析普遍性在我们研究的两个 one-layer 模型之间有多广泛，而第二个将把我们发现的特征与文献中报告的其他特征进行比较，以寻找更强形式的普遍性。

我们观察到两种类型的实质性普遍性。事实上，我们发现一些特征如此普遍，以至于我们开始将其视为评估字典学习运行工作流程中的基本工具。例如，base64 特征——我们先前在 SoLU 模型中观察到的——是如此一致地普遍，以至于它的存在是一个有用的调试启发式。在高层面上，这是有道理的：如果一个特征对一个模型在表示数据时有用，它可能对其他模型也有用，如果两个模型表示相同的特征，那么一个好的字典学习算法应该找到它。

#### 比较两个 one-layer transformers 之间的特征

为了比较来自不同模型的特征，我们需要与模型无关的方式来表示特征。

一种自然的方法是将特征视为为数据点分配值的函数；如果两个特征在多样化的数据集上采用相似的值，那么它们在这个意义上是相似的。许多先前的论文已经探索了这种一般方法（例如）。在实践中，这可以通过将特征表示为向量来近似，索引对应于固定的数据集。我们称这些向量之间的相关性为特征之间的激活相似度。

第二种自然方法是从其下游效果的角度来思考特征；如果两个特征的激活以相似的方式改变它们模型的预测，那么它们在这个意义上是相似的。在我们的 one-layer 模型中，一个简单的近似是 logit 权重。这个近似将每个特征表示为向量，索引对应于词汇表 token。我们称这些向量之间的相关性为特征之间的 logit 权重相似度。

这两种相似性概念对应于我们 earlier 在 [分析单个特征](index.html#feature-ananlysis) 时使用的两个散点图中的点的相关性。我们在下面为 Arabic 特征重现了这些图：

![Figure 50](images/figure_050.png)

对于运行 [A/1](vis/a1.html) 中的每个特征，我们在运行 [B/1](vis/b1.html) 中通过激活相似度找到最近的特征，这是不同的字典学习运行，在不同 transformer 的不同激活上训练，具有不同的随机种子，但其他超参数相同。我们发现许多特征在模型之间高度相似，[A/1](vis/a1.html) 中的特征与来自 [B/1](vis/b1.html) 的最相似特征具有 0.72 的中位数激活相关性。（我们对 transformers 之间找到最近的神经元进行相同的分析，发现相似性显著较低，中位数激活相关性为 0.46。）模型之间激活相关性低的特征可能代表字典学习中不同的"特征分裂"或基础模型学习的不同"真实特征"。

![Figure 51](images/figure_051.png)

一个自然的下一个问题是，在相同 token 上触发的特征是否也具有相同的 logit 效果。也就是说，激活相似度和 logit 权重相似度的一致性如何？

上面的 Arabic 特征可以看到两者之间有一些差距：特征效果的"重要 token"（Arabic 脚本中的那些）被两个模型的特征上调，但有大量 token 具有较小的效果，看起来几乎是各向同性噪声，导致 logit 权重相关性仅为 0.23，显著低于 0.91 的激活相关性。

在下面的散点图中，我们发现这种不一致是普遍的。
![Figure 52](images/figure_052.png)

这种差异最显著的例子是特征 [A/1/3949](vis/a1.html#feature-3949) 和 [B/1/3321](vis/b1.html#feature-3321)，它们的激活相关性为 0.98，但 logit 权重相关性为负。这些特征在 pone 上触发（偶尔也在 pgen 和 pcbi 上触发），作为引用中期刊名称 PLOSOne 的缩写，如 @pone.0082392，并预测随后的 .。该特征是双峰的，在较大的峰中是单语义的，并在 0.02% 的 token 上触发。这意味着在 Pile 数据集中，至少有万分之一的 token 是引用中 PLoS 期刊的缩写！这是一个如何通过检查特征来揭示数据集属性的例子，在这种情况下，Pile 对科学内容有强烈的偏向。

放大 logit 权重散点图（上图中的插图），我们看到只有 . token 在两个模型中都有高 logit 权重，而每个其他 token 都位于 logit 权重分布的"干扰"部分。实际上，模型可能根本不关心特征对那些已经被直接路径、注意力层或 MLP 的其他特征抑制的本来就不可能的 token 做了什么。

我们想要衡量的是更像"特征对 token 概率的实际影响"的东西。一种方法是为每个特征在每个数据点上计算消融效应向量；那些消融会损害模型对相同 token 预测的特征对，必定是在预测相同的东西。不幸的是，这在计算上会相当昂贵。相反，我们将特征的激活向量乘以数据集中经验上接下来出现的 token 的 logit 权重，以产生一个归因向量。假设特征 f_i 对 k ∈ {1,...,n_vocab} 有 logit 权重 v_{ik}。在给定 token t_j 处，我们计算特征 f_i(t_j) 的激活，并将其乘以接下来出现的 token t_{j+1} 的 logit 权重 v_{it_{j+1}}，得到归因分数 f_i(t_j)v_{it_{j+1}}。归因向量是通过对随机采样的数据点堆叠归因分数得到的。这近似于经典的归因方法（将梯度乘以激活），不同之处在于我们忽略了 softmax 和 layer norm 的分母。这些向量之间的相关性提供了归因相似性，它结合了特征的活动及其对损失的影响。我们发现归因相似性与激活相似性高度相关，这意味着在模型之间共激活的特征在预测相同 token 时是有用的。

![Figure 53](images/figure_053.png)

鉴于此，我们认为整篇论文中使用的激活相关性实际上是我们单层模型背景下两种普遍性概念的良好代理。

#### [与文献比较特征](index.html#universality-literature)

到目前为止，我们已经确定许多特征在有限意义上是普遍的。在一个 transformer 中发现的特征也可以在用不同随机种子训练的替代版本中找到。但这第二个模型具有相同的架构，并在相同的数据上训练。这是人们可能希望的最小版本的普遍性。尽管如此，我们相信我们发现的许多特征在更深的意义上是普遍的，因为非常相似的特征以前在文献中已有报道。

让我们首先注意到的比较是，许多特征似乎与我们之前在单层 SoLU 模型中发现的神经元非常相似，后者使用一种旨在使神经元更加单语义的激活函数。特别是，我们在 SoLU 研究中观察到了 base64 神经元、hexadecimal 神经元和 all caps 神经元，而在这里也发现了 base64 ([A/0/45](vis/a0.html#feature-45))、hexademical ([A/0/119](vis/a0.html#feature-119)) 和 all caps ([A/0/317](vis/a0.html#feature-317)) 特征。其中一些神经元的讨论可以在 SoLU 论文的 [6.3.1 节](https://transformer-circuits.pub/2022/solu/index.html#section-6-3-1) 中找到。

我们还发现许多与 Smith 相似的特征，他将字典学习应用于残差流。除了我们也观察到他们注意到的单 token 特征的优势（见我们对这一现象的 [解释](index.html#features-seem-like-bugs)），我们还发现了类似的德语检测器（例如 [A/0/493](vis/a0.html#feature-493)）和类似的首字母大写检测器（例如 [A/0/508](vis/a0.html#feature-508)）。同样，我们发现许多与 Gurnee 等人相似的特征，包括一个"质因数"特征 ([A/4/22414](vis/a4.html#feature-22414)) 和一个法语特征 ([A/0/14](vis/a0.html#feature-14))。

在更抽象的层面上，我们发现的许多特征似乎与 Goh 等人 在多模态模型中报告的特征相似。例如，我们发现许多相似的特征，包括 Australia 特征 ([A/3/16085](vis/a3.html#feature-16085))、Canada 特征 ([A/3/13683](vis/a3.html#feature-13683))、Africa 特征 ([A/3/14490](vis/a3.html#feature-14490)) 和 Israel-Palestine 特征 ([A/3/739](vis/a3.html#feature-739))，它们在语法适当时预测这些区域中的位置。这大致反映了 Goh 等人论文中报道的"区域神经元"。对于其他特征族，相似之处就不那么清楚了。例如，Goh 等人 最引人注目的结果之一是人物检测神经元（类似于神经科学中的著名结果）。我们发现一些特征在非常狭窄的上下文中是人物检测器，例如响应人名并预测适当的下一个词，或预测他们的名字（例如 [A/1/3240](vis/a1.html#feature-3240) 有点类似于 Goh 等人的 Trump 神经元），但它们似乎非常狭窄。我们也没有发现似乎与 Goh 等人的情绪神经元明显类似的特征。

### ["有限状态自动机"](index.html#phenomenology-fsa)

我们在单层模型特征研究中观察到的最引人注目的现象之一是存在"有限状态自动机"般的特征组件。这些组件不是传统意义上的电路——它们由一个特征增加 token 的概率形成，这反过来导致另一个特征在下一步触发，依此类推。"有限状态自动机"般的特征组件与电路的不同之处在于，模型学习它们不是为了协同工作。相反，在学习自回归地建模文本的过程中，它学习了由于真实数据集中的模式而通过 token 流相互作用的特征。相比之下，用强化学习训练的语言模型可能有这样的系统——其特征组件通过生成的 token 相互作用的电路——它们在 RL 训练期间共同进化并适应协同工作。

最简单的例子是在下一个 token 上激发自身的特征，形成单节点循环。例如，base64 特征增加了像 Qg 和 zA 这样的 token 的概率——这些是合理的延续，会继续激活它。

![Figure 54](images/figure_054.png)

值得注意的是，这些例子来自 [A/0](vis/a0.html)，一个不过完备的字典学习运行（字典维度为 512，等于 transformer MLP 维度）。当我们转向具有更多特征的运行时，中心特征将经历特征分裂，并成为一个更复杂的系统。

现在让我们考虑一个用于生成"全大写蛇形命名法"变量（例如 ARRAY_MAX_VALUE）的双节点系统。一个节点 ([A/0/207](vis/a0.html#feature-207)) 在全大写文本 token 上激活，另一个节点 ([A/0/358](vis/a0.html#feature-358)) 在下划线符上激活：

![Figure 55](images/figure_055.png)

这种双节点系统对于 Unicode 字符有时被分成两个 token 的语言来说相当常见。（同样，随着更多特征分裂，这些将扩展为更复杂的系统。）

例如，Tamil Unicode 字符（[块 U+0B80–U+0BFF](https://www.compart.com/en/unicode/block/U+0B80)）通常被分成两个 token。例如，字符"ண"（[U+0BA3](https://www.compart.com/en/unicode/U+0BA3)）被 token 化为 \xe0\xae，后跟 \xa3。第一部分（\xe0\xae 或 \xe0\xaf）大致指定 Unicode 块，而第二部分指定该块内的字符。因此，模型在两个特征之间交替是很自然的，一个用于 Unicode 前缀 token，一个用于后缀 token。

一个更复杂的例子是中文。虽然许多常见汉字有专用 token，但许多其他汉字被分割。这因汉字分布在许多 Unicode 块上而变得更加复杂，这些块很大，并且跨越许多以字节指定的逻辑块。为了理解模型为实现此目的而实现的状态机，关键观察是完整字符类似于分割字符的"后缀"部分：两者都可以后跟新的完整字符或新前缀。因此，我们观察到两个特征，一个在完整字符或后缀上触发（预测新的完整字符或前缀），而另一个仅在前缀上触发并预测后缀。

![Figure 56](images/figure_056.png)

现在让我们考虑一个非常简单的四节点系统来建模 HTML。通过它的"主路径"是：

- [A/0/20](vis/a0.html#feature-20) 在开始标签上触发并预测标签名
- [A/0/0](vis/a0.html#feature-0) 在标签名上触发并预测标签闭合
- [A/0/30](vis/a0.html#feature-30) 在标签闭合上触发并预测空白
- [A/0/494](vis/a0.html#feature-494) 在空白上触发并预测新标签开始。

这可能生成的典型样本类似于 &lt;div&gt;\n\t\t&lt;span&gt;。

完整系统如下所示：

![Figure 57](images/figure_057.png)

请记住，我们关注的是 [A/0](vis/a0.html) 特征，这里非常简单——如果我们看 [A/1](vis/a1.html)，我们会发现更复杂的东西！[A/0](vis/a0.html) 特征的一个特别显著的缺点是它们没有描述当 [A/0/0](vis/a0.html#feature-0) 发出像 href 这样的 token 时会发生什么，这会导致更复杂的状态。

值得注意的是，这些特征可能非常依赖上下文。有几个与 IRC 记录相关的特征形成了一个完全不同的有限状态自动机般的系统：

![Figure 58](images/figure_058.png)

这可能生成的典型样本类似于 &lt;nickonia_&gt; lol ubuntu ;)。大概 Pile 数据集大量代表了关于 linux 的 IRC 记录。

一个特别有趣的行为是明显记住了特定短语。这只能在具有相对大量特征的运行中观察到（如 [A/4](vis/a4.html)）。在以下示例中，一系列特征似乎在功能上记住了短语 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE 的粗体部分。这是相对标准的法律语言，值得注意的是出现在流行开源软件许可证的文件头中，意味着模型在训练期间可能多次看到它。

![Figure 59](images/figure_059.png)

这似乎是我们之前在 Henighan 等人 中描述的机械化记忆理论的一个例子——我们观察到相对二元且对非常具体情况做出响应的特征。这也可以被视为机械化异常检测 的一个实例：模型在特定、狭窄的情况下表现不同。在只有 512 个神经元的模型中可以找到如此狭窄的东西有点令人惊讶；从这个角度来看，这是叠加能力在少数神经元中嵌入许多东西的有趣例子。另一方面，因为这些机制深埋在叠加中，它们可能非常嘈杂。

## [相关工作](index.html#related-work)

叠加和解决它的尝试与许多研究路线有着深刻的联系，包括对可解释特征的一般研究、线性探测、压缩感知、字典学习和稀疏编码、神经编码理论、分布式表示、数学框架、向量符号架构等等。我们不在这里试图公正地对待所有这些联系，而是将读者参考 Toy Models of Superposition 的 [相关工作部分](https://transformer-circuits.pub/2022/toy_model/index.html#related)，我们在那里深入讨论了这些主题，也参考我们的文章 [分布式表示：组合与叠加](../superposition-composition/index.html)。相反，我们将重点讨论与解决叠加的尝试相关的工作，以及我们对叠加理解的最新进展。

#### 叠加

自从我们发表 Toy Models of Superposition 以来，已经有大量进一步的工作试图更好地理解叠加。我们在下面简要总结。

叠加是真实的吗？Gurnee 等人 使用稀疏线性探针展示了一些可能处于叠加中的特征的引人注目的例子。另外，Li 等人 和 Nanda 等人 之间的交流似乎是对特征作为方向的总体 picture 是否正确的更新；Li 等人 似乎表明它不是，使假设处于危险之中，然后由 Nanda 等人 解决。

叠加何时以及为何发生？Scherlis 等人 为思考单语义性与多语义性提供了一个数学框架。lsgos 探索了 dropout 对叠加玩具模型的影响。

记忆——在 Henighan 等人 中，我们研究了与 Toy Models of Superposition 中相同的玩具模型，但这次在许多重复的有限大小数据集上训练。我们发现小数据集在叠加中被记忆，而不是在大数据集的情况下泛化特征。Hobbhahn 复制了其中一些发现，并进一步展示了扩展到其他设置，包括层之间的瓶颈（类似于 MLP 层之间的残差流）。随后，在每月更新中，我们 [检查了](../july-update/index.html#finite-data) 记忆和泛化机制之间的边界，发现了一个尖锐的相变，以及在边界记忆侧的叠加中的数据集聚类。

#### 解缠和架构方法

还有关于解缠的丰富且相关的文献，它寻求找到将影响数据的概念上不同的现象分离（解缠）的数据表示。与叠加相反，这项工作通常寻求找到等于被表示空间维度的变异因子或特征数量，而叠加寻求找到更多。

这通常作为架构/训练时问题来处理。例如，Kim & Mnih 提出了一种方法，通过鼓励维度之间的独立性来推动变分自编码器解缠因子。同样，Chen 等人 开发了一种生成对抗网络方法，试图通过最大化因子小子集与数据集之间的互信息来解缠因子。Makhzani & Frey 使用 TopK 激活来鼓励稀疏性从而解缠。参见 Bengio 等人 和 Räuker 等人 讨论其他此类方法。

这样来看，一些解决叠加的架构方法也可以被理解为解缠的尝试。例如，在 Elhage 等人 中，我们提出了 SoLU 激活函数，它通过鼓励特征与神经元基对齐来增加 transformer 中可解释神经元的数量。不幸的是，用 SoLU 激活函数训练模型似乎使一些神经元更可解释，但代价是使其他神经元比以前更不可解释。

同样，Jermyn 等人 研究了在压缩感知任务上训练的 MLP 层，发现多个等损失最小值，一些强烈多语义，一些强烈单语义。这表明训练干预可以引导模型走向更多单语义最小值，尽管随后对更现实任务的调查表明等损失属性是特定于所选任务的。

这两个通过架构解决叠加的尝试示例及其遇到的挑战，突出了解缠问题和叠加问题之间的关键区别：解缠从根本上寻求确保模型潜在空间中的维度被解缠，而叠加假设这种解缠通常会损害性能（因为成功需要丢弃许多特征），并且模型通常会对解缠干预做出反应，使一些特征更强地纠缠（正如 Mahinpei 等人 和 Elhage 等人 2022 在略有不同的背景下发现的）。

#### 字典学习与特征

我们的工作建立在更长的使用字典学习和稀疏自编码器分解神经网络激活的传统之上。

该领域的早期工作集中在词嵌入和其他非 transformer 神经网络上。Faruqui 等人 和 Arora 等人 都使用稀疏编码方法在词嵌入中发现了线性结构。Subramanian 等人 同样发现了词嵌入的线性因子，这次使用了稀疏自编码器。Zhang 等人 使用字典学习方法解决了类似问题，而 Panigrahi 等人 用潜在狄利克雷分配来处理这个问题。

最近，许多工作将字典学习方法应用于 transformer 模型。Yun 等人 将字典学习应用于 12 层 transformer 的残差流，以找到特征的欠完备基。

此时，我们在 Toy Models 中的工作主张将字典学习作为解决叠加的潜在方法。这激发了我们的同事 Cunningham 等人的并行调查，作为一系列中期报告发表，与本文主题非常相似，最终形成了一份手稿。我们很高兴看到我们的工作之间有这么多确证的发现。

在他们的中期报告中，Sharkey 等人 使用稀疏自编码器在单层 transformer 上执行字典学习，识别出大量（过完备）特征基。（Sharkey 等人 应该因专注于字典学习，特别是稀疏自编码器方法而受到赞誉，而我们的调查只是将其作为几种并行方法之一来探索。）这项工作随后被 Cunningham & Smith 和 Huben 部分复制。接下来，Smith 使用自编码器在六层模型的一个 MLP 层中找到特征。生成的特征似乎是可解释的，例如在 LaTeX 方程的上下文中检测'$'。在后续工作中，Smith 然后将此方法扩展到同一模型的残差流，识别出许多有趣的特征（见 [前面的讨论](index.html#universality-literature)）。基于这些结果，Cunningham 将 Bills 等人 的自解释技术应用于同一六层模型的残差流和 MLP 层中的特征，发现稀疏自编码器发现的特征比神经元可解释得多。

## [讨论](index.html#discussion)

### [叠加理论](index.html#discussion-superposition)

在进行这项工作时，我们对叠加的理解主要来自 Toy Models。这给了我们一个可以称为各向同性叠加模型的 picture。特征是离散的一维对象，由于干扰而相互排斥，产生大致均匀间隔的特征方向组织。

这项工作说服我们，我们之前的模型遗漏了一些关键的东西。至少，特征似乎聚集在更高密度的相关特征组中。对此的一种解释（Toy Models 简要考虑过）是特征可能有相关的激活——一起触发。另一种——我们怀疑更为核心——是特征产生相似的动作。在 base64 中触发单个数字的特征预测的 token 集与触发 base64 中其他字符的特征大致相同，除了其他数字；这些相似的下游效应表现为几何上接近的特征方向。

此外，目前尚不清楚特征是否需要是一维对象（仅编码某些强度）。原则上，似乎可能有高维"特征流形"（见前面 [这里](../may-update/index.html#feature-manifolds) 的讨论）。

![Figure 60](images/figure_060.png)

这些假设并不相互排斥。几个相关特征的凸包可以被理解为特征流形。另一方面，一些流形不会允许用有限数量的一维特征进行唯一描述。（也许这解释了上面观察到的持续 [特征分裂](index.html#phenomenology-feature-splitting)。）

![Figure 61](images/figure_061.png)

尽管如此，这些实验让我们更有信心，某些版本的叠加假设（和线性表示假设）是正确的。发现的可解释特征数量、激活水平似乎对应于"强度"或"置信度"的事实、logit 权重大多有意义，以及"干扰权重"的观察：所有这些观察都是你从叠加中期望看到的。

最后，我们注意到，在叠加的某些扩展理论中，找到"正确的特征数量"可能没有明确定义。在其他理论中，有真实的特征数量，但完全正确地得到它不那么重要，因为我们"优雅地失败"，随着我们增加自编码器中学习特征的数量，在不同粒度分辨率下观察"真实特征"。

### ["上下文中的 Token"特征是真实的吗？](index.html#discussion-token-in-context)

我们发现的最常见主题之一是"上下文中的 token"特征。它们也代表了随着字典大小增加通过特征分裂出现的许多特征。其中一些是直观的——借用一个例子，将德语中的"die"（它是定冠词）与英语中的"die"（意思是"死亡"或"骰子"）表示为不同的是有意义的。

但为什么我们会看到数百个不同的"the"特征（例如物理学中的"the"，不同于数学中的"the"）？我们也对其他常见词（例如"a"、"of"）和像句号这样的标点符号观察到这一点。这些特征不是我们开始调查单层模型时预期会发现的！

为了使问题更精确，借用局部与组合表示的语言和例子是有帮助的。单独表示 token-上下文对（例如物理学中的"the"）在技术上是一种 ["局部编码"](../superposition-composition/index.html#distributed-local)。表示这的更直观方式将是 ["组合编码"](../superposition-composition/index.html#distributed-compositional)——将"the"表示为独立于 Physics 的特征。所以我们真正想问的是为什么我们观察到局部编码，以及这是否真的是正在发生的事情。有两个假设：

- 底层 transformer 使用组合编码，我们字典学习方案的一个特性产生了使用局部编码的特征。
- 底层 transformer 确实在使用局部编码（至少部分如此），字典学习正确地表示了这一点。

如果前者成立，那么更好的字典学习方案可能有助于从同一 transformer 中发现更多组合特征集。局部编码比组合编码更稀疏，我们的 L1 惩罚可能将模型推向太强的稀疏性。

然而，我们相信第二个假设在某种程度上可能成立。让我们再次考虑物理学中"the"的例子，它预测物理学中的名词短语：如果模型独立表示"the"和 Physics 上下文，它将被迫使 logit 成为"提升 the 之后出现的 token"和"提升物理学中出现的 token"的总和。但模型可能希望有比这更"锐利"的预测，这只有用局部编码才有可能。

### [未来工作](index.html#discussion-future-work)

扩展稀疏自编码器。将稀疏自编码器的应用扩展到前沿模型对我们来说是未来最重要的问题之一。我们相当有希望这些或类似方法会起作用——Cunningham 等人 的工作 似乎表明这种方法可以在稍大的模型上工作，我们也有指向同一方向的初步结果。然而，有重大的计算挑战需要克服。考虑一个具有 100 倍扩展因子的自编码器应用于宽度为 10,000 的单个 MLP 层的激活：它将具有约 200 亿个参数。此外，许多这些特征可能相当罕见，可能需要自编码器在大型模型训练语料库的很大一部分上进行训练。因此，训练自编码器可能变得非常昂贵，甚至可能比原始模型更昂贵，这似乎是合理的。然而，我们仍然乐观，并且有一线希望——现在似乎有很大一部分机械化可解释性议程将取决于成功解决一个困难的工程和扩展问题，前沿 AI 实验室在这方面有重要的专业知识。

字典学习的扩展定律。值得注意的是，关于上述字典学习和稀疏自编码器扩展动态存在巨大的不确定性。随着我们使主题模型变大，理想的扩展因子如何变化？（它保持不变吗？）所需的数据量如何变化？这些问题的解决将决定这种方法如果执行良好是否可以扩展到前沿模型。理想情况下，我们希望有扩展定律来回答这个问题。

我们如何识别好的特征？这项工作最大的挑战之一是我们某种程度上在"黑暗中摸索"。我们没有很好的系统方法知道我们是否成功提取了高质量特征。自动可解释性 似乎是解决这个问题的有力竞争者。或者，人们可能希望有一些纯粹抽象的定义（例如 [基于信息的度量](../may-update/index.html#simple-factorization) 提案），但我们还没有在真实数据上看到令人信服的迹象。除了 MMCS、激活相似性和归因相似性之外，拥有更多用于比较特征集以评估一致性和普遍性的度量也会有帮助。

分析的可扩展性。假设稀疏自编码器完全解决了叠加。我们是否有把握完全机械化地理解模型？似乎很明显至少还会有一个基本障碍：模型的分析扩展，以便我们可以将微观洞察转化为更宏观的理解。同样，这里的一种方法可能是自动可解释性。但出于各种原因，将 AI 的理解委托给 AI 可能不完全令人满意。可能有其他基于发现更大规模结构的路径（见 [这里](../interpretability-dreams/index.html#larger-scale) 的讨论）。

稀疏自编码器的算法改进。改进稀疏自编码器方法的新算法可能有用。人们可以探索使用变分自编码器（例如，），或除了对激活的简单 L1 惩罚之外的稀疏性促进先验正则化技术（例如，），例如鼓励不同层中学习特征之间的相互作用的稀疏性。早期研究表明，噪声注入也可以在不依赖 L1 惩罚的情况下增加神经元可解释性。

注意力叠加？许多关于 MLP 层中存在叠加的动机 也适用于自注意力层。似乎可以想象类似的方法可以从注意力层中提取有用结构，尽管尚未建立清晰的例子（例如，见我们的 [五月](../may-update/index.html#attention-superposition) 和 [七月](../july-update/index.html#attn-skip-trigram) 更新）。如果这是真的，解决这可能成为机械化可解释性议程的未来瓶颈。

叠加与特征理论。即使假设在非常广泛的意义上是正确的，我们对于叠加的理解仍有许多基本问题有待解答。例如，如上所述，这项工作表明叠加假设的扩展涵盖了具有相似效应的特征簇，或特征的连续族。我们相信通过玩具模型的使用，在进一步探索叠加理论方面有重要的工作要做。

## [评论与复制](index.html#comments)

受原始 [Circuits Thread](https://distill.pub/2020/circuits/) 和 [Distill 的讨论文章实验](https://distill.pub/2019/advex-bugs-discussion/) 的启发，作者邀请了几位我们之前与之讨论过初步结果的外部研究人员对这项工作进行评论。他们的评论 included below。

### [复制与教程](index.html#comment-nanda)

Neel Nanda 是一位外部机械化可解释性研究员。这是对 [一篇博客文章](https://www.alignmentforum.org/posts/fKuugaxt2XLTkASkk/open-source-replication-and-commentary-on-anthropic-s) 的总结，该文章复制并扩展了本文，并附有 [配套教程](https://colab.research.google.com/drive/1u8larhpxy8w4mMsJiSBddNOzFGj7_RTn?usp=sharing) 来加载一些训练好的自编码器并练习解释特征。

本文的核心结果似乎得到了复制。我在一个开源 1 层 GELU 语言模型的 MLP 层上训练了一个稀疏自编码器，潜在空间特征的相当一部分是可解释的。

我已经开源了两个训练好的自编码器和 [一个关于如何使用它们以及如何解释特征的教程](https://colab.research.google.com/drive/1u8larhpxy8w4mMsJiSBddNOzFGj7_RTn?usp=sharing)。我还开源了一个（非常！）粗略的 [训练代码库](https://github.com/neelnanda-io/1L-Sparse-Autoencoder)，以及一些出现的 [实现细节](https://www.alignmentforum.org/posts/fKuugaxt2XLTkASkk/open-source-replication-and-commentary-on-anthropic-s#Implementation_Details) 和训练你自己的提示。

我调查了 [解码器权重在神经元基中的稀疏程度](https://www.alignmentforum.org/posts/fKuugaxt2XLTkASkk/open-source-replication-and-commentary-on-anthropic-s#Exploring_Neuron_Sparsity)，发现它们高度分布，4% 由单个神经元很好地解释，4% 由 2 到 10 个很好地解释，其余 92% 是密集的。我发现这相当令人惊讶！尽管如此，峰度显示神经元基仍然是特权的。

![Figure 62](images/figure_062.png)

我还展示了 [一些我找到的特征的案例研究](https://www.alignmentforum.org/posts/fKuugaxt2XLTkASkk/open-source-replication-and-commentary-on-anthropic-s#Case_Studies)，如首字母大写特征和"and I"特征。

我没有发现任何死特征，但超过一半的特征形成了一个 [超低频率簇](https://www.alignmentforum.org/posts/fKuugaxt2XLTkASkk/open-source-replication-and-commentary-on-anthropic-s#Ultra_Low_Frequency_Features_Are_All_The_Same_Feature)（频率小于 1e-4）。令人惊讶的是，我发现这个簇几乎完全是相同的特征（就编码器权重而言，但就解码器权重而言不是）。在一个输入上，95% 的这些超罕见特征被触发！

- 相同的方向在随机种子之间形成，表明这是关于模型的真实事情，而不仅仅是自编码器的人工产物
- 我未能解释这个共享方向是什么
- 我试图通过训练一个与该方向正交的自编码器来修复问题，但它仍然形成一个超低频率簇（都在一个新方向上聚类）

这项工作的一个问题是编码器和解码器是否应该绑定。我发现，根据经验，[每个特征的解码器和编码器权重适度不同](https://www.alignmentforum.org/posts/fKuugaxt2XLTkASkk/open-source-replication-and-commentary-on-anthropic-s#Misc_Questions)，中值余弦相似度仅为 0.5，这是经验证据表明它们在做不同的事情，不应该绑定。从概念上讲，编码器和解码器在做不同的事情：编码器是检测，找到最佳方向投影以检测特征，最小化与其他相似特征的干扰，而解码器试图表示特征，并试图近似"真实"特征方向，而不管任何干扰。

## 附录

-->

### [作者贡献声明](index.html#author-contributions)

#### 基础设施、工具与核心算法工作

通用基础设施——我们字典学习工作的基本框架由 Adly Templeton、Trenton Bricken、Tom Henighan 和 Tristan Hume 构建和维护。Adly Templeton 与 Trenton Bricken 和 Tom Conerly 合作，进行了将我们的实验扩展到大量 token 的工程工作。Robert Lasenby 创建了允许我们训练极小语言模型的工具。Yifan Wu 导入了"Pile"数据集，以便我们可以在标准外部数据集上训练模型。Tom Conerly 广泛协助我们的基础设施和维护高质量代码。Adly Templeton 实现了自动绘图，用于在扫描中比较不同的实验。

稀疏自编码器（算法/ML）——Trenton 最初实现并倡导稀疏自编码器作为字典学习的方法。Trenton Bricken 和 Adly Templeton 随后合作进行了实现我们结果所需的研究，包括扫描超参数、迭代算法、引入"神经元重采样"方法，以及表征数据集规模的重要性。（其他作者很难传达 Trenton Bricken 和 Adly Templeton 在迭代算法和超参数上投入了多少工作。）Josh Batson 通过分析运行并与 Chris Olah、Adly Templeton 和 Trenton Bricken 设计度量来衡量成功。

分析基础设施——收集可视化背后数据的工具由 Trenton Bricken 和 Adly Templeton 创建。Tom Conerly 大大加速了这一过程。Adly Templeton 实现了执行大规模特征消融分析的工具，并创建了混洗权重模型作为基线。
**Interface（界面）** – 可视化与探索特征的界面由 Brian Chen 创建，Shan Carter 提供支持。它取代了 Trenton Bricken 开发的早期版本。

#### Analysis（分析）

**Feature Deep Dives（特征深入分析）** – 数据集示例和消融实验来自 Brian Chen 的界面工作和 Adly Templeton 的消融基础设施。Chris Olah 开发了按代理分解的激活谱图。Josh Batson 开发了 logit 散点图可视化和敏感性分析。Tom Henighan 创建了固定采样可视化。Nick Turner、Josh Batson 和 Tom Henighan 探索了如何最好地分析神经元对齐。许多人致力于系统地详细分析许多特征，包括 Tom Henighan、Josh Batson、Trenton Bricken、Adly Templeton、Nick Turner、Brian Chen 和 Chris Olah。

**Manual Analysis of Features（特征手动分析）** – Nick Turner 和 Adam Jermyn 创建了用于评估特征区间是否可解释的评分标准。Adam Jermyn 手动评分了一组随机特征。

**Automated Interpretability（自动化可解释性）** – 我们的自动化可解释性管道由 Trenton Bricken、Cem Anil、Carson Denison 和 Amanda Askell 创建。Trenton Bricken 使用它运行实验来评估我们的特征。这建立在 Shauna Kravec 早期对自动化可解释性的探索之上，并且只有在 Tim Maxwell、Nicholas Schiefer 和 Nicholas Joseph 的基础设施贡献下才成为可能。

**Feature Splitting（特征分裂）** – Josh Batson、Adam Jermyn 和 Chris Olah 分析了特征分裂。Shan Carter 生成了特征的 UMAP 图。

**Universality（普遍性）** – Josh Batson 分析了普遍性，Trenton Bricken 和 Tom Henighan 提供了工程支持。

**"Finite State Automata"（"有限状态自动机"）** – Chris Olah 分析了"有限状态自动机"。

#### Paper Production（论文制作）

**Writing（写作）** – 手稿主要由 Chris Olah、Josh Batson 和 Adam Jermyn 起草，所有其他作者提供了广泛的反馈和编辑。关于字典学习的详细附录由 Adly Templeton 和 Trenton Bricken 起草。Josh Batson 和 Chris Olah 管理了响应内部和外部反馈的修订过程。

**Illustration（插图）** – 图表由 Chris Olah、Josh Batson、Adam Jermyn 和 Shan Carter 创建，基于他们自己和其他人生成的数据。

#### Development of Intuition & Negative Results（直觉发展与负面结果）

**Early Dictionary Learning Experiments（早期字典学习实验）** – 许多作者（包括 Trenton Bricken、Adly Templeton、Tristan Hume、Tom Henighan、Adam Jermyn、Josh Batson 和 Chris Olah）进行了实验，将更传统的字典学习方法和稀疏自编码器应用于各种玩具问题和小型 MNIST 模型。这项工作的大部分重点是寻找指标，我们希望这些指标能告诉我们字典学习是否在简单环境中成功。这些实验与理论工作一起，建立了宝贵的直觉，帮助我们发现了几种算法改进，并阐明了传统字典学习的挑战。

**Sparse Architectures（稀疏架构）** – Brian Chen 运行了实验并生成了反例，说服我们相信训练具有稀疏激活的模型前景不大。至关重要的是，他生成了神经元通常孤立激活的模型，并表明它们仍然是多义的。然后他生成了文中描述的反例。Robert Lasenby 实现了基础设施，使实验稀疏激活架构变得更加容易。

#### Other（其他）

**Support（支持）** – Alex Tamkin、Karina Nguyen、Brayden McLean 和 Josiah E Burke 通过基础设施、运营支持、特征标记和评论草稿做出了各种贡献。

**Leadership（领导）** – Tom Henighan 领导了字典学习项目。Tristan Hume 领导了该项目的早期版本，然后将其移交给 Tom Henighan。Shan Carter 管理了整个团队。Chris Olah 提供了一般研究指导。

### [Acknowledgments（致谢）](index.html#acknowledgments)

我们深深感谢 Martin Wattenberg、Neel Nanda、Hoagy Cunningham、David Lindner、Logan Smith、Steven Bills、William Saunders、Jonathan Marcus、Daniel Mossing、Nick Cammarata、Robert Huben、Aidan Ewart、Nicholas Sofroniew、Anna Golubeva、Bruno Olshausen 的详细评论和反馈，这些极大地改进了我们的工作。

我们也感谢 Anthropic 的同事慷慨提供反馈，其中许多人还作为"特征派对"的一部分帮助我们探索字典学习发现的特征。我们特别感谢 Oliver Rausch、Pujaa Rajan、Anna Chen、Alexander Silverstein、Marat Freytsis、Maryam Mortazavi、Mike Lambert、Justin Spahr-Summers、Mike Lambert、Justin Spahr-Summers、Emmanuel Ameisen、Andre Callahan、Shannon Yang、Zachary Witten、Zac Hatfield-Dodds、Karina Nguyen、Avital Balwit、Amanda Askell、Brayden McLean 和 Nicholas Scheifer。

我们的工作之所以成为可能，是因为 Anthropic 所有同事的广泛支持，从基础设施到工程到运营等等。我们无法列出所有间接支持这篇论文的人，因为人数众多，但我们深深感谢他们的支持。

### [Citation Information（引用信息）](index.html#citation)

请引用为：

Bricken, et al., "Towards Monosemanticity: Decomposing Language Models With Dictionary Learning", Transformer Circuits Thread, 2023.

BibTeX Citation:

```
@article{bricken2023monosemanticity,
   title={Towards Monosemanticity: Decomposing Language Models With Dictionary Learning},
   author={Bricken, Trenton and Templeton, Adly and Batson, Joshua and Chen, Brian and Jermyn, Adam and Conerly, Tom and Turner, Nick and Anil, Cem and Denison, Carson and Askell, Amanda and Lasenby, Robert and Wu, Yifan and Kravec, Shauna and Schiefer, Nicholas and Maxwell, Tim and Joseph, Nicholas and Hatfield-Dodds, Zac and Tamkin, Alex and Nguyen, Karina and McLean, Brayden and Burke, Josiah E and Hume, Tristan and Carter, Shan and Henighan, Tom and Olah, Christopher},
   year={2023},
   journal={Transformer Circuits Thread},
   note={https://transformer-circuits.pub/2023/monosemantic-features/index.html}
}
```

### [Feature Proxies（特征代理）](index.html#appendix-proxies)

为了分析特征，我们为每个特征构建可以轻松计算的"代理"。我们的代理是在特征假设下和在完整经验分布下的字符串的对数似然比。例如，$\log(P(s|\text{base64}) / P(s))$ 或 $\log(P(s|\text{Arabic Script}) / P(s))$。我们使用对数似然代理是基于这样的直觉：特征由于与 logits 线性交互，将被激励跟踪对数似然。

由于特征在 token 上的激活部分可能是由于前面的 token（例如，阿拉伯特征在长阿拉伯字符串末尾可能触发更强），我们在到达并包括最终 token 的不同前缀上最大化对数似然比。

但是我们如何估计不同的项呢？让我们分别考虑每个部分。

#### Estimating P(s)（估计 P(s)）

为了计算 P(s)，我们使用 token 上的 unigram 分布并计算 $P(s) = \prod_{t\in s} p(t)$。

#### Estimating P(s|\text{base64}) (and other characters features)（估计 P(s|base64)（及其他字符特征））

对于 base64，我们假设我们正在建模一个随机 base64 字符串，其中字符 c 的概率为 $P(c) = 1/64$（如果它是 base64 字符），否则为 $10^{-10}$。然后我们计算 $P(s) = \prod_{c\in s} P(c)$。

我们将 DNA 建模为 [ATCG] 的随机字符串，每个概率为 1/4。

（虽然我们在这份草稿中没有使用它们，但我们发现这种方法对 hexadecimal、binary 和类似特征也很有帮助。）

#### Estimating P(s|\text{Arabic}) (and other scripts features)（估计 P(s|Arabic)（及其他文字特征））

我们还为使用独特 unicode 块的文字语言构建代理。我们将以阿拉伯语为例。

对于 $P(s|\text{Arabic})$，我们使用贝叶斯规则（即 $P(s|\text{Arabic}) = P(\text{Arabic}|s) \cdot P(s) / P(\text{Arabic})$）。对于 $P(s)$，我们使用上面讨论的方法。对于其他项，我们利用这样一个事实：检测字符是否在与阿拉伯文字相关的 Unicode 块中很容易（包括例如 [U+0600–U+06FF](https://www.compart.com/en/unicode/block/U+0600)、[U+0750–U+077F](https://www.compart.com/en/unicode/block/U+0750)）。注意，这会将语言之间共享的常见字符（如标点符号）计为非阿拉伯字符。如果字符串 s 完全由阿拉伯字符组成，$P(\text{Arabic}|s)$ 为 1；如果它包含非阿拉伯字符，$P(\text{Arabic}|s)$ 被赋予 $10^{-10}$ 的微小概率。（请记住，我们将最大化多个前缀字符串。）如果 s 由单个 token 组成且不是完整的 unicode 字符，我们对其随机出现进行采样，并观察它在给定文字中使用的时间分数。我们还通过对数据集的随机样本应用此启发式方法来估计 $P(\text{Arabic})$。

### [Feature Ablations（特征消融）](index.html#appendix-feature-ablations)

我们通过以下方式执行特征消融：在上下文中运行模型直到 MLP 层，运行自编码器计算特征激活，从上下文中每个 token 的 MLP 激活中减去特征方向乘以其激活（将 $\mathbf{x}^j$ 替换为 $\mathbf{x}^j - f_i(\mathbf{x}^j)\mathbf{d}_j$），然后完成前向传递。我们记录上下文中每个 token 的预测对数似然的所得变化，用该 token 下划线的颜色表示。因此，如果特征在序列 [A][B][C] 中的 token [B] 上活跃，并且消融该特征降低了对 C 预测的几率，那么 [B] 上会有橙色背景（激活），[C] 上会有蓝色下划线（消融效应），表明消融该特征增加了模型对 [C] 预测的损失，因此该特征负责提高模型在该上下文中预测 [C] 的能力。

### [Feature Interpretability Rubric（特征可解释性评分标准）](index.html#appendix-rubric)

我们用于评分特征可解释性的评分标准有以下说明：

- 基于所有区间的正 logits 和特征激活，形成对特征的解释。
- 在 0-3 的范围内，对这一解释的信心进行评分。
- 在 0-5 的范围内，对高激活（加粗）token 与 (1) 中解释的一致性进行评分。
- 在 0-3 的范围内，对正 logit 效应与 (1) 中解释的一致性进行评分。
- 如果某些正 logit 效应与你的解释不一致，一致和不一致的效应之间是否存在效应大小的分离？如果是，评分为 1，否则或不适用，评分为 0。
- 在 0-3 的范围内，你对这一特征的解释有多具体？

特征可解释性的总分是这些步骤评分的总和。注意最大分数为 14，因为第 4 项的完美分数意味着第 5 项不适用。

### [Feature Density Histograms（特征密度直方图）](index.html#appendix-feature-density)

在迭代不同技术时，特征密度是自编码器性能的重要代理。我们自编码器中的每个特征仅在训练集中很小百分比的 token 上激活。我们将每个特征的特征密度定义为特征具有非零值的 token 的比例。

我们假设语言模型包含大量特征，分布在特征密度分布中，并且低密度特征更难被我们的自编码器发现，因为它们在训练数据集中出现较少。使用大型训练数据集是为了尝试恢复这些低密度特征。

作为测量自编码器性能的一种方式，我们获取所有特征密度并在对数尺度上绘制它们分布的直方图。粗略地说，我们寻找两个直方图指标：我们恢复的特征数量，以及我们恢复的特征中的最小特征密度。根据经验，我们发现这些指标是主观自编码器性能的合理代理，对快速迭代周期很有用。

理想情况下，自编码器神经元应该是要么有意义的特征，要么完全死亡。确实，训练确实使一些自编码器神经元完全未使用。然而，许多神经元似乎属于第三类，我们暂时命名为超低密度簇（ultralow density cluster）。

许多特征密度直方图是双峰的。例如，考虑 A/16 的特征密度直方图：

![Figure 63](images/figure_063.png)

该直方图有两个主要模式：左侧模式在 $10^{-7}$ 左右（对应于超低密度簇），右侧模式在 $10^{-5}$ 左右。此示例中的右侧模式实际上可能分为两个模式，一个在 $10^{-5}$ 左右，另一个在 $10^{-3}$ 左右。我们仍在研究这种分裂的性质。我们将右侧模式称为"高密度簇"，尽管密度的绝对幅度非常低。根据经验，高密度簇中几乎所有特征都是可解释的，但超低密度簇中几乎所有特征都不是。顺便说一句，我们怀疑特征密度的这种双峰性可能部分解释了 Huben 观察到的跨字典 MCS 的双峰性。

在许多初步的小规模实验中，这两个簇通常是完全可分离的。然而，对于具有大量自编码器神经元和大量 L1 系数的运行，这两个簇经常重叠。

![Figure 64](images/figure_064.png)

即使在这些情况下，也可以通过结合其他统计量来分离这两个簇。对于每个特征，除了密度外，我们还绘制偏差以及解码器和编码器中对应于每个特征的向量的点积。沿这三个维度，高密度簇明显可分离。

![Figure 65](images/figure_065.png)

超低密度簇似乎是自编码器训练过程的伪影，而不是底层 transformer 的真实属性。我们继续研究这种现象的来源以及其他缓解这些特征或稳健地自动检测和过滤它们的方法。

下面，我们展示所有 Seed A 运行的特征密度直方图，按 L1 系数分组。随着我们增加自编码器神经元数量（或"N learned sparse"），我们继续发现不仅更多的特征，而且更稀有的特征，表明我们还没有耗尽单层 transformer 中的特征。

![Figure 66](images/figure_066.png)

### [Transformer Training and Preprocessing（Transformer 训练与预处理）](index.html#appendix-transformer)

我们研究的单层 transformer 是在 Pile 上训练的。我们选择在这些模型上训练 Pile 而不是 Anthropic 的内部数据集，以使我们的实验更具可重复性。虽然我们认为许多特征是普遍的，但其他特征很可能对数据集是特异的。

我们使用 Adam 优化器在 1000 亿 token 上训练 transformer。我们假设非常高数量的训练 token 可能允许我们的模型在叠加中学习更清晰的表示。这些 transformer 的 residual stream 维度为 128，内部 MLP 维度为 512。MLP 激活是 ReLU。

### [Advice for Training Sparse Autoencoders: Autoencoder Dataset and Basic Training（训练稀疏自编码器的建议：自编码器数据集与基础训练）](index.html#appendix-autoencoder-dataset)

为了创建用于自编码器训练的数据集，我们在 Pile 上评估 transformer 4000 万个上下文，并收集每个上下文中每个 token 的 ReLU 之后的 MLP 激活向量。然后我们从每个上下文中的 250 个 token 采样激活向量并将它们混洗在一起，以便批次内的样本来自不同的上下文。

对于训练，我们使用 8192 的批次大小无替换地采样 MLP 激活向量。我们发现无替换采样（即不重复数据）对于最佳结果很重要。我们执行 100 万次更新步骤，使用略多于 80 亿个激活向量，而总数据集大小为 100 亿。我们使用 Adam 优化器来最小化均方误差损失和自编码器隐藏层激活上的 L1 正则化惩罚的总和。

### [Advice for Training Sparse Autoencoders: Autoencoder Architecture（训练稀疏自编码器的建议：自编码器架构）](index.html#appendix-autoencoder)

我们的字典学习模型是单隐藏层 MLP。它作为自编码器训练，使用输入权重作为编码器，输出权重作为解码器。隐藏层比输入宽得多，并应用 ReLU 非线性。我们使用默认的 Pytorch Kaiming Uniform 初始化。

形式上，令 n 为输入和输出维度，m 为自编码器隐藏层维度。给定编码器权重 $W_e \in \mathbb{R}^{m \times n}$，解码器权重 $W_d \in \mathbb{R}^{n \times m}$（列具有单位范数），以及偏差 $\mathbf{b}_e \in \mathbb{R}^{m}$，$\mathbf{b}_d \in \mathbb{R}^{n}$，数据集 X 上的操作和损失函数为：

$$
\begin{aligned}
\bar{\mathbf{x}} &= \mathbf{x} - \mathbf{b}_{d} \\
\mathbf{f} &= \text{ReLU}( W_e \bar{\mathbf{x}}+\mathbf{b}_e ) \\
\hat{\mathbf{x}} &= W_d \mathbf{f}+\mathbf{b}_d \\
\mathcal{L} &= \frac{1}{|X|} \sum_{\mathbf{x}\in X}  ||\mathbf{x}-\hat{\mathbf{x}}||_2^2 + \lambda||\mathbf{f}||_1
\end{aligned}
$$

注意我们的隐藏层是过完备的 $m\geq n$，MSE 是每个向量元素的均值，而 L1 惩罚是求和（$\lambda$ 是 L1 系数）。隐藏层激活 $\mathbf{f}$ 是我们学习的特征。如图所示，我们从输入中减去除码器偏差，称之为预编码器偏差。回想一下，解码器也被称为"字典"，而编码器可以被视为对更强大的稀疏编码算法的线性、摊销近似。

我们对标准自编码器的修改有理论和经验消融的支持。然而，因为这些修改出现在我们研究的不同时期并且可以相互交互，我们没有提供严格的消融实验，而是提供直觉和轶事证据来说明为什么每个修改是合理的。可能还有许多重要的修改可以进一步提高性能。

以下是按章节内和章节间排序的修改摘要，按重要性大致排序：

- **Pre encoder bias（预编码器偏差）** – 这在玩具模型中提升了性能。
- **Decoder weights not tied（解码器权重未绑定）** – 学习到的编码器权重通常远非相应的解码器权重，这对于增加模型容量很重要。
- **Neuron resampling（神经元重采样）** – 帮助找到更多特征并实现更低的总损失。
- **Many training steps（许多训练步骤）** – 超出训练损失看似趋于平稳的时候。
- **Learning rate sweep（学习率扫描）** – 较低的学习率产生更多真实特征。
- **Interaction Between Adam and Decoder Normalization（Adam 与解码器归一化之间的交互）** – 一种原则性的方法来解释字典向量 L2 归一化如何与 Adam 交互，从而降低总损失。

#### [Pre-Encoder Bias（预编码器偏差）](index.html#appendix-autoencoder-bias)

在具有偏差的玩具问题上测试自编码器时，我们发现它无法产生我们[之前描述](../may-update/index.html#simple-factorization)的"bounce plots"，除非我们在解码器输出和编码器输入上都添加学习偏差项。我们将预编码器偏差约束为等于后解码器偏差的负值，并将其初始化为数据集的几何中位数。这些调查是由 Hobbhahn 的观察激发的。

#### [Decoder Weights Not Tied（解码器权重未绑定）](index.html#appendix-autoencoder-untied)

通常将单隐藏层自编码器的编码器和解码器权重绑定。然而，我们发现，在我们训练的模型中，学习到的编码器权重不是解码器权重的转置，而是巧妙地偏移以增加表示容量。具体来说，我们发现具有密切相关的字典向量的相似特征具有偏移的编码器权重，以防止噪声特征输入之间的串扰和不同特征之间的混淆。

例如，在 ["Bug" 2: Multiple Features for a Single Context](index.html#features-seem-like-bugs-2) 中，我们描述了 3 个处理不同类型 base64 字符串的特征。它们都有相似的字典向量，但事实证明，编码器权重向量虽然仍然相似，但更倾斜以帮助区分它们。

看待这一点的一种方式是，我们的自编码器正在学习多步、非线性稀疏编码算法的摊销、线性近似。允许编码器的权重独立于解码器，使我们能够拥有更多的表示容量，正如我们通过经验观察到的那样。

#### [Neuron Resampling（神经元重采样）](index.html#appendix-autoencoder-resampling)

在训练过程中，一部分自编码器神经元在大量数据点上将具有零活动。我们发现，在训练期间"重采样"这些死亡神经元可以提高可能可解释特征的数量（即那些在高密度簇中的特征，参见 [Feature Density Histograms](index.html#appendix-feature-density)）并降低总损失。这种重采样可能与 Lottery Ticket Hypothesis 兼容，并增加网络找到有希望特征方向的机会。

关于死亡神经元的一个有趣细微差别涉及超低密度簇。我们发现，如果我们增加训练步骤数，网络将杀死更多这些超低密度神经元。这加强了使用高密度簇作为有用指标的合理性，因为可能存在实际上死亡但在仅看死亡神经元数量时不会显现的神经元。

训练期间出现的死亡神经元数量似乎取决于许多因素，包括但不限于：学习率（太高）；批次大小（太低）；数据集冗余（每个上下文太多 token 或在同一数据集上重复 epoch）；训练步骤数（太多）；使用的优化器。我们在这里的结果与 Bricken 等人的结果一致。

更好的重采样策略是我们积极研究的领域。这项工作中使用的方法如下：

- 在训练步骤 25,000、50,000、75,000 和 100,000 时，识别在前 12,500 个训练步骤中未触发的神经元。
- 计算当前模型在 819,200 个输入的随机子集上的损失。
- 为每个输入向量分配一个被选中的概率，该概率与自编码器在该输入上的损失的平方成正比。
- 对于每个死亡神经元，根据这些概率采样一个输入。将输入向量重新归一化为单位 L2 范数，并将其设置为死亡自编码器神经元的字典向量。
- 对于相应的编码器向量，将输入向量重新归一化为等于存活神经元编码器权重的平均范数 × 0.2。将相应的编码器偏差元素设置为零。
- 重置每个修改的权重和偏差项的 Adam 优化器参数。

该重采样过程旨在播种新特征以适应当前自编码器表现最差的输入。重置编码器范数和偏差对于确保该重采样神经元仅对类似于用于其重新初始化的输入弱触发至关重要。我们这样做是为了最小化与网络其余部分的干扰。

这种重采样方法优于基线，包括不重采样和使用默认 Kaiming Uniform 初始化重新初始化相关编码器和解码器权重。然而，可能还有更好的重采样方法有待开发——这种方法仍然会导致突然的损失峰值，并且过于频繁地重采样会导致训练发散。

#### [Learning Rate Sweep（学习率扫描）](index.html#appendix-learning-rate-sweep)

我们使用多种学习率进行了几次训练运行，同时也改变训练步骤数，发现较低的学习率，在给定足够的训练步骤时，会产生更低的总损失和发现更多"真实"特征（如 [Feature Density Histograms](index.html#appendix-feature-density) 所示）。我们还尝试在训练过程中 annealing 学习率，但发现这不会进一步提高性能。

#### [Interaction Between Adam and Decoder Normalization（Adam 与解码器归一化之间的交互）](index.html#appendix-autoencoder-optimization)

回想一下，我们将字典向量约束为单位范数。我们第一次天真的实现只是在每个梯度步骤后重置所有向量到单位范数。这意味着任何修改向量长度的梯度更新都被移除，在 Adam 优化器使用的梯度和真实梯度之间产生差异。我们发现，在应用梯度步骤之前移除与字典向量平行的任何梯度信息，会导致总损失小幅但真实的降低。

### [Advice for Training Sparse Autoencoders: Hyperparameter Selection（训练稀疏自编码器的建议：超参数选择）](index.html#appendix-hyperparameters)

字典学习的最终目标是产生可解释且准确表示底层模型的特征。定量测量可解释性目前困难且缓慢，因此我们在测试更改或优化超参数时经常查看代理指标。我们优化超参数的方法远非完美，但我们希望分享对其他从事类似工作的研究人员可能有用的见解。

我们最常查看以下代理指标：

- **Training loss（训练损失）**：这是最简单的指标，对于测试优化器或学习率等更改很有用。不幸的是，比较改变损失函数的超参数（如 L1 系数）的训练损失没有意义。
- **[Feature Density Histograms](index.html#appendix-feature-density)**：这些直方图的具体指标包括：
  - 超低密度簇之外的活跃特征数量
  - 我们看到大量非超低密度簇特征的最小特征密度
  - 密度高于 1% 的特征数量。大量特征高于此水平似乎对应于 L1 系数太低。
- **$\mathbf{L^0}$ norm**：稀疏表示中非零条目的平均数量。我们还没有知道一种原则性的方法来确定目标稀疏度水平，但我们通常针对小于 10 或 20 的 $L^0$ 范数。我们特别不信任 $L^0$ 范数是 transformer 激活维度重要分数的解决方案。
- **Reconstructed Transformer NLL（重构 Transformer NLL）**：我们希望我们发现的特征能解释底层 transformer 的几乎所有行为。测量这一点的一种方法是获取 transformer，通过自编码器运行 MLP 激活，用自编码器预测替换 MLP 激活，测量训练数据集上的损失，并计算损失差异。

我们通常通过除以基线 transformer 性能与其在消融 MLP 层后性能之间的损失差异来归一化这一点。这给了我们由我们的 transformer 解释的 MLP 损失贡献的分数。然而，具有消融 MLP 的性能可能是一个特别糟糕的基线，因此这个百分比被认为是高估。临时实验（数据未显示）表明，通过使用小型 MLP 从头开始训练 transformer 可以达到类似高的百分比。

$L^0$ 范数和 Reconstructed Transformer NLL 指标合在一起，显示了稀疏性和解释行为之间的人类可解释权衡：

![Figure 67](images/figure_067.png)

此图中的每条线显示单个 L1 系数和不同自编码器大小的数据。最低 L1 系数被排除以创建合理的比例。

### [Activation Visualization（激活可视化）](index.html#appendix-visualization)

可视化是使用我们训练数据集的 1 亿 token 子集生成的，其中每个上下文仅取 10 个 token。我们为可视化显示所选 token 每侧四个 token 的窗口。

### [Feature UMAPs](index.html#appendix-umap)

我们从 transformer 构建两个学习特征的 UMAP 嵌入。我们将每个特征表示为维度 512（神经元数量）的向量，即其在解码器矩阵 $W_d$ 中的列。第一个 UMAP 将来自 A/0 和 A/1 的特征联合嵌入到 2 维中，并使用超参数 n_neighbors=15, metric="cosine", min_dist=0.05。第二个 UMAP 使用相同的超参数，但 min_dist=0.01，还包括来自 A/2 的特征。我们还通过将 HDBSCAN 与 min_cluster_size=3 应用于相同特征的 10 维 UMAP 嵌入（使用超参数 n_neighbors=15, metric="cosine", min_dist=0.1 拟合）来将第一个 UMAP 中的点组织成簇。特征列表按一维 UMAP 排序，该 UMAP 拟合到未聚类的特征和簇 mediods。

### [Automated Interpretability（自动化可解释性）](index.html#appendix-automated)

在这里，我们在解释重要性评分并提供额外结果之前，提供有关自动化可解释性实现的更多细节。

#### [Experimental Setup（实验设置）](index.html#appendix-automated-setup)

为了获得特征解释，Claude 2 总共提供 49 个示例：来自最高激活区间的十个示例；来自其他 12 个区间的各两个；五个完全随机的示例；以及十个最高激活 token 出现在不同上下文中的示例。我们明确保持所有这些示例与我们在测试激活预测时使用的示例分开。例如，在正文中我们讨论了一个在机器学习上下文中触发 token "the" 的特征，这里的十个示例将包含单词"the"，但在不同上下文中。我们还提供每个示例来自哪个区间的顶部和底部 logits 和标签。此外，我们在保留特征上提供八个人类演示，包括思维链推理。遵循 Bills 等人，我们所有的激活都被量化为 0-9（包括）。最后，我们要求模型在回答中简洁，不要提供它激活的 token 的具体示例。

使用生成的解释，在新的交互中，Claude 被要求预测 60 个示例的激活：来自最高激活的六个；来自其他 12 个区间的各两个；十个完全随机的；以及二十个上下文外的最高激活 token。相同的八个保留演示特征显示每个 token 应如何引发预测激活。所有示例都被混洗，每个示例来自的 logits 和区间被移除，并在模型应填写其激活预测的地方留空。为了计算效率，Claude 在单次中评分所有 60 个示例，重复每个 token 后跟其预测激活。在理想设置中，每个示例将作为其自己的提示独立给出。

注意，有时特征的示例少于 49 个解释示例和 60 个预测示例，因为我们删除了出现在特征可视化区间中的任何重复示例。然而，这发生在极少数特征上，我们删除了任何总示例少于 20 个的特征。

为了与 Bills 等人比较，下图包括 Pearson 相关性以及文中其他地方使用的 Spearman。分布和总体结论与 Spearman 几乎相同。

![Figure 68](images/figure_068.png)

我们还使用 Claude 系统地编目特征输出权重 logits。我们使用相同的 Claude 生成的解释来预测激活并提供 100 个 logits，50 个随机获取，50 个是第 10-60 大的正 logits（前 10 个用于生成原始解释，因此保留）。Claude 被要求输出一个二元标签，表示在给定解释的情况下，这个 logit 是否可能在特征触发后出现。注意随机表现是 50%。A/1 特征比神经元好得多，中位数为 0.74，而神经元为 0.53，随机 transformer 为 0.5。

#### [Randomized Transformer（随机 Transformer）](index.html#appendix-automated-randomized)

作为进一步的消融，我们将人类和自动化可解释性方法与随机 transformer 进行比较。随机 transformer 的 logit 权重预测围绕随机机会居中并不令人惊讶，这是由其随机权重的本质决定的。手动可解释性也偏向 A/1 特征。然而，对于自动化可解释性，随机特征具有更高的中位数分数。

事实证明，随机 transformer 特征明显是双峰的，由单 token 和多义簇组成，它们在下图底部的插图中分开。

![Figure 69](images/figure_069.png)

如果在前 20 个示例的最高激活区间中，具有最大激活的 token 相同，则特征被标记为"单 token"。随机 transformer 的单 token 特征不仅数量更多，而且更真正的单 token，例如，即使在最弱激活区间中也为相同 token 触发。这使得它们更容易评分，如高分黄色峰值所示（图底部行左侧）。

同时，对于非"单 token"簇，A/1 特征得分更高，而随机特征实际上具有与多义神经元相似的分布。

注意，随机 transformer 特征的这种双峰聚类也得到手动人类分析的支持，其中在 0 处有一个簇（与正文中给予多义神经元的分数相同）和一个非零簇。非零簇在这里得分比 A/1 特征差（与自动化方法不同），因为评分标准的一部分考虑了 logit 可解释性，这在洗牌情况下得分为零。

随机 transformer 学习更多高度单 token 特征的事实符合字典学习将学习数据集的特征而非 transformer 的表示的假设。

#### [Importance Scoring（重要性评分）](index.html#appendix-automated-importance-scoring)

重要性评分是原则性的方法，用于纠正我们未随机采样模型被要求评分的所有示例的事实。形式上，我们给来自随机示例的所有 token 分配权重 1，给来自每个特征区间的示例分配权重 feature_density*interval_probability。feature_density 是该特征在数据集大部分上触发的时间分数，interval_probability 将非零激活的分布转换为对应于每个区间的分类分布并使用相应的概率。然后我们在 Spearman 相关性中使用这些权重，如前所述。上下文外的最高激活 token 示例继承最高激活示例分位数的权重。

重要性评分的问题在于，因为我们的特征密度通常在 $10^{-3}$ 到 $10^{-6}$ 范围内（见下一个附录部分），几乎所有权重都分配给特征几乎从不触发的随机示例。因此，特征可能通过几乎总是预测零而得分良好，反过来偏向过于限制性的解释，说明特征不触发什么，而不是它触发什么。相反，即使很小的假阳性率也会受到高度惩罚，因为真实发生率非常低。

下图显示了特征和神经元的重要性评分。注意，现在许多特征的分数非常接近零，而神经元受到的影响相对较小。我们假设这是因为神经元在更多义的情况下，有更多非零激活，在触发和不触发的事情上测试其解释。根据经验，对特征取平均，来自随机示例的 88% 的真实激活为零，而神经元为 54%（中位数分别约为 91% 和 58%）。

![Figure 70](images/figure_070.png)

#### [Explanation Lengths Caveat（解释长度注意事项）](index.html#appendix-automated-explanation-length)

Claude 有时会未能将其解释包装在 `<answer></answer>` 解释标签中，导致使用完整的思维链。这可能长得多，并泄露更多特征触发的特定单词。

这里我们绘制每个解释中的字符数，其中右侧的第二个模式突出了这些情况。然而，这不仅很少发生，而且在特征、神经元和随机 transformer 结果中都发生。事实上，它在神经元上发生最频繁，发生 19% 的时间，而随机 transformer 为 15%，特征为 13%。最重要的是，当我们分开长解释和短解释的表现时，它确实导致明显不同的分数。

![Figure 71](images/figure_071.png)

总之，虽然自动化可解释性对于我们才刚刚开始研究的模型来说是一项困难的任务，但它已经非常有用，可以以可扩展的方式快速理解字典学习特征。我们鼓励读者探索具有自动化可解释性分数的可视化：[A/1](vis/a1.html)、[A/0](vis/a0.html)、[随机模型特征](vis/random1.html)、[神经元](vis/a-neurons.html)。
