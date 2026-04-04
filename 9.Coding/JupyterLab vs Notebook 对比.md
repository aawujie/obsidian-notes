# JupyterLab vs Jupyter Notebook 对比

> 核心区别：**Notebook 是单文档编辑器，JupyterLab 是完整的 IDE 工作区**

---

## 快速对比表

| 维度 | Jupyter Notebook | JupyterLab |
|------|------------------|------------|
| **定位** | 经典笔记本界面 | 下一代 IDE 式工作区 |
| **界面** | 单文档标签页 | 多面板、可分屏、可拖拽 |
| **扩展性** | 有限 | 插件系统丰富 |
| **文件管理** | 基础列表 | 侧边栏文件浏览器 |
| **终端** | ❌ 无 | ✅ 内置终端 |
| **多文档协作** | 困难 | 原生支持（并排查看） |
| **官方状态** | 维护模式 | 主推方向 |

---

## Jupyter Notebook（经典版）

### 特点
- 单一 `.ipynb` 文件界面
- 简单、轻量、启动快
- 每个笔记本独立浏览器标签页

### 适用场景
- ✅ 快速验证代码片段
- ✅ 教学演示（界面简洁）
- ✅ 简单数据分析
- ✅ 临时探索性工作

### 局限
- ❌ 一次只能专注一个笔记本
- ❌ 文件管理靠浏览器标签切换
- ❌ 无法分屏对比多个文件
- ❌ 无内置终端

---

## JupyterLab（现代化 IDE）

### 核心功能

#### 1. 多面板布局
- 同时打开多个 notebook、文件、终端
- 自由拖拽排列
- 支持左右/上下分屏

#### 2. 侧边栏工具
- **文件浏览器**：项目管理
- **运行中内核**：监控会话
- **命令面板**：快速搜索命令
- **Git**：版本控制（需插件）

#### 3. 内置终端
- 直接运行 shell 命令
- 无需额外开终端窗口
- 支持多个终端标签

#### 4. 文件编辑器
- 支持 `.py`、`.md`、`.json` 等语法高亮
- 可直接编辑非 notebook 文件

#### 5. 插件生态
- Debugger（断点调试）
- Git 集成
- LaTeX 公式预览
- 目录导航
- 代码格式化工具

### 适用场景
- ✅ 复杂项目开发
- ✅ 多文件协作（notebook + 数据 + 脚本）
- ✅ 需要终端配合的工作流
- ✅ 生产环境开发
- ✅ 长期替代传统 IDE

---

## 启动命令

```bash
# 启动经典 Notebook
jupyter notebook
# 默认端口：8888

# 启动 JupyterLab
jupyter lab
# 默认端口：8888（可配置）
```

### 常用配置

```bash
# 指定端口
jupyter lab --port=9999

# 允许远程访问
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser

# 生成配置文件
jupyter lab --generate-config
# 配置文件位置：~/.jupyter/jupyter_lab_config.py
```

---

## 安装与升级

```bash
# 安装 JupyterLab
pip install jupyterlab

# 安装经典 Notebook
pip install notebook

# 升级到最新版
pip install -U jupyterlab notebook

# 查看版本
jupyter --version
```

---

## 使用建议

| 你的需求 | 推荐选择 |
|----------|----------|
| 新手入门学习 | Notebook（界面简单） |
| 日常数据分析 | JupyterLab |
| 机器学习项目开发 | JupyterLab |
| 教学/培训演示 | Notebook |
| 需要 Git 版本控制 | JupyterLab + Git 插件 |
| 需要调试代码 | JupyterLab + Debugger 插件 |
| 服务器远程开发 | JupyterLab（支持多会话） |

---

## 插件推荐（JupyterLab）

| 插件 | 功能 |
|------|------|
| `@jupyterlab/git` | Git 版本控制 |
| `@jupyterlab/debugger` | 断点调试 |
| `jupyterlab-toc` | 目录导航 |
| `jupyterlab-code-formatter` | 代码格式化（Black/isort） |
| `@jupyterlab/latex` | LaTeX 公式预览 |

安装示例：
```bash
jupyter labextension install @jupyterlab/git
```

---

## 迁移建议

如果你现在用 Notebook：

1. **直接尝试 Lab**：界面相似，上手成本低
2. **保留 Notebook**：某些旧插件可能不兼容 Lab
3. **逐步迁移**：新项目用 Lab，旧项目慢慢转

> 💡 **趋势**：Jupyter 官方已明确 JupyterLab 是未来方向，Notebook 进入维护模式。

---

## 一句话总结

> **Notebook ≈ 记事本，JupyterLab ≈ VS Code** —— 前者是单文档编辑器，后者是完整 IDE 工作区。

**建议**：新项目直接用 JupyterLab，老项目逐步迁移。

---

**创建时间**:: 2026-04-04
**更新时间**:: 2026-04-04
**标签**:: #Python #Jupyter #开发工具 #数据科学 #IDE
