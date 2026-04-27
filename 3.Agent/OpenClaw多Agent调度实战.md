# OpenClaw 多Agent调度实战：量化交易闭环

> ⚠️ 说明：本文使用 OpenClaw 原生子Agent（`sessions_spawn runtime=subagent`），不是 Claude Code。如需真CC多Agent调度，需配合 ACP 插件或 exec 并行 + 文件通信。

## 一句话

用 OpenClaw 的 `sessions_spawn` + `sessions_send` 调度多个子Agent，实现"选股→择时→风控→决策"的完整交易闭环。三个Agent独立判断互不串通，主Agent汇总拍板。

---

## 架构（OpenClaw 原生子Agent方案）

```
主Agent（OpenClaw会话）
  │
  ├── sessions_spawn → 选股子Agent（OpenClaw原生）
  │       ← sessions_send "请选出top 10"
  │       → "688506, 688336, ..."
  │
  ├── sessions_spawn → 择时子Agent（OpenClaw原生）
  │       ← sessions_send "能开仓吗？"
  │       → "能开仓 — 均线多头排列..."
  │
  └── sessions_spawn → 风控子Agent（OpenClaw原生）
          ← sessions_send "风险评估？"
          → "半仓 — 高beta需留现金..."
```

## 替代方案（真Claude Code多Agent，文件通信）

由于 ACP 插件未安装，无法通过 sessions_spawn 直接开 CC 会话。替代方案是用 exec 并行启动多个 CC，通过文件互传：

```
exec bg → CC1: claude --print "选股,结果写到 /tmp/agent_picks.txt"
exec bg → CC2: claude --print "读 /tmp/agent_picks.txt,择时,写到 /tmp/agent_timing.txt"
exec bg → CC3: claude --print "读 /tmp/agent_picks.txt,风控,写到 /tmp/agent_risk.txt"
# 主Agent汇总三个文件做最终决策
```

文件通信的缺点：只能串行或预定义依赖，不像 sessions_send 可以灵活实时通信。

**核心理念**：三个子Agent各自用不同数据和逻辑判断，不共享上下文、不串通——相当于独立的三个分析师。

---

## 完整调度流程

### Step 1：初始化三个子Agent

```python
# 开3个子Agent（run模式，跑完不退出可复用）
sessions_spawn(label="选股Agent", task="""
你是截面选股专家。等待主Agent给你发任务。
数据文件在 /home/dr/code/quant-factor/evaluation/。
收到指令后分析并回复，只回股票代码列表(逗号分隔)。
""")

sessions_spawn(label="择时Agent", task="""
你是择时判断专家。等待主Agent给你发任务。
回答只回"能开仓"或"不能开仓"+简短一句话理由。
""")

sessions_spawn(label="风控Agent", task="""
你是风控专家。等待主Agent给你发任务。
只回仓位建议(满仓/半仓/空仓)+一句话理由。
""")
```

### Step 2：依次调度

```python
# 选股：具体数据+因子指令
sessions_send(
    sessionKey="选股Agent的sessionKey",
    message="请从 full_market_factor_panel.csv 最新一期，按5因子IR加权选top 10。只回代码。"
)
# → "688506,688336,688525,600536,2709,2460,2624,2603,300857,792"

# 择时：传入票池+市场数据
sessions_send(
    sessionKey="择时Agent的sessionKey",
    message=f"选股Agent选出: {stocks}。请读取hs300日线判断能否开仓。"
)
# → "能开仓 — 均线多头排列但赚钱效应回落需控仓"

# 风控：传入持仓+历史数据
sessions_send(
    sessionKey="风控Agent的sessionKey",
    message=f"持仓: {stocks}。请参考历史回撤和夏普做风险评估。"
)
# → "半仓 — 科创/创业板高beta，涨幅87%后反转风险"

# 主Agent汇总决策
decision = f"择时={择时结果}, 风控={风控结果} → 最终仓位={仓位}"
```

### Step 3：执行

```python
# 主Agent拍板后调用Python下单
exec(command=f"python3.11 execute_order.py --stocks {stocks} --position {仓位}")
```

---

## 关键技术点

### 1. sessions_spawn 的两种模式

| 模式                     | 特点                              | 适用   |
| :--------------------- | :------------------------------ | :--- |
| `run`                  | 一次性跑完退出，但可以用 sessions_send 二次发送 | 批处理  |
| `session`（需thread+ACP） | 持久化等消息                          | 持续运行 |

**实测**：`run` 模式已完成的子会话，用 `sessions_send` 仍能收到新消息并执行——不限于单次。

### 2. sessions_send 同步等待

- 发送消息后，发送者会等待接收者完成才继续
- timeoutSeconds 设60秒足够（因子分析/读数据通常在20~40秒内）
- 返回的 `reply` 字段直接就是子Agent的回复文本

### 3. 子Agent独立上下文

每个 `sessions_spawn` 出来的子会话是**完全独立**的：
- 看不到父会话历史
- 看不到其他子Agent的回答
- 避免"信息泄露"导致决策趋同

### 4. 提示词设计原则

子Agent的提示词要精简且有约束：
- ✅ 明确角色定位（"你是XX专家"）
- ✅ 给出数据文件路径
- ✅ 限制输出格式（"只回代码列表"、"只回能/不能+一句话"）
- ❌ 不给具体判断逻辑（让它自己推理）
- ❌ 不给其他Agent的输出（保持独立性）

---

## 实战结果（2026-04-27 测试）

| Agent | 输入 | 输出 |
|:---|:---|:---|
| 选股 | 796只A股因子面板 | 688506,688336,688525,600536,002709,002460,002624,002603,300857,000792 |
| 择时 | 票池+沪深300日线 | ✅ 能开仓 — 均线多头，但赚钱效应回落 |
| 风控 | 票池+历史绩效 | ⚠️ 半仓 — 高beta科创创业板+涨幅87%反转风险 |

**最终决策**：开仓，半仓执行，10只等权各5%，留50%现金防回调。

---

## 对比其他方案

| 方案 | 多Agent调度 | 上下文隔离 | 二次通信 | 适用 |
|:---|:---|:---|:---|:---|
| OpenClaw sessions_spawn（原生子Agent） | ✅ | ✅ 独立 | ✅ sessions_send | 低频决策 |
| exec 并行 CC --print（真CC方案） | ✅ | ✅ 独立 | ⚠️ 文件通信 | 批处理 |
| CC --print 批处理 | ❌ 单次 | — | ❌ | 一次性任务 |
| PandaAI可视化节点 | ✅ | ❌ 串一起 | ✅ | 高频实时 |
| LangChain/LangGraph | ✅ | 可配置 | ✅ | 复杂生产 |

OpenClaw方案的优势是极简——不需要写Agent框架代码，不需要维护通信协议，三行 sessions_spawn 就搞定。

---

## 扩展思路

1. **复盘Agent**：每月底层加一个复盘Agent，自动分析上月绩效、更新因子权重建议
2. **中频联动**：主Agent同时调度月频选股+周频龙虎榜，心跳驱动
3. **多策略投票**：不只绑一个主Agent，而是三个独立策略各自运行 Agent → 投票
4. **自动cron调度**：把整条流程写到 cron 里，每月最后一个交易日自动触发

---

## 调度脚本模板

```markdown
你是量化交易总指挥。当前是每月最后一个交易日。

# 调度计划
1. Spawn 3个子Agent（选股、择时、风控）
2. 用 sessions_send 依次获取结果
3. 三者都过 → 执行下单
4. 任一不通过 → 降低仓位或空仓
5. 完成后 Spawn 复盘Agent总结

# 规则
- 选股只回股票代码
- 择时只回"能/不能"+理由
- 风控只回"满/半/空"+理由
- 你只做调度和拍板，不自己选股。
```

---

*创建日期：2026-04-27（基于实战验证）*
*更新日期：2026-04-27（修正：标注OpenClaw子Agent ≠ Claude Code）*
*标签： #OpenClaw #多Agent #量化交易 #子Agent调度 *
