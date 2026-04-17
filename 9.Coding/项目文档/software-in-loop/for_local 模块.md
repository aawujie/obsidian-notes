# for_local 模块

#HIL #local-control

> 本机（Linux 环境）仿真底盘与系统服务的启动、停止与状态管理。

## 关键组件

| 组件                 | 职责                                |
| ------------------ | --------------------------------- |
| `ForCarplus`       | sim_chassis 仿真进程生命周期（启动/停止/状态/日志） |
| `ForDockerCompose` | docker-compose 场景容器编排与健康检查        |
| `ForPtp4l`         | PTP 时间同步守护进程                      |
| `ForPhc2Sys`       | PHC↔SYS 时间同步服务                    |

## ForCarplus 细节

- `SetEnvironment`: 注入 `CAR_TYPE`、ZLG 设备类型等环境变量
- `Start/Stop/Running`: 基于 `ps`/锁文件/日志输出判断状态
- 内部使用三个 `shell::Client` 分别监控 carplus 进程、`ps` 输出与锁状态
- 日志路径: `/tmp/docker/sim_chassis.log`

## 依赖

- `third_party/shell/client.h`: 非交互方式启动/监控外部进程
- `utility::ArgumentManager`: 禁用模块列表、图像转换参数、密码需求等

## 典型流程

1. GUI 读取用户输入 → 初始化 `ArgumentManager`
2. 调用 `ForDockerCompose` 准备场景
3. 调用 `ForCarplus::Start` 启动仿真底盘
4. 按需启动 `ForPtp4l` / `ForPhc2Sys` 时间同步
5. 停止时逆序关闭并清理资源
