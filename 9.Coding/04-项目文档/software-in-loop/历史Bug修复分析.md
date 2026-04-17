---
share_link: https://share.note.sx/38664a0h#dfvkhiwlxSj9IiTxkrnFgn68hvniYWU+FbsXu2Q2R0Y
share_updated: 2026-04-02T16:53:39+08:00
---
# 历史 Bug 修复分析

#HIL #code-quality #bug-analysis

> 统计范围：2024-01-01 至 2026-04-02，共 1148 个 commit，其中 **199 个非 merge 的 bug fix commit**（占比 17.3%）。

## 一、按模块统计（最常被修复的文件 Top 15）

| 排名 | 文件 | Bug Fix 次数 | 模块 |
|---|---|---|---|
| 1 | `src/hil/utils/remote_invoke.cc` | 38 | 远程调用 |
| 2 | `src/hil/gui/window.cc` | 35 | GUI 主窗体 |
| 3 | `pipeline/config.xml` | 31 | 部署配置 |
| 4 | `config/hil/orin/initialize.sh` | 29 | Orin 初始化 |
| 5 | `pipeline/scripts/hil_gui` | 22 | 启动脚本 |
| 6 | `src/hil/base/ip_setter.cc` | 21 | IP 配置 |
| 7 | `config/initialize.py` | 19 | 初始化脚本 |
| 8 | `src/hil/script/main.py` | 17 | carplus 入口 |
| 9 | `src/hil/script/sim_chassis.py` | 15 | 底盘脚本 |
| 10 | `pybind_so/dr_websocket_client.cc` | 13 | WebSocket 客户端 |
| 11 | `src/hil/base/docker_module.cc` | 12 | Docker 管理 |
| 12 | `src/hil/server/joystick/g29_control.cc` | 11 | 方向盘控制 |
| 13 | `src/hil/gui/window.h` | 11 | GUI 头文件 |
| 14 | `src/hil/base/topic_table.cc` | 10 | Topic 监控 |
| 15 | `pybind_so/dr_ego_controller.cc` | 8 | 自车控制器 |

**观察**：Bug 修复最集中在 **远程调用**（38 次）和 **GUI 主窗体**（35 次），这两个文件是修改最频繁的热点区域。

---

## 二、按 Bug 类型分类

通过分析 199 条 commit message，按 bug 的类型/表现归为以下 9 个维度：

### 2.1 车型适配问题（~45 条，占 22.6%）

**表现**：某车型功能不可用、信号不正确、控车不生效

#### 真实案例 1：GWM 行车/泊车信号值不同但代码未区分（`3670f9b`）

**commit**: `gwm车型纵向控车行车和泊车用的信号一致，但是值不一致，进行了修复`
**改了 16 个文件**

DE09 底盘链路中，`BrkgTrqModResp` 信号在行车模式返回值 `2`、泊车模式返回值 `3`，但代码中用 `== 3` 作为纵向激活判断，导致行车模式下纵向控制完全不生效。修复：

```diff
- lon_enable = self.get("ADAS1", 0x12e, "BrkgTrqModResp", 0)
+ brkg_trq_mod_resp = self.get("ADAS1", 0x12e, "BrkgTrqModResp", 0)
+ lon_enable = brkg_trq_mod_resp in [2, 3]
```

**根因**：对 DBC 信号值域理解不完整 — 知道泊车值但不知道行车值。

#### 真实案例 2：基类重构遗漏车型特有信号配置表（`db197ea`）

**commit**: `之前提取了一个基类来抽象所有需要与底盘进行交互的server，但是G29中维护了一个配置表来保存不同车型中的细微信号差别，忘了将这一部分同步到基类中`
**改了 6 个文件**

三个问题叠加：(1) 接管信号仅在自动驾驶状态下有效，但代码全局判断；(2) 底盘链路未先判断纵向是否激活就提取控制信号；(3) 提取 G29 基类时遗漏了车型特有信号映射表。核心 diff：

```diff
- in_auto_mode_.store(control_cmd->driving_mode() != DrivingMode::MANUAL);
+ driving_mode_.store(control_cmd->driving_mode());

- if (acc_desire >= 0 && (takeover_state_ & takeover_throttle_enable)) {
-   control_command.set_acceleration_desire(acc_desire);
+ // 仅在自动/纵向自动模式下才判断接管信号
+ if (driving_mode_.load() == DrivingMode::LONGITUDINAL_AUTO ||
+     driving_mode_.load() == DrivingMode::AUTO) {
+   if (acc_desire >= 0 && !(takeover_state_ & takeover_throttle_enable)) {
+     control_command.set_acceleration_desire(0);  // 油门接管不可用则归零
```

**根因**：重构抽象时丢失了车型特定上下文（接管模式的多态行为）。

#### 真实案例 3：Carplus 共型号导致配置加载函数 copy-paste 错误（`8128bde`）

**commit**: `bugfix: 处理Carplus共型号导致的配置文件加载错误`
**改了 10 个文件**

`SaveConfig()` 中连续 4 行都调用了 `SetOrinHostname()`（copy-paste），实际应分别调 4 个不同方法：

```diff
- DCUConnectConfigFactory::GetInstance().SetOrinHostname(orin_name_->text().toStdString());
- DCUConnectConfigFactory::GetInstance().SetOrinHostname(orin_host_->text().toStdString());
- DCUConnectConfigFactory::GetInstance().SetOrinHostname(orin_pwd_->text().toStdString());
- DCUConnectConfigFactory::GetInstance().SetOrinHostname(orin_ip_->text().toStdString());
+ DCUConnectConfigFactory::GetInstance().SetOrinUsername(orin_name_->text().toStdString());
+ DCUConnectConfigFactory::GetInstance().SetOrinHostname(orin_host_->text().toStdString());
+ DCUConnectConfigFactory::GetInstance().SetOrinPassword(orin_pwd_->text().toStdString());
+ DCUConnectConfigFactory::GetInstance().SetOrinIp(orin_ip_->text().toStdString());
```

**根因**：密码/IP/用户名全被当成 hostname 保存，导致 ORIN 连接信息完全错乱。因为是 `SetOrinHostname()` 的合法调用，编译器无法检测。

**根因模式**：
- DBC 信号值域理解不完整（行车 vs 泊车模式返回值不同）
- 基类重构时丢失车型特有上下文
- Copy-paste 编程导致配置函数调错（编译器无法检测语义错误）
- 新车型适配涉及 15+ 文件的散落改动，反复遗漏返工

### 2.2 远程连接/部署问题（~35 条，占 17.6%）

**表现**：SSH 连接失败、driver 安装异常、域控环境部署出错

**典型 commit**：

| 描述 | 根因 |
|---|---|
| `修复域控连接不上时疯狂重试的bug` | 无退避策略 |
| `修复安装driver包时的权限问题` | 安装目录所有者不对 |
| `修复driver配置更新bug` | 配置覆盖顺序错误 |
| `域控重启后GUI可以自动恢复连接` | 未检测连接状态变化 |
| `ssh无法连接时报错但是不crash` | 异常未捕获 |
| `修复ros跨机通信时模块重启导致通信失败` | 重启后未重建连接 |
| `兜底底软中没有dpkg的问题` | 平台差异未兜底 |
| `修复SSHFS挂载代码` | C++ 和 Python 实现不一致 |

#### 真实案例 1：安装目录所有者问题（`c963dd2`）

**commit**: `安装driver之前先确保安装目录所有者没问题`
**改了 3 个文件**：`car_config.py` + `orin_setup.py` + `for_trip.h`

安装 driver 包前未检查 `/ota/deeproute` 目录的所有者，导致解压后文件权限错误，算法无法读取配置。修复方式：安装前先 `chown`。

#### 真实案例 2：域控重连风暴（`5c2120d`）

**commit**: `不管是节点的启动关闭还是切换场景都不会造成GUI的卡顿 + 域控重启后GUI可以自动恢复连接`
**改了 17 个文件，479 行重写 remote_invoke.cc**

域控连接断开后 GUI 疯狂重试（无退避），导致 GUI 卡死。修复方式：重构 `remote_invoke` + `remote_client`，添加连接状态管理和 10s 退避重试。

#### 真实案例 3：QNX 平台 sudo 报错（`e8c827b`）

**commit**: `remove use_sudo on qnx`
**改了 2 个文件**：QNX 上不存在 `sudo` 命令，初始化脚本中硬编码的 `sudo xxx` 直接报错。修复：检测平台后决定是否使用 sudo。

**根因模式**：
- 远端环境不可控（权限、目录、工具缺失）
- 网络异常处理不完善（重试/超时/重连）
- 跨平台差异（ORIN Linux vs QNX）

### 2.3 GUI 崩溃/卡顿/显示问题（~30 条，占 15.1%）

**表现**：GUI 闪退、界面卡顿、按钮/状态显示不正确

**典型 commit**：

| 描述 | 根因 |
|---|---|
| `没安装driver包时GUI不crash` | 缺少 null check |
| `修复gui闪退bug` | 多线程访问 Qt 对象 |
| `修复GUI在注入topic时会崩溃的问题` | 回调线程操作UI |
| `修复1920x1080分辨率下无法全屏的bug` | 布局未适配低分辨率 |
| `修复切换场景卡在99%的问题` | 异步操作未正确完成 |
| `修复右上角点击模块时无法启动docker的bug` | 信号槽连接错误 |
| `修复查询DEM异常节点时界面卡顿的bug` | 阻塞 UI 线程 |
| `修复x86 ip选择之后无法保存的bug` | QSettings 写入时机 |

#### 真实案例 1：注入 topic 时崩溃（`13adabc`）

**commit**: `优化HIL-GUI在注入topic时会崩溃的问题`
**改了 4 个文件（91 行新增，45 行删除）**

`MsgPublisher` 在回调线程中直接操作 protobuf Message 对象，与 UI 线程的读取产生竞态。修复：添加 `std::mutex` 保护共享数据。

#### 真实案例 2：WebSocket 线程安全导致崩溃（`2e5e31f`）

**commit**: `修复WebSocket客户端和消息发布器的线程安全问题，避免多线程并发访问导致的崩溃`
**改了 4 个文件**

`MsgPublisher` 使用裸指针管理 `MsgPublishTask`，多线程并发访问导致悬挂指针。修复：改为 `std::shared_ptr<MsgPublishTask>`。

#### 真实案例 3：缺少 driver 包时 GUI 崩溃（`b9443bf`）

**commit**: `没安装driver包时GUI不crash`
**改了 3 个文件**

域控上未安装 driver 包时，`dr_websocket_client` 尝试访问不存在的配置文件 → 空指针 → crash。修复：添加文件存在性检查。

**根因模式**：
- Qt 线程安全问题（非 UI 线程操作 Qt 对象）
- 缺少 null check / 空指针防护
- 阻塞 UI 线程的同步操作
- 状态同步不一致

### 2.4 底盘/控车问题（~25 条，占 12.6%）

**表现**：控车不生效、控车精度差、档位切换异常、画龙

**典型 commit**：

| 描述 | 根因 |
|---|---|
| `修复AEB控车bug` | AEB 信号值映射错误 |
| `修复档位切换bug` | 档位变更延迟处理不当 |
| `改善画龙问题` | P03 定位数据发送触发方式 |
| `修复纵向控车精度问题` | DBC 编码精度 |
| `修复方向盘控车bug` | G29 力矩映射错误 |
| `修复接管理解有误` | 仅自动状态下才有接管信号 |
| `修复底盘退出时ros资源管理导致的崩溃` | ROS shutdown 顺序 |

#### 真实案例 1：GWM 纵向控车精度（`6a22da0`）

**commit**: `修复GWM纵向控车精度问题`
**改了 12 个文件**

`de09_model_bridge_processor.cc` 和 `p03_model_bridge_processor.cc` 中，从动力学模型读取的加速度值通过 DBC 编码后精度丢失（float→int 截断），导致车辆加速/减速不平稳。修复：在 `vehicle_config.json` 中增加车辆质量和轮径参数，在 model_bridge 中进行高精度计算。

#### 真实案例 2：接管逻辑理解有误（`db197ea`）

**commit**: `之前对接管的理解有误，与彭尚对接后进行修复：仅在进自动状态下才会有是否可以接管的信号，不应该全局判断`

三个问题叠加：(1) 接管信号仅在自动驾驶状态下有效，但代码在全局判断；(2) 底盘链路未先判断纵向是否激活就提取控制信号；(3) G29 基类重构时遗漏了车型特有信号差异表。

#### 真实案例 3：P03 画龙问题（`c978572`）

**commit**: `优化P03定位数据发送触发方式，改善画龙问题`

定位数据通过 UDP 周期发送，发送频率与域控期望不匹配，导致航向角抖动 → 车辆画龙。修复：改为由域控侧触发请求后再发送。

**根因模式**：
- DBC 信号定义/精度/值域理解错误
- 控制逻辑与车辆实际行为不匹配
- 资源释放顺序不正确

### 2.5 WebSocket/通信问题（~20 条，占 10.1%）

**表现**：WebSocket 连接失败、消息丢失、订阅不生效

**典型 commit**：

| 描述 | 根因 |
|---|---|
| `修复WebSocket客户端和消息发布器的线程安全问题` | 多线程并发裸指针 |
| `修复websocket订阅可能失败的bug` | 订阅时机过早 |
| `修复偶发前几个topic未订阅上的bug` | 连接建立前发送 |
| `修复websocket被关闭的bug` | 自动化中未保持连接 |
| `修复websocket取消订阅的bug` | 取消逻辑不完整 |

#### 真实案例 1：裸指针竞态导致崩溃（`2e5e31f`）

同 GUI 崩溃案例 2。`websocket_client.h` 中回调函数在网络线程执行，但访问了 UI 线程持有的 `MsgPublishTask*`。修复：加 mutex + 改 shared_ptr。

#### 真实案例 2：前几个 topic 未订阅上（`c39e4c5`）

**commit**: `修复PIPELINE运行时偶发前几个topic未订阅上的bug`

WebSocket 连接建立后立即发送订阅请求，但此时 DEM 可能尚未完成初始化。修复：添加 DEM ready 状态检查后再发送订阅。

**根因模式**：
- 线程安全问题（裸指针、竞态条件）
- 连接时序问题（过早/过晚/未重建）

### 2.6 传感器仿真问题（~15 条，占 7.5%）

**表现**：传感器数据不正确、TCP/UDP 连接失败、帧率异常

**典型 commit**：

| 描述 | 根因 |
|---|---|
| `修复AT128雷达TCP服务` | TCP 连接管理问题 |
| `修复ATX雷达TCP服务` | 同上 |
| `修复sensor lidar crash问题` | socket 发送方式不对 |
| `修复Lidar数据发送bug：修改为整百毫秒发送` | 发送时机不对 |
| `修复camera时间戳，修复perception帧同步失败` | 时间戳偏移 |
| `修复Rolling Counter异常逻辑` | 计数器溢出处理 |

#### 真实案例 1：P177 E2E 特定值计算错误（`58385c4`）

**commit**: `fix：修复P177某些特定值的E2E计算BUG`
**只改了 1 个文件（`crc8_payload_strategy.cc`），核心改动 1 行**：

```diff
- return static_cast<int64_t>(std::llround((physical_value - offset) / factor));
+ return static_cast<int64_t>((physical_value - offset) / factor);
```

物理值转原始值时使用了 `llround`（四舍五入），但 ECU 使用截断转换，导致某些边界值的 CRC 校验不匹配。改为截断后与 ECU 行为一致。

#### 真实案例 2：吉利雷达时间戳计算（`f469154`）

**commit**: `fix: 修复吉利雷达时间戳计算`
**改了 2 个文件**：`timestamp_gl_split_unix_strategy.cc/h`

吉利的时间戳策略（`GlSplitUnix`）将 Unix 时间戳拆分为秒和微秒两个字段，但拆分计算中微秒部分的精度处理有误。

#### 真实案例 3：E2E 精度改善反而引入错误（`65b3d02`）

**commit**: `Fix：修复dbc编码精度改善引入吉利E2E计算错误`
**改了 7 个文件**：提升 DBC 编码精度时改动了 `base_channel_manager` 和 `base_vehicle_simulator` 的接口，导致吉利系列的 CRC8 Payload 策略使用了错误的数据源。

**根因模式**：
- 网络协议细节（字节流/数据报区别）
- 时间戳/帧率精度问题
- 协议字段计算错误（CRC/E2E 必须 bit 级一致）

### 2.7 配置/初始化问题（~15 条，占 7.5%）

**表现**：配置加载失败、初始化异常、配置不生效

**典型 commit**：

| 描述 | 根因 |
|---|---|
| `修复事件屏蔽不生效的bug` | 配置写入路径错误 |
| `修复初始化过程中误修改了docker-compose_bak` | 修改了备份而非工作文件 |
| `修复vehicle-config不更新的bug` | 切换车型未清理缓存 |
| `修复密码无法保存的错误` | JSON 序列化字段遗漏 |
| `修复配置文件无权限bug` | 文件权限默认值不对 |
| `修复safety event配置读取路径` | 路径硬编码不一致 |

#### 真实案例 1：初始化误修改备份文件（`28725758`）

**commit**: `修复初始化过程中误修改了docker-compose_bak.yaml的bug`

GUI 启动时对 `config.jsonnet` 做了修改，但修改的是 `docker-compose_bak.yml`（备份文件）而非工作文件。结果：sim-pbox 按钮一直存在（因为读的是未修改的原始 jsonnet）。

#### 真实案例 2：P177→P171 切换时 config 不更新（`e218ee8`）

**commit**: `修复PIPELINE从P177切换到P171时vehicle-config不更新的bug`

切换车型后未清理旧的 vehicle-config 缓存，导致 P171 继续使用 P177 的配置包运行。

**根因模式**：
- 配置路径硬编码不一致
- 配置覆盖/清理时机不正确
- 权限问题

### 2.8 编译/构建问题（~8 条，占 4.0%）

**表现**：编译失败、链接错误、CI 失败

**典型 commit**：

| 描述 | 根因 |
|---|---|
| `libssh编译问题修复` | 头文件路径变更 |
| `fix build for osbridge` | 依赖缺失 |
| `修复2004下的打包问题` | Ubuntu 版本差异 |
| `修复CI` | CI 配置与代码不同步 |

### 2.9 资源管理/稳定性问题（~6 条，占 3.0%）

**表现**：内存泄漏、资源未释放、进程僵死

#### 真实案例 1：底盘退出崩溃（`5e60a59`）

**commit**: `fix：修复底盘退出时ros资源管理问题导致的崩溃`

底盘仿真器停止时，ROS 节点的 shutdown 顺序不正确 — 先销毁了 publisher，但回调线程仍在使用。修复：按依赖顺序逆序 shutdown。

#### 真实案例 2：域控僵尸进程（`95ddbd9`）

**commit**（部分）: `启动GUI时先回收域控里的僵尸bash进程`

SSH 远程执行命令后未正确回收子进程，导致域控上积累大量僵尸 bash 进程。GUI 启动时先执行 `kill` 清理。

---

## 三、真实案例汇总（含时间/作者）

| Commit | 日期 | 作者 | 类别 | 描述 |
|---|---|---|---|---|
| `3670f9b` | 2025-04-30 | 罗小四 | 车型适配 | GWM 行车/泊车信号值不同但代码未区分 |
| `db197ea` | 2025-04-30 | 罗小四 | 车型适配/底盘 | 基类重构遗漏车型特有信号配置表 |
| `8128bde` | 2025-08-01 | 叶旭芳 | 车型适配 | SaveConfig copy-paste 调错函数 |
| `c963dd2` | 2026-03-09 | 罗小四 | 远程部署 | 安装目录所有者权限问题 |
| `5c2120d` | 2025-06-09 | 罗小四 | 远程部署/GUI | 域控重连风暴，479 行重写 |
| `13adabc` | 2025-06-09 | 宋亚琦 | GUI 崩溃 | 注入 topic 时 protobuf 竞态崩溃 |
| `2e5e31f` | 2026-03-12 | 宋亚琦 | GUI/WebSocket | 裸指针竞态改 shared_ptr |
| `b9443bf` | 2026-03-26 | 罗小四 | GUI 崩溃 | 缺少 driver 包时空指针 crash |
| `6a22da0` | 2025-12-03 | 罗小四 | 底盘/控车 | GWM 纵向控车精度（float→int 截断） |
| `c978572` | 2025-07-14 | 罗小四 | 底盘/控车 | P03 画龙（定位发送频率不匹配） |
| `c39e4c5` | 2026-03-24 | Xiaosi Luo | WebSocket | 前几个 topic 偶发未订阅上 |
| `58385c4` | 2025-10-11 | 刘志磊 | 传感器仿真 | P177 E2E llround vs 截断 |
| `f469154` | 2025-12-03 | 刘志磊 | 传感器仿真 | 吉利雷达时间戳拆分精度 |
| `65b3d02` | 2025-11-27 | 刘志磊 | 传感器仿真 | DBC 精度改善反引入 E2E 错误 |
| `2872575` | 2025-12-24 | Xiaosi Luo | 配置/初始化 | 误修改 docker-compose 备份文件 |
| `e218ee8` | 2026-03-14 | 罗小四 | 配置/初始化 | 车型切换后 config 缓存未清理 |
| `5e60a59` | 2025-09-24 | 刘志磊 | 资源管理 | ROS shutdown 顺序导致底盘退出崩溃 |

---

## 四、修复人统计

| 作者 | Bug Fix 次数 | 占比 | 主要负责领域 |
|---|---|---|---|
| 罗小四 / Xiaosi Luo / xiaosiluo | 142 | 71.4% | GUI、远程调用、底盘控车、车型适配全栈 |
| 刘志磊 | 20 | 10.1% | 底盘策略（CRC/E2E/时间戳）、吉利系列 |
| 叶旭芳 | 12 | 6.0% | 车型适配、初始化、配置工厂 |
| 宋亚琦 | 10 | 5.0% | 线程安全、WebSocket、Topic 监控 |
| 刘洪梅 | 9 | 4.5% | LiDAR 仿真、HUT、相机 |
| 陈清匀 / qingyunchen | 4 | 2.0% | GUI 改进、编译修复、driver 安装 |
| @changweilu | 1 | 0.5% | 零跑底盘数据 |

> 注意：罗小四一人修复了 **71.4%** 的 bug，是该项目的核心维护者（bus factor = 1 风险）。

---

## 五、按月趋势

```
2024-04  █                              1
2024-06  ███                            3
2024-07  ██████                         6
2024-08  ███████                        7
2024-09  ██████                         6
2024-10  ████                           4
2024-11  ███                            3
2024-12  ████████                       8
2025-01  █████████                      9
2025-02  ████                           4
2025-03  █████                          5
2025-04  █████████████████             17  ← DE09适配+接管逻辑修复
2025-05  ████████                       8
2025-06  █████████████                 13  ← GUI卡顿重构
2025-07  ██████████████                14  ← P03画龙+Smart适配
2025-08  ██████████                    10
2025-09  ████████                       8
2025-10  ██████████████████            18  ← P177 E2E修复高峰
2025-11  ████████████                  12  ← B26A适配+DBC精度
2025-12  ██████████                    10  ← 时间戳/精度修复
2026-01  ████████████                  12
2026-02  ███                            3
2026-03  ██████████████████            18  ← P03A适配+WebSocket修复
```

> Bug 修复有明显的 **波峰模式**：每次新车型适配（2025-04 DE09、2025-10 P177、2025-11 B26A、2026-03 P03A）后 1-2 个月是 bug fix 高峰期。

---

## 六、Bug 类型分布图

```
车型适配问题          ████████████████████████  22.6%  (45)
远程连接/部署问题      ██████████████████        17.6%  (35)
GUI 崩溃/卡顿/显示    ████████████████          15.1%  (30)
底盘/控车问题          █████████████             12.6%  (25)
WebSocket/通信问题     ██████████                10.1%  (20)
传感器仿真问题         ████████                   7.5%  (15)
配置/初始化问题        ████████                   7.5%  (15)
编译/构建问题          ████                       4.0%  (8)
资源管理/稳定性        ███                        3.0%  (6)
```

---

## 七、根因模式总结

| 根因模式 | 出现频率 | 涉及 Bug 类型 | 示例 |
|---|---|---|---|
| **车型硬编码散落** | 🔴 极高 | 车型适配、配置 | 新车型遗漏注册、信号名写错 |
| **线程安全问题** | 🔴 高 | GUI 崩溃、WebSocket、通信 | 多线程操作 Qt 对象、裸指针竞态 |
| **异常处理不充分** | 🟡 中 | 远程连接、GUI、传感器 | SSH 失败未捕获、null check 缺失 |
| **环境/平台差异** | 🟡 中 | 远程部署、编译 | ORIN vs QNX、Ubuntu 版本差异 |
| **DBC/信号精度** | 🟡 中 | 底盘/控车、车型适配 | CRC 计算、时间戳格式、编码精度 |
| **时序/状态管理** | 🟡 中 | WebSocket、配置、GUI | 连接时序过早、异步状态不同步 |
| **路径硬编码不一致** | 🟢 低但反复 | 配置、初始化 | 同一路径在不同文件中写法不同 |
| **资源泄漏/未释放** | 🟢 低 | 稳定性 | socket/进程/指针未清理 |

---

## 八、热点文件与模块风险评估

| 风险等级 | 模块 | 理由 |
|---|---|---|
| 🔴 高风险 | `remote_invoke` / `for_remote` | Bug Fix 次数最多（38次），远程环境不可控 |
| 🔴 高风险 | `gui/window.cc` | Bug Fix 次数第二（35次），Qt 线程安全问题频发 |
| 🟡 中风险 | `dr_websocket_client` | 通信核心，线程安全问题反复出现 |
| 🟡 中风险 | `joystick/g29_control` | 多车型信号映射，每新增车型都需改动 |
| 🟡 中风险 | `config/initialize.py` + `orin_setup.py` | 域控初始化流程复杂，环境差异大 |
| 🟢 低风险 | `chassis/simulator/` 核心代码 | Bug 修复集中在数据层，核心逻辑稳定 |

---

## 九、改进建议

| 优先级 | 建议 | 预期收益 |
|---|---|---|
| 🔴 P0 | 引入车型注册表，消除散落硬编码 | 减少 22.6% 的车型适配 bug |
| 🔴 P0 | 为 `remote_invoke` 添加重试/超时/断线重连策略 | 减少 17.6% 的远程部署 bug |
| 🟡 P1 | 将 GUI 中所有网络/远程操作移到 Worker 线程 | 减少 GUI 崩溃/卡顿 |
| 🟡 P1 | WebSocket 客户端引入线程安全封装（mutex + shared_ptr） | 减少通信层 bug |
| 🟡 P1 | DBC 数据自动一致性校验（CI 集成） | 减少信号精度/命名 bug |
| 🟢 P2 | 统一配置路径管理（消除硬编码路径） | 减少配置/初始化 bug |
| 🟢 P2 | 为 strategy 模块添加基于真实 CAN 数据的回归测试 | 防止 CRC/E2E 回归 |
