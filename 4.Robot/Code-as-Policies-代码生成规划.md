---
title: Code-as-Policies-代码生成规划
type: paper-note
created: 2026-06-01
tags: [embodied-ai, paper-note, llm-planning, code-generation, robot]
---

## 论文信息
- **标题**: Code as Policies: Language Model Programs for Embodied Control
- **作者/机构**: Jacky Liang, Wenlong Huang, Fei Xia, Peng Xu, Karol Hausman, Brian Ichter, Pete Florence, Andy Zeng — Robotics at Google
- **发表时间**: 2022 (arXiv:2209.07753, v3: Feb 2023)
- **arXiv/链接**: https://arxiv.org/abs/2209.07753
- **发表会议**: ICRA 2023
- **项目页面**: https://code-as-policies.github.io/

## 核心问题
SayCan 和 Inner Monologue 都将 LLM 用于选择预定义的技能，这限制了系统的灵活性和泛化能力。当遇到新任务时，需要重新训练技能或修改代码。**Code as Policies (CaP) 要解决的核心问题是：能否让 LLM 直接生成可执行的机器人代码（Python 程序），而不是从固定的技能库中选择，从而实现对新任务和新组合的零样本泛化？**

## 关键方法

1. **LLM 直接生成 Python 代码**
   不是让 LLM 输出文本指令或技能选择，而是直接生成完整的 Python 函数。这些函数调用感知 API（如 `get_object_bbox()`, `detect_objects()`）和动作 API（如 `pick()`, `place()`, `move_to()`），构成分层、有状态、可组合的策略。

2. **分层代码生成 (Hierarchical Code Generation)**
   - LLM 首先生成高层任务函数（如 `def clean_table()`）
   - 高层函数调用中层函数（如 `def sort_objects_by_color()`）
   - 中层函数调用底层原语（如 `pick_and_place(obj, target)`）
   - 这种递归分解让代码可以处理复杂的长序列任务

3. **感知 API 的语义集成**
   LLM 理解感知 API 的语义，可以在代码中使用它们进行推理。例如：
   ```python
   objects = detect_objects()
   red_objects = [obj for obj in objects if obj.color == 'red']
   leftmost = min(red_objects, key=lambda o: o.position.x)
   pick(leftmost)
   ```
   LLM 能够自然地组合感知结果和逻辑判断。

4. **代码组合与重用**
   已生成的代码函数可以被后续任务引用和复用，形成逐步增长的代码库。LLM 还能通过组合已有的函数来生成新任务的代码。

5. **自纠错与注释**
   生成的代码带有自然语言注释，可读性强。如果执行出错，LLM 可以读取错误信息并重新生成修正后的代码。

## 重要细节

- **实验平台**: 真实机器人操作平台（桌面操作场景）
- **任务类型**: 物体排序、按颜色/形状分类、空间关系推理（"把左边的物体放到右边"）、多步操作链
- **零样本泛化**: 不需要额外训练，LLM 可以直接为从未见过的任务组合生成代码
- **空间推理**: LLM 能通过代码表达空间关系（如 `left_of`, `above`, `between`），这是它相比其他方法的一个重要优势
- **与 SayCan/Inner Monologue 的关系**: CaP 可以看作是用代码生成替代了技能选择，提供了更强的表达能力和泛化能力
- **局限性**: 代码质量依赖于 LLM 的能力；生成的代码可能有 bug；感知 API 的准确性直接影响任务成功率；复杂物理交互（如接触力控制）难以用代码表达
- **引用量**: 500+ (截至 2025 年初)

## 与面试50题的关系
- **Q10**: LLM/VLM 在机器人规划中的应用 — CaP 是 LLM 用于机器人规划的第三种范式（代码生成），超越了 SayCan 的技能选择和 Inner Monologue 的文本规划
- **Q18**: 具身智能中的代码生成 — CaP 是该方向的代表性工作

## 个人思考