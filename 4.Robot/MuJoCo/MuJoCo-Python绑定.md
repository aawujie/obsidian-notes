---
title: MuJoCo Python 绑定
type: summary
created: 2026-04-28
updated: 2026-04-28
sources: [https://mujoco.readthedocs.io/en/stable/python.html]
tags: [MuJoCo, Python, pybind11, 仿真]
---

# MuJoCo Python 绑定（Python Bindings）

MuJoCo Python 绑定使用 pybind11（C++）开发，API 与底层 C API 一致。

## 安装

```bash
pip install mujoco
```

MuJoCo 库打包在 Python 包中，无需单独安装。

## 交互式查看器（Interactive Viewer）

### 三种模式

#### 1. Managed Viewer（受管查看器）
`viewer.launch` 阻塞用户代码，适合通过引擎插件或物理回调实现的控制：

```python
import mujoco
import mujoco.viewer

# 空查看器（可拖放加载模型）
mujoco.viewer.launch()

# 加载指定模型
mujoco.viewer.launch(model)

# 使用已有 data
mujoco.viewer.launch(model, data)
```

#### 2. Standalone App（独立应用）
命令行直接启动：
```bash
python -m mujoco.viewer
python -m mujoco.viewer --mjcf=/path/to/model.xml
```

#### 3. Passive Viewer（被动查看器）
不阻塞，用户脚本控制时序：

```python
with mujoco.viewer.launch_passive(m, d) as viewer:
    while viewer.is_running():
        mujoco.mj_step(m, d)
        viewer.sync()
```

**查看器句柄属性/方法**：

| 属性/方法 | 说明 |
| --- | --- |
| `.cam`, `.opt`, `.pert` | mjvCamera, mjvOption, mjvPerturb 访问 |
| `.lock()` | 上下文管理器，获取查看器互斥锁 |
| `.sync(state_only=False)` | 同步 mjModel/mjData 与 GUI |
| `.update_hfield(id)` | 更新高度场数据 |
| `.update_mesh(id)` | 更新网格数据 |
| `.update_texture(id)` | 更新纹理数据 |
| `.close()` | 关闭查看器窗口 |
| `.is_running()` | 检查查看器是否运行 |
| `.user_scn` | 用户自定义 mjvScene |

**macOS 注意**：`launch_passive` 需要通过 `mjpython` 启动（渲染需主线程）。

**key_callback**：键盘事件回调。

**show_left_ui / show_right_ui**：初始 UI 面板显示状态。

## 基本用法（Basic Usage）

### Structs（结构体）

```python
import mujoco

# 加载模型
model = mujoco.MjModel.from_xml_path('/path/to/model.xml')
model = mujoco.MjModel.from_xml_string(xml_string)
model = mujoco.MjModel.from_binary_path('/path/to/model.mjb')

# 创建数据
data = mujoco.MjData(model)

# 其他结构体（自动调用默认初始化器）
opt = mujoco.MjOption()
scene = mujoco.MjvScene(model, maxgeom=100)
```

- 结构体名首字母大写（PEP 8）：`mjData` → `Mujoco.MjData`
- 除 `MjModel` 外均有构造函数
- 对应 `mj_makeFoo` 的资源在 Python 对象删除时自动释放
- `MjModel` 无构造函数，使用三个静态工厂方法

### 内存模型（重要）

Python 绑定直接访问 MuJoCo 原始内存，无复制/缓冲。**务必创建副本**：

```python
# WRONG: 所有元素指向最新值
positions = []
for _ in range(100):
    mujoco.mj_step(model, data)
    positions.append(data.body('torso').xpos)  # 全部相同！

# CORRECT: 创建副本
positions.append(data.body('torso').xpos.copy())
```

### Functions（函数）

- 函数名与 C API 相同（不做 PEP 8 化）
- 数组大小参数自动推断，省略传入
- 输入：NumPy 数组或可迭代对象
- 输出参数：必须为可写 NumPy 数组
- 调用时释放 GIL（Python Global Interpreter Lock）
- `mj_step` 额外支持 `nstep` 参数（多次步进，中间不获取 GIL）：

```python
# 等效，但前者不频繁获取 GIL
mj_step(model, data, nstep=20)
for _ in range(20): mj_step(model, data)
```

### Enums 和 Constants

```python
mujoco.mjtObj.mjOBJ_SITE       # enum
mujoco.mjVISSTRING              # constant
```

### Named Access（命名访问）

每个 `name_fooadr` 字段定义名称类别 `foo`，提供 `model.foo(name)` 和 `data.foo(name)` 方法：

```python
m.geom('gizmo').rgba     # → geom_rgba[4*i:4*i+4]
d.joint('elbow').qpos    # → 该关节的 qpos 段
m.geom('gizmo').id       # 同 mj_name2id(m, mjOBJ_GEOM, 'gizmo')
m.geom(i).name           # → 'gizmo'
```

访问器是 O(1)，不随实体数量增加。

**别名**：`jnt`/`joint`, `cam`/`camera`, `tex`/`texture`, `mat`/`material`, `eq`/`equality`, `ten`/`tendon`, `key`/`keyframe`

## Rendering（渲染）

```python
# 创建离屏渲染上下文
ctx = mujoco.GLContext(max_width, max_height)
ctx.make_current()
# ... 调用 mjr_ 渲染函数 ...
ctx.free()
```

- 上下文在同一时刻仅能在一个线程上 current
- `ctx.free()` 显式释放（多线程场景必要）

## Error Handling（错误处理）

- MuJoCo 不可恢复错误通过 `mju_error` → 终止进程
- Python 绑定使用 `longjmp` 将错误转为 `mujoco.FatalError` 异常
- 线程局部安装错误回调（支持多线程并发调用）

## Callbacks（回调）

```python
# 设置 Python 回调
mujoco.set_mjcb_control(my_python_callback)
mujoco.set_mjcb_control(None)  # 移除
cb = mujoco.get_mjcb_control() # 获取当前回调

# C 函数指针（通过 ctypes，不获取 GIL）
mujoco.set_mjcb_control(c_func_ptr)
```

**性能注意**：Python 回调每次触发都获取 GIL，性能影响严重。适合原型开发，生产建议用原生库。

## Model Editing（模型编辑）

```python
import mujoco

# 创建/加载 spec
spec = mujoco.MjSpec()
spec.modelname = "my model"

# 构建模型
body = spec.worldbody.add_body(pos=[1, 2, 3], quat=[0, 1, 0, 0])
geom = body.add_geom(
    name='my_geom',
    type=mujoco.mjtGeom.mjGEOM_SPHERE,
    size=[1, 0, 0],
    rgba=[1, 0, 0, 1],
)

# 编译
model = spec.compile()

# 保存为 XML
print(spec.to_xml())
```

### 加载方式
```python
spec = mujoco.MjSpec()                          # 空
spec = mujoco.MjSpec.from_string(xml_string)    # 从 XML 字符串
spec = mujoco.MjSpec.from_file(file_path)       # 从 XML 文件
```

### Assets
```python
assets = {'image.png': b'image_data'}
spec = mujoco.MjSpec.from_string(xml, assets=assets)
```

### Attachment（附加）
```python
body.attach_body(child_body, prefix, suffix)
frame.attach_frame(child_frame, prefix, suffix)
parent_spec.attach(child_spec, site=site_name)
parent_spec.attach(child_spec, frame=frame_name)
```

- 默认行为：不复制（修改子 = 修改父）
- `spec.copy_during_attach = True` 可改为深复制

### 便捷方法

| 方法 | 说明 |
| --- | --- |
| `spec.body(name)` | 命名访问元素 |
| `spec.bodies` | 所有 body 列表 |
| `body.geoms` | 直接子 geom 列表 |
| `body.find_all('site')` | 递归搜索子树中所有 site |
| `site.parent` | 父 body |
| `spec.delete(element)` | 删除元素及其引用 |
| `spec.to_zip(file)` | 序列化到 zip |
| `MjSpec.from_zip(file)` | 从 zip 加载 |

### 与 PyMJCF 的比较

- MjSpec 比 dm_control 的 PyMJCF **快约两个数量级**（C++ vs Python 字符串操作）
- `bind` 方法直接绑定 mjModel/mjData 值：
```python
torsos = [data.bind(geom) for geom in spec.geoms if 'torso' in geom.name]
```

## 模块

### rollout（轨迹推演）

```python
from mujoco import rollout

state, sensordata = rollout.rollout(model, data, initial_state, control)
```

- 支持批量推演（nbatch x nstate）
- 内部线程池并行（多 `MjData` 时）
- `persistent_pool=True` 复用线程池
- `Rollout` 类支持多线程池

### minimize（优化）

```python
from mujoco import minimize
# 非线性最小二乘优化器
minimize.least_squares(...)
```

### USD Exporter（USD 导出）

```python
from mujoco.usd import exporter

exp = exporter.USDExporter(model=m)
while d.time < duration:
    mujoco.mj_step(m, d)
    if exp.frame_count < d.time * framerate:
        exp.update_scene(data=d)
exp.save_scene(filetype="usd")
```

- 支持完整轨迹保存
- 自定义相机/灯光
- 输出目录包含 assets/ 和 frames/
- 需要 `pip install mujoco[usd]`

## mujoco-py 迁移对照

| mujoco-py | mujoco (新) |
| --- | --- |
| `load_model_from_xml(bstring)` | `MjModel.from_xml_string()` + `MjData(model)` |
| `sim.reset()` | `mj_resetData(model, data)` |
| `sim.forward()` | `mj_forward(model, data)` |
| `sim.step()` | `mj_step(model, data)` |
| `sim.get_state()` | `mj_getState()` |
| `sim.model.*_name2id(name)` | `mj_name2id()` 或 named access |
| `sim.save(fstream, format)` | `mj_saveLastXML()` |

## 从源码构建 Python 绑定

```bash
cd mujoco/python
python3 -m venv /tmp/mujoco && source /tmp/mujoco/bin/activate
bash make_sdist.sh
cd dist
MUJOCO_PATH=/PATH/TO/MUJOCO \
MUJOCO_PLUGIN_PATH=/PATH/TO/MUJOCO/PLUGIN \
pip install mujoco-x.y.z.tar.gz
```
