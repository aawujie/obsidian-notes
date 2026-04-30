# PDF 翻译工作流：pdftotext → LLM 子 Agent

> Date: 2026-04-30
> 以 Yogo DSAP NBER 课件翻译为案例

---

## 1. 总览

整个流程分两步，简单干净：

```
PDF 文件 → pdftotext 提取纯文本 → 子 Agent (LLM) 翻译 → 中文 Markdown
```

不需要 OCR、不依赖在线翻译 API、不手动复制粘贴。全命令行自动化。

---

## 2. 第一步：文本提取 — pdftotext

### 2.1 是什么

`pdftotext` 是 Poppler 工具包里的命令行工具，几乎所有 Linux 发行版都预装了。它直接读取 PDF 文件内部的文字流，按阅读顺序输出纯文本。

### 2.2 为什么能工作

PDF 文件本质上就是把文字 + 字体 + 坐标打包在一起的容器。`pdftotext` 做的事情就是：
- 解析 PDF 内部结构
- 提取每页的文字对象
- 按坐标位置重新排列成自然阅读顺序
- 输出纯文本

### 2.3 使用方法

```bash
# 基本用法
pdftotext input.pdf output.txt

# 只提取前 5 页
pdftotext -f 1 -l 5 input.pdf output.txt

# 保持物理布局（表格、列）
pdftotext -layout input.pdf output.txt
```

### 2.4 案例

Yogo 的 41 页 NBER 课件 PDF，一行命令提取全部文本：

```bash
pdftotext Yogo_DSAP_NBER2025_Slides.pdf /tmp/yogo_slides_full.txt
```

结果：1535 行、约 26KB 纯文本，包含所有标题、正文、表格、公式。几秒完成。

### 2.5 适用性

| 情况 | 能用 | 说明 |
|:---|:---|:---|
| 标准文字 PDF | ✅ | 绝大多数论文、课件、电子书 |
| 扫描版 PDF | ❌ | 需要 OCR（文字是图片，不是文本流） |
| 数学公式 | ⚠️ 部分 | LaTeX 公式可提取，手写公式不行 |
| 图表 | ❌ | 只能提取图表中的文字标注 |

---

## 3. 第二步：翻译 — LLM 子 Agent

### 3.1 为什么用子 Agent 而不是翻译 API

- **语境理解**：LLM 理解学术语境。知道 SDF = 随机折现因子、IV = 工具变量，不会硬翻
- **格式保留**：要求 LLM 保持原文结构（标题、列表、公式、引用），输出 Markdown
- **术语准确**：可以指定学术术语的翻译规范
- **全本地**：不依赖 Google Translate / DeepL API，不受限制

### 3.2 工作方式

```python
# 伪代码逻辑
text = open("extracted.txt").read()

# 发送给 LLM 子 Agent
task = f"""
Translate to Chinese. Preserve structure.
Academic terms: SDF=随机折现因子, DSAP=需求系统资产定价
Content: {text}
"""
result = subagent.run(task)
```

### 3.3 Prompt 设计要点

发给 LLM 的翻译指令必须包含：

1. **明确翻译方向**：English → Chinese
2. **学术术语映射表**：专业术语的正确翻译
3. **保留规则**：公式不动、数字不动、引用不动
4. **格式要求**：输出 Markdown，保留原标题层级
5. **不要自由发挥**：严格翻译，不要总结或评论

---

## 4. 完整流程复盘（Yogo 课件案例）

### 实际操作步骤

```bash
# Step 1: 提取文本
pdftotext Yogo_DSAP_NBER2025_Slides.pdf /tmp/yogo_slides_full.txt

# Step 2: 检查提取结果
wc -l /tmp/yogo_slides_full.txt  # 1535 行
head -50 /tmp/yogo_slides_full.txt  # 预览前50行

# Step 3: 派给子 Agent 翻译
# 将文本 + 翻译指令发送给 OpenClaw 子 Agent
# 子 Agent 逐段翻译，输出中文 Markdown

# Step 4: 保存结果
mv /tmp/yogo_slides_cn.md 目标路径
```

### 关键指标

| 指标 | 值 |
|:---|:---|
| PDF 页数 | 41 |
| 提取文本量 | ~26KB / 1535 行 |
| 提取耗时 | < 1 秒 |
| 翻译方式 | LLM 子 Agent |
| 输出格式 | 中文 Markdown |
| 公式/数字 | 原样保留 |

---

## 5. 方法论价值

这套方法的价值不在"能翻译 PDF"——而是在**完全本地化、可复现、可批量**。

- **可复现**：换一个 PDF，走同样的 pdftotext → LLM 流程即可
- **可批量**：后续可以在脚本里批量处理多个 PDF 论文
- **可定制**：不同学科换不同的术语映射表
- **学术友好**：保留了公式、引用、图表标注，不是简单机翻

---

## 6. 局限性

1. **扫描版 PDF 不适用** — 需要先 OCR（Tesseract / PaddleOCR）
2. **大 PDF 需分段处理** — 单次 LLM 上下文有限，超过 10 万字符需拆开翻译
3. **图表信息丢失** — 纯文本提取会丢掉图表，如需保留图表需要更复杂的处理
4. **非英语 PDF** — pdftotext 对中文 PDF 的提取效果取决于字体嵌入方式
