---
description: "Docker 镜像构建原理：从 Dockerfile 到镜像的完整流程，Builder、层缓存、BuildKit 核心概念。"
---
# Docker 打镜像原理

## 一、什么是"打镜像"

**打镜像** = 用 Dockerfile 作为"配方"，构建出可运行的 Docker 镜像（Image）的过程。

```bash
docker build -t my-app:1.0 .
#         │         │
#         │         └── 镜像名:标签
#         └── 构建命令
```

- **输入**：Dockerfile + 构建上下文（当前目录文件）
- **输出**：镜像（可被 `docker run` 运行）
- **执行者**：Builder（构建器）

---

## 二、构建流程总览

```
┌─────────────────────────────────────────────────────────────┐
│  docker build -t my-app:1.0 .                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  1. 发送构建上下文到 Docker 引擎                              │
│     (. 目录下的文件被打包上传)                                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  2. Builder 解析 Dockerfile                                  │
│     按指令顺序逐行执行                                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  3. 每条指令生成一层 (Layer)                                  │
│     FROM → 基础层 | RUN → 新层 | COPY → 新层 | ...            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  4. 层按顺序堆叠，形成只读镜像                                 │
│     镜像 = 多层只读文件系统的叠加                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  5. 打上标签 (my-app:1.0) 并保存到本地                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 三、Builder（构建器）是啥

**Builder** = 实际执行 `docker build` 的"引擎"。

### 两种常见 Builder

| Builder           | 说明                              | 特点              |
| ----------------- | ------------------------------- | --------------- |
| **default**       | 传统构建引擎                          | 稳定、兼容性好         |
| **desktop-linux** | Docker Desktop 默认，通常基于 BuildKit | 构建更快、支持并行、缓存更智能 |
|                   |                                 |                 |

### 查看和切换 Builder

```bash
# 查看当前 builder
docker buildx ls

# 使用 default builder
docker buildx use default

# 使用 desktop-linux（Docker Desktop 常见）
docker buildx use desktop-linux
```

### 打镜像时用哪个 Builder？

```
docker build
    │
    └── 使用当前选中的 Builder（Docker Desktop 设置里可见）
```

---

## 四、镜像 = 多层只读文件系统

### 分层结构

镜像由**多个只读层 (Layer)** 叠加而成，每层对应 Dockerfile 里的一条（或一组）指令。

```
┌─────────────────────────────────────┐
│  Layer 4: CMD ["node", "app.js"]     │  ← 最上层，定义启动命令
├─────────────────────────────────────┤
│  Layer 3: COPY . /app                │  ← 复制应用代码
├─────────────────────────────────────┤
│  Layer 2: RUN npm install            │  ← 安装依赖
├─────────────────────────────────────┤
│  Layer 1: FROM node:18-alpine        │  ← 基础镜像
└─────────────────────────────────────┘
```

### 为什么分层？

- **复用**：不同镜像可共享相同底层（如 `node:18-alpine`）
- **缓存**：某层未变化时，直接用缓存，不重算
- **增量**：只传输/存储变更的层，节省空间和时间

---

## 五、Dockerfile 与层的对应关系

### 会生成新层的指令

| 指令 | 作用 | 是否生成新层 |
|------|------|-------------|
| `FROM` | 指定基础镜像 | ✅ 复用基础镜像的层 |
| `RUN` | 执行命令 | ✅ 每一条 RUN 一层 |
| `COPY` / `ADD` | 复制文件 | ✅ |
| `WORKDIR` | 设置工作目录 | ✅（元数据变更） |

### 不单独生成层的指令（元数据）

| 指令 | 作用 |
|------|------|
| `ENV` | 环境变量 |
| `EXPOSE` | 声明端口 |
| `LABEL` | 标签 |
| `CMD` / `ENTRYPOINT` | 启动命令 |

这些会合并在上一条"生成层"的指令里，作为镜像元数据。

---

## 六、构建缓存原理

### 缓存规则

- 从第一条指令开始按顺序校验
- 某条指令的**输入**与上次构建一致 → 命中缓存，跳过执行
- 某条指令变化 → 该指令及之后所有指令的缓存失效，重新执行

### 示例

```dockerfile
FROM node:18-alpine      # ① 基础镜像不变 → 缓存
RUN npm install -g pnpm  # ② 命令不变 → 缓存
COPY package.json .      # ③ package.json 不变 → 缓存
RUN pnpm install         # ④ 依赖不变 → 缓存
COPY . .                 # ⑤ 代码变了！→ 从这里开始全部重算
RUN pnpm build           # ⑥ 重新执行
```

**优化技巧**：把变化频率低的放前面（如依赖安装），变化频繁的放后面（如源代码 `COPY`）。

---

## 七、BuildKit 简介（现代构建引擎）

Docker 18.09+ 支持 **BuildKit**，作为默认或可选构建引擎。

### BuildKit 的优势

| 特性 | 说明 |
|------|------|
| **并行构建** | 独立分支可并行执行 |
| **更好的缓存** | 内容寻址缓存，更精准 |
| **无缓存构建** | `--no-cache` 更彻底 |
| **多阶段构建** | 更高效地做多阶段 build |
| ** secrets 支持** | 构建时可安全传入密钥 |

### 启用 BuildKit

```bash
# 单次启用
DOCKER_BUILDKIT=1 docker build -t my-app .

# 默认启用（写入 ~/.docker/config.json 或 环境变量）
export DOCKER_BUILDKIT=1
```

---

## 八、多阶段构建 (Multi-stage)

一次 Dockerfile 中有多个 `FROM`，前几个阶段只用来构建，最后一个阶段才是最终镜像。

```dockerfile
# 阶段 1：构建
FROM node:18-alpine AS builder
WORKDIR /app
COPY . .
RUN npm install && npm run build

# 阶段 2：运行（只保留产物）
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

**好处**：
- 最终镜像不包含源码、构建工具
- 镜像体积更小，安全性更好

---

## 九、构建上下文 (Build Context)

`docker build` 最后一个参数（如 `.`）是**构建上下文**。

### 作用

- 把指定目录下的文件发送给 Docker 引擎
- Dockerfile 里的 `COPY` / `ADD` 只能访问上下文内的文件

### 注意事项

```
项目目录
├── src/
├── node_modules/   ← 若在 .dockerignore 中，不会发送
├── .git/           ← 同上
├── Dockerfile
└── ...
```

**建议**：用 `.dockerignore` 排除 `node_modules`、`.git` 等，加快构建、减小上下文。

---

## 十、常用命令速查

| 命令 | 说明 |
|------|------|
| `docker build -t name:tag .` | 构建并打标签 |
| `docker build --no-cache -t name:tag .` | 不使用缓存构建 |
| `docker buildx ls` | 列出 builders |
| `docker buildx use <name>` | 切换 builder |
| `docker history <image>` | 查看镜像各层 |
| `docker image inspect <image>` | 查看镜像详细信息 |

---

## 十一、一张图总结

```
Dockerfile + 构建上下文
         │
         ▼
    ┌─────────┐
    │ Builder │  ← 构建引擎（default / desktop-linux / BuildKit）
    └─────────┘
         │
         │  ① 解析 Dockerfile
         │  ② 按指令生成层
         │  ③ 利用缓存
         │  ④ 堆叠成镜像
         ▼
    ┌─────────┐
    │  Image  │  ← 多层只读文件系统
    └─────────┘
         │
         ▼
    docker run  ← 创建容器，加一层可写层运行
```

---

## 十二、延伸阅读

- [Docker 官方文档 - Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
- [BuildKit 文档](https://docs.docker.com/build/buildkit/)
- [多阶段构建最佳实践](https://docs.docker.com/build/building/multi-stage/)
