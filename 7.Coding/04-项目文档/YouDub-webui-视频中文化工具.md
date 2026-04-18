# YouDub-webui - 视频中文化工具

**项目地址**: https://github.com/liuzhao1225/YouDub-webui  
**类型**: AI 视频翻译/配音工具  
**最后更新**: 2026-04-12

---

## 📋 项目简介

YouDub-webui 是 [YouDub](https://github.com/liuzhao1225/YouDub) 的网页交互版本，基于 Gradio 构建。用于将 YouTube 等平台的视频自动翻译成中文并配音。

### 核心功能

| 功能 | 技术 |
|------|------|
| 视频下载 | YouTube 链接/播放列表/频道 |
| 人声分离 | Demucs 模型 |
| 语音识别 | WhisperX（带说话人识别） |
| 字幕翻译 | OpenAI GPT 模型 |
| 语音合成 | Coqui TTS / 火山引擎 |
| 视频合成 | 音视频同步 + 字幕 |
| 自动上传 | Bilibili 一键上传 |

---

## 🛠️ 环境需求

### 基础环境
```bash
# 克隆项目
git clone https://github.com/liuzhao1225/YouDub-webui.git
cd YouDub-webui

# 安装依赖
pip install -r requirements.txt
pip install TTS  # TTS 需单独安装
```

### 环境变量配置（.env）

| 变量 | 说明 |
|------|------|
| `OPENAI_API_KEY` | OpenAI API 密钥 |
| `MODEL_NAME` | 模型名称（gpt-4/gpt-3.5-turbo） |
| `OPENAI_API_BASE` | 自定义 API 地址（可选） |
| `HF_TOKEN` | Hugging Face token |
| `APPID` | 火山引擎 TTS 凭据 |
| `ACCESS_TOKEN` | 火山引擎 TTS 凭据 |
| `BILI_BASE64` | Bilibili API 凭据 |

### 运行方式
```bash
# Windows
./run_windows.bat

# 通用
python app.py
```

---

## 💰 使用成本估算

### API 费用（每小时视频）

| 配置方案 | 费用估算 |
|---------|---------|
| **经济版**（GPT-3.5 + 标准 TTS） | ¥1-3 / 小时 |
| **标准版**（GPT-4 + 标准 TTS） | ¥6-17 / 小时 |
| **高配版**（GPT-4 + 高级 TTS） | ¥7-19 / 小时 |

### 费用明细

**OpenAI API（翻译）**
- GPT-4 Turbo: ¥5-15 / 小时视频
- GPT-3.5 Turbo: ¥0.5-2 / 小时视频

**火山引擎 TTS（配音）**
- 标准 TTS: ¥0.3-0.5 / 小时
- 高级 TTS: ¥1-2 / 小时

**Hugging Face（说话人识别）**
- 免费额度：30,000 字符/月
- 超额：$0.0001/字符

**本地运行（免费）**
- WhisperX 语音识别 ✅
- Demucs 人声分离 ✅
- 视频处理 ✅

---

## 💡 技术细节

### AI 语音识别
- 基于 **WhisperX**（OpenAI Whisper 增强版）
- 支持自动时间对齐
- 支持说话人分离（Speaker Diarization）

### 翻译
- 支持 OpenAI GPT 系列模型
- 可通过 `OPENAI_API_BASE` 接入本地 LLM

### 语音合成
- **Coqui AI TTS** - 开源方案
- **火山引擎** - 音质更好，适合单一说话人

### 视频处理
- 音视频同步
- 字幕嵌入
- 帧率/分辨率调整

---

## 📝 使用流程

1. **全自动模式** - 一键完成所有步骤
2. **分步模式** - 可选择单独执行：
   - 下载视频 → 人声分离 → 语音识别 → 字幕翻译 → 语音合成 → 视频合成

### 关键参数
- `Resolution` - 下载分辨率
- `Demucs Model` - 音频分离模型
- `Whisper Model` - 语音识别模型
- `Translation Target Language` - 目标语言
- `Force Bytedance` - 强制使用火山引擎 TTS
- `Auto Upload Video` - 自动上传 Bilibili

---

## ⚠️ 注意事项

1. **版权问题** - 使用时需遵守版权法
2. **GPU 加速** - 需手动安装对应 CUDA 版本的 PyTorch
3. **Bilibili 凭据** - 参考 [bilibili-toolman](https://github.com/mos9527/bilibili-toolman)
4. **省钱建议**:
   - 使用 GPT-3.5 Turbo（便宜 10 倍+）
   - 批量处理减少 API 调用
   - 本地 LLM 替代 OpenAI

---

## 🔗 相关资源

- **主项目**: https://github.com/liuzhao1225/YouDub
- **Discord**: https://discord.gg/vbkYnN2Rrm
- **Bilibili 教程**: https://space.bilibili.com/12637318

---

*最后更新：2026-04-12*
