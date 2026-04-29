---
title: 15-NLP 应用
source: https://zh.d2l.ai/chapter_natural-language-processing-applications/index.html
converted_at: 2026-02-28
---

# 15\. 自然语言处理：应用[¶](#chap-nlp-app "Permalink to this heading")

前面我们学习了如何在文本序列中表示词元， 并在[14节](../chapter%5Fnatural-language-processing-pretraining/index.html#chap-nlp-pretrain)中训练了词元的表示。 这样的预训练文本表示可以通过不同模型架构，放入不同的下游自然语言处理任务。

前一章我们提及到一些自然语言处理应用，这些应用没有预训练，只是为了解释深度学习架构。 例如，在 [8节](../chapter%5Frecurrent-neural-networks/index.html#chap-rnn)中， 我们依赖循环神经网络设计语言模型来生成类似中篇小说的文本。 在[9节](../chapter%5Frecurrent-modern/index.html#chap-modern-rnn)和 [10节](../chapter%5Fattention-mechanisms/index.html#chap-attention)中， 我们还设计了基于循环神经网络和注意力机制的机器翻译模型。

然而，本书并不打算全面涵盖所有此类应用。 相反，我们的重点是_如何应用深度语言表征学习来解决自然语言处理问题_。 在给定预训练的文本表示的情况下， 本章将探讨两种流行且具有代表性的下游自然语言处理任务： 情感分析和自然语言推断，它们分别分析单个文本和文本对之间的关系。

图15.1 预训练文本表示可以通过不同模型架构，放入不同的下游自然语言处理应用（本章重点介绍如何为不同的下游应用设计模型）[¶](#id2 "Permalink to this image")

如 [图15.1](#fig-nlp-map-app)所述， 本章将重点描述然后使用不同类型的深度学习架构 （如多层感知机、卷积神经网络、循环神经网络和注意力） 设计自然语言处理模型。 尽管在 [图15.1](#fig-nlp-map-app)中， 可以将任何预训练的文本表示与任何应用的架构相结合， 但我们选择了一些具有代表性的组合。 具体来说，我们将探索基于循环神经网络和卷积神经网络的流行架构进行情感分析。 对于自然语言推断，我们选择注意力和多层感知机来演示如何分析文本对。 最后，我们介绍了如何为广泛的自然语言处理应用， 如在序列级（单文本分类和文本对分类）和词元级（文本标注和问答）上 对预训练BERT模型进行微调。 作为一个具体的经验案例，我们将针对自然语言推断对BERT进行微调。

正如我们在 [14.8节](../chapter%5Fnatural-language-processing-pretraining/bert.html#sec-bert)中介绍的那样， 对于广泛的自然语言处理应用，BERT只需要最少的架构更改。 然而，这一好处是以微调下游应用的大量BERT参数为代价的。 当空间或时间有限时，基于多层感知机、卷积神经网络、循环神经网络 和注意力的精心构建的模型更具可行性。 下面，我们从情感分析应用开始，分别解读基于循环神经网络和卷积神经网络的模型设计。

* [15.1\. 情感分析及数据集](sentiment-analysis-and-dataset.html)  
   * [15.1.1\. 读取数据集](sentiment-analysis-and-dataset.html#id2)  
   * [15.1.2\. 预处理数据集](sentiment-analysis-and-dataset.html#id3)  
   * [15.1.3\. 创建数据迭代器](sentiment-analysis-and-dataset.html#id4)  
   * [15.1.4\. 整合代码](sentiment-analysis-and-dataset.html#id5)  
   * [15.1.5\. 小结](sentiment-analysis-and-dataset.html#id6)  
   * [15.1.6\. 练习](sentiment-analysis-and-dataset.html#id7)
* [15.2\. 情感分析：使用循环神经网络](sentiment-analysis-rnn.html)  
   * [15.2.1\. 使用循环神经网络表示单个文本](sentiment-analysis-rnn.html#id3)  
   * [15.2.2\. 加载预训练的词向量](sentiment-analysis-rnn.html#id4)  
   * [15.2.3\. 训练和评估模型](sentiment-analysis-rnn.html#id5)  
   * [15.2.4\. 小结](sentiment-analysis-rnn.html#id6)  
   * [15.2.5\. 练习](sentiment-analysis-rnn.html#id7)
* [15.3\. 情感分析：使用卷积神经网络](sentiment-analysis-cnn.html)  
   * [15.3.1\. 一维卷积](sentiment-analysis-cnn.html#id3)  
   * [15.3.2\. 最大时间汇聚层](sentiment-analysis-cnn.html#id4)  
   * [15.3.3\. textCNN模型](sentiment-analysis-cnn.html#textcnn)  
   * [15.3.4\. 小结](sentiment-analysis-cnn.html#id9)  
   * [15.3.5\. 练习](sentiment-analysis-cnn.html#id10)
* [15.4\. 自然语言推断与数据集](natural-language-inference-and-dataset.html)  
   * [15.4.1\. 自然语言推断](natural-language-inference-and-dataset.html#id2)  
   * [15.4.2\. 斯坦福自然语言推断（SNLI）数据集](natural-language-inference-and-dataset.html#snli)  
   * [15.4.3\. 小结](natural-language-inference-and-dataset.html#id7)  
   * [15.4.4\. 练习](natural-language-inference-and-dataset.html#id8)
* [15.5\. 自然语言推断：使用注意力](natural-language-inference-attention.html)  
   * [15.5.1\. 模型](natural-language-inference-attention.html#id3)  
   * [15.5.2\. 训练和评估模型](natural-language-inference-attention.html#id7)  
   * [15.5.3\. 小结](natural-language-inference-attention.html#id12)  
   * [15.5.4\. 练习](natural-language-inference-attention.html#id13)
* [15.6\. 针对序列级和词元级应用微调BERT](finetuning-bert.html)  
   * [15.6.1\. 单文本分类](finetuning-bert.html#id1)  
   * [15.6.2\. 文本对分类或回归](finetuning-bert.html#id3)  
   * [15.6.3\. 文本标注](finetuning-bert.html#id5)  
   * [15.6.4\. 问答](finetuning-bert.html#id6)  
   * [15.6.5\. 小结](finetuning-bert.html#id8)  
   * [15.6.6\. 练习](finetuning-bert.html#id9)
* [15.7\. 自然语言推断：微调BERT](natural-language-inference-bert.html)  
   * [15.7.1\. 加载预训练的BERT](natural-language-inference-bert.html#id1)  
   * [15.7.2\. 微调BERT的数据集](natural-language-inference-bert.html#id2)  
   * [15.7.3\. 微调BERT](natural-language-inference-bert.html#id3)  
   * [15.7.4\. 小结](natural-language-inference-bert.html#id4)  
   * [15.7.5\. 练习](natural-language-inference-bert.html#id5)

[ Previous 14.10\. 预训练BERT ](../chapter%5Fnatural-language-processing-pretraining/bert-pretraining.html) [ Next 15.1\. 情感分析及数据集 ](sentiment-analysis-and-dataset.html)