# Python Entrypoints 详解

**创建时间**: 2026-03-03  
**标签**: #Python #插件系统 #包管理 #Takopi

---

## 📖 什么是 Entrypoints？

**Entrypoints（入口点）** 是 Python 包的一种**元数据机制**，允许包在安装时向系统注册"可扩展的插件点"。其他程序可以在运行时发现并加载这些注册项，实现**插件化架构**。

简单说：**Entrypoints 让 Python 包能够"声明自己能被扩展"**。

---

## 🎯 核心概念

### 传统方式 vs Entrypoints

| 方式 | 做法 | 缺点 |
|------|------|------|
| **传统硬编码** | 在代码中 `import plugin_a, plugin_b` | 每次新增插件要改代码、重新部署 |
| **Entrypoints** | 插件自己注册，主程序动态发现 | 零配置、即插即用 |

### 工作原理

```
插件包安装时
    ↓
entrypoints 写入元数据 (dist-info/entry_points.txt)
    ↓
主程序运行时用 importlib.metadata 发现
    ↓
按需加载（懒加载）
```

---

## 📝 配置语法

### pyproject.toml (现代方式 - PEP 621)

```toml
[project.entry-points."takopi.engine_backends"]
claude = "takopi.runners.claude:BACKEND"
codex = "takopi.runners.codex:BACKEND"
acme = "acme_plugin:BACKEND"  # 第三方插件
```

### setup.cfg (传统方式)

```ini
[options.entry_points]
takopi.engine_backends =
    claude = takopi.runners.claude:BACKEND
    codex = takopi.runners.codex:BACKEND
```

### 格式解析

```
<entry_point_name> = <module_path>:<object_name>
                     │              │
                     │              └─ 导出的对象（类/函数/实例）
                     └─ 模块路径
```

---

## 🔧 实际示例

### 示例 1：CLI 命令注册

很多 Python CLI 工具用 entrypoints 注册命令：

```toml
# pytest 的 pyproject.toml
[project.entry-points.pytest11]
cov = "pytest_cov.plugin"
xdist = "xdist.plugin"
```

```python
# 主程序发现插件
from importlib.metadata import entry_points

plugins = entry_points(group="pytest11")
for plugin in plugins:
    plugin.load()  # 导入并注册
```

---

### 示例 2：Takopi 引擎插件

```toml
# Takopi 主包的 pyproject.toml
[project.entry-points."takopi.engine_backends"]
claude = "takopi.runners.claude:BACKEND"
codex = "takopi.runners.codex:BACKEND"

# 第三方插件的 pyproject.toml
[project.entry-points."takopi.engine_backends"]
acme = "acme_plugin:BACKEND"
```

```python
# Takopi 发现引擎
from importlib.metadata import entry_points

def discover_engines():
    engines = {}
    for ep in entry_points(group="takopi.engine_backends"):
        engines[ep.name] = ep.load()  # 懒加载
    return engines

# 使用
engines = discover_engines()
claude_backend = engines["claude"]  # 此时才导入模块
```

---

### 示例 3：Pandas 后端注册

```toml
# pandas_gbq 的 pyproject.toml
[project.entry-points."pandas_sql_engine"]
gbq = "pandas_gbq:GbqEngine"
```

```python
# Pandas 发现 SQL 引擎
for ep in entry_points(group="pandas_sql_engine"):
    register_engine(ep.name, ep.load())
```

---

## 🛠️ 使用 API

### Python 3.8+ (importlib.metadata)

```python
from importlib.metadata import entry_points

# 获取指定组的所有 entrypoints
eps = entry_points(group="pytest11")

# 遍历
for ep in eps:
    print(f"{ep.name} = {ep.value}")
    print(f"  模块：{ep.module}")
    print(f"  对象：{ep.attr}")
    
    # 加载（导入并返回对象）
    obj = ep.load()
```

### Python 3.9+ (更简洁)

```python
from importlib.metadata import entry_points

# 直接按组过滤
eps = entry_points(group="takopi.engine_backends")

# 按名称获取
claude_ep = entry_points(group="takopi.engine_backends")["claude"]
claude_backend = claude_ep.load()
```

### 获取所有组

```python
from importlib.metadata import entry_points

all_eps = entry_points()
print(all_eps.groups)  # 所有注册的组名
```

---

## 📦 查看已安装的 Entrypoints

### 命令行查看

```bash
# 查看包的元数据
pip show pytest | grep Location

# 查看 entry_points.txt
cat $(pip show pytest | grep Location | cut -d' ' -f2)/pytest-*.dist-info/entry_points.txt
```

### Python 查看

```python
from importlib.metadata import entry_points

# 列出所有组
for group in entry_points().groups:
    print(group)

# 列出某组的所有插件
for ep in entry_points(group="pytest11"):
    print(f"{ep.name} -> {ep.value}")
```

---

## 🏗️ 设计模式

### 1. 定义插件组名

```toml
# 组名约定：<项目名>.<插件类型>
takopi.engine_backends      # 引擎后端
takopi.transport_backends   # 传输后端
takopi.command_backends     # 命令插件
```

### 2. 定义插件协议

```python
# takopi/api.py
class EngineBackend(Protocol):
    id: str
    def build_runner(...) -> Runner: ...
```

### 3. 发现并加载

```python
def load_plugins():
    plugins = {}
    for ep in entry_points(group="takopi.engine_backends"):
        try:
            plugins[ep.name] = ep.load()
        except ImportError as e:
            logger.warning(f"Failed to load {ep.name}: {e}")
    return plugins
```

### 4. 懒加载优化

```python
class PluginRegistry:
    def __init__(self):
        self._entrypoints = {}
        self._loaded = {}
    
    def register_group(self, group):
        for ep in entry_points(group=group):
            self._entrypoints[ep.name] = ep
    
    def get(self, name):
        if name not in self._loaded:
            ep = self._entrypoints[name]
            self._loaded[name] = ep.load()  # 首次访问才加载
        return self._loaded[name]
```

---

## ✅ 优点

| 优点 | 说明 |
|------|------|
| **零配置** | 安装即用，无需手动注册 |
| **解耦** | 主程序不知道插件存在，插件不依赖主程序 |
| **懒加载** | 只在需要时导入，减少启动开销 |
| **可发现** | 可列出所有可用插件 |
| **版本独立** | 插件和主程序可独立发布 |

---

## ⚠️ 注意事项

### 1. 命名冲突

```toml
# ❌ 危险：不同包可能注册同名插件
[project.entry-points."takopi.engine_backends"]
claude = "my_package:BACKEND"  # 可能覆盖官方的 claude

# ✅ 安全：用唯一前缀
[project.entry-points."takopi.engine_backends"]
my-claude = "my_package:BACKEND"
```

### 2. 加载失败处理

```python
for ep in entry_points(group="myapp.plugins"):
    try:
        plugin = ep.load()
    except Exception as e:
        logger.error(f"Plugin {ep.name} failed to load: {e}")
        continue  # 跳过失败插件，不影响其他
```

### 3. 循环依赖

```
主程序 → 定义协议
插件 → 实现协议（依赖主程序）
主程序 → 发现插件（不导入直到运行时）
```

**解决**：协议放在独立包，或用 `typing.Protocol`

---

## 📚 实际案例

### 1. pytest

```toml
[project.entry-points.pytest11]
cov = "pytest_cov.plugin"
flake8 = "pytest_flake8.plugin"
```

### 2. Sphinx

```toml
[project.entry-points."sphinx.html_themes"]
sphinx_rtd_theme = "sphinx_rtd_theme"
```

### 3. VS Code Python

```toml
[project.entry-points."jupyter.kernelspecs"]
python3 = "ipykernel_launcher"
```

### 4. Takopi

```toml
[project.entry-points."takopi.engine_backends"]
claude = "takopi.runners.claude:BACKEND"

[project.entry-points."takopi.transport_backends"]
telegram = "takopi.telegram.backend:BACKEND"

[project.entry-points."takopi.command_backends"]
agent = "takopi.commands.agent:BACKEND"
```

---

## 🔍 调试技巧

### 查看 entry_points.txt 内容

```bash
# 找到包的安装位置
python -c "import takopi; print(takopi.__file__)"

# 查看元数据
cat /path/to/takopi-*.dist-info/entry_points.txt
```

### 验证插件是否被发现

```python
from importlib.metadata import entry_points

# 应该看到所有注册的插件
for ep in entry_points(group="takopi.engine_backends"):
    print(f"✓ {ep.name}")
```

### 强制刷新缓存

```bash
# 重新安装包
pip install -e . --force-reinstall

# 或清除 __pycache__
find . -name "__pycache__" -exec rm -rf {} +
```

---

## 📖 相关标准

| 标准 | 说明 |
|------|------|
| **PEP 370** | Per user site-packages |
| **PEP 517/518** | 构建系统标准化 |
| **PEP 621** | pyproject.toml 元数据（含 entry-points） |
| **PEP 685** | 依赖项比较规范 |

---

## 💡 最佳实践

1. **组名用点分层次**：`myapp.plugins.type`
2. **插件名用小写 + 连字符**：`my-plugin`
3. **导出对象用大写**：`BACKEND`, `PLUGIN`
4. **懒加载**：不要启动时加载所有插件
5. **错误隔离**：一个插件失败不影响其他
6. **版本兼容**：在文档中说明兼容的主程序版本

---

## 🔗 相关链接

- [Python 官方文档 - entry points](https://packaging.python.org/en/latest/specifications/entry-points/)
- [importlib.metadata 文档](https://docs.python.org/3/library/importlib.metadata.html)
- [Takopi 插件 API](https://github.com/banteg/takopi/blob/master/docs/reference/plugin-api.md)

---

*笔记由 OpenClaw 自动整理*
