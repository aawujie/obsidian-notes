---
title: Obsidian 老板亲自下场讨好AI
type: 摘录
created: 2026-06-24
updated: 2026-06-24
source: https://x.com/liulangtutu/status/2069571107959496892
tags:
  - AI
  - Obsidian
  - 工具
  - 思维方式
---

# 当一个软件（Obsidian）的老板，开始亲自讨好AI

> 原文：流浪土土（@liulangtutu）X Article
> 2026-06-24

这两天我在GitHub上刷到一个仓库，star数已经三万七千多了，叫obsidian-skills。我以为也就是普普通通的skill，直到我看了一眼作者——kepano。

你可能觉得这个名字陌生，不过没关系，你只需要知道这个人叫 Steph Ango，是 Obsidian 的 CEO。

这不是普通爱好者自己折腾的 skill，而是 Obsidian 的老板亲自下场给 Obsidian 写了一套给 AI 用的说明书。

我还是很惊讶的，不是因为这个 skill 多么有技术含量，而是一个工具的创始人，亲自下场琢磨"怎么让AI更好的用我的工具"，这个信号比 36000 个 star 更吸引人。

关于 skill 本身我们就不多说了，我们说下这个仓库里的 5 个 skill 都是干什么的。

第一个叫 **obsidian-markdown**，教AI写Obsidian风味的markdown。你可能觉得 markdown 谁不会啊？但是你知道 Obsidian 为了笔记内容更丰富，自创了一些指令，比如连接`[[这样]]`、嵌入`![[这样]]`、还有十三种callout提示框、属性、Mermaid图、LaTeX公式。AI 当然能写出来markdown，但那只是普普通通的markdown。而装备了这个skill，AI 就可以写出原汁原味的 Obsidian markdown。

第二个叫 **obsidian-bases**，这个很有用。Bases是Obsidian去年才出的功能，可以把我们零散的笔记变成一个能筛选、能排序、能算公式的数据库视图。支持表格视图、卡片视图、列表视图、地图视图。还能写if判断、算日期差、做求和求平均。但是Bases 的语法挺复杂的，是YAML格式，而且校验很严格，一个引号没写对就会报错，手写的话还是有点费精力的。但如果你装了这个skill，就可以直接跟AI说，把所有category是article的笔记拉出来，按时间排序，给我做一个视图。AI 会自己识别到该用 Bases 这个skill，只需要几秒，一个格式完全正确的.base文件就做好了，不需要去学习语法了，只需要跟 AI 说人话就好了。

第三个叫 **defuddle**，可以过滤掉网页里的广告和无关内容，只留下正文给AI看。毕竟现在网页上充满了边边角角的广告，有了这个，我们的笔记也更干净了。

第四个是 **json-canvas**，完整支持JSON Canvas格式（.canvas文件）。智能体能创建节点、连线、群组，实现可视化思维导图和项目画布的自动化构建。

第五个是 **obsidian-cli**，让AI通过Obsidian官方CLI管理仓库、开发插件和主题。适合进阶用户实现自动化工作流。

把这5个skill放在一起，AI 与你的笔记就可以无缝集成，无缝协作了——能读，能写，能查，能建视图，能存干净网页到笔记里。AI 从聊天窗口直接住进了笔记里，变成了我们的笔记小助理。

如果你已经在用Obsidian，又想让AI真正"懂"你的笔记库，而不是简单聊天，obsidian-skills 是目前最优雅、最本地化的解决方案。