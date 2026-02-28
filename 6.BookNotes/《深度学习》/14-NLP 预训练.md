---
title: 14-NLP 预训练
source: https://zh.d2l.ai/chapter_natural-language-processing-pretraining/index.html
converted_at: 2026-02-28
---

# 14\. 自然语言处理：预训练[¶](#chap-nlp-pretrain "Permalink to this heading")

人与人之间需要交流。 出于人类这种基本需要，每天都有大量的书面文本产生。 比如，社交媒体、聊天应用、电子邮件、产品评论、新闻文章、 研究论文和书籍中的丰富文本， 使计算机能够理解它们以提供帮助或基于人类语言做出决策变得至关重要。

_自然语言处理_是指研究使用自然语言的计算机和人类之间的交互。 在实践中，使用自然语言处理技术来处理和分析文本数据是非常常见的， 例如[8.3节](../chapter%5Frecurrent-neural-networks/language-models-and-dataset.html#sec-language-model)的语言模型 和[9.5节](../chapter%5Frecurrent-modern/machine-translation-and-dataset.html#sec-machine-translation)的机器翻译模型。

要理解文本，我们可以从学习它的表示开始。 利用来自大型语料库的现有文本序列， _自监督学习_（self-supervised learning） 已被广泛用于预训练文本表示， 例如通过使用周围文本的其它部分来预测文本的隐藏部分。 通过这种方式，模型可以通过有监督地从_海量_文本数据中学习，而不需要_昂贵_的标签标注！

本章我们将看到：当将每个单词或子词视为单个词元时， 可以在大型语料库上使用word2vec、GloVe或子词嵌入模型预先训练每个词元的词元。 经过预训练后，每个词元的表示可以是一个向量。 但是，无论上下文是什么，它都保持不变。 例如，“bank”（可以译作银行或者河岸）的向量表示在 “go to the bank to deposit some money”（去银行存点钱） 和“go to the bank to sit down”（去河岸坐下来）中是相同的。 因此，许多较新的预训练模型使相同词元的表示适应于不同的上下文， 其中包括基于Transformer编码器的更深的自监督模型BERT。 在本章中，我们将重点讨论如何预训练文本的这种表示， 如[图14.1](#fig-nlp-map-pretrain)中所强调的那样。

图14.1 预训练好的文本表示可以放入各种深度学习架构，应用于不同自然语言处理任务（本章主要研究上游文本的预训练）[¶](#id2 "Permalink to this image")

[图14.1](#fig-nlp-map-pretrain)显示了 预训练好的文本表示可以放入各种深度学习架构，应用于不同自然语言处理任务。 我们将在 [15节](../chapter%5Fnatural-language-processing-applications/index.html#chap-nlp-app)中介绍它们。

* [14.1\. 词嵌入（word2vec）](word2vec.html)  
   * [14.1.1\. 为何独热向量是一个糟糕的选择](word2vec.html#id1)  
   * [14.1.2\. 自监督的word2vec](word2vec.html#id2)  
   * [14.1.3\. 跳元模型（Skip-Gram）](word2vec.html#skip-gram)  
   * [14.1.4\. 连续词袋（CBOW）模型](word2vec.html#cbow)  
   * [14.1.5\. 小结](word2vec.html#id8)  
   * [14.1.6\. 练习](word2vec.html#id9)
* [14.2\. 近似训练](approx-training.html)  
   * [14.2.1\. 负采样](approx-training.html#subsec-negative-sampling)  
   * [14.2.2\. 层序Softmax](approx-training.html#softmax)  
   * [14.2.3\. 小结](approx-training.html#id3)  
   * [14.2.4\. 练习](approx-training.html#id4)
* [14.3\. 用于预训练词嵌入的数据集](word-embedding-dataset.html)  
   * [14.3.1\. 读取数据集](word-embedding-dataset.html#id2)  
   * [14.3.2\. 下采样](word-embedding-dataset.html#id3)  
   * [14.3.3\. 中心词和上下文词的提取](word-embedding-dataset.html#id5)  
   * [14.3.4\. 负采样](word-embedding-dataset.html#id6)  
   * [14.3.5\. 小批量加载训练实例](word-embedding-dataset.html#subsec-word2vec-minibatch-loading)  
   * [14.3.6\. 整合代码](word-embedding-dataset.html#id9)  
   * [14.3.7\. 小结](word-embedding-dataset.html#id10)  
   * [14.3.8\. 练习](word-embedding-dataset.html#id11)
* [14.4\. 预训练word2vec](word2vec-pretraining.html)  
   * [14.4.1\. 跳元模型](word2vec-pretraining.html#id1)  
   * [14.4.2\. 训练](word2vec-pretraining.html#id4)  
   * [14.4.3\. 应用词嵌入](word2vec-pretraining.html#subsec-apply-word-embed)  
   * [14.4.4\. 小结](word2vec-pretraining.html#id9)  
   * [14.4.5\. 练习](word2vec-pretraining.html#id10)
* [14.5\. 全局向量的词嵌入（GloVe）](glove.html)  
   * [14.5.1\. 带全局语料统计的跳元模型](glove.html#subsec-skipgram-global)  
   * [14.5.2\. GloVe模型](glove.html#id2)  
   * [14.5.3\. 从条件概率比值理解GloVe模型](glove.html#id4)  
   * [14.5.4\. 小结](glove.html#id6)  
   * [14.5.5\. 练习](glove.html#id7)
* [14.6\. 子词嵌入](subword-embedding.html)  
   * [14.6.1\. fastText模型](subword-embedding.html#fasttext)  
   * [14.6.2\. 字节对编码（Byte Pair Encoding）](subword-embedding.html#byte-pair-encoding)  
   * [14.6.3\. 小结](subword-embedding.html#id6)  
   * [14.6.4\. 练习](subword-embedding.html#id7)
* [14.7\. 词的相似性和类比任务](similarity-analogy.html)  
   * [14.7.1\. 加载预训练词向量](similarity-analogy.html#id2)  
   * [14.7.2\. 应用预训练词向量](similarity-analogy.html#id3)  
   * [14.7.3\. 小结](similarity-analogy.html#id6)  
   * [14.7.4\. 练习](similarity-analogy.html#id7)
* [14.8\. 来自Transformers的双向编码器表示（BERT）](bert.html)  
   * [14.8.1\. 从上下文无关到上下文敏感](bert.html#id1)  
   * [14.8.2\. 从特定于任务到不可知任务](bert.html#id5)  
   * [14.8.3\. BERT：把两个最好的结合起来](bert.html#bert)  
   * [14.8.4\. 输入表示](bert.html#subsec-bert-input-rep)  
   * [14.8.5\. 预训练任务](bert.html#subsec-bert-pretraining-tasks)  
   * [14.8.6\. 整合代码](bert.html#id11)  
   * [14.8.7\. 小结](bert.html#id12)  
   * [14.8.8\. 练习](bert.html#id13)
* [14.9\. 用于预训练BERT的数据集](bert-dataset.html)  
   * [14.9.1\. 为预训练任务定义辅助函数](bert-dataset.html#id2)  
   * [14.9.2\. 将文本转换为预训练数据集](bert-dataset.html#id5)  
   * [14.9.3\. 小结](bert-dataset.html#id7)  
   * [14.9.4\. 练习](bert-dataset.html#id8)
* [14.10\. 预训练BERT](bert-pretraining.html)  
   * [14.10.1\. 预训练BERT](bert-pretraining.html#id1)  
   * [14.10.2\. 用BERT表示文本](bert-pretraining.html#id3)  
   * [14.10.3\. 小结](bert-pretraining.html#id4)  
   * [14.10.4\. 练习](bert-pretraining.html#id5)

[ Previous 13.14\. 实战Kaggle比赛：狗的品种识别（ImageNet Dogs） ](../chapter%5Fcomputer-vision/kaggle-dog.html) [ Next 14.1\. 词嵌入（word2vec） ](word2vec.html)