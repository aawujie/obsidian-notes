import marimo

__generated_with = "0.8.22"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    print(f"PyTorch {torch.__version__}")
    return F, mo, nn, torch


@app.cell
def __(mo):
    mo.md(
        """
        # PyTorch 基础速查

        **目标:** 看懂 Transformer 代码需要的所有 PyTorch 语法。

        前置要求: 会 Python 就行，不需要懂深度学习。
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## 0. 变量命名规范 — 看懂 Transformer 代码的前提

        ### Marimo 的 `_` 前缀规则

        在 Marimo notebook 里:
        - `_x` (有下划线): **私有变量**，只在当前 cell 里有效，其他 cell 看不到
        - `x` (无下划线): **公开变量**，其他 cell 可以引用它

        如果两个 cell 都定义了 `x`（没有 `_`），Marimo 会报错 `MultipleDefinitionError`。
        所以临时变量、演示变量都加 `_` 前缀。

        **这是 Marimo 特有的规则，普通 Python 不需要。**

        ### Transformer 常用变量名

        | 变量名 | 含义 | 原论文值 |
        |---|---|---|
        | `d_model` | 模型隐藏维度（每个词的向量长度）| 512 |
        | `d_k` | 每个注意力头的维度 = d_model / num_heads | 64 |
        | `d_v` | Value 的维度（通常和 d_k 相同）| 64 |
        | `d_ff` | FFN 中间层维度（通常 4 × d_model）| 2048 |
        | `num_heads` / `h` | 注意力头数 | 8 |
        | `num_layers` / `N` | 编码器/解码器层数 | 6 |
        | `seq_len` / `n` | 序列长度（一句话几个词）| 可变 |
        | `batch_size` / `bs` | 一批多少个样本 | 可变 |
        | `vocab_size` | 词表大小（总共认识多少词）| ~30000 |

        ### 命名规律

        - `d_` 开头 = dimension（维度）
        - `num_` 开头 = number of（数量）
        - `src_` = source（源语言，如英文）
        - `tgt_` = target（目标语言，如法文）
        - `enc_` = encoder（编码器）
        - `dec_` = decoder（解码器）

        ### 组合例子

        - `_d_model = 64` → "这个 cell 里，模型维度设为 64"
        - `src_vocab_size` → "源语言的词表大小"
        - `enc_output` → "编码器的输出"
        - `tgt_mask` → "目标语言的掩码"
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## 1. 张量 (Tensor) = 多维数组

        | 维度 | 名称 | 例子 |
        |---|---|---|
        | 0维 | 标量 | 温度 36.5 |
        | 1维 | 向量 | [1, 2, 3] |
        | 2维 | 矩阵 | 一张灰度图 |
        | 3维 | 3D张量 | 一批句子 (batch, seq_len, features) |
        """
    )
    return


@app.cell
def __(torch):
    # 创建张量的几种方式
    _a = torch.tensor([1, 2, 3])             # 从列表
    _b = torch.zeros(2, 3)                    # 全零: 2行3列
    _c = torch.ones(2, 3)                     # 全一
    _d = torch.randn(2, 3)                    # 随机正态分布
    _e = torch.randint(0, 10, (2, 3))         # 随机整数 [0, 10)

    print("从列表创建:", _a)
    print("全零 (2×3):\n", _b)
    print("随机正态 (2×3):\n", _d)
    print("随机整数 (2×3):\n", _e)
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## 2. shape 和 size() — 张量的"体检表"

        `.shape` 和 `.size()` 是一样的，返回每个维度的大小。

        Transformer 里最常见的形状: `(batch, seq_len, d_model)`
        - batch = 一批里有几个样本
        - seq_len = 序列长度（几个词）
        - d_model = 每个词的特征维度
        """
    )
    return


@app.cell
def __(torch):
    _x = torch.randn(2, 5, 64)  # 2个样本, 5个词, 64维特征

    print(f"x.shape     = {_x.shape}")        # torch.Size([2, 5, 64])
    print(f"x.size()    = {_x.size()}")        # 同上
    print(f"x.size(0)   = {_x.size(0)}")       # 第0维 = 2 (batch)
    print(f"x.size(1)   = {_x.size(1)}")       # 第1维 = 5 (seq_len)
    print(f"x.size(2)   = {_x.size(2)}")       # 第2维 = 64 (d_model)
    print(f"x.size(-1)  = {_x.size(-1)}")      # 最后一维 = 64 ← Transformer 里常用!
    print(f"x.size(-2)  = {_x.size(-2)}")      # 倒数第二维 = 5
    print()
    print("理解 -1: Python 里负数索引表示从后往前数")
    print(f"  列表版: ['a','b','c'][-1] = {'abc'[-1]}")
    print(f"  张量版: shape=(2,5,64) 的 size(-1) = 64")
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## 3. view / reshape — 改变形状

        `view` 和 `reshape` 都可以改变张量的形状，**不改变数据**。

        Transformer 里多头注意力要把 `(batch, seq, d_model)`
        拆成 `(batch, seq, num_heads, d_k)` 再转置。
        """
    )
    return


@app.cell
def __(torch):
    _x = torch.arange(12)  # [0, 1, 2, ..., 11]
    print(f"原始: {_x}  shape={_x.shape}")

    _a = _x.view(3, 4)     # 变成 3行4列
    print(f"view(3,4):\n{_a}")

    _b = _x.view(2, -1)    # -1 表示"自动计算": 12/2=6
    print(f"view(2,-1):\n{_b}  ← -1 自动算出 6")

    _c = _x.view(2, 2, 3)  # 变成 3D
    print(f"view(2,2,3):\n{_c}")
    return


@app.cell
def __(torch):
    # Transformer 多头注意力的关键操作
    _batch, _seq, _d_model, _heads = 2, 5, 64, 4
    _d_k = _d_model // _heads  # 64/4 = 16

    _x = torch.randn(_batch, _seq, _d_model)  # (2, 5, 64)
    print(f"原始: {_x.shape}")

    # 拆分多头: (batch, seq, d_model) → (batch, seq, heads, d_k)
    _y = _x.view(_batch, _seq, _heads, _d_k)
    print(f"view 拆头: {_y.shape}")

    # 转置: (batch, seq, heads, d_k) → (batch, heads, seq, d_k)
    _z = _y.transpose(1, 2)
    print(f"transpose(1,2): {_z.shape}  ← 每个头独立处理!")
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## 4. transpose — 交换两个维度

        `x.transpose(dim0, dim1)` 交换第 dim0 和 dim1 维。

        类比: 矩阵转置 = 行变列，高维张量也可以交换任意两个维度。
        """
    )
    return


@app.cell
def __(torch):
    _x = torch.randn(2, 3, 4)
    print(f"原始: {_x.shape}")              # (2, 3, 4)
    print(f"transpose(1,2): {_x.transpose(1, 2).shape}")  # (2, 4, 3)
    print(f"transpose(-2,-1): {_x.transpose(-2, -1).shape}")  # 同上

    print("\n在注意力中: Q·Kᵀ 需要 K 的最后两维转置")
    _Q = torch.randn(2, 3, 8)  # (batch, seq_q, d_k)
    _K = torch.randn(2, 5, 8)  # (batch, seq_k, d_k)
    _scores = torch.matmul(_Q, _K.transpose(-2, -1))
    print(f"Q{tuple(_Q.shape)} × K.T{tuple(_K.transpose(-2,-1).shape)} = scores{tuple(_scores.shape)}")
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## 5. matmul — 矩阵乘法

        `torch.matmul(A, B)` 或 `A @ B`

        这是注意力机制的核心: $QK^T$ 和 $\text{weights} \cdot V$ 都是矩阵乘法。
        """
    )
    return


@app.cell
def __(torch):
    # 2D: 普通矩阵乘法
    _A = torch.randn(3, 4)  # 3×4
    _B = torch.randn(4, 5)  # 4×5
    _C = torch.matmul(_A, _B)
    print(f"2D: {tuple(_A.shape)} × {tuple(_B.shape)} = {tuple(_C.shape)}")

    # 3D: batch 矩阵乘法 (每个样本独立算)
    _A3 = torch.randn(2, 3, 4)  # batch=2, 3×4
    _B3 = torch.randn(2, 4, 5)  # batch=2, 4×5
    _C3 = torch.matmul(_A3, _B3)
    print(f"3D: {tuple(_A3.shape)} × {tuple(_B3.shape)} = {tuple(_C3.shape)}")

    print("\n规则: 最后两维做矩阵乘法，前面的维度按 batch 对齐")
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## 6. softmax — 变成概率

        把任意实数变成 [0,1] 之间、加起来=1 的概率。

        $\text{softmax}(x_i) = \frac{e^{x_i}}{\sum_j e^{x_j}}$

        大的值变成大概率，小的值变成小概率。
        """
    )
    return


@app.cell
def __(F, torch):
    _scores = torch.tensor([2.0, 1.0, 0.1])
    _probs = F.softmax(_scores, dim=-1)  # dim=-1: 在最后一维做 softmax
    print(f"原始分数: {_scores.tolist()}")
    print(f"softmax:  {[f'{p:.3f}' for p in _probs]}")
    print(f"和:       {_probs.sum():.3f}")
    print()

    # dim 参数很重要: 指定在哪个维度做 softmax
    _x = torch.tensor([[1.0, 2.0, 3.0],
                        [1.0, 1.0, 1.0]])
    print(f"2D 输入:\n{_x}")
    print(f"dim=-1 (每行内部): \n{F.softmax(_x, dim=-1)}")
    print(f"↑ 每行加起来=1")
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## 7. masked_fill — 遮住不该看的

        `x.masked_fill(mask, value)`: mask 为 True 的位置填入 value。

        Transformer 用它实现:
        - **Padding mask**: 忽略填充位置
        - **因果 mask**: 不让解码器偷看未来
        """
    )
    return


@app.cell
def __(F, torch):
    _scores = torch.tensor([[1.0, 2.0, 3.0, 4.0]])

    # mask: 0 表示"遮住", 1 表示"可看"
    _mask = torch.tensor([[1, 1, 0, 0]])  # 只能看前两个位置

    # 被遮住的位置填 -inf
    _masked = _scores.masked_fill(_mask == 0, float('-inf'))
    print(f"原始分数:   {_scores.tolist()}")
    print(f"mask:       {_mask.tolist()}")
    print(f"masked_fill: {_masked.tolist()}")

    # softmax 后 -inf 变成 0
    _probs = F.softmax(_masked, dim=-1)
    print(f"softmax:    {[f'{p:.3f}' for p in _probs[0]]}")
    print("↑ 位置2和3的权重变成了0!")
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## 8. nn.Module — 模型的积木

        PyTorch 里所有模型都继承 `nn.Module`。

        常用层:
        | 层 | 作用 | Transformer 用途 |
        |---|---|---|
        | `nn.Linear(in, out)` | 线性变换 y=xW+b | Q/K/V 投影, FFN |
        | `nn.Embedding(vocab, dim)` | 词→向量查表 | 词嵌入 |
        | `nn.LayerNorm(dim)` | 层归一化 | Add&Norm |
        | `nn.Dropout(p)` | 随机丢弃 p 比例 | 防过拟合 |
        """
    )
    return


@app.cell
def __(nn, torch):
    # nn.Linear: 线性变换 (全连接层)
    _linear = nn.Linear(64, 128)  # 输入64维 → 输出128维
    _x = torch.randn(2, 5, 64)   # (batch=2, seq=5, 64维)
    _y = _linear(_x)
    print(f"nn.Linear(64, 128):")
    print(f"  输入: {tuple(_x.shape)} → 输出: {tuple(_y.shape)}")
    print(f"  参数: W={tuple(_linear.weight.shape)}, b={tuple(_linear.bias.shape)}")
    return


@app.cell
def __(nn, torch):
    # nn.Embedding: 词嵌入查表
    _emb = nn.Embedding(100, 64)   # 词表100个词, 每词64维
    _ids = torch.tensor([[1, 5, 3],  # 第1个句子: 词1,词5,词3
                          [2, 8, 0]])  # 第2个句子: 词2,词8,词0
    _vecs = _emb(_ids)
    print(f"nn.Embedding(vocab=100, dim=64):")
    print(f"  输入 token IDs: {tuple(_ids.shape)} → 输出向量: {tuple(_vecs.shape)}")
    print(f"  把每个整数 ID 查表变成 64 维向量")
    return


@app.cell
def __(nn, torch):
    # nn.LayerNorm: 层归一化
    _ln = nn.LayerNorm(64)
    _x = torch.randn(2, 5, 64) * 10 + 5  # 故意让均值偏大
    _y = _ln(_x)
    print(f"nn.LayerNorm(64):")
    print(f"  归一化前: 均值={_x.mean():.2f}, 标准差={_x.std():.2f}")
    print(f"  归一化后: 均值={_y.mean():.2f}, 标准差={_y.std():.2f}")
    print(f"  ↑ 让每层输入的分布稳定，加速训练")
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## 9. contiguous — 内存连续

        `transpose` 后数据在内存中不连续，`view` 会报错。
        加 `.contiguous()` 让数据重排为连续存储。

        这是纯粹的内存布局问题，不影响数值。
        """
    )
    return


@app.cell
def __(torch):
    _x = torch.randn(2, 3, 4)
    _t = _x.transpose(1, 2)  # 交换维度后内存不连续

    print(f"transpose 前 is_contiguous: {_x.is_contiguous()}")
    print(f"transpose 后 is_contiguous: {_t.is_contiguous()}")

    try:
        _t.view(-1)  # 会报错!
    except RuntimeError as _e:
        print(f"直接 view 报错: {str(_e)[:60]}...")

    _t_cont = _t.contiguous()  # 重排内存
    print(f"contiguous 后 is_contiguous: {_t_cont.is_contiguous()}")
    print(f"contiguous 后 view 成功: {_t_cont.view(-1).shape}")
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## 10. unsqueeze / squeeze — 加减维度

        - `unsqueeze(dim)`: 在 dim 位置插入一个大小为 1 的维度
        - `squeeze(dim)`: 去掉大小为 1 的维度

        mask 经常需要用 unsqueeze 扩展维度来广播。
        """
    )
    return


@app.cell
def __(torch):
    _x = torch.tensor([1, 2, 3])
    print(f"原始: {_x.shape}")                     # (3,)
    print(f"unsqueeze(0): {_x.unsqueeze(0).shape}")  # (1, 3) — 加一行
    print(f"unsqueeze(1): {_x.unsqueeze(1).shape}")  # (3, 1) — 加一列
    print()

    # mask 的典型用法
    _seq = torch.tensor([[1, 2, 3, 0, 0]])  # (1, 5) 后两个是 padding
    _mask = (_seq != 0)                       # (1, 5) [True True True False False]
    print(f"mask: {_mask.shape} → {_mask}")
    _mask = _mask.unsqueeze(1).unsqueeze(2)   # (1, 1, 1, 5) — 广播到注意力矩阵
    print(f"扩展后: {_mask.shape} → 可以广播到 (batch, heads, seq_q, seq_k)")
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## 11. tril — 下三角矩阵

        `torch.tril` 保留下三角，上三角置零。

        这就是解码器因果掩码的核心！
        """
    )
    return


@app.cell
def __(torch):
    _ones = torch.ones(4, 4)
    _mask = torch.tril(_ones)
    print("因果掩码 (4×4):")
    print(_mask)
    print()
    print("含义:")
    print("  位置0: [1 0 0 0] — 只能看自己")
    print("  位置1: [1 1 0 0] — 能看位置0和自己")
    print("  位置2: [1 1 1 0] — 能看0、1和自己")
    print("  位置3: [1 1 1 1] — 能看所有已生成的")
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## 12. register_buffer — 非参数的常量

        `self.register_buffer('name', tensor)`:
        - **不是**可学习参数（不会被优化器更新）
        - **会**跟着模型保存/加载
        - **会**跟着 `.to(device)` 移到 GPU

        位置编码用它: 预计算好的 sin/cos 值不需要学习，但要跟着模型走。
        """
    )
    return


@app.cell
def __(nn, torch):
    class _Demo(nn.Module):
        def __init__(self):
            super().__init__()
            self.weight = nn.Parameter(torch.randn(3))  # 可学习参数
            self.register_buffer('constant', torch.tensor([1.0, 2.0, 3.0]))  # 常量

    _m = _Demo()
    print("可学习参数:")
    for _name, _p in _m.named_parameters():
        print(f"  {_name}: {_p.data} (requires_grad={_p.requires_grad})")
    print("Buffer (常量):")
    for _name, _b in _m.named_buffers():
        print(f"  {_name}: {_b} (requires_grad={_b.requires_grad})")
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## 13. 位置编码可视化 — matplotlib 画图示范

        在 Marimo 中显示图片，只需让 cell 最后一个表达式是 matplotlib Figure 对象。

        **不需要** `io.BytesIO` + `savefig` + `plt.close` 那套！
        Marimo 自动拦截 matplotlib，把 figure 渲染成图片。
        """
    )
    return


@app.cell
def __(torch):
    import math
    import matplotlib.pyplot as plt

    _n_pos, _d_pe = 128, 64
    _pe = torch.zeros(_n_pos, _d_pe)
    _pos = torch.arange(_n_pos).float().unsqueeze(1)
    _div = torch.exp(torch.arange(0, _d_pe, 2).float() * (-math.log(10000.0) / _d_pe))
    _pe[:, 0::2] = (_pos * _div).sin()
    _pe[:, 1::2] = (_pos * _div).cos()
    _z = _pe.numpy()

    _fig, _ax = plt.subplots(1, 2, figsize=(10, 3.2))
    _ax[0].imshow(_z.T, aspect="auto", cmap="RdBu_r")
    _ax[0].set(xlabel="position", ylabel="dimension", title="位置编码热力图")
    for _j in (0, 1, 4, 8, 16, 32):
        _ax[1].plot(_z[:, _j], lw=1.2, label=f"dim {_j}")
    _ax[1].set(xlabel="position", ylabel="PE value", title="不同维度的波形")
    _ax[1].legend(fontsize=7, ncol=3, loc="upper right")
    _fig.tight_layout()
    _fig
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## 14. 常用缩写速查表

        | 代码 | 含义 | 例子 |
        |---|---|---|
        | `x.size(-1)` | 最后一维大小 | (2,5,64) → 64 |
        | `x.size(0)` | 第一维 (batch) | (2,5,64) → 2 |
        | `x.view(a, -1, c)` | -1=自动计算 | (2,5,64).view(2,-1,16) → (2,20,16) |
        | `x.transpose(1,2)` | 交换第1和第2维 | (2,5,64) → (2,64,5) |
        | `x.contiguous()` | 内存连续化 | transpose 后必加 |
        | `x.unsqueeze(0)` | 在第0维加1 | (5,) → (1,5) |
        | `x.squeeze()` | 去掉大小=1的维度 | (1,5,1) → (5,) |
        | `F.softmax(x, dim=-1)` | 最后一维做softmax | 注意力权重 |
        | `x.masked_fill(m==0, -inf)` | mask为0处填-inf | 遮掩 |
        | `torch.matmul(A, B)` | 矩阵乘法 | QK^T, weights·V |
        | `torch.tril(x)` | 保留下三角 | 因果掩码 |
        | `nn.Linear(in, out)` | 线性层 | QKV投影 |
        | `nn.Embedding(v, d)` | 词嵌入 | ID→向量 |
        | `nn.LayerNorm(d)` | 层归一化 | Add&Norm |

        ---

        现在回去看 `transformer_tutorial_marimo.py` 应该就能看懂了!

        ### Marimo 显示 matplotlib 图的规则

        ```python
        # ✅ 正确: 让 figure 做最后一个表达式
        _fig, _ax = plt.subplots()
        _ax.plot([1,2,3])
        _fig

        # ❌ 错误: savefig + close，Marimo 拿不到图
        fig.savefig(buf)
        plt.close(fig)
        ```
        """
    )
    return


if __name__ == "__main__":
    app.run()
