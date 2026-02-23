# OpenClaw TTS vs Message 语音消息对比

## 概述

OpenClaw 有两种方式发送语音到 Telegram：
1. **TTS 工具** - 自动发送，但 Telegram 会循环播放
2. **Message 工具 + asVoice** - 手动发送，只播放一次

---

## 对比表

| 特性              | TTS 工具             | Message 工具 + asVoice     |
| --------------- | ------------------ | ------------------------ |
| **发送方式**        | 自动（`[[tts]]` 标签触发） | 手动调用 `message` 工具        |
| **Telegram 显示** | 普通音频文件（📎）         | 语音消息（🎤 圆形图标）            |
| **播放行为**        | 循环播放 ❌             | 只播放一次 ✅                  |
| **配置复杂度**       | 简单，自动              | 需要手动生成 + 发送              |
| **文件位置**        | 临时目录               | `~/.openclaw/workspace/` |
| **适用场景**        | 闲聊、短回复             | 长内容、需要语音体验               |

---

## TTS 工具（普通音频）

### 配置位置
`~/.openclaw/openclaw.json`

```json
{
  "messages": {
    "tts": {
      "auto": "tagged",
      "provider": "edge",
      "edge": {
        "voice": "zh-CN-XiaoyiNeural",
        "lang": "zh-CN",
        "rate": "+10%"
      }
    }
  }
}
```

### 使用方式
在回复中添加 `[[tts]]` 标签：
```
[[tts]] 这是一条语音消息
```

### 问题
- Telegram 将其识别为**普通音频文件**
- 默认**循环播放**，无法自动停止
- 用户体验较差

---

## Message 工具（语音消息）

### 核心参数
```json
{
  "action": "send",
  "channel": "telegram",
  "target": "6227868121",
  "path": "/Users/apple/.openclaw/workspace/audio.mp3",
  "asVoice": true
}
```

### 工作流程
1. **生成音频**：使用 edge-tts 生成 MP3
   ```bash
   uv run --with edge-tts python3 -c "
   import asyncio, edge_tts
   async def gen():
       c = edge_tts.Communicate('文本', 'zh-CN-XiaoyiNeural')
       await c.save('/tmp/audio.mp3')
   asyncio.run(gen())
   "
   ```

2. **移动到允许目录**：
   ```bash
   cp /tmp/audio.mp3 ~/.openclaw/workspace/audio.mp3
   ```

3. **发送语音消息**：
   ```bash
   openclaw message send \
     --channel telegram \
     --target 6227868121 \
     --media ~/.openclaw/workspace/audio.mp3 \
     --asVoice
   ```

### 允许的文件目录
OpenClaw 限制本地媒体文件必须在以下目录：
- `~/.openclaw/workspace/` ✅
- `~/.openclaw/media/` ✅
- `~/.openclaw/agents/` ✅
- `/tmp/` ✅

---

## 技术原理（深度分析）

### TTS 工具完整流程

**源码位置**: `/opt/homebrew/lib/node_modules/openclaw/dist/pi-embedded-BxoxxVJz.js`

#### 步骤 1: TTS 生成
```javascript
// textToSpeech() 函数
async function textToSpeech(params) {
    const config = resolveTtsConfig(params.cfg);
    const output = resolveOutputFormat(resolveChannelId(params.channel));
    
    // Telegram 频道配置
    const TELEGRAM_OUTPUT = {
        openai: "opus",
        elevenlabs: "opus_48000_64",
        extension: ".opus",
        voiceCompatible: true  // ← 标记为语音兼容
    };
    
    // 生成音频后检查是否 voiceCompatible
    const voiceCompatible = isVoiceCompatibleAudio({ 
        fileName: edgeResult.audioPath 
    });
    
    // 返回结果包含 voiceCompatible 标志
    return {
        success: true,
        audioPath: edgeResult.audioPath,
        voiceCompatible: output.voiceCompatible  // Telegram = true
    };
}
```

#### 步骤 2: 生成 `[[audio_as_voice]]` 标签
```javascript
// TTS 工具返回格式
if (result.success && result.audioPath) {
    const lines = [];
    if (result.voiceCompatible) 
        lines.push("[[audio_as_voice]]");  // ← 生成标签！
    lines.push(`MEDIA:${result.audioPath}`);
    
    return {
        content: [{
            type: "text",
            text: lines.join("\n")
        }]
    };
}
```

**关键发现**: TTS 工具**确实生成了 `[[audio_as_voice]]` 标签**！

#### 步骤 3: 标签解析
**源码位置**: `/opt/homebrew/lib/node_modules/openclaw/dist/deliver-1hfFp6Dp.js`

```javascript
const AUDIO_TAG_RE = /\[\[\s*audio_as_voice\s*\]\]/gi;

function parseInlineDirectives(text, options = {}) {
    let audioAsVoice = false;
    
    // 解析 [[audio_as_voice]] 标签
    cleaned = cleaned.replace(AUDIO_TAG_RE, (match) => {
        audioAsVoice = true;  // ← 设置标志
        hasAudioTag = true;
        return stripAudioTag ? " " : match;
    });
    
    return {
        text: cleaned,
        audioAsVoice: audioAsVoice,  // ← 返回解析结果
        hasAudioTag: hasAudioTag
    };
}
```

#### 步骤 4: Telegram 发送决策
**源码位置**: `/opt/homebrew/lib/node_modules/openclaw/dist/send-B8LVpxsa.js`

```javascript
// resolveTelegramVoiceDecision() 函数
function resolveTelegramVoiceDecision(opts) {
    if (!opts.wantsVoice) return { useVoice: false };
    if (isTelegramVoiceCompatibleAudio(opts)) return { useVoice: true };
    return { useVoice: false, reason: "..." };
}

// Telegram 发送主逻辑
if (kind === "audio") {
    const { useVoice } = resolveTelegramVoiceSend({
        wantsVoice: opts.asVoice === true,  // ← 关键：需要 asVoice 参数
        contentType: media.contentType,
        fileName,
        logFallback: logVerbose
    });
    
    if (useVoice) 
        return api.sendVoice(chatId, file, effectiveParams);  // 语音消息
    else 
        return api.sendAudio(chatId, file, effectiveParams);  // 普通音频
}
```

### 问题根源

**`[[audio_as_voice]]` 标签被正确生成和解析，但 `asVoice` 参数没有传递到 Telegram 发送层！**

流程断点：
```
TTS 工具 → [[audio_as_voice]] + MEDIA:file.mp3
         ↓
parseInlineDirectives() → audioAsVoice: true
         ↓
deliverOutboundPayloads() → ❌ 没有将 audioAsVoice 转换为 asVoice 参数
         ↓
sendMessageTelegram() → opts.asVoice === undefined
         ↓
resolveTelegramVoiceDecision() → useVoice: false
         ↓
api.sendAudio() → 普通音频文件（循环播放）
```

### Message 工具为什么能成功

手动调用 `message` 工具时：
```javascript
{
    action: "send",
    channel: "telegram",
    target: "6227868121",
    media: "/path/to/audio.mp3",
    asVoice: true  // ← 直接传递参数，绕过标签解析
}
```

参数直接传递给 `sendMessageTelegram()`，`opts.asVoice === true`，所以 `useVoice: true`。

---

## 配置文件对比

### TTS 工具配置
**文件**: `~/.openclaw/openclaw.json`

```json
{
  "messages": {
    "tts": {
      "auto": "tagged",      // 触发模式：tagged/always/inbound/off
      "provider": "edge",    // TTS 提供商
      "edge": {
        "enabled": true,
        "voice": "zh-CN-XiaoyiNeural",
        "lang": "zh-CN",
        "rate": "+10%",
        "outputFormat": "mp3"  // ← 影响 voiceCompatible 判断
      }
    }
  }
}
```

**为什么不能传递 `asVoice` 参数？**
- TTS 工具是**自动生成音频**的工具，设计时只考虑了"生成并发送"
- `[[audio_as_voice]]` 标签是**事后标记**，在消息交付层解析
- 但交付层 (`deliverOutboundPayloads`) **没有将 `audioAsVoice` 转换为频道特定的 `asVoice` 参数**
- 这是 OpenClaw 的**实现遗漏**，不是配置问题

### Message 工具配置
无需配置文件，直接在调用时传递参数：
```json
{
  "action": "send",
  "channel": "telegram",
  "target": "<user_id>",
  "media": "<file_path>",
  "asVoice": true  // ← 直接生效
}
```

---

## 解决方案对比

| 方案 | 优点 | 缺点 |
|------|------|------|
| **修改 TTS 工具代码** | 一劳永逸，自动生效 | 需要改 OpenClaw 源码 |
| **手动 Message 发送** | 立即生效，无需改代码 | 每次需要手动操作 |
| **配置 `ttsAsVoice`** | 简单 | OpenClaw 不支持此配置 |

---

## 推荐做法

### 短期方案
使用 Message 工具手动发送：
```bash
# 1. 生成
uv run --with edge-tts python3 -c "..."

# 2. 复制
cp /tmp/audio.mp3 ~/.openclaw/workspace/

# 3. 发送
openclaw message send --channel telegram --target <ID> --media <PATH> --asVoice
```

### 长期方案
修改 OpenClaw TTS 工具，在 Telegram 频道自动使用 `asVoice: true`：
- 位置：`/opt/homebrew/lib/node_modules/openclaw/dist/`
- 需要添加频道特定的 TTS 配置

---

## 相关文件

- 配置：`~/.openclaw/openclaw.json`
- 工作目录：`~/.openclaw/workspace/`
- TTS 工具：`/opt/homebrew/lib/node_modules/openclaw/dist/`

---

## 参考资料

- [Telegram Bot API - sendVoice](https://core.telegram.org/bots/api#sendvoice)
- [Telegram Bot API - sendAudio](https://core.telegram.org/bots/api#sendaudio)
- [edge-tts GitHub](https://github.com/rany2/edge-tts)

---

---

## 配置影响检查

**检查时间**: 2026-02-22

### 修改过的配置
1. **`~/.openclaw/openclaw.json`** - 尝试添加 `ttsAsVoice: true` 到 Telegram 频道配置
   - 结果：**未生效**，OpenClaw 不支持此配置项
   - 状态：已回滚（实际未成功写入）

2. **`~/.openclaw/workspace/`** - 临时音频文件目录
   - 用途：存放手动发送的语音消息文件
   - 状态：保留（这是标准用法）

### 未修改的配置
- TTS 配置 (`messages.tts.*`) - 无改动
- Telegram 频道配置 - 无改动
- 其他频道配置 - 无改动

### 清理的临时文件
```bash
rm -f ~/.openclaw/workspace/*.mp3 /tmp/voice_test.mp3 /tmp/question.mp3 \
      /tmp/confirm.mp3 /tmp/done.mp3 /tmp/analysis.mp3 /tmp/short.mp3
```

---

## 结论

**系统配置安全**：本次调试没有对 OpenClaw 配置造成任何持久性影响。

**唯一变更**：在 `~/.openclaw/workspace/` 目录生成临时音频文件（这是正常用法，文件可随时清理）。

**推荐实践**：
- 需要语音消息时，手动使用 `message` 工具 + `asVoice: true`
- 不要依赖 TTS 工具的 `[[audio_as_voice]]` 标签（实现有遗漏）
- 定期清理 `~/.openclaw/workspace/` 目录

---

**创建时间**: 2026-02-22  
**最后更新**: 2026-02-22（添加配置影响检查）  
**标签**: #OpenClaw #Telegram #TTS #语音消息 #配置对比
