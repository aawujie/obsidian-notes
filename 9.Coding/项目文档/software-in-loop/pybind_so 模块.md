# pybind_so 模块

#HIL #python #pybind11

> PyBind11 封装层，将 C++ 核心能力导出为 Python 模块，支持自动化测试。

## 导出的 Python 模块

| 模块                        | 用途                    |
| ------------------------- | --------------------- |
| `dr_hil_autotest`         | 自动化测试绑定               |
| `dr_hil_service`          | HIL 服务绑定              |
| `dr_hil_someip`           | SOME/IP 通信绑定          |
| `chassis_simulator_entry` | 底盘仿真器 Python 入口       |
| `dr_common`               | 公共工具（SSHFS Mounter 等） |

## 核心类

| 文件 | 类/功能 |
|---|---|
| `dr_ego_controller` | 自车控制器 |
| `dr_hil_powerctl` | 电源控制 |
| `dr_hil_socket` | Socket 通信 |
| `dr_node` | ROS 节点封装 |
| `dr_sim_map` | 仿真地图 |
| `dr_msg_translator` | 消息翻译器 |
| `dr_websocket_client` | WebSocket 客户端 |

## 服务层 (service/)

| 文件 | 用途 |
|---|---|
| `dr_orin_warpper` | Orin 域控包装器 |
| `dr_local_wrapper` | 本地服务包装器 |
| `dr_lidar_manager` | LiDAR 管理器 |
| `dr_carplus_entry` | Carplus 入口 |

## 车型 HUT 测试

- `gwm-hut/`: 长城车型 Human-machine Unit Tester（SOME/IP FIDL）
- `yinhe_hut/`: 银河车型 HUT

## NPC 控制 (emulator/)

- `dr_npc_control`: NPC（非玩家车辆）控制接口
