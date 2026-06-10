---
name: longhu-score
display_name: "龙虎榜量化评分"
description: 读取每日龙虎榜数据，用 panda_factor longhu 模型跑评分，输出排名和信号，记录验证结果
metadata:
  version: 1.0.0
  loop:
    frequency: daily
    trigger: after-market-close
    state_file: longhu-state.md
---

# 龙虎榜量化评分 Skill

## 功能

每日盘后拉取龙虎榜数据，用 `panda_factor/factors/longhu.py` 的 `composite_longhu_score` 模型评分，输出排名和信号等级。

## 数据来源

1. 东方财富龙虎榜 API 或证券时报龙虎榜报道
2. 个股行情数据（东方财富 push API）

## 评分模型

使用 `panda_factor/factors/longhu.py`：
- 资金流评分 × 0.4
- 技术面评分 × 0.3
- 量价评分 × 0.2
- 追高风险惩罚（减法）

信号等级：>=70 强 | >=42 中 | >=32 弱 | <32 过滤

## 执行步骤

1. 搜索当日龙虎榜数据（机构净买入/卖出排行）
2. 提取每只上榜标的的机构净买、北向净买、营业部净买等参数
3. 获取个股技术面数据（涨跌幅、RSI、量比等）
4. 调用 `composite_longhu_score()` 逐只评分
5. 按 composite_score 降序排列
6. 输出评分表到 `longhu-state.md`
7. 记录当日市场环境（指数涨跌、板块表现）

## 验证方式

次日对比预测信号与实际涨跌：
- 中信号票当日表现
- 弱信号/过滤票当日表现
- 计算准确率，记录到 state file

## 注意事项

- 龙虎榜数据盘后 16:30-17:00 公布
- 技术面数据需要实时行情 API
- 模型不是预测工具，是评分筛选工具
- 历史准确率参考：机构净买次日上涨概率 ~46%