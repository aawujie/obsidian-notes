---
title: SpiderFoot OSINT 自动化工具原理
type: concept
created: 2026-06-22
source: https://github.com/smicallef/spiderfoot
tags: [OSINT, 安全工具, SpiderFoot, 侦察, 威胁情报]
---

## 概述

SpiderFoot 是 OSINT 自动化工具，200+ 模块，Python 3，MIT 协议。核心设计：**事件驱动的发布/订阅模块系统**。

## 核心架构：事件驱动级联

```
用户输入目标（域名/IP/邮箱/人名）
        ↓
   生成种子事件（Seed Event）
   例如：INTERNET_NAME
        ↓
   ┌─────────────────────────────┐
   │     事件总线（Event Bus）     │
   │  订阅此事件类型的模块被唤醒    │
   └─────────────────────────────┘
        ↓
   sfp_dnsresolve → 解析域名 → 发出 IP_ADDRESS
        ↓
   sfp_shodan + sfp_abuseipdb → 查询端口/恶意记录 → 发出 TCP_PORT_OPEN
        ↓
   sfp_sslcert → 查证书 → 发出 SSL_CERTIFICATE_ISSUED
        ↓
   ... 级联传播，直到没有新事件产生
```

不是线性执行，而是**级联图**：每个模块只看自己订阅的事件类型，产出结果后发出新事件，新事件触发更多模块。

## 两种扫描模式

| 模式 | 原理 | 是否接触目标 |
|:---|:---|:---|
| 被动 | 只查第三方数据源（搜索引擎、证书日志、DNS、威胁情报、泄露库） | 不接触 |
| 主动 | 直接连接目标（端口扫描、爬虫、横幅抓取、暴力破解） | 会接触 |

被动模式法务安全，主动模式更深入但留痕迹。

## 模块分类

- DNS 类：解析、反向解析、子域名爆破、区域传输
- 搜索引擎类：Google、Bing、Shodan、Censys
- 证书透明类：crt.sh、CertSpotter
- 威胁情报类：AlienVault OTX、AbuseIPDB、blocklist.de
- 泄露数据类：HaveIBeenPwned、Dehashed
- 社交媒体类：账户查找（500+ 平台）
- 基础设施类：S3 Bucket 发现、Azure Blob 发现
- 工具链类：Wappalyzer、WhatWeb、TruffleHog

## 数据关联

扫描完成后自动关联：域名 → IP → 端口 → 证书 → 内部主机名 → 员工邮箱 → 泄露记录。

## 部署

- 内嵌 Web 服务器 + Web UI
- 支持纯命令行
- 商业版 HX 支持定时扫描、变更通知、Splunk/ES 实时推送

## 一句话

200+ 数据源 × 事件驱动级联 × 自动关联分析。给一个起点，自动沿信息图谱扩散，穷尽所有关联数据。