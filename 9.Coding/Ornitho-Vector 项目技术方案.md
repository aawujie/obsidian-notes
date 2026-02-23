# Ornitho-Vector：基于声学流形的鸟鸣三维可视化系统

**创建日期**:: 2026-02-22  
**项目类型**:: 技术方案 / 音频可视化  
**技术栈**:: Python, librosa, PCA, Plotly  
**状态**:: 📋 方案待实施

---

## 📋 项目全景技术方案 (Project Master Plan)

### 1. 系统架构概览

将整个系统划分为四个独立的层级（Layers），以保证代码的解耦和可维护性：

| 层级 | 名称 | 职责 |
|------|------|------|
| **Layer 1** | 基础设施层 (Infrastructure) | 文件管理、环境依赖 |
| **Layer 2** | ETL 处理层 (Extract-Transform-Load) | 音频加载、静音切除、预处理 |
| **Layer 3** | 核心算法层 (Core Algorithm) | MFCC 特征提取、特征聚合、数据标准化、PCA 降维 |
| **Layer 4** | 表现层 (Presentation) | 3D 坐标映射、交互式场景构建、动画渲染 |

---

### 2. 模块详细设计与实现细节

#### 模块一：基础设施与环境 (Infrastructure)

**目录结构设计**：

```text
/Project_Ornitho
│
├── /raw_audio/              # [输入] 存放原始 .wav/.mp3 鸟鸣文件
│   ├── /sparrow/            # 按鸟类品种分类（可选，用于自动打标签）
│   └── /crow/
│
├── /processed_data/         # [中间产物] 存放清洗后的数据
│   └── features.csv         # 提取出的高维特征表
│
├── /output/                 # [输出] 存放最终的可视化结果
│   └── 3d_manifold.html     # 交互式 3D 网页
│
├── main.py                  # 主程序入口
├── config.py                # 配置文件（采样率、MFCC 数量等）
└── utils.py                 # 工具函数包
```

**技术栈依赖 (requirements.txt)**：

| 库 | 用途 |
|------|------|
| `librosa` | 音频处理的核心库 |
| `numpy` | 矩阵运算 |
| `pandas` | 结构化数据管理（像 Excel 一样管理特征） |
| `scikit-learn` | 提供 PCA 和数据标准化工具 |
| `plotly` | 生成支持 WebGL 加速的 3D 交互图表（实现"展示模式"的关键） |

---

#### 模块二：音频预处理 (Audio Preprocessing)

**痛点**：原始录音通常包含大量的背景白噪音（风声、电流声）以及长段的空白。如果不处理，机器会把"静音"也当成特征，导致分析结果全部挤在原点。

**详细步骤**：

1. **重采样 (Resampling)**
   - 强制将所有音频转为 `22050 Hz` 单声道
   - 这是音频分析的黄金标准频率，既保留了人耳听觉范围，又减少了数据量

2. **静音移除 (Silence Trimming)**
   - 使用能量阈值算法
   - 切掉音频开头和结尾低于 60dB 的静音片段

3. **定长切片 (Optional)**
   - 如果录音特别长，需要将其切分为多个 3~5 秒的片段
   - 增加样本数量

---

#### 模块三：核心算法层 —— 从 MFCC 到特征向量

这是最"数学"的部分，也是把声音变成数字的关键。

**1. 特征提取策略 (Feature Extraction Strategy)**

MFCC 计算出来是一个 `(特征数，时间帧)` 的矩阵。例如，一段 5 秒的音频，可能生成 `(13, 215)` 的矩阵。

但是，PCA 算法要求**每一个样本必须是一个固定长度的一维向量**。

因此，我们必须对时间维度进行**聚合 (Aggregation)**。

**2. 具体的数学操作**：

对于每一段音频的 MFCC 矩阵（假设有 20 个 MFCC 系数）：

| 操作 | 说明 | 输出 |
|------|------|------|
| **计算均值 (Mean)** | 这只鸟在整段录音中的"平均音色" | 20 个数值 |
| **计算方差 (Variance)** | 这只鸟叫声的"变化剧烈程度" | 20 个数值 |
| **拼接 (Concatenation)** | 将均值和方差拼起来 | **40 维向量** |

**3. 数据标准化 (Standardization) —— *极其重要***

MFCC 的第一个系数（能量）通常很大（比如 -200 到 200），而其他系数很小（-10 到 10）。如果不处理，PCA 会误以为第一个系数最重要，忽略其他细节。

**解决方案**：使用 `StandardScaler`，将所有特征缩放到 `均值=0, 方差=1` 的标准正态分布。

---

#### 模块四：降维层 (PCA Dimensionality Reduction)

**目标**：将 40 维的向量压缩到 3 维。

**逻辑流程**：

1. 构建一个大矩阵 `X`，形状为 `(样本数 N, 40)`
2. 初始化 PCA，设置 `n_components=3`
3. 执行运算，得到新矩阵 `X_new`，形状为 `(样本数 N, 3)`
4. 这三列数据分别命名为 `PC1 (x)`, `PC2 (y)`, `PC3 (z)`

---

#### 模块五：表现层 —— 3D 可视化与展示模式

**需求实现**：

| 功能 | 实现方式 |
|------|----------|
| **3D 坐标** | 使用 PCA 输出的 X, Y, Z |
| **旋转与交互** | Plotly 引擎生成的 HTML 自带 3D 引擎，支持鼠标拖拽旋转、滚轮缩放 |
| **展示模式 (Display Mode)** | 通过设置摄像机轨道 (Camera Orbital) 参数，让视图更加美观 |

---

### 3. 核心代码逻辑

```python
"""
Ornitho-Vector 系统核心逻辑代码
"""
import librosa
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import os

# =================配置区域=================
CONFIG = {
    'SR': 22050,        # 采样率
    'N_MFCC': 20,       # 提取多少个 MFCC 系数
    'HOP_LENGTH': 512,  # 帧移
    'INPUT_DIR': './raw_audio',  # 音频输入路径
}
# =========================================


def step_1_load_and_extract(file_path):
    """
    负责读取音频，并把波形变成一个 40 维的向量
    """
    try:
        # 1. 加载音频 (自动转为单声道 mono=True)
        y, sr = librosa.load(file_path, sr=CONFIG['SR'])
        
        # 2. 静音切除 (去除首尾静音，top_db=20 表示切掉低于 20 分贝的声音)
        y_trimmed, _ = librosa.effects.trim(y, top_db=20)
        
        if len(y_trimmed) < 1024:
            return None  # 忽略太短的杂音
        
        # 3. 提取 MFCC
        # 结果形状：(20, 时间帧数)
        mfcc = librosa.feature.mfcc(y=y_trimmed, sr=sr, n_mfcc=CONFIG['N_MFCC'])
        
        # 4. 特征聚合 (核心步骤：将时间维度压扁)
        # axis=1 表示沿着时间轴计算
        mfcc_mean = np.mean(mfcc, axis=1)  # 计算 20 个系数的平均值
        mfcc_var = np.var(mfcc, axis=1)    # 计算 20 个系数的方差
        
        # 5. 拼接向量 (20 + 20 = 40 维)
        feature_vector = np.concatenate((mfcc_mean, mfcc_var))
        
        return feature_vector
    
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None


def step_2_build_dataset(folder_path):
    """
    遍历文件夹，构建数据表
    """
    features_list = []
    labels = []
    filenames = []
    
    # 遍历所有子文件夹 (假设文件夹名就是鸟的种类)
    for label in os.listdir(folder_path):
        sub_dir = os.path.join(folder_path, label)
        if os.path.isdir(sub_dir):
            for file in os.listdir(sub_dir):
                if file.endswith('.wav') or file.endswith('.mp3'):
                    path = os.path.join(sub_dir, file)
                    
                    # 提取特征
                    vector = step_1_load_and_extract(path)
                    
                    if vector is not None:
                        features_list.append(vector)
                        labels.append(label)  # 记录鸟的种类
                        filenames.append(file)
                        print(f"Processed: {file}")
    
    # 转换为 DataFrame 方便后续处理
    df = pd.DataFrame(features_list)
    df['label'] = labels
    df['filename'] = filenames
    
    return df


def step_3_dimensionality_reduction(df):
    """
    执行标准化和 PCA
    """
    # 1. 分离特征数据 (去掉标签和文件名列)
    X = df.drop(['label', 'filename'], axis=1).values
    
    # 2. 数据标准化 (StandardScaler)
    # 这一步至关重要，让所有数据处于同一量级
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 3. PCA 降维 (40 维 -> 3 维)
    pca = PCA(n_components=3)
    principal_components = pca.fit_transform(X_scaled)
    
    # 4. 将结果存回 DataFrame
    df['pc_x'] = principal_components[:, 0]
    df['pc_y'] = principal_components[:, 1]
    df['pc_z'] = principal_components[:, 2]
    
    # 计算保留了多少信息量 (可选打印)
    print(f"信息保留率：{sum(pca.explained_variance_ratio_):.2f}")
    
    return df


def step_4_visualization(df):
    """
    生成可交互的 3D 图表
    """
    print("正在生成 3D 渲染...")
    
    # 使用 Plotly Express 创建 3D 散点图
    fig = px.scatter_3d(
        df,
        x='pc_x', y='pc_y', z='pc_z',
        color='label',           # 不同种类的鸟显示不同颜色
        hover_name='filename',   # 鼠标悬停显示文件名
        opacity=0.8,             # 稍微透明一点，增加立体感
        size_max=10              # 点的大小
    )
    
    # 这里的设置是为了满足您的"展示模式"需求
    fig.update_layout(
        title="鸟鸣声景三维流形 (Bird Soundscape Manifold)",
        # 设置深色背景 (Dark Mode)，像星空一样
        template="plotly_dark",
        # 隐藏坐标轴的刻度，只保留空间感
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
        ),
        # 调整初始摄像机位置
        scene_camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.2)
        ),
        margin=dict(l=0, r=0, b=0, t=30)  # 撑满全屏
    )
    
    # 导出为 HTML 文件
    output_file = "Bird_Visualization.html"
    fig.write_html(output_file)
    print(f"成功！请在浏览器打开：{output_file}")


# =================主程序运行入口=================
if __name__ == "__main__":
    # 1. 构建数据集
    print("阶段 1: 正在提取声学特征...")
    raw_df = step_2_build_dataset(CONFIG['INPUT_DIR'])
    
    if len(raw_df) > 0:
        # 2. 降维
        print("阶段 2: 正在进行 PCA 降维...")
        final_df = step_3_dimensionality_reduction(raw_df)
        
        # 3. 可视化
        step_4_visualization(final_df)
    else:
        print("错误：没有找到有效的音频数据。")
```

---

### 4. 方案亮点与功能解析

#### 1. 为什么这个方案能成？

| 关键点 | 说明 |
|--------|------|
| **高维特征对齐** | 通过计算 Mean 和 Variance，我们解决了"音频长短不一"的问题，这是所有音频 AI 项目的第一道坎 |
| **数学严谨性** | 引入了 `StandardScaler`。如果不标准化，响度大的鸟叫会因为数值大而占据主导，导致聚类失败。加上这一步，我们比较的是"音色"而不是"音量" |

#### 2. 关于"3D 坐标"与"展示模式"

这个方案生成的 `.html` 文件是完全独立的：

| 特性 | 说明 |
|------|------|
| **交互性** | 您不需要写任何前端代码。生成的页面直接支持 WebGL |
| **展示效果** | 代码中配置了 `template="plotly_dark"` 和隐藏坐标轴 (`visible=False`)，这意味着最终效果看起来不像枯燥的统计图表，而像是一个悬浮在太空中的**粒子云** |
| **旋转** | 在浏览器中，按住鼠标左键即可随意旋转流形；按住右键可以平移 |

#### 3. 如何启动？

您只需要准备好音频文件，安装好 Python 和依赖库，把上面的代码保存为 `.py` 文件运行，所有的复杂的数学运算、降维、渲染都会在几秒钟内自动完成，最后吐出一个网页文件给您展示。

---

## 🔗 相关参考

- **灵感来源**: lucioarese YouTube 频道 - "Seeing Birdsong" 项目
- **类似技术**: 音频流形学习 (Audio Manifold Learning)、生物声学可视化 (Bioacoustics Visualization)

---

## 📝 待办事项

- [ ] 准备鸟鸣音频样本（建议至少 20-30 段，涵盖 2-3 种鸟类）
- [ ] 创建项目目录结构
- [ ] 安装 Python 依赖 (`pip install librosa numpy pandas scikit-learn plotly`)
- [ ] 运行测试并调整参数
- [ ] 优化可视化效果（颜色、透明度、摄像机角度）

---

*最后更新：2026-02-22*
