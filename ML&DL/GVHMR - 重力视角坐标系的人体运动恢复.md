# GVHMR — 从单目视频恢复世界坐标系下的人体运动

> **论文**: World-Grounded Human Motion Recovery via Gravity-View Coordinates
> **会议**: SIGGRAPH Asia 2024
> **机构**: 浙江大学 (zju3dv)
> **代码**: [zju3dv/GVHMR](https://github.com/zju3dv/GVHMR)
> **项目页**: [zju3dv.github.io/gvhmr](https://zju3dv.github.io/gvhmr)

## 一句话概括

提出 **Gravity-View (GV) 坐标系**，将人体姿态估计从"逐帧自回归累积漂移"变成"逐帧独立预测后拼接"，实现从单目视频高速、准确地恢复世界坐标系下的全局人体运动。1430 帧(~45s) 视频只需 280ms (RTX 4090)。

---

## 要解决什么问题？

从单目视频恢复人体 3D 运动有两个层次：

1. **相机空间 (Camera-space)**：每帧人相对于相机的姿态 → HMR2 等方法已较成熟
2. **世界坐标系 (World-grounded)**：<span style="color:rgb(255, 77, 77)">人在全局空间中的绝对位置和朝向</span> → **难点所在**

难点：**<span style="color:rgb(255, 77, 77)">世界坐标系的定义本身就是模糊的</span>**（每段视频的"世界"都不同）。之前的方法（如 WHAM）用自回归方式逐帧预测相对运动，累积误差严重——人会越走越偏。

---

## 核心创新：<span style="color:rgb(255, 77, 77)">Gravity-View (GV) 坐标系</span>

### 什么是 GV 坐标系？

<span style="color:rgb(255, 77, 77)">对于视频的<b>每一帧</b>，定义一个坐标系：</span>

- **<span style="color:rgb(195, 117, 255)">Y 轴** = 重力方向（朝上）</span>
- **<span style="color:rgb(195, 117, 255)">Z 轴** = 相机视线方向</span>（投影到水平面后的分量）
- **X 轴** = Y × Z（右手系补全）

### 为什么好？

| 特性         | 说明                                                                    |
| ---------- | --------------------------------------------------------------------- |
| **自然考虑重力** | <span style="color:rgb(195, 117, 255)">Y 轴对齐重力</span>，人的姿态天然有"上下"概念   |
| **每帧唯一定义** | 只要知道<span style="color:rgb(195, 117, 255)">重力方向和相机朝向</span>，就能确定坐标系   |
| **避免误差累积** | <span style="color:rgb(195, 117, 255)">每帧独立预测 GV 坐标下的姿态</span>，不依赖上一帧 |
|            |                                                                       |

### 与其他坐标系的对比

- **相机坐标系**：<span style="color:rgb(255, 77, 77)">每帧不同，朝向随相机运动变化</span> → 需要额外处理
- **世界坐标系**：全局唯一但无法从单张图片推断 → 必须自回归累积
- **GV 坐标系**：每帧独立可推断 + 重力对齐 → 两全其美

---

## 整体 Pipeline

```
单目视频
    │
    ├─→ [人体检测 + 2D关键点] → ViTPose → 2D Keypoints (obs)
    ├─→ [图像特征提取] → HMR2 backbone → f_imgseq (1024-d)
    ├─→ [相机旋转估计] → SimpleVO / DPVO → cam_angvel (6-d)
    ├─→ [检测框] → bbx_xys → CLIFF camera params
    │
    ▼
┌─────────────────────────────────────────┐
│  Relative Transformer (核心网络)         │
│  输入：2D关键点 + 图像特征 + 相机信息    │
│  输出：                                  │
│    ① body_pose (GV坐标下的全身姿态)      │
│    ② global_orient_gv (GV坐标下的朝向)   │
│    ③ local_transl_vel (局部速度)          │
│    ④ pred_cam (相机空间参数)              │
│    ⑤ static_conf (关节静止置信度)         │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│  GV→World 坐标转换                       │
│  用 cam_angvel 链式恢复全局朝向和位移     │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│  后处理 (Post-processing)                │
│  ① 静止关节约束 (脚不打滑)               │
│  ② IK 修正                              │
└─────────────────────────────────────────┘
                │
                ▼
        SMPL 参数 (全局坐标)
```

---

## 核心网络：Relative Transformer

文件：`hmr4d/network/gvhmr/relative_transformer.py`

架构：`NetworkEncoderRoPE`

### 输入融合

1. **2D 关键点** (obs)：COCO-17 格式的 (x, y, confidence)
   - 每个关键点学一个 32-d 的位置嵌入
   - 低置信度的关键点用**可学习参数** `learned_pos_params` 替代（不是简单置零）
   - 17 个关键点 × 32-d → MLP → 512-d token
2. **CLIFF Camera** (f_cliffcam)：检测框在全图中的位置 → 3-d
3. **相机角速度** (f_cam_angvel)：相邻帧相机旋转 → 6-d (rotation_6d)
4. **图像序列特征** (f_imgseq)：HMR2 backbone 提取 → 1024-d

所有条件通过**加法融合**到主 token 上。

### Transformer 主体

- 12 层 RoPE (Rotary Position Embedding) Encoder
- 512-d latent，8 heads，mlp_ratio=4.0
- 支持长视频的**滑动窗口注意力**（超过 max_len=120 时限制注意力范围）

### 输出头

- `final_layer` → 151-d 主输出（body_pose + betas + orientations + velocity）
- `pred_cam_head` → 3-d 相机参数（带均值/标准差归一化）
- `static_conf_head` → 6-d 静止关节置信度（脚踝、脚、手腕）
- **betas 全序列平均**：体型参数在整个视频上取平均（同一个人体型不变）

### zero_module 初始化技巧

条件嵌入器的最后一层用 `zero_module` 初始化为全零：训练开始时条件信号对主 token 无影响，网络先学基本预测，再逐渐利用额外条件。这是 ControlNet/扩散模型中常见的稳定训练技巧。

---

## EnDecoder：编解码器

文件：`hmr4d/model/gvhmr/utils/endecoder.py`

负责 SMPL 参数和网络 151-d 向量之间的互相转换：

```
151-d 向量的定义：
├── 0:126   → body_pose_r6d        (21个关节 × 6-d rotation)
├── 126:136 → betas                (10-d 体型参数)
├── 136:142 → global_orient_r6d    (相机空间朝向, 6-d)
├── 142:148 → global_orient_gv_r6d (GV坐标系朝向, 6-d)
└── 148:151 → local_transl_vel     (局部移动速度, 3-d)
```

关键设计：
- 编码时做**标准化** (x - mean) / std
- 旋转统一用 **rotation_6d** 表示（比 axis-angle 更适合网络学习，连续性更好）
- 内置 **Forward Kinematics (FK)**：从关节角度 + betas → 3D 关节位置

---

## GV → World 坐标转换

文件：`gvhmr_pipeline.py` 中的 `get_smpl_params_w_Rt_v2`

把逐帧独立预测的 GV 坐标姿态拼成全局运动：

1. **从 cam_angvel 恢复相机旋转链**：$R_{t \to t+1}$ 逐帧累积 → $R_{t \to 0}$
2. **从 GV 朝向 + 相机朝向 → 计算 $R_{c \to gv}$**
3. **用相机旋转将各帧 GV 坐标对齐到同一个世界坐标系**
4. **Rollout 局部速度 → 全局位移**：用全局朝向旋转局部速度后累积
5. **高斯平滑**：对旋转链做 gaussian_smooth 减少抖动

注意：虽然也有"累积"，但只累积**相机旋转**（来自 VO，比较准确），而非人体姿态的误差。

### local_transl_vel 的设计含义

- **为什么不直接预测世界坐标？** → 绝对值无界，难学
- **为什么不预测世界坐标下的速度？** → 需要知道朝向才能用，而朝向本身是待预测的
- **为什么用 SMPL 局部速度？** → 在"人自己的坐标系"下，前进=+z，左移=+x，**与绝对朝向解耦**，范围有界、容易学

---

## 损失函数设计

### 主损失

- `simple_loss`：网络输出 151-d 与 GT 编码的 MSE

### 相机空间辅助损失

- `cr_j3d_loss`：Root-aligned 3D 关节位置误差
- `transl_c_loss`：相机空间平移（通过 pred_cam 参数间接监督）
- `j2d_loss`：2D 重投影误差
- `cr_vert_loss`：Root-aligned 顶点位置误差
- `verts2d_loss`：顶点 2D 重投影误差

### 全局辅助损失

- `transl_w_loss`：世界坐标系下的位移 L1 误差
- `static_conf_loss`：静止关节分类的 BCE 损失（GT 通过速度阈值自动生成）

### 特殊处理

- 3DPW 数据只有相机空间 GT → 只监督相机空间损失，不监督全局损失
- 通过 `mask["spv_incam_only"]` 控制

---

## 后处理

文件：`hmr4d/model/gvhmr/utils/postprocess.py`

1. **Static Joint Constraint（静止关节约束）**：
   - 网络预测每个关节（脚踝、脚、手腕）的"静止置信度"
   - 高置信度帧强制该关节不移动 → 消除脚滑 (foot sliding)
   - 静态相机场景有额外的 `pp_static_joint_cam` 处理

2. **IK 修正 (Inverse Kinematics)**：
   - `process_ik` 修正身体姿态使其更符合物理约束

---

## 训练细节

### 数据

混合 4 个数据集：
- **AMASS**：大规模 MoCap 动作数据（提供全局运动 GT）
- **BEDLAM**：合成视频数据（提供图像 + 完美 GT）
- **H36M**：室内多视角人体数据
- **3DPW**：户外真实视频数据（只有相机空间 GT）

### 数据增强（非常激进）

1. GT 关键点加高斯噪声 → 模拟 2D 检测器误差
2. 随机手脚修改 (`randomly_modify_hands_legs`) → 模拟检测器混淆
3. 随机遮挡下半身 (`randomly_occlude_lower_half`) → 模拟半身遮挡
4. 深度过近的点标为不可见 (z < 0.3) → 防止投影异常
5. **50% 概率替换为真实 ViTPose 检测** → 缩小训练/推理域差距
6. **10% Classifier-free 条件 dropout** → 不过度依赖任何单一条件

### 遮挡处理

```
可见关键点 → learned_pos_linear(x, y) 学习位置嵌入
不可见关键点 → learned_pos_params (可学习的"我不知道"默认向量)
```

网络能区分"关键点在原点"和"关键点被遮挡了"。

### 训练配置

- 2 × RTX 4090, batch_size=256, 420 epochs, ~13 小时
- 从头训练，不依赖预训练权重

---

## 推理技巧

### Flip Test（翻转增强）

1. 正常推理 → 结果 A
2. 图像水平翻转后推理 → 翻转结果 B
3. 将 B 翻转回来（`flip_smplx_params`）
4. A 和 B 的 body_pose 用旋转平均（`avg_smplx_aa`），betas 直接平均

利用人体左右对称性，几乎无成本提升精度。

### 相机旋转估计

- **DPVO**：深度学习 Visual Odometry，精度高但依赖较重
- **SimpleVO**（2025 新增）：轻量级自实现方案，更高效兼容
- **静态相机**：`-s` 参数跳过 VO，相机旋转为零

---

## 评估指标

### 世界坐标系指标 (World-grounded)

- **W-MPJPE**：世界坐标下的平均关节位置误差
- **WA-MPJPE**：对齐后的世界坐标关节误差
- **RTE / AOE**：根关节位移误差 / 朝向角度误差

### 相机空间指标 (Camera-space)

- **PA-MPJPE**：Procrustes 对齐后的 MPJPE
- **MPJPE**：相机空间直接关节误差
- **PVE**：顶点误差
- **Accel**：加速度误差（衡量运动平滑度）

---

## 项目结构

```
GVHMR/
├── hmr4d/
│   ├── model/
│   │   └── gvhmr/
│   │       ├── gvhmr_pl.py           # PyTorch Lightning 训练/评估模块
│   │       ├── gvhmr_pl_demo.py       # 推理 demo 模块
│   │       ├── pipeline/
│   │       │   └── gvhmr_pipeline.py  # 核心 Pipeline（前向+损失+GV→World）
│   │       └── utils/
│   │           ├── endecoder.py       # SMPL ↔ 151-d 编解码
│   │           ├── postprocess.py     # 后处理（静止约束 + IK）
│   │           └── stats_compose.py   # 标准化统计量
│   ├── network/
│   │   ├── gvhmr/
│   │   │   └── relative_transformer.py  # 核心 Transformer 网络
│   │   ├── hmr2/                         # HMR2 图像特征提取
│   │   └── base_arch/                    # Transformer 基础组件 (RoPE等)
│   ├── configs/                          # Hydra 配置
│   ├── dataset/                          # 数据集定义
│   └── utils/                            # 几何变换、可视化等工具
├── tools/
│   ├── demo/                             # 推理脚本
│   └── train.py                          # 训练入口
└── third-party/                          # 第三方依赖
```

---

## 与 PBHC 的关系

GVHMR 在 PBHC (KungfuBot) 项目中是**动作处理流水线的第一步**：

```
视频 ──[GVHMR]──→ SMPL 运动序列 ──[过滤/重定向]──→ 机器人动作 ──[RL训练]──→ 控制策略
```

PBHC 用 GVHMR 从功夫/舞蹈视频中提取人体运动的 SMPL 表示，然后再重定向到宇树 G1 机器人。

---

## 核心亮点总结

| 要点 | 说明 |
|---|---|
| **GV 坐标系** | 重力+视线方向定义，每帧唯一，避免自回归漂移 |
| **逐帧独立预测** | 不依赖上一帧预测结果，不累积姿态误差 |
| **RoPE Transformer** | 12 层，滑动窗口注意力支持长视频 |
| **多条件融合** | 2D 关键点+图像特征+相机旋转+检测框，zero_module 初始化 |
| **local_transl_vel** | 局部速度与绝对朝向解耦，范围有界易学 |
| **静止关节约束** | 预测关节静止置信度 → 后处理消除脚滑 |
| **激进数据增强** | 遮挡/噪声/真实检测混合 + Classifier-free dropout |
| **速度极快** | 1430 帧(~45s) 视频只需 280ms |
