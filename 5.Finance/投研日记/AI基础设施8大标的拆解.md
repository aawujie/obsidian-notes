---
title: 态势感知基金 · 8大AI基础设施标的拆解
type: research
created: 2026-05-09
updated: 2026-05-09
sources:
  - Reddit r/wallstreetbets
tags:
  - AI基础设施
  - 美股
  - 数据中心
  - 标的分析
---

## 来源

Reddit r/wallstreetbets 流传的 "Situational Awareness Fund" meme pie chart，持仓覆盖 AI 基础设施全链条。

## 标的一览

| # | 公司 | 代码 | 赛道 |
|:---|:---|:---|:---|
| 1 | Bloom Energy | BE | 分布式电源 |
| 2 | CoreWeave | CRWV | GPU 云 |
| 3 | Intel | INTC | 芯片/代工 |
| 4 | Lumentum | LITE | 光通信 |
| 5 | Core Scientific | CORZ | 矿场→AI托管 |
| 6 | IREN | IREN | 可再生能源数据中心 |
| 7 | Applied Digital | APLD | AI数据中心 |
| 8 | SanDisk | （分拆中） | 闪存存储 |

## 逐家拆解

### 1. Bloom Energy（BE）— 固态氧化物燃料电池

做固定式燃料电池发电系统（Bloom Energy Server），用天然气/氢气现场发电，不依赖电网。数据中心是核心客户——AI 数据中心电力需求爆炸，Bloom 的"分布式基荷电源"概念跟着起飞。2024 年和 Intel、CoreWeave 都有供电协议。

### 2. CoreWeave（CRWV）— GPU 云服务商

原来是挖矿公司，转型成 GPU 云计算平台。手握数十万块 NVIDIA H100/GB200 GPU，出租算力给 AI 公司（包括 OpenAI、Microsoft）。2025 年 IPO，估值 ~230 亿美元。本质就是"算力房东"——买 GPU → 建数据中心 → 租出去。

### 3. Intel（INTC）— 半导体 IDM

关键是为什么出现在这个组合里——Intel 在赌晶圆代工翻身（18A 工艺），同时还做 Gaudi AI 加速器、数据中心 CPU（Xeon）。但 2024-2025 年困境明显：代工亏损、市场份额被 AMD/NVIDIA 蚕食、CEO 换人。这个持仓争议最大。

### 4. Lumentum（LITE）— 光通信器件

做激光器、光模块、3D 传感（iPhone Face ID 的 VCSEL 供应商）。AI 数据中心的核心受益者——GPU 互联需要 800G/1.6T 光模块，光学器件需求爆发。此外还做工业激光和量子通信相关。

### 5. Core Scientific（CORZ）— 比特币挖矿 + AI 托管

北美最大比特币矿企之一。2024 年破产重组后翻身，核心逻辑切换：不只挖矿，还把矿场改造成 AI 数据中心（GPU 托管），签了 CoreWeave 的大单。本质是"电力基础设施公司"——有电、有场地、有冷却，卖算力比挖矿赚钱。

### 6. IREN（IREN）— 可再生能源数据中心

原名 Iris Energy，加拿大/美国运营，用 100% 可再生能源挖比特币 + 做 AI 云计算。跟 Core Scientific 类似——有电有地，转型 AI 托管。2024 年签了 GPU 云服务合同，对标 CoreWeave 的轻资产版。

### 7. Applied Digital（APLD）— 数据中心建设/运营

设计和运营高性能数据中心（HPC），专门给 AI/区块链客户。跟 NVIDIA 有合作，建液冷 GPU 集群。体量比 Equinix 小得多，但 "pure play"——只做 AI 数据中心，没有传统 colocation 包袱。

### 8. SanDisk — 闪存存储

原西部数据（WDC）旗下，2025 年分拆独立上市。做 NAND 闪存、SSD、存储卡。AI 数据中心的存储需求增长（训练数据需要高速存储），但跟上面七个"电力+算力"的逻辑不太一样——存储是配角，不是瓶颈。

## 逻辑链

```
电力（BE）→ 场地/冷却（APLD/CORZ/IREN）→ GPU算力（CRWV）→ 光互联（LITE）→ 芯片（INTC）→ 存储（SanDisk）
```

本质上就是个 meme 版 AI 铲子 ETF，从头到尾把 AI 基础设施全赌了。