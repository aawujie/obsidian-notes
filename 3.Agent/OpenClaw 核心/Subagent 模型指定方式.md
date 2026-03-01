# Subagent 模型指定方式

> 创建日期:: 2026-02-27
> 标签:: #OpenClaw #SubAgent #模型配置 #成本优化

---

## 🎯 核心结论

主 Agent 创建 Subagent 时，有 **3 种指定模型的方式**，优先级从高到低：

```
sessions_spawn 显式指定 model 参数  ← 最高优先级（动态覆盖）
         ↓
agents.list[].subagents.model       ← 父 agent 专属配置
         ↓
agents.defaults.subagents.model     ← 全局默认配置
         ↓
继承父 agent 当前模型               ← 兜底（无配置时）
```

---

## 1️⃣ 方式一：sessions_spawn 工具调用

**优先级：⭐⭐⭐ 最高**

当主 Agent 通过 `sessions_spawn` 工具创建子 agent 时，可以直接在参数中指定 `model`。

### 工具调用示例

```json
{
  "tool": "sessions_spawn",
  "params": {
    "task": "读取 /Users/apple/code/project 的所有.ts 文件并总结架构",
    "model": "bailian/qwen-plus",  // ← 直接指定模型
    "label": "代码分析",
    "runTimeoutSeconds": 600
  }
}
```

### 可用参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task` | string | ✅ | 子 agent 的任务描述 |
| `model` | string | ❌ | 覆盖默认模型 |
| `thinking` | string | ❌ | 思考级别 (low/medium/high) |
| `agentId` | string | ❌ | 指定子 agent 的 agent id |
| `label` | string | ❌ | 任务标签（用于标识） |
| `runTimeoutSeconds` | number | ❌ | 运行超时（秒） |
| `mode` | "run"\|"session" | ❌ | 运行模式 |
| `thread` | boolean | ❌ | 是否绑定线程 |

### 模型值格式

```javascript
"bailian/qwen-plus"              // 完整 provider/model 格式
"qwen-plus"                      // 仅 model 名（使用默认 provider）
"claude-sonnet-4-5-20250929"     // Claude 模型
"bge-m3"                         // Embedding 模型
```

### 完整工具调用示例

```typescript
// 复杂任务 - 用高性能模型
sessions_spawn({
  task: "重构认证模块，使用 JWT 替代 Session",
  model: "claude-sonnet-4-5-20250929",
  thinking: "high",
  runTimeoutSeconds: 1800
})

// 简单任务 - 用便宜模型
sessions_spawn({
  task: "把所有.md 文件转成.pdf",
  model: "bailian/qwen-plus",
  thinking: "low",
  runTimeoutSeconds: 300
})
```

---

## 2️⃣ 方式二：父 Agent 专属配置

**优先级：⭐⭐ 中等**

在 `openclaw.json` 中为特定 agent 配置其子 agent 的默认模型。

### 配置结构

```json5
{
  "agents": {
    "list": [
      {
        "id": "main",
        "name": "主 Agent",
        "model": { "primary": "bailian/qwen-max" },
        
        // ← 父 agent 专属子 agent 配置
        "subagents": {
          "model": {
            "primary": "bailian/qwen-plus"
          },
          "thinking": "low",
          "runTimeoutSeconds": 600
        }
      },
      
      {
        "id": "code",
        "name": "代码专家",
        "model": { "primary": "claude-sonnet-4-5-20250929" },
        
        // ← 代码 agent 的子 agent 用更便宜的模型
        "subagents": {
          "model": {
            "primary": "claude-haiku-3-5"
          }
        }
      }
    ]
  }
}
```

### 效果

| 父 Agent | 子 Agent 默认模型 | 说明 |
|----------|------------------|------|
| `main` | `qwen-plus` | 中等性能，平衡成本 |
| `code` | `haiku-3-5` | 便宜 70%，适合简单任务 |

### 适用场景

- 不同 agent 有不同成本预算
- 代码 agent 的子任务通常较简单 → 用便宜模型
- 主 agent 的子任务较复杂 → 用中等模型

---

## 3️⃣ 方式三：全局默认配置

**优先级：⭐ 基础**

为所有 agent 设置统一的子 agent 默认模型。

### 配置结构

```json5
{
  "agents": {
    "defaults": {
      "subagents": {
        // 全局子 agent 默认模型
        "model": {
          "primary": "bailian/qwen-plus"
        },
        
        // 可选：全局思考级别
        "thinking": "low",
        
        // 可选：全局超时
        "runTimeoutSeconds": 600,
        
        // 可选：最大嵌套深度
        "maxSpawnDepth": 2,
        
        // 可选：并发限制
        "maxConcurrent": 8,
        
        // 可选：每个 agent 最大子 agent 数
        "maxChildrenPerAgent": 5
      }
    }
  }
}
```

### 适用场景

- 统一成本控制
- 所有子 agent 任务类型相似
- 初期配置，后续按需覆盖

---

## 📋 完整配置示例

### 成本优化策略

```json5
{
  "agents": {
    // ========== 全局默认 ==========
    "defaults": {
      "subagents": {
        // 子 agent 统一用便宜模型，降低 60-70% 成本
        "model": { 
          "primary": "bailian/qwen-plus"
        },
        "thinking": "low",
        "runTimeoutSeconds": 600
      }
    },
    
    "list": [
      // ========== 主 Agent ==========
      {
        "id": "main",
        "name": "主 Agent",
        // 主 agent 自己用高性能模型
        "model": { "primary": "bailian/qwen-max" },
        // 子 agent 用中等模型（覆盖全局默认）
        "subagents": {
          "model": { "primary": "bailian/qwen-plus" }
        }
      },
      
      // ========== 代码专家 ==========
      {
        "id": "code",
        "name": "代码专家",
        // 代码 agent 用高性能模型
        "model": { "primary": "claude-sonnet-4-5-20250929" },
        // 但它的子 agent 用最便宜的（代码任务多且简单）
        "subagents": {
          "model": { "primary": "claude-haiku-3-5" }
        },
        "skills": ["coding-agent", "github", "tmux"]
      },
      
      // ========== 写作专家 ==========
      {
        "id": "write",
        "name": "写作专家",
        "model": { "primary": "claude-sonnet-4-5-20250929" },
        // 写作子任务也需要高质量 → 用中等模型
        "subagents": {
          "model": { "primary": "claude-haiku-3-5" }
        }
      }
    ]
  }
}
```

---

## 🛠️ 用户命令行调用

用户也可以通过 `/subagents spawn` 命令直接指定模型：

### 基本语法

```bash
/subagents spawn <agentId> <task> [--model <model>] [--thinking <level>]
```

### 示例

```bash
# 指定模型
/subagents spawn code "分析项目结构" --model bailian/qwen-plus

# 指定思考级别
/subagents spawn code "写单元测试" --model claude-haiku --thinking low

# 完整参数
/subagents spawn code "重构认证模块" \
  --model claude-sonnet-4-5-20250929 \
  --thinking high
```

---

## 📊 优先级测试

### 场景：main agent 创建子 agent

| 配置层级 | 设置值 | 最终使用 |
|----------|--------|----------|
| sessions_spawn.model | `"qwen-plus"` | ✅ **qwen-plus** |
| agents.list[main].subagents.model | `"haiku"` | ❌ 被覆盖 |
| agents.defaults.subagents.model | `"sonnet"` | ❌ 被覆盖 |
| 父 agent 当前模型 | `"qwen-max"` | ❌ 被覆盖 |

### 场景：无显式指定

| 配置层级 | 设置值 | 最终使用 |
|----------|--------|----------|
| sessions_spawn.model | 未指定 | - |
| agents.list[main].subagents.model | `"qwen-plus"` | ✅ **qwen-plus** |
| agents.defaults.subagents.model | `"haiku"` | ❌ 被覆盖 |
| 父 agent 当前模型 | `"qwen-max"` | ❌ 被覆盖 |

### 场景：无任何配置

| 配置层级 | 设置值 | 最终使用 |
|----------|--------|----------|
| sessions_spawn.model | 未指定 | - |
| agents.list[].subagents.model | 未配置 | - |
| agents.defaults.subagents.model | 未配置 | - |
| 父 agent 当前模型 | `"qwen-max"` | ✅ **继承 qwen-max** |

---

## 📚 官方推荐配置方法

### 官方文档建议

根据 OpenClaw 官方文档，推荐的配置策略是：

> **Cost note**: each sub-agent has its **own** context and token usage. For heavy or repetitive tasks, set a cheaper model for sub-agents and keep your main agent on a higher-quality model.
> You can configure this via `agents.defaults.subagents.model` or per-agent overrides.

**核心原则**：
1. 主 agent 用高质量模型（保证回复质量）
2. 子 agent 用便宜模型（降低成本 60-70%）
3. 通过配置实现，无需手动选择

---

### 官方推荐配置结构

```json5
{
  "agents": {
    // ========== 第一步：全局默认（必须） ==========
    "defaults": {
      "subagents": {
        // 所有子 agent 的默认模型（推荐用便宜模型）
        "model": {
          "primary": "claude-haiku-3-5"
        },
        // 可选：思考级别
        "thinking": "low",
        // 可选：运行超时
        "runTimeoutSeconds": 600,
        // 可选：并发限制
        "maxConcurrent": 8
      }
    },
    
    // ========== 第二步：按需覆盖（可选） ==========
    "list": [
      {
        "id": "main",
        "name": "主 Agent",
        // 主 agent 用高性能模型
        "model": { "primary": "claude-sonnet-4-5-20250929" }
        // 子 agent 继承全局默认（haiku）
      },
      {
        "id": "code",
        "name": "代码专家",
        // 代码 agent 用高性能
        "model": { "primary": "claude-sonnet-4-5-20250929" },
        // 可选：为特定 agent 覆盖子 agent 模型
        "subagents": {
          "model": { "primary": "claude-haiku-3-5" }
        }
      }
    ]
  }
}
```

---

## 💡 最佳实践

### 1. 成本优化策略

```json5
{
  "agents": {
    "defaults": {
      "subagents": {
        // 子 agent 默认用便宜模型
        "model": { "primary": "bailian/qwen-plus" },
        "thinking": "low"
      }
    },
    "list": [
      {
        "id": "main",
        // 主 agent 用高性能
        "model": { "primary": "bailian/qwen-max" }
      },
      {
        "id": "code",
        // 代码 agent 用高性能
        "model": { "primary": "claude-sonnet-4-5-20250929" },
        // 子 agent 用便宜 70% 的 haiku
        "subagents": { "model": { "primary": "claude-haiku-3-5" } }
      }
    ]
  }
}
```

**效果**：
- 主对话：高质量回复
- 子任务：低成本执行
- 整体成本降低 60-70%

---

### 2. 任务类型匹配

| 任务类型 | 推荐模型 | 配置方式 | 原因 |
|----------|----------|----------|------|
| 代码分析/架构设计 | Sonnet/Qwen-Max | sessions_spawn 显式指定 | 需要深度理解 |
| 文件读取/格式转换 | Haiku/Qwen-Plus | 配置默认 | 简单重复任务 |
| 资料搜索/整理 | Haiku | 配置默认 | 信息提取为主 |
| 复杂调试 | Sonnet | sessions_spawn 显式指定 | 需要推理能力 |
| 单元测试生成 | Haiku | 配置默认 | 模式化任务 |
| 文档编写 | Sonnet | sessions_spawn 显式指定 | 需要语言质量 |

---

### 3. 完整配置示例（可直接套用）

#### 示例 1：单 Agent + 全局默认（最简单）

```json5
{
  "agents": {
    "defaults": {
      "subagents": {
        "model": { "primary": "bailian/qwen-plus" }
      }
    },
    "list": [
      {
        "id": "main",
        "model": { "primary": "bailian/qwen-max" }
      }
    ]
  }
}
```

**适用**：个人使用，单一 agent

---

#### 示例 2：多 Agent + 分别配置（推荐）

```json5
{
  "agents": {
    "defaults": {
      "subagents": {
        "model": { "primary": "bailian/qwen-plus" }
      }
    },
    "list": [
      {
        "id": "main",
        "name": "主 Agent",
        "model": { "primary": "bailian/qwen-max" }
      },
      {
        "id": "code",
        "name": "代码专家",
        "model": { "primary": "claude-sonnet-4-5-20250929" },
        "subagents": { "model": { "primary": "claude-haiku-3-5" } }
      },
      {
        "id": "write",
        "name": "写作专家",
        "model": { "primary": "claude-sonnet-4-5-20250929" },
        "subagents": { "model": { "primary": "claude-haiku-3-5" } }
      }
    ]
  }
}
```

**适用**：多 agent 协作，不同领域用不同模型

---

#### 示例 3：极致成本优化

```json5
{
  "agents": {
    "defaults": {
      "subagents": {
        "model": { "primary": "bailian/qwen-light" },  // 最便宜
        "thinking": "low",
        "runTimeoutSeconds": 300
      }
    },
    "list": [
      {
        "id": "main",
        "model": { "primary": "bailian/qwen-max" },
        "subagents": {
          "model": { "primary": "bailian/qwen-light" }
        }
      }
    ]
  }
}
```

**适用**：预算有限，子任务多为简单操作

---

#### 示例 4：高性能优先

```json5
{
  "agents": {
    "defaults": {
      "subagents": {
        "model": { "primary": "claude-sonnet-4-5-20250929" },
        "thinking": "medium",
        "runTimeoutSeconds": 1200
      }
    },
    "list": [
      {
        "id": "main",
        "model": { "primary": "claude-sonnet-4-5-20250929" }
      },
      {
        "id": "research",
        "name": "研究助手",
        "model": { "primary": "claude-sonnet-4-5-20250929" },
        "subagents": {
          "model": { "primary": "claude-sonnet-4-5-20250929" }  // 子任务也用高性能
        }
      }
    ]
  }
}
```

**适用**：研究/分析任务为主，质量优先于成本

---

### 3. 动态选择策略

在主 agent 的 SOUL.md 或 AGENTS.md 中添加指导：

```markdown
## Subagent 模型选择原则

当使用 sessions_spawn 创建子 agent 时：

### 用高性能模型 (Sonnet/Qwen-Max)
- 需要理解复杂业务逻辑
- 涉及架构决策
- 需要创造性解决方案
- 调试疑难问题

### 用中等模型 (Qwen-Plus)
- 代码重构
- 文档整理
- 常规分析任务

### 用便宜模型 (Haiku/Qwen-Light)
- 文件读取/转换
- 格式化处理
- 批量重复任务
- 简单信息提取
```

---

## 🔍 验证配置

### 查看当前配置

```bash
# 查看 subagents 配置
openclaw config show | grep -A 20 "subagents"

# 查看完整 agents 配置
openclaw config show | jq '.agents'
```

### 测试 Spawn

```bash
# 测试子 agent 创建
/subagents spawn main "测试任务" --model bailian/qwen-plus

# 查看子 agent 信息
/subagents info <run-id>

# 查看子 agent 使用的模型
/subagents log <run-id> | grep -i "model"
```

### 检查实际使用

```bash
# 查看最近的子 agent 运行记录
ls -lt ~/.openclaw/agents/main/sessions/ | head -10

# 查看会话详情（包含模型信息）
cat ~/.openclaw/agents/main/sessions/<session-id>.jsonl | grep -i "model"
```

---

## 📈 成本对比

### 场景：每日 10 个子 agent 任务

| 方案 | 模型 | Token/任务 | 成本/任务 | 成本/天 | 成本/月 |
|------|------|------------|-----------|---------|---------|
| 全用 Sonnet | Sonnet | 10K | $0.03 | $0.30 | $9.00 |
| 全用 Haiku | Haiku | 10K | $0.005 | $0.05 | $1.50 |
| **混合策略** | 按需 | - | - | **$0.12** | **$3.60** |

**混合策略**：
- 2 个复杂任务 → Sonnet ($0.06)
- 8 个简单任务 → Haiku ($0.04)
- **节省 60%**

---

## ⚠️ 注意事项

### 1. 模型值验证

```json5
{
  "model": "invalid-model-name"  // ❌ 无效模型
}
```

**结果**：
- 不会报错
- 会回退到默认模型
- 在 tool result 中会有 warning

### 2. Provider 配置

确保模型对应的 provider 已配置：

```json5
{
  "models": {
    "providers": {
      "bailian": {
        "apiKey": "sk-xxx"  // ← 必须配置
      },
      "anthropic": {
        "apiKey": "sk-ant-xxx"  // ← 必须配置
      }
    }
  }
}
```

### 3. 嵌套深度限制

```json5
{
  "agents": {
    "defaults": {
      "subagents": {
        "maxSpawnDepth": 2  // 默认 1，最大 5
      }
    }
  }
}
```

- `maxSpawnDepth: 1` → 子 agent 不能 spawn 子子 agent
- `maxSpawnDepth: 2` → 允许 orchestrator 模式

---

## 🔗 相关文档

- [OpenClaw Sub-Agents](/tools/subagents)
- [Configuration Reference](/gateway/configuration-reference)
- [Agent Workspace](/concepts/agent-workspace)
- [Session Management](/reference/session-management-compaction)

---

## ⚠️ 重要澄清：不会自动根据意图选择

### ❌ 系统不会自动选择模型

OpenClaw **不会**根据任务复杂度或意图自动切换子 agent 模型：

```
用户请求
   ↓
主 Agent 决定创建子 agent
   ↓
使用配置的默认模型 (agents.defaults.subagents.model)
   ↓
❌ 不会分析任务类型
❌ 不会根据复杂度选择
❌ 不会根据意图切换模型
```

### 实际行为

| 配置 | 任务类型 | 实际使用模型 |
|------|----------|--------------|
| `"model": "qwen-plus"` | "读取这个文件" | qwen-plus |
| `"model": "qwen-plus"` | "重构整个架构" | qwen-plus |
| `"model": "qwen-plus"` | "写个 hello world" | qwen-plus |

**结论**：模型选择是**静态配置**，不是**动态智能**。

---

### ✅ 如何实现"智能选择"效果

#### 方式 1：在 SOUL.md/AGENTS.md 中指导

```markdown
## Subagent 模型选择指南

当你需要创建子 agent 时，根据任务类型选择模型：

### 复杂任务 → 用高性能模型
sessions_spawn({
  task: "...",
  model: "claude-sonnet-4-5-20250929"
})
```

**适用场景**：
- 架构设计
- 复杂调试
- 代码重构
- 需要创造性解决方案

### 简单任务 → 用便宜模型
sessions_spawn({
  task: "...",
  model: "claude-haiku-3-5"
})
```

**适用场景**：
- 文件读取
- 格式转换
- 批量处理
- 信息提取
```

#### 方式 2：配置多个专用 Agent

```json5
{
  "agents": {
    "list": [
      {
        "id": "code-heavy",
        "subagents": { "model": { "primary": "haiku" } }  // 便宜
      },
      {
        "id": "code-smart",
        "subagents": { "model": { "primary": "sonnet" } }  // 高性能
      }
    ]
  }
}
```

**使用方式**：主 agent 判断任务类型 → spawn 到对应 agent

#### 方式 3：Skill 指导

创建 `skills/subagent-model-selector/SKILL.md`，定义任务类型到模型的映射规则。

---

### 🔍 验证方法

```bash
# 创建两个不同类型的子 agent 任务
/subagents spawn main "读取 package.json"  # 简单任务
/subagents spawn main "重构整个项目架构"   # 复杂任务

# 查看实际使用的模型
/subagents info <run-id>
```

如果两个任务用的模型相同 → **证实不会自动选择**

---

## 💭 总结

| 方式 | 优先级 | 适用场景 | 灵活性 |
|------|--------|----------|--------|
| sessions_spawn.model | ⭐⭐⭐ | 动态任务，按需选择 | 最高 |
| agents.list[].subagents.model | ⭐⭐ | 固定 agent 的固定策略 | 中等 |
| agents.defaults.subagents.model | ⭐ | 统一成本控制 | 较低 |
| 继承父 agent | - | 无配置时的兜底 | - |

**推荐做法**：
1. 配置全局默认（成本控制）
2. 为特殊 agent 配置专属模型（如代码 agent 用便宜模型）
3. 复杂任务在 sessions_spawn 中显式指定（灵活性）
4. **在 SOUL.md 中添加模型选择指导**（实现"智能"效果）
