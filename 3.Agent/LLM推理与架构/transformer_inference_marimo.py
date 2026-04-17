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
        # Transformer 推理篇 —— 解码策略与加速

        承接 [[transformer_training_marimo]]，这篇讲如何用训练好的模型做推理。

        | 步骤 | 内容 | 核心问题 |
        |---|---|---|
        | 1 | 自回归解码 | 推理和训练有何不同？ |
        | 2 | 贪心解码 | 每步取最高概率 |
        | 3 | Beam Search | 保留 top-k 条路径 |
        | 4 | 采样解码 | 温度、Top-k、Top-p |
        | 5 | KV Cache | 避免重复计算，加速推理 |
        | 6 | Demo | 对比各种解码策略 |

        **前置知识**: [[transformer_tutorial_marimo]] + [[transformer_training_marimo]]
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 1 步: 自回归解码 —— 推理和训练的区别

        ### 训练时（Teacher Forcing）
        ```
        输入 tgt: [<bos>, 我, 爱, 你]   ← 一次性全部输入，并行计算
        目标 tgt: [我, 爱, 你, <eos>]
        ```

        ### 推理时（自回归）
        ```
        step 1: 输入 [<bos>]          → 输出 [我]
        step 2: 输入 [<bos>, 我]       → 输出 [爱]
        step 3: 输入 [<bos>, 我, 爱]   → 输出 [你]
        step 4: 输入 [<bos>, 我, 爱, 你] → 输出 [<eos>]  ← 终止
        ```

        **关键区别：**

        - 训练：已知完整目标序列，并行计算
        - 推理：逐步生成，每步依赖上一步的输出，**串行**
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 2 步: 贪心解码（Greedy Decoding）

        最简单的解码策略：**每步取概率最高的词**

        ```
        输出概率: [0.01, 0.05, 0.60, 0.30, 0.04]
                                 ↑
                              取这个！（argmax）
        ```

        - **优点**：快，简单
        - **缺点**：容易陷入次优解（局部最优 ≠ 全局最优）

        ```
        例子：
          贪心选了 "我" (0.6)，但后续只能生成 "我 吃 饭"
          如果选了 "他" (0.3)，后续可以生成 "他 很 好 呀"（整体更通顺）

        贪心看不到未来，可能选了一个"坑"
        ```
        """
    )
    return


@app.cell
def __(math, nn, torch):
    class Transformer(nn.Module):
        """简化版 Transformer，复用自架构篇"""
        def __init__(self, src_vocab, tgt_vocab, d_model=64, nhead=4, num_layers=2, d_ff=256, dropout=0.1):
            super().__init__()
            self.src_embed = nn.Embedding(src_vocab, d_model, padding_idx=0)   # 源语言词嵌入
            self.tgt_embed = nn.Embedding(tgt_vocab, d_model, padding_idx=0)   # 目标语言词嵌入
            self.pos_enc = PositionalEncoding(d_model, dropout=dropout)          # 位置编码
            encoder_layer = nn.TransformerEncoderLayer(d_model, nhead, d_ff, dropout, batch_first=True)
            decoder_layer = nn.TransformerDecoderLayer(d_model, nhead, d_ff, dropout, batch_first=True)
            self.encoder = nn.TransformerEncoder(encoder_layer, num_layers)     # 编码器
            self.decoder = nn.TransformerDecoder(decoder_layer, num_layers)     # 解码器
            self.fc_out = nn.Linear(d_model, tgt_vocab)                         # 输出投影层
            self.d_model = d_model

        def encode(self, src, src_key_padding_mask=None):
            """只跑编码器，推理时只需编码一次"""
            x = self.pos_enc(self.src_embed(src) * math.sqrt(self.d_model))    # 词嵌入 + 位置编码
            return self.encoder(x, src_key_padding_mask=src_key_padding_mask)  # 返回 memory

        def decode_step(self, tgt, memory, tgt_mask=None, memory_key_padding_mask=None):
            """跑解码器一步"""
            x = self.pos_enc(self.tgt_embed(tgt) * math.sqrt(self.d_model))    # 目标词嵌入 + 位置编码
            out = self.decoder(x, memory, tgt_mask=tgt_mask,                   # 解码器前向
                               memory_key_padding_mask=memory_key_padding_mask)
            return self.fc_out(out)                                            # 返回 logits

        def forward(self, src, tgt):
            tgt_len = tgt.size(1)
            # causal mask
            tgt_mask = nn.Transformer.generate_square_subsequent_mask(tgt_len, device=src.device)  

            memory = self.encode(src)
            return self.decode_step(tgt, memory, tgt_mask=tgt_mask)


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
    return PositionalEncoding, Transformer


@app.cell
def __(mo):
    mo.md(r"""### 贪心解码实现""")
    return


@app.cell
def __(torch):
    def greedy_decode(model, src, max_len, bos_idx, eos_idx, device):
        """
        贪心解码：每步取 argmax
        src: (1, src_len) 源序列
        """
        model.eval()
        with torch.no_grad():
            # 1. 编码源序列（只做一次）
            memory = model.encode(src.to(device))                       # (1, src_len, d_model)

            # 2. 初始化：解码器输入从 <bos> 开始
            tgt = torch.tensor([[bos_idx]], device=device)              # (1, 1)

            for _ in range(max_len):
                tgt_len = tgt.size(1)
                tgt_mask = torch.nn.Transformer.generate_square_subsequent_mask(
                    tgt_len, device=device)                             # causal mask

                # 3. 解码一步
                logits = model.decode_step(tgt, memory, tgt_mask=tgt_mask)  # (1, tgt_len, vocab)
                next_logit = logits[:, -1, :]                           # 只取最后一个位置 (1, vocab)

                # 4. 贪心：取概率最高的词
                next_token = next_logit.argmax(dim=-1, keepdim=True)    # (1, 1)

                # 5. 拼接到已生成序列
                tgt = torch.cat([tgt, next_token], dim=1)               # (1, tgt_len+1)

                # 6. 遇到 <eos> 终止
                if next_token.item() == eos_idx:
                    break

        return tgt[0].tolist()  # 返回生成的 token id 列表
    return (greedy_decode,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 3 步: Beam Search —— 保留 top-k 条路径

        贪心解码每步只保留 1 条路径，Beam Search 保留 **beam_size** 条。

        ### 直观理解（beam_size=2）

        ```
        step 1: 候选词 [我(0.6), 他(0.3), 你(0.1)]
                保留 top-2: [我(0.6), 他(0.3)]

        step 2: 从"我"扩展 → [我爱(0.5), 我吃(0.1)]
                从"他"扩展 → [他很(0.25), 他去(0.05)]
                所有候选: [我爱(0.6×0.5=0.30), 他很(0.3×0.25=0.075), 我吃(0.06), 他去(0.015)]
                保留 top-2: [我爱(0.30), 他很(0.075)]

        step 3: 继续扩展...直到生成 <eos>

        最终选得分最高的完整路径
        ```

        - **优点**：比贪心找到更好的翻译
        - **缺点**：计算量是贪心的 beam_size 倍
        """
    )
    return


@app.cell
def __(torch):
    def beam_search(model, src, max_len, bos_idx, eos_idx, device, beam_size=3):
        """
        Beam Search 解码
        src: (1, src_len)
        beam_size: 保留的候选数量
        """
        model.eval()
        with torch.no_grad():
            # 1. 编码源序列（只做一次）
            memory = model.encode(src.to(device))                           # (1, src_len, d_model)

            # 2. 初始化 beam：每个 beam 是 (累计log概率, token序列)
            beams = [(0.0, [bos_idx])]                                      # 初始 beam，只有 <bos>
            completed = []                                                  # 已完成的序列

            for _ in range(max_len):
                candidates = []                                             # 本步所有候选

                for score, tokens in beams:
                    if tokens[-1] == eos_idx:                               # 已经结束的 beam 直接保留
                        completed.append((score, tokens))
                        continue

                    # 3. 解码当前 beam
                    tgt = torch.tensor([tokens], device=device)             # (1, cur_len)
                    tgt_len = tgt.size(1)
                    tgt_mask = torch.nn.Transformer.generate_square_subsequent_mask(
                        tgt_len, device=device)
                    logits = model.decode_step(tgt, memory, tgt_mask=tgt_mask)  # (1, cur_len, vocab)
                    log_probs = torch.log_softmax(logits[:, -1, :], dim=-1)     # (1, vocab)

                    # 4. 取 top beam_size 个词
                    topk_log_probs, topk_ids = log_probs[0].topk(beam_size)     # (beam_size,)

                    for log_p, token_id in zip(topk_log_probs.tolist(), topk_ids.tolist()):
                        candidates.append((score + log_p, tokens + [token_id])) # 累加 log 概率

                if not candidates:
                    break

                # 5. 保留得分最高的 beam_size 条路径
                candidates.sort(key=lambda x: x[0], reverse=True)
                beams = candidates[:beam_size]                              # 保留 top beam_size

            # 6. 合并已完成和未完成的，取得分最高的
            completed += beams
            completed.sort(key=lambda x: x[0] / len(x[1]), reverse=True)  # 用长度归一化得分
            return completed[0][1]                                        # 返回得分最高的序列
    return (beam_search,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 4 步: 采样解码 —— 增加多样性

        贪心和 Beam Search 每次生成相同结果。采样策略引入随机性，适合**创意生成**。

        ### 1. **温度采样**（Temperature）

        $$P'_i = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)}$$

        ```
        T=1.0（默认）：原始分布
        T<1.0（如0.5）：分布更尖锐，更保守（接近贪心）
        T>1.0（如2.0）：分布更平坦，更随机（更有创意）
        ```

        ### 2. **Top-k 采样**

        **只从概率最高的 k 个词中采样，避免选到奇怪的低概率词**

        ### 3. **Top-p 采样**（核采样 Nucleus Sampling）

        - **只从累计概率达到 p 的词中采样**
        - **自适应：高置信时候选少，低置信时候选多**
        """
    )
    return


@app.cell
def __(F, torch):
    def sample_decode(model, src, max_len, bos_idx, eos_idx, device,
                      temperature=1.0, top_k=0, top_p=0.9):
        """
        采样解码：支持温度、Top-k、Top-p
        temperature: 温度，<1 更保守，>1 更随机
        top_k: 只从 top-k 个词采样，0 表示不限制
        top_p: 累计概率阈值（核采样）
        """
        model.eval()
        with torch.no_grad():
            memory = model.encode(src.to(device))                           # 编码源序列
            tgt = torch.tensor([[bos_idx]], device=device)                  # 初始化 <bos>

            for _ in range(max_len):
                tgt_len = tgt.size(1)
                tgt_mask = torch.nn.Transformer.generate_square_subsequent_mask(
                    tgt_len, device=device)
                logits = model.decode_step(tgt, memory, tgt_mask=tgt_mask)
                next_logit = logits[:, -1, :] / temperature                 # 除以温度，调整分布

                # Top-k 过滤：只保留 top-k 个词
                if top_k > 0:
                    topk_vals = next_logit.topk(top_k).values[:, -1:]      # 第 k 大的值
                    next_logit = next_logit.masked_fill(next_logit < topk_vals, float('-inf'))

                # Top-p 过滤：保留累计概率达到 p 的词
                if top_p > 0:
                    sorted_logits, sorted_idx = next_logit.sort(descending=True)
                    cum_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)
                    remove_mask = cum_probs - F.softmax(sorted_logits, dim=-1) > top_p
                    sorted_logits[remove_mask] = float('-inf')
                    next_logit = torch.zeros_like(next_logit).scatter_(1, sorted_idx, sorted_logits)

                # 按概率采样
                probs = torch.softmax(next_logit, dim=-1)                   # 转概率分布
                next_token = torch.multinomial(probs, num_samples=1)        # 采样一个词

                tgt = torch.cat([tgt, next_token], dim=1)
                if next_token.item() == eos_idx:
                    break

        return tgt[0].tolist()
    return (sample_decode,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 5 步: KV Cache —— 推理加速

        ### 没有 KV Cache 时

        ```
        step 1: 输入 [<bos>]              → 计算 K,V for [<bos>]
        step 2: 输入 [<bos>, 我]          → 重新计算 K,V for [<bos>, 我]  ← 重复计算！
        step 3: 输入 [<bos>, 我, 爱]      → 重新计算 K,V for [<bos>, 我, 爱]  ← 重复计算！
        ```

        ### 有 KV Cache 时

        ```
        step 1: 计算 K₁,V₁ for <bos>     → 缓存 {0: (K₁,V₁)}
        step 2: 只算 K₂,V₂ for 我         → 缓存 {0: (K₁,V₁), 1: (K₂,V₂)}
                Attention 用缓存的所有 K,V
        step 3: 只算 K₃,V₃ for 爱         → 缓存 {..., 2: (K₃,V₃)}
        ```

        **节省计算量**：从 O(n²) 降到 O(n)，序列越长加速越明显

        **代价**：需要额外内存存储 KV Cache
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ### KV Cache 原理图

        ```
        没有 KV Cache（step 3）:
        ┌──────────────────────────────────┐
        │  输入: [<bos>, 我, 爱]            │
        │  Q = W_q × [bos, 我, 爱]         │  ← 全部重算
        │  K = W_k × [bos, 我, 爱]         │  ← 全部重算
        │  V = W_v × [bos, 我, 爱]         │  ← 全部重算
        │  Attention(Q, K, V)              │
        └──────────────────────────────────┘

        有 KV Cache（step 3）:
        ┌──────────────────────────────────┐
        │  输入（只有新词）: [爱]            │
        │  Q = W_q × [爱]                  │  ← 只算新词
        │  K_new = W_k × [爱]              │  ← 只算新词
        │  V_new = W_v × [爱]              │  ← 只算新词
        │  K = concat(K_cache, K_new)      │  ← 从缓存取历史
        │  V = concat(V_cache, V_new)      │  ← 从缓存取历史
        │  Attention(Q, K, V)              │
        └──────────────────────────────────┘
        ```
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 6 步: Demo —— 对比各种解码策略

        用一个玩具英→法翻译任务，对比贪心 vs Beam Search vs 采样。
        """
    )
    return


@app.cell
def __(Transformer, torch):
    # ── 词汇表定义（与训练篇一致）──
    SRC_VOCAB = {"<pad>":0,"<unk>":1,"<bos>":2,"<eos>":3,
                 "I":4,"love":5,"you":6,"we":7,"are":8,"happy":9,"today":10,"hello":11}
    TGT_VOCAB = {"<pad>":0,"<unk>":1,"<bos>":2,"<eos>":3,
                 "Je":4,"t'aime":5,"nous":6,"sommes":7,"heureux":8,
                 "aujourd'hui":9,"bonjour":10,"vous":11,"aime":12,"monde":13}
    TGT_IDX2WORD = {v: k for k, v in TGT_VOCAB.items()}    # id → 词，用于解码输出

    PAD_IDX, BOS_IDX, EOS_IDX = 0, 2, 3
    device = torch.device("cpu")

    # ── 构建模型（超参数与训练篇一致）──
    infer_model = Transformer(
        src_vocab=len(SRC_VOCAB), tgt_vocab=len(TGT_VOCAB),
        d_model=64, nhead=4, num_layers=2, d_ff=256
    ).to(device)

    # ── 简单训练几步让模型有点意义 ──
    import torch.optim as optim
    pairs = [
        ("I love you", "Je t'aime"),
        ("we are happy", "nous sommes heureux"),
        ("hello you", "bonjour vous"),
        ("I love you today", "Je t'aime aujourd'hui"),
        ("we are happy today", "nous sommes heureux aujourd'hui"),
        ("hello world", "bonjour monde"),
    ]
    optimizer = optim.Adam(infer_model.parameters(), lr=1e-3)
    infer_model.train()

    for _ep in range(200):
        total_loss = 0
        for _src_str, _tgt_str in pairs:
            _src_ids = [SRC_VOCAB.get(w, 1) for w in _src_str.split()]
            _tgt_ids = [BOS_IDX] + [TGT_VOCAB.get(w, 1) for w in _tgt_str.split()] + [EOS_IDX]
            _src_t = torch.tensor([_src_ids], device=device)
            _tgt_t = torch.tensor([_tgt_ids], device=device)
            logits = infer_model(_src_t, _tgt_t[:, :-1])                 # teacher forcing
            loss = torch.nn.functional.cross_entropy(
                logits.reshape(-1, len(TGT_VOCAB)), _tgt_t[:, 1:].reshape(-1), ignore_index=PAD_IDX)
            optimizer.zero_grad(); loss.backward(); optimizer.step()
            total_loss += loss.item()
        if (_ep+1) % 50 == 0:
            # 所有样本的平均 loss
            print(f"epoch {_ep+1:3d}  loss={total_loss/len(pairs):.4f}")

    infer_model.eval()
    print("训练完成！")
    return (
        BOS_IDX,
        EOS_IDX,
        PAD_IDX,
        SRC_VOCAB,
        TGT_IDX2WORD,
        TGT_VOCAB,
        device,
        infer_model,
        logits,
        loss,
        optim,
        optimizer,
        pairs,
        total_loss,
    )


@app.cell
def __(
    BOS_IDX,
    EOS_IDX,
    SRC_VOCAB,
    TGT_IDX2WORD,
    beam_search,
    device,
    greedy_decode,
    infer_model,
    sample_decode,
    torch,
):
    def ids_to_str(ids):
        """将 token id 列表转回字符串"""
        words = [TGT_IDX2WORD.get(i, "<unk>") for i in ids]
        words = [w for w in words if w not in ("<bos>", "<eos>", "<pad>")]
        return " ".join(words)

    # 测试句子
    test_sentences = ["I love you", "we are happy today", "hello you"]

    print("=" * 55)
    print(f"{'输入':<20} {'策略':<15} {'输出'}")
    print("=" * 55)

    for sent in test_sentences:
        _src_ids = [SRC_VOCAB.get(w, 1) for w in sent.split()]
        _src_t = torch.tensor([_src_ids], device=device)

        # 贪心解码
        greedy_out = greedy_decode(infer_model, _src_t, 20, BOS_IDX, EOS_IDX, device)
        print(f"{sent:<20} {'贪心':<15} {ids_to_str(greedy_out)}")

        # Beam Search（beam=3）
        beam_out = beam_search(infer_model, _src_t, 20, BOS_IDX, EOS_IDX, device, beam_size=3)
        print(f"{'':20} {'Beam(k=3)':<15} {ids_to_str(beam_out)}")

        # 温度采样
        sample_out = sample_decode(infer_model, _src_t, 20, BOS_IDX, EOS_IDX, device,
                                   temperature=0.8, top_k=5, top_p=0.9)
        print(f"{'':20} {'采样(T=0.8)':<15} {ids_to_str(sample_out)}")
        print("-" * 55)
    return (
        beam_out,
        greedy_out,
        ids_to_str,
        sample_out,
        sent,
        test_sentences,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 总结：三种解码策略对比

        | 策略 | 原理 | 优点 | 缺点 | 适用场景 |
        |------|------|------|------|---------|
        | **贪心** | 每步取 argmax | 快，简单 | 容易次优 | 实时推理 |
        | **Beam Search** | 保留 top-k 路径 | 质量更好 | 慢 k 倍 | 翻译、摘要 |
        | **采样** | 按概率采样 | 多样，有创意 | 不稳定 | 对话、创作 |

        ## KV Cache 总结

        | 对比 | 无 KV Cache | 有 KV Cache |
        |------|------------|------------|
        | 每步计算量 | O(n²) | O(n) |
        | 内存占用 | 小 | 需存所有 K,V |
        | 适用场景 | 训练 | 推理加速 |

        ## 推理完整流程

        ```
        1. 编码源序列 → memory（只做一次）
        2. 初始化 tgt = [<bos>]
        3. 循环：
           a. decode_step(tgt, memory) → logits
           b. 用解码策略选下一个词（贪心/Beam/采样）
           c. 拼接到 tgt
           d. 如果是 <eos> 或达到最大长度，终止
        4. 将 token id 转回文字
        ```

        ---

        **相关笔记**: [[transformer_tutorial_marimo]] | [[transformer_training_marimo]]
        """
    )
    return


if __name__ == "__main__":
    app.run()
