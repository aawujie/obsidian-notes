# server 模块

#HIL #simulation #sensor

> 传感器仿真服务，模拟各类车载传感器向域控发送数据。

## 仿真服务列表

| 服务            | 协议      | 用途                                |
| ------------- | ------- | --------------------------------- |
| `sim-lidar`   | UDP/TCP | 模拟多型号 LiDAR（AT128/ATX/EMX192/MX）  |
| `sim-radar`   | UDP     | 模拟 4D 毫米波雷达                       |
| `sim-pbox`    | SOME/IP | 模拟 PBox（IMU/GNSS 组合导航盒），含 NMEA 协议 |
| `sim-uss`     | -       | 模拟超声波传感器                          |
| `sim-relayer` | ZMQ     | 视频流中继（FFmpeg H264 / NVENC 编码）     |
| `joystick`    | evdev   | G29 方向盘硬件控制                       |

## sim-lidar 架构

`SimLidarServer` 基类 → 车型/型号特定实现：

- `at128/`: AT128 激光雷达（UDP 点云 + TCP 控制）
- `atx/`: ATX 激光雷达
- `emx192/`: EMX192 激光雷达
- `mx/`: MX 激光雷达

核心流程：订阅 ROS PointCloud2 Topic → 转换为厂商私有协议 → UDP 发送到域控

## sim-pbox 架构

`SimPboxServerBase` 基类 → 车型特定实现：

- `c01/`: C01 车型（含 SOME/IP fidl-gen 代码、NMEA 协议 GPGGA/GPRMC/GPGST）
- `p03/`: P03 车型

## sim-radar

- `SimRadarServer`: 基础雷达仿真
- `SimRadar4dUdp`: 4D 雷达 UDP 数据仿真

## sim-relayer

- `ZmqRelayer`: ZMQ 消息中继
- `FfmpegH264Transcoder`: FFmpeg H264 软编码
- `NvencEncoderPool`: NVIDIA 硬件编码池

## joystick

G29 方向盘控制适配，支持多车型：
- `g29_control_geely.cc` — 吉利
- `g29_control_gwm.cc` — 长城
- `g29_control_lp.cc` — 力帆
- `g29_control_smart.cc` — Smart
