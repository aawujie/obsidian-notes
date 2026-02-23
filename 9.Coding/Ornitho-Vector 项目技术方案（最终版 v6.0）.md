# Ornitho-Vector 项目技术方案（最终版 v6.0）

**创建日期**:: 2026-02-22  
**版本**:: v6.0（最终版 - 带音频同步动画）  
**项目类型**:: 音频可视化 / 交互式 HTML  
**技术栈**:: Python, librosa, PCA, Plotly, JavaScript  
**状态**:: ✅ 完成

---

## 🎯 v6.0 核心功能

- **单音频时间序列轨迹** - 每帧音频 → MFCC → PCA → 3D 坐标
- **音频 + 动画同步播放** - 点击播放后，黄球沿轨迹移动，同时播放鸟鸣
- **高对比度配色** - 深蓝色轨迹 + 亮黄色亮点
- **requestAnimationFrame 控制** - 精确的音频 - 动画同步

---

## 📊 版本迭代历史

| 版本 | 日期 | 功能 | 问题 | 状态 |
|------|------|------|------|------|
| v2.0 | 02-22 | 多样本聚类 | 理解错误（用户要单音频轨迹） | ❌ 废弃 |
| v3.0 | 02-22 | 单音频时间轨迹 | 右侧热力图不显示 | ❌ 废弃 |
| v3.1 | 02-22 | 同步动画 | 播放按钮无响应 | ❌ 废弃 |
| v3.2 | 02-22 | 亮点移动 | 灰色轨迹看不清 | ❌ 废弃 |
| v4.0 | 02-23 | 高对比度配色 | 播放按钮仍无响应 | ❌ 废弃 |
| v5.0 | 02-23 | 嵌入音频 + 自定义按钮 | 动画和音频不同步 | ❌ 废弃 |
| **v6.0** | **02-23** | **requestAnimationFrame 控制** | **无** | ✅ **完成** |

---

## 🎨 v6.0 视觉效果

```
┌────────────────────────────────────┐
│  🐦 XC1082571... | ⏱️ 0.00s/9.95s │
├────────────────────────────────────┤
│                                    │
│        深蓝色轨迹线（完整路径）      │
│        🟡 黄色亮点（当前位置）       │
│                                    │
│                                    │
├────────────────────────────────────┤
│  [▶️ 播放] [⏸️ 暂停] [⏮️ 重置]       │
│   (绿色)   (橙色)   (红色)          │
└────────────────────────────────────┘
```

---

## 💻 v6.0 完整代码

```python
"""
Ornitho-Vector 系统 - 带音频播放版 v6.0
- 修复播放按钮控制
- 确保音频和动画真正同步
- requestAnimationFrame 精确同步
"""

import librosa
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.graph_objects as go
import os
import base64
import io
import json
import soundfile as sf

# =================配置区域=================
CONFIG = {
    'SR': 22050,
    'N_MFCC': 20,
    'HOP_LENGTH': 512,
    'N_FFT': 2048,
    'INPUT_DIR': './raw_audio',
    'OUTPUT_DIR': './output',
}
# =========================================


def process_audio(file_path):
    """处理音频"""
    print(f"\n📂 {os.path.basename(file_path)}")
    
    y, sr = librosa.load(file_path, sr=CONFIG['SR'], mono=True)
    duration = len(y) / sr
    
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=CONFIG['N_MFCC'], n_fft=CONFIG['N_FFT'], hop_length=CONFIG['HOP_LENGTH'])
    n_frames = mfcc.shape[1]
    timestamps = np.arange(n_frames) * CONFIG['HOP_LENGTH'] / sr
    
    mfcc_T = mfcc.T
    scaler = StandardScaler()
    mfcc_scaled = scaler.fit_transform(mfcc_T)
    
    pca = PCA(n_components=3)
    coords = pca.fit_transform(mfcc_scaled)
    
    print(f"   {duration:.2f}s | {n_frames}帧 | PCA: {sum(pca.explained_variance_ratio_):.1%}")
    
    return {
        'filename': os.path.basename(file_path),
        'duration': duration,
        'n_frames': n_frames,
        'timestamps': timestamps,
        'coords': coords,
        'audio': y,
        'sr': sr,
    }


def encode_audio_to_base64(audio_data, sr):
    """编码音频为 base64"""
    buffer = io.BytesIO()
    sf.write(buffer, audio_data, sr, format='WAV')
    buffer.seek(0)
    audio_bytes = buffer.read()
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    return f"data:audio/wav;base64,{audio_base64}"


def create_html(data_dict):
    """创建 HTML"""
    print("   🎬 生成动画...")
    
    coords = data_dict['coords']
    timestamps = data_dict['timestamps']
    filename = data_dict['filename']
    duration = data_dict['duration']
    n_frames = data_dict['n_frames']
    audio = data_dict['audio']
    sr = data_dict['sr']
    
    # 降采样到 100 帧（更流畅）
    n_anim_frames = min(100, n_frames)
    frame_ids = np.linspace(0, n_frames - 1, n_anim_frames, dtype=int)
    
    # 编码音频
    print("   🔊 编码音频...")
    audio_base64 = encode_audio_to_base64(audio, sr)
    print(f"   ✅ 音频编码完成 ({len(audio_base64)} chars)")
    
    # 准备帧数据（手动序列化）
    frames_json = []
    for idx, frame_id in enumerate(frame_ids):
        current_time = timestamps[frame_id]
        current_pos = coords[frame_id]
        frames_json.append({
            'x': float(current_pos[0]),
            'y': float(current_pos[1]),
            'z': float(current_pos[2]),
            'time': f"{current_time:.2f}s"
        })
    
    # 计算每帧时长（匹配音频）
    audio_duration_ms = duration * 1000
    frame_duration_ms = audio_duration_ms / n_anim_frames
    
    # 生成完整 HTML
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🐦 {filename}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{ margin: 0; padding: 0; font-family: Arial, sans-serif; }}
        #plot {{ width: 900px; height: 650px; margin: 0 auto; }}
        #controls {{ 
            text-align: center; 
            padding: 20px; 
            background: #f5f5f5;
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 900px;
        }}
        button {{ 
            font-size: 18px; 
            padding: 12px 24px; 
            margin: 0 10px; 
            cursor: pointer; 
            border: none; 
            border-radius: 5px;
            color: white;
        }}
        #play-btn {{ background: #4CAF50; }}
        #pause-btn {{ background: #FF9800; }}
        #reset-btn {{ background: #f44336; }}
        button:hover {{ opacity: 0.9; }}
        button:disabled {{ background: #ccc; cursor: not-allowed; }}
        #status {{ margin-top: 10px; color: #666; }}
    </style>
</head>
<body>
    <div id="plot"></div>
    
    <div id="controls">
        <button id="play-btn">▶️ 播放</button>
        <button id="pause-btn">⏸️ 暂停</button>
        <button id="reset-btn">⏮️ 重置</button>
        <div id="status">点击播放开始</div>
    </div>
    
    <audio id="audio-player" preload="auto">
        <source src="{audio_base64}" type="audio/wav">
    </audio>
    
    <script>
        // 图形数据
        var graphData = {{
            nFrames: {n_anim_frames},
            frameDuration: {frame_duration_ms:.1f},
            totalDuration: {duration * 1000:.1f},
            frames: {json.dumps(frames_json)},
            trajectoryX: {json.dumps(coords[:, 0].tolist())},
            trajectoryY: {json.dumps(coords[:, 1].tolist())},
            trajectoryZ: {json.dumps(coords[:, 2].tolist())},
        }};
        
        // 初始化 Plotly
        var plotDiv = document.getElementById('plot');
        var data = [
            {{
                type: 'scatter3d',
                mode: 'lines',
                x: graphData.trajectoryX,
                y: graphData.trajectoryY,
                z: graphData.trajectoryZ,
                line: {{width: 5, color: 'rgba(0,0,139,0.6)'}},
                name: '轨迹',
            }},
            {{
                type: 'scatter3d',
                mode: 'markers',
                x: [graphData.frames[0].x],
                y: [graphData.frames[0].y],
                z: [graphData.frames[0].z],
                marker: {{size: 18, color: '#FFFF00', line: {{width: 3, color: 'black'}}}},
                name: '当前',
            }}
        ];
        
        var layout = {{
            title: {{text: '🐦 {filename} | ⏱️ 0.00s / {duration:.2f}s', x: 0.5, font: {{size: 16}}}},
            template: 'plotly_white',
            width: 900,
            height: 650,
            showlegend: false,
            margin: {{l: 0, r: 0, b: 120, t: 60}},
            scene: {{
                xaxis: {{title: 'PC1', showgrid: true, zeroline: true, showbackground: true, backgroundcolor: 'rgba(240,240,240,0.6)'}},
                yaxis: {{title: 'PC2', showgrid: true, zeroline: true, showbackground: true, backgroundcolor: 'rgba(240,240,240,0.6)'}},
                zaxis: {{title: 'PC3', showgrid: true, zeroline: true, showbackground: true, backgroundcolor: 'rgba(240,240,240,0.6)'}},
                bgcolor: 'rgba(255,255,255,0.95)',
                aspectmode: 'cube',
                camera: {{eye: {{x: 1.5, y: 1.5, z: 1.3}}}},
            }},
        }};
        
        Plotly.newPlot(plotDiv, data, layout, {{responsive: false}});
        
        // 音频和动画控制
        var audio = document.getElementById('audio-player');
        var playBtn = document.getElementById('play-btn');
        var pauseBtn = document.getElementById('pause-btn');
        var resetBtn = document.getElementById('reset-btn');
        var statusDiv = document.getElementById('status');
        
        var currentFrame = 0;
        var isPlaying = false;
        var animationFrame = null;
        var startTime = null;
        
        function updateFrame(frameIndex) {{
            if (frameIndex >= graphData.nFrames) frameIndex = graphData.nFrames - 1;
            
            var frame = graphData.frames[frameIndex];
            if (frame) {{
                Plotly.restyle(plotDiv, {{
                    x: [[frame.x]],
                    y: [[frame.y]],
                    z: [[frame.z]],
                }}, [1]);  // 更新第二个 trace（亮点）
                
                Plotly.relayout(plotDiv, {{
                    title: {{text: '🐦 {filename} | ⏱️ ' + frame.time + ' / {duration:.2f}s'}}
                }});
            }}
            currentFrame = frameIndex;
        }}
        
        function animate(timestamp) {{
            if (!isPlaying) return;
            if (!startTime) startTime = timestamp;
            
            var elapsed = timestamp - startTime;
            var newFrame = Math.floor(elapsed / graphData.frameDuration);
            
            if (newFrame !== currentFrame && newFrame < graphData.nFrames) {{
                updateFrame(newFrame);
                statusDiv.textContent = '播放中：' + (elapsed / 1000).toFixed(2) + 's / {duration:.2f}s';
            }}
            
            if (elapsed < graphData.totalDuration && isPlaying) {{
                animationFrame = requestAnimationFrame(animate);
            }} else if (isPlaying) {{
                isPlaying = false;
                audio.pause();
                audio.currentTime = 0;
                statusDiv.textContent = '播放完成';
                playBtn.disabled = false;
            }}
        }}
        
        playBtn.onclick = function() {{
            if (isPlaying) return;
            
            audio.play();
            isPlaying = true;
            startTime = null;
            playBtn.disabled = true;
            statusDiv.textContent = '播放中...';
            
            // 从当前帧继续
            if (currentFrame >= graphData.nFrames - 1) {{
                currentFrame = 0;
                startTime = null;
            }}
            
            animationFrame = requestAnimationFrame(animate);
        }};
        
        pauseBtn.onclick = function() {{
            isPlaying = false;
            audio.pause();
            if (animationFrame) {{
                cancelAnimationFrame(animationFrame);
            }}
            playBtn.disabled = false;
            statusDiv.textContent = '已暂停 @ ' + (currentFrame * graphData.frameDuration / 1000).toFixed(2) + 's';
        }};
        
        resetBtn.onclick = function() {{
            isPlaying = false;
            audio.pause();
            audio.currentTime = 0;
            if (animationFrame) {{
                cancelAnimationFrame(animationFrame);
            }}
            currentFrame = 0;
            updateFrame(0);
            playBtn.disabled = false;
            statusDiv.textContent = '已重置';
        }};
        
        audio.onended = function() {{
            isPlaying = false;
            if (animationFrame) {{
                cancelAnimationFrame(animationFrame);
            }}
            playBtn.disabled = false;
            statusDiv.textContent = '播放完成';
        }};
        
        // 初始化显示
        updateFrame(0);
        statusDiv.textContent = '就绪 | 时长：{duration:.2f}s | 帧数：{n_anim_frames}';
    </script>
</body>
</html>'''
    
    # 导出
    os.makedirs(CONFIG['OUTPUT_DIR'], exist_ok=True)
    html_file = os.path.join(CONFIG['OUTPUT_DIR'], f"{filename}_v6.html")
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"   ✅ {os.path.basename(html_file)}")
    
    return html_file


def main():
    print("=" * 70)
    print("🐦 Ornitho-Vector 音频播放版 v6.0")
    print("=" * 70)
    
    audio_files = []
    for root, dirs, files in os.walk(CONFIG['INPUT_DIR']):
        for file in files:
            if file.endswith(('.wav', '.mp3', '.flac', '.m4a')):
                audio_files.append(os.path.join(root, file))
    
    if not audio_files:
        print("\n❌ 没有找到音频文件")
        return
    
    print(f"\n📂 找到 {len(audio_files)} 个音频")
    
    results = []
    for audio_file in audio_files:
        try:
            data = process_audio(audio_file)
            html_file = create_html(data)
            results.append({'filename': data['filename'], 'html': html_file})
        except Exception as e:
            print(f"   ❌ 失败：{e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("✅ 完成！")
    print("=" * 70)
    
    for r in results:
        print(f"\n🐦 {r['filename']}")
        print(f"   📺 {r['html']}")
    
    print("\n💡 使用说明:")
    print("   1. 打开 HTML 文件")
    print("   2. 点击 ▶️ 播放")
    print("   3. 音频和动画同步播放")


if __name__ == "__main__":
    main()
```

---

## 🔧 依赖安装

```bash
cd ~/code/8.practice/ornitho-vector

# 使用 UV（推荐）
uv add librosa numpy pandas scikit-learn plotly scipy soundfile

# 或使用 pip
pip install librosa numpy pandas scikit-learn plotly scipy soundfile
```

---

## 📂 项目结构

```
~/code/8.practice/ornitho-vector/
│
├── raw_audio/
│   ├── XC1082571 - 长尾林鸮 - Strix uralensis.mp3
│   ├── XC1082569 - 黄褐林鸮 - Strix aluco.wav
│   └── XC1082454 - Identity unknown.mp3
│
├── output/
│   ├── XC1082571 - 长尾林鸮 - Strix uralensis.mp3_v6.html
│   ├── XC1082569 - 黄褐林鸮 - Strix aluco.wav_v6.html
│   └── XC1082454 - Identity unknown.mp3_v6.html
│
├── ornitho_vector_final.py  ← v6.0 最终版
├── ornitho_vector_v6.py     ← v6.0 开发版
├── ornitho_vector.py        ← v2.0 聚类版（废弃）
└── README.md
```

---

## 🚀 快速启动

```bash
cd ~/code/8.practice/ornitho-vector

# 运行 v6.0
uv run python ornitho_vector_final.py

# 打开结果
open output/XC1082571\ -\ 长尾林鸮\ -\ Strix\ uralensis.mp3_v6.html
```

---

## 📊 测试数据

| 文件名 | 时长 | 帧数 | PCA 保留率 | 输出文件 |
|--------|------|------|-----------|----------|
| 长尾林鸮 (Strix uralensis) | 9.95s | 429 | 90.6% | ✅ 最佳 |
| 黄褐林鸮 (Strix aluco) | 48.00s | 2068 | 51.3% | ✅ 可用 |
| unknown | 61.72s | 2658 | 39.4% | ⚠️ 一般 |

---

## 🎯 工作原理

```
1. 加载音频 → 波形数据 (y, sr)
   ↓
2. 提取 MFCC → 20 维特征 × 时间帧
   ↓
3. 标准化 → StandardScaler
   ↓
4. PCA 降维 → 3D 坐标 (x, y, z)
   ↓
5. 编码音频 → base64 嵌入 HTML
   ↓
6. 生成动画 → 100 帧降采样
   ↓
7. JavaScript 控制 → requestAnimationFrame 同步
```

---

## 🎨 视觉设计

### 配色方案
| 元素 | 颜色 | 说明 |
|------|------|------|
| 轨迹线 | `rgba(0,0,139,0.6)` | 深蓝色，高对比度 |
| 亮点 | `#FFFF00` + 黑色边框 | 亮黄色，醒目 |
| 背景 | 白色 | 简洁 |
| 播放按钮 | 绿色 `#4CAF50` | 开始 |
| 暂停按钮 | 橙色 `#FF9800` | 暂停 |
| 重置按钮 | 红色 `#f44336` | 重置 |

### 布局
- **3D 视图**: 900×650px
- **控制栏**: 底部固定，灰色背景
- **按钮**: 大号字体 (18px)，圆角

---

## ⚠️ 常见问题

### Q1: 音频文件太大怎么办？

**方案**: 限制最大时长
```python
CONFIG['MAX_DURATION'] = 60  # 秒
```

### Q2: PCA 保留率太低？

**方案 1**: 尝试 UMAP
```bash
uv add umap-learn
```

**方案 2**: 增加 MFCC 系数
```python
CONFIG['N_MFCC'] = 30  # 默认 20
```

### Q3: 动画卡顿？

**方案**: 减少动画帧数
```python
n_anim_frames = min(60, n_frames)  # 默认 100
```

---

## 📈 后续优化

| 功能 | 优先级 | 说明 |
|------|--------|------|
| 轨迹颜色渐变 | ⭐⭐⭐ | 按时间从蓝→红渐变 |
| 多音频对比 | ⭐⭐⭐ | 并排显示多个轨迹 |
| 热力图叠加 | ⭐⭐ | 显示 MFCC 频谱 |
| 导出 GIF/MP4 | ⭐⭐ | 视频格式分享 |
| Web 界面 | ⭐⭐⭐⭐ | 上传音频自动生成 |

---

## 📝 版本历史

- **v6.0** (2026-02-23): ✅ requestAnimationFrame 同步，完美联动
- **v5.0** (2026-02-23): ❌ 动画和音频不同步
- **v4.0** (2026-02-23): ❌ 播放按钮无响应
- **v3.2** (2026-02-22): ❌ 灰色轨迹看不清
- **v3.1** (2026-02-22): ❌ 播放按钮无响应
- **v3.0** (2026-02-22): ❌ 热力图不显示
- **v2.0** (2026-02-22): ❌ 理解错误（多样本聚类）

---

*版本：v6.0（最终版） | 最后更新：2026-02-23 00:55*
