# marimo - 下一代 Python 笔记本

> marimo 是一个响应式 Python 笔记本，定位为 Jupyter Notebook 的现代化替代品。
> 官网：https://marimo.io | 文档：https://docs.marimo.io

---

## 快速上手

### 安装

```bash
# pip
pip install marimo

# uv（推荐）
uv pip install marimo
```

### 核心命令

```bash
# 启动交互式教程（入门推荐）
marimo tutorial intro

# 创建/编辑笔记本
marimo edit                      # 打开笔记本服务器
marimo edit my_notebook.py       # 编辑指定笔记本

# 以只读 Web App 模式运行
marimo run my_notebook.py

# 当作普通 Python 脚本运行
python my_notebook.py

# 从 Jupyter 转换
marimo convert notebook.ipynb -o notebook.py
```

---

## 核心特性

### 1. 响应式执行

marimo 最大的亮点。当你修改一个 cell 时，所有依赖它的下游 cell **自动重新执行**。

```
# Cell 1
x = 10

# Cell 2（依赖 x，修改 Cell 1 后自动重跑）
y = x * 2
print(y)  # 自动更新
```

不再需要手动"Run All"或担心"上面的 cell 忘了跑"。

### 2. 纯 Python 文件

笔记本保存为 `.py` 文件，不是 JSON。意味着：
- Git diff 干净可读
- 可以直接 `import` 笔记本中的函数
- 可以用任何编辑器打开

### 3. 内置交互组件

```python
import marimo as mo

# 滑块
slider = mo.ui.slider(1, 100, value=50)

# 下拉框
dropdown = mo.ui.dropdown(["选项A", "选项B", "选项C"])

# 文本输入
text = mo.ui.text(placeholder="输入点什么...")
```

交互组件的值变化时，依赖的 cell 自动更新，无需回调函数。

### 4. SQL 支持

可以直接在 cell 里写 SQL 查询数据库或 DataFrame：

```python
# 直接对 DataFrame 写 SQL
result = mo.sql(f"SELECT * FROM {df} WHERE age > 30")
```

### 5. 一键部署 Web App

```bash
marimo run my_analysis.py
```

笔记本直接变成可交互的 Web 应用，适合分享给不懂代码的人。

---

## marimo vs Jupyter Notebook 对比

| 维度 | Jupyter Notebook | marimo |
|------|-----------------|--------|
| **执行模式** | 手动逐 cell 执行，顺序任意 | 响应式自动执行，依赖驱动 |
| **文件格式** | `.ipynb`（JSON） | `.py`（纯 Python） |
| **Git 友好度** | 差（JSON diff 不可读，常冲突） | 好（标准 Python diff） |
| **隐藏状态** | 有（删了 cell 变量还在内存里） | 无（自动清理无效变量） |
| **可复现性** | 差（36%+ 笔记本无法复现） | 好（执行顺序由依赖图决定） |
| **交互组件** | 需要 ipywidgets + 回调 | 内置，自动联动 |
| **部署为 App** | 需要 Voilà/Streamlit 等额外工具 | 原生支持 `marimo run` |
| **作为脚本运行** | 需要 nbconvert 转换 | 直接 `python xxx.py` |
| **import 复用** | 不支持 | 支持（import 笔记本中的函数） |
| **变量定义** | 同名变量可在多个 cell 定义 | 每个变量只能在一个 cell 定义 |
| **生态/社区** | 成熟（数十年积累） | 年轻但增长快 |
| **学习成本** | 低（大家都熟悉） | 低-中（需适应响应式思维） |

---

## marimo 的限制

### 1. 变量不能重复定义

每个变量只能在一个 cell 中定义。如果你习惯在多个 cell 里覆盖同一个变量（比如不断修改 `df`），需要改变写法：

```python
# ❌ 不行：两个 cell 都定义了 df
# Cell 1
df = pd.read_csv("data.csv")
# Cell 2
df = df.dropna()  # 报错！df 已在 Cell 1 定义

# ✅ 正确：合并到一个 cell，或用不同变量名
# Cell 1
raw_df = pd.read_csv("data.csv")
# Cell 2
clean_df = raw_df.dropna()
```

### 2. 生态不如 Jupyter 成熟

一些 Jupyter 扩展和特殊集成可能还没有 marimo 版本。

### 3. 团队协作

如果团队都在用 Jupyter，切换有迁移成本。

---

## 什么时候用 marimo？什么时候用 Jupyter？

### 推荐用 marimo

- 数据分析项目需要**可复现性**
- 需要**版本管理**（Git）
- 要做**交互式 Dashboard / App**
- 探索性分析中经常**调参、改变量**
- 想把笔记本中的函数**复用到其他项目**

### 继续用 Jupyter

- 团队已有大量 Jupyter 笔记本且无迁移计划
- 依赖 Jupyter 特有的扩展（如 nbgrader）
- 教学场景（学生更熟悉 Jupyter）
- 需要和 Colab / Kaggle 等平台配合

---

## 从 Jupyter 迁移

```bash
# 转换单个笔记本
marimo convert my_notebook.ipynb -o my_notebook.py

# 转换后用 marimo 打开
marimo edit my_notebook.py
```

转换后可能需要手动处理：
- 同名变量重定义的问题
- 某些 Jupyter magic command（如 `%matplotlib inline`）

---

## 个人评价

marimo 解决了 Jupyter 的几个核心痛点：**隐藏状态、不可复现、Git 不友好**。响应式执行模式一旦习惯了，回不去 Jupyter 那种"手动管理执行顺序"的方式。

对于量化研究、数据分析这类需要频繁迭代和调参的场景，marimo 的体验明显更好。但如果只是写个简单的教程或一次性分析，Jupyter 也完全够用。

**建议**：新项目直接用 marimo，老项目按需迁移。

---

#Python #笔记本 #marimo #Jupyter #数据分析 #工具
