这是一篇关于 Andrej Karpathy 这段“原子级”GPT 代码的学习笔记。

---

# 📝 【硬核拆解】徒手搓 GPT：Karpathy 的“原子级”Python 代码解读

> **核心看点**：这段代码展示了在没有任何深度学习框架（如 PyTorch/TensorFlow）和矩阵运算库（如 NumPy）的情况下，如何仅用 Python 标准库（`math`, `random`）从零构建一个能够训练和推理的 GPT 模型。
>
> **一句话总结**：**一切皆为计算图，一切皆为链式法则。**
>
> 可视化讲解：https://microgpt.enescang.dev/

---

## 1. 地基：手搓自动微分引擎 (`class Value`)

这是整个代码的灵魂。Karpathy 在这里复现了一个微型的 Autograd 引擎（类似他的 `micrograd` 项目）。

*   **设计哲学**：为了能训练神经网络，我们需要知道调整哪个参数能降低 Loss。这需要**反向传播（Backpropagation）**。
*   **实现细节**：
    * 每个 `Value` 对象包装一个标量数据（`data`）和它的梯度（`grad`）。
    *   **运算重载**：重写了 `__add__`（加）、`__mul__`（乘）、`relu`、`log` 等运算。当你做 `c = a * b` 时，它不仅计算结果，还记下了 `a` 和 `b` 是 `c` 的“孩子”，并记下了局部导数（`_local_grads`）。
    *   **拓扑排序与反向传播**：`backward()` 函数通过**拓扑排序**（Topological Sort）确保在计算某个节点的梯度前，它的所有后继节点的梯度都已经计算完毕，然后通过**链式法则**递归回传梯度。

## 2. 数据准备：字符级 Tokenizer

这就好比让 AI 学说话前先认字。

*   **Tokenizer**：这里非常简单，是**字符级（Character-level）**。
    * 词表（Vocab）：数据集中所有出现过的唯一字符 + 1 个特殊的 `BOS`（Beginning of Sequence）标记。
    * 输入：`['a', 'b', 'c']` $\rightarrow$ `[1, 2, 3]`。

## 3. 骨架：GPT 模型架构

函数 `gpt(...)` 定义了模型的前向传播逻辑。虽然代码短，但它包含了 Transformer 的所有关键组件（除了 Dropout 和 Bias）。

### 3.1 嵌入层 (Embeddings)

*   **Token Embedding (`wte`)**：把字变成向量。
*   **Position Embedding (`wpe`)**：GPT 需要知道“第几个字”，这里使用的是可学习的位置编码，而不是正弦位置编码。
*   **输入** = Token 向量 + 位置向量。

### 3.2 Transformer Block (层)

这里通过循环 `n_layer` 次来堆叠层。每层包含两个核心子层：

1.  **多头注意力机制 (Multi-Head Attention)**：
    *   **Q, K, V**：通过线性层（`linear`）生成 Query, Key, Value。
    *   **KV-Cache**：注意代码中的 `keys[li].append(k)` 和 `values[li].append(v)`。这是一个非常有趣的细节！通常训练时我们会利用矩阵并行一次性计算所有 Masked Attention，但这里为了代码逻辑统一（且因为没有矩阵库），Karpathy 选择了**串行训练**（一个 Token 一个 Token 地喂），因此训练过程也使用了推理时常用的 KV Cache 技术。
    *   **Attention 公式**：$\text{softmax}(\frac{Q K^T}{\sqrt{d_k}}) V$。代码里用列表推导式硬写了这个数学公式。
2.  **前馈神经网络 (MLP)**：
    * 结构：Linear $\rightarrow$ ReLU $\rightarrow$ Linear。
    * 作用：增加非线性，整合特征。

### 3.3 细节处理

*   **RMSNorm**：使用了 Root Mean Square Layer Normalization（去除了均值项，比标准 LayerNorm 更简单且效果相当），用于稳定训练。
*   **残差连接 (Residual Connection)**：`x = [a + b for a, b in zip(x, x_residual)]`，防止梯度消失，让网络能做得更深。

## 4. 训练循环：极简的 Adam 优化器

这部分代码展示了如何在没有 PyTorch `optim` 模块的情况下更新参数。

*   **损失函数**：**负对数似然 (Negative Log Likelihood)**。
    *   `loss_t = -probs[target_id].log()`。目标概率越大，Loss 越小。
*   **手动 Adam**：
    *   Adam 需要维护两个动量：一阶矩 `m`（梯度的移动平均）和二阶矩 `v`（梯度平方的移动平均）。
    * 代码手动实现了 Adam 的更新公式：
        $$ \theta_{t+1} = \theta_t - \eta \frac{\hat{m}}{\sqrt{\hat{v}} + \epsilon} $$
    * 包含 Bias correction（偏差修正）和学习率衰减。

## 5. 推理 (Inference)

模型训练完后，“做梦”的过程。

*   **Temperature**：控制生成的随机性。
    *   `logits / temperature`。温度越低，分布越尖锐（越保守）；温度越高，分布越平缓（越胡说八道）。
*   **Sampling**：使用 `random.choices` 根据概率分布采样下一个字符，直到遇到 `BOS` 结束。

---

## 💡 深度思考：这段代码告诉了我们什么？

1.  **去魅**：ChatGPT 看起来高深莫测，但拆解到最底层，就是加减乘除、指数对数，加上链式法则求导。没有魔法，只有数学。
2.  **效率 vs 原理**：这段代码的效率极低（纯 Python 循环，无向量化），在现代 GPU 上训练大模型时，我们会把这些循环全部变成矩阵乘法（Matrix Multiplication）。Karpathy 在开头注释写道：*Everything else is just efficiency*（其余的只是效率问题）。
3.  **串行训练的代价**：注意看训练循环 `for pos_id in range(n)`。标准的 GPT 训练是并行的（一次性预测所有位置的下一个 Token），而这里为了代码可读性和“原子性”，采用了串行预测。这意味着它的训练速度是 $O(N)$ 而不是并行下的 $O(1)$ (就时间步而言)。

## Code

```python
The most atomic way to train and inference a GPT in pure, dependency-free Python.
This file is the complete algorithm.
Everything else is just efficiency.

@karpathy
"""

import os       # os.path.exists
import math     # math.log, math.exp
import random   # random.seed, random.choices, random.gauss, random.shuffle
random.seed(42) # Let there be order among chaos

# Let there be an input dataset `docs`: list[str] of documents (e.g. a dataset of names)
if not os.path.exists('input.txt'):
    import urllib.request
    names_url = 'https://raw.githubusercontent.com/karpathy/makemore/refs/heads/master/names.txt'
    urllib.request.urlretrieve(names_url, 'input.txt')
docs = [l.strip() for l in open('input.txt').read().strip().split('\n') if l.strip()] # list[str] of documents
random.shuffle(docs)
print(f"num docs: {len(docs)}")

# Let there be a Tokenizer to translate strings to discrete symbols and back
uchars = sorted(set(''.join(docs))) # unique characters in the dataset become token ids 0..n-1
BOS = len(uchars) # token id for the special Beginning of Sequence (BOS) token
vocab_size = len(uchars) + 1 # total number of unique tokens, +1 is for BOS
print(f"vocab size: {vocab_size}")

# Let there be Autograd, to recursively apply the chain rule through a computation graph
class Value:
    __slots__ = ('data', 'grad', '_children', '_local_grads') # Python optimization for memory usage

    def __init__(self, data, children=(), local_grads=()):
        self.data = data                # scalar value of this node calculated during forward pass
        self.grad = 0                   # derivative of the loss w.r.t. this node, calculated in backward pass
        self._children = children       # children of this node in the computation graph
        self._local_grads = local_grads # local derivative of this node w.r.t. its children

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.data + other.data, (self, other), (1, 1))

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.data * other.data, (self, other), (other.data, self.data))

    def __pow__(self, other): return Value(self.data**other, (self,), (other * self.data**(other-1),))
    def log(self): return Value(math.log(self.data), (self,), (1/self.data,))
    def exp(self): return Value(math.exp(self.data), (self,), (math.exp(self.data),))
    def relu(self): return Value(max(0, self.data), (self,), (float(self.data > 0),))
    def __neg__(self): return self * -1
    def __radd__(self, other): return self + other
    def __sub__(self, other): return self + (-other)
    def __rsub__(self, other): return other + (-self)
    def __rmul__(self, other): return self * other
    def __truediv__(self, other): return self * other**-1
    def __rtruediv__(self, other): return other * self**-1

    def backward(self):
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._children:
                    build_topo(child)
                topo.append(v)
        build_topo(self)
        self.grad = 1
        for v in reversed(topo):
            for child, local_grad in zip(v._children, v._local_grads):
                child.grad += local_grad * v.grad

# Initialize the parameters, to store the knowledge of the model.
n_embd = 16     # embedding dimension
n_head = 4      # number of attention heads
n_layer = 1     # number of layers
block_size = 16 # maximum sequence length
head_dim = n_embd // n_head # dimension of each head
matrix = lambda nout, nin, std=0.08: [[Value(random.gauss(0, std)) for _ in range(nin)] for _ in range(nout)]
state_dict = {'wte': matrix(vocab_size, n_embd), 'wpe': matrix(block_size, n_embd), 'lm_head': matrix(vocab_size, n_embd)}
for i in range(n_layer):
    state_dict[f'layer{i}.attn_wq'] = matrix(n_embd, n_embd)
    state_dict[f'layer{i}.attn_wk'] = matrix(n_embd, n_embd)
    state_dict[f'layer{i}.attn_wv'] = matrix(n_embd, n_embd)
    state_dict[f'layer{i}.attn_wo'] = matrix(n_embd, n_embd)
    state_dict[f'layer{i}.mlp_fc1'] = matrix(4 * n_embd, n_embd)
    state_dict[f'layer{i}.mlp_fc2'] = matrix(n_embd, 4 * n_embd)
params = [p for mat in state_dict.values() for row in mat for p in row] # flatten params into a single list[Value]
print(f"num params: {len(params)}")

# Define the model architecture: a stateless function mapping token sequence and parameters to logits over what comes next.
# Follow GPT-2, blessed among the GPTs, with minor differences: layernorm -> rmsnorm, no biases, GeLU -> ReLU
def linear(x, w):
    return [sum(wi * xi for wi, xi in zip(wo, x)) for wo in w]

def softmax(logits):
    max_val = max(val.data for val in logits)
    exps = [(val - max_val).exp() for val in logits]
    total = sum(exps)
    return [e / total for e in exps]

def rmsnorm(x):
    ms = sum(xi * xi for xi in x) / len(x)
    scale = (ms + 1e-5) ** -0.5
    return [xi * scale for xi in x]

def gpt(token_id, pos_id, keys, values):
    tok_emb = state_dict['wte'][token_id] # token embedding
    pos_emb = state_dict['wpe'][pos_id] # position embedding
    x = [t + p for t, p in zip(tok_emb, pos_emb)] # joint token and position embedding
    x = rmsnorm(x)

    for li in range(n_layer):
        # 1) Multi-head attention block
        x_residual = x
        x = rmsnorm(x)
        q = linear(x, state_dict[f'layer{li}.attn_wq'])
        k = linear(x, state_dict[f'layer{li}.attn_wk'])
        v = linear(x, state_dict[f'layer{li}.attn_wv'])
        keys[li].append(k)
        values[li].append(v)
        x_attn = []
        for h in range(n_head):
            hs = h * head_dim
            q_h = q[hs:hs+head_dim]
            k_h = [ki[hs:hs+head_dim] for ki in keys[li]]
            v_h = [vi[hs:hs+head_dim] for vi in values[li]]
            attn_logits = [sum(q_h[j] * k_h[t][j] for j in range(head_dim)) / head_dim**0.5 for t in range(len(k_h))]
            attn_weights = softmax(attn_logits)
            head_out = [sum(attn_weights[t] * v_h[t][j] for t in range(len(v_h))) for j in range(head_dim)]
            x_attn.extend(head_out)
        x = linear(x_attn, state_dict[f'layer{li}.attn_wo'])
        x = [a + b for a, b in zip(x, x_residual)]
        # 2) MLP block
        x_residual = x
        x = rmsnorm(x)
        x = linear(x, state_dict[f'layer{li}.mlp_fc1'])
        x = [xi.relu() for xi in x]
        x = linear(x, state_dict[f'layer{li}.mlp_fc2'])
        x = [a + b for a, b in zip(x, x_residual)]

    logits = linear(x, state_dict['lm_head'])
    return logits

# Let there be Adam, the blessed optimizer and its buffers
learning_rate, beta1, beta2, eps_adam = 0.01, 0.85, 0.99, 1e-8
m = [0.0] * len(params) # first moment buffer
v = [0.0] * len(params) # second moment buffer

# Repeat in sequence
num_steps = 1000 # number of training steps
for step in range(num_steps):

    # Take single document, tokenize it, surround it with BOS special token on both sides
    doc = docs[step % len(docs)]
    tokens = [BOS] + [uchars.index(ch) for ch in doc] + [BOS]
    n = min(block_size, len(tokens) - 1)

    # Forward the token sequence through the model, building up the computation graph all the way to the loss.
    keys, values = [[] for _ in range(n_layer)], [[] for _ in range(n_layer)]
    losses = []
    for pos_id in range(n):
        token_id, target_id = tokens[pos_id], tokens[pos_id + 1]
        logits = gpt(token_id, pos_id, keys, values)
        probs = softmax(logits)
        loss_t = -probs[target_id].log()
        losses.append(loss_t)
    loss = (1 / n) * sum(losses) # final average loss over the document sequence. May yours be low.

    # Backward the loss, calculating the gradients with respect to all model parameters.
    loss.backward()

    # Adam optimizer update: update the model parameters based on the corresponding gradients.
    lr_t = learning_rate * (1 - step / num_steps) # linear learning rate decay
    for i, p in enumerate(params):
        m[i] = beta1 * m[i] + (1 - beta1) * p.grad
        v[i] = beta2 * v[i] + (1 - beta2) * p.grad ** 2
        m_hat = m[i] / (1 - beta1 ** (step + 1))
        v_hat = v[i] / (1 - beta2 ** (step + 1))
        p.data -= lr_t * m_hat / (v_hat ** 0.5 + eps_adam)
        p.grad = 0

    print(f"step {step+1:4d} / {num_steps:4d} | loss {loss.data:.4f}")

# Inference: may the model babble back to us
temperature = 0.5 # in (0, 1], control the "creativity" of generated text, low to high
print("\n--- inference (new, hallucinated names) ---")
for sample_idx in range(20):
    keys, values = [[] for _ in range(n_layer)], [[] for _ in range(n_layer)]
    token_id = BOS
    sample = []
    for pos_id in range(block_size):
        logits = gpt(token_id, pos_id, keys, values)
        probs = softmax([l / temperature for l in logits])
        token_id = random.choices(range(vocab_size), weights=[p.data for p in probs])[0]
        if token_id == BOS:
            break
        sample.append(uchars[token_id])
    print(f"sample {sample_idx+1:2d}: {''.join(sample)}")
```
