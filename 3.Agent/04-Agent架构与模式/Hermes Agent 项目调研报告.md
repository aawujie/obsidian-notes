# Hermes Agent 项目调研报告

> 调研时间：2026-04-15
> 项目地址：https://github.com/nousresearch/hermes-agent
> 官方文档：https://hermes-agent.nousresearch.com/docs/

---

## 一、项目概述

**Hermes Agent** 是由 **Nous Research** 开发的自改进型 AI Agent 框架。它是目前唯一具备内置学习循环的 Agent 系统，能够从经验中创建技能、在使用过程中改进技能、主动提示自己保存知识，并构建跨会话的用户画像模型。

### 核心理念

> "The agent that grows with you" —— 随你成长的 Agent

与传统 IDE 绑定的编程助手或单一 API 包装器不同，Hermes Agent 是一个**自主 Agent**，运行时间越长能力越强。它可以部署在 $5 的 VPS、GPU 集群或几乎零成本的 Serverless 基础设施上，用户可以通过 Telegram 等消息平台与它交互，而无需直接 SSH 到云服务器。

---

## 二、核心特性

### 1. 闭环学习系统（Closed Learning Loop）

| 特性                | 说明               |
| ----------------- | ---------------- |
| **Agent 策划的记忆**   | 周期性提示保存重要信息      |
| **自主技能创建**        | 完成复杂任务后自动生成技能    |
| **技能自我改进**        | 在使用过程中持续优化技能     |
| **FTS5 跨会话搜索**    | 结合 LLM 摘要实现跨会话回忆 |
| **Honcho 辩证用户建模** | 深度理解用户行为和偏好      |

### 2. 多平台支持（15+ 平台）

- **CLI**: 本地终端交互
- **消息平台**: Telegram、Discord、Slack、WhatsApp、Signal、Matrix、Mattermost
- **其他**: Email、SMS、DingTalk、Feishu、WeCom、BlueBubbles、Home Assistant

### 3. 多模型支持（无锁定）

支持任意模型，一键切换：

- **Nous Portal** (官方)
- **OpenRouter** (200+ 模型)
- **Xiaomi MiMo**
- **z.ai/GLM**
- **Kimi/Moonshot**
- **MiniMax**
- **Hugging Face**
- **OpenAI**
- **自定义端点**

切换命令：`hermes model` —— 无需修改代码，无供应商锁定。

### 4. 终端后端（6种部署方式）

| 后端          | 特点               |
| ----------- | ---------------- |
| Local       | 本地运行             |
| Docker      | 容器化部署            |
| SSH         | 远程 SSH 连接        |
| Daytona     | Serverless，空闲时休眠 |
| Singularity | HPC 环境           |
| Modal       | Serverless，按需唤醒  |

**Serverless 优势**: Daytona 和 Modal 支持环境休眠，空闲时几乎零成本。

### 5. 技能系统（Skills System）

兼容 [agentskills.io](https://agentskills.io) 开放标准：

- **渐进式披露**: 按需加载，节省 Token
- **Skill Hub**: 社区共享技能
- **自动创建**: Agent 从经验中创建技能
- **自我改进**: 使用过程中自动优化

**技能目录结构**:
```
~/.hermes/skills/
├── mlops/
│   ├── axolotl/
│   │   ├── SKILL.md      # 主说明文件（必需）
│   │   ├── references/   # 附加文档
│   │   ├── templates/    # 输出模板
│   │   ├── scripts/      # 辅助脚本
│   │   └── assets/       # 补充文件
│   └── vllm/
└── devops/
    └── deploy-k8s/
```

### 6. 记忆系统（Memory System）

两个核心记忆文件：

| 文件 | 用途 | 字符限制 |
|------|------|----------|
| `MEMORY.md` | Agent 个人笔记（环境、约定、经验） | 2,200 字符 |
| `USER.md` | 用户画像（偏好、沟通风格） | 1,375 字符 |

**特点**:
- 会话开始时注入系统提示
- Agent 自主管理（添加、替换、删除）
- 自动去重
- 安全扫描防止注入

### 7. 工具与工具集（47+ 工具）

- **完整 Web 控制**: 搜索、提取、浏览、视觉、图像生成、TTS
- **MCP 集成**: 连接任意 MCP 服务器扩展能力
- **Cron 调度**: 内置定时任务，支持任意平台推送
- **子 Agent**: 并行工作流，零上下文成本的多步管道

### 8. 语音模式（Voice Mode）

- 实时语音交互
- 支持 CLI、Telegram、Discord 语音频道
- 语音备忘录转录

---

## 三、与 OpenClaw 的关系

Hermes Agent 可以看作是 **OpenClaw 的演进版本**，由同一团队（Nous Research）开发。

### 迁移支持

Hermes 提供完整的 OpenClaw 迁移工具：

```bash
hermes claw migrate              # 交互式迁移（完整预设）
hermes claw migrate --dry-run    # 预览迁移内容
hermes claw migrate --preset user-data  # 仅迁移用户数据（不含密钥）
hermes claw migrate --overwrite  # 覆盖现有冲突
```

**迁移内容**:
- SOUL.md —— 人格文件
- Memories —— MEMORY.md 和 USER.md 条目
- Skills —— 用户创建的技能
- 命令白名单 —— 审批模式
- 消息设置 —— 平台配置、允许用户、工作目录
- API 密钥 —— 白名单密钥（Telegram、OpenRouter、OpenAI 等）
- TTS 资源 —— 工作区音频文件
- 工作区指令 —— AGENTS.md

---

## 四、技术架构

### 项目结构

```
hermes-agent/
├── hermes/              # 核心代码
│   ├── agent/          # Agent 循环、关键类
│   ├── tools/          # 工具实现
│   ├── skills/         # 技能系统
│   ├── memory/         # 记忆系统
│   └── gateway/        # 消息网关
├── scripts/            # 安装脚本
├── tests/              # 测试
├── docs/               # 文档
└── tinker-atropos/     # RL 训练环境（子模块）
```

### 关键组件

1. **Agent Loop**: 核心推理循环
2. **Tool System**: 工具调用和管理
3. **Skill Manager**: 技能加载和执行
4. **Memory Manager**: 记忆持久化
5. **Gateway**: 多平台消息路由
6. **Cron Scheduler**: 定时任务调度

### 研究特性

- **批量轨迹生成**: 用于训练数据收集
- **Atropos RL 环境**: 强化学习环境
- **轨迹压缩**: 用于训练下一代工具调用模型

---

## 五、安装与使用

### 快速安装（60秒）

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

**支持平台**:
- Linux
- macOS
- WSL2
- Android (Termux)

**注意**: Windows 原生不支持，需使用 WSL2。

### 启动命令

```bash
source ~/.bashrc  # 或 source ~/.zshrc
hermes            # 启动交互式 CLI
```

### 常用命令

| 命令 | 功能 |
|------|------|
| `hermes` | 启动交互式 CLI |
| `hermes model` | 选择 LLM 提供商和模型 |
| `hermes tools` | 配置启用的工具 |
| `hermes config set` | 设置配置值 |
| `hermes gateway` | 启动消息网关 |
| `hermes setup` | 运行完整设置向导 |
| `hermes update` | 更新到最新版本 |
| `hermes doctor` | 诊断问题 |

### CLI 快捷键

| 操作 | CLI | 消息平台 |
|------|-----|----------|
| 新会话 | `/new` 或 `/reset` | `/new` 或 `/reset` |
| 切换模型 | `/model [provider:model]` | `/model [provider:model]` |
| 设置人格 | `/personality [name]` | `/personality [name]` |
| 重试/撤销 | `/retry`, `/undo` | `/retry`, `/undo` |
| 压缩上下文 | `/compress` | `/compress` |
| 查看使用统计 | `/usage`, `/insights` | `/usage`, `/insights` |
| 浏览技能 | `/skills` | `/skills` |
| 中断工作 | `Ctrl+C` | `/stop` |

---

## 六、开发贡献

### 开发环境设置

```bash
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv venv --python 3.11
source venv/bin/activate
uv pip install -e ".[all,dev]"
python -m pytest tests/ -q
```

### RL 训练（可选）

```bash
git submodule update --init tinker-atropos
uv pip install -e "./tinker-atropos"
```

---

## 七、社区与资源

| 资源 | 链接 |
|------|------|
| 官方文档 | https://hermes-agent.nousresearch.com/docs/ |
| GitHub | https://github.com/NousResearch/hermes-agent |
| Discord | https://discord.gg/NousResearch |
| Skills Hub | https://agentskills.io |
| Issues | https://github.com/NousResearch/hermes-agent/issues |
| Discussions | https://github.com/NousResearch/hermes-agent/discussions |
| Nous Research | https://nousresearch.com |

---

## 八、优势与特点总结

### 相比其他 Agent 框架的优势

1. **真正的学习循环**: 不是简单的 RAG，而是 Agent 自主创建和改进技能
2. **跨平台统一**: 15+ 平台，单一网关进程
3. **模型无关**: 支持 200+ 模型，无供应商锁定
4. **Serverless 友好**: Daytona/Modal 支持，空闲零成本
5. **研究导向**: 内置 RL 训练、轨迹生成能力
6. **开放标准**: agentskills.io 兼容，技能可移植共享
7. **完整迁移路径**: OpenClaw 用户可无缝迁移

### 适用场景

- **个人助手**: 跨设备、跨平台的智能助手
- **开发工作流**: 代码审查、自动化任务、文档生成
- **研究实验**: RL 训练、Agent 行为研究
- **企业部署**: Serverless 部署，成本可控

---

## 九、与当前 OpenClaw 的对比

| 特性         | OpenClaw      | Hermes Agent            |
| ---------- | ------------- | ----------------------- |
| 开发团队       | Nous Research | Nous Research           |
| 学习循环       | 基础记忆          | 闭环学习 + 技能自改进            |
| 技能系统       | 有             | 更完善 + agentskills.io 标准 |
| 支持平台       | 较少            | 15+ 平台                  |
| 模型支持       | 有限            | 200+ 模型                 |
| Serverless | 不支持           | Daytona/Modal 支持        |
| 语音模式       | 有限            | 完整实时语音                  |
| RL 训练      | 无             | 内置 Atropos              |
| 迁移支持       | -             | 完整迁移工具                  |

---

## 十、结论与建议

Hermes Agent 代表了 AI Agent 框架的演进方向：

1. **从工具到伙伴**: 不仅是执行命令，而是持续学习和适应
2. **从单一到多元**: 支持更多平台、更多模型、更多部署方式
3. **从静态到动态**: 技能和自我改进机制让 Agent 越用越聪明

对于当前 OpenClaw 用户，建议：
- 关注 Hermes Agent 的发展
- 利用 `hermes claw migrate` 工具评估迁移成本
- 在新项目中尝试 Hermes Agent

---

*报告生成时间: 2026-04-15*
*调研工具: Web Fetch + Web Search*
