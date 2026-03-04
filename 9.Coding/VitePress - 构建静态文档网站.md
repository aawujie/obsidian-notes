# VitePress - 构建现代静态文档网站

## 📌 什么是 VitePress？

**VitePress** 是一个由 Vue.js 团队开发的**静态站点生成器 (SSG)**，专为技术文档、项目文档、个人博客等场景设计。

### 核心特点

| 特性 | 说明 |
|------|------|
| ⚡ **极速** | 基于 Vite 构建，热重载 (HMR) 速度极快 |
| 🎨 **简洁** | 默认主题美观，开箱即用 |
| 📝 **Markdown 优先** | 直接用 Markdown 写文档，支持 Vue 组件 |
| 🚀 **高性能** | 预渲染 + 客户端导航，加载速度快 |
| 🔧 **易部署** | 生成纯静态文件，可部署到任意静态托管 |

### 与同类工具对比

| 工具 | 特点 | 适用场景 |
|------|------|----------|
| **VitePress** | 轻量、快速、Vue 生态 | 技术文档、项目文档 |
| **Docusaurus** | 功能丰富、React 生态 | 大型文档站、博客 |
| **VuePress** | VitePress 前身，基于 Webpack | 旧项目维护 |
| **GitBook** | 商业化、协作功能 | 团队文档协作 |

---

## 🛠️ 快速开始

### 1. 初始化项目

```bash
# 创建项目目录
mkdir my-docs && cd my-docs

# 初始化 npm 项目
npm init -y

# 安装 VitePress
npm add -D vitepress
```

### 2. 创建目录结构

```
my-docs/
├── docs/
│   ├── .vitepress/
│   │   └── config.js    # 配置文件
│   ├── index.md         # 首页
│   └── guide/
│       └── intro.md     # 文档页面
├── package.json
└── README.md
```

### 3. 配置 VitePress

创建 `docs/.vitepress/config.js`：

```javascript
export default {
  title: '我的文档站',
  description: '使用 VitePress 构建的静态文档',
  
  themeConfig: {
    // 顶部导航
    nav: [
      { text: '首页', link: '/' },
      { text: '指南', link: '/guide/intro' },
    ],
    
    // 侧边栏
    sidebar: {
      '/guide/': [
        {
          text: '指南',
          items: [
            { text: '介绍', link: '/guide/intro' },
            { text: '快速开始', link: '/guide/quickstart' },
          ]
        }
      ]
    },
    
    // 社交链接
    socialLinks: [
      { icon: 'github', link: 'https://github.com/your-username/my-docs' }
    ]
  }
}
```

### 4. 编写文档

**首页** `docs/index.md`：

```markdown
---
layout: home
hero:
  name: 我的文档站
  text: 使用 VitePress 构建的现代化文档
  tagline: 快速、简洁、高性能
  actions:
    - theme: brand
      text: 快速开始
      link: /guide/intro
    - theme: alt
      text: GitHub
      link: https://github.com/your-username/my-docs
features:
  - title: ⚡ 极速开发
    details: 基于 Vite 的热重载，开发体验极佳
  - title: 📦 开箱即用
    details: 默认主题美观，无需额外配置
  - title: 🚀 高性能
    details: 预渲染 + 客户端导航，加载飞快
---
```

**文档页面** `docs/guide/intro.md`：

```markdown
# 介绍

欢迎来到我的文档站！

## 什么是 VitePress？

VitePress 是一个...

## 为什么选择它？

- 速度快
- 配置简单
- 支持 Vue 组件
```

### 5. 运行命令

在 `package.json` 中添加脚本：

```json
{
  "scripts": {
    "docs:dev": "vitepress dev docs",
    "docs:build": "vitepress build docs",
    "docs:preview": "vitepress preview docs"
  }
}
```

**启动开发服务器：**
```bash
npm run docs:dev
```
访问 `http://localhost:5173`

**构建生产版本：**
```bash
npm run docs:build
```
输出到 `docs/.vitepress/dist/`

---

## 🎨 高级功能

### 自定义主题

创建 `docs/.vitepress/theme/index.js`：

```javascript
import DefaultTheme from 'vitepress/theme'
import './custom.css'

export default {
  ...DefaultTheme,
  enhanceApp({ app }) {
    // 注册全局 Vue 组件
    // app.component('MyComponent', MyComponent)
  }
}
```

### 使用 Vue 组件

在 Markdown 中直接使用 Vue 组件：

```markdown
# 我的文档

<MyCustomComponent />

```vue
<script setup>
import { ref } from 'vue'
const count = ref(0)
</script>

<button @click="count++">点击 {{ count }}</button>
```
```

### 搜索功能

VitePress 内置本地搜索（无需额外配置）：

```javascript
// .vitepress/config.js
export default {
  themeConfig: {
    search: {
      provider: 'local'
    }
  }
}
```

### 多语言支持

```javascript
export default {
  locales: {
    root: {
      label: '中文',
      lang: 'zh-CN',
      title: '我的文档',
    },
    en: {
      label: 'English',
      lang: 'en',
      title: 'My Docs',
      link: '/en/'
    }
  }
}
```

---

## 🚀 部署方案

### GitHub Pages

```bash
# 安装部署工具
npm add -D gh-pages

# 添加部署脚本到 package.json
{
  "scripts": {
    "deploy": "npm run docs:build && gh-pages -d docs/.vitepress/dist"
  }
}

# 部署
npm run deploy
```

**GitHub Actions 自动部署** `.github/workflows/deploy.yml`：

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run docs:build
      - uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: docs/.vitepress/dist
```

### Vercel / Netlify

1. 连接 GitHub 仓库
2. 构建设置：
   - **Build Command:** `npm run docs:build`
   - **Output Directory:** `docs/.vitepress/dist`
3. 自动部署

### Docker 部署

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run docs:build
FROM nginx:alpine
COPY --from=0 /app/docs/.vitepress/dist /usr/share/nginx/html
```

---

## 📚 最佳实践

### 目录组织

```
docs/
├── .vitepress/          # 配置和主题
│   ├── config.js
│   ├── theme/
│   └── components/
├── guide/               # 使用指南
│   ├── intro.md
│   └── advanced.md
├── api/                 # API 参考
│   └── components.md
├── blog/                # 博客文章
│   └── 2024-01-01-post.md
└── index.md             # 首页
```

### 文档写作技巧

1. **使用 Frontmatter** 控制页面布局
2. **合理分节** 每页内容不宜过长
3. **添加代码示例** 用 ` ``` ` 包裹
4. **使用内部链接** `[](/path/to/page)`
5. **添加目录** 自动生成 TOC

### 性能优化

- 启用图片懒加载
- 压缩静态资源
- 使用 CDN 加载外部资源
- 合理拆分文档页面

---

## 🔗 相关资源

- **官方文档**: https://vitepress.dev
- **GitHub**: https://github.com/vuejs/vitepress
- **Vite**: https://vitejs.dev
- **Vue.js**: https://vuejs.org

---

## 💡 小结

VitePress 是构建技术文档的**最佳选择之一**：

✅ 开发体验极佳（热重载秒级响应）
✅ 配置简单，上手快
✅ 默认主题美观专业
✅ 性能优秀，SEO 友好
✅ 生态完善，社区活跃

**适合场景：**
- 开源项目文档
- 公司内部知识库
- 个人技术博客
- 产品使用手册

---

**创建日期**: 2026-03-04
**标签**: #VitePress #静态网站 #文档工具 #Vue #前端开发
