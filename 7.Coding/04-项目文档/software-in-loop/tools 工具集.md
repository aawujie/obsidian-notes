# tools 工具集

#HIL #python #tools

> Python 工具集，用于底盘控制、FOTA 刷写、驱动配置等。

## 目录结构

### carplus/ — 底盘控制

各车型底盘 Python 控制实现：

| 文件 | 车型 |
|---|---|
| `c01_chassis.py` | C01 |
| `c01t_chassis.py` | C01T |
| `de09_chassis.py` | DE09 |
| `hy11_chassis.py` | HY11 |
| `hy11p_chassis.py` | HY11P |
| `p03_chassis.py` | P03 |
| `p177_chassis.py` | P177 |
| `sim_chassis.py` | 仿真底盘 |
| `car_plus.py` | 基类 |
| `pid_controller.py` | PID 控制器 |
| `main.py` | 入口 |

### fota/ — 远程固件升级

- `get_latest_fotatools.py`: 获取最新 FOTA 工具
- `get_update_file.py`: 获取升级文件
- `remotecline.py`: 远程命令行
- `other_tools.py`: 辅助工具

### driver/ — 驱动配置

- `car_config.py`: 车型配置管理
- `orin_setup.py`: Orin 域控初始化
- `update_driver_config.py`: 更新驱动配置
- `update_sensor_config.py`: 更新传感器配置
- `event_update.py`: 事件更新

### common/ — 公共工具

- `dr_common.py`: 通用工具函数
- `dr_logging.py`: 日志配置
- `dr_ssh_client.py`: SSH 客户端封装

### serial_logger/ (C++)

- 串口日志采集器

### tool/ — 辅助工具

- `vlan_configure.py`: VLAN 网络配置
- `vpm_map_downloader.py`: VPM 地图下载器
