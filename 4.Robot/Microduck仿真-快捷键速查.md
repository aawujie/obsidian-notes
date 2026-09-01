---
tags:
  - microduck
  - mujoco
  - 仿真
  - 快捷键
created: 2026-08-31
---

# Microduck 仿真 · 快捷键速查

> 在本地 Mac (Apple Silicon) 上跑 Microduck 的 MuJoCo 仿真。环境:`/Users/apple/code/0.drl/microduck_rl`(venv 已装好,依赖 127 个包)。
> 策略文件在 `/Users/apple/code/0.drl/microduck/policies/`(真机发布的 ONNX)。

## 启动命令

交互版(一键脚本,全部策略已挂载):

```bash
cd /Users/apple/code/0.drl/microduck_rl && ./duck-interactive.sh
```

等价完整命令:

```bash
uv run mjpython scripts/infer_policy.py \
  --walking  /Users/apple/code/0.drl/microduck/policies/alpha_walking.onnx \
  --standing /Users/apple/code/0.drl/microduck/policies/alpha_stand.onnx \
  --sitstand /Users/apple/code/0.drl/microduck/policies/alpha_sitstand.onnx \
  --ground-pick /Users/apple/code/0.drl/microduck/policies/alpha_ground_pick.onnx \
  --roulade  /Users/apple/code/0.drl/microduck/policies/roulade.onnx \
  --kick-left  /Users/apple/code/0.drl/microduck/policies/ball_kick_left.onnx \
  --kick-right /Users/apple/code/0.drl/microduck/policies/ball_kick_right.onnx \
  --new-cmd-obs
```

要点:

- macOS 上必须用 `mjpython` 启动原生窗口(普通 `python` 会报 `launch_passive requires mjpython`)
- `--new-cmd-obs` 必须加:61 维统一命令观测(速度3+头4+身体6),不加则观测 51 维,策略加载失败
- `--lin-vel-x 0.3` 可让鸭子一启动就走(不加则按 `↑` 启动)

## 按键分工(重要)

- **终端里按** = 给鸭子下命令(速度、动作)
- **MuJoCo 窗口里按** = 视图快捷键(面板、相机、帮助)

## 鸭子控制键(在终端里按)

### 速度模式(默认)

| 按键 | 动作 |
| --- | --- |
| `↑` / `↓` | 前进 / 后退(加速/减速) |
| `←` / `→` | 横移(左/右) |
| `A` / `E` | 左转 / 右转 |
| `空格` | 停车(归零) |
| `T` | 暂停/恢复策略(暂停=舵机保持最后目标) |
| `G` | 俯身捡东西(需 `--ground-pick`) |
| `Y` | 坐下 ↔ 站起(`--sitstand`)或斜坡模式(`--slope`) |
| `K` / `L` | 左脚 / 右脚踢球(需 `--kick-left` / `--kick-right`) |
| `R` | 前滚翻(需 `--roulade`) |
| `P` | 随机推它一把(躯干速度 1.0 m/s 随机方向) |
| `Q` | 退出 |

### 身体姿态模式(按 `B` 切换)

| 按键 | 动作 |
| --- | --- |
| `↑` / `↓` | Δz ±10 mm(最大 ±30 mm) |
| `←` / `→` | Δpitch ±10°(最大 ±30°) |
| `A` / `E` | Δroll ±10°(最大 ±30°) |
| `Z` / `S` | Δyaw ±10°(需 `--new-cmd-obs`,最大 ±30°) |
| `空格` | 复位身体姿态 |

### 头部控制模式(按 `H` 切换)

| 按键 | 动作 |
| --- | --- |
| `Z` / `S` | neck_pitch ±步进 |
| `↑` / `↓` | head_pitch ±步进 |
| `←` / `→` | head_yaw ±步进 |
| `A` / `E` | head_roll ±步进 |
| `空格` | 复位头部偏移 |

## MuJoCo 窗口快捷键(在窗口里按)

来源:MuJoCo 3.10 `simulate/simulate.cc` 官方 help 表。

### 面板

| 按键 | 功能 |
| --- | --- |
| `Tab` | 切换左侧面板(Options:physics / visualization / rendering) |
| `Shift+Tab` | 切换右侧面板(Info) |
| `F1` | 帮助覆盖层(完整快捷键总表) |
| `F2` / `F3` / `F4` | 右侧面板切页:Info / Profiler / Sensors |
| `F5` | 全屏 |

> ⚠️ `infer_policy.py` 启动时 `show_left_ui=False, show_right_ui=False`,两个面板默认关闭,按 `Tab` / `Shift+Tab` 调出。

### 仿真控制与相机

| 按键 | 功能 |
| --- | --- |
| `空格` | 播放 / 暂停 |
| `+` / `-` | 加速 / 减速 |
| `←` / `→` | 上一步 / 下一步 |
| `[` / `]` | 循环切换相机 |
| `Esc` | 自由相机 |
| `双击` | 选中物体 |
| `Page Up` | 选中父物体 |
| `右键双击` | 居中相机 |
| `Ctrl+右键双击` | 跟踪相机 |

### 鼠标

| 操作 | 功能 |
| --- | --- |
| 滚轮 / 中键拖拽 | 缩放 |
| 左键拖拽 | 视角环绕(orbit) |
| `Shift`+右键拖拽 | 平移视角 |
| `Ctrl`(+Shift)+拖拽 | 旋转物体 |
| `Ctrl`(+Shift)+右键拖拽 | 平移物体 |

## 网页版查看器(mjlab play)

```bash
uv run play Mjlab-Velocity-Flat-MicroDuck --agent zero      # 零动作(站着被推)
uv run play Mjlab-Velocity-Flat-MicroDuck --agent random    # 随机动作
uv run play Mjlab-Velocity-Flat-MicroDuck --viewer native   # 强制原生窗口
```

- 默认 `--viewer auto`:有 `$DISPLAY`(Linux 图形会话)→ 原生;macOS 无此变量 → **viser 网页版**(`http://localhost:8080`)
- 网页版 = 作者训练时用的界面,带奖励面板/曲线/checkpoint 热切换

## 常见坑

- **训练**:mjlab 需要 NVIDIA GPU(CUDA),Apple Silicon 本地训不了;用 `--hf-jobs` 提交 Hugging Face 云端
- **libpython**:`mjpython` 启动失败先查 `.venv/lib/libpython3.12.dylib` 软链是否存在(指向 `~/.local/share/uv/python/cpython-3.12.11-*/lib/`)
- **后台无 TTY**:键盘控制依赖 stdin 是真实终端,ssh/后台进程里会打印 `stdin is not a TTY — keyboard control disabled`
