# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib", "marimo"]
# ///

import marimo

__generated_with = "0.23.4"
app = marimo.App(width="medium", app_title="卡尔曼滤波入门")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 卡尔曼滤波入门 — 交互示例

    配合笔记 [[卡尔曼滤波入门]]，用代码直观感受 Kalman Filter 的每一步。

    ---

    ## 例子设定

    一辆小车沿直线运动。每 0.1 秒，我们用**噪声传感器**测一次它的位置。

    - **真实运动**：匀速 + 随机加速度扰动（我们不知道）
    - **传感器**：GPS 读数，有高斯噪声
    - **KFilter**：同时运行，估计真实位置

    看 Kalman 怎么把噪声传感器读数"拉"回真实位置。
    """)
    return


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    np.random.seed(42)
    return np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 1. 一维位置跟踪
    """)
    return


@app.cell
def _(np):
    # ============================================
    # 仿真参数
    # ============================================
    dt = 0.1              # 时间步长 (10Hz)
    N_SIM = 200            # 仿真步数
    true_velocity = 2.0    # 真实速度 (m/s)

    # 真实状态 (位置, 速度)
    x_true = np.zeros((N_SIM, 2))
    x_true[0] = [0.0, true_velocity]

    # 生成真实轨迹 + 过程噪声
    q_accel = 0.5  # 加速度噪声强度
    for step in range(1, N_SIM):
        accel_noise = np.sqrt(q_accel) * np.random.randn()
        x_true[step, 0] = x_true[step-1, 0] + x_true[step-1, 1]*dt + 0.5*accel_noise*dt**2
        x_true[step, 1] = x_true[step-1, 1] + accel_noise*dt

    # 传感器测量 (只测位置，有噪声)
    r_measure = 5.0  # 测量噪声方差 (传感器标准差 ≈ 2.24m)
    z = x_true[:, 0] + np.sqrt(r_measure) * np.random.randn(N_SIM)
    return dt, q_accel, r_measure, x_true, z


@app.cell
def _(dt, np, q_accel, r_measure, z):
    # ============================================
    # 卡尔曼滤波
    # ============================================
    n_1d = len(z)

    # 状态: [位置, 速度]
    F = np.array([[1, dt],
                  [0, 1]])   # 状态转移
    H = np.array([[1, 0]])   # 只观测位置

    # 过程噪声协方差 (从加速度推导)
    G = np.array([[0.5*dt**2],
                  [dt]])
    Q = G @ G.T * q_accel
    R = np.array([[r_measure]])

    # 初始状态
    x_hat = np.array([z[0], 0.0])
    P = np.array([[500, 0],
                  [0, 500]])

    x_est = np.zeros((n_1d, 2))
    P_hist = np.zeros((n_1d, 2))
    K_hist = np.zeros((n_1d, 2))

    for idx in range(n_1d):
        # Predict
        x_pred1 = F @ x_hat
        P_pred1 = F @ P @ F.T + Q
        # Update
        y = z[idx] - H @ x_pred1
        S = H @ P_pred1 @ H.T + R
        K = P_pred1 @ H.T @ np.linalg.inv(S)
        x_hat = x_pred1 + K @ y
        P = (np.eye(2) - K @ H) @ P_pred1
        x_est[idx] = x_hat
        P_hist[idx] = [P[0, 0], P[1, 1]]
        K_hist[idx] = K.flatten()
    return K_hist, P_hist, x_est


@app.cell(hide_code=True)
def _(K_hist, P_hist, mo, np, plt, x_est, x_true, z):
    # ============================================
    # 可视化
    # ============================================
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    t = np.arange(len(z))

    # 子图1: 位置估计 vs 测量 vs 真实
    ax = axes[0, 0]
    ax.plot(t, x_true[:, 0], 'k-', linewidth=1.5, label='真实位置', alpha=0.7)
    ax.plot(t, z, 'r.', markersize=2, alpha=0.4, label='传感器测量')
    ax.plot(t, x_est[:, 0], 'b-', linewidth=2, label='Kalman 估计')
    sigma = np.sqrt(P_hist[:, 0])
    ax.fill_between(t, x_est[:, 0] - 2*sigma, x_est[:, 0] + 2*sigma,
                     alpha=0.15, color='blue', label='95% 置信区间')
    ax.set_xlabel('时间步')
    ax.set_ylabel('位置 (m)')
    ax.set_title('位置跟踪：Kalman 滤掉了传感器噪声')
    ax.legend(fontsize=8, loc='upper left')
    ax.grid(True, alpha=0.3)

    rmse_measure = np.sqrt(np.mean((z - x_true[:, 0])**2))
    rmse_kalman = np.sqrt(np.mean((x_est[:, 0] - x_true[:, 0])**2))
    ax.text(0.98, 0.05,
            f'RMSE: 原始测量={rmse_measure:.2f}m  |  Kalman后={rmse_kalman:.2f}m',
            transform=ax.transAxes, ha='right', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # 子图2: 速度估计
    ax = axes[0, 1]
    ax.plot(t, x_true[:, 1], 'k-', linewidth=1.5, label='真实速度', alpha=0.7)
    ax.plot(t, x_est[:, 1], 'g-', linewidth=2, label='Kalman 估计速度')
    sigma_v = np.sqrt(P_hist[:, 1])
    ax.fill_between(t, x_est[:, 1] - 2*sigma_v, x_est[:, 1] + 2*sigma_v,
                     alpha=0.15, color='green')
    ax.set_xlabel('时间步')
    ax.set_ylabel('速度 (m/s)')
    ax.set_title('速度估计 (传感器没测速度，Kalman 自己推断)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # 子图3: 卡尔曼增益收敛
    ax = axes[1, 0]
    ax.plot(t, K_hist[:, 0], 'b-', label='位置增益', linewidth=1.5)
    ax.plot(t, K_hist[:, 1], 'orange', label='速度增益', linewidth=1.5)
    ax.axhline(y=0.3, color='gray', linestyle='--', alpha=0.5)
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax.set_xlabel('时间步')
    ax.set_ylabel('Kalman Gain')
    ax.set_title('卡尔曼增益收敛过程 (K -> 稳态)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # 子图4: 不确定性衰减
    ax = axes[1, 1]
    ax.semilogy(t, np.sqrt(P_hist[:, 0]), 'b-', label='位置标准差', linewidth=1.5)
    ax.semilogy(t, np.sqrt(P_hist[:, 1]), 'g-', label='速度标准差', linewidth=1.5)
    ax.set_xlabel('时间步')
    ax.set_ylabel('标准差 (log scale)')
    ax.set_title('协方差 P 的衰减 (不确定性逐渐消除)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('kalman_1d_demo.png', dpi=150, bbox_inches='tight')

    mo.md(f"""**关键观察：**

    - **RMSE 改善**：原始测量 {rmse_measure:.2f}m -> Kalman 后 {rmse_kalman:.2f}m
    - **速度推断**：传感器只测了位置，但 Kalman 通过状态转移矩阵 **自己推断出了速度**
    - **K 收敛**：前几步 K 很大（信传感器），不确定性降低后 K 趋于稳态
    - **P 衰减**：不确定性从开始的巨大值迅速降到稳态，P 不再缩小 = 达到"可达到的最优精度"
    """)

    mo.mpl.interactive(plt.gcf())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 2. 二维目标跟踪 (位置 + 速度)
    """)
    return


@app.cell
def _(np):
    # ============================================
    # 二维仿真
    # ============================================
    DT = 0.1
    N_2D = 150

    t_arr = np.arange(N_2D) * DT
    true_x = 3.0 * t_arr
    true_y = 2.0 * np.sin(0.5 * t_arr)
    true_vx = np.full(N_2D, 3.0)
    true_vy = 1.0 * np.cos(0.5 * t_arr)

    true_2d = np.column_stack([true_x, true_y, true_vx, true_vy])

    r2 = 2.0
    z_x = true_x + np.sqrt(r2) * np.random.randn(N_2D)
    z_y = true_y + np.sqrt(r2) * np.random.randn(N_2D)
    return DT, N_2D, r2, true_2d, z_x, z_y


@app.cell
def _(DT, N_2D, np, r2, z_x, z_y):
    # ============================================
    # 二维 Kalman (位置+速度)
    # ============================================
    F2 = np.array([[1, 0, DT, 0],
                   [0, 1, 0, DT],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])

    H2 = np.array([[1, 0, 0, 0],
                   [0, 1, 0, 0]])

    q2 = 0.1
    Q2 = q2 * np.eye(4)
    Q2[2, 2] = q2 * 0.5
    Q2[3, 3] = q2 * 0.5

    R2 = r2 * np.eye(2)

    x_hat_2d = np.array([z_x[0], z_y[0], 0.0, 0.0])
    P2 = 100 * np.eye(4)

    x_est_2d = np.zeros((N_2D, 4))
    for t2_idx in range(N_2D):
        x_pred2 = F2 @ x_hat_2d
        P_pred2 = F2 @ P2 @ F2.T + Q2
        z_k = np.array([z_x[t2_idx], z_y[t2_idx]])
        y_k = z_k - H2 @ x_pred2
        S_k = H2 @ P_pred2 @ H2.T + R2
        K_k = P_pred2 @ H2.T @ np.linalg.inv(S_k)
        x_hat_2d = x_pred2 + K_k @ y_k
        P2 = (np.eye(4) - K_k @ H2) @ P_pred2
        x_est_2d[t2_idx] = x_hat_2d
    return (x_est_2d,)


@app.cell(hide_code=True)
def _(mo, np, plt, true_2d, x_est_2d, z_x, z_y):
    # ============================================
    # 二维可视化
    # ============================================
    fig2, axes2 = plt.subplots(1, 2, figsize=(14, 5.5))

    ax = axes2[0]
    ax.plot(true_2d[:, 0], true_2d[:, 1], 'k-', linewidth=2, label='真实轨迹')
    ax.plot(z_x, z_y, 'r.', markersize=3, alpha=0.5, label='传感器测量')
    ax.plot(x_est_2d[:, 0], x_est_2d[:, 1], 'b-', linewidth=2, label='Kalman 估计')
    ax.plot(true_2d[0, 0], true_2d[0, 1], 'ko', markersize=8, label='起点')
    ax.plot(true_2d[-1, 0], true_2d[-1, 1], 'ks', markersize=8, label='终点')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_title('二维轨迹跟踪')
    ax.legend(fontsize=9)
    ax.axis('equal')
    ax.grid(True, alpha=0.3)

    ax = axes2[1]
    t2 = np.arange(len(z_x))
    err_measure_x = z_x - true_2d[:, 0]
    err_kalman_x = x_est_2d[:, 0] - true_2d[:, 0]
    ax.plot(t2, err_measure_x, 'r-', alpha=0.4, linewidth=1, label='测量误差')
    ax.plot(t2, err_kalman_x, 'b-', linewidth=2, label='Kalman 误差')
    ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax.set_xlabel('时间步')
    ax.set_ylabel('X 位置误差 (m)')
    ax.set_title('位置误差对比：Kalman 明显压低误差')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    rmse_x_measure = np.sqrt(np.mean(err_measure_x**2))
    rmse_x_kalman = np.sqrt(np.mean(err_kalman_x**2))
    ax.text(0.98, 0.95,
            f'RMSE X: 测量={rmse_x_measure:.2f}m  Kalman={rmse_x_kalman:.2f}m',
            transform=ax.transAxes, ha='right', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig('kalman_2d_demo.png', dpi=150, bbox_inches='tight')

    mo.mpl.interactive(plt.gcf())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. 手动调试：改变 Q 和 R 看效果

    拖动滑块修改 **Q (过程噪声)** 和 **R (测量噪声)**，重跑滤波看变化。

    - **R 调大** -> Kalman 更不信任传感器，估计曲线更平滑但可能滞后
    - **Q 调大** -> Kalman 更信任传感器，更快响应但噪声更多
    """)
    return


@app.cell
def _(mo):
    Q_slider = mo.ui.slider(start=0.01, stop=10.0, step=0.1, value=0.5, label="过程噪声 Q")
    R_slider = mo.ui.slider(start=0.1, stop=30.0, step=0.1, value=5.0, label="测量噪声 R")
    mo.hstack([Q_slider, R_slider], gap=2)
    return Q_slider, R_slider


@app.cell
def _(Q_slider, R_slider, dt, mo, np, plt, x_true, z):
    _q = Q_slider.value
    _r = R_slider.value

    iF = np.array([[1, dt], [0, 1]])
    iH = np.array([[1, 0]])
    iG = np.array([[0.5*dt**2], [dt]])
    iQ = iG @ iG.T * _q
    iR = np.array([[_r]])

    n_int = len(z)
    ix_hat = np.array([z[0], 0.0])
    iP = np.array([[500, 0], [0, 500]])

    ix_est = np.zeros((n_int, 2))
    for ti in range(n_int):
        ix_pred = iF @ ix_hat
        iP_pred = iF @ iP @ iF.T + iQ
        iy = z[ti] - iH @ ix_pred
        iS = iH @ iP_pred @ iH.T + iR
        iK = iP_pred @ iH.T @ np.linalg.inv(iS)
        ix_hat = ix_pred + iK @ iy
        iP = (np.eye(2) - iK @ iH) @ iP_pred
        ix_est[ti] = ix_hat

    fig3, ax3 = plt.subplots(figsize=(12, 4))
    t_arr = np.arange(n_int)
    ax3.plot(t_arr, x_true[:, 0], 'k-', linewidth=1.5, label='真实', alpha=0.6)
    ax3.plot(t_arr, z, 'r.', markersize=2, alpha=0.3, label='测量')
    ax3.plot(t_arr, ix_est[:, 0], 'b-', linewidth=2, label=f'Kalman (Q={_q}, R={_r})')
    ax3.set_xlabel('时间步')
    ax3.set_ylabel('位置 (m)')
    ax3.set_title(f'Q={_q}, R={_r}')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    irmse_meas = np.sqrt(np.mean((z - x_true[:, 0])**2))
    irmse_kf = np.sqrt(np.mean((ix_est[:, 0] - x_true[:, 0])**2))
    ax3.text(0.98, 0.05,
             f'RMSE: 测量={irmse_meas:.2f}m  Kalman={irmse_kf:.2f}m',
             transform=ax3.transAxes, ha='right', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    mo.mpl.interactive(fig3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. 核心直觉总结

    | 卡尔曼做的 | 相当于 |
    |:-----------|:-------|
    | Predict -> Update 循环 | 贝叶斯更新——每一步用新数据修正先验 |
    | K 自动算权重 | 不需要手动"信传感器还是信模型" |
    | P 的衰减轨迹 | 你获得信息的速度——P 不再缩小 = 已达极限 |
    | 速度估计 (传感器没测) | 状态转移矩阵 F 给你"免费"推断能力 |

    > **一句话：Kalman = 自动加权平均的递归状态估计器。Q 大信传感器，R 大信模型。**
    """)
    return


if __name__ == "__main__":
    app.run()
