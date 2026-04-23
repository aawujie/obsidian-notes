# Chassis / CAN / ZLG 底盘仿真系统 — 深度架构分析

> 基于 `software_in_loop/src/chassis/` 代码库逆向分析
> 分析日期: 2026-04-23

---

## 目录

- [[#一、系统总览与核心设计思想]]
- [[#二、分层架构逆向分析]]
- [[#三、关键模块设计决策推演]]
- [[#四、编码细节深度解析]]
- [[#五、数据流完整路径]]
- [[#六、多车型适配机制]]
- [[#七、Troubleshooting 问题排查手册]]
- [[#八、已知设计权衡与潜在改进]]

---

## 一、系统总览与核心设计思想

### 1.1 系统定位

这是一个 **HIL (Hardware-in-the-Loop) 底盘仿真系统**，核心职责是：
- 模拟真实 ECU 在 CAN/CANFD 总线上的行为
- 周期性发送符合 DBC 规范的 CAN 报文
- 接收域控制器下发的控制命令并转发到动力学模型
- 支持 E2E (End-to-End) 校验、SECOC、Rolling Counter 等汽车安全机制

### 1.2 作者核心设计哲学推测

通过代码结构逆向推测，原作者遵循以下设计原则：

1. **接口隔离 + 依赖倒转**：`DeviceInterface` / `DbcCoder` / `ChannelStrategyChain` 三个核心接口将硬件、编解码、策略三个关注点彻底解耦
2. **组合优于继承**：`PeriodChannel` 通过组合 `TxProcessor` + `RxProcessor` + `TimerService` + `StrategyChain` 实现功能，而非继承
3. **单一职责**：每个类只做一件事——`CanChannel` 只管 Socket 读写、`CanFrame` 只管帧格式转换、`PcieCanManager` 只管生命周期
4. **车型无关的核心 + 车型相关的工厂**：核心通道逻辑 (`PeriodChannel`) 与车型 (`GwmSimulatorFactory`, `GlSimulatorFactory`, `LpSimulatorFactory`) 完全分离

### 1.3 技术栈

| 维度 | 选型 |
|------|------|
| 构建系统 | Bazel |
| CAN 通信 | Linux SocketCAN (非 ZLG 私有 API) |
| CAN 硬件 | ZLG PCIe CANFD 卡 (内核驱动 `zpcicanfd`) |
| 序列化 | nlohmann/json, protobuf |
| 日志 | glog + spdlog |
| Python 绑定 | pybind11 |
| GUI | Qt (QPushButton 子类) |
| 中间件 | Church (类 ROS 的 pub/sub) |

---

## 二、分层架构逆向分析

### 2.1 六层架构

```
┌─────────────────────────────────────────────────────┐
│  Layer 6: Entry / Python Binding / GUI              │
│  SimulatorEntry, PySimulator, SimChassisWrapper      │
├─────────────────────────────────────────────────────┤
│  Layer 5: Vehicle Simulator (车型层)                  │
│  GwmVehicleSimulator, GlVehicleSimulator, ...        │
│  ├── Handshake (握手)                                │
│  ├── WakeUp (唤醒: VIN / NM)                         │
│  └── ModelBridge (动力学桥接)                          │
├─────────────────────────────────────────────────────┤
│  Layer 4: Channel Manager                           │
│  BaseChannelManager → GwmChannelManager / ...        │
│  管理多个 PeriodChannel 的生命周期                      │
├─────────────────────────────────────────────────────┤
│  Layer 3: Period Channel (核心)                       │
│  PeriodChannel                                       │
│  ├── TimerService (定时调度)                           │
│  ├── TxProcessor (发送处理流水线)                       │
│  │   └── PreSend → DBC Encode → PostSend → Device    │
│  ├── RxProcessor (接收处理)                            │
│  │   └── Device → DBC Decode → MessagePool            │
│  ├── CanMessagePool (报文池 / 数据中心)                 │
│  └── StrategyChainImpl (策略链)                        │
├─────────────────────────────────────────────────────┤
│  Layer 2: Abstraction (抽象层)                        │
│  DeviceInterface, DbcCoder, ChannelStrategyChain     │
│  BaseMessagePool, MessageData, CanFrame              │
├─────────────────────────────────────────────────────┤
│  Layer 1: Hardware / OS (硬件层)                      │
│  CanChannel (SocketCAN), PcieCanManager (单例)        │
│  Kernel Driver: zpcicanfd (xpcfd.c)                  │
└─────────────────────────────────────────────────────┘
```

### 2.2 依赖方向

**严格自顶向下**，Layer 3 (PeriodChannel) 只依赖 Layer 2 的接口，不直接引用 Layer 1 的 `CanChannel`。这使得：
- 可以用 mock 设备替换真实 CAN 卡进行单元测试
- 理论上可以支持 FlexRay / 以太网等不同总线（已有 `FlexRayMessagePool` 占位）

---

## 三、关键模块设计决策推演

### 3.1 为什么用 SocketCAN 而非 ZLG 私有 API？

**推测原因：**

1. **可移植性**：SocketCAN 是 Linux 内核标准接口，任何 CAN 卡只要有内核驱动都能用
2. **工具链兼容**：`candump`, `cansend`, `ip link set` 等标准工具直接可用，方便调试
3. **多进程共享**：SocketCAN 天然支持多进程同时读写同一个 CAN 接口
4. **ZLG 特殊处理已在内核驱动层完成**：`xpcfd.c` 将 ZLG PCIe 硬件注册为标准 SocketCAN `netdev`，上层无感知

**代价：**
- 需要维护自己的内核驱动模块
- 内核驱动与内核版本强绑定（代码中已做 `KERNEL_VERSION(5,15,0)` 兼容）

### 3.2 为什么 CanFrame 构造后不可变（ID/DLC）？

```cpp
// 私有修改器方法，仅供内部使用
void SetId(uint32_t id) { id_ = id; }
void SetDlc(uint8_t dlc) { dlc_ = dlc; }
```

**推测原因：**
- CAN 帧的 ID 和 DLC 在物理层面是帧的"身份"，修改它们等于创建新帧
- 只允许修改 `data_` 内容（通过 `SetData()`），这是安全设计——防止意外篡改帧路由
- `FromSocketCan()` 是唯一的"完整构造"路径，用于从内核数据创建对象

### 3.3 PcieCanManager 为什么是单例？

```cpp
static PcieCanManager& GetInstance();
```

**推测原因：**
- 物理 CAN 接口是全局唯一资源，`can0` 只能有一个 socket 绑定
- 单例保证整个进程只有一份通道映射
- 通过 `std::shared_ptr<CanChannel>` 分发，允许多个 PeriodChannel 共享同一物理通道（虽然当前设计是 1:1）

### 3.4 策略链为什么分 Pre/Post 两个阶段？

```
PreSend (编码前): Rolling Counter → Timestamp → Block Counter
    ↓
DBC Encode: 信号值 → 字节数组
    ↓
PostSend (编码后): CRC8 → SECOC → VIN
```

**推测原因：**
- **Rolling Counter** 是信号级操作（操作报文池中的信号值 → 需要在编码前执行）
- **CRC8/Checksum** 是字节级操作（需要对编码后的完整字节数组计算 → 必须在编码后执行）
- 这是汽车行业 E2E 保护的标准处理流程，作者严格遵循了这个顺序

### 3.5 为什么 SendFrame 里有硬编码的帧 ID？

```cpp
bool use_canfd = (data.size() != 8) || (message_id == 0x5c1 || message_id == 0x295);
```

**推测原因：**
- `0x5c1` 和 `0x295` 是特定车型中始终需要用 CANFD 格式发送的帧
- 尽管数据长度是 8 字节（普通 CAN 也能发），但这些帧在真实 ECU 上必须以 CANFD 格式发送
- **这是一个已知的技术债**——正确做法应该通过 DBC 或配置文件声明帧类型

### 3.6 锁文件机制 (`/tmp/chassis_simulator.lock`)

```cpp
current_lock_manager_->SetPath("/tmp/chassis_simulator.lock");
if (!current_lock_manager_->TryAcquire()) { ... }
```

**推测原因：**
- 防止多个 simulator 实例同时操作同一组 CAN 通道
- CAN 总线上两个模拟器同时发送会导致总线冲突 (Bus-off)
- `StartWatch()` 在锁文件被外部删除时自动停止模拟器——这是远程"紧急停车"机制

### 3.7 共享内存日志 (SharedStringBuffer)

```cpp
void EnableShmLogger(const std::string& shm_name, ...);
```

**推测原因：**
- CAN 数据需要实时可观测，但不能因为日志 I/O 影响发送周期精度
- 共享内存写入几乎零延迟，外部进程可以 mmap 读取（如 GUI 的报文监控面板）
- 环形缓冲区设计，8MB 容量自动覆盖旧数据

---

## 四、编码细节深度解析

### 4.1 CanFrame 的 SocketCAN 转换

```cpp
CanFrame CanFrame::FromSocketCan(const struct canfd_frame& frame) {
    can_frame.SetId(frame.can_id & CAN_EFF_MASK);        // 提取纯 ID
    can_frame.SetExtended(!!(frame.can_id & CAN_EFF_FLAG)); // 扩展帧标志在 ID 的高位
    can_frame.SetRemote(!!(frame.can_id & CAN_RTR_FLAG));   // 远程帧标志
    can_frame.SetCanfd((frame.len > CAN_MAX_DLC) || (frame.flags & CANFD_FDF));
}
```

**关键细节：**
- Linux SocketCAN 的 `can_id` 字段同时编码了帧 ID 和标志位（EFF/RTR/ERR）
- `CAN_EFF_MASK = 0x1FFFFFFF` 用于剥离标志位
- CANFD 判断有两个条件：数据长度 >8 **或** FDF 标志置位

### 4.2 非阻塞接收 + poll 机制

```cpp
// 设置 socket 为非阻塞模式
fcntl(socket_fd_, F_SETFL, flags | O_NONBLOCK);

// 接收时用 poll 检查是否有数据
int poll_result = poll(&pfd, 1, static_cast<int>(timeout_ms));
```

**设计考量：**
- 非阻塞模式允许 `ReceiveAllCanFrames()` 在无数据时立即返回
- `timeout_ms=0` 意味着纯轮询，不阻塞——适合高频周期性接收 (10ms 周期)
- 避免了线程阻塞导致的发送延迟

### 4.3 线程安全设计

```cpp
mutable std::mutex send_mutex_;     // 发送独占
mutable std::mutex receive_mutex_;  // 接收独占
mutable std::mutex stats_mutex_;    // 统计独占
```

**三把独立锁而非一把大锁：**
- 发送和接收可以并发执行（CAN 物理层本来就是全双工）
- 统计信息独立保护，避免影响核心收发路径
- `MessageData` 用 `shared_mutex`（读写锁），允许多读单写

### 4.4 TxProcessor 的四步流水线

```
Step 1: ExecutePreSendStrategies(message_id)
    → 策略链遍历所有 PreSendStrategy，更新 MessagePool 中的信号值
    → Rolling Counter 递增、Timestamp 更新

Step 2: ExecuteDbcEncoding(message_id)
    → 从 MessagePool 读取所有信号值
    → 通过 DbcCoder.EncodeMessage() 编码为字节数组

Step 3: ExecutePostSendStrategies(message_id, encoded_data)
    → 策略链遍历所有 PostSendStrategy
    → CRC8 在字节数组上计算并回写

Step 4: ExecuteDeviceSend(message_id, encoded_data)
    → 通过 DeviceInterface.SendFrame() 发送到物理总线
```

### 4.5 CRC8 策略的模板方法模式

```cpp
class Crc8BaseStrategy : public PostSendStrategy {
protected:
    virtual int GetCrcDataLength() const = 0;
    virtual uint8_t GetInitialValue() const = 0;
    virtual uint8_t ProcessFinalResult(uint8_t crc_result) const = 0;
};
```

**衍生类：**
- `Crc8PayloadStrategy` — 标准 payload CRC
- `Crc8A10PayloadStrategy` — A10 车型定制 CRC
- `Crc8_9ByteStrategy` — 9 字节变种
- `Crc8_33ByteStrategy` — 33 字节变种（CANFD 64 字节帧）

不同车型的 CRC 多项式、初始值、数据段长度各不相同，但计算流程一致——经典的模板方法模式应用。

### 4.6 Python Binding 的 Hint 格式

```python
# 格式: <dbc_name>.<frame_id>.<signal_name>
sim.set_signal_info_hint("ADAS1.0x295.Checksum_ABM1", 42.0)
```

**设计巧妙之处：**
- 一个字符串同时定位到 通道(dbc) + 帧(id) + 信号(name)
- 支持 `0x` 前缀的十六进制帧 ID
- 返回下次发送的 Unix 时间戳（毫秒），测试脚本可以据此做时序验证

---

## 五、数据流完整路径

### 5.1 发送路径 (Tx)

```
Python/GUI 设置信号值
    ↓
BaseVehicleSimulator.SetSignalValue(channel, msg_id, signal, value)
    ↓
PeriodChannel.SetSignalValue()
    ↓
CanMessagePool.SetSignalValue()  ← 线程安全写入
    ↓
[TimerService 定时触发]
    ↓
TxPeriodService → TxProcessor.ProcessMessage(msg_id)
    ↓
Step 1: PreSend策略 (RollingCounter++ / Timestamp更新)
    ↓
Step 2: DbcCoder.EncodeMessage() → bytes
    ↓
Step 3: PostSend策略 (CRC8计算 / VIN填充)
    ↓
Step 4: DeviceInterface.SendFrame(msg_id, bytes)
    ↓
CanChannel.SendCanFrame() → write(socket_fd_, canfd_frame)
    ↓
Linux SocketCAN → ZLG PCIe 内核驱动 → CAN 总线
```

### 5.2 接收路径 (Rx)

```
CAN 总线 → ZLG PCIe 驱动 → SocketCAN
    ↓
RxPeriodService [10ms周期] → RxProcessor.ProcessReceivedDataFromDevice()
    ↓
CanChannel.ReceiveAllFrames() → poll + read → CanFrame列表
    ↓
DbcCoder.DecodeMessage() → 信号值 map
    ↓
CanMessagePool.SetSignalValues() ← 更新报文池
    ↓
[ModelBridge 20ms周期读取]
    ↓
BaseModelBridgeProcessor.ConvertToControlCommand()
    ↓
DrEgoController → ROS Topic: control_command
    ↓
动力学模型
```

### 5.3 HIL Socket 桥接路径

```
HIL 上位机 (远程)
    ↓ TCP Socket
DrHilSocket 回调
    ↓
HilSocketBridge.OnData(json)     → ChannelManager → PeriodChannel.SetSignalValues()
HilSocketBridge.OnMessageState() → E2E/SECOC/RC 开关控制
HilSocketBridge.OnHandshake()    → HandshakeProcessor 握手逻辑
```

---

## 六、多车型适配机制

### 6.1 三大产品线

| 工厂类 | 品牌 | 代表车型 | 特殊机制 |
|--------|------|----------|----------|
| `GwmSimulatorFactory` | 长城 (GWM) | de09, D19 | VIN 码唤醒, 特殊握手 |
| `GlSimulatorFactory` | GL 系列 | p177 | NM 网络唤醒 |
| `LpSimulatorFactory` | LP 系列 | A10, p03 | 标准握手 |

### 6.2 车型发现机制

```cpp
// simulator_entry.cc - 按优先级尝试
auto gl_simulator = GlSimulatorFactory::CreateSimulator(vehicle_type, {});
if (gl_simulator) return gl_simulator;

auto gwm_simulator = GwmSimulatorFactory::CreateSimulator(vehicle_type, {});
if (gwm_simulator) return gwm_simulator;

auto lp_simulator = LpSimulatorFactory::CreateSimulator(vehicle_type, {});
if (lp_simulator) return lp_simulator;
```

每个工厂内部通过 `catalog` 配置文件确定支持哪些车型。

### 6.3 车型特有配置结构

```
src/chassis/vehicle/<车型>/
├── dbc/              # DBC 编解码器 C++ 实现
├── config/           # JSON 配置
│   ├── handshake_config.json     # 握手配置
│   ├── *_messages.json           # 报文定义
│   ├── *_frame_ids.json          # 帧 ID 映射
│   └── *_signal_to_canid.json    # 信号→帧ID映射
└── *.dbc             # CAN DB 源文件
```

---

## 七、Troubleshooting 问题排查手册

### 7.1 CAN 通道打不开

**症状**：日志出现 `创建socket失败` 或 `获取接口索引失败`

**排查步骤：**

```bash
# 1. 检查 CAN 接口是否存在
ip link show type can

# 2. 检查 ZLG 内核驱动是否加载
lsmod | grep zpcicanfd

# 3. 如果驱动未加载，手动安装
cd src/chassis/devices/pcie_zlg/driver/
sudo bash install_driver.sh

# 4. 检查 PCI 设备是否被识别
lspci | grep -i "9a01\|9a02\|9a04\|9a22\|0108"

# 5. 确认 CAN 接口已 UP 且配置了波特率
sudo ip link set can0 up type can bitrate 500000 dbitrate 2000000 fd on
```

**常见原因：**
- 内核版本升级后驱动需要重新编译（`xpcfd.c` 含版本兼容宏）
- ZLG PCIe 卡物理接触不良
- 未配置 CANFD 的 `dbitrate`（数据段波特率）

### 7.2 发送报文但域控收不到

**症状**：`stats_.sent_frames` 递增但域控侧无响应

**排查步骤：**

```bash
# 1. 用 candump 独立验证总线上是否有数据
candump can0

# 2. 检查是否 bus-off
ip -details link show can0 | grep "state"
# 如果显示 "state BUS-OFF"，需要重启接口
sudo ip link set can0 down && sudo ip link set can0 up

# 3. 检查共享内存日志（无需重启）
# 在运行中的进程中查看实时 CAN 数据
cat /dev/shm/chassis/*_data  # 或通过 GUI 的报文监控面板

# 4. 检查波特率是否匹配域控
ip -details link show can0 | grep "bitrate"

# 5. 检查终端电阻（物理层）
# CAN 总线两端各需要一个 120Ω 终端电阻
```

**常见原因：**
- 波特率不匹配（CANFD 有仲裁段和数据段两个波特率）
- Bus-off 状态（总线错误累积超限）
- 帧格式错误（CAN vs CANFD，标准帧 vs 扩展帧）

### 7.3 Rolling Counter / CRC 校验失败

**症状**：域控报 E2E 错误，日志中无 CRC/RC 相关错误

**排查步骤：**

```bash
# 1. 确认策略是否被加载
# 检查策略配置 JSON 中是否包含目标报文
cat src/chassis/vehicle/<车型>/config/*_messages.json | python3 -m json.tool | grep -A5 "rolling_counter"

# 2. 确认 RC/CRC 开关是否启用
# 通过 Python API 查询
sim.is_e2e_enable("ADAS1", "Checksum_ABM1")
sim.is_counter_enable("ADAS1", "RollingCounter_ABM1")

# 3. 使用 cansniffer 对比真实 ECU 和仿真器的报文
cansniffer can0 -c  # 彩色高亮变化字节

# 4. 检查 CRC 多项式是否正确
# 不同车型使用不同的 CRC8 变种
grep -r "GetInitialValue\|GetCrcDataLength" src/chassis/strategy/strategies/
```

**常见原因：**
- 策略 JSON 配置中的 `start_byte` / `high_byte` / `low_byte` 与 DBC 不匹配
- CRC 多项式与域控端不一致（使用了错误的 strategy 子类）
- Rolling Counter 的 min/max/step 配置错误

### 7.4 模拟器锁冲突

**症状**：`TryAcquire() failed`，模拟器无法启动

**排查步骤：**

```bash
# 1. 检查锁文件
cat /tmp/chassis_simulator.lock

# 2. 检查是否有残留进程
ps aux | grep chassis_simulator

# 3. 如果无残留进程，手动删除锁文件
rm /tmp/chassis_simulator.lock

# 4. 如果有残留进程，先 kill
kill -SIGTERM <pid>
# 等待 3 秒后如果还在：
kill -SIGKILL <pid>
rm /tmp/chassis_simulator.lock
```

**设计注意事项：**
- `StartWatch()` 会在锁文件被外部删除时自动 Stop 模拟器
- 这是一个**远程紧急停车**机制：运维可以通过删除锁文件来强制停止仿真

### 7.5 信号值设置不生效

**症状**：`SetSignalValue()` 返回 true 但 CAN 总线上的数据未变化

**排查步骤：**

1. **确认通道名称正确**：`sim.get_channel_names()` 查看实际通道名
2. **确认帧 ID 正确**：十六进制 vs 十进制，`0x295` vs `661`
3. **确认信号名拼写正确**：DBC 信号名大小写敏感
4. **确认发送周期不为 0**：`sim.modify_cycle_time(channel, signal, 1)` 恢复默认周期
5. **确认未被暂停**：`sim.is_sending_paused(channel)`
6. **确认未处于 chassis stopped 状态**：检查 `IsChassisStopped()`

### 7.6 动力学模型收不到 control_command

**症状**：底盘仿真运行正常但动力学模型无反应

**排查步骤：**

```bash
# 1. 检查 ROS topic 是否在发布
rostopic list | grep control_command
rostopic hz /control_command

# 2. 检查 ModelBridge 是否初始化成功
# 日志中搜索 "ModelBridgeProcessor"

# 3. 检查控车使能开关
sim.is_control_command_enabled()  # Python 接口暂无，检查日志

# 4. 检查分字段失效掩码
# 可能某个字段被标记为 disabled
```

### 7.7 内核驱动编译失败

**症状**：`make` 报错，通常是内核 API 变更导致

**排查步骤：**

```bash
# 1. 确认内核头文件已安装
apt list --installed | grep linux-headers-$(uname -r)

# 2. 如果缺少，安装
sudo apt install linux-headers-$(uname -r)

# 3. 检查 xpcfd.c 的版本兼容宏
# 代码已包含 KERNEL_VERSION(5,15,0) 的条件编译
# 如果内核版本更新，可能需要添加新的兼容分支

# 4. 检查 MODULE_LICENSE
# 必须为 "GPL"，否则某些内核符号不可用
```

### 7.8 CANFD 模式问题

**症状**：发送 CANFD 帧失败，或对端收到的数据长度不对

**排查步骤：**

```bash
# 1. 确认内核支持 CANFD
ip link set can0 up type can bitrate 500000 fd on
# 如果报错 "RTNETLINK answers: Invalid argument"，可能内核不支持 CANFD

# 2. 确认 setsockopt 成功
# 日志中搜索 "CAN-FD支持已启用"

# 3. DLC 长度对照表
# CANFD 有效 DLC: 0,1,2,3,4,5,6,7,8,12,16,20,24,32,48,64
# 不在此列表中的长度会被驱动拒绝

# 4. 确认对端 ECU 支持 CANFD
# 某些 ECU 只支持经典 CAN (最大 8 字节)
```

### 7.9 性能问题：发送周期抖动

**症状**：实际发送周期与配置周期偏差较大

**排查步骤：**

```bash
# 1. 检查系统负载
top -bn1 | head -5

# 2. 检查内核定时器精度
cat /proc/timer_list | grep "resolution"

# 3. 使用 cansniffer 观察实际时间间隔
cansniffer can0 -t a  # 显示绝对时间戳

# 4. 检查事件循环超时设置
# kEventLoopTimeoutMs = 1ms 是否足够

# 5. 检查 GC / 内存压力
# glog 的磁盘写入可能引起延迟
```

**优化建议：**
- 使用 `SCHED_FIFO` 实时调度策略
- 将 CAN 发送线程绑定到固定 CPU 核心
- 减少 `VLOG(2)` 级别的日志输出

### 7.10 多车型切换问题

**症状**：更换车型后行为异常

**排查步骤：**

1. 确认完全停止上一个车型的模拟器
2. 检查是否有残留的 CAN 接口配置（波特率可能不同）
3. 确认 DBC 文件与车型匹配
4. 清除共享内存：`rm /dev/shm/chassis/*`
5. 删除锁文件：`rm /tmp/chassis_simulator.lock`

---

## 八、已知设计权衡与潜在改进

### 8.1 已知技术债

| 问题 | 位置 | 影响 |
|------|------|------|
| SendFrame 中硬编码帧 ID (`0x5c1`, `0x295`) | `can_channel.cc:231` | 新车型可能需要修改源码 |
| 工厂链的 try-order 硬编码 | `simulator_entry.cc:17-35` | 新产品线需要改代码 |
| PcieCanManager 单例 + static 锁管理器 | 全局 | 进程级单实例限制 |
| 中文日志字符串 | 全局 | 非 UTF-8 终端可能乱码 |

### 8.2 架构优势

- **策略模式的极致应用**：新增 CRC 变种只需继承 `Crc8BaseStrategy`，实现 3 个虚函数
- **Python binding 设计精良**：context manager (`with` 语句) 保证资源释放
- **共享内存日志**：零侵入的实时观测能力
- **锁文件 + Watch 机制**：优雅的进程间互斥和远程控制

### 8.3 潜在改进方向

1. **帧类型配置化**：将 CAN/CANFD 选择移到 JSON 配置中
2. **插件式工厂**：用动态注册替代硬编码的工厂链
3. **统一总线抽象**：`FlexRayMessagePool` 暗示了未来扩展方向，可以做一个 `BusInterface`
4. **指标导出**：`CanChannel::Stats` 可以导出到 Prometheus/Grafana
5. **热更新**：支持运行时更换 DBC/策略配置，无需重启模拟器

---

## 附录：关键文件速查表

| 功能 | 文件路径 |
|------|----------|
| 设备抽象接口 | `src/chassis/interfaces/device_interface.h` |
| DBC 编解码接口 | `src/chassis/interfaces/dbc_interfaces.h` |
| 策略链接口 | `src/chassis/interfaces/strategy_interfaces.h` |
| CAN 帧封装 | `src/chassis/devices/pcie_zlg/can_frame.h/.cc` |
| SocketCAN 通道 | `src/chassis/devices/pcie_zlg/can_channel.h/.cc` |
| PCIe 管理器 | `src/chassis/devices/pcie_zlg/pcie_can_manager.h/.cc` |
| ZLG 内核驱动 | `src/chassis/devices/pcie_zlg/driver/xpcfd.c` |
| 报文数据模型 | `src/chassis/data_pool/message_data.h` |
| CAN 报文池 | `src/chassis/data_pool/can_message_pool.h` |
| 发送处理器 | `src/chassis/processor/tx_processor.h` |
| 接收处理器 | `src/chassis/processor/rx_processor.h` |
| 周期通道 | `src/chassis/channel/period_channel.h` |
| 策略基类 | `src/chassis/strategy/core/strategy_base.h` |
| 策略链实现 | `src/chassis/strategy/core/strategy_chain_impl.h` |
| 策略工厂 | `src/chassis/strategy/core/strategy_factory.h` |
| 模拟器入口 | `src/chassis/simulator/entry/simulator_entry.h/.cc` |
| 基础模拟器 | `src/chassis/simulator/base_simulator_class/base_vehicle_simulator.h` |
| HIL Socket 桥接 | `src/chassis/simulator/business/hil_socket_bridge/hil_socket_bridge.h` |
| 动力学桥接基类 | `src/chassis/simulator/business/vehicle_model_bridge/base_model_bridge_processor.h` |
| Python 绑定 | `pybind_so/chassis_simulator_entry_bind.cc` |
| GUI 封装 | `src/gui/base/sim_chassis_wrapper.h` |
| CAN 信号服务 | `src/server/sim_server_for_can.h` |

---

*本文档基于源码逆向分析，部分推测可能与原作者意图有偏差。欢迎补充修正。*
