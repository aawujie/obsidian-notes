# 5.Finance 审计修复与补充计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 修复审计报告中发现的公式损坏、文件冗余、结构问题，并补充最关键的量化知识缺口

**Architecture:** 分两阶段 — Phase 1 修复已有内容（合并同名文件、修正公式、更新索引、清理空壳），Phase 2 补充缺失的量化知识（衍生品、微观结构、协整、Black-Litterman）。每阶段独立可交付。

**前置验证: 审计报告的"重复"发现已修正 — 同名文件大多是同一主题的不同版本（内容有差异），不是简单复制。只有 3 对是真正完全相同的文件。**

**Tech Stack:** Obsidian Markdown + KaTeX 公式 + Wikilinks

**审计来源:** 2026-06-04 审计报告，见会话上下文

---

## Phase 1: 修复与清理（纯文件操作）

### Task 1: 修复 Chapter 1.md 公式损坏（CRITICAL）

**Files:**
- Modify: `5.Finance/00-因子投资/Chapter 1.md:179-418`

**背景:** 从第 179 行 `## 详解 $E[R_i^e] = \boldsymbol{\beta}_i' \boldsymbol{\lambda}$` 开始到文件末尾，KaTeX 公式大面积损坏 — 出现 `CEHOLDER}`、重复的 `**和**`、符号错位。两个核心段落需要重写：
- `详解 E[R_i^e] = β_i'λ` (向量展开与点积)
- `详解 Σ = β Σ_λ β' + Σ_ε` (方差模型降维直觉)

**Step 1: 确认损坏范围**

```bash
grep -n "CEHOLDER" 5.Finance/00-因子投资/Chapter\ 1.md
# Expected: lines 181, 191, 213 出现 CEHOLDER} 标记
grep -c "CEHOLDER" 5.Finance/00-因子投资/Chapter\ 1.md
# Expected: 3
```

**Step 2: 删除损坏部分（行 179-418），替换为重写内容**

损坏内容覆盖两个子章节。替换内容必须保持与原笔记风格一致：中文解释 + KaTeX 公式 + 直觉比喻。

替换内容如下：

```markdown
## 详解 $E[R_i^e] = \boldsymbol{\beta}_i' \boldsymbol{\lambda}$

这个公式之所以看起来像"单因子"，是因为它使用了**向量（Vector）**和**矩阵代数**的缩写形式。数学上的"多因子"体现在符号的**加粗**和右上角的**转置符号 $'$** 上。

### 1. 符号的展开

**$\boldsymbol{\beta}_i$（因子暴露向量）**：不是一个单一的 $\beta$ 值，而是包含了资产 $i$ 对 $K$ 个不同因子的敏感度。

$$
\boldsymbol{\beta}_i = \begin{bmatrix}
\beta_{i,1} \\
\beta_{i,2} \\
\vdots \\
\beta_{i,K}
\end{bmatrix}
$$

*(例如：$\beta_{i,1}$ 是市场贝塔，$\beta_{i,2}$ 是规模贝塔，$\beta_{i,3}$ 是价值贝塔...)*

**$\boldsymbol{\lambda}$（因子溢价向量）**：代表了这 $K$ 个因子各自的预期收益率。

$$
\boldsymbol{\lambda} = \begin{bmatrix}
\lambda_1 \\
\lambda_2 \\
\vdots \\
\lambda_K
\end{bmatrix}
$$

### 2. 运算的展开

公式中的 $'$ 表示**转置**。$\boldsymbol{\beta}_i'$ 将列向量转成行向量，再与 $\boldsymbol{\lambda}$ 做**点积**：

$$
E[R_i^e] = [\beta_{i,1}, \beta_{i,2}, \cdots, \beta_{i,K}] \times \begin{bmatrix}
\lambda_1 \\
\lambda_2 \\
\vdots \\
\lambda_K
\end{bmatrix}
$$

展开后：

$$
E[R_i^e] = \underbrace{\beta_{i,1}\lambda_1}_{\text{因子1贡献}} + \underbrace{\beta_{i,2}\lambda_2}_{\text{因子2贡献}} + \cdots + \underbrace{\beta_{i,K}\lambda_K}_{\text{因子K贡献}}
$$

### 3. 具体例子（Fama-French 三因子）

如果是一个三因子模型（市场、规模、价值），这个简短的公式实际上代表：

$$
E[R_i^e] = \beta_{i,Mkt} \cdot \lambda_{Mkt} + \beta_{i,SMB} \cdot \lambda_{SMB} + \beta_{i,HML} \cdot \lambda_{HML}
$$

**总结：** 数学家为了书写简洁，把后面这一长串加法公式压缩成了 $\boldsymbol{\beta}_i' \boldsymbol{\lambda}$ 两个符号的乘积。"多因子"就隐藏在代表向量的**加粗字体**里。

---

## 详解 $\boldsymbol{\Sigma} = \boldsymbol{\beta} \boldsymbol{\Sigma}_\lambda \boldsymbol{\beta}' + \boldsymbol{\Sigma}_\varepsilon$

这个公式是量化投资（特别是风险管理）中**最重要**也**最昂贵**（因为 Barra 等商业模型卖得很贵）的公式之一。

**核心作用**：把一个极其复杂、几乎无法计算的数学难题，变成了一个简单可控的计算题。

### 1. 推导逻辑

基于第 1.4 节提到的**时序回归模型**推导。假设 $N$ 个资产在某一时刻的收益率向量 $\boldsymbol{R}$ 由两部分组成：

1. **共同因子部分**：$\boldsymbol{\beta} \boldsymbol{\lambda}$（因子暴露 $\times$ 因子收益）
2. **特质（残差）部分**：$\boldsymbol{\varepsilon}$（个股独有的波动）

即：$\boldsymbol{R} = \boldsymbol{\beta} \boldsymbol{\lambda} + \boldsymbol{\varepsilon}$

对等式两边求**协方差**，假设因子收益 $\boldsymbol{\lambda}$ 与特质收益 $\boldsymbol{\varepsilon}$ 不相关（Cov = 0），且 $\boldsymbol{\beta}$ 是常数矩阵，得到：

$$\underbrace{\boldsymbol{\Sigma}}_{\text{资产的总风险}} = \underbrace{\boldsymbol{\beta} \boldsymbol{\Sigma}_\lambda \boldsymbol{\beta}'}_{\text{系统性风险（因子风险）}} + \underbrace{\boldsymbol{\Sigma}_\varepsilon}_{\text{特质性风险（残差风险）}}$$

### 2. 结构拆解

假设有 $N = 3000$ 只股票（A 股数量），模型选用 $K = 10$ 个因子。

| 符号 | 维度 | 含义 |
|:---|:---|:---|
| $\boldsymbol{\Sigma}$ | $3000 \times 3000$ | **资产协方差矩阵**，描述任意两只股票之间的同涨同跌关系 |
| $\boldsymbol{\beta}$ | $3000 \times 10$ | **因子暴露矩阵**，如某只股票是"高波动、大市值、银行股" |
| $\boldsymbol{\Sigma}_\lambda$ | $10 \times 10$ | **因子协方差矩阵**，描述因子间如何互动（如大盘涨时小市值因子跌？） |
| $\boldsymbol{\Sigma}_\varepsilon$ | $3000 \times 3000$ | **特质风险矩阵**。关键假设：个股特质波动互不相关 → **对角阵**（只有对角线上有数字） |

### 3. 核心价值：降维打击

**直接计算的困境**：要算 $3000 \times 3000$ 的协方差矩阵，需要估计 $3000 \times 3001 / 2 \approx 450$ 万个参数。要准确估计 450 万个参数，需要长达几百年的日线数据。如果样本天数 $T < N$（肯定小于），矩阵不可逆，**无法做投资组合优化**。

**方差模型的魔法**：通过 $\boldsymbol{\Sigma} = \boldsymbol{\beta} \boldsymbol{\Sigma}_\lambda \boldsymbol{\beta}' + \boldsymbol{\Sigma}_\varepsilon$，参数数量变为：

1. $\boldsymbol{\beta}$：$3000 \times 10 = 30,000$ 个
2. $\boldsymbol{\Sigma}_\lambda$：$10 \times 11 / 2 = 55$ 个
3. $\boldsymbol{\Sigma}_\varepsilon$：$3000$ 个（只算对角线方差）

**总计参数量：约 3.3 万个**，从 450 万压缩到了 3.3 万——减少了 99% 以上。

### 4. 直观比喻

想象股票是一群**木偶**。直接做法是观察每一对木偶之间的动作关系（450 万对），乱成一团。Barra 的做法是：找到木偶上方的**几根提线**（因子）和一只**看不见的手**（因子收益率），只需要研究：
- 这只手的动作（$\boldsymbol{\Sigma}_\lambda$，因子波动）
- 每根线绑在哪个部位（$\boldsymbol{\beta}$，因子暴露）
- 木偶自己随风的轻微抖动（$\boldsymbol{\Sigma}_\varepsilon$，特质风险）

这样就能完美预测整群木偶的运动幅度（组合风险）。

---
```

**Step 3: 验证文件完整性**

```bash
wc -l 5.Finance/00-因子投资/Chapter\ 1.md
# 文件应有合理行数（~250-350 行，删除了损坏的 240 行后）
grep -c "CEHOLDER" 5.Finance/00-因子投资/Chapter\ 1.md
# Expected: 0（无残留损坏标记）
```

**Step 4: Commit**

```bash
git add 5.Finance/00-因子投资/Chapter\ 1.md
git commit -m "fix: 修复 Chapter 1.md 后半部分 KaTeX 公式损坏

删除 179-418 行的 CEHOLDER 乱码内容，重写：
- 矩阵代数展开详解（β_i'λ 向量点积）
- 方差模型降维详解（Σ = β Σ_λ β' + Σ_ε）
保留原笔记风格：中文解释 + KaTeX + 直觉比喻"
```

---

### Task 2: 修复 Cheatsheet.md Math 部分公式格式（HIGH）

**Files:**
- Modify: `5.Finance/00-因子投资/Cheatsheet.md:264-1053`

**背景:** "Math" 部分（模块一~模块十二）中，KaTeX 公式与纯文本错误的 ```` ```plain text ```` 代码块混排。变量名重复三次（如 `PtP_tPt`），来自原始 HTML→Markdown 转换失败。

**修复策略:** 不重写内容（数学推导正确），只修正**格式**——将 `plain text` 代码块内的公式提取为正确的 KaTeX inline/block。

**Step 1: 确认损坏范围**

```bash
grep -n '```plain text' 5.Finance/00-因子投资/Cheatsheet.md | head -20
# Expected: 大量 plain text 代码块行号
grep -c '```plain text' 5.Finance/00-因子投资/Cheatsheet.md
# Expected: ~50+
```

**Step 2: 逐模块修正格式**

修复原则：
- `PtP_tPt` → 删除重复，保留 `$P_t$`
- `Xt+1X_{t+1}Xt+1` → `$X_{t+1}$`
- `E[Rie]=βi,1λ1+βi,2λ2+⋯+βi,KλK(+αi)E[R_i^e] = ...` → `$$E[R_i^e] = \beta_{i,1}\lambda_1 + \beta_{i,2}\lambda_2 + \dots + \beta_{i,K}\lambda_K (+ \alpha_i)$$`
- `βi,k\beta_{i,k}βi,k` → `$\beta_{i,k}$`
- 所有 ` ```plain text ` 公式块 → 改为 KaTeX `$$...$$` 或 `$...$`

**示例修正（模块一 资产定价基本方程）：**

Before:
````
所有资产价格

```plain text
        PtP_tPt
```

等于未来支付

```plain text
        Xt+1X_{t+1}Xt+1
```

乘以随机折现因子

```plain text
        Mt+1M_{t+1}Mt+1
```

的期望：

```plain text
        Pt=Et[Mt+1Xt+1]P_t = E_t [ M_{t+1} X_{t+1} ]Pt=Et[Mt+1Xt+1]
```
````

After:
```markdown
所有资产价格 $P_t$ 等于未来支付 $X_{t+1}$ 乘以随机折现因子 $M_{t+1}$ 的期望：

$$P_t = E_t [ M_{t+1} X_{t+1} ]$$

- **推论：** 如果 $P_t = 1$（考虑收益率 $R_{t+1}$），则 $1 = E_t [ M_{t+1} (1 + R_{t+1}) ]$。
- **含义：** 资产的超额收益 $E[R^e]$ 取决于它与 $M$（宏观坏时光）的协方差：

$$E[R_i^e] \approx -R_f \cdot \text{Cov}(R_i, M)$$
```

**Step 3: 验证**

```bash
grep -c '```plain text' 5.Finance/00-因子投资/Cheatsheet.md
# Expected: 0（所有 plain text 块已替换为 KaTeX）
```

**Step 4: Commit**

```bash
git add 5.Finance/00-因子投资/Cheatsheet.md
git commit -m "fix: 修复 Cheatsheet.md Math 部分公式格式

将 ~50 个 plain text 代码块替换为正确的 KaTeX 公式，
修复变量名重复渲染问题（PtP_tPt → P_t）"
```

---

### Task 3: 合并 Jie TradingNote 中 7 个同名但不同版本的文件

**背景:** 这 7 个文件在 `01-交易与策略/`（上层）和 `Jie TradingNote/`（下层）各有一份，**但不是简单重复**——它们是同一主题的两个版本：
- 上层版本：已迁移为标准 frontmatter（`title/type/created/updated`），内容可能经过整理
- 下层版本：保留 Notion 导入原始 frontmatter（`notion-id/Last edited time`），内容与上层有差异

**Files:**
- Merge (manual): `5.Finance/01-交易与策略/Jie TradingNote/斐波那契.md` → `5.Finance/01-交易与策略/斐波那契.md`
- Merge (manual): `5.Finance/01-交易与策略/Jie TradingNote/期权 VS 期货.md` → `5.Finance/01-交易与策略/期权 VS 期货.md`
- Merge (manual): `5.Finance/01-交易与策略/Jie TradingNote/庄家是如何操纵现货合约价格最终收割散户.md` → `5.Finance/01-交易与策略/庄家是如何操纵现货合约价格最终收割散户.md`
- Merge (manual): `5.Finance/01-交易与策略/Jie TradingNote/卓野-活下来.md` → `5.Finance/01-交易与策略/卓野-活下来.md`
- Merge (manual): `5.Finance/01-交易与策略/Jie TradingNote/卓野-基本面研究.md` → `5.Finance/01-交易与策略/卓野-基本面研究.md`
- Merge (manual): `5.Finance/01-交易与策略/Jie TradingNote/卓野-入场时机：支撑&阻力.md` → `5.Finance/01-交易与策略/卓野-入场时机：支撑&阻力.md`
- Merge (manual): `5.Finance/01-交易与策略/Jie TradingNote/K线形态.md` → `5.Finance/01-交易与策略/K线形态.md`

**Step 1: 逐文件 diff 查看差异**

```bash
for f in \
  "斐波那契.md" \
  "期权 VS 期货.md" \
  "庄家是如何操纵现货合约价格最终收割散户.md" \
  "卓野-活下来.md" \
  "卓野-基本面研究.md" \
  "卓野-入场时机：支撑&阻力.md" \
  "K线形态.md"; do
  echo "====== $f ======"
  diff "5.Finance/01-交易与策略/$f" "5.Finance/01-交易与策略/Jie TradingNote/$f" | head -40
  echo ""
done
```

**Step 2: 人工判断合并方向**

每个文件二选一策略：
- **策略 A（保留上层）**: 上层已经是标准 frontmatter，内容可能更精简。如果有缺失的重要内容，从下层版本补入
- **策略 B（保留下层 + 迁移 frontmatter）**: 下层版本内容更完整，但 frontmatter 需要迁移为标准格式

优先策略 A（保留已迁移的上层版本），只有当 diff 显示下层有实质性额外内容时才考虑策略 B。

**Step 3: 合并后删除下层版本，更新 Wikilinks**

```bash
cd 5.Finance/01-交易与策略/Jie\ TradingNote/
git rm "斐波那契.md"
git rm "期权 VS 期货.md"
git rm "庄家是如何操纵现货合约价格最终收割散户.md"
git rm "卓野-活下来.md"
git rm "卓野-基本面研究.md"
git rm "卓野-入场时机：支撑&阻力.md"
git rm "K线形态.md"

# 检查是否有内部链接指向这些已删除文件
grep -rn "斐波那契\|期权 VS 期货\|庄家.*操纵\|卓野.*活下来\|卓野.*基本面\|卓野.*入场\|K线形态" . --include="*.md" 2>/dev/null || echo "No internal links to update"
```

**Step 4: Commit**

```bash
git commit -m "refactor: 合并 Jie TradingNote 中 7 个同名文件到上层

两个版本为同一主题不同阶段：上层是已迁移的标准格式，
下层是原始 Notion 导入格式。合并后保留下层删除。
斐波那契、期权VS期货、庄家操纵、卓野×3、K线形态"
```

---

### Task 4: 更新 index.md

**Files:**
- Modify: `5.Finance/index.md`

**背景:** index.md 从 2026-04-17 未更新，只列出 3 篇文章，缺少所有子目录索引。

**Step 1: 替换 index.md 全部内容**

```markdown
# 5.Finance 知识库索引

> 金融 / 投资 / 量化交易 — 因子投资、交易策略、金融理论、加密货币
> 更新于: 2026-06-04 · 审计后重建

## 子目录

| 目录 | 内容 | 文件数 |
|:---|:---|:---|
| [[00-因子投资/]] | 因子模型、Barra、回归方法、统计概念 | ~49 |
| [[01-交易与策略/]] | 交易系统、技术分析、量化策略 | ~100 |
| [[02-加密货币/]] | 区块链、DeFi、钱包、交易所 | ~70 |
| [[03-计量经济学/]] | 时间序列、统计检验、因子评价 | ~25 |
| [[04-金融理论/]] | EMH、CAPM、MVO、MM定理 | 9 |
| [[05-理财与财富建设/]] | 个人理财、财富自由 | 4 |
| [[06-股票与投资基础/]] | A股美股基础、ETF | 5 |
| [[投研日记/]] | 日常研究记录、个股调研 | ~100 |

## 核心理论

- [[马科维茨均值方差模型]] — 现代投资组合理论基石，MVO 核心公式与有效前沿
- [[CAPM - Capital Asset Pricing Model]] — 单因子资产定价模型
- [[有效市场假说 - EMH 详解]] — EMH 三种形式、行为金融学挑战、A 股适用性
- [[MM 定理 - Modigliani_Miller Theorem]] — 资本结构无关性定理

## 量化核心

- [[00-因子投资/Chapter 1]] — 因子投资数学基础（CAPM → 多因子 → 方差模型）
- [[00-因子投资/Chapter 2]] — 排序法、时序/截面回归、Fama-MacBeth、GRS 检验
- [[00-因子投资/Cheatsheet]] — 因子投资全术语速查 + 核心公式
- [[回测四大技术笔记]] — 参数敏感性、滚动窗口、压力测试、蒙特卡洛
- [[量化因子挖掘七条教训]] — 因子研究实战经验总结
- [[厚尾建模与正偏态发现-5因子策略EVT实证]] — EVT + 跳跃扩散 + Kelly 仓位
- [[HMM Regime Detection-用隐马尔可夫模型识别市场状态]] — 市场状态切换

## 策略研究

- [[龙虎榜中频事件驱动策略]] — 机构席位跟风，夏普 5.20
- [[量化交易终极框架-尾部风险与生存系统]] — 七层系统架构
- [[卡尔曼滤波在量化中的应用]] — 动态对冲比、因子权重自适应
- [[正交化与滑点]] — 正交化能清洗信号，不能解决滑点

## 学习路线

1. **入门**: [[00-因子投资/Cheatsheet]] 绿色部分 → [[04-金融理论/]]
2. **建模**: Cheatsheet 黄色部分 → Chapter 1 → Chapter 2
3. **实战**: [[回测四大技术笔记]] → [[量化因子挖掘七条教训]]
4. **进阶**: [[实证资产定价中高阶学习资料索引]] → EVT/HMM 实证项目

## 待补充

- [ ] 衍生品定价（Black-Scholes, Greeks）
- [ ] 市场微观结构（订单簿模型, 最优执行）
- [ ] 协整与统计套利（配对交易）
- [ ] Black-Litterman 模型
- [ ] 风险平价（Risk Parity）详解
- [ ] A 股制度性知识系统整理（壳价值、涨跌停）
- [ ] 相关金融内容也分布在 [[7.AI Summary/投资与金融/]] 中
- [ ] [[6.BookNotes/《因子投资：方法与实践》/]] 有深度金融笔记

## 工具与资源

- 市场数据日报: [[DailyData/]]
- PandaAI 因子框架: [[PandaAI官方/PandAI 知识库]]
- Polymarket 预测市场: [[Polymarket UpDown 市场上6种主要的交易机器人类型]]
```

**Step 2: Commit**

```bash
git add 5.Finance/index.md
git commit -m "docs: 重建 5.Finance/index.md 索引页

审计后更新：添加所有子目录索引、核心理论链接、
量化核心文档、学习路线、待补充清单"
```

---

### Task 5: 清理 DailyData/geopolitics 空壳文件 + 其他空文件

**Files:**
- Delete: `5.Finance/DailyData/geopolitics/2026-05-13.md` 到 `2026-06-04.md` 中的空壳（共 ~16 个仅 4 行的文件）

**Step 1: 确认空壳文件**

```bash
find 5.Finance/DailyData/geopolitics/ -name "*.md" -exec wc -l {} \; | awk '$1 <= 5 {print $2}'
# Expected: 列出 ~16 个 4 行以下文件
```

**Step 2: 检查是否有关联 JSON 数据**

```bash
# 确认对应 .json 文件也存在（如有 json 则文件仍有价值，不删除）
for f in $(find 5.Finance/DailyData/geopolitics/ -name "*.md" -exec wc -l {} \; | awk '$1 <= 5 {print $2}'); do
  json="${f%.md}.json"
  if [ -f "$json" ]; then
    echo "KEEP: $f (has companion JSON)"
  else
    echo "DELETE: $f (no companion JSON)"
  fi
done
```

**Step 3: 只删除无 companion JSON 的空壳**

```bash
# 根据 Step 2 输出，只删除无 JSON 的空壳
cd 5.Finance/DailyData/geopolitics/
# 逐文件 git rm
```

**Step 4: Commit**

```bash
git commit -m "chore: 清理 DailyData/geopolitics 无数据的空壳文件"
```

---

## Phase 2: 知识补充（内容创作）

### Task 6: 新增衍生品定价基础 — Black-Scholes + Greeks

**Files:**
- Create: `5.Finance/04-金融理论/Black-Scholes 期权定价模型.md`
- Create: `5.Finance/04-金融理论/期权 Greeks 详解.md`

**内容范围:**
- Black-Scholes: 假设、公式推导直觉、Put-Call Parity、隐含波动率
- Greeks: Delta/Gamma/Vega/Theta/Rho 各自的定义、交易含义、盈亏分解

**Step 1: 创建 Black-Scholes 笔记**

```bash
touch "5.Finance/04-金融理论/Black-Scholes 期权定价模型.md"
```

模板：
```markdown
---
title: Black-Scholes 期权定价模型
type: concept
created: 2026-06-04
updated: 2026-06-04
tags: [衍生品, 期权, 定价, Black-Scholes, 量化]
---

# Black-Scholes 期权定价模型

## 一句话

Black-Scholes 告诉你：一个欧式期权的"公平价格"应该是多少，假设股票价格服从几何布朗运动。

## 核心公式

### 看涨期权 (Call)

$$C = S_0 N(d_1) - K e^{-rT} N(d_2)$$

### 看跌期权 (Put) — 由 Put-Call Parity 导出

$$P = K e^{-rT} N(-d_2) - S_0 N(-d_1)$$

其中：

$$d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}$$

$$d_2 = d_1 - \sigma\sqrt{T}$$

| 符号 | 含义 |
|:---|:---|
| $S_0$ | 当前股价 |
| $K$ | 行权价 |
| $r$ | 无风险利率 |
| $\sigma$ | 波动率（唯一不可观测的参数） |
| $T$ | 到期时间（年） |
| $N(\cdot)$ | 标准正态分布的累积分布函数 |

## 核心假设

| 假设 | 现实 |
|:---|:---|
| 股价服从几何布朗运动（连续、无跳跃） | ❌ 实际有跳跃 |
| 波动率恒定 | ❌ 实际波动率时变（波动率微笑） |
| 无交易成本、无税费 | ❌ 实际有摩擦 |
| 可以连续交易、任意做空 | ❌ 有做空限制 |
| 无风险利率恒定 | ⚠️ 短期近似 |

## Put-Call Parity（买卖权平价）

$$C + K e^{-rT} = P + S_0$$

**直觉**：持有看涨期权 + 现金 = 持有看跌期权 + 股票。如果这个等式不成立，就存在无风险套利。

## 隐含波动率 (Implied Volatility, IV)

BS 公式中唯一不可直接观测的参数是 $\sigma$。**隐含波动率**就是反解 BS 公式得到的 $\sigma$ —— 把市场价格 $C_{market}$ 代入，解出 $\sigma_{IV}$。

$$C_{market} = BS(S_0, K, r, T, \sigma_{IV})$$

- IV 是市场对未来波动的**预期**，不等同于历史波动率
- **波动率微笑 (Volatility Smile)**：不同行权价的 IV 不同 → BS 假设 $\sigma$ 恒定的证据不成立

## 与因子投资的关系

- 因子投资关注**横截面**：为什么股票 A 比股票 B 收益高？
- BS 模型关注**纵截面**：同一资产、不同行权价/到期日的期权之间如何定价？
- 量化多策略通常两者都用：因子选股 + 期权对冲尾部风险

## 相关笔记

- [[马科维茨均值方差模型]] — BS 的 $\sigma$ 来自 MVO 的协方差矩阵
- [[有效市场假说 - EMH 详解]] — BS 假设无套利，与 EMH 一致
```

**Step 2: 创建 Greeks 笔记**

类似结构，覆盖 Delta/Gamma/Vega/Theta/Rho + 实际交易中的 Greeks 盈亏分解。

**Step 3: 更新 index.md 添加链接**

在 `5.Finance/index.md` 核心理论区添加：
```markdown
- [[Black-Scholes 期权定价模型]] — 欧式期权定价与隐含波动率
- [[期权 Greeks 详解]] — Delta/Gamma/Vega/Theta/Rho 交易含义
```

**Step 4: Commit**

```bash
git add 5.Finance/04-金融理论/Black-Scholes\ 期权定价模型.md
git add 5.Finance/04-金融理论/期权\ Greeks\ 详解.md
git add 5.Finance/index.md
git commit -m "feat: 新增衍生品定价基础 — Black-Scholes + Greeks"
```

---

### Task 7: 新增市场微观结构基础

**Files:**
- Create: `5.Finance/concepts/订单簿与市场微观结构.md`

**内容范围:** bid-ask spread、市场深度、Kyle (1985) 模型直觉、Glosten-Milgrom (1985) 信息不对称、最优执行 Almgren-Chriss (2001) 框架

**Step 1: 创建笔记**

覆盖三个层次：
1. 订单簿基础（L1/L2/L3 数据、价差、深度）
2. 微观结构理论（信息不对称 → bid-ask spread 存在的根本原因）
3. 最优执行（Almgren-Chriss 框架：临时冲击 + 永久冲击 → 最优拆单曲线）

**Step 2: Commit**

```bash
git add 5.Finance/concepts/订单簿与市场微观结构.md
git commit -m "feat: 新增市场微观结构基础概念页"
```

---

### Task 8: 新增协整与统计套利

**Files:**
- Create: `5.Finance/concepts/协整与配对交易.md`

**内容范围:** 平稳性 vs 协整、Engle-Granger 两步法、Johansen 检验、配对交易策略构建（选对→检验→确定对冲比→开仓→止损→平仓）

**Step 1: 创建笔记**

**Step 2: Commit**

```bash
git add 5.Finance/concepts/协整与配对交易.md
git commit -m "feat: 新增协整与统计套利（配对交易）概念页"
```

---

### Task 9: 新增 Black-Litterman 模型

**Files:**
- Create: `5.Finance/04-金融理论/Black-Litterman 模型.md`

**内容范围:** MVO 的痛点（输入敏感）→ BL 如何融合市场均衡收益 + 投资者主观观点 → 公式推导直觉 → 与 MVO 对比

**Step 1: 创建笔记**

```markdown
---
title: Black-Litterman 模型
type: concept
created: 2026-06-04
tags: [投资组合, 资产配置, Black-Litterman, 贝叶斯, MVO]
---

# Black-Litterman 模型

## 一句话

Black-Litterman 解决了 MVO 最头疼的问题：**预期收益估计不准导致极端权重**。它用贝叶斯方法，把"市场均衡收益"（先验）和"你的主观观点"（似然）融合在一起，输出更稳健的预期收益估计。

## 为什么 MVO 不够用

MVO 对输入极端敏感：
- 预期收益 $\mu$ 差 1% → 权重可能从 10% 跳到 80%
- 分析师对某些资产有强观点（"Apple 下季度必涨"），但 MVO 无法吸收

## 核心公式

BL 模型的**后验预期收益**：

$$\hat{\mu}_{BL} = [(\tau\Sigma)^{-1} + P'\Omega^{-1}P]^{-1} [(\tau\Sigma)^{-1}\Pi + P'\Omega^{-1}Q]$$

直觉拆解：
- $\Pi$：市场隐含的均衡收益（先验，"没有观点时的最佳猜测"）
- $Q$：你的主观观点（"我认为 Apple 会跑赢大盘 5%"）
- 结果 $\hat{\mu}_{BL}$：两者按置信度加权融合

## 四步流程

1. **计算均衡收益** $\Pi = \lambda \Sigma w_{mkt}$（逆优化：从市值权重反推）
2. **表达主观观点**：$P$（选择矩阵）+ $Q$（观点向量）+ $\Omega$（观点置信度）
3. **贝叶斯融合**：用上述公式算后验 $\hat{\mu}_{BL}$
4. **MVO 优化**：把 $\hat{\mu}_{BL}$ 和 $\Sigma$ 喂入标准 MVO

## vs MVO 对比

| | MVO | Black-Litterman |
|:---|:---|:---|
| 输入 | 自己估计 $\mu$ | 市场均衡 + 你的观点 |
| 极端权重 | 常见 | 大幅减少 |
| 观点表达 | 无法 | 可以表达"相对强弱" |
| 数学基础 | 优化 | 贝叶斯 + 优化 |

## 相关笔记

- [[马科维茨均值方差模型]] — BL 的前置和输出端
- [[CAPM - Capital Asset Pricing Model]] — 均衡收益 $\Pi$ 的理论基础
```

**Step 2: Commit**

```bash
git add 5.Finance/04-金融理论/Black-Litterman\ 模型.md
git commit -m "feat: 新增 Black-Litterman 模型概念页"
```

---

## 总览

| Phase | Task | 类型 | 预计时间 | CR |
|:---|:---|:---|:---|:---|
| 1 | 1. 修复 Chapter 1 公式 | 修复 | 15min | ⚠️ 需审核 KaTeX |
| 1 | 2. 修复 Cheatsheet 公式 | 修复 | 20min | ⚠️ 需审核 KaTeX |
| 1 | 3. 删除 7 个重复文件 | 删除 | 5min | ✅ |
| 1 | 4. 更新 index.md | 重建 | 10min | ✅ |
| 1 | 5. 清理空壳文件 | 删除 | 5min | ✅ |
| 2 | 6. Black-Scholes + Greeks | 新增 | 25min | ⚠️ 需审核内容 |
| 2 | 7. 市场微观结构 | 新增 | 20min | ⚠️ 需审核内容 |
| 2 | 8. 协整与配对交易 | 新增 | 20min | ⚠️ 需审核内容 |
| 2 | 9. Black-Litterman | 新增 | 15min | ⚠️ 需审核内容 |

**总计**: Phase 1 约 55 分钟，Phase 2 约 80 分钟。