# JSONL 格式详解

> **JSONL**（JSON Lines）= 每行一个 JSON 对象 —— 适合流式处理、日志存储、大数据场景

---

## 什么是 JSONL

**JSONL**（`.jsonl` 或 `.jsonlines`）是一种**每行一个 JSON 对象**的文本格式。

### 格式示例

```jsonl
{"name": "Alice", "age": 25, "city": "Beijing"}
{"name": "Bob", "age": 30, "city": "Shanghai"}
{"name": "Charlie", "age": 28, "city": "Guangzhou"}
```

### 核心规则

| 规则 | 说明 |
|------|------|
| ✅ 每行独立 | 每行是一个完整 JSON 对象 |
| ✅ 无需逗号 | 行与行之间不需要分隔符 |
| ✅ 单行对象 | 每个 JSON 对象必须在一行内（不能多行格式化） |
| ❌ 不是数组 | 文件整体不是 JSON 数组 |

---

## JSONL vs 标准 JSON

### 标准 JSON 写法
```json
[
  {"name": "Alice", "age": 25},
  {"name": "Bob", "age": 30},
  {"name": "Charlie", "age": 28}
]
```

### JSONL 写法
```jsonl
{"name": "Alice", "age": 25}
{"name": "Bob", "age": 30}
{"name": "Charlie", "age": 28}
```

### 对比表

| 维度 | 标准 JSON | JSONL |
|------|-----------|-------|
| **结构** | 单一根元素（数组/对象） | 每行独立 JSON |
| **分隔符** | 逗号分隔 | 换行分隔 |
| **文件大小** | 较小（无重复键） | 稍大（每行重复键） |
| **解析方式** | 一次性加载全部 | 逐行流式处理 |
| **内存占用** | 高（全量加载） | 低（逐行处理） |
| **追加写入** | ❌ 困难（需修改结尾） | ✅ 简单（直接 append） |
| **容错性** | ❌ 一处错误全文件失效 | ✅ 坏行可跳过 |
| **适用场景** | 配置文件、API 响应 | 日志、数据集、流式数据 |

---

## 核心优势

### 1. 流式处理（内存友好）

```python
# 逐行读取，大文件不爆内存
with open('data.jsonl', 'r') as f:
    for line in f:
        obj = json.loads(line)
        process(obj)  # 处理完即释放
```

### 2. 易于追加

```bash
# 直接追加新记录，无需修改原文件
echo '{"name": "David", "age": 35}' >> data.jsonl
```

### 3. 容错性强

- 某行损坏不影响其他行
- 适合日志、增量数据
- 可跳过坏行继续处理

### 4. 工具链支持好

- `jq` 原生支持
- 大数据工具（Spark、Hadoop）友好
- 机器学习数据集常用格式（HuggingFace、OpenAI）

---

## 常见用途

| 场景 | 说明 | 示例 |
|------|------|------|
| **日志文件** | 每行一条日志记录 | 服务器访问日志、应用日志 |
| **数据集** | 机器学习训练数据 | HuggingFace 数据集、微调数据 |
| **数据交换** | 流式 API 响应、批量导入导出 | 数据管道中间格式 |
| **中间数据** | ETL 管道中的临时存储 | 数据清洗、转换过程 |

---

## 常用命令

### jq 处理

```bash
# 转为 JSON 数组
jq -s '.' data.jsonl > data.json

# 提取每行的 name 字段
jq '.name' data.jsonl

# 过滤（age > 28）
jq 'select(.age > 28)' data.jsonl

# 转为紧凑格式（如果有多行 JSON）
jq -c '.' data.json > data.jsonl
```

### 其他命令

```bash
# 统计行数
wc -l data.jsonl

# 查看前 10 条
head -n 10 data.jsonl | jq '.'

# 查看最后 5 条
tail -n 5 data.jsonl | jq '.'

# 搜索包含关键字的行
grep "Beijing" data.jsonl | jq '.'

# 转换 JSON 数组 → JSONL
jq -c '.[]' data.json > data.jsonl

# 转换 JSONL → JSON 数组
jq -s '.' data.jsonl > data.json
```

---

## Python 读写示例

### 写入 JSONL

```python
import json

records = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
    {"name": "Charlie", "age": 28},
]

with open('data.jsonl', 'w') as f:
    for record in records:
        f.write(json.dumps(record) + '\n')
```

### 读取 JSONL

```python
import json

# 方式 1：逐行读取（推荐）
with open('data.jsonl', 'r') as f:
    for line in f:
        obj = json.loads(line)
        print(obj)

# 方式 2：一次性加载为列表
with open('data.jsonl', 'r') as f:
    records = [json.loads(line) for line in f]
```

### 追加写入

```python
def append_record(filepath, record):
    with open(filepath, 'a') as f:
        f.write(json.dumps(record) + '\n')

append_record('data.jsonl', {"name": "David", "age": 35})
```

---

## 注意事项

### ❌ 常见错误

```jsonl
// 错误：多行格式化
{
  "name": "Alice",
  "age": 25
}

// 错误：缺少换行
{"name": "Alice"}{"name": "Bob"}

// 错误：尾部逗号
{"name": "Alice"},
{"name": "Bob"}
```

### ✅ 正确写法

```jsonl
{"name": "Alice", "age": 25}
{"name": "Bob", "age": 30}
```

---

## 一句话总结

> **JSONL = 每行一个 JSON 对象** —— 牺牲一点空间换取更好的**可扩展性**、**流式处理能力**和**容错性**，是日志、数据集、大数据管道的首选格式。

---

**创建时间**:: 2026-04-04
**标签**:: #JSON #数据格式 #Python #大数据 #日志 #机器学习
