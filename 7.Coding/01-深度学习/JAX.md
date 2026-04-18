---
notion-id: 2f478d23-e296-808a-90ef-c328d844a117
---
JAX = 高性能可微分数值计算库

一句话总结：“能在 GPU/TPU 上飞速运行的加强版 NumPy + 超级好用的自动求导”

### 核心特点（为什么很多人突然都在用它）

- 接口跟 **NumPy** 几乎一模一样（`jax.numpy` 简称 `jnp`）
- 但它能直接在 **GPU/TPU** 上跑得非常快（通过 XLA 编译）
- 内置非常强大的**自动微分**（比 PyTorch 的 autograd 更灵活，支持更高阶导数、反向模式、前向模式随便混用）
- 支持几种“魔法”函数变换：
    - `grad()` / `value_and_grad()` → 自动求导
    - `jit()` → 即时编译提速几十上百倍
    - `vmap()` → 自动向量化（类似超方便的 batch 处理）
    - `pmap()` → 简单写多卡并行

### 现在最常见的几种说法对比

| 你听到的说法 | 实际是什么 | 流行程度（2026年视角） |
| --- | --- | --- |
| “JAX 是 PyTorch 的竞品” | 不准确 | ★★★☆☆ |
| “JAX 就是加速版的 NumPy” | **最接近日常理解的说法** | ★★★★★ |
| “JAX 是下一代深度学习框架” | 半对（更偏向研究级灵活计算框架） | ★★★★☆ |
| “用 JAX 写模型比 PyTorch 快” | **在很多前沿/大规模实验场景是真的** | ★★★★★ |
| “JAX 生态已经很成熟了” | 2025-2026 年确实已经非常可用了 | 目前趋势 |

简单记忆口诀：

**“NumPy 的接口 + PyTorch 的求导 + XLA 的速度 + 研究级的灵活性” → 这就是 JAX**

office:

[https://jax-js.com/](https://jax-js.com/)

repo:

[https://github.com/jax-ml/jax](https://github.com/jax-ml/jax)

[https://github.com/ekzhang/jax-js](https://github.com/ekzhang/jax-js)

[https://github.com/openxla/xla](https://github.com/openxla/xla)


## 附录

### XLA = Accelerated Linear Algebra（加速线性代数）

- Google 开发的机器学习专用编译器（现在已开源为 OpenXLA 项目），主要用来把高层次的计算图（比如矩阵乘法、卷积、激活函数等）自动优化并编译成针对特定硬件的高效低级代码。
- XLA 就是 JAX / TensorFlow / PyTorch 的“加速引擎”：**它负责 JIT（即时编译）、操作融合（fusion）、内存优化、针对 GPU/TPU/CPU 生成最快代码**。

**在 JAX 中的关键作用**

- 当你写 `jax.jit(my_function)` 时，JAX 实际上是把函数**追踪（tracing）**成计算图，然后**交给 XLA** 去编译。
- XLA 会：
    - 融合多个操作（例如 matmul + add + relu 变成一个 kernel，减少内存读写）
    - 自动选择最优的 GPU kernel 或 TPU 指令
    - 支持 CPU、CUDA、ROCm、TPU 等后端
- 没有 XLA，JAX 的 jit、vmap、pmap 等“魔法”就无法实现高速执行。

简单比喻：
**NumPy ≈ 解释执行 JAX + XLA ≈ 编译成 C++/CUDA 级别的高速代码**

**jax-js（浏览器版）与 XLA 的关系**

- **jax-js 没有使用原生 XLA**（因为 XLA 是 C++ 后端，无法直接跑在浏览器）。
- 它**模仿 JAX 的接口和编译流程**，但自己实现了类似的 JIT 编译器：→ 把你的代码编译成 **WebGPU shader**（GPU 加速） 或 **WebAssembly**（CPU 加速）。
- 所以功能上很像（支持 jax.jit、grad 等），但底层引擎不同。
