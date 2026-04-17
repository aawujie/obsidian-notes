# chassis 模块

#HIL #chassis #CAN #simulation

> 底盘 CAN/FlexRay 仿真器，通过 PCIe-ZLG CAN 卡与真实底盘 ECU 通信。

## 分层设计

```
simulator/     ← 车辆仿真器核心（入口 + 多车型工厂）
  ├── entry/   ← SimulatorEntry 统一入口
  ├── gl/      ← 吉利车型仿真器
  ├── gwm/     ← 长城车型仿真器
  └── lp/      ← 力帆车型仿真器

strategy/      ← 信号处理策略链
  ├── core/    ← StrategyBase / StrategyChain / StrategyFactory
  └── strategies/  ← CRC8/RollingCounter/Timestamp 等具体策略

devices/       ← 硬件驱动
  └── pcie_zlg/    ← PCIe-ZLG CAN 卡

data_pool/     ← 消息池
  ├── can_message_pool     ← CAN 消息池
  └── flexray_message_pool ← FlexRay 消息池

channel/       ← 周期性通道管理
processor/     ← RX/TX 处理器
services/      ← 收发周期服务、定时服务
interfaces/    ← DBC/设备/策略接口定义
common/        ← DBC 工厂、文件管理、错误监控等
tools/         ← 辅助工具（帧发送器、CCP Flash、时间同步）
vehicle/       ← 车辆参数定义
```

## SimulatorEntry

统一入口，提供两种启动方式：

1. `Create()` + `Start()` 分步启动
2. `StartAll()` 一步到位

通过 `vehicle_type` 字符串选择车型工厂创建对应仿真器。

## 信号策略（Strategy Pattern）

| 策略 | 用途 |
|---|---|
| `CRC8BaseStrategy` | CRC8 基础校验 |
| `CRC8PayloadStrategy` | CRC8 载荷校验 |
| `CRC8_9ByteStrategy` | 9 字节 CRC8 |
| `CRC8_33ByteStrategy` | 33 字节 CRC8 |
| `RollingCounterStrategy` | 滚动计数器 |
| `BlockCounterStrategy` | 块计数器 |
| `TimestampUnixMsStrategy` | Unix 毫秒时间戳 |
| `TimestampDatetimeStrategy` | 日期时间戳 |
| `GwmVinStrategy` | 长城 VIN 码策略 |

策略通过 `StrategyChainImpl` 链式组合，由 `StrategyFactory` 根据车型配置创建。

## 多车型仿真器

每个车型仿真器包含：
- `*_vehicle_simulator`: 车辆仿真器实现
- `*_channel_manager`: CAN 通道管理器
- `*_mapping`: 信号映射表
- `*_simulator_factory`: 工厂类
