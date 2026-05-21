---
title: Text-to-CAD项目深度调研
type: research
created: 2026-05-21
updated: 2026-05-21
sources:
  - https://github.com/earthtojake/text-to-cad
  - https://www.cadskills.xyz
  - https://github.com/gumyr/build123d
  - https://www.skills.sh/
tags:
  - CAD
  - Agent
  - 3D建模
  - 机器人
  - build123d
  - OpenCascade
  - STEP
  - URDF
  - Agent-Skill
---

## 项目概述

**CAD Skills** — 一套面向 AI 编码 Agent（Codex、Claude Code 等）的 CAD/机器人/硬件设计技能集合。由 [@earthtojake](https://x.com/earthtojake) 开发，MIT 协议开源。

- 官网: [cadskills.xyz](https://www.cadskills.xyz)
- Demo: [demo.cadskills.xyz](https://demo.cadskills.xyz)
- 安装: `npx skills add earthtojake/text-to-cad`（通过 [skills.sh](https://www.skills.sh/) 分发）

## 核心能力

### 1. 自然语言 → 参数化 CAD
- 用户用自然语言描述零件/装配体需求
- Agent 生成 **build123d Python 源码**（而非直接生成 STEP）
- 通过 CLI 工具 `scripts/step` 运行生成器，输出 STEP/STL/3MF/GLB/DXF
- **关键设计原则**：源码是真理，STEP 是派生产物。修改源码后重新生成，不手动编辑 STEP

### 2. CAD Explorer — 浏览器内 3D 预览
- 基于 WebGL 的轻量级查看器（Vite + Three.js）
- 支持 `.step`、`.stp`、`.glb`、`.stl`、`.3mf`、`.dxf`、`.urdf`、`.srdf`、`.sdf`
- 支持快照渲染（headless screenshot）、剖面视图、线框模式
- 端口复用机制 `dev:ensure`：先扫描已有实例，复用而非新建

### 3. @cad 引用系统
- `scripts/inspect refs --facts --planes --positioning` 提取几何信息
- `@cad[...]` 引用供 Agent 做精确的后续编辑
- 支持 `measure`、`mate`、`frame`、`diff` 子命令进行几何验证

### 4. 机器人描述文件
- **URDF**: 机器人运动学描述（links, joints, limits, inertials）
- **SRDF**: MoveIt2 语义组、逆运动学、路径规划
- **SDF**: Gazebo/Ignition 仿真模型

### 5. 标准件目录 (step.parts)
- 托管的标准件 API：螺丝、螺母、垫圈、轴承、电机、连接器等
- 通过 `https://api.step.parts` 搜索和下载 STEP 文件
- 支持 SHA256 校验

## 技术栈

| 层级 | 技术 |
|------|------|
| CAD 内核 | [build123d](https://github.com/gumyr/build123d) (Python BREP建模) → OpenCascade (OCP) |
| 网格处理 | numpy, trimesh, vtk |
| DXF 导出 | ezdxf |
| 渲染查看器 | Vite + Three.js + React (CAD Explorer) |
| 文档站 | Next.js 16 + Tailwind CSS 4 + shadcn/ui |
| Python | 3.11+ |

## 架构设计

### Skills 目录结构

```
skills/
├── cad/              # 核心 CAD 技能
│   ├── SKILL.md      # Agent 指令 (规格 + 工作流)
│   ├── scripts/
│   │   ├── step/     # STEP 生成 CLI (Python)
│   │   ├── inspect/  # 几何检测 CLI
│   │   └── dxf/      # DXF 导出 CLI
│   └── references/   # 按需加载的参考文档
│       ├── build123d-modeling.md
│       ├── step-generation.md
│       ├── inspection-and-validation.md
│       ├── natural-language-specs.md
│       ├── render-review.md
│       ├── dxf.md
│       └── ...
├── render/           # 渲染/查看器技能
│   ├── SKILL.md
│   └── scripts/viewer/  # Vite + Three.js CAD Explorer
├── urdf/             # URDF 机器人描述
├── srdf/             # MoveIt2 SRDF 语义
├── sdf/              # SDFormat 仿真描述
├── step-parts/       # step.parts 标准件检索
└── sendcutsend/      # SendCutSend 钣金加工
```

### Agent 工作流

1. **Describe** → 用户描述零件/装配体需求
2. **Edit** → Agent 编写 build123d Python 源码
3. **Regenerate** → `scripts/step source.py` 生成 STEP + 侧车文件
4. **Inspect** → `scripts/inspect` 验证几何、提取 @cad 引用
5. **Render** → 自动启动/复用 CAD Explorer 返回预览链接
6. **Iterate** → 基于视觉反馈和几何验证修改源码 → 重新生成
7. **Commit** → 源码 + 生成物一起提交

### 关键设计决策

1. **STEP-first**: STEP 是主要 CAD 产物，STL/3MF/GLB/DXF 为次要
2. **Source-controlled geometry**: Python 源码入 Git，STEP 等二进制走 Git LFS
3. **Progressive references**: `SKILL.md` 定义触发条件，Agent 按需加载 reference 文档，避免上下文污染
4. **Harness pattern**: 提供 `harness/AGENTS.md` + `harness/CLAUDE.md` 模板，可复制到任何 CAD 项目使用
5. **不跑目录级操作**: 所有工具明确要求传入文件路径，禁止批量生成

## Benchmarks

内置 10 个标准测试用例，覆盖常见机械设计场景：

| # | 零件 | 复杂度 |
|---|------|--------|
| 1 | 矩形校准块 + 4孔 | 基础 |
| 2 | 圆形法兰 + 螺栓孔阵列 | 基础 |
| 3 | L型支架 + 角撑板 | 中等 |
| 4 | 阶梯轴 + 键槽 | 中等 |
| 5 | 开顶电子外壳 + 固定柱 | 中等 |
| 6 | 航空Clevis支架 + 减重孔 | 复杂 |
| 7 | 星形发动机气缸 + 散热片 | 复杂 |
| 8 | 离心叶轮 + 后弯叶片 | 复杂 |
| 9 | 螺旋楼梯 + 扶手 | 复杂 |
| 10 | 行星齿轮减速级 | 复杂装配 |

## 与类似项目的关系

| 项目 | 定位 | 对比 |
|------|------|------|
| [build123d](https://github.com/gumyr/build123d) | Python BREP CAD 库 | CAD Skills 的底层建模引擎 |
| [OpenCascade](https://dev.opencascade.org/) | C++ CAD 内核 | build123d/OCP 的上游 |
| [CadQuery](https://github.com/CadQuery/cadquery) | 另一个 Python CAD 框架 | 与 build123d 同生态，不同 API 风格 |
| [OpenSCAD](https://openscad.org/) | 脚本化 CSG 建模 | 不同的建模范式（CSG vs BREP） |

## 评价

### 优点
- **Agent-Native 设计**：不是给人类用的 CAD 工具，而是专门为 AI 编码 Agent 设计的工作流。每个 Skill 本质上是 Agent 的 "操作手册"，包含触发条件、工作流、非协商规则
- **源码可控**：Python 代码生成 CAD，diff 友好，版本控制友好
- **渐进式上下文加载**：reference 文件按需加载，避免一次性塞入大量文档
- **端到端闭环**：生成 → 验证 → 渲染 → 迭代，完整覆盖 CAD 开发循环
- **机器人全栈**：不只是几何建模，还覆盖 URDF/SRDF/SDF 机器人描述和 MoveIt2 集成

### 局限性
- **依赖 Agent 编码能力**：最终质量取决于 Agent 的 build123d Python 代码水平
- **BREP 建模门槛**：参数化 BREP 建模比 CSG 更强大但也更复杂，Agent 容易写出无效几何
- **LFS 依赖**：大文件依赖 Git LFS，国内网络环境可能拉取困难
- **无 GUI 编辑器**：纯代码驱动，不适合非程序员用户
- **社区生态早期**：2026 年新项目，社区和第三方 Skill 尚在起步

### 对 S1-Brain 的启示
- **Skill 分发模式**：通过 `npx skills add` 安装 Skill 包，这是 Agent 工具生态的新范式
- **Harness 模板化**：将 Agent 操作规则（AGENTS.md/CLAUDE.md）模板化并复用，可借鉴到本项目的 Agent 配置
- **Progressive Disclosure**：按需加载文档的策略，适合知识库较大的 Agent 项目