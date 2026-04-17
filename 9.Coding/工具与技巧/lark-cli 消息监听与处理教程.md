# lark-cli 消息监听与处理教程

> 创建时间：2026-04-15
> 目标：使用 lark-cli 监听指定人的飞书消息，自动处理后续任务

---

## 目录

1. [前置准备](#前置准备)
2. [获取历史消息](#获取历史消息)
3. [实时监听消息](#实时监听消息)
4. [监听特定人的消息](#监听特定人的消息)
5. [监听群内 @ 我的消息](#监听群内-at-我的消息)
6. [自动化处理流程](#自动化处理流程)
7. [完整示例脚本](#完整示例脚本)

---

## 一、前置准备

### 1.1 安装与认证

```bash
# 确保 lark-cli 已安装
lark-cli --version

# 查看当前认证状态
lark-cli auth status

# 如果未认证，执行登录
lark-cli auth login
```

### 1.2 平台端配置（重要！）

在飞书开放平台控制台配置事件订阅：

1. 进入 **事件与回调 → 订阅方式**
2. 选择 **"使用长连接接收事件"**
3. 添加需要的事件类型：
   - `im.message.receive_v1` — 接收消息
4. 启用对应权限：
   - `im:message:receive_as_bot` — 以机器人身份接收消息

> **注意**：这些配置必须在飞书开放平台控制台完成，CLI 无法动态订阅。

---

## 二、获取历史消息

### 2.1 查找用户

```bash
# 搜索用户（获取 open_id）
lark-cli contact +search-user --query "用户名" --format pretty

# 输出示例：
# name         open_id
# ───────────  ───────────────────────────────────
# Zefeng Chen  ou_946a92986c93577a3b4e6bcd57adeaae
```

### 2.2 查看私聊历史消息

```bash
# 列出与某人的私聊消息（最新 50 条）
lark-cli im +chat-messages-list \
  --user-id "ou_xxx" \
  --as user \
  --format pretty \
  --page-size 50

# 查看更多历史消息（使用 page_token）
lark-cli im +chat-messages-list \
  --user-id "ou_xxx" \
  --as user \
  --format pretty \
  --page-size 50 \
  --page-token "xxx"
```

### 2.3 搜索特定消息

```bash
# 搜索包含关键词的消息
lark-cli im +messages-search \
  --query "关键词" \
  --sender "ou_xxx" \
  --as user \
  --format pretty

# 搜索时间范围内的消息
lark-cli im +messages-search \
  --query "关键词" \
  --sender "ou_xxx" \
  --start "2026-04-01T00:00:00+08:00" \
  --end "2026-04-15T23:59:59+08:00" \
  --as user \
  --format pretty
```

---

## 三、实时监听消息

### 3.1 基本监听命令

```bash
# 监听所有消息事件（24 种常见事件类型）
lark-cli event +subscribe

# 只监听消息接收事件
lark-cli event +subscribe --event-types im.message.receive_v1

# 使用 compact 格式（Agent 友好输出）
lark-cli event +subscribe \
  --event-types im.message.receive_v1 \
  --compact \
  --quiet
```

### 3.2 输出格式

**原始格式（NDJSON）**：
```json
{"schema":"2.0","header":{"event_id":"xxx","event_type":"im.message.receive_v1"},"event":{"message":{"chat_id":"oc_xxx","content":"{\"text\":\"Hello\"}","message_id":"om_xxx"}}}
```

**Compact 格式（推荐）**：
```json
{"type":"im.message.receive_v1","message_id":"om_xxx","chat_id":"oc_xxx","chat_type":"p2p","message_type":"text","content":"Hello","sender_id":"ou_xxx"}
```

### 3.3 将事件写入文件

```bash
# 所有事件写入目录
lark-cli event +subscribe --output-dir ./events

# 按类型路由到不同目录
lark-cli event +subscribe \
  --route '^im\.message=dir:./messages/' \
  --route '^contact\.=dir:./contacts/'
```

---

## 四、监听特定人的消息

### 4.1 获取目标用户的 open_id

```bash
# 搜索获取
lark-cli contact +search-user --query "目标用户名" --format json | jq '.[0].open_id'

# 或直接从历史消息获取
lark-cli im +chat-messages-list --user-id "ou_xxx" --format json | jq '.[0].sender_id'
```

### 4.2 过滤特定人的消息

```bash
# 监听 + 过滤特定发送者
lark-cli event +subscribe \
  --event-types im.message.receive_v1 \
  --compact --quiet \
  | grep --line-buffered '"sender_id":"ou_TARGET_ID"'
```

### 4.3 更精确的 jq 过滤

```bash
# 使用 jq 精确过滤
TARGET_ID="ou_946a92986c93577a3b4e6bcd57adeaae"

lark-cli event +subscribe \
  --event-types im.message.receive_v1 \
  --compact --quiet \
  | while IFS= read -r line; do
      sender=$(echo "$line" | jq -r '.sender_id // empty')
      [[ "$sender" == "$TARGET_ID" ]] && echo "$line"
    done
```

---

## 五、监听群内 @ 我的消息

### 5.1 消息内容结构

群消息中 `@某人` 的内容格式：

```json
{
  "text": "<at user_id=\"ou_xxx\">@张三</at> 请帮忙看一下"
}
```

### 5.2 过滤 @ 我的消息

```bash
# 获取自己的 open_id
MY_ID=$(lark-cli contact +get-user --format json | jq -r '.open_id')

# 监听 @ 我的消息
lark-cli event +subscribe \
  --event-types im.message.receive_v1 \
  --compact --quiet \
  | while IFS= read -r line; do
      content=$(echo "$line" | jq -r '.content // empty')
      chat_type=$(echo "$line" | jq -r '.chat_type // empty')
      
      # 只处理群消息
      [[ "$chat_type" != "group" ]] && continue
      
      # 检查是否 @ 我
      if echo "$content" | grep -q "at user_id=\"$MY_ID\""; then
        echo "$line"
      fi
    done
```

### 5.3 使用 lark-cli 内置过滤

```bash
# 如果只是需要 @ 消息的搜索
lark-cli im +messages-search \
  --is-at-me \
  --as user \
  --format pretty
```

---

## 六、自动化处理流程

### 6.1 基本架构

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  lark-cli event  │ ──▶ │    过滤器        │ ──▶ │   处理器         │
│  +subscribe      │     │  (jq/grep)       │     │  (脚本/API)      │
└──────────────────┘     └──────────────────┘     └──────────────────┘
                               │
                               ▼
                         ┌──────────────────┐
                         │  消息队列/文件    │
                         └──────────────────┘
```

### 6.2 消息处理 Pipeline

```bash
#!/bin/bash
# monitor-and-process.sh

TARGET_USER="ou_946a92986c93577a3b4e6bcd57adeaae"
MY_ID=$(lark-cli contact +get-user --format json | jq -r '.open_id')

lark-cli event +subscribe \
  --event-types im.message.receive_v1 \
  --compact --quiet \
  | while IFS= read -r event; do
      # 解析事件
      sender=$(echo "$event" | jq -r '.sender_id')
      chat_type=$(echo "$event" | jq -r '.chat_type')
      content=$(echo "$event" | jq -r '.content')
      message_id=$(echo "$event" | jq -r '.message_id')
      chat_id=$(echo "$event" | jq -r '.chat_id')
      
      # 判断消息来源
      source="unknown"
      
      # 1. 来自特定用户的私聊
      if [[ "$chat_type" == "p2p" && "$sender" == "$TARGET_USER" ]]; then
        source="target_user"
      fi
      
      # 2. 群内 @ 我的消息
      if [[ "$chat_type" == "group" && "$content" =~ "at user_id=\"$MY_ID\"" ]]; then
        source="group_at_me"
      fi
      
      # 3. 来自特定用户的群消息
      if [[ "$chat_type" == "group" && "$sender" == "$TARGET_USER" ]]; then
        source="target_user_in_group"
      fi
      
      # 根据来源执行不同处理
      case "$source" in
        target_user)
          echo "[私聊] 来自目标用户: $content"
          # 执行处理逻辑...
          ;;
        group_at_me)
          echo "[群聊] 有人 @ 我: $content"
          # 执行处理逻辑...
          ;;
        target_user_in_group)
          echo "[群聊] 目标用户发言: $content"
          # 执行处理逻辑...
          ;;
        *)
          # 忽略其他消息
          continue
          ;;
      esac
      
      # 记录到日志文件
      echo "$(date '+%Y-%m-%d %H:%M:%S') [$source] $content" >> ./message-log.txt
    done
```

---

## 七、完整示例脚本

### 7.1 监听特定用户 + 自动回复

```bash
#!/bin/bash
# auto-reply.sh

TARGET_USER="ou_946a92986c93577a3b4e6bcd57adeaae"

lark-cli event +subscribe \
  --event-types im.message.receive_v1 \
  --compact --quiet \
  | while IFS= read -r event; do
      sender=$(echo "$event" | jq -r '.sender_id')
      chat_type=$(echo "$event" | jq -r '.chat_type')
      content=$(echo "$event" | jq -r '.content')
      message_id=$(echo "$event" | jq -r '.message_id')
      
      # 只处理来自目标用户的私聊消息
      [[ "$chat_type" != "p2p" ]] && continue
      [[ "$sender" != "$TARGET_USER" ]] && continue
      
      echo "收到消息: $content"
      
      # 调用 AI 生成回复
      reply=$(claude -p "简洁回复: $content" 2>/dev/null)
      
      # 发送回复
      lark-cli im +messages-reply \
        --message-id "$message_id" \
        --text "$reply" \
        --as bot
      
      echo "已回复: $reply"
    done
```

### 7.2 监听 @ 我 + 执行任务

```bash
#!/bin/bash
# at-me-handler.sh

MY_ID=$(lark-cli contact +get-user --format json | jq -r '.open_id')

lark-cli event +subscribe \
  --event-types im.message.receive_v1 \
  --compact --quiet \
  | while IFS= read -r event; do
      chat_type=$(echo "$event" | jq -r '.chat_type')
      content=$(echo "$event" | jq -r '.content')
      message_id=$(echo "$event" | jq -r '.message_id')
      chat_id=$(echo "$event" | jq -r '.chat_id')
      
      # 只处理群消息
      [[ "$chat_type" != "group" ]] && continue
      
      # 检查是否 @ 我
      if ! echo "$content" | grep -q "at user_id=\"$MY_ID\""; then
        continue
      fi
      
      # 提取实际消息内容（去掉 @ 部分）
      actual_content=$(echo "$content" | sed 's/<at[^>]*>[^<]*<\/at>//g' | xargs)
      
      echo "群内有人 @ 我: $actual_content"
      
      # 根据内容关键词执行任务
      case "$actual_content" in
        *"查日志"*|*"看日志"*)
          # 执行日志查询任务
          result=$(./check-logs.sh)
          lark-cli im +messages-reply \
            --message-id "$message_id" \
            --text "日志查询结果:\n$result" \
            --as bot
          ;;
        *"重启服务"*)
          # 执行重启任务
          ./restart-service.sh
          lark-cli im +messages-reply \
            --message-id "$message_id" \
            --text "服务已重启" \
            --as bot
          ;;
        *"状态"*)
          # 返回状态
          status=$(./get-status.sh)
          lark-cli im +messages-reply \
            --message-id "$message_id" \
            --text "当前状态:\n$status" \
            --as bot
          ;;
        *)
          # 默认回复
          lark-cli im +messages-reply \
            --message-id "$message_id" \
            --text "收到，请稍后处理" \
            --as bot
          ;;
      esac
    done
```

### 7.3 消息转发到另一个群

```bash
#!/bin/bash
# forward-messages.sh

TARGET_USER="ou_xxx"
FORWARD_CHAT="oc_xxx"  # 目标群 chat_id

lark-cli event +subscribe \
  --event-types im.message.receive_v1 \
  --compact --quiet \
  | while IFS= read -r event; do
      sender=$(echo "$event" | jq -r '.sender_id')
      content=$(echo "$event" | jq -r '.content')
      
      [[ "$sender" != "$TARGET_USER" ]] && continue
      
      # 转发到目标群
      lark-cli im +messages-send \
        --chat-id "$FORWARD_CHAT" \
        --text "[转发] $content" \
        --as bot
      
      echo "已转发: $content"
    done
```

### 7.4 记录消息到 Obsidian

```bash
#!/bin/bash
# log-to-obsidian.sh

OBSIDIAN_PATH="/home/dr/文档/Obsidian Vault/"
TARGET_USER="ou_xxx"

lark-cli event +subscribe \
  --event-types im.message.receive_v1 \
  --compact --quiet \
  | while IFS= read -r event; do
      sender=$(echo "$event" | jq -r '.sender_id')
      sender_name=$(lark-cli contact +get-user --user-id "$sender" --format json | jq -r '.name')
      content=$(echo "$event" | jq -r '.content')
      timestamp=$(echo "$event" | jq -r '.create_time')
      date=$(date -d "@$timestamp" '+%Y-%m-%d')
      time=$(date -d "@$timestamp" '+%H:%M')
      
      [[ "$sender" != "$TARGET_USER" ]] && continue
      
      # 写入 Obsidian 日记
      note_file="$OBSIDIAN_PATH/daily/$date.md"
      [[ ! -f "$note_file" ]] && touch "$note_file"
      
      echo "- [$time] $sender_name: $content" >> "$note_file"
      echo "已记录到 $note_file"
    done
```

---

## 八、常见问题

### Q1: 为什么收不到事件？

**检查清单**：
1. 平台控制台是否配置了事件订阅
2. 是否选择了"长连接"模式
3. 是否添加了 `im.message.receive_v1` 事件类型
4. 是否启用了 `im:message:receive_as_bot` 权限
5. 是否在应用可见范围内

### Q2: 私聊消息和群消息的区别？

| 字段 | 私聊 (p2p) | 群聊 (group) |
|------|-----------|-------------|
| `chat_type` | `p2p` | `group` |
| `chat_id` | 私聊 ID | 群 ID |
| `sender_id` | 对方 open_id | 发言者 open_id |

### Q3: 如何回复消息？

```bash
# 回复消息（机器人身份）
lark-cli im +messages-reply \
  --message-id "om_xxx" \
  --text "回复内容" \
  --as bot

# 发送新消息到群
lark-cli im +messages-send \
  --chat-id "oc_xxx" \
  --text "消息内容" \
  --as bot
```

### Q4: 如何获取发送者姓名？

```bash
# 从 open_id 获取用户信息
lark-cli contact +get-user --user-id "ou_xxx" --format json | jq '.name'
```

### Q5: 如何持续运行监听？

```bash
# 使用 systemd 服务
cat > ~/.config/systemd/user/lark-monitor.service << EOF
[Unit]
Description=Lark Message Monitor
After=network.target

[Service]
ExecStart=/home/dr/scripts/monitor-and-process.sh
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOF

# 启用并启动
systemctl --user enable lark-monitor
systemctl --user start lark-monitor
```

---

## 九、进阶用法

### 9.1 多目标监听

```bash
# 定义多个目标用户
TARGETS=(
  "ou_946a92986c93577a3b4e6bcd57adeaae"
  "ou_cd23b9165c9dbe5bedda5c24820a9d97"
  "ou_b928d6bf84759d49126e639f6b2b1c95"
)

lark-cli event +subscribe \
  --event-types im.message.receive_v1 \
  --compact --quiet \
  | while IFS= read -r event; do
      sender=$(echo "$event" | jq -r '.sender_id')
      
      # 检查是否在目标列表中
      for target in "${TARGETS[@]}"; do
        if [[ "$sender" == "$target" ]]; then
          echo "来自目标用户 $target: $(echo "$event" | jq -r '.content')"
          # 处理逻辑...
        fi
      done
    done
```

### 9.2 消息优先级处理

```bash
# 高优先级关键词触发立即处理
HIGH_PRIORITY=("紧急" "bug" "崩溃" "报警")

lark-cli event +subscribe \
  --event-types im.message.receive_v1 \
  --compact --quiet \
  | while IFS= read -r event; do
      content=$(echo "$event" | jq -r '.content')
      
      # 检查高优先级关键词
      for keyword in "${HIGH_PRIORITY[@]}"; do
        if [[ "$content" =~ "$keyword" ]]; then
          echo "⚠️ 高优先级消息: $content"
          # 立即处理 + 通知
          ./send-alert.sh "$content"
        fi
      done
    done
```

### 9.3 与其他工具集成

```bash
# 集成 n8n workflow
lark-cli event +subscribe \
  --compact --quiet \
  | while IFS= read -r event; do
      # 发送到 n8n webhook
      curl -X POST "http://localhost:5678/webhook/lark" \
        -H "Content-Type: application/json" \
        -d "$event"
    done

# 集成 Python 脚本
lark-cli event +subscribe --compact --quiet \
  | python3 ./process-events.py

# 集成 AI Agent
lark-cli event +subscribe --compact --quiet \
  | claude --agent "处理飞书消息"
```

---

## 十、参考资源

- [lark-cli 官方文档](https://open.feishu.cn/document/client-docs/lark-cli)
- [飞书事件订阅指南](https://open.feishu.cn/document/server-docs/event-subscription-guide)
- [lark-im SKILL.md](~/.agents/skills/lark-im/SKILL.md)
- [lark-event SKILL.md](~/.agents/skills/lark-event/SKILL.md)

---

*教程创建时间: 2026-04-15*