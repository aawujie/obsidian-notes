import marimo

__generated_with = "0.8.22"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import torch
    import torch.nn as nn
    from torch.utils.data import Dataset, DataLoader
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    from sklearn.metrics import classification_report, confusion_matrix
    import numpy as np
    import matplotlib.pyplot as plt
    return (
        AutoModelForSequenceClassification,
        AutoTokenizer,
        DataLoader,
        Dataset,
        classification_report,
        confusion_matrix,
        mo,
        nn,
        np,
        plt,
        torch,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        # 情感分析实战项目

        用 BERT 微调一个中文情感分析模型，完整流程：

        ```
        数据准备 → Tokenizer → 模型加载 → 训练 → 评估 → 推理
        ```

        | 步骤 | 内容 |
        |------|------|
        | 1 | 数据准备（中文电影评论）|
        | 2 | Tokenizer 编码 |
        | 3 | 加载 BERT 模型 |
        | 4 | 训练循环 |
        | 5 | 评估（F1、混淆矩阵）|
        | 6 | 推理演示 |
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"""## 第 1 步：数据准备""")
    return


@app.cell
def __():
    # 中文电影评论数据（正面=1，负面=0）
    # 实际项目可替换为从文件/数据库加载
    train_data = [
        # 正面评论
        ("这部电影真的太好看了，剧情紧凑，演员表演精彩！", 1),
        ("感动到哭，是今年看过最好的电影之一", 1),
        ("导演很有才华，每个镜头都很有意境", 1),
        ("演员演技炸裂，剧情反转太刺激了", 1),
        ("画面精美，配乐动听，强烈推荐", 1),
        ("看了两遍还意犹未尽，经典之作", 1),
        ("笑中带泪，故事很有深度，值得一看", 1),
        ("特效很棒，场面宏大，视觉享受", 1),
        ("剧情逻辑严谨，人物刻画细腻，好评", 1),
        ("节奏流畅，两小时完全不无聊，五星", 1),
        ("这是我今年看过最好的华语片", 1),
        ("主角表演非常自然，完全代入剧情", 1),
        ("结局出人意料，让人深思", 1),
        ("配乐太好听了，光是原声带就值回票价", 1),
        ("每个角色都有血有肉，立体饱满", 1),
        # 负面评论
        ("剧情太拖沓了，看了一半就想睡觉", 0),
        ("特效粗糙，演员演技尴尬，浪费时间", 0),
        ("故事老套，没有任何新意，失望", 0),
        ("逻辑漏洞太多，完全经不起推敲", 0),
        ("演员台词像在背书，毫无感情", 0),
        ("剧情虎头蛇尾，结局烂尾了", 0),
        ("票钱打水漂，强行煽情让人尴尬", 0),
        ("节奏拖沓，剧情无聊，中途想离场", 0),
        ("角色扁平，没有任何立体感", 0),
        ("导演不知道想表达什么，看完一头雾水", 0),
        ("特效五毛钱，还不如国产网剧", 0),
        ("剧情漏洞百出，观众当傻子糊弄", 0),
        ("演员选角失误，完全不符合角色气质", 0),
        ("配乐噪杂，完全破坏观影体验", 0),
        ("故事毫无逻辑，编剧应该道歉", 0),
    ]

    test_data = [
        ("这部电影真的很感人，推荐大家去看", 1),
        ("演员演技在线，剧情引人入胜", 1),
        ("完全是在浪费时间，剧情一塌糊涂", 0),
        ("毫无亮点，全程昏昏欲睡", 0),
        ("拍摄手法创新，给人耳目一新的感觉", 1),
        ("强行催泪，剧情假到离谱", 0),
        ("每个细节都经过精心设计，用心之作", 1),
        ("剪辑混乱，完全不知道在讲什么", 0),
    ]

    print(f"训练集: {len(train_data)} 条")
    print(f"测试集: {len(test_data)} 条")
    print(f"正面样本: {sum(1 for _, l in train_data if l==1)}")
    print(f"负面样本: {sum(1 for _, l in train_data if l==0)}")
    return test_data, train_data


@app.cell
def __(mo):
    mo.md(r"""## 第 2 步：Tokenizer 编码""")
    return


@app.cell
def __(AutoTokenizer, DataLoader, Dataset, test_data, torch, train_data):
    # 加载中文 BERT tokenizer
    MODEL_NAME = "hfl/chinese-roberta-wwm-ext"     # 中文 RoBERTa，效果好于原版 BERT
    MAX_LEN = 128                                  # 最大序列长度

    print(f"加载 tokenizer: {MODEL_NAME} ...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    print(f"词汇表大小: {tokenizer.vocab_size}")
    print(f"示例分词: {tokenizer.tokenize('这部电影太好看了')}")

    class SentimentDataset(Dataset):
        """情感分类数据集"""
        def __init__(self, data, tokenizer, max_len):
            self.texts = [d[0] for d in data]       # 文本列表
            self.labels = [d[1] for d in data]      # 标签列表

        def __len__(self):
            return len(self.labels)

        def __getitem__(self, idx):
            encoding = tokenizer(
                self.texts[idx],
                max_length=MAX_LEN,
                padding="max_length",               # 填充到 max_length
                truncation=True,                    # 超长截断
                return_tensors="pt"                 # 返回 PyTorch 张量
            )
            return {
                "input_ids": encoding["input_ids"].squeeze(0),          # (max_len,)
                "attention_mask": encoding["attention_mask"].squeeze(0), # (max_len,)
                "labels": torch.tensor(self.labels[idx], dtype=torch.long)
            }

    train_dataset = SentimentDataset(train_data, tokenizer, MAX_LEN)
    test_dataset = SentimentDataset(test_data, tokenizer, MAX_LEN)

    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=8, shuffle=False)

    print(f"\n训练集 batches: {len(train_loader)}")
    print(f"测试集 batches: {len(test_loader)}")

    # 查看一个样本
    sample = train_dataset[0]
    print(f"\n样本 input_ids shape: {sample['input_ids'].shape}")
    print(f"样本 attention_mask shape: {sample['attention_mask'].shape}")
    print(f"样本 label: {sample['labels'].item()}")
    return (
        MAX_LEN,
        MODEL_NAME,
        SentimentDataset,
        sample,
        test_dataset,
        test_loader,
        tokenizer,
        train_dataset,
        train_loader,
    )


@app.cell
def __(mo):
    mo.md(r"""## 第 3 步：加载 BERT 模型""")
    return


@app.cell
def __(AutoModelForSequenceClassification, MODEL_NAME, torch):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"使用设备: {device}")

    # 加载预训练模型，添加分类头（2分类）
    print(f"加载模型: {MODEL_NAME} ...")
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2                                # 二分类：正面/负面
    )
    model = model.to(device)

    # 查看参数量
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"总参数: {total/1e6:.1f}M")
    print(f"可训练参数: {trainable/1e6:.1f}M")
    return device, model, total, trainable


@app.cell
def __(mo):
    mo.md(r"""## 第 4 步：训练""")
    return


@app.cell
def __(device, model, test_loader, torch, train_loader):
    import torch.optim as optim

    # 优化器：AdamW（比 Adam 对权重衰减处理更好）
    optimizer = optim.AdamW(
        model.parameters(),
        lr=2e-5,            # BERT 微调学习率要小！通常 1e-5 ~ 5e-5
        weight_decay=0.01   # 权重衰减，防止过拟合
    )

    # 学习率调度：线性衰减
    from transformers import get_linear_schedule_with_warmup
    NUM_EPOCHS = 5
    total_steps = len(train_loader) * NUM_EPOCHS
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=total_steps // 10,     # 前 10% 步 warmup
        num_training_steps=total_steps
    )

    def evaluate(model, loader, device):
        """在数据集上评估准确率"""
        model.eval()
        correct, total = 0, 0
        with torch.no_grad():
            for _batch in loader:
                _input_ids = _batch["input_ids"].to(device)
                _attention_mask = _batch["attention_mask"].to(device)
                _labels = _batch["labels"].to(device)
                _outputs = model(input_ids=_input_ids, attention_mask=_attention_mask)
                _preds = _outputs.logits.argmax(dim=-1)
                correct += (_preds == _labels).sum().item()
                total += _labels.size(0)
        return correct / total

    # 训练循环
    train_losses, train_accs, test_accs = [], [], []

    for _epoch in range(NUM_EPOCHS):
        model.train()
        _epoch_loss = 0

        for _batch in train_loader:
            _input_ids = _batch["input_ids"].to(device)
            _attention_mask = _batch["attention_mask"].to(device)
            _labels = _batch["labels"].to(device)

            optimizer.zero_grad()
            _outputs = model(input_ids=_input_ids, attention_mask=_attention_mask, labels=_labels)
            _loss = _outputs.loss
            _loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()
            _epoch_loss += _loss.item()

        _avg_loss = _epoch_loss / len(train_loader)
        _train_acc = evaluate(model, train_loader, device)
        _test_acc = evaluate(model, test_loader, device)

        train_losses.append(_avg_loss)
        train_accs.append(_train_acc)
        test_accs.append(_test_acc)

        print(f"Epoch {_epoch+1}/{NUM_EPOCHS}  loss={_avg_loss:.4f}  "
              f"train_acc={_train_acc:.3f}  test_acc={_test_acc:.3f}")

    print("\n训练完成！")
    return (
        NUM_EPOCHS,
        evaluate,
        get_linear_schedule_with_warmup,
        optim,
        optimizer,
        scheduler,
        test_accs,
        total_steps,
        train_accs,
        train_losses,
    )


@app.cell
def __(mo):
    mo.md(r"""## 第 5 步：评估""")
    return


@app.cell
def __(
    NUM_EPOCHS,
    classification_report,
    device,
    model,
    plt,
    test_accs,
    test_loader,
    torch,
    train_accs,
    train_losses,
):
    # 收集预测结果
    all_preds, all_labels = [], []
    model.eval()
    with torch.no_grad():
        for _batch in test_loader:
            _input_ids = _batch["input_ids"].to(device)
            _attention_mask = _batch["attention_mask"].to(device)
            _labels = _batch["labels"].to(device)
            _outputs = model(input_ids=_input_ids, attention_mask=_attention_mask)
            _preds = _outputs.logits.argmax(dim=-1)
            all_preds.extend(_preds.cpu().tolist())
            all_labels.extend(_labels.cpu().tolist())

    # 分类报告
    print("分类报告:")
    print(classification_report(all_labels, all_preds, target_names=["负面", "正面"]))

    # 图1：训练曲线
    fig1, axes = plt.subplots(1, 2, figsize=(12, 4))
    epochs = range(1, NUM_EPOCHS + 1)

    axes[0].plot(epochs, train_losses, 'b-o', label='Train Loss')
    axes[0].set(xlabel='Epoch', ylabel='Loss', title='训练损失')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    axes[1].plot(epochs, train_accs, 'b-o', label='Train Acc')
    axes[1].plot(epochs, test_accs, 'r-o', label='Test Acc')
    axes[1].set(xlabel='Epoch', ylabel='Accuracy', title='准确率', ylim=[0, 1.05])
    axes[1].legend(); axes[1].grid(True, alpha=0.3)

    fig1.tight_layout()
    fig1
    return all_labels, all_preds, axes, epochs, fig1


@app.cell
def __(all_labels, all_preds, confusion_matrix, plt):
    # 图2：混淆矩阵
    cm = confusion_matrix(all_labels, all_preds)
    fig2, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(cm, cmap='Blues')
    plt.colorbar(im)
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.set_xticklabels(['负面', '正面'])
    ax.set_yticklabels(['负面', '正面'])
    ax.set_xlabel('预测'); ax.set_ylabel('真实')
    ax.set_title('混淆矩阵')
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i, j]), ha='center', va='center',
                    color='white' if cm[i, j] > cm.max()/2 else 'black', fontsize=14)
    fig2.tight_layout()
    fig2
    return ax, cm, fig2, i, im, j


@app.cell
def __(mo):
    mo.md(r"""## 第 6 步：推理演示""")
    return


@app.cell
def __(device, model, tokenizer, torch):
    def predict(text):
        """对单条文本做情感预测"""
        model.eval()
        encoding = tokenizer(
            text,
            max_length=128,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        input_ids = encoding["input_ids"].to(device)
        attention_mask = encoding["attention_mask"].to(device)

        with torch.no_grad():
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            probs = torch.softmax(outputs.logits, dim=-1)[0]
            pred = probs.argmax().item()

        label = "正面 😊" if pred == 1 else "负面 😞"
        confidence = probs[pred].item()
        return label, confidence

    # 测试几条句子
    test_cases = [
        "这部电影让我感动到流泪，强烈推荐！",
        "剧情太烂了，浪费我两个小时",
        "还行吧，没有特别惊喜",
        "演员演技在线，但剧情有点拖",
        "年度最佳，必须五星好评！",
        "看了想睡觉，完全不推荐",
    ]

    print(f"{'文本':<25} {'预测':<10} {'置信度'}")
    print("─" * 50)
    for text in test_cases:
        label, conf = predict(text)
        print(f"{text:<25} {label:<10} {conf:.3f}")
    return conf, label, predict, test_cases, text


if __name__ == "__main__":
    app.run()
