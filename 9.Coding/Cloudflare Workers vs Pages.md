# Cloudflare Workers vs Pages

## 一句话区别

| | Workers | Pages |
|---|---|---|
| **定位** | 运行代码的**计算服务** | 部署静态网站的**托管服务** |
| **类比** | 类似 AWS Lambda / Vercel Functions | 类似 Vercel / Netlify / GitHub Pages |
| **适合** | API、中间件、边缘逻辑 | 前端网站（React/Vue/静态页面） |

---

## Cloudflare Workers

- **本质**：运行在 Cloudflare 全球边缘节点的 **JavaScript 函数**
- **没有服务器**：你写一个函数，Cloudflare 在离用户最近的节点执行它
- **适合做什么**：
  - API 接口（REST / GraphQL）
  - 请求转发、A/B 测试
  - 认证鉴权中间件
  - 实时数据处理
  - 图片/内容的动态转换

```js
// Worker 示例：一个简单的 API
export default {
  async fetch(request) {
    return new Response(JSON.stringify({ hello: "world" }), {
      headers: { "Content-Type": "application/json" },
    });
  },
};
```

---

## Cloudflare Pages

- **本质**：托管**构建产物（静态文件）**的 CDN 服务
- **工作流程**：连接 GitHub → 自动构建 → 部署到全球 CDN
- **适合做什么**：
  - React / Vue / Next.js 等前端项目
  - 静态博客（Hugo / Astro）
  - 任何 `npm run build` 出来的网站

```
GitHub push → Cloudflare 自动运行 npm run build → 把 dist/ 部署到 CDN
```

- **Pages Functions**：Pages 也支持在 `functions/` 目录写后端函数，底层其实就是 Workers

---

## 对比总结

| 特性       | Workers    | Pages             |
| -------- | ---------- | ----------------- |
| 部署内容     | JS 代码（函数）  | 静态文件（HTML/CSS/JS） |
| 触发方式     | HTTP 请求时执行 | 用户访问时返回文件         |
| 构建步骤     | 不需要        | 需要（npm run build） |
| 自定义域名    | 支持         | 支持                |
| 免费额度     | 10万次/天     | 无限请求（带宽限制）        |
| Git 自动部署 | 需要配置       | 原生支持              |
| 后端能力     | 完整         | 有限（通过 Functions）  |

---

## 我的项目用哪个？

**前端（nest-wander-ui）→ Cloudflare Pages**
- Vite + React，`npm run build` 出 `dist/`，直接托管

**如果需要后端 API → Cloudflare Workers**
- 但我们的后端用的是 Supabase Edge Functions（基于 Deno），不需要额外的 Workers

---

## 类比记忆

```
Pages  ≈  Vercel / Netlify   → 放网站的地方
Workers ≈  AWS Lambda        → 跑代码的地方
```

> 简单说：**做网站用 Pages，做 API 用 Workers**。
