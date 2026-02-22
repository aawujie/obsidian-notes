# RSSHub 架构分析

> 创建时间：2026-02-22
> 标签：#RSS #爬虫 #架构分析 #开源项目

---

## 核心概念

**RSSHub 是什么？**

一个开源的 RSS 订阅源生成器，能为各种**没有 RSS 的网站**自动生成 RSS 订阅源。

**核心思想：**
```
没有 RSS 的网站  →  [RSSHub]  →  标准 RSS 订阅源
(YouTube/B 站/微博)           (你可以订阅的链接)
```

---

## 工作原理

### 基本流程

```
用户请求 → RSSHub 路由匹配 → 调用爬虫脚本 → 爬取目标网站 → 生成 RSS XML → 返回
```

### 示例：YouTube 频道订阅

1. **用户请求**
   ```
   GET http://localhost:1200/youtube/channel/UCBJycsmduvYEL83R_U4JriQ
   ```

2. **路由匹配**
   ```javascript
   router.get('/youtube/channel/:id', async (ctx) => {
       const channelId = ctx.params.id;
       const videos = await youtubeCrawler.fetchChannelVideos(channelId);
       ctx.state.data = { title, link, item: videos };
   });
   ```

3. **爬取数据**
   - 调用 YouTube API 或爬取网页
   - 解析 HTML，提取视频信息

4. **返回 RSS**
   ```xml
   <rss version="2.0">
     <channel>
       <title>YouTube Channel - UCBJycsmduvYEL83R_U4JriQ</title>
       <item>
         <title>最新视频标题</title>
         <link>https://youtube.com/watch?v=xxx</link>
         <pubDate>Sun, 22 Feb 2026 10:00:00 GMT</pubDate>
       </item>
     </channel>
   </rss>
   ```

---

## 架构设计

### 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                      RSSHub                              │
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │ YouTube 路由 │  │ B 站路由     │  │ 微博路由     │ ... │
│  │ (爬虫脚本)  │  │ (爬虫脚本)  │  │ (爬虫脚本)  │      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
│         ↓                ↓                ↓              │
│  ┌─────────────────────────────────────────────────┐    │
│  │              路由路由器 (Router)                 │    │
│  │    /youtube/channel/:id → 调用 YouTube 路由      │    │
│  │    /bilibili/user/video/:uid → 调用 B 站路由     │    │
│  └─────────────────────────────────────────────────┘    │
│                          ↓                               │
│  ┌─────────────────────────────────────────────────┐    │
│  │           RSS 模板引擎 (生成标准 RSS XML)        │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### 代码结构

```
RSSHub 代码结构：
lib/
  routes/
    youtube/          ← YouTube 相关路由
      channel.js
      user.js
    bilibili/         ← B 站相关路由
      user.js
      video.js
    weibo/            ← 微博相关路由
      user.js
      search.js
    javbus/           ← JavBus 路由
      index.js
    ...
```

---

## 技术实现

### 依赖的技术栈

| 库 | 用途 | 类似 Python 库 |
|------|------|---------------|
| `got` / `axios` | HTTP 请求 | `requests` |
| `cheerio` | HTML 解析 (类似 jQuery) | `BeautifulSoup` |
| `puppeteer` | 无头浏览器 (处理 JS 渲染) | `Selenium` |
| `crypto-js` | 加密/解密 | `pycryptodome` |

### 典型路由脚本示例

```javascript
// 文件：lib/routes/youtube/channel.js

const got = require('got');        // 第三方 HTTP 库
const cheerio = require('cheerio'); // 第三方 HTML 解析库

async function fetchChannelVideos(ctx) {
    const channelId = ctx.params.id;
    
    // 1. 用 got 发送 HTTP 请求
    const response = await got({
        method: 'get',
        url: `https://www.youtube.com/channel/${channelId}/videos`,
        headers: { 'User-Agent': 'Mozilla/5.0 ...' }
    });
    
    // 2. 用 cheerio 解析 HTML
    const $ = cheerio.load(response.body);
    
    // 3. 自己写的爬取逻辑
    const videos = [];
    $('.yt-lockup-video').each((index, element) => {
        videos.push({
            title: $(element).find('.yt-lockup-title a').text(),
            url: $(element).find('.yt-lockup-title a').attr('href'),
            thumbnail: $(element).find('img').attr('src'),
        });
    });
    
    return videos;
}

module.exports = fetchChannelVideos;
```

---

## 为什么能支持这么多平台？

### 1. 模块化设计

- **每个网站 = 一个独立爬虫脚本**
- 路由之间互不影响
- 易于维护和扩展

### 2. 社区驱动

- 开源项目，GitHub 上很火
- 几百个贡献者维护几百个路由
- 任何人可以提交新路由

### 3. 路由开发简单

写一个新路由只需要：
```javascript
router.get('/website/:type/:id', async (ctx) => {
    const data = await crawlWebsite(ctx.params.type, ctx.params.id);
    ctx.state.data = {
        title: '网站名称',
        item: data.map(item => ({
            title: item.title,
            link: item.url,
            description: item.content
        }))
    };
});
```

### 4. 统一输出格式

不管爬取什么网站，最终都输出**标准 RSS 格式**

---

## 爬虫方式

| 方式 | 说明 | 例子 |
|------|------|------|
| **官方 API** | 调用网站开放 API | YouTube API, Twitter API |
| **网页爬取** | 直接解析 HTML | JavBus, 新闻网站 |
| **RSS 桥接** | 转换现有 RSS | 一些博客 |
| **移动端 API** | 调用 App 接口 | 抖音，小红书 |

---

## 部署与资源占用

### 快速部署

```bash
# 最简单的方式（无缓存，适合测试）
docker run -d --name rsshub -p 1200:1200 diygod/rsshub

# 正式使用（加 Redis 缓存）
docker run -d --name rsshub \
  -p 1200:1200 \
  -e CACHE_TYPE=redis \
  -e REDIS_URL=redis://redis:6379 \
  diygod/rsshub

docker run -d --name redis redis:alpine
```

### 资源占用

| 资源 | 占用 | 说明 |
|------|------|------|
| **内存** | 150-300 MB | Node.js 应用，启动后相对稳定 |
| **CPU** | 几乎 0%（空闲时） | 有请求时才消耗 |
| **磁盘** | ~500 MB | 镜像 + 容器 + 依赖 |
| **网络** | 按请求量 | 每次查询都去目标网站爬取 |

### 有缓存后

- 相同请求直接返回缓存，不重复爬取
- CPU/网络消耗降低 80%+
- 内存占用略增（Redis 约 50-100 MB）

---

## 使用场景

### 监控订阅流程

```
┌─────────────────────────────────────────────────────────┐
│                   RSSHub Monitor Skill                   │
│                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌────────────┐ │
│  │  定时任务     │    │  对比逻辑     │    │  通知推送   │ │
│  │  (cron)     │───→│  (有新内容？) │───→│  (message)│ │
│  └──────────────┘    └──────────────┘    └────────────┘ │
│         ↓                                              │
│         ↓ 查询                                         │
│         ↓                                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │              RSSHub (localhost:1200)               │ │
│  │   /youtube/channel/xxx  → 实时爬取返回最新内容     │ │
│  │   /bilibili/user/video/xxx → 实时爬取返回最新内容  │ │
│  │   /javbus/en → 实时爬取返回最新内容                │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 常见路由示例

| 网站 | 路由格式 | 示例 |
|------|----------|------|
| YouTube | `/youtube/channel/:id` | `/youtube/channel/UCBJycsmduvYEL83R_U4JriQ` |
| B 站 | `/bilibili/user/video/:uid` | `/bilibili/user/video/123456` |
| 微博 | `/weibo/user/:uid` | `/weibo/user/1234567890` |
| JavBus | `/javbus/:lang` | `/javbus/en` |

---

## 关键优势

1. ✅ **模块化设计** — 每个网站独立，互不影响
2. ✅ **社区驱动** — 几百个贡献者维护几百个路由
3. ✅ **易于扩展** — 写新路由只需几十行代码
4. ✅ **统一输出** — 不管什么网站，都是标准 RSS

---

## 注意事项

### RSSHub 本身没有"订阅"功能

RSSHub 只是一个**按需生成器**：
- 你请求 → 它实时爬取返回
- 它不存储、不订阅、不推送

### "订阅"是监控工具做的事

```
定时检查 → 对比上次 → 发现新的 → 通知你
```

### 官方实例限制

- `rsshub.app` 仅用于测试目的
- 建议自建 RSSHub 用于稳定使用
- 官方逐步限制公共实例访问

---

## 相关链接

- **官网**: https://rsshub.app
- **GitHub**: https://github.com/DIYgod/RSSHub
- **文档**: https://docs.rsshub.app
- **路由列表**: https://docs.rsshub.app/routes

---

## 待办

- [ ] 部署自建 RSSHub 实例
- [ ] 编写 RSSHub 监控 Skill
- [ ] 配置定时任务检查更新
- [ ] 添加通知推送功能
