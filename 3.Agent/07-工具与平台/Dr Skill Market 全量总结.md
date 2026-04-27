# Dr Skill Market 全量总结

# 行业公共知识 & 通用研发效能 Skills 摘录

> 以下 Skill 与公司具体业务弱相关，偏向行业公共知识，可通用于其他自动驾驶/机器人/互联网研发团队：

**1. 通用性能排查 (Perf & Profiling)**
- `perf-analyzer`: 通用的 QNX/Linux 性能排查引擎，CPU/GPU/IO 异常与通用内存/调度诊断。
- `cpu-flamegraph-analysis-skill`: CPU 火焰图数据获取与代码级优化分析。
- `memory-profile-leak-troubleshooting`: jemalloc (Linux) 和 tcmalloc (QNX) 的通用内存泄漏分析。
- `compilation-diagnosis`: 专门用于诊断 Bazel (Monorepo) 编译错误的排查工具。

**2. AI Agent 与大模型基建 (Agent & LLM)**
- `llm-wiki-skill`: 构建 Karpathy 风格的本地 Obsidian LLM 知识库。
- `agent-learning-system-skill` / `team-shared-learning`: AI Agent 跨会话记忆与团队持续学习体系。
- `infinite-qa-mode`: 让 Agent 进入持续问答循环的通用模式。
- `auto-cot-analyzer`: 通用的复杂系统大思维链（Chain-of-Thought）日志分析与补全。

**3. 通用代码开发与代码审查 (DevOps & Git)**
- `gitlab-cli-skill`: GitLab 原生 CLI (glab) 专家级使用指导。
- `resolve-conflicts` / `rebase-helper`: 通用的 Git 解决合并/Rebase 冲突辅助。
- `code-integration`: 跨仓库/跨分支的 Cherry-pick 代码移植与集成。
- `parallel-review-loop`: 利用多路 Agent 并行进行 Code Review 的通用工作流。
- `repo-documentation-builder`: 为代码仓库自动建立渐进式的规范文档体系。

---

## Adas Farm

1. **adas-farm-cli**: 管理 ADAS Farm CI/CD 平台资源的 CLI 工具 farmctl。涵盖 driver/model 发布版本（release）、模型训练（training）、MRSets、变更集（changeset）、里程碑（milestone）的创建与查询，artifact 制品（driver包、fota包、OTA交付版本）的查询与下载，以及 driver 版本性能数据报告导出。
2. **adas-farm-workflow**: Orchestrate ADAS development workflows via Python scripts using python-gitlab, AdasFarmSdk, and artifacts-client. Covers code review, release management, driver metrics, diagnosis result update, Artifacts same-release driver lookup, MRSet rebase (cherry-pick), and model release config comparison for ADAS projects.
3. **dr-modify-full-driver**: 从 ADAS Farm Release 下载指定架构的 Driver 包并安装到本地环境。支持 Release 信息获取、Release Task 查询、Driver 包下载解压安装的完整流程。

## Aeb

1. **aeb-diagnose**: AEB 漏触发/晚触发自动化诊断：按 tag 下载双包、本地 DDL 开环、日志分析与后验，支持 MCP 与飞书反馈。

## Ai Agent

1. **dr-ai-wizard**: Deeproute 公司级 AI 编码环境一键配置，自动检测并配置 Claude Code / Cursor / Codex 三平台的指令规则、安全 hooks 和基础 skills

## Blc

1. **blc-new-vehicle-bringup**: blc/safety/dta/bridge/dsm 新车型适配
2. **blc-diagnosis**: 诊断 BLC 飞书问题，自动从飞书项目空间下载关联的问题数据，对 BLC 的泊车/行车/主动安全问题进行定位分析

## Cbw

1. **autonomous-diagnose**: CBW 控制模块全自动诊断。输入 tag_instance_id，自动完成 bag 下载、CSV 导出、场景分诊、数据分析和诊断结论输出。覆盖横向、纵向、安全策略、轨迹一致性、流程五大诊断领域。
2. **cbw-sim-verify**: 修改代码后通过下载 bag、编译、开环仿真、数据分析对比的完整流程验证修复效果
3. **cbw-build**: 编译 control-by-wire 项目并生成发布包，支持多车型配置和本地编译。

## Cloud Sim

1. **simulation-copilot**: 暂无描述

## Data Mining

1. **nano-mining-guide**: pp_thanos 项目的 nano_mining 数据挖掘运维指南。涵盖 CPU 集群配置、断点续跑、资源规划、按类型存储障碍物指标的 Mining 方案，以及常见问题排查。
2. **data-mining**: AI Agent 设计的自动驾驶数据挖掘通用完整流程。7 Phase 端到端覆盖：需求澄清、metric 设计、mining 运行、后处理筛选、质检抽检、可复现性管理、经验沉淀。适用于泊车/行车/高速/城市任意场景。

## Data Ops

1. **deelooper-task-helper**: Deelooper 数据生产平台操作。创建工作流任务（含产线）、查询进度、资源级完成/失败/运行中统计（按专项+LTX任务名分组、饼图、缓存）、错误归因分析、调度慢诊断、预设管理。

## Dr Platform

1. **onboard-crash-diagnosis**: 分析 drplatform 上的车辆 crash 事件。查询事件详情、按版本汇总 crash 分布、按堆栈哈希归类、检查 trip 的 log/bag 可用性、触发厂商数据拉回、管理 crash 知识库。
2. **bag-merge**: 根据 tag_instance_id 下载并合并 bag 文件。当用户需要下载 bag、merge bag、合并 bag、按 tag 下载 bag、下载 light_topic 时使用。
3. **perf-analyzer**: 车端性能排查与全模块优化。通用代码审计引擎 + 分层 SOP 诊断（模式 1-39 + 35A），支持发现已知和未知问题。分析 QNX/Linux 日志定位 CPU/GPU/IO/内存异常根因，GPU kernel OOB 通用审计（检测模式 A–L + C2，覆盖 atomic/gid/类型/坐标/索引/shared_mem/循环/buffer/barrier/struct成员/向量对齐/间接索引链/日志深度扫描 越界，以 generic-audit-engine.md 为 SSOT），输出代码级修复建议和按负责人分类的报告。支持火焰图、kev、SMMU/kgsl、Planning 心跳、DNM 网络、全车 CPU 预算拆解、sched_agg 调度聚合分析、devb-ufs IO 尖峰、整机 CPU 过载、内存泄漏、优先级抢占、传感器断流、网络链路诊断、跨平台性能对比（SA8797 vs DE09/Thor）、冷启动依赖链分析等场景。核心理念：以通用排查方法为主，已知案例为辅，持续迭代更新。
4. **sil-diagnosis**: 让 AI 帮你一键诊断 SIL（Software-in-the-Loop）仿真测试 Job 的失败原因。
5. **bi-copilot**: BI 平台数据查询助手，支持矩阵查询、DataView 查询、SQL/DQL 执行、看板分析等

## Dr Training

1. **experiment-iteration-loop**: 让 AI Agent 自主完成实验迭代闭环：定义假设、注册实验、运行训练、汇总 pros/cons、记录决策。支持 ML 训练实验和离线评测。 Agent 连接内部 Grafana 实例，为 Cursor IDE 提供监控数据查询能力.

## Driving Perception

1. **percep-model-release**: 一键触发 percep/e2e 一段式发版：通过 ADAS Farm register-automation API 生成真实 percep payload，完成模型 MR 提交、driver 构建和 custom-e2e-benchmark 配置；也支持根据 YAML 改动描述创建 pth_update_mr_url MR。

## Driving Pp

1. **openloop-benchmark-comparison-viz**: 从嵌套JSON或飞书/Markdown评测报告生成交互式HTML对比看板，支持viz.py一键生成、多模型多场景metric对比、Chart.js图表、样本量置信度分析、拖拽列排序

## Gitlab

1. **gitlab-cli-skill**: A comprehensive Claude Code skill that provides expert guidance for using the GitLab CLI (glab) to manage GitLab resources directly from the command line.

## Map

1. **map-onboard-diagnostics**: 地图onboard自动诊断skill，自动下载case对应描述并分析

## Mcu

1. **sil-cli**: 自动化 SIL 仿真平台的构建和运行 CLI 工具，支持一键初始化、构建、运行测试用例
2. **loc-mcu-assistant**: MCU 融合定位模块独立构建与测试助手，支持独立编译 localization-mcu、单元测试、回放测试、数据集制作、结果评估、对比分析、配置生成等功能。
3. **mcu-workflow**: 通过mcuctl CLI完成MCU域控开发工作，支持初始化、编译、OTA 升级、日志查看、串口调试、代码质量审查
4. **mcu-log-analysis**: AURIX TC3xx MCU 日志分析：抽取复位、Trap、ErrorHook、PanicHook、WdgM、SystemReset、HCU 等并生成HTML/Markdown；支持 Map 与 Os/WdgM/SystemPower 等工程头文件，解析前预检工作区头文件，可用 GitLab API 拉取相关文件；预检；支持单文件、目录批量与时间或 tick 窗。
5. **mcu-code-reviewer**: MCU编码规范（目前不维护，请使用MCU Workflow CLI(mcuctl) ）

## Ml Ops

1. **trdatacli**: 操作 MLOps 训练数据管理服务的 CLI 工具，支持 workspace、训练数据、数据版本、元数据、数据 review 的全生命周期管理

## Parking

1. **roaming-parking-loc-diagnosis**: 基于 debug_plots_vpa_gamma 画图并读图，诊断漫游泊车/记忆泊车地图定位问题（定位不成功、位置或航向偏差、map matching 状态），替代人眼看图。
2. **avp-song-biao**: AVP 泊车送标：自动查询 bag、按时间分组、创建 Batch 和 Work 任务

## Perf

1. **cpu-flamegraph-analysis-skill**: 基于 CPU 火焰图的深度性能分析 Skill，覆盖从数据获取到代码级优化建议的完整流程。
2. **memory-profile-leak-troubleshooting**: Memory profiling and leak troubleshooting for jemalloc (Linux) and tcmalloc (QNX).

## Skill Market

1. **skill-market-cli**: 通过 skillctl CLI 完成 Skill Market 所有操作：安装/查找/搜索 Skill、创建和发布 Skill、查看企业 Skill 规范、浏览能力图谱
2. **dr-cli-core-skill**: 这个SKILL是公司所有CLI壳子的SKILL。关联仓库：https://code.deeproute.ai/deeproute-org/agi/drclictrl。理论上所有其他的CLI的SKILL，都应该依赖此。
3. **dr-skills-env-setup**: 一站式配置所有 Skill Market skill 需要的环境变量（GitLab Token、DR Platform 账号、Grafana Token 等），配一次全部 skill 通用
4. **skill-market-finder**: AI Agent 编写的内部 Skill Market 搜索安装工具。搜索、浏览、安装、更新 Cursor Skill，对接 skill-market.srv.deeproute.cn API。

## Soc-Infra

1. **vpm-config-triage**: 暂无描述

## Takeover

1. **dts-problem-diagnosis**: 定位 Dr TimeSync (DTS) 模块的时间同步问题，系统化检查数据面(ptp4l/PHC)和管理面(NTP/system clock)同步状态
2. **vlm-agent**: 通过 Docker 运行 vlm pipeline，完成 AEB/导航/接管/感知场景的诊断分析。

## Test

1. **testcase-auto-generation**: 一站式智能驾驶测试用例自动生成系统，从需求文档PDF到完整Excel测试用例集的全流程自动化。

## Traffic Light

1. **find-volc-path-by-bagname**: 根据bag_name 去查找火山上生产的record的路径
2. **opencode-use-qiniu**: 在opencode上配置qiniu api (目前dj-chatgpt5.4 比较好用，anthropic 的不太行）
3. **traffic-light-autolabel**: 通过自然语言指令驱动红绿灯E2E自动标注全流程，覆盖解包、数据同步、大模型推理、查diff、规则清洗、vllm清洗、训练数据格式转换7个步骤

## 其他未分类 (Other)

1. **skill-usage-tracer**: 自动追踪 Agent Skill 调用记录，通过 HTTP 上报到 Skill Market 用量统计 API，支持按 turn 分组分析调用链路
2. **canbus-dbc-generator**: Generate and update CAN DBC parsing code for control-by-wire (cbw). Supports multiple OEMs (GWM, Geely, Leapmotor, etc). Produces ready-to-use dbc_xxx_vyy directories with assign_proto, assign_struct, cantools C code, frame_handler, special_process, BUILD file, and chassis_detail.proto.
3. **simulation-readme**: 仿真仿平一篮子skill集合
4. **monitor-cli**: 操作 Monitor 管理服务的 CLI 工具，支持 event、car、vin、metadata数据查询
5. **aep-skills**: 对 AEP/LP 案例进行诊断与 Debug。支持从 Tag 实例拉取案例数据（Bags、Logs、Driver、配置）、解析 Metric、分析模块日志与 Perception/Safety，产出诊断报告。当用户提出案例诊断、分析 tag、看 metric/日志/安全事件或需要根因分析时使用此 skill。
6. **benchmark-analyze**: 如何使用 ai benchmark cli
7. **vlm-prompt-generator**: 为 VLM Mining 自动生成主动安全场景质检 prompt，结合 AEB 场景知识输出结构化的 VLM 质检指令
8. **llm-wiki-skill**: 用于构建 Karpathy 风格的 LLM 知识库的代理技能——一个自编译的 Obsidian markdown wiki，其中 AI 代理摄取原始资源，编译交叉链接的概念/实体/摘要页面，回答针对语料库的查询，检查健康状况，并处理人类反馈。
9. **diagnose-planning**: 诊断 Planning 模块问题。当实车出现不绕行、点刹、刹车重、距离太近、决策不合理、轨迹异常、减速过早/过晚等问题时使用。
10. **cbw-mbd-create**: 在 canbus-stateflow 仓库中指导线控 MBD 迭代
11. **lake-search**: Paimon/StarRocks 湖表多维检索、Record 视图联合导出 CSV 与只读统计分析。
12. **ai-safety-simulation**: AI Safety 组仿真测试智能助手，支持触发仿真测试任务、AEB Backfill 回灌与流程自动化脚本（裁剪/汇总/场景集/创建任务）、诊断模板查询、主动安全版本获取。
13. **agent-learning-system**: AI Agent 设计的一站式跨 session 记忆 + 持续学习系统。8 条协同 Rules、Engram 语义搜索、结构化学习记录，200+ 条 learnings 实战验证。
14. **feishu-gitlab-workflow**: 从飞书项目需求/缺陷自动解析基线分支，创建 GitLab Issue、分支、MR，并可选同步到 ADAS Farm
15. **prophet-worldsim-builder**: 用于在 Prophet 中完成自动场景搭建、上传到 simulation-scenarios/prophet-world-sim，并提供复用检索、校验与记录回填流程。
16. **resolve-conflicts**: 解决 Git 合并冲突或 rebase 冲突。当用户需要解冲突、处理 merge conflict、rebase 冲突、MR 有冲突需要修复时使用。解完冲突后生成总结供用户检视，不自动 push。
17. **grading-skills**: Grading 相关能力集合，包含飞书文档集成、飞书项目集成、迭代计划元文档站，支持文档读写、工作项查询、场景入库、批量回灌诊断等
18. **open-loop-planning**: Planning 开环回放验证。当用户需要播包验证、回放 bag、开环仿真 planning、DDL 仿真、rosbag play 验证 planning 修改时使用。
19. **perception-data-tracker**: 用于追踪感知数据专项和单批次生产任务进展，并对齐deelooper和飞书项目信息，判断风险，提醒对应负责人，生成周报等功能
20. **build-planning**: 编译 Planning 项目。当用户需要编译 planning、构建 planning、打包 planning、安装 planning_package 时使用。
21. **pp-data-production**: 帮助用户快速执行 PP 相关飞书项目管理、镜像更新、工作流创建等任务；支持从 txt 列表创建 Deelooper batch（URI/BAG 输入、backfill_version、可选 dataset 来源等）
22. **vpa-levelk-task-guide**: pp_thanos 项目中创建 VPA Level-K Prediction 混合任务的完整指南。涵盖 specific_task 注册机制、Unified Agent 解码器设计、9维→18维数据格式映射、Feature/Target/Anchor Builder 构建、Loss/Metric 适配、Agent-Map Fusion 模块，以及常见 runtime 错误排查。
23. **data-collection-requirements**: 对话提供必要字段，快速创建数据采集需求
24. **simcli-skill**: 仿平CLI的官方SKILL
25. **bench-cli**: 通过 benchctl CLI 管理台架资源：台架 CRUD（by-model）、OTA/SOTA/FOTA 升级、交互终端、远程执行、文件传输、复现任务、预约管理
26. **sanmap-kpi-generator**: 根据仿真平台 Sim Test 链接，自动生成 SANMap KPI 对比报告（HTML 可交互）
27. **mining-skill**: 通过自然语言创建挖掘模板到挖掘平台，集成托管平台自动获取算法版本和标签。Use when the user mentions 挖掘模板, mining template, 跑算法, 查询算法, or wants to create mining templates.
28. **map-engine-network-diagnosis-without-code**: 纯日志驱动的 map-engine HTTPS 网络诊断，内置服务清单、错误码字典和智驾影响分析，无需查看源码即可定位网络故障。
29. **search-cli**: 资源多维度检索与热力分布可视化：数据包（bag）/ 帧级数据（record）/ trigger / link 热力图 / 轨迹图。支持按场景、车型/车辆、时长里程、任务类型、地图属性、障碍物、事件/drtag、trip 名、城市/多边形、时间范围等维度自由组合，无需记命令、字段或 JSON。
30. **trip-name-matcher**: 根据测试信息匹配DR Platform行程名称，支持GL/LP双项目（VIN/秘钥映射、HTML清洗、多时间格式），生成诊断页URL
31. **church-cli**: 将 bag 文件中的 Protobuf 消息 dump 为 JSON，并提供 .desc 与 topic_map 生成工具。支持自动查询 driver 版本并完成端到端 dump。
32. **ci-self-healing**: 自动巡检 ADAS Farm CI 失败 Job，诊断瞬时故障，执行自动重试
33. **sanmap-benchmark-reporter**: SANMap 模型评测指标报告与多版本对比分析工具，支持 Lane3d、Curb Seg、RoadMask、BoundaryPassableEgo、Passable E2E、ETC 七大指标
34. **tjob-skills**: 通过 tjob CLI 提交和管理训练任务：支持 dr_training / 火山引擎 volc / 阿里云 PAI 三平台，涵盖任务提交、查询、停止、资源锁定/解锁、飞书通知监控、deekeeper 实验查询
35. **perception-training-launch**: UniPrime 训练任务启动模板管理，支持 DrTraining / Volc / PAI 三平台。提供训练模板生成、参数确认、farmctl CLI 启动流程。当需要启动模型训练任务、配置训练参数时使用此 skill。
36. **sim-log**: 从仿真平台（simulation.deeproute.cn）按 task_id + scene_id 下载仿真任务的 log/bag/grading 产物，用于 crash 分析和问题诊断
37. **event-data-analysis**: Analyze autonomous-driving events with SENTRY-based location enrichment, distribution metrics, hotspot clustering, and webfile report publishing.
38. **flamecraft-cli**: flamecraft的Cli工具
39. **progressive-autonomous-driving-research**: 递进式自动驾驶研究 Skill
40. **det-defect-tracker**: 从「基础感知问题诊断」飞书群收集 DET 感知缺陷，经门禁过滤与去重后写入「DET感知问题闭环」多维表格，并回写飞书项目 benchmark 确认状态；含版本查询与 FO 规则。
41. **cbw-dbc-generator**: Generate and update CAN DBC parsing code for control-by-wire (CBW). Supports multiple OEMs (GWM, Geely, Leapmotor, VinFast, etc). Produces ready-to-use dbc_xxx_vyy directories from DBC/XLSX files with assign_proto, assign_struct, cantools C code, frame_handler, special_process, BUILD file, and chassis_detail.proto.
42. **code-index**: 本地语义索引 Skill：把自然语言问题（代码在哪、怎么实现、调用链、Bazel 依赖等）转成对本机 code-index CLI 的调用，再基于 NDJSON 结果作答并带 path:行号 引用。不把源码外传，所有嵌入走本机 Ollama。
43. **canbus-diagnose**: Canbus 模块全自动诊断工具集，覆盖横向/纵向握手、换挡、安全带、自动模式等诊断领域，支持 bag 数据分析、诊断框架填充和飞书项目集成
44. **vlm-mining-operator**: VLM Mining 平台全流程操作：创建/调试/上线算法，管理数据集，运行评测/迭代，提交场景挖掘
45. **ltx-cli**: LTX 标注平台：用 dr ltx 或 ltx-cli 管理任务/实例/供应商/专项、下载结果与排查状态。
46. **cbw-md-to-feishu**: 从本地 Markdown 文件和图片生成飞书文档，支持导入 wiki 并批量嵌入截图。
47. **odometry-diagnosis**: 局部定位模块（sensor-ins-online / odometry）问题诊断，支持飞书 Case 输入、自动绘图分析、根因定位、报告生成与评论回传
48. **sd-op-trace**: 通过 Elasticsearch MCP 查询 SDMap 闭环流程的操作日志，支持资料/任务/母库变更的追溯查询
49. **cbw-apa-error-analysis**: 针对 APA 准出报告中的 Heading/Lateral/Velocity/Longitudinal 误差超限项进行批量分析、截图生成与报告产出。
50. **aeb-dev-assistant**: AEB（自动紧急制动）模块的 AI 编程助手，提供架构理解、开发指导、代码审查、改动验证和发版流程支持
51. **code-integration**: Cherry-pick commits from ADAS Farm MRSet links or GitLab MR links onto a base branch across multiple repos. Handles conflict resolution preserving all new functionality, generates integration reports, and creates new MRs/MRSet. Use when the user mentions code integration, cherry-pick, branch merging, MRSet integration, or wants to port changes from one branch to another.
52. **lane-change-debug**: 帮助诊断 planning 模块中变道决策链路的问题，覆盖意图生成、安全筛选、Force 拦截等全链路。内置架构知识库、已诊断 case 和六步排查方法论。
53. **safety-pptag-premining-workflow**: 运行 Safety PPTAG 预挖掘或预挖掘+数据生产的标准化 6 步串行流程，包含启动前交互确认、强制本轮新检索、Deelooper 任务创建与状态门禁、Step4 标签筛选以及失败节点回传。
54. **sanmap-auto-eval**: 自动执行 SANMap 评测流程，基于 Sim Test 链接生成 KPI 对比与评测摘要。
55. **sync-sim-scenarioset-to-feishu**: 该SKILL可以自动从仿平读取当前已创建的场景集列表并同步到飞书项目的感知benchmark所属场景集字段中，便于研发在送标时能比较方便地直接选择对应场景集
56. **test-route-planner**: 测试路线规划：告诉我城市、目标里程、OA 账号和想测的场景（一个或多个），我自动拉取多场景热力图、合并并串出一条总里程接近目标、多场景均衡覆盖、尽量经过高热力点的路线，产出 heatmap.json 并给出按场景维度的总结表格。
57. **rodin-3d-modeling**: 自动化 3D 建模工作流：通过 Rodin (hyper3d.ai) 平台实现图片搜索、上传建模、几何生成、材质贴图、OBJ 导出的全流程自动化
58. **volcengine-drive-devbox**: 连接和使用火山云 DRIVE 开发机，SSH 配置、共享目录约定、标准开发工作流
59. **tjob-submit**: 通过 tjob 命令行提交火山云 DLC 训练/挖掘任务，提交前做完整正确性验证
60. **build-farseer**: 编译安装 Farseer 预测模块，配置带预测的 DDL 播包环境
61. **quant-precision-analysis**: Analyze ONNX model quantization precision from AIMET PTQ experiment results. Identifies bottlenecks, traces error propagation, and suggests precision optimization.
62. **vpa-farseer-parking**: Farseer stopnet 泊车/VPA：四路轨迹输出、Frenet 坐标链、PerceptionObstacles 直写、FillTrajToObstacles 分支、LOW_SPEED 下 MODEL_PARKING 与 agent_context 关系及调试要点。
63. **qnn-graph-optimization**: 面向高通 QNN/HTP 的 ONNX 模型图优化 Cursor Agent Skill。自动完成子图分析、优化 Pass 编写、测试验证、板端编译运行与性能分析的端到端工作流。
64. **query-tag-link-modifications**: 给定标注 tag，查询该 tag 下所有任务发布时修改了哪些 sd_link_id，输出逐 task 明细和去重汇总。
65. **robotaxi-diag**: Diagnose Robotaxi system issues by analyzing logs, FSM states, gRPC errors, WebSocket messages, and navigation failures.
66. **localization-mr-chief-review**: 对定位相关 GitLab MR 做首席级评审；输出须含 gitlab-mr-code-review 同构的 AI Code Review 摘要必要块；用户给出 MR 链接时默认须将评论区压缩版发 GitLab。支持 localization、localization-mcu、离线 localization-tools。
67. **record-dump-helper**: record生产助手，帮助bag/issue数据进行回流和专项生产
68. **dr-model-release**: DR 量化工具的感知模型发版与 OTA 上传，支持 uni_model/vision/magic_carpet 三类模型的增量发版
69. **diagnose-speed-limit**: 从飞书 Case 下载数据、提取限速诊断输入并结合知识库分析；支持 dpbag 与曲率半径工具。
70. **global-localization-diagnosis**: 对齐飞书 Wiki 做地图匹配/GNSS/绑路诊断；默认按 ntpTime 选单段 Light+drfile 拉包；bag 出图与 gps_localization 日志溯源；默认回填闭环多维表；可选经确认的飞书评论。
71. **safety-model-dev-assistant**: SafetyModel 模型开发辅助，覆盖训练数据 pkl 探索（ttc_infov4、past_agent_info 字段解读、版本对比）、数据生产流程（PP Tag 开发验证、试产、全量）、环境配置（数据挂载、Docker 镜像、Trajcaching）、闭环验证（仿真回灌、Backfill、Benchmark）。
72. **sensor-stress-test-analysis**: LP 平台传感器模块（camera/radar/lidar/ultrasonic）台架压力测试日志捞取、异常分析与飞书报告生成。支持 SA8650/SA8797 QNX 平台，覆盖 SSH 日志拉取、drtar 解包、逐传感器帧率与异常检测、系统资源分析、根因归类及结构化报告输出。
73. **release-health-summary**: 查看 ADAS Farm Release 的编译、SIL、Module-Bench 等 CI 健康状态总览，支持交互式深入诊断失败项
74. **diagnose-ilqr**: 输入 proto 文件和 tag 时间戳，自动解析 iLQR debug 数据、选帧、构建上下文、执行诊断分析，生成 HTML 诊断报告
75. **ilqr-batch-diagnosis**: 批量处理飞书项目中的 Planning 问题，对每个 case 运行开环仿真 + iLQR 诊断，生成汇总报告
76. **drp-api**: 查询和调用 DR Platform 的各类 API，支持行程、Bag 等数据查询，自动匹配接口并格式化返回结果
77. **hil-diagnosis**: HIL 功能逻辑智能诊断工具。自动分析 NCA/ICA/ACC 状态异常、大红手接管、CAN 信号残留、MRM 退出异常、AEB/MEB/FCW 触发、Safety 策略退出等问题，支持飞书文档辅助查证、bag 数据验证、诊断记录对比，诊断结论自动沉淀为知识库。
78. **compilation-diagnosis**: 这个 skill 专门用于诊断 Bazel 编译错误，特别针对 monorepo 架构项目。支持从 GitLab job 链接自动提取日志，或直接分析粘贴的错误日志。
79. **module-bench-diagnosis**: 让 AI 帮你一键诊断 Module Bench 性能测试 Job 的失败原因。
80. **lp-oncall**: LP 车型自动驾驶诊断模块的 Oncall 工程师，内置历史案例知识库
81. **agent-learning-system-skill**: AI Agent 设计的一站式跨 session 记忆 + 持续学习系统。8 条协同 Rules、Engram 语义搜索、结构化学习记录，200+ 条 learnings 实战验证。
82. **metric-design-skill**: AI Agent 编写的数据挖掘 Metric 设计指南。AbstractMetric/Statistic 框架 API 详解、8 层 Tier 结构、Agent 张量格式、坐标转换、新 Metric Checklist。
83. **agent-skill-spotcheck**: 通用数据挖掘抽检 skill。对 mining 结果进行混合抽检（结构化数据引导 + 多帧视觉确认）或快速抽检（单帧），验证挖掘质量。支持对向会车、动态交互、排队、变道、停车、障碍物等场景。50+ 轮迭代验证的 Protocol v14.3-HYBRID 分析框架。v0_t1_new 95%，new/common TP率 91-100%，exist TP率 78-88%。支持生成含 Anyviz 链接+帧数+截图的 Markdown/飞书多维表格报告。
84. **agent-skill-anyviz-viewer**: AI Agent 编写的自动驾驶场景数据可视化 Skill。从 PKL 路径自动生成 Anyviz 链接、支持批量生成、单帧定位和整段播放。
85. **arch-quality-skill**: Arch & Quality Cursor Skill bundle: monorepo build/deploy, OKR planning, log forensics, doc sync, git commit, knowledge capture, plus internal team KB and Feishu project integration.
86. **rebase-helper**: agent驱动的rebase冲突解决skill
87. **pkl-data-operations**: AI Agent 编写的 PKL 数据文件操作 Skill。加载检查、NFS/PFS 路径互转、去重对比、完整性验证、合并输出，处理训练数据 PKL 列表文件。
88. **train-mining-preflight**: Preflight and submit cloud-bound training/mining commands to Volcengine DLC. Catches launcher bugs, checkpoint/config issues, DDP failures, OOM, and missing artifacts. Includes tjob submit workflow with mandatory preflight and human confirmation.
89. **drp-service-troubleshooter**: RP服务问题排查：内置 ES 日志分析（概览、错误分类、链路追踪），可选 Grafana 监控查询，结合代码定位根因。支持日志分析、异步任务、API 状态、健康检查四种场景。
90. **dr-knowledge-agent**: Deeproute 智驾领域知识智能助手。
91. **lcm-memory-cursor**: 基于 Lossless Context Management 的 Cursor Agent 持久化记忆系统，自动分析项目并创建分层记忆文件
92. **infinite-qa-mode**: 让 Cursor Agent 进入持续问答循环，配套 Rule 协议保证每次回复末尾必须调用 AskQuestion，禁止未经请求的 build/compile
93. **sensors-case-analysis**: 自动下载并分析自动驾驶传感器模块日志，支持从飞书 Case 或行程名入手排查问题；当出现全大写事件名或错误码时，结合 sensors 仓库源码做触发条件与调用链分析。
94. **apa-planning-diagnosis**: 诊断APA规划问题根因。支持传入飞书 Case URL 和日志关键词，自动下载日志、提取关键日志、从 GitLab 远程获取代码、分析问题根因并输出诊断结果
95. **feishu-mcp**: 通过飞书 MCP 访问飞书文档、知识库、多维表格和消息。支持读取 Wiki 节点、搜索云文档、获取文档纯文本等操作，含 Token 过期引导。
96. **gitlab-hil-ops**: 通过 GitLab API 管理 HIL 测试台架的 Runner、Job、Pipeline，支持查询状态、触发流水线、运维操作和故障诊断
97. **calib-log-analyze**: 自动分析 adas_online_calibrator 标定日志，快速定位失败原因，生成面向现场人员的诊断报告，支持一键同步到飞书云文档
98. **aes-diagnose**: 输入 case，端到端自动完成数据拉取 → DDL openloop 仿真 → bag 解析 → 日志诊断，结合 aeb 代码库输出 AES/ESA 功能表现的根因分析报告。
99. **drp-diagnosis**: DR Platform 问题诊断分析工具，通过三级路由体系（模块→问题类型→根因排查）定位问题根因并提供修复建议
100. **cbw-bag-analysis**: 分析 bag 文件中的控制数据，支持 CSV 导出和可视化两种方式。
101. **lor-diagnosis-skill**: Lock-on-Road (LOR) 绑路算法的 AI 辅助诊断技能库，配合 Cursor AI 使用，实现从飞书工单到根因定位的自动化诊断流程。
102. **ai-fusa-hil-diagnosis**: 功能安全诊断skill
103. **cbw-get-bag-by-tag**: 根据 tag_instance_id 从仿真平台下载 light_topic bag 文件并合并为单个 bag，同时提取场景信息
104. **searching-similar-issues**: 该skill用于检索用户所需要的飞书缺陷问题，用户可以输入需要的缺陷问题场景描述并附带提供示例问题链接，该skill会深入分析用户需求和示例物体，并通过粗筛+精细筛选出符合用户描述或者和示例问题场景相似的飞书缺陷，并返回这些问题的飞书链接给用户。
105. **diagnose-tracker**: 诊断 control-by-wire Trajectory Tracker 异常进入/退出导致的转角突变，自动定位 BaseTracker::Run() 的 Reset 分支
106. **lua-trigger-dev-assistant**: 指导感知研发完成 Lua Trigger 全流程开发：场景定义、本地调试、Lua算子编写、algo_meta/all_tag/BUILD配置补齐到上线准备
107. **iam-integration**: 帮助开发者检查系统与 DR IAM 平台的对接状态，分析代码找出认证/SSO/鉴权的缺失项，给出补充建议和代码示例
108. **sim-test-frame-analysis**: 分析 Sim Test 的帧级指标并生成结构化报告，支持失败帧率对比与 crash 过滤。
109. **calib-config-generate**: 校验车型参数vehicle-confi中传感器布置等是否正确
110. **cbw-open-loop-sim**: 使用录制的 bag 文件进行开环仿真测试，验证控制算法效果。
111. **vlm-tag-agent-builder**: 在 vlm_tag 智驾诊断系统中创建新的诊断 Agent Pipeline 或审查现有 Agent 的设计质量，覆盖感知、导航、规划等模块
112. **qnx-dev-navigator**: QNX Neutrino RTOS 开发文档和代码导航器，覆盖 QNX 7.1/8.0，自动检索文档、头文件和工具源码
113. **local-run-online-task**: 帮助用户在本地 Docker 中调试 Deelooper 在线任务，自动解析链接、获取配置、处理 Artifacts、生成 Docker 命令
114. **data-progress-query**: 从飞书项目拉取「感知数据专项」和「感知单批数据生产」工作项，结合 Deelooper执行数据查询 URI 统计，汇总数据专项进度。
115. **aeb-config-generator**: AEB 策略与配置智能助手：查询策略/配置含义与关联字段，按配置名生成最小 Jsonnet overlay；提供脚本与中间数据源，可脱离 Skill 直接使用。
116. **deelooper-board-analytics**: Deelooper看板数据分析助手目前支持通过在cursor中用自然语言实现数空看板的数据分析
117. **tpm-daily-focus**: 为 TPM 提供每日跟进支持：从飞书任务与群聊汇总待办、需沟通人、按项目划分的进展与风险，生成按日期分段的 Markdown，便于粘贴到同一份项目进展文档。
118. **config-service**: 用于使用config_service接口识别车型，并判断各feature功能开关状态
119. **avm-log-analyze-skill**: 自动分析 perception_avm 环视系统日志，快速定位初始化失败、图像缺失、运行异常等问题，生成面向现场人员的诊断报告
120. **cbw-new-vehicle-create**: 在 control-by-wire 模块中创建新车型完整骨架，可选同步适配其他依赖仓库。
121. **aeb-trajcaching-tag-analysis**: 分析 trajcaching pptag-mining 输出的 AEB 场景分类 log，自动判断分类准确性并生成 Markdown 报告，识别 CPLA/CBLA 误触发等常见 BUG。
122. **team-shared-learning**: AI Agent 设计的团队知识共享方案。通过共享存储 + symlink 让所有 Agent 共建 learnings 知识库，支持跨成员搜索。
123. **simulation-local**: simulation相关skill，主要是ddl相关
124. **drp-flow**: 在 DR Platform 中快速发起各种流程，支持模块-流程的查询链路，帮助用户快速定位并执行目标流程
125. **model-debug-workflow**: 验证 pp_thanos 模型结构或损失函数修改的可用性。流程：代码审查 → 配置开关 → 完整训练验证 → loss 观察 → 验证结果输出 → 可选复制到 experment。
126. **production-issue-triage**: 产线通用性问题排查，待后续更新
127. **mining-postprocess**: AI Agent 编写的数据挖掘后处理筛选 Skill。JSONL→Parquet 转换、DuckDB SQL 查询、三层 Tiered 筛选、NFS/PFS 路径转换、去重、PKL 输出。
128. **parking-planning-process**: 快速梳理泊车规划相关流程并定位问题原因，帮助研发高效排查与沟通。
129. **parallel-review-loop**: 用多路并行 reviewer 做循环式 review：共享上下文 → focused review → synthesis 收口。支持主题化和场景化两种 reviewer 模式。
130. **repo-documentation-builder**: 为代码仓库建立完整文档体系：渐进式披露的文档结构、Cursor Rule 自动维护、交叉链接验证。
131. **auto-cot-analyzer**: 在预定义的大思维链框架下，自动读取现有项目代码分支，完成诊断日志自动补全与脚本解析。适用于需要对复杂系统进行逐层推理诊断的场景，支持 AI 自动填充细节推理链路。
132. **safety-evaluation-pipeline**: 暂无描述
133. **aeb-data-magic**: AEB数据处理、分析工具
134. **aeb-bringup-quickstart**: 指导AEB仓库在dev_master上开合入分支、按车企与车型代码增量目录、完成配置注册并推送创建指向dev_master的GitLab MR。
135. **memos-memory**: 基于 MemOS Cloud 的 Cursor Agent 持久化记忆。通过 MCP 连接 MemOS Cloud API，实现跨会话上下文记忆，支持 LCM 结构化 Session 格式写入。
136. **cursor-market-quickstart**: 用清单化步骤说明如何从新建 GitLab 仓库到打 Tag 发布 Cursor Skill，并附本地校验与常见问题。 多 Agent 协作的后端自动化开发流水线，支持从需求描述到代码提交的全流程自动化：PM 设计 → 开发 → CodeReview → 测试 → QA 验收 → 提交

