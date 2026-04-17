# Weights & Biases (W&B) - 机器学习实验跟踪平台

> **W&B** 是机器学习领域最流行的实验跟踪、可视化和协作平台。

---

## 核心功能

| 功能 | 说明 |
|------|------|
| **实验跟踪** | 记录训练指标（loss、accuracy、学习率等） |
| **超参数调优** | Sweeps 支持网格搜索、随机搜索、贝叶斯优化 |
| **模型版本管理** | Artifacts 保存和对比不同 checkpoint |
| **可视化** | 实时图表、embedding 投影、模型结构图 |
| **团队协作** | 共享实验、评论、生成报告 |

---

## 快速开始

### 1. 安装

```bash
pip install wandb
```

### 2. 登录

```bash
wandb login
# 输入 API key（从 https://wandb.ai/authorize 获取）
```

### 3. 基础使用

```python
import wandb
import random

# 初始化项目
wandb.init(
    project="my-project",
    name="experiment-1",
    config={
        "learning_rate": 0.001,
        "epochs": 100,
        "batch_size": 32
    }
)

# 模拟训练
for epoch in range(100):
    loss = random.random() * (1 - epoch/100)
    accuracy = epoch / 100
    
    # 记录指标
    wandb.log({
        "loss": loss,
        "accuracy": accuracy,
        "epoch": epoch
    })

# 结束运行
wandb.finish()
```

---

## 工作原理

```
训练代码 → wandb.log() → 本地缓存 → 异步上传 → 云端仪表盘
                ↓
           WebSocket 持久连接
                ↓
           实时更新网页图表
```

**关键机制：**
- **本地缓存**：数据先写本地文件，不阻塞训练
- **异步上传**：后台线程批量发送到云端
- **增量同步**：只传变化的数据
- **自动聚合**：多次 log() 合并，减少网络请求

---

## 与 TensorBoard 对比

| 特性 | TensorBoard | W&B |
|------|-------------|-----|
| 归属 | Google | Weights & Biases, Inc. |
| 部署 | 本地 | 云端为主 |
| 协作 | 弱 | **强** |
| 超参搜索 | HParams | **Sweeps（更强）** |
| 模型管理 | 简单 | **Artifacts（版本控制）** |
| 成本 | 免费 | 免费额度 + 付费 |

**选择建议：**
- 个人小项目 → TensorBoard
- 团队协作/企业 → W&B

---

## 定价

| 版本             | 价格      | 限制              |
| -------------- | ------- | --------------- |
| **Free**       | $0      | 100 GB 存储，1 人团队 |
| **Teams**      | $50/人/月 | 100 GB，无限成员     |
| **Enterprise** | 定制      | 更多存储、SSO、私有部署   |

**免费版包含：**
- 无限实验和运行次数
- 公开项目无限
- 私有项目 1 个

---

## 高级功能

### 超参数搜索 (Sweeps)

```python
sweep_config = {
    "method": "random",
    "metric": {"name": "loss", "goal": "minimize"},
    "parameters": {
        "lr": {"min": 0.0001, "max": 0.1},
        "batch_size": {"values": [16, 32, 64]}
    }
}

sweep_id = wandb.sweep(sweep_config, project="my-project")
wandb.agent(sweep_id, function=train, count=10)
```

### 保存模型 (Artifacts)

```python
# 保存模型
artifact = wandb.Artifact("model", type="model")
artifact.add_file("model.pth")
wandb.log_artifact(artifact)

# 加载历史版本
artifact = wandb.use_artifact("my-project/model:v2")
artifact.download()
```

### 自动记录系统指标

```python
wandb.init(
    project="my-project",
    settings=wandb.Settings(
        _stats_sample_rate_seconds=2,  # 系统指标采样频率
        _stats_samples_to_average=15
    )
)
# 自动记录：CPU/GPU 利用率、显存占用、网络 IO 等
```

---

## 最佳实践

1. **组织项目结构**
   ```
   project/
   ├── experiment-1/
   ├── experiment-2/
   └── baselines/
   ```

2. **使用有意义的运行名称**
   ```python
   wandb.init(name=f"lr-{lr}-bs-{batch_size}")
   ```

3. **定期清理旧实验**（节省存储）

4. **本地调试时禁用**
   ```python
   wandb.init(mode="disabled")  # 不上传任何数据
   ```

---

## 相关链接

- 官网：https://wandb.ai/site
- 文档：https://docs.wandb.ai/
- GitHub：https://github.com/wandb/wandb

---

## 标签

#ML #深度学习 #实验跟踪 #可视化 #工具 #Python

---

*创建时间：2026-04-11*
