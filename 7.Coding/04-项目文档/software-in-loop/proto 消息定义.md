# proto 消息定义

#HIL #protobuf #protocol

> Protobuf 消息定义，用于各模块间通信。

## 文件列表

| Proto 文件 | 用途 |
|---|---|
| `carplus.proto` | CAN 信号、E2E 校验、握手、控制信号 |
| `signal_inject.proto` | 信号注入协议 |
| `vehicle_control_d2d.proto` | D2D 车辆控制 |
| `lidar_fault.proto` | LiDAR 故障注入 |
| `radar_fault.proto` | Radar 故障注入 |
| `imu_fault.proto` | IMU 故障注入 |

## carplus.proto 消息结构

```protobuf
CarplusSignals
├── timestamp
└── oneof
    ├── CanSignals       — CAN 信号列表（name/value/editable）
    ├── E2eSignal        — E2E 校验配置（sig/e2e/secoc/cycle）
    ├── CtrlSignal       — 控制信号（throttle/brake/gear 等）
    └── ShakeHandsSignal — 握手信号列表
```

### CtrlSignal 档位定义

- NONE / PARK / REVERSE / NEUTRAL / DRIVE
