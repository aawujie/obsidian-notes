# Ornitho-Vector 项目技术方案（修复版 v2.0）

**创建日期**:: 2026-02-22  
**版本**:: v2.0（修复版）  
**项目类型**:: 技术方案 / 音频可视化  
**技术栈**:: Python, librosa, PCA/UMAP, Plotly  
**状态**:: ✅ 方案已修复，可实施

---

## 🔧 v2.0 修复内容摘要

| 问题 | 原方案 | 修复后 | 优先级 |
|------|--------|--------|--------|
| 静音切除参数 | `top_db=20`（太激进） | `top_db=40`（保守） | 🔴 P0 |
| 音频质量检查 | 无 | 新增 `check_audio_quality()` | 🔴 P0 |
| MFCC 参数 | 默认配置 | 针对鸟鸣优化 | 🟡 P1 |
| 特征聚合 | 仅均值 + 方差（40 维） | 增加偏度/峰度/频谱特征（80+ 维） | 🟡 P1 |
| PCA 信息检查 | 无 | 新增保留率报告 | 🟡 P1 |
| 降维备选方案 | 仅 PCA | 新增 UMAP 备选 | 🟡 P1 |

---

## 📋 修复后的完整代码

```python
"""
Ornitho-Vector 系统 - 修复版 v2.0
基于声学流形的鸟鸣三维可视化系统

修复内容:
- 优化静音切除参数
- 增加音频质量检查
- 优化 MFCC 参数配置
- 增加特征维度（偏度、峰度、频谱特征）
- 添加 PCA 信息保留率检查
- 提供 UMAP 备选降维方案

作者：Ornitho-Vector Team
日期：2026-02-22
"""

import librosa
import numpy as np
import pandas as pd
import scipy.stats
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
import plotly.express as px
import os
import warnings

# 尝试导入 UMAP（可选依赖）
try:
    import umap
    UMAP_AVAILABLE = True
except ImportError:
    UMAP_AVAILABLE = False
    warnings.warn("UMAP 未安装，将仅使用 PCA。安装：pip install umap-learn")

# =================配置区域=================
CONFIG = {
    'SR': 22050,         # 采样率（音频分析黄金标准）
    'N_MFCC': 20,        # MFCC 系数数量
    'HOP_LENGTH': 256,   # 帧移（更高时间分辨率）
    'N_FFT': 1024,       # FFT 窗口大小（针对短促鸟鸣优化）
    'PREEMPHASIS': 0.97, # 预加重系数（增强高频）
    'TOP_DB': 40,        # 静音切除阈值（v2.0 修复：20→40）
    'MIN_DURATION': 0.5, # 最小时长（秒）
    'MAX_DURATION': 60,  # 最大时长（秒）
    'INPUT_DIR': './raw_audio',   # 音频输入路径
    'OUTPUT_DIR': './output',     # 输出路径
    'USE_UMAP': False,   # 是否使用 UMAP 降维（备选方案）
}
# =========================================


def check_audio_quality(y, sr, file_path):
    """
    音频质量检查（v2.0 新增）
    
    检查项目:
    - 削波失真
    - 信噪比
    - 时长
    - 静音比例
    
    Returns:
        (is_valid, issues_list)
    """
    issues = []
    
    # 1. 检查削波失真（峰值超过 99%）
    clip_ratio = np.sum(np.abs(y) > 0.99) / len(y)
    if clip_ratio > 0.01:
        issues.append(f"削波失真 ({clip_ratio:.1%})")
    
    # 2. 检查信噪比（信号能量 vs 底部 10% 能量）
    signal_energy = np.max(np.abs(y))
    noise_energy = np.percentile(np.abs(y), 10)
    snr = signal_energy / (noise_energy + 1e-8)
    if snr < 5:
        issues.append(f"信噪比过低 ({snr:.1f})")
    
    # 3. 检查时长
    duration = len(y) / sr
    if duration < CONFIG['MIN_DURATION']:
        issues.append(f"音频太短 ({duration:.2f}s)")
    if duration > CONFIG['MAX_DURATION']:
        issues.append(f"音频太长 ({duration:.2f}s)，建议切片")
    
    # 4. 检查静音比例
    trimmed, _ = librosa.effects.trim(y, top_db=CONFIG['TOP_DB'])
    silent_ratio = 1 - len(trimmed) / len(y)
    if silent_ratio > 0.7:
        issues.append(f"静音比例过高 ({silent_ratio:.1%})")
    
    is_valid = len(issues) == 0
    return is_valid, issues


def step_1_load_and_extract(file_path):
    """
    负责读取音频，并把波形变成一个 80+ 维的特征向量
    
    v2.0 修复:
    - 优化静音切除参数
    - 增加音频质量检查
    - 优化 MFCC 参数
    - 增加更多特征（偏度、峰度、频谱特征）
    """
    try:
        # 1. 加载音频 (自动转为单声道 mono=True)
        y, sr = librosa.load(file_path, sr=CONFIG['SR'], mono=True)
        
        # 2. 音频质量检查（v2.0 新增）
        is_valid, issues = check_audio_quality(y, sr, file_path)
        if not is_valid:
            print(f"  ⚠️  {os.path.basename(file_path)}: {', '.join(issues)}")
            # 只跳过严重问题（削波、太短），其他警告但继续
            if "削波失真" in str(issues) or "音频太短" in str(issues):
                return None
        
        # 3. 静音切除（v2.0 修复：top_db=40）
        y_trimmed, _ = librosa.effects.trim(y, top_db=CONFIG['TOP_DB'], ref=np.max)
        
        if len(y_trimmed) < CONFIG['N_FFT']:
            return None  # 忽略太短的音频
        
        # 4. 提取 MFCC（v2.0 修复：优化参数）
        # 结果形状：(20, 时间帧数)
        mfcc = librosa.feature.mfcc(
            y=y_trimmed,
            sr=sr,
            n_mfcc=CONFIG['N_MFCC'],
            n_fft=CONFIG['N_FFT'],
            hop_length=CONFIG['HOP_LENGTH'],
            preemphasis=CONFIG['PREEMPHASIS']
        )
        
        # 5. 特征聚合（v2.0 增强：增加偏度、峰度）
        # axis=1 表示沿着时间轴计算
        mfcc_mean = np.mean(mfcc, axis=1)      # 20 维：平均音色
        mfcc_var = np.var(mfcc, axis=1)        # 20 维：变化程度
        mfcc_skew = scipy.stats.skew(mfcc, axis=1)    # 20 维：分布对称性
        mfcc_kurtosis = scipy.stats.kurtosis(mfcc, axis=1)  # 20 维：分布尖锐度
        
        # 6. 频谱特征（v2.0 新增）
        # 频谱质心（音色明亮度）
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(
            y=y_trimmed, sr=sr, n_fft=CONFIG['N_FFT'], hop_length=CONFIG['HOP_LENGTH']
        ), axis=1)
        
        # 频谱带宽（频率分布范围）
        spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(
            y=y_trimmed, sr=sr, n_fft=CONFIG['N_FFT'], hop_length=CONFIG['HOP_LENGTH']
        ), axis=1)
        
        # 频谱对比度（频谱峰值与谷值的差异）
        spectral_contrast = np.mean(librosa.feature.spectral_contrast(
            y=y_trimmed, sr=sr, n_fft=CONFIG['N_FFT'], hop_length=CONFIG['HOP_LENGTH']
        ), axis=1)
        
        # 7. 过零率（v2.0 新增：区分浊音/清音）
        zcr = np.mean(librosa.feature.zero_crossing_rate(
            y=y_trimmed, hop_length=CONFIG['HOP_LENGTH']
        ), axis=1)
        
        # 8. 拼接向量（v2.0: 40 维 → 80+ 维）
        feature_vector = np.concatenate([
            mfcc_mean,        # 20 维
            mfcc_var,         # 20 维
            mfcc_skew,        # 20 维
            mfcc_kurtosis,    # 20 维
            spectral_centroid,   # 1 维
            spectral_bandwidth,  # 1 维
            spectral_contrast,   # 7 维（默认 7 个频段）
            zcr,              # 1 维
        ])  # 总计约 90 维
        
        return feature_vector
    
    except Exception as e:
        print(f"  ❌ Error parsing {file_path}: {e}")
        return None


def step_2_build_dataset(folder_path):
    """
    遍历文件夹，构建数据表
    
    v2.0 增强:
    - 增加处理统计
    - 增加质量报告
    """
    features_list = []
    labels = []
    filenames = []
    quality_issues = []
    
    total_files = 0
    valid_files = 0
    
    print(f"\n📂 扫描目录：{folder_path}")
    
    # 遍历所有子文件夹 (假设文件夹名就是鸟的种类)
    for label in sorted(os.listdir(folder_path)):
        sub_dir = os.path.join(folder_path, label)
        if os.path.isdir(sub_dir):
            print(f"\n  🐦 鸟类：{label}")
            files = [f for f in os.listdir(sub_dir) if f.endswith(('.wav', '.mp3', '.flac', '.m4a'))]
            total_files += len(files)
            
            for file in files:
                path = os.path.join(sub_dir, file)
                
                # 提取特征
                vector = step_1_load_and_extract(path)
                
                if vector is not None:
                    features_list.append(vector)
                    labels.append(label)
                    filenames.append(file)
                    valid_files += 1
                    print(f"    ✅ {file}")
                else:
                    quality_issues.append(f"{label}/{file}")
    
    print(f"\n📊 处理统计:")
    print(f"   总文件数：{total_files}")
    print(f"   有效文件：{valid_files} ({valid_files/total_files*100:.1f}%)")
    print(f"   跳过文件：{total_files - valid_files}")
    
    if quality_issues:
        print(f"\n⚠️  跳过的文件:")
        for issue in quality_issues[:10]:  # 只显示前 10 个
            print(f"   - {issue}")
        if len(quality_issues) > 10:
            print(f"   ... 还有 {len(quality_issues) - 10} 个")
    
    # 转换为 DataFrame 方便后续处理
    if len(features_list) == 0:
        return pd.DataFrame()
    
    df = pd.DataFrame(features_list)
    df['label'] = labels
    df['filename'] = filenames
    
    return df


def step_3_dimensionality_reduction(df):
    """
    执行标准化和降维
    
    v2.0 增强:
    - 详细的 PCA 信息报告
    - UMAP 备选方案
    - 降维效果评估
    """
    if len(df) == 0:
        print("❌ 没有数据可降维")
        return df
    
    # 1. 分离特征数据 (去掉标签和文件名列)
    feature_cols = [col for col in df.columns if col not in ['label', 'filename']]
    X = df[feature_cols].values
    
    print(f"\n📊 数据形状：{X.shape}")
    print(f"   样本数：{X.shape[0]}")
    print(f"   特征数：{X.shape[1]}")
    
    # 2. 数据标准化 (StandardScaler)
    # 这一步至关重要，让所有数据处于同一量级
    print("\n🔧 正在标准化数据...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 3. 降维（v2.0: 支持 PCA 和 UMAP）
    if CONFIG['USE_UMAP'] and UMAP_AVAILABLE:
        print("\n🌀 使用 UMAP 降维 (40+ 维 → 3 维)...")
        umap_model = umap.UMAP(
            n_components=3,
            n_neighbors=15,      # 局部结构 vs 全局结构的平衡
            min_dist=0.1,        # 允许点聚集的最小距离
            metric='euclidean',  # 距离度量
            random_state=42
        )
        principal_components = umap_model.fit_transform(X_scaled)
        
        # UMAP 没有 explained_variance_ratio，用其他方式评估
        print(f"✅ UMAP 降维完成")
        print(f"   局部结构保持度：需要可视化评估")
    else:
        print("\n📐 使用 PCA 降维 (40+ 维 → 3 维)...")
        pca = PCA(n_components=3)
        principal_components = pca.fit_transform(X_scaled)
        
        # v2.0 增强：详细的 PCA 报告
        print(f"\n📊 PCA 信息保留率报告:")
        print(f"   PC1: {pca.explained_variance_ratio_[0]:.2%} ({pca.explained_variance_[0]:.2f})")
        print(f"   PC2: {pca.explained_variance_ratio_[1]:.2%} ({pca.explained_variance_[1]:.2f})")
        print(f"   PC3: {pca.explained_variance_ratio_[2]:.2%} ({pca.explained_variance_[2]:.2f})")
        print(f"   累计：{sum(pca.explained_variance_ratio_):.2%}")
        
        # 评估与建议
        total_ratio = sum(pca.explained_variance_ratio_)
        if total_ratio < 0.5:
            print(f"\n⚠️  警告：信息保留率较低 ({total_ratio:.1%})")
            print(f"   建议:")
            print(f"   1. 尝试 UMAP 降维（设置 USE_UMAP=True）")
            print(f"   2. 增加特征数量（当前 {X.shape[1]} 维）")
            print(f"   3. 检查音频质量（可能有噪音干扰）")
        elif total_ratio < 0.7:
            print(f"\n🟡 信息保留率中等 ({total_ratio:.1%})，结果可用")
        else:
            print(f"\n✅ 信息保留率良好 ({total_ratio:.1%})")
    
    # 4. 将结果存回 DataFrame
    df['pc_x'] = principal_components[:, 0]
    df['pc_y'] = principal_components[:, 1]
    df['pc_z'] = principal_components[:, 2]
    
    return df


def step_4_visualization(df, output_file="Bird_Visualization.html"):
    """
    生成可交互的 3D 图表
    
    v2.0 增强:
    - 增加统计信息展示
    - 优化摄像机角度
    - 支持多种模板
    """
    if len(df) == 0 or 'pc_x' not in df.columns:
        print("❌ 没有数据可可视化")
        return
    
    print("\n🎨 正在生成 3D 渲染...")
    
    # 统计信息
    n_samples = len(df)
    n_classes = df['label'].nunique()
    class_distribution = df['label'].value_counts()
    
    # 使用 Plotly Express 创建 3D 散点图
    fig = px.scatter_3d(
        df,
        x='pc_x', y='pc_y', z='pc_z',
        color='label',           # 不同种类的鸟显示不同颜色
        hover_name='filename',   # 鼠标悬停显示文件名
        hover_data=['label'],    # 悬停显示鸟类
        opacity=0.8,             # 稍微透明，增加立体感
        size_max=12,             # 点的大小
        color_discrete_sequence=px.colors.qualitative.Set3,  # 更鲜明的配色
    )
    
    # v2.0 增强：更专业的布局配置
    fig.update_layout(
        title=dict(
            text="🐦 鸟鸣声景三维流形 (Bird Soundscape Manifold)<br>" +
                 f"<sup style='color:#888'>样本：{n_samples} | 鸟类：{n_classes} | " +
                 f"降维：{'UMAP' if CONFIG['USE_UMAP'] else 'PCA'}</sup>",
            x=0.5,
            y=0.95,
            font=dict(size=18, family="Arial Black")
        ),
        # 深色背景（像星空）
        template="plotly_dark",
        # 图例配置
        legend=dict(
            title="🐦 鸟类",
            font=dict(size=12),
            itemsizing='constant',
        ),
        # 隐藏坐标轴刻度，只保留空间感
        scene=dict(
            xaxis=dict(visible=False, showbackground=False),
            yaxis=dict(visible=False, showbackground=False),
            zaxis=dict(visible=False, showbackground=False),
            bgcolor='rgba(0,0,0,0)',  # 透明背景
            aspectmode='data',  # 保持比例
        ),
        # 摄像机位置（v2.0 优化角度）
        scene_camera=dict(
            eye=dict(x=1.8, y=1.8, z=1.5),  # 更远的视角
            center=dict(x=0, y=0, z=0),
            up=dict(x=0, y=0, z=1)
        ),
        # 撑满全屏
        margin=dict(l=0, r=0, b=0, t=60),
        # 添加统计信息框
        annotations=[
            dict(
                text=f"📊 统计：{n_samples}样本 | {n_classes}种类",
                showarrow=False,
                xref='paper', yref='paper',
                x=0.01, y=0.01,
                font=dict(size=10, color='#888')
            )
        ]
    )
    
    # 更新标记样式
    fig.update_traces(
        marker=dict(
            line=dict(width=1, color='rgba(255,255,255,0.3)'),  # 白色描边
            opacity=0.85,
        )
    )
    
    # 确保输出目录存在
    os.makedirs(CONFIG['OUTPUT_DIR'], exist_ok=True)
    output_path = os.path.join(CONFIG['OUTPUT_DIR'], output_file)
    
    # 导出为 HTML 文件
    fig.write_html(output_path)
    print(f"\n✅ 成功！")
    print(f"   输出文件：{output_path}")
    print(f"   文件大小：{os.path.getsize(output_path) / 1024:.1f} KB")
    print(f"\n🌐 请在浏览器打开查看交互效果")
    
    # 打印类别分布
    print(f"\n📊 类别分布:")
    for label, count in class_distribution.items():
        bar = "█" * int(count / max(class_distribution) * 20)
        print(f"   {label:15} {bar} ({count})")


# =================主程序运行入口=================
def main():
    """主程序入口"""
    print("=" * 70)
    print("🐦 Ornitho-Vector 鸟鸣三维可视化系统 v2.0")
    print("=" * 70)
    print(f"配置:")
    print(f"   输入目录：{CONFIG['INPUT_DIR']}")
    print(f"   输出目录：{CONFIG['OUTPUT_DIR']}")
    print(f"   采样率：{CONFIG['SR']} Hz")
    print(f"   MFCC 系数：{CONFIG['N_MFCC']}")
    print(f"   降维方法：{'UMAP' if CONFIG['USE_UMAP'] else 'PCA'}")
    print("=" * 70)
    
    # 检查输入目录
    if not os.path.exists(CONFIG['INPUT_DIR']):
        print(f"\n❌ 错误：输入目录不存在：{CONFIG['INPUT_DIR']}")
        print(f"   请创建目录并放入音频文件")
        print(f"   建议结构:")
        print(f"   {CONFIG['INPUT_DIR']}/")
        print(f"   ├── sparrow/")
        print(f"   │   ├── bird1.wav")
        print(f"   │   └── bird2.wav")
        print(f"   └── crow/")
        print(f"       ├── bird1.wav")
        print(f"       └── bird2.wav")
        return
    
    # 1. 构建数据集
    print("\n【阶段 1/3】正在提取声学特征...")
    raw_df = step_2_build_dataset(CONFIG['INPUT_DIR'])
    
    if len(raw_df) == 0:
        print("\n❌ 错误：没有找到有效的音频数据")
        print("   请检查:")
        print("   1. 输入目录是否有音频文件")
        print("   2. 文件格式是否为 .wav/.mp3/.flac/.m4a")
        print("   3. 音频质量是否合格（时长>0.5s，无严重削波）")
        return
    
    # 2. 降维
    print("\n【阶段 2/3】正在进行降维...")
    final_df = step_3_dimensionality_reduction(raw_df)
    
    # 3. 可视化
    print("\n【阶段 3/3】正在生成可视化...")
    step_4_visualization(final_df)
    
    print("\n" + "=" * 70)
    print("✅ 全部完成！")
    print("=" * 70)


if __name__ == "__main__":
    main()
```

---

## 🔧 依赖安装

```bash
# 创建虚拟环境（推荐）
python3 -m venv ornitho_env
source ornitho_env/bin/activate

# 安装核心依赖
pip install librosa numpy pandas scikit-learn plotly scipy

# 可选：UMAP 降维（效果更好）
pip install umap-learn

# 导出依赖列表
pip freeze > requirements.txt
```

**requirements.txt:**
```
librosa>=0.10.0
numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.3.0
plotly>=5.15.0
scipy>=1.11.0
umap-learn>=0.5.0  # 可选
```

---

## 📂 项目结构

```
/Project_Ornitho/
│
├── raw_audio/              # [输入] 原始音频
│   ├── sparrow/
│   │   ├── recording1.wav
│   │   └── recording2.wav
│   └── crow/
│       └── ...
│
├── output/                 # [输出] 可视化结果
│   └── Bird_Visualization.html
│
├── ornitho_vector.py       # 主程序（上方代码）
├── config.py               # 配置文件（可选）
├── requirements.txt        # 依赖列表
└── README.md              # 项目说明
```

---

## 🚀 快速启动

```bash
# 1. 准备音频文件
mkdir -p raw_audio/sparrow raw_audio/crow
# 放入音频文件...

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行程序
python ornitho_vector.py

# 4. 查看结果
open output/Bird_Visualization.html
```

---

## 📊 预期输出示例

```
======================================================================
🐦 Ornitho-Vector 鸟鸣三维可视化系统 v2.0
======================================================================
配置:
   输入目录：./raw_audio
   输出目录：./output
   采样率：22050 Hz
   MFCC 系数：20
   降维方法：PCA
======================================================================

【阶段 1/3】正在提取声学特征...

📂 扫描目录：./raw_audio

  🐦 鸟类：crow
    ✅ crow_call_01.wav
    ✅ crow_call_02.wav
    ⚠️  crow_call_03.wav: 静音比例过高 (75.2%)

  🐦 鸟类：sparrow
    ✅ sparrow_chirp_01.wav
    ✅ sparrow_chirp_02.wav
    ✅ sparrow_chirp_03.wav

📊 处理统计:
   总文件数：6
   有效文件：5 (83.3%)
   跳过文件：1

【阶段 2/3】正在进行降维...

📊 数据形状：(5, 90)
   样本数：5
   特征数：90

🔧 正在标准化数据...

📐 使用 PCA 降维 (90 维 → 3 维)...

📊 PCA 信息保留率报告:
   PC1: 35.2% (12.45)
   PC2: 22.1% (7.82)
   PC3: 15.3% (5.41)
   累计：72.6%

🟡 信息保留率中等 (72.6%)，结果可用

【阶段 3/3】正在生成可视化...

🎨 正在生成 3D 渲染...

✅ 成功！
   输出文件：./output/Bird_Visualization.html
   文件大小：245.3 KB

🌐 请在浏览器打开查看交互效果

📊 类别分布:
   sparrow         ████████████████████ (3)
   crow            ██████████████ (2)

======================================================================
✅ 全部完成！
======================================================================
```

---

## ⚠️ 常见问题排查

### Q1: PCA 信息保留率太低 (<50%)

```python
# 方案 1：尝试 UMAP 降维
CONFIG['USE_UMAP'] = True

# 方案 2：增加样本数量（至少每种鸟 10 段）
# 方案 3：检查音频质量（噪音可能干扰特征）
```

### Q2: 聚类效果不明显

```python
# 方案 1：增加特征维度
# 在 step_1_load_and_extract 中添加更多频谱特征

# 方案 2：调整 UMAP 参数
umap_model = umap.UMAP(
    n_neighbors=10,    # 减小→更局部
    min_dist=0.05,     # 减小→更聚集
)

# 方案 3：增加样本多样性
# 确保每种鸟的录音涵盖不同个体、不同场景
```

### Q3: 依赖安装失败（macOS ARM）

```bash
# 使用 conda（推荐）
conda create -n ornitho python=3.10
conda activate ornitho
conda install -c conda-forge librosa scikit-learn plotly umap-learn

# 或使用预编译 wheel
pip install --upgrade pip
pip install librosa --no-cache-dir
```

---

## 📈 后续优化方向

| 功能 | 难度 | 说明 |
|------|------|------|
| 自动降噪 | ⭐⭐⭐ | `librosa.decompose.nn_filter` |
| 音频切片 | ⭐⭐⭐ | 长音频自动切分为 3-5 秒片段 |
| 批量处理 | ⭐⭐ | 支持多个输入目录 |
| 动画效果 | ⭐⭐⭐⭐ | Plotly 动画展示时间维度 |
| 机器学习分类 | ⭐⭐⭐⭐ | SVM/RandomForest 自动识别鸟种 |
| 实时分析 | ⭐⭐⭐⭐⭐ | 麦克风输入 + 实时可视化 |

---

*版本：v2.0（修复版） | 最后更新：2026-02-22*
