---
title: OpenVLA-开源VLA模型
type: paper-note
created: 2026-06-01
tags: [vla, embodied-ai, paper-note, open-source]
---

## 论文信息
- **标题**: OpenVLA: An Open-Source Vision-Language-Action Model
- **作者/机构**: Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, Chelsea Finn (Stanford, UC Berkeley, TRI, Google DeepMind)
- **发表时间**: 2024年6月
- **arXiv**: https://arxiv.org/abs/2406.09246
- **项目主页**: https://openvla.github.io
- **引用**: Kim et al., "OpenVLA: An Open-Source Vision-Language-Action Model", 2024

## 核心问题
虽然RT-2证明了VLA模型的有效性，但存在两个核心障碍阻碍其广泛采用：(1) 现有VLA模型(RT-2等)是闭源的，公众无法获取；(2) 如何在消费级GPU上高效微调VLA模型以适应新任务尚未被探索。OpenVLA的目标是提供一个**开源、7B参数、可在消费级GPU上微调的VLA模型**。

## 关键方法
1. **多粒度视觉编码**：使用DINOv2(捕捉空间结构)和SigLIP(捕捉语义信息)两个视觉编码器的融合特征作为视觉输入，获取多粒度的视觉表示。
2. **Llama 2语言模型Backbone**：采用Llama 2-7B作为语言模型基础，将视觉特征通过投影层映射后送入LLM中。
3. **大规模机器人数据训练**：在Open X-Embodiment数据集的970k条真实机器人演示轨迹上训练，覆盖多种机器人硬件形态(embodiment)、任务和场景。
4. **LoRA微调**：首次证明VLA模型可以通过低秩适配(LoRA)在消费级GPU上高效微调，且不影响下游任务成功率。
5. **量化部署**：支持通过模型量化实现高效推理，不损失任务成功率。

## 重要细节
- **参数量**：7B参数(相比RT-2-X的55B参数，仅1/7)
- **性能**：跨29个任务和多种机器人形态，**绝对成功率比RT-2-X(55B)高16.5%**
- **微调后性能**：微调后的OpenVLA在涉及多物体和语言接地的多任务环境中，比Diffusion Policy高20.4%成功率
- **跨embodiment泛化**：支持WidowX和Google Robot等多种机器人硬件
- **代码开源**：提供PyTorch代码库，支持FSDP全分片数据并行、FlashAttention、AMP自动混合精度训练
- **训练基础设施**：可从单GPU微调扩展到多节点GPU集群训练

## 与面试50题的关系
- **Q4 (开源VLA/如何在自己的机器人上使用VLA)**：OpenVLA是当前最重要的开源VLA方案，了解它的架构、微调方式(LoRA)和部署方案(量化)是回答此类问题的关键。面试官可能直接问"如果你要在自己的机器人上部署VLA，你会用什么方案？"

## 个人思考