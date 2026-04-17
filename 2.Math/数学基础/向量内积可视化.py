import marimo

__generated_with = "0.8.22"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    from mpl_toolkits.mplot3d import Axes3D

    # 用字体文件路径直接加载，避免字体缓存问题
    _font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
    CN = fm.FontProperties(fname=_font_path, size=11)
    CN_title = fm.FontProperties(fname=_font_path, size=13)
    CN_small = fm.FontProperties(fname=_font_path, size=9)
    return Axes3D, CN, CN_small, CN_title, fm, mo, np, plt


@app.cell
def __(mo):
    mo.md("""# 向量内积可视化""")
    return


@app.cell
def __(CN, CN_small, CN_title, np, plt):
    def plot_vectors_3d(a, b, title=""):
        dot_product = float(np.dot(a, b))
        norm_a = float(np.linalg.norm(a))
        norm_b = float(np.linalg.norm(b))
        cos_theta = dot_product / (norm_a * norm_b) if norm_a * norm_b > 0 else 0
        angle = float(np.arccos(np.clip(cos_theta, -1, 1)) * 180 / np.pi)

        fig = plt.figure(figsize=(13, 5))

        # 左图：3D 向量
        ax1 = fig.add_subplot(121, projection='3d')
        origin = np.zeros(3)

        ax1.quiver(*origin, *a, color='red', linewidth=2, arrow_length_ratio=0.15, label='a')
        ax1.quiver(*origin, *b, color='blue', linewidth=2, arrow_length_ratio=0.15, label='b')

        # 投影虚线（辅助理解）
        ax1.plot([0, a[0]], [0, a[1]], [0, 0], 'r--', alpha=0.3, linewidth=1)
        ax1.plot([0, b[0]], [0, b[1]], [0, 0], 'b--', alpha=0.3, linewidth=1)

        max_val = max(np.max(np.abs(a)), np.max(np.abs(b))) * 1.3 or 1.0
        ax1.set_xlim(-max_val, max_val)
        ax1.set_ylim(-max_val, max_val)
        ax1.set_zlim(-max_val, max_val)
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        ax1.set_title(title, fontproperties=CN_title, pad=10)

        # 图例手动设置字体
        handles, labels = ax1.get_legend_handles_labels()
        leg_labels = [f'a = {list(a)}', f'b = {list(b)}']
        ax1.legend(handles, leg_labels, loc='upper left', prop=CN_small)

        # 右图：信息面板
        ax2 = fig.add_subplot(122)
        ax2.axis('off')

        if dot_product > 0.1:
            relation = "正相关（同向）"
            color = 'green'
        elif dot_product < -0.1:
            relation = "负相关（反向）"
            color = 'red'
        else:
            relation = "无关（垂直）"
            color = 'gray'

        # 信息文本
        lines_data = [
            (f"a = [{a[0]:.2f}, {a[1]:.2f}, {a[2]:.2f}]", 'black'),
            (f"|a| = {norm_a:.3f}", 'black'),
            ("", 'black'),
            (f"b = [{b[0]:.2f}, {b[1]:.2f}, {b[2]:.2f}]", 'black'),
            (f"|b| = {norm_b:.3f}", 'black'),
            ("", 'black'),
            (f"a · b = {dot_product:.3f}", 'darkblue'),
            (f"cos(θ) = {cos_theta:.3f}", 'darkblue'),
            (f"θ = {angle:.1f}°", 'darkblue'),
            ("", 'black'),
            (f"关系：{relation}", color),
        ]

        y_pos = 0.92
        for text, clr in lines_data:
            ax2.text(0.1, y_pos, text, fontproperties=CN, color=clr,
                     transform=ax2.transAxes, verticalalignment='top')
            y_pos -= 0.08

        ax2.add_patch(plt.Rectangle((0.05, 0.02), 0.9, 0.96,
                      fill=True, facecolor='lightyellow', edgecolor=color,
                      linewidth=2, transform=ax2.transAxes))
        # 重新绘制文字在矩形上面
        y_pos = 0.92
        for text, clr in lines_data:
            ax2.text(0.1, y_pos, text, fontproperties=CN, color=clr,
                     transform=ax2.transAxes, verticalalignment='top', zorder=5)
            y_pos -= 0.08

        fig.tight_layout()
        return fig
    return (plot_vectors_3d,)


@app.cell
def __(mo):
    mo.md("""## 示例 1：强正相关（完全同向）""")
    return


@app.cell
def __(np, plot_vectors_3d):
    _fig = plot_vectors_3d(np.array([1, 2, 3]), np.array([2, 4, 6]), "示例1：强正相关（同方向倍数）")
    _fig
    return


@app.cell
def __(mo):
    mo.md("""## 示例 2：弱正相关（45° 夹角）""")
    return


@app.cell
def __(np, plot_vectors_3d):
    _fig = plot_vectors_3d(np.array([1.0, 0.0, 0.0]), np.array([0.7, 0.7, 0.0]), "示例2：弱正相关（45°夹角）")
    _fig
    return


@app.cell
def __(mo):
    mo.md("""## 示例 3：无关（垂直，内积=0）""")
    return


@app.cell
def __(np, plot_vectors_3d):
    _fig = plot_vectors_3d(np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]), "示例3：垂直无关（内积=0）")
    _fig
    return


@app.cell
def __(mo):
    mo.md("""## 示例 4：负相关（反向）""")
    return


@app.cell
def __(np, plot_vectors_3d):
    _fig = plot_vectors_3d(np.array([1.0, 2.0, 1.0]), np.array([-2.0, -4.0, -2.0]), "示例4：负相关（反方向）")
    _fig
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## 总结

        | 情况 | 内积值 | 夹角 | 关系 |
        |------|--------|------|------|
        | 同向 | > 0 | < 90° | 正相关 |
        | 垂直 | = 0 | = 90° | 无关 |
        | 反向 | < 0 | > 90° | 负相关 |

        公式：**a · b = a₁b₁ + a₂b₂ + a₃b₃ = |a||b|cos(θ)**
        """
    )
    return


if __name__ == "__main__":
    app.run()
