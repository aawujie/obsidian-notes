import marimo

__generated_with = "0.8.22"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo          # 交互式笔记本库
    import math                   # 数学函数
    import torch                  # PyTorch 深度学习框架
    import torch.nn as nn         # 神经网络模块
    import torch.nn.functional as F  # 函数式 API
    from torch.utils.data import Dataset, DataLoader  # 数据加载工具
    return DataLoader, Dataset, F, math, mo, nn, torch


@app.cell
def __(mo):
    mo.md(
        r"""
        # Transformer 训练篇 —— 从零训练一个翻译模型

        承接 [[transformer_tutorial_marimo]]，这篇讲如何训练 Transformer。

        | 步骤 | 内容 | 核心问题 |
        |---|---|---|
        | 1 | 数据准备 | 如何构造 src/tgt 对？ |
        | 2 | 损失函数 | 交叉熵 + Label Smoothing |
        | 3 | 优化器 | Adam + 学习率调度 |
        | 4 | 训练循环 | 前向 → 损失 → 反向 → 更新 |
        | 5 | 验证 & 保存 | 早停、模型选择 |
        | 6 | 简单 Demo | 训练一个英→法翻译模型 |

        **前置知识**: 理解 Transformer 架构（[[transformer_tutorial_marimo]]）
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 1 步: 数据准备

        翻译任务的输入是 **(源语言, 目标语言)** 句子对。

        关键处理:

        - **Tokenization**: 句子 → 词 ID 序列
        - **Padding**: 批量填充到相同长度
        - **BOS/EOS**: 目标语言加开始/结束标记

        **示例**:

        ```
        src: "I am a student" → [2, 45, 12, 89, 3]
        tgt: "Je suis étudiant" → [1, 23, 56, 78, 4, 3]  (1=BOS, 4=étudiant, 3=EOS)
        ```

        训练时 **解码器输入是 tgt[:-1]**（去掉 EOS），
        **目标是 tgt[1:]**（去掉 BOS），这叫 **Teacher Forcing**。
        """
    )
    return


@app.cell
def __(Dataset, torch):
    class TranslationDataset(Dataset):                          # 自定义数据集类，继承 PyTorch Dataset
        """简单翻译数据集"""
        def __init__(self, pairs, src_vocab, tgt_vocab):
            self.pairs = pairs                                  # 保存句子对列表，如 [("I am", "Je suis"), ...]
            self.src_vocab = src_vocab                          # 源语言词汇表，词到ID的映射字典
            self.tgt_vocab = tgt_vocab                          # 目标语言词汇表，词到ID的映射字典

        def __len__(self):
            return len(self.pairs)                              # 返回句子对的数量

        def __getitem__(self, idx):                             # 获取单个样本，DataLoader会调用
            src, tgt = self.pairs[idx]                          # 取出第 idx 个句子对
            src_ids = [self.src_vocab.get(w, 0) for w in src.split()]  # 源句子分词后转ID列表，未知词用0
            tgt_ids = [self.tgt_vocab["<bos>"]] + \
                      [self.tgt_vocab.get(w, 0) for w in tgt.split()] + \
                      [self.tgt_vocab["<eos>"]]                  # 目标句子加BOS和EOS标记
            return torch.tensor(src_ids), torch.tensor(tgt_ids)  # 转成 PyTorch 张量返回


    def collate_fn(batch, pad_idx=0):                           # 批量数据整理函数，处理变长序列
        """批量填充"""
        srcs, tgts = zip(*batch)                                # 解压 batch，得到 src 列表和 tgt 列表
        max_src = max(len(s) for s in srcs)                     # 找最长源句子长度，用于填充
        max_tgt = max(len(t) for t in tgts)                     # 找最长目标句子长度，用于填充

        # 建了两个空表格，表格的大小是：行数 = 句子数量，列数 = 最长句子的长度
        # 创建源填充张量，初始值为 pad_idx
        src_padded = torch.full((len(srcs), max_src), pad_idx, dtype=torch.long)
        # 创建目标填充张量，初始值为 pad_idx
        tgt_padded = torch.full((len(tgts), max_tgt), pad_idx, dtype=torch.long)

        # s: 第 i 个源句子
        # t: 第 i 个目标句子
        # 剩下没覆盖的格子还是填充符 pad_idx
        for i, (s, t) in enumerate(zip(srcs, tgts)):
            src_padded[i, :len(s)] = s                          # 将源句子填充到对应位置
            tgt_padded[i, :len(t)] = t                          # 将目标句子填充到对应位置

        return src_padded, tgt_padded                           # 返回填充后的批次数据
    return TranslationDataset, collate_fn


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 2 步: 损失函数 —— 交叉熵 + Label Smoothing

        ### 标准交叉熵
        $$\text{CE} = -\log P_{\text{target}}$$

        ### Label Smoothing
        把 one-hot 变成"软"标签，防止模型太自信:
        $$Q'_i = \begin{cases} 1 - \epsilon & i = \text{target} \\ \epsilon / (V-1) & \text{otherwise} \end{cases}$$

        原论文 $\epsilon = 0.1$。
        """
    )
    return


@app.cell
def __(F, nn, torch):
    class LabelSmoothingCrossEntropy(nn.Module):                # 带标签平滑的交叉熵损失类，继承 nn.Module
        """带标签平滑的交叉熵损失"""
        def __init__(self, vocab_size, smoothing=0.1, pad_idx=0):
            super().__init__()
            self.smoothing = smoothing                          # 平滑系数 ε，默认 0.1
            self.confidence = 1.0 - smoothing                   # 给真实标签的概率 (1-ε)
            self.vocab_size = vocab_size                        # 词汇表大小，用于计算分布
            self.pad_idx = pad_idx                              # 填充符 ID，用于忽略填充位置

        def forward(self, pred, target):                        # 前向计算损失
            mask = (target != self.pad_idx)                     # 创建布尔掩码，标记非填充位置为 True
            pred = pred[mask]                                   # 根据掩码过滤预测值，去掉填充位置
            target = target[mask]                               # 根据掩码过滤目标值，去掉填充位置

            if len(target) == 0:                                # 如果全是填充（空批次）
                return torch.tensor(0.0, device=pred.device)    # 返回 0 损失，避免报错

            log_probs = F.log_softmax(pred, dim=-1)             # 计算 log softmax，数值更稳定

            with torch.no_grad():                               # 不计算梯度，节省内存
                # 初始化平滑分布，其他词均匀分配
                true_dist = torch.full_like(log_probs, self.smoothing / (self.vocab_size - 1))  
                true_dist.scatter_(1, target.unsqueeze(1), self.confidence)  # 给真实标签位置分配 (1-ε) 概率

            loss = F.kl_div(log_probs, true_dist, reduction='batchmean')  # KL 散度，等价于交叉熵（减去常数熵）
            return loss
    return (LabelSmoothingCrossEntropy,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 3 步: 优化器 —— Adam + 学习率调度

        ### Adam 参数
        - $\beta_1 = 0.9$, $\beta_2 = 0.98$, $\epsilon = 10^{-9}$

        ### 学习率调度
        $$\text{lr} = d_{\text{model}}^{-0.5} \cdot \min(\text{step}^{-0.5}, \text{step} \cdot \text{warmup}^{-1.5})$$

        - **Warmup**: 前 N 步线性增加
        - **衰减**: 按 $1/\sqrt{\text{step}}$ 衰减
        """
    )
    return


@app.cell
def __():
    class TransformerLRScheduler:                               # Transformer 学习率调度器类
        """Transformer 学习率调度器"""
        def __init__(self, optimizer, d_model, warmup_steps=4000):
            self.optimizer = optimizer                          # 保存优化器引用，用于更新学习率
            self.d_model = d_model                              # 模型维度 d_model，影响初始学习率
            self.warmup_steps = warmup_steps                    # Warmup 步数，默认 4000
            self.step_num = 0                                   # 当前训练步数，从 0 开始

        def step(self):                                         # 更新学习率，每个 batch 调用一次
            self.step_num += 1                                  # 步数加 1
            lr = self._get_lr()                                 # 计算当前步的学习率
            for param_group in self.optimizer.param_groups:     # 遍历优化器的参数组
                param_group['lr'] = lr                          # 更新该参数组的学习率
            return lr                                           # 返回当前学习率，可用于日志记录

        def _get_lr(self):                                      # 内部方法：计算学习率
            step = self.step_num                                # 获取当前步数
            d = self.d_model                                    # 获取模型维度
            lr = (d ** -0.5) * min(                             # d^(-0.5) 缩放因子
                step ** -0.5,                                   # Decay 项：按 1/sqrt(step) 衰减
                step * (self.warmup_steps ** -1.5)              # Warmup 项：线性上升
            )                                                   # 取 min 实现分段：小值生效
            return lr                                           # 返回计算好的学习率
    return (TransformerLRScheduler,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 4 步: 训练循环

        ```
        for epoch in range(num_epochs):
            for batch in dataloader:
                # 1. 前向传播
                output = model(src, tgt_input)

                # 2. 计算损失
                loss = criterion(output.view(-1, vocab_size), tgt_output.view(-1))

                # 3. 反向传播
                optimizer.zero_grad()
                loss.backward()

                # 4. 梯度裁剪 (防止爆炸)
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

                # 5. 更新参数
                optimizer.step()
                scheduler.step()
        ```
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 5 步: 验证 & 保存

        - **验证集**: 每个 epoch 后评估，监控过拟合
        - **早停 (Early Stopping)**: 验证损失不下降时停止
        - **模型保存**: 保存验证集上最好的模型
        - **Checkpoint**: 定期保存，防止训练中断
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 6 步: 完整训练 Demo

        下面是一个完整的训练流程演示。
        注意: 这里复用了 [[transformer_tutorial_marimo]] 中的 Transformer 架构。
        """
    )
    return


@app.cell
def __(F, math, nn, torch):
    # 重新定义核心组件 (从 transformer_tutorial_marimo 复制)

    def scaled_dot_product_attention(Q, K, V, mask=None):         # 缩放点积注意力函数
        d_k = Q.size(-1)                                        # 获取每个头的维度
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)  # QK^T / sqrt(d_k)
        if mask is not None:                                    # 如果提供了掩码
            scores = scores.masked_fill(mask == 0, float('-inf'))  # 掩码位置设为负无穷
        weights = F.softmax(scores, dim=-1)                     # Softmax 得到注意力权重
        output = torch.matmul(weights, V)                       # 权重乘 V 得到输出
        return output, weights                                  # 返回输出和权重


    class MultiHeadAttention(nn.Module):                        # 多头注意力类
        def __init__(self, d_model, num_heads, dropout=0.1):    # 初始化
            super().__init__()                                  # 父类初始化
            assert d_model % num_heads == 0                     # 确保 d_model 能被 num_heads 整除
            self.d_model = d_model                              # 模型维度
            self.num_heads = num_heads                          # 头数
            self.d_k = d_model // num_heads                     # 每个头的维度
            self.W_q = nn.Linear(d_model, d_model)              # Q 的线性投影
            self.W_k = nn.Linear(d_model, d_model)              # K 的线性投影
            self.W_v = nn.Linear(d_model, d_model)              # V 的线性投影
            self.W_o = nn.Linear(d_model, d_model)              # 输出线性投影
            self.dropout = nn.Dropout(dropout)                  # Dropout 正则化

        def forward(self, Q, K, V, mask=None):                  # 前向传播
            bs = Q.size(0)                                      # 获取 batch size
            Q = self.W_q(Q).view(bs, -1, self.num_heads, self.d_k).transpose(1, 2)  # (bs, heads, seq, d_k)
            K = self.W_k(K).view(bs, -1, self.num_heads, self.d_k).transpose(1, 2)  # (bs, heads, seq, d_k)
            V = self.W_v(V).view(bs, -1, self.num_heads, self.d_k).transpose(1, 2)  # (bs, heads, seq, d_k)
            out, w = scaled_dot_product_attention(Q, K, V, mask)  # 计算注意力
            out = self.dropout(out)                             # Dropout
            out = out.transpose(1, 2).contiguous().view(bs, -1, self.d_model)  # 拼接多头 (bs, seq, d_model)
            return self.W_o(out), w                             # 输出投影


    class PositionalEncoding(nn.Module):                        # 位置编码类
        def __init__(self, d_model, max_len=5000, dropout=0.1):  # 初始化
            super().__init__()                                  # 父类初始化
            self.dropout = nn.Dropout(dropout)                  # Dropout
            pe = torch.zeros(max_len, d_model)                  # 创建位置编码矩阵
            pos = torch.arange(0, max_len).unsqueeze(1).float()  # 位置索引 (max_len, 1)
            div = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))  # 频率项
            pe[:, 0::2] = torch.sin(pos * div)                  # 偶数维用 sin
            pe[:, 1::2] = torch.cos(pos * div)                  # 奇数维用 cos
            self.register_buffer('pe', pe.unsqueeze(0))         # 注册为 buffer，不更新

        def forward(self, x):                                   # 前向传播
            return self.dropout(x + self.pe[:, :x.size(1)])     # 加位置编码后 dropout


    class PositionwiseFFN(nn.Module):                           # 位置前馈网络类
        def __init__(self, d_model, d_ff, dropout=0.1):         # 初始化
            super().__init__()                                  # 父类初始化
            self.w1 = nn.Linear(d_model, d_ff)                  # 第一层线性 (d_model -> d_ff)
            self.w2 = nn.Linear(d_ff, d_model)                  # 第二层线性 (d_ff -> d_model)
            self.dropout = nn.Dropout(dropout)                  # Dropout

        def forward(self, x):                                   # 前向传播
            return self.w2(self.dropout(F.relu(self.w1(x))))    # Linear -> ReLU -> Dropout -> Linear


    class AddNorm(nn.Module):                                   # 残差连接 + LayerNorm 类
        def __init__(self, d_model, dropout=0.1):               # 初始化
            super().__init__()                                  # 父类初始化
            self.norm = nn.LayerNorm(d_model)                   # LayerNorm
            self.dropout = nn.Dropout(dropout)                  # Dropout

        def forward(self, x, sublayer_output):                  # 前向传播
            return self.norm(x + self.dropout(sublayer_output))  # x + Dropout(sublayer) 后 LayerNorm


    class EncoderLayer(nn.Module):                              # 编码器层类
        def __init__(self, d_model, num_heads, d_ff, dropout=0.1):  # 初始化
            super().__init__()                                  # 父类初始化
            self.self_attn = MultiHeadAttention(d_model, num_heads, dropout)  # 自注意力
            self.ffn = PositionwiseFFN(d_model, d_ff, dropout)  # 前馈网络
            self.norm1 = AddNorm(d_model, dropout)              # 第一个 AddNorm
            self.norm2 = AddNorm(d_model, dropout)              # 第二个 AddNorm

        def forward(self, x, src_mask=None):                    # 前向传播
            attn_out, _ = self.self_attn(x, x, x, src_mask)     # 自注意力
            x = self.norm1(x, attn_out)                         # 残差 + LayerNorm
            x = self.norm2(x, self.ffn(x))                      # FFN + 残差 + LayerNorm
            return x                                            # 返回输出


    class DecoderLayer(nn.Module):                              # 解码器层类
        def __init__(self, d_model, num_heads, d_ff, dropout=0.1):  # 初始化
            super().__init__()                                  # 父类初始化
            self.masked_self_attn = MultiHeadAttention(d_model, num_heads, dropout)  # 掩码自注意力
            self.cross_attn = MultiHeadAttention(d_model, num_heads, dropout)  # 交叉注意力
            self.ffn = PositionwiseFFN(d_model, d_ff, dropout)  # 前馈网络
            self.norm1 = AddNorm(d_model, dropout)              # 第一个 AddNorm
            self.norm2 = AddNorm(d_model, dropout)              # 第二个 AddNorm
            self.norm3 = AddNorm(d_model, dropout)              # 第三个 AddNorm

        def forward(self, x, enc_out, src_mask=None, tgt_mask=None):  # 前向传播
            attn_out, _ = self.masked_self_attn(x, x, x, tgt_mask)  # 掩码自注意力
            x = self.norm1(x, attn_out)                         # 残差 + LayerNorm
            attn_out, _ = self.cross_attn(x, enc_out, enc_out, src_mask)  # 交叉注意力
            x = self.norm2(x, attn_out)                         # 残差 + LayerNorm
            x = self.norm3(x, self.ffn(x))                      # FFN + 残差 + LayerNorm
            return x                                            # 返回输出


    class Transformer(nn.Module):                               # Transformer 完整模型类
        def __init__(self, src_vocab, tgt_vocab, d_model=512,   # 初始化
                     num_heads=8, num_layers=6, d_ff=2048,
                     dropout=0.1, max_len=5000):
            super().__init__()                                  # 父类初始化
            self.d_model = d_model                              # 模型维度
            self.src_emb = nn.Embedding(src_vocab, d_model)     # 源语言嵌入
            self.tgt_emb = nn.Embedding(tgt_vocab, d_model)     # 目标语言嵌入
            self.src_pos = PositionalEncoding(d_model, max_len, dropout)  # 源位置编码
            self.tgt_pos = PositionalEncoding(d_model, max_len, dropout)  # 目标位置编码
            self.enc_layers = nn.ModuleList([                   # 编码器层列表
                EncoderLayer(d_model, num_heads, d_ff, dropout)
                for _ in range(num_layers)])
            self.dec_layers = nn.ModuleList([                   # 解码器层列表
                DecoderLayer(d_model, num_heads, d_ff, dropout)
                for _ in range(num_layers)])
            self.out_proj = nn.Linear(d_model, tgt_vocab)       # 输出投影到词汇表

        def encode(self, src, mask):                            # 编码方法
            x = self.src_pos(self.src_emb(src) * math.sqrt(self.d_model))  # 嵌入 + 位置编码
            for layer in self.enc_layers:                       # 逐层编码
                x = layer(x, mask)                              # 通过编码器层
            return x                                            # 返回编码器输出

        def decode(self, tgt, enc_out, src_mask, tgt_mask):     # 解码方法
            x = self.tgt_pos(self.tgt_emb(tgt) * math.sqrt(self.d_model))  # 嵌入 + 位置编码
            for layer in self.dec_layers:                       # 逐层解码
                x = layer(x, enc_out, src_mask, tgt_mask)       # 通过解码器层
            return x                                            # 返回解码器输出

        def forward(self, src, tgt, src_mask=None, tgt_mask=None):  # 前向传播
            enc_out = self.encode(src, src_mask)                # 编码源句子
            dec_out = self.decode(tgt, enc_out, src_mask, tgt_mask)  # 解码目标句子
            return self.out_proj(dec_out)                       # 投影到词汇表大小
    return (
        AddNorm,
        DecoderLayer,
        EncoderLayer,
        MultiHeadAttention,
        PositionalEncoding,
        PositionwiseFFN,
        Transformer,
        scaled_dot_product_attention,
    )


@app.cell
def __(torch):
    def make_pad_mask(seq, pad_idx=0):                          # 创建填充掩码函数
        return (seq != pad_idx).unsqueeze(1).unsqueeze(2)       # (batch, 1, 1, seq_len)，标记非填充位置

    def make_causal_mask(size):                                 # 创建因果掩码函数（下三角）
        return torch.tril(torch.ones(size, size)).unsqueeze(0).unsqueeze(0)  # (1, 1, size, size)，下三角为1
    return make_causal_mask, make_pad_mask


@app.cell
def __(
    LabelSmoothingCrossEntropy,
    Transformer,
    TransformerLRScheduler,
    make_causal_mask,
    make_pad_mask,
    torch,
):
    # 完整训练 Demo

    # 源语言词汇表
    SRC_VOCAB = {"<pad>": 0, "<unk>": 1, "I": 2, "am": 3, "a": 4, "student": 5,
                 "teacher": 6, "like": 7, "apples": 8, "you": 9, "are": 10, "good": 11}

    # 目标语言词汇表
    TGT_VOCAB = {"<pad>": 0, "<unk>": 1, "<bos>": 2, "<eos>": 3,
                 "Je": 4, "suis": 5, "un": 6, "étudiant": 7, "professeur": 8,
                 "aime": 9, "pommes": 10, "Tu": 11, "es": 12, "bon": 13}

    # 训练数据：英→法句子对
    PAIRS = [
        ("I am a student", "Je suis un étudiant"),
        ("I am a teacher", "Je suis un professeur"),
        ("I like apples", "Je aime pommes"),
        ("you are good", "Tu es bon"),
        ("you are a student", "Tu es un étudiant"),
        ("I like you", "Je aime Tu"),
    ]

    # 模型超参数：d_model=64, heads=4, layers=2, d_ff=256
    D, H, L, FF = 64, 4, 2, 256

    # 创建模型
    model = Transformer(len(SRC_VOCAB), len(TGT_VOCAB), D, H, L, FF, dropout=0.1)

    criterion = LabelSmoothingCrossEntropy(len(TGT_VOCAB), smoothing=0.1)  # 损失函数，标签平滑 0.1
    optimizer = torch.optim.Adam(model.parameters(), lr=0, betas=(0.9, 0.98), eps=1e-9)  # Adam 优化器
    scheduler = TransformerLRScheduler(optimizer, D, warmup_steps=30)  # 学习率调度，Warmup 30步

    # ── 数据预处理：只需执行一次，不要放在训练循环里 ──
    src_ids = [[SRC_VOCAB.get(w, 0) for w in s.split()] for s, _ in PAIRS]  # 源句子转 ID
    tgt_ids = [[TGT_VOCAB["<bos>"]] + [TGT_VOCAB.get(w, 0) for w in t.split()] + [TGT_VOCAB["<eos>"]]
               for _, t in PAIRS]                           # 目标句子加 BOS/EOS

    max_src = max(len(s) for s in src_ids)                  # 最长源句子
    max_tgt = max(len(t) for t in tgt_ids)                  # 最长目标句子
    src_batch = torch.full((len(src_ids), max_src), 0, dtype=torch.long)  # 源填充张量
    tgt_batch = torch.full((len(tgt_ids), max_tgt), 0, dtype=torch.long)  # 目标填充张量

    for i, (s, t) in enumerate(zip(src_ids, tgt_ids)):      # 填充数据
        src_batch[i, :len(s)] = torch.tensor(s)             # 填充源
        tgt_batch[i, :len(t)] = torch.tensor(t)             # 填充目标

    tgt_input = tgt_batch[:, :-1]                           # Teacher Forcing：输入去掉最后一个（EOS）
    tgt_output = tgt_batch[:, 1:]                           # 目标去掉第一个（BOS）

    src_mask = make_pad_mask(src_batch)                     # 源填充掩码（固定不变）
    tgt_mask = make_causal_mask(tgt_input.size(1))          # 目标因果掩码（固定不变）

    model.train()                                               # 设置训练模式
    num_epochs = 100                                            # 训练 100 个 epoch

    for epoch in range(num_epochs):                             # 遍历每个 epoch
        output = model(src_batch, tgt_input, src_mask, tgt_mask)  # 前向传播

        loss = criterion(output.reshape(-1, len(TGT_VOCAB)), tgt_output.reshape(-1))  # 计算损失

        optimizer.zero_grad()                                   # 清零梯度
        loss.backward()                                         # 反向传播
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0) # 梯度裁剪，防止爆炸
        optimizer.step()                                        # 更新参数
        scheduler.step()                                        # 更新学习率

        if (epoch + 1) % 20 == 0:                               # 每 20 个 epoch 打印
            print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item():.4f}, LR: {scheduler._get_lr():.6f}")

    print("\n=== 训练完成 ===")                                 # 训练结束
    print(f"最终损失: {loss.item():.4f}")                       # 打印最终损失
    return (
        D,
        FF,
        H,
        L,
        PAIRS,
        SRC_VOCAB,
        TGT_VOCAB,
        criterion,
        epoch,
        i,
        loss,
        max_src,
        max_tgt,
        model,
        num_epochs,
        optimizer,
        output,
        s,
        scheduler,
        src_batch,
        src_ids,
        src_mask,
        t,
        tgt_batch,
        tgt_ids,
        tgt_input,
        tgt_mask,
        tgt_output,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 总结

        这篇教程覆盖了 Transformer 训练的完整流程:

        1. **数据准备**: Dataset + DataLoader + Collate + Padding
        2. **损失函数**: Label Smoothing Cross Entropy
        3. **优化器**: Adam + Transformer LR Scheduler (Warmup + Decay)
        4. **训练循环**: Forward → Loss → Backward → Clip → Step
        5. **Teacher Forcing**: 训练时解码器输入用真实标签

        **下一步**: [[transformer_inference_marimo]] —— 推理篇：KV Cache、贪心解码、Beam Search
        """
    )
    return


if __name__ == "__main__":
    app.run()
