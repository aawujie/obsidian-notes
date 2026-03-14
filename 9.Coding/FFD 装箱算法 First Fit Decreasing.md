# FFD 装箱算法 First Fit Decreasing

> 经典的装箱问题（Bin Packing Problem）近似算法，贪心策略 + 排序优化

**复杂度**：O(n log n)  
**近似比**：≤ 11/9 · OPT + 1  
**类型**：离线近似算法

---

## 问题定义

### 装箱问题（Bin Packing Problem）

**输入**：
- n 个物品，每个物品有重量 $w_i$
- 箱子容量为 $C$（所有箱子相同）

**目标**：
- 使用**最少数量的箱子**装下所有物品
- 每个箱子内物品总重量 ≤ C

**约束**：
- 物品不可分割
- 每个物品必须放入恰好一个箱子

---

## FFD 算法核心思想

```
FFD = 排序（降序） + 首次适配（First Fit）
```

### 两步策略

1. **排序阶段**：将所有物品按重量**从大到小排序**
2. **放置阶段**：依次处理每个物品，放入**第一个能容纳它的箱子**

### 为什么先排序？

> 大物品优先放置，避免小物品填满箱子后大物品无处可放

---

## 算法流程

### 伪代码

```python
def FFD(items, capacity):
    # 步骤 1：降序排序
    items = sort(items, reverse=True)
    
    # 步骤 2：初始化箱子列表
    bins = []
    
    # 步骤 3：依次放置每个物品
    for item in items:
        placed = False
        
        # 尝试放入现有箱子
        for bin in bins:
            if bin.remaining_capacity >= item:
                bin.add(item)
                placed = True
                break
        
        # 没有合适箱子，开新箱子
        if not placed:
            new_bin = Bin(capacity)
            new_bin.add(item)
            bins.append(new_bin)
    
    return bins
```

### 流程图

```
物品列表 → 降序排序 → 遍历每个物品
                           ↓
                    能否放入现有箱子？
                           ↓
           ┌───────────────┴───────────────┐
           ↓ 是                            ↓ 否
    放入第一个能容纳的箱子          创建新箱子
           ↓                            ↓
           └────────────┬───────────────┘
                        ↓
                   所有物品处理完毕？
                        ↓
           ┌────────────┴────────────┐
           ↓ 否                      ↓ 是
         继续处理                   返回箱子列表
```

---

## 实例演示

### 输入数据

| 物品 | A | B | C | D | E | F |
| --- | --- | --- | --- | --- | --- | --- |
| 重量 | 5 | 3 | 4 | 2 | 6 | 3 |
| 箱子容量 | **8** | | | | | |

### 执行过程

**步骤 1：降序排序**
```
排序后：E(6) → A(5) → C(4) → B(3) → F(3) → D(2)
```

**步骤 2：依次放置**

| 步骤 | 物品 | 箱子 1 | 箱子 2 | 箱子 3 |
| --- | --- | --- | --- | --- |
| 1 | E(6) | [6] | - | - |
| 2 | A(5) | [6] | [5] | - |
| 3 | C(4) | [6] | [5] | - |
| 4 | B(3) | [6] | [5, 3] | - |
| 5 | F(3) | [6] | [5, 3] | [3] |
| 6 | D(2) | [6, 2] | [5, 3] | [3] |

**结果**：3 个箱子
- 箱子 1：E(6) + D(2) = 8 ✅
- 箱子 2：A(5) + B(3) = 8 ✅
- 箱子 3：F(3) = 3

---

## 算法分析

### 时间复杂度

| 阶段 | 复杂度 | 说明 |
| --- | --- | --- |
| 排序 | O(n log n) | 快速排序/归并排序 |
| 放置 | O(n · m) | m 为最终箱子数，最坏 O(n²) |
| **总计** | **O(n log n)** | 排序占主导 |

### 空间复杂度

- **O(n)**：存储箱子列表和物品

### 近似比（Approximation Ratio）

```
FFD(I) ≤ 11/9 · OPT(I) + 1
```

- OPT(I)：最优解的箱子数
- 即 FFD 使用的箱子数不超过最优解的 11/9 倍 + 1

> 💡 这是装箱问题中**最好的多项式时间近似算法**之一

---

## 变体对比

### First Fit (FF) vs First Fit Decreasing (FFD)

| 特性 | FF | FFD |
| --- | --- | --- |
| 排序 | ❌ 无 | ✅ 降序 |
| 时间复杂度 | O(n²) | O(n log n) |
| 近似比 | ≤ 1.7 · OPT | ≤ 11/9 · OPT + 1 |
| 性能 | 较差 | 更好 |

### 其他近似算法

| 算法 | 策略 | 近似比 |
| --- | --- | --- |
| **FFD** | 降序 + 首次适配 | 11/9 · OPT + 1 |
| **BFD** (Best Fit Decreasing) | 降序 + 最佳适配 | 11/9 · OPT + 1 |
| **NFD** (Next Fit Decreasing) | 降序 + 下一适配 | 2 · OPT |
| **NF** (Next Fit) | 无排序 + 下一适配 | 2 · OPT |

---

## 代码实现

### Python 实现

```python
from typing import List, Tuple

class Bin:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items = []
        self.remaining = capacity
    
    def can_fit(self, item: int) -> bool:
        return item <= self.remaining
    
    def add(self, item: int):
        self.items.append(item)
        self.remaining -= item
    
    def __repr__(self):
        return f"Bin({self.items}, remaining={self.remaining})"


def first_fit_decreasing(items: List[int], capacity: int) -> List[Bin]:
    """FFD 装箱算法"""
    # 降序排序
    sorted_items = sorted(items, reverse=True)
    
    bins = []
    
    for item in sorted_items:
        placed = False
        
        # 尝试放入第一个能容纳的箱子
        for bin in bins:
            if bin.can_fit(item):
                bin.add(item)
                placed = True
                break
        
        # 开新箱子
        if not placed:
            new_bin = Bin(capacity)
            new_bin.add(item)
            bins.append(new_bin)
    
    return bins


# 使用示例
items = [5, 3, 4, 2, 6, 3]
capacity = 8
bins = first_fit_decreasing(items, capacity)

print(f"使用箱子数：{len(bins)}")
for i, bin in enumerate(bins, 1):
    print(f"箱子{i}: {bin}")
```

### 输出优化版本（带详细信息）

```python
def ffd_with_stats(items: List[int], capacity: int):
    bins = first_fit_decreasing(items, capacity)
    
    total_used = sum(capacity - b.remaining for b in bins)
    total_capacity = len(bins) * capacity
    utilization = total_used / total_capacity * 100
    
    print(f"物品总数：{len(items)}")
    print(f"使用箱子数：{len(bins)}")
    print(f"空间利用率：{utilization:.2f}%")
    print(f"总浪费空间：{total_capacity - total_used}")
    
    return bins
```

---

## 实际应用场景

### 📦 物流与仓储

| 场景 | 说明 |
| --- | --- |
| 包裹装箱 | 将不同尺寸包裹装入标准集装箱 |
| 货车装载 | 优化货车空间利用率 |
| 仓库货位 | 物品分配到货架/货位 |

### 💻 计算机资源分配

| 场景 | 说明 |
| --- | --- |
| 内存分配 | 进程/任务分配到内存块 |
| 磁盘存储 | 文件分配到磁盘块 |
| 云服务器 | VM 分配到物理服务器 |
| 任务调度 | 任务分配到计算节点 |

### 🎬 媒体与广告

| 场景 | 说明 |
| --- | --- |
| 广告时段 | 广告插入到固定时长时段 |
| 视频分段 | 视频切片到固定大小块 |
| 音频缓冲 | 音频流分配到缓冲区 |

---

## 优化技巧

### 1. 二分查找优化

对于大规模数据，可用二分查找加速箱子选择：

```python
import bisect

def ffd_optimized(items: List[int], capacity: int):
    sorted_items = sorted(items, reverse=True)
    
    # 维护剩余容量的有序列表
    remaining_caps = []  # 降序
    bin_items = []
    
    for item in sorted_items:
        # 二分查找第一个能容纳的箱子
        idx = bisect.bisect_left(remaining_caps, item)
        
        if idx < len(remaining_caps):
            # 找到合适箱子
            remaining_caps[idx] -= item
            bin_items[idx].append(item)
            # 重新排序保持有序
            remaining_caps.sort(reverse=True)
        else:
            # 开新箱子
            remaining_caps.append(capacity - item)
            bin_items.append([item])
    
    return bin_items
```

### 2. 多箱并行

```python
# 对于超大规模数据，可并行处理多个箱子组
# 适用于分布式系统
```

### 3. 混合策略

```python
# FFD + 局部搜索优化
# 先用 FFD 得到初始解，再用交换/移动优化
```

---

## 局限性

### ⚠️ 不是最优解

```
输入：物品 [6, 5, 4, 3, 2]，箱子容量 10

FFD 结果：
  箱子 1: [6, 4] = 10
  箱子 2: [5, 3, 2] = 10
  共 2 个箱子 ✅（此例最优）

反例：物品 [4, 4, 4, 3, 3, 2, 2, 2, 2]，箱子容量 10

FFD 结果：
  箱子 1: [4, 4, 2] = 10
  箱子 2: [4, 3, 3] = 10
  箱子 3: [2, 2, 2] = 6
  共 3 个箱子

最优解：
  箱子 1: [4, 3, 3] = 10
  箱子 2: [4, 4, 2] = 10
  箱子 3: [2, 2, 2, 2, 2] = 10（如果有 5 个 2）
```

### ⚠️ 不适合在线场景

- FFD 需要**预先知道所有物品**（离线算法）
- 在线场景需用 **Next Fit** 或 **First Fit**

---

## 相关概念

- [[装箱问题 Bin Packing Problem]]
- [[贪心算法 Greedy Algorithm]]
- [[近似算法 Approximation Algorithm]]
- [[背包问题 Knapsack Problem]]
- [[调度问题 Scheduling Problem]]
- [[动态规划 Dynamic Programming]]
- [[NP 完全问题 NP-Complete]]

---

## 扩展阅读

### 理论边界

| 结果 | 说明 |
| --- | --- |
| 最优解是 NP-hard | 不存在多项式时间精确算法（P≠NP 假设下） |
| FFD 近似比 11/9 | 1973 年由 Garey & Graham 证明 |
| 最优近似比 | 存在 APTAS（渐近多项式时间近似方案） |

### 经典论文

1. Garey, M. R., & Graham, R. L. (1973). "Bin packing with restricted item sizes"
2. Johnson, D. S. (1973). "Approximation algorithms for combinatorial problems"
3. Coffman, E. G., et al. (1997). "Bin packing approximation algorithms: A survey"

---

**Tags**: #算法 #装箱问题 #贪心算法 #近似算法 #运筹学 #计算机科学 #FFD
**Created**: 2026-03-12
**Difficulty**: ⭐⭐⭐ 中等
**Category**: 算法与数据结构
