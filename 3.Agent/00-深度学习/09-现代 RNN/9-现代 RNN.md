---
title: 9-现代 RNN
source: https://zh.d2l.ai/chapter_recurrent-modern/index.html
converted_at: 2026-02-28
---

# 9\. 现代循环神经网络[¶](#chap-modern-rnn "Permalink to this heading")

前一章中我们介绍了循环神经网络的基础知识， 这种网络可以更好地处理序列数据。 我们在文本数据上实现了基于循环神经网络的语言模型， 但是对于当今各种各样的序列学习问题，这些技术可能并不够用。

例如，循环神经网络在实践中一个常见问题是数值不稳定性。 尽管我们已经应用了梯度裁剪等技巧来缓解这个问题， 但是仍需要通过设计更复杂的序列模型来进一步处理它。 具体来说，我们将引入两个广泛使用的网络， 即_门控循环单元_（gated recurrent units，GRU）和 _长短期记忆网络_（long short-term memory，LSTM）。 然后，我们将基于一个单向隐藏层来扩展循环神经网络架构。 我们将描述具有多个隐藏层的深层架构， 并讨论基于前向和后向循环计算的双向设计。 现代循环网络经常采用这种扩展。 在解释这些循环神经网络的变体时， 我们将继续考虑[8节](../chapter%5Frecurrent-neural-networks/index.html#chap-rnn)中的语言建模问题。

事实上，语言建模只揭示了序列学习能力的冰山一角。 在各种序列学习问题中，如自动语音识别、文本到语音转换和机器翻译， 输入和输出都是任意长度的序列。 为了阐述如何拟合这种类型的数据， 我们将以机器翻译为例介绍基于循环神经网络的 “编码器－解码器”架构和束搜索，并用它们来生成序列。

* [9.1\. 门控循环单元（GRU）](gru.html)  
   * [9.1.1\. 门控隐状态](gru.html#id4)  
   * [9.1.2\. 从零开始实现](gru.html#id8)  
   * [9.1.3\. 简洁实现](gru.html#id12)  
   * [9.1.4\. 小结](gru.html#id13)  
   * [9.1.5\. 练习](gru.html#id14)
* [9.2\. 长短期记忆网络（LSTM）](lstm.html)  
   * [9.2.1\. 门控记忆元](lstm.html#id2)  
   * [9.2.2\. 从零开始实现](lstm.html#id7)  
   * [9.2.3\. 简洁实现](lstm.html#id11)  
   * [9.2.4\. 小结](lstm.html#id12)  
   * [9.2.5\. 练习](lstm.html#id13)
* [9.3\. 深度循环神经网络](deep-rnn.html)  
   * [9.3.1\. 函数依赖关系](deep-rnn.html#id2)  
   * [9.3.2\. 简洁实现](deep-rnn.html#id3)  
   * [9.3.3\. 训练与预测](deep-rnn.html#id4)  
   * [9.3.4\. 小结](deep-rnn.html#id5)  
   * [9.3.5\. 练习](deep-rnn.html#id6)
* [9.4\. 双向循环神经网络](bi-rnn.html)  
   * [9.4.1\. 隐马尔可夫模型中的动态规划](bi-rnn.html#id2)  
   * [9.4.2\. 双向模型](bi-rnn.html#id5)  
   * [9.4.3\. 双向循环神经网络的错误应用](bi-rnn.html#id10)  
   * [9.4.4\. 小结](bi-rnn.html#id11)  
   * [9.4.5\. 练习](bi-rnn.html#id12)
* [9.5\. 机器翻译与数据集](machine-translation-and-dataset.html)  
   * [9.5.1\. 下载和预处理数据集](machine-translation-and-dataset.html#id3)  
   * [9.5.2\. 词元化](machine-translation-and-dataset.html#id4)  
   * [9.5.3\. 词表](machine-translation-and-dataset.html#id5)  
   * [9.5.4\. 加载数据集](machine-translation-and-dataset.html#subsec-mt-data-loading)  
   * [9.5.5\. 训练模型](machine-translation-and-dataset.html#id7)  
   * [9.5.6\. 小结](machine-translation-and-dataset.html#id8)  
   * [9.5.7\. 练习](machine-translation-and-dataset.html#id9)
* [9.6\. 编码器-解码器架构](encoder-decoder.html)  
   * [9.6.1\. 编码器](encoder-decoder.html#id2)  
   * [9.6.2\. 解码器](encoder-decoder.html#id3)  
   * [9.6.3\. 合并编码器和解码器](encoder-decoder.html#id4)  
   * [9.6.4\. 小结](encoder-decoder.html#id5)  
   * [9.6.5\. 练习](encoder-decoder.html#id6)
* [9.7\. 序列到序列学习（seq2seq）](seq2seq.html)  
   * [9.7.1\. 编码器](seq2seq.html#id4)  
   * [9.7.2\. 解码器](seq2seq.html#sec-seq2seq-decoder)  
   * [9.7.3\. 损失函数](seq2seq.html#id6)  
   * [9.7.4\. 训练](seq2seq.html#sec-seq2seq-training)  
   * [9.7.5\. 预测](seq2seq.html#id8)  
   * [9.7.6\. 预测序列的评估](seq2seq.html#id9)  
   * [9.7.7\. 小结](seq2seq.html#id11)  
   * [9.7.8\. 练习](seq2seq.html#id12)
* [9.8\. 束搜索](beam-search.html)  
   * [9.8.1\. 贪心搜索](beam-search.html#id2)  
   * [9.8.2\. 穷举搜索](beam-search.html#id3)  
   * [9.8.3\. 束搜索](beam-search.html#id5)  
   * [9.8.4\. 小结](beam-search.html#id6)  
   * [9.8.5\. 练习](beam-search.html#id7)

[ Previous 8.7\. 通过时间反向传播 ](../chapter%5Frecurrent-neural-networks/bptt.html) [ Next 9.1\. 门控循环单元（GRU） ](gru.html)