import marimo

__generated_with = "0.8.22"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell
def __():
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    from torch.utils.data import DataLoader, Dataset
    import torch
    import torch.nn as nn
    return (
        AutoModelForSequenceClassification,
        AutoTokenizer,
        DataLoader,
        Dataset,
        nn,
        torch,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        # Hugging Face 入门 —— 站在巨人肩膀上

        学完 Transformer 原理后，实战中几乎不会从头写模型。

        **Hugging Face** 提供了数千个预训练模型，几行代码就能用上。

        | 模块 | 作用 |
        |------|------|
        | `transformers` | 预训练模型（BERT、GPT、T5 等）|
        | `datasets` | 数据集加载 |
        | `tokenizers` | 分词器 |
        | `pipeline` | 一行代码完成常见任务 |

        **核心思路：**
        ```
        预训练模型（通用知识）+ 你的数据（具体任务）= Fine-tuned 模型
        ```
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 1 步: Pipeline —— 最快上手方式

        `pipeline` 封装了完整推理流程：分词 → 模型 → 解码输出

        ### 支持的任务
        ```python
        "text-classification"     # 文本分类（情感分析）
        "token-classification"    # 序列标注（NER 命名实体识别）
        "question-answering"      # 问答
        "summarization"           # 文本摘要
        "translation"             # 翻译
        "text-generation"         # 文本生成
        "fill-mask"               # 掩码填充（完形填空）
        "zero-shot-classification" # 零样本分类
        ```
        """
    )
    return


@app.cell
def __():
    from transformers import pipeline

    # ── 情感分析（指定模型 + GPU）──
    classifier = pipeline(
        "sentiment-analysis",
        model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
        device=0  # 0 = 第一块 GPU (RTX 3090)，CPU 用 -1
    )
    result = classifier("I love this movie!")
    # [{'label': 'POSITIVE', 'score': 0.9998}]

    # ── 文本生成 ──
    generator = pipeline("text-generation", model="gpt2", device=0)
    result = generator("Once upon a time", max_length=50, truncation=True, pad_token_id=50256)
    # [{'generated_text': 'Once upon a time there was a ...'}]

    # ── 问答 ──
    qa = pipeline(
        "question-answering",
        model="distilbert/distilbert-base-cased-distilled-squad",
        device=0
    )
    result = qa(
        question="What is the capital of France?",
        context="Paris is the capital of France."
    )
    # {'answer': 'Paris', 'score': 0.998}

    # ── 文本摘要 ──
    summarizer = pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6",
        device=0
    )
    result = summarizer("Long article text here...", max_length=50, truncation=True)

    # ── 零样本分类（不需要训练！）──
    # cross-encoder 是 zero-shot 的底层模型，用 text-classification 任务加载
    zs_classifier = pipeline(
        "text-classification",
        model="cross-encoder/nli-distilroberta-base",
        device=0
    )
    result = zs_classifier(
        "I love playing football [SEP] sports",
    )
    # cross-encoder 直接输出 entailment/contradiction/neutral
    return (
        classifier,
        generator,
        pipeline,
        qa,
        result,
        summarizer,
        zs_classifier,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 2 步: Tokenizer —— 文本转 Token

        Tokenizer 做三件事：

        1. **分词**：文本 → token 列表
        2. **编码**：token → id 列表
        3. **添加特殊 token**：`[CLS]`, `[SEP]`, `<bos>`, `<eos>` 等
        """
    )
    return


@app.cell
def __(AutoTokenizer):
    tok5 = AutoTokenizer.from_pretrained("bert-base-uncased")

    text5 = "Hello, how are you?"
    print(f"tokens: {tok5.tokenize(text5)}")
    print(f"ids:    {tok5.encode(text5)}")

    batch5 = tok5(["Hello world", "I love NLP"],
                  padding=True, truncation=True, max_length=128, return_tensors="pt")
    print(f"input_ids shape: {batch5['input_ids'].shape}")
    print(f"decoded: {tok5.decode(tok5.encode(text5))}")
    print(f"词汇表大小: {tok5.vocab_size}")

    bert5 = AutoTokenizer.from_pretrained("bert-base-uncased")
    gpt25 = AutoTokenizer.from_pretrained("gpt2")
    print(f"BERT  tokenize('unhappiness'): {bert5.tokenize('unhappiness')}")
    print(f"GPT2  tokenize('unhappiness'): {gpt25.tokenize('unhappiness')}")
    return batch5, bert5, gpt25, text5, tok5


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 3 步: AutoModel —— 加载预训练模型

        `Auto` 系列会根据模型名自动选择正确的类。

        ### 常用 AutoModel 类

        | 类 | 用途 |
        |----|------|
        | `AutoModel` | 基础模型，输出 hidden states |
        | `AutoModelForSequenceClassification` | 文本分类 |
        | `AutoModelForTokenClassification` | 序列标注 NER |
        | `AutoModelForQuestionAnswering` | 问答 |
        | `AutoModelForSeq2SeqLM` | 序列到序列（翻译、摘要）|
        | `AutoModelForCausalLM` | 因果语言模型（GPT 系列）|
        | `AutoModelForMaskedLM` | 掩码语言模型（BERT 系列）|
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 4 步: Fine-tuning —— 微调预训练模型

        ### 核心思路

        ```
        BERT（通用语言理解）
           ↓ 加一个分类头
        BERT + Linear(768→2)
           ↓ 在你的数据上训练
        情感分析模型
        ```

        **只有最后几层参数更新**（或者全部更新），
        比从头训练快很多，数据量需求也少很多。

        ### 两种微调策略

        ```
        策略1: 全量微调（Full Fine-tuning）
          所有参数都更新
          效果好，但慢，显存需求大

        策略2: 冻结底层（Frozen Layers）
          只更新顶层 + 分类头
          快，显存小，但效果略差
        ```
        """
    )
    return


@app.cell
def __(
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataLoader,
    Dataset,
    torch,
):
    class SentimentDataset(Dataset):
        def __init__(self, texts, labels, tokenizer, max_len=128):
            self.encodings = tokenizer(texts, truncation=True, padding=True,
                                       max_length=max_len, return_tensors="pt")
            self.labels = torch.tensor(labels)
        def __len__(self): return len(self.labels)
        def __getitem__(self, idx):
            return {"input_ids": self.encodings["input_ids"][idx],
                    "attention_mask": self.encodings["attention_mask"][idx],
                    "labels": self.labels[idx]}

    train_texts = ["I love this!", "This is terrible", "Amazing film", "Awful movie"]
    train_labels = [1, 0, 1, 0]
    model_name = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    dataset = SentimentDataset(train_texts, train_labels, tokenizer)
    loader = DataLoader(dataset, batch_size=2, shuffle=True)

    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
    model.train()
    for _epoch in range(3):
        for _batch in loader:
            optimizer.zero_grad()
            _outputs = model(**_batch)
            _loss = _outputs.loss
            _loss.backward()
            optimizer.step()
        print(f"Epoch {_epoch+1}, Loss: {_loss.item():.4f}")

    model.eval()
    _inputs9 = tokenizer("This movie is fantastic!", return_tensors="pt")
    with torch.no_grad():
        _pred9 = model(**_inputs9).logits.argmax().item()
    print(f"预测: {'正面' if _pred9 == 1 else '负面'}")
    return (
        SentimentDataset,
        dataset,
        loader,
        model,
        model_name,
        optimizer,
        tokenizer,
        train_labels,
        train_texts,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 5 步: 常用预训练模型速查

        ### 编码器（理解类任务）

        | 模型 | 参数量 | 适合任务 | 特点 |
        |------|--------|---------|------|
        | `bert-base-uncased` | 110M | 分类、NER、问答 | 最经典 |
        | `bert-large-uncased` | 340M | 同上，更强 | 慢 |
        | `roberta-base` | 125M | 分类、NER | 比 BERT 稳 |
        | `distilbert-base-uncased` | 66M | 分类 | BERT 的小版本，快 2x |
        | `chinese-roberta-wwm-ext` | 102M | 中文任务 | 中文首选 |

        ### 解码器（生成类任务）

        | 模型 | 参数量 | 适合任务 | 特点 |
        |------|--------|---------|------|
        | `gpt2` | 117M | 文本生成 | 英文生成 |
        | `gpt2-medium` | 345M | 文本生成 | 更强 |
        | `THUDM/chatglm3-6b` | 6B | 中文对话 | 中文生成首选 |

        ### 编码器-解码器（翻译/摘要）

        | 模型 | 参数量 | 适合任务 | 特点 |
        |------|--------|---------|------|
        | `t5-small` | 60M | 翻译、摘要、问答 | 万能模型 |
        | `t5-base` | 220M | 同上 | 更强 |
        | `Helsinki-NLP/opus-mt-en-zh` | 74M | 英→中翻译 | 专门翻译 |
        | `facebook/bart-large-cnn` | 406M | 摘要 | 摘要首选 |
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 第 6 步: 实战项目推荐路线

        ### 项目1：情感分析（入门，1-2天）

        ```python
        # 数据集: SST-2 (英文) 或 ChnSentiCorp (中文)
        # 模型: bert-base-uncased 或 chinese-roberta-wwm-ext
        # 任务: 二分类（正面/负面）

        from datasets import load_dataset
        dataset = load_dataset("sst2")
        ```

        ### 项目2：命名实体识别（进阶，3-5天）

        ```python
        # 数据集: CoNLL-2003
        # 模型: bert-base-uncased
        # 任务: 识别人名、地名、机构名
        dataset = load_dataset("conll2003")
        ```

        ### 项目3：文本摘要（挑战，1周）

        ```python
        # 数据集: CNN/DailyMail
        # 模型: t5-small 或 facebook/bart-large-cnn
        # 任务: 长文→短摘要
        dataset = load_dataset("cnn_dailymail", "3.0.0")
        ```

        ---

        ## 关键学习路径

        ```
        你现在（原理扎实）
              ↓
        Hugging Face pipeline（今天）
              ↓
        Tokenizer + AutoModel（今天）
              ↓
        Fine-tuning 情感分析（明天）← 第一个实战项目
              ↓
        Fine-tuning 其他任务
              ↓
        部署推理（ONNX / FastAPI）
        ```

        **下一步**: 用 `bert-base-uncased` fine-tune 一个情感分析模型！

        ---

        **相关笔记**: [[transformer_tutorial_marimo]] | [[transformer_training_marimo]] | [[transformer_inference_marimo]]
        """
    )
    return


if __name__ == "__main__":
    app.run()
