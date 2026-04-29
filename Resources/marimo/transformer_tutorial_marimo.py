import marimo

__generated_with = "0.8.22"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import math
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    return F, math, mo, nn, torch


@app.cell
def __(mo):
    mo.md(
        r"""
        # Transformer 从零搭建教学

        纯 PyTorch 实现，不依赖任何第三方高层库。

        | 步骤 | 内容 | 核心类比 |
        |---|---|---|
        | 1 | Scaled Dot-Product Attention | 图书馆找书 |
        | 2 | Multi-Head Attention | 多个"视角"并行 |
        | 3 | Positional Encoding | 给位置发"身份证" |
        | 4 | Feed-Forward Network | 会后各自思考 |
        | 5 | Add & Norm | 梯度的高速公路 |
        | 6 | Encoder Layer | 自注意力 + FFN |
        | 7 | Decoder Layer | +掩码 + 交叉注意力 |
        | 8 | 完整 Transformer | 编码器 + 解码器 |
        | 9 | Demo | 前向传播验证 |
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 1 步: Scaled Dot-Product Attention

        **公式:** $\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right) V$

        **直觉——你在图书馆找书:**

        - **Q (Query)** = 你脑子里想找的主题
        - **K (Key)** = 每本书封面上的标签
        - **V (Value)** = 书的实际内容
        - $QK^T$ = 用主题跟每本书标签做匹配，得到相关度分数
        - $/ \sqrt{d_k}$ = 防止分数太大导致 softmax 极端化
        - softmax = 把分数变成概率（加起来 = 1）
        - $\cdot V$ = 按概率加权取出书的内容
        """
    )
    return


@app.cell
def __(F, math, torch):
    def scaled_dot_product_attention(Q, K, V, mask=None):
        d_k = Q.size(-1)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        weights = F.softmax(scores, dim=-1)
        output = torch.matmul(weights, V)
        return output, weights
    return (scaled_dot_product_attention,)


@app.cell
def __(scaled_dot_product_attention, torch):
    _Q = torch.randn(1, 3, 8)
    _K = torch.randn(1, 4, 8)
    _V = torch.randn(1, 4, 8)
    _out, _w = scaled_dot_product_attention(_Q, _K, _V)
    print(f"Q: {tuple(_Q.shape)}  K: {tuple(_K.shape)}  V: {tuple(_V.shape)}")
    print(f"输出: {tuple(_out.shape)}  权重: {tuple(_w.shape)}")
    print("注意力权重 (每行加起来=1):")
    for _i, _row in enumerate(_w[0]):
        _vals = " ".join(f"{v:.3f}" for v in _row)
        print(f"  Query {_i}: [{_vals}]  和={_row.sum():.3f}")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 2 步: Multi-Head Attention

        **为什么要多头？** 一个头只能学一种"关注模式"。

        比如 *"The animal didn't cross the street because it was too tired"*

        - 头1: "it" → "animal" (指代)
        - 头2: "tired" → "animal" (属性)

        **做法:** 把 $d_{model}$ 切成 $h$ 份 → 各自做 Attention → 拼回去
        """
    )
    return


@app.cell
def __(nn, scaled_dot_product_attention):
    class MultiHeadAttention(nn.Module):
        def __init__(self, d_model, num_heads, dropout=0.1):
            super().__init__()
            assert d_model % num_heads == 0
            self.d_model = d_model
            self.num_heads = num_heads
            self.d_k = d_model // num_heads
            self.W_q = nn.Linear(d_model, d_model)
            self.W_k = nn.Linear(d_model, d_model)
            self.W_v = nn.Linear(d_model, d_model)
            self.W_o = nn.Linear(d_model, d_model)
            self.dropout = nn.Dropout(dropout)

        def forward(self, Q, K, V, mask=None):
            bs = Q.size(0)
            # (batch, seq, d_model) -> (batch, heads, seq, d_k)
            Q = self.W_q(Q).view(bs, -1, self.num_heads, self.d_k).transpose(1, 2)
            K = self.W_k(K).view(bs, -1, self.num_heads, self.d_k).transpose(1, 2)
            V = self.W_v(V).view(bs, -1, self.num_heads, self.d_k).transpose(1, 2)
            out, w = scaled_dot_product_attention(Q, K, V, mask)
            out = self.dropout(out)
            # (batch, heads, seq, d_k) -> (batch, seq, d_model)
            out = out.transpose(1, 2).contiguous().view(bs, -1, self.d_model)
            return self.W_o(out), w
    return (MultiHeadAttention,)


@app.cell
def __(MultiHeadAttention, torch):
    _mha = MultiHeadAttention(d_model=64, num_heads=4, dropout=0.0)
    _mha.eval()
    _x = torch.randn(2, 5, 64)
    _out, _w = _mha(_x, _x, _x)
    print(f"输入: {tuple(_x.shape)} -> 输出: {tuple(_out.shape)} (形状不变!)")
    print(f"权重: {tuple(_w.shape)} (batch, heads, seq_q, seq_k)")
    print(f"每头维度: d_k = 64/4 = {64//4}")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 3 步: Positional Encoding

        注意力不知道词的顺序! "猫追狗" = "狗追猫"。

        用 sin/cos 给每个位置一个独特的"身份证":

        $$PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d}}\right), \quad PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d}}\right)$$

        ### 直观理解

        **位置编码表** = 预计算的 sin/cos 矩阵，每行是一个位置的"指纹":

        ```
        位置 | dim0(长波)   dim1(长波)   dim2(短波)   dim3(短波)  ...
        -----|----------------------------------------------------
          0  |  sin(0)       cos(0)       sin(0)       cos(0)     ← 位置0
          1  |  sin(ω₁)      cos(ω₁)      sin(ω₂)      cos(ω₂)    ← 位置1
          2  |  sin(2ω₁)     cos(2ω₁)     sin(2ω₂)     cos(2ω₂)   ← 位置2
          3  |  sin(3ω₁)     cos(3ω₁)     sin(3ω₂)     cos(3ω₂)   ← 位置3
          ...
             ↑ ω₁ 小(周期长)              ↑ ω₂ 大(周期短)
        ```

        **关键：不同维度用不同频率！**

        - dim0,1：ω₁ = 1/10000^(0/d) 很小 → 周期长，变化慢 → 捕捉**远距离**关系
        - dim2,3：ω₂ = 1/10000^(2/d) 较大 → 周期短，变化快 → 捕捉**近距离**关系

        **为什么用 sin/cos？**

        - 有界（-1 到 1），数值稳定
        - 不同频率，可以表示不同尺度的位置信息
        - 相对位置可以线性表示：PE(pos+k) 可以用 PE(pos) 线性表示

        **使用方式**：词嵌入 + 位置编码（直接相加）

        ```
        词嵌入("猫")   = [0.2, -0.5, 0.8, ..., 0.3]     (512维，表示"猫"的含义)
        位置编码(0)  = [0.0,  1.0, 0.0, ..., 1.0]     (512维，表示"第0个位置")
        ─────────────────────────────────────────────
        最终输入     = [0.2,  0.5, 0.8, ..., 1.3]     (512维，同时包含词义和位置信息)
        ```

        **一句话**：词嵌入告诉模型"这是什么词"，位置编码告诉模型"这个词在哪里"，相加后模型同时知道"什么词"和"在哪里"。
        """
    )
    return


@app.cell
def __(math, nn, torch):
    class PositionalEncoding(nn.Module):
        def __init__(self, d_model, max_len=5000, dropout=0.1):
            super().__init__()
            self.dropout = nn.Dropout(dropout)
            pe = torch.zeros(max_len, d_model)
            pos = torch.arange(0, max_len).unsqueeze(1).float()
            div = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
            pe[:, 0::2] = torch.sin(pos * div)
            pe[:, 1::2] = torch.cos(pos * div)
            self.register_buffer('pe', pe.unsqueeze(0))

        def forward(self, x):
            return self.dropout(x + self.pe[:, :x.size(1)])
    return (PositionalEncoding,)


@app.cell
def __(PositionalEncoding, torch):
    _pe = PositionalEncoding(d_model=64, dropout=0.0)
    _x = torch.zeros(1, 10, 64)
    _enc = _pe(_x)
    print(f"输入全零 {tuple(_x.shape)} -> 输出 {tuple(_enc.shape)}")
    print(f"位置0 前8维: {[f'{v:.3f}' for v in _enc[0,0,:8]]}")
    print(f"位置1 前8维: {[f'{v:.3f}' for v in _enc[0,1,:8]]}")
    print(f"位置9 前8维: {[f'{v:.3f}' for v in _enc[0,9,:8]]}")
    print("↑ 不同位置有不同编码值，模型就能区分顺序了")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ### 位置编码可视化

        - **左图（热力图）**：横轴是序列位置，纵轴是维度；颜色表示编码值（红=正，蓝=负）。
        - **右图**：4 个 subplot，每个展示**同频率**的 sin（蓝实线）和 cos（红虚线）波形：

              - 越上面频率越低（周期越长）→ 捕捉**远距离**关系
              - 越下面频率越高（周期越短）→ 捕捉**近距离**关系
        """
    )
    return


@app.cell
def __(math, torch):
    import matplotlib.pyplot as plt

    # 生成位置编码数据（用不带下划线的变量名，才能跨 cell 传递）
    pe_n_pos, pe_d = 128, 64
    pe_mat = torch.zeros(pe_n_pos, pe_d)
    pe_pos = torch.arange(pe_n_pos).float().unsqueeze(1)
    pe_div = torch.exp(torch.arange(0, pe_d, 2).float() * (-math.log(10000.0) / pe_d))
    pe_mat[:, 0::2] = (pe_pos * pe_div).sin()
    pe_mat[:, 1::2] = (pe_pos * pe_div).cos()
    pe_z = pe_mat.numpy()

    # 图1：热力图
    _fig1, _ax1 = plt.subplots(figsize=(7, 4))
    _im = _ax1.imshow(pe_z.T, aspect="auto", cmap="RdBu_r", vmin=-1, vmax=1)
    _ax1.set(xlabel="position", ylabel="dimension", title="位置编码热力图")
    plt.colorbar(_im, ax=_ax1, shrink=0.6)
    _fig1.tight_layout()
    _fig1
    return pe_d, pe_div, pe_mat, pe_n_pos, pe_pos, pe_z, plt


@app.cell
def __(mo, pe_z, plt):
    # 图2：不同频率的 sin/cos 波形（4个独立图，每个展示一对同频率的sin/cos）
    _dims_to_plot = [0, 2, 8, 16]
    _colors = ['green', 'blue', 'purple', 'orange']
    _labels = ['w1(低频)', 'w2', 'w3', 'w4(高频)']
    _figs = []

    for _idx, _dim in enumerate(_dims_to_plot):
        _fig, _ax = plt.subplots(figsize=(8, 2))
        _positions = range(pe_z.shape[0])
        _color = _colors[_idx]

        _ax.plot(_positions, pe_z[:, _dim], color=_color, lw=1.5, label=f'dim{_dim} sin')
        _ax.plot(_positions, pe_z[:, _dim+1], color=_color, lw=1.5, ls='--', alpha=0.7, label=f'dim{_dim+1} cos')

        _ax.set_ylabel(_labels[_idx], fontsize=10)
        _ax.set_ylim(-1.2, 1.2)
        _ax.legend(loc='upper right', fontsize=8)
        _ax.grid(True, alpha=0.3)

        if _idx == 0:
            _ax.set_title('频率最低（周期最长）→ 捕捉远距离关系', fontsize=9, color='green')
        elif _idx == 3:
            _ax.set_title('频率最高（周期最短）→ 捕捉近距离关系', fontsize=9, color='orange')

        if _idx == 3:
            _ax.set_xlabel('position', fontsize=10)

        _fig.tight_layout()
        _figs.append(_fig)
        plt.close(_fig)  # 防止重复显示

    mo.output.append(mo.vstack(_figs))
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 4 步: Feed-Forward Network

        $\text{FFN}(x) = \text{ReLU}(xW_1 + b_1)W_2 + b_2$

        中间维度扩大 4 倍。**类比:** 注意力=开会讨论, FFN=会后各自思考。

        ## 第 5 步: Add & Norm

        $\text{output} = \text{LayerNorm}(x + \text{Sublayer}(x))$

        **残差连接:** 梯度可以"抄近路"直接回传 (GPT-3 有 96 层!)
        """
    )
    return


@app.cell
def __(F, nn):
    class PositionwiseFFN(nn.Module):
        def __init__(self, d_model, d_ff, dropout=0.1):
            super().__init__()
            self.w1 = nn.Linear(d_model, d_ff)
            self.w2 = nn.Linear(d_ff, d_model)
            self.dropout = nn.Dropout(dropout)

        def forward(self, x):
            return self.w2(self.dropout(F.relu(self.w1(x))))

    class AddNorm(nn.Module):
        def __init__(self, d_model, dropout=0.1):
            super().__init__()
            self.norm = nn.LayerNorm(d_model)
            self.dropout = nn.Dropout(dropout)

        def forward(self, x, sublayer_output):
            return self.norm(x + self.dropout(sublayer_output))
    return AddNorm, PositionwiseFFN


@app.cell
def __(AddNorm, PositionwiseFFN, torch):
    _d_model, _d_ff = 64, 256
    _x = torch.randn(2, 5, _d_model)  # (batch=2, seq=5, d_model=64)

    _ffn = PositionwiseFFN(_d_model, _d_ff, dropout=0.0)
    _ffn.eval()
    _ffn_out = _ffn(_x)
    print("=== PositionwiseFFN ===")
    print(f"输入:  {tuple(_x.shape)}")
    print(f"输出:  {tuple(_ffn_out.shape)}  ← 形状不变!")
    print(f"中间层: {_d_model} → {_d_ff} → {_d_model}  (扩大{_d_ff//_d_model}倍再缩回)")
    print(f"参数: W1={tuple(_ffn.w1.weight.shape)}, W2={tuple(_ffn.w2.weight.shape)}")
    print(f"输入均值={_x.mean():.3f}, 输出均值={_ffn_out.mean():.3f}")
    print()

    _an = AddNorm(_d_model, dropout=0.0)
    _an.eval()
    _sublayer_out = torch.randn(2, 5, _d_model) * 0.5
    _norm_out = _an(_x, _sublayer_out)
    print("=== AddNorm (残差连接 + 层归一化) ===")
    print(f"x:            {tuple(_x.shape)}  均值={_x.mean():.3f} 标准差={_x.std():.3f}")
    print(f"sublayer_out: {tuple(_sublayer_out.shape)}  均值={_sublayer_out.mean():.3f}")
    print(f"x + sublayer: 均值={(_x + _sublayer_out).mean():.3f} 标准差={(_x + _sublayer_out).std():.3f}")
    print(f"LayerNorm后:  均值={_norm_out.mean():.4f} 标准差={_norm_out.std():.3f}  ← 归一化了!")
    print()
    print("流程: output = LayerNorm(x + Sublayer(x))")
    print("  x 直接跳过去 (残差) → 梯度不会消失")
    print("  LayerNorm → 稳定分布，加速训练")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 6 步: Encoder Layer

        两个子层: **Self-Attention** + **FFN**，每个外套 Add&Norm。
        输入输出形状相同 `(batch, seq, d)` → 可以任意堆叠。

        ## 第 7 步: Decoder Layer

        三个子层:

        1. **Masked Self-Attention** — 不能偷看未来，通过 mask 将未来位置的 Attention 权重置为 0，使每个位置只能依赖当前及之前的信息。（不是"Q 不能查询 后续 K/V"，而是 "查了但权重被清零"。）
        2. **Cross-Attention** — Q=来自解码器（来自德语）, K/V=来自编码器（来自英文）
        3. **FFN**
        """
    )
    return


@app.cell
def __(AddNorm, MultiHeadAttention, PositionwiseFFN, nn):
    class EncoderLayer(nn.Module):
        def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
            super().__init__()
            self.self_attn = MultiHeadAttention(d_model, num_heads, dropout)
            self.ffn = PositionwiseFFN(d_model, d_ff, dropout)
            self.norm1 = AddNorm(d_model, dropout)
            self.norm2 = AddNorm(d_model, dropout)

        def forward(self, x, src_mask=None):
            attn_out, _ = self.self_attn(x, x, x, src_mask)
            x = self.norm1(x, attn_out)
            x = self.norm2(x, self.ffn(x))
            return x

    class DecoderLayer(nn.Module):
        def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
            super().__init__()
            self.masked_self_attn = MultiHeadAttention(d_model, num_heads, dropout)
            self.cross_attn = MultiHeadAttention(d_model, num_heads, dropout)
            self.ffn = PositionwiseFFN(d_model, d_ff, dropout)
            self.norm1 = AddNorm(d_model, dropout)
            self.norm2 = AddNorm(d_model, dropout)
            self.norm3 = AddNorm(d_model, dropout)

        def forward(self, x, enc_output, src_mask=None, tgt_mask=None):
            attn_out, _ = self.masked_self_attn(x, x, x, tgt_mask)
            x = self.norm1(x, attn_out)
            attn_out, _ = self.cross_attn(x, enc_output, enc_output, src_mask)
            x = self.norm2(x, attn_out)
            x = self.norm3(x, self.ffn(x))
            return x
    return DecoderLayer, EncoderLayer


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 8 步: 完整 Transformer

        - **编码器** = 词嵌入 × $\sqrt{d}$ + 位置编码 + N × EncoderLayer
        - **解码器** = 词嵌入 × $\sqrt{d}$ + 位置编码 + N × DecoderLayer + 线性输出层
        """
    )
    return


@app.cell
def __(DecoderLayer, EncoderLayer, PositionalEncoding, math, nn):
    class Transformer(nn.Module):
        def __init__(self, src_vocab, tgt_vocab, d_model=512,
                     num_heads=8, num_layers=6, d_ff=2048,
                     dropout=0.1, max_len=5000):
            super().__init__()
            self.d_model = d_model # 单个词的维度，也叫模型宽度
            self.src_emb = nn.Embedding(src_vocab, d_model) # 源句子词表
            self.tgt_emb = nn.Embedding(tgt_vocab, d_model)
            self.src_pos = PositionalEncoding(d_model, max_len, dropout)
            self.tgt_pos = PositionalEncoding(d_model, max_len, dropout)
            self.enc_layers = nn.ModuleList([
                EncoderLayer(d_model, num_heads, d_ff, dropout)
                for _ in range(num_layers)])
            self.dec_layers = nn.ModuleList([
                DecoderLayer(d_model, num_heads, d_ff, dropout)
                for _ in range(num_layers)])
            self.out_proj = nn.Linear(d_model, tgt_vocab)

        def encode(self, src, mask):
            x = self.src_pos(self.src_emb(src) * math.sqrt(self.d_model))
            for layer in self.enc_layers:
                x = layer(x, mask)
            return x

        def decode(self, tgt, enc_out, src_mask, tgt_mask):
            x = self.tgt_pos(self.tgt_emb(tgt) * math.sqrt(self.d_model))
            for layer in self.dec_layers:
                x = layer(x, enc_out, src_mask, tgt_mask)
            return x

        def forward(self, src, tgt, src_mask=None, tgt_mask=None):
            enc_out = self.encode(src, src_mask)
            dec_out = self.decode(tgt, enc_out, src_mask, tgt_mask)
            return self.out_proj(dec_out)
    return (Transformer,)


@app.cell
def __(torch):
    def make_pad_mask(seq, pad_idx=0):
        return (seq != pad_idx).unsqueeze(1).unsqueeze(2)

    def make_causal_mask(size):
        return torch.tril(torch.ones(size, size)).unsqueeze(0).unsqueeze(0)
    return make_causal_mask, make_pad_mask


@app.cell
def __(mo):
    mo.md(r"""## 第 9 步: 前向传播 Demo""")
    return


@app.cell
def __(Transformer, make_causal_mask, make_pad_mask, torch):
    SRC_V, TGT_V = 100, 80
    D, H, L, FF = 64, 4, 2, 256

    _src = torch.randint(1, SRC_V, (2, 5))
    _tgt = torch.randint(1, TGT_V, (2, 4))
    _src_mask = make_pad_mask(_src)
    _tgt_mask = make_causal_mask(4)

    _model = Transformer(SRC_V, TGT_V, D, H, L, FF)
    _model.eval()
    _params = sum(p.numel() for p in _model.parameters())

    with torch.no_grad():
        _output = _model(_src, _tgt, _src_mask, _tgt_mask)

    _pred = _output.argmax(dim=-1)

    print("=" * 55)
    print("Transformer 前向传播 Demo")
    print("=" * 55)
    print(f"超参: d={D}, heads={H}, layers={L}, d_ff={FF}")
    print(f"参数量: {_params:,}")
    print(f"\nsrc tokens: {_src.tolist()}")
    print(f"tgt tokens: {_tgt.tolist()}")
    print(f"\n因果掩码 (下三角=可看, 上三角=禁看):")
    for _i, _row in enumerate(_tgt_mask.squeeze()):
        print(f"  位置{_i}: [{' '.join(str(int(v)) for v in _row)}]")
    print(f"\n输出形状: {tuple(_output.shape)} (batch, tgt_len, tgt_vocab)")
    print(f"预测 IDs: {_pred.tolist()} (未训练，是随机的)")
    print(f"\n数据流:")
    print(f"  编码器: {tuple(_src.shape)} → 嵌入 (2,5,{D}) → ×{L}层 → (2,5,{D})")
    print(f"     ↓ 作为 K,V")
    print(f"  解码器: {tuple(_tgt.shape)} → 嵌入 (2,4,{D}) → ×{L}层 → (2,4,{D})")
    print(f"     ↓ 线性投影")
    print(f"  输出:   {tuple(_output.shape)} → softmax → argmax → 预测词")
    print(f"\n✅ 完成!")
    return D, FF, H, L, SRC_V, TGT_V


if __name__ == "__main__":
    app.run()
