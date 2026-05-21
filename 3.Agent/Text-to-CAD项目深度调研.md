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

## 使用指南：Skill 如何与 Agent 协作

### Skill 机制原理

这套系统的核心设计是 **"Skill 即操作手册"**。每个 `SKILL.md` 文件本质上是写给 AI Agent 的指令文档，包含：

- **触发条件**（什么时候该用这个 Skill）
- **工作流步骤**（怎么做、按什么顺序做）
- **非协商规则**（绝对不能做的事）
- **Progressive references**（什么情况下加载哪些补充文档）

Agent 安装 Skill 后，当用户说"帮我画个法兰盘"，Agent 会：
1. 识别触发词 → 匹配到 `cad` skill
2. 加载 `skills/cad/SKILL.md` → 获取完整工作流
3. 按需加载 `references/build123d-modeling.md` 等参考文档
4. 写 build123d Python 代码 → 通过 CLI 工具生成 STEP
5. 自动渲染预览链接

### 当前环境配置

本机已安装完成，环境变量参考：

```bash
# Skill 定义目录
SKILL_DIR="$HOME/Documents/MyBrain/.agents/skills"

# Python CAD 环境（独立 venv，Python 3.13）
CAD_PYTHON="$HOME/Documents/MyBrain/.agents/cad-venv/bin/python"

# CAD Explorer 查看器
CAD_EXPLORER="$SKILL_DIR/render/scripts/viewer"
```

> Python 3.14 不兼容（OpenCascade 无 cp314 wheel），因此 CAD 环境使用 uv 下载的独立 Python 3.13.7。

### 完整工作流实操

以"生成一个 L 型支架"为例：

#### Step 1: 写 build123d Python 源码

```python
# l_bracket.py
from build123d import *

def gen_step():
    length, width = 80.0, 50.0
    base_thick, back_thick = 8.0, 8.0
    back_height = 50.0
    hole_dia = 6.0

    with BuildPart() as bracket:
        # 底板
        Box(length, width, base_thick)
        # 背板
        with Locations((0, width / 2 - back_thick / 2, back_height / 2)):
            Box(length, back_thick, back_height)
        # 底板安装孔 x2
        with Locations((-25, -10, 0), (25, -10, 0)):
            Cylinder(radius=hole_dia / 2, height=base_thick, mode=Mode.SUBTRACT)
        # 背板安装孔 x2
        with Locations((-25, width / 2, 30), (25, width / 2, 30)):
            Cylinder(radius=hole_dia / 2, height=back_thick,
                     rotation=(0, 90, 0), mode=Mode.SUBTRACT)

    return bracket.part

if __name__ == "__main__":
    export_step(gen_step(), "l_bracket.step")
```

#### Step 2: 用 Skill 工具生成 STEP

```bash
# 使用 cad skill 的 step CLI
$CAD_PYTHON $SKILL_DIR/cad/scripts/step/__main__.py l_bracket.py -o l_bracket.step

# 同时导出 STL 和 3MF（可选）
$CAD_PYTHON $SKILL_DIR/cad/scripts/step/__main__.py l_bracket.py \
    --stl l_bracket.stl --3mf l_bracket.3mf
```

输出：
- `l_bracket.step` — 主产物，BREP 精确几何
- `l_bracket.stl` / `l_bracket.3mf` — 3D 打印格式
- `.l_bracket.step.glb` — 隐藏 GLB 供 Explorer 使用
- `.l_bracket.step/` — 拓扑数据目录（topology.bin + topology.json）

#### Step 3: 启动 CAD Explorer 预览

```bash
# 自动检测并复用已有实例，没有则启动新的
npm --prefix $CAD_EXPLORER run dev:ensure -- \
    --workspace-root "$PWD" \
    --root-dir . \
    --file l_bracket.step
```

浏览器打开输出的 URL，可旋转/缩放/剖切三维模型。支持 `.step .stp .glb .stl .3mf .dxf .urdf .srdf .sdf`。

#### Step 4: 几何检测与 @cad 引用

```bash
# 获取模型的 @cad 引用（面/边 ID）
$CAD_PYTHON $SKILL_DIR/cad/scripts/inspect/__main__.py refs l_bracket.step \
    --facts --planes --positioning

# 精确测量
$CAD_PYTHON $SKILL_DIR/cad/scripts/inspect/__main__.py measure l_bracket.step \
    --from-face <face_id> --to-face <face_id>

# 两颗零件的配合检查
$CAD_PYTHON $SKILL_DIR/cad/scripts/inspect/__main__.py mate \
    part_a.step part_b.step --face-a <id> --face-b <id>

# 对比两次生成的差异
$CAD_PYTHON $SKILL_DIR/cad/scripts/inspect/__main__.py diff \
    old.step new.step
```

`@cad[...]` 引用是 Agent 实现精确迭代的关键——从 inspect 输出中复制引用 ID，下次修改可以直接定位到特定面/边。

#### Step 5: 渲染快照（自动化视觉验证）

```bash
$CAD_PYTHON $SKILL_DIR/render/scripts/snapshot \
    --input l_bracket.step \
    --output /tmp/bracket_review.png \
    --mode view \
    --theme technical \
    --camera iso \
    --view-labels
```

适合批量自动化：生成 → 快照 → 视觉 review → 修改源码 → 重新生成。

### 机器人相关工作流

#### URDF：生成机器人运动学描述

```bash
$CAD_PYTHON $SKILL_DIR/urdf/scripts/urdf robot.py -o robot.urdf
```

其中 `robot.py` 定义 `gen_urdf()` → 返回 URDF XML 字符串。自动做 XML 验证、关节树检查、inertial 合理性验证。

#### SRDF：MoveIt2 语义配置

```bash
$CAD_PYTHON $SKILL_DIR/srdf/scripts/srdf robot.py --urdf robot.urdf -o robot.srdf
```

可选启动 MoveIt2 服务器获得交互式 IK：
```bash
$SKILL_DIR/render/scripts/moveit2_server/run-moveit2-server.sh
```

#### step.parts：下载标准件

```bash
$CAD_PYTHON $SKILL_DIR/step-parts/scripts/download_step_part.py \
    "M3 socket head 12" --download --out-dir ./parts
```

直接输出标准 STEP 文件，可被装配体脚本 import 使用。

### Agent 视角：一次完整交互示例

当用户对 Claude Code 说"帮我生成一个 80mm 法兰盘，中心 30mm 孔，6 个 M6 螺栓孔"：

1. Agent 加载 `cad` skill → 识别为 STEP 生成任务
2. 读取 `natural-language-specs.md` → 从自然语言提取 CAD 参数
3. 读取 `build123d-modeling.md` → 获取 build123d API 参考
4. 写出 Python 源码 → 调用 Cylinder、Hole、fillet、polar array
5. 执行 `scripts/step flange.py -o flange.step`
6. 执行 `scripts/inspect refs flange.step --facts` → 验证尺寸和孔数
7. 调用 render skill → 返回 CAD Explorer 预览链接
8. 用户查看 3D 模型 → Agent 根据反馈调整

整个过程 Agent 自主完成，用户只需自然语言描述 + 浏览器确认。

### DXF 导出（SendCutSend 钣金加工）

```bash
$CAD_PYTHON $SKILL_DIR/cad/scripts/dxf/__main__.py part.step -o part.dxf \
    --projection top
```

结合 `sendcutsend` skill 可做预检报告，直接对接在线钣金加工。

### 故障排查

| 问题 | 解决 |
|------|------|
| Python 版本不匹配 | 确认使用 `.agents/cad-venv/bin/python`（3.13），不要用系统 python3（3.14） |
| Explorer 打不开 | 先运行 `npm --prefix ... run dev:ensure`，不要手动指定端口 |
| 生成 STEP 为空/无效 | 用 `scripts/inspect refs --facts` 检查；通常是 build123d 源码的布尔运算或选择器出错 |
| STL/3MF 导出失败 | 部分几何需要先 mesh 化，使用 `trimesh` 做二次处理 |

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