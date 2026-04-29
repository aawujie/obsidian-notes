# 卡尔曼滤波 — marimo 交互笔记

> 代码：[[kalman_filter_intro]] (`Resources/marimo/kalman_filter_intro.py`)

用 `marimo run` 或 `marimo edit` 打开，可交互修改 Q/R 参数看效果。

## 包含内容

1. **一维位置跟踪** — 小车匀速运动，GPS 噪声传感器，Kalman 滤噪 + 自推断速度
2. **二维轨迹跟踪** — 正弦变道，X/Y 同时估计，轨迹图 + 误差对比
3. **交互调参** — 拖动滑块改 Q/R，实时看滤波效果变化
4. **协方差 P 和增益 K 的收敛过程** — 理解滤波器怎么从"不确定"到"稳态"

## 相关笔记

- [[卡尔曼滤波入门]] — 理论推导
- [[卡尔曼滤波 EKF vs UKF]] — 非线性扩展
