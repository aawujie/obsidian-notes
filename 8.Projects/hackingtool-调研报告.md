# HackingTool 项目调研报告

> **项目地址**: https://github.com/Z4nzu/hackingtool  
> **调研日期**: 2026-04-22  
> **调研人**: 温境城

---

## 一、项目概览

| 指标 | 数据 |
|------|------|
| **Stars** | 58,890 |
| **Forks** | 6,640 |
| **Watchers** | 1,299 |
| **Open Issues** | 58 |
| **语言** | Python |
| **协议** | MIT License |
| **创建时间** | 2020-04-11 |
| **最近更新** | 2026-04-22 |
| **最近推送** | 2026-03-15 |
| **仓库大小** | 2,486 KB |

**定位**：ALL IN ONE 渗透测试工具集，面向安全从业者的菜单式工具聚合器。类似 Kali Linux 的"命令行版"，将 185+ 个安全工具按攻击阶段分类，提供统一安装和调用入口。

---

## 二、核心特性

| 特性 | 说明 |
|------|------|
| **Python 3.10+** | 全面迁移到现代语法，已移除所有 Python 2 代码 |
| **OS 感知菜单** | macOS 自动隐藏 Linux-only 工具，跨平台适配 |
| **185+ 工具** | 6 大类 20 子类，覆盖渗透测试全流程 |
| **搜索功能** | `/` 键按名称/描述/关键词搜索所有工具 |
| **标签过滤** | `t` 键按 19 个标签过滤（osint, web, c2, cloud, mobile...） |
| **智能推荐** | `r` 键输入场景描述，自动推荐匹配工具 |
| **安装状态** | ✔/✘ 标识每个工具是否已安装 |
| **批量安装** | 每个分类 Option 97 一键批量安装 |
| **智能更新** | 自动检测 git pull / pip upgrade / go install |
| **Docker 支持** | 本地构建镜像，不依赖外部未验证镜像 |
| **一键安装** | `curl -sSL .../install.sh | sudo bash` |

---

## 三、工具分类（20 个类别）

| # | 类别 | 工具数 | 核心工具 |
|---|------|--------|----------|
| 1 | 🛡 匿名隐藏 | 2 | Anonsurf, Multitor |
| 2 | 🔍 信息收集 | 26 | Nmap, theHarvester, Amass, Masscan, RustScan, SpiderFoot, Subfinder, httpx |
| 3 | 📚 字典生成 | 7 | Cupp, Hashcat, John the Ripper, haiti |
| 4 | 📶 无线攻击 | 13 | WiFi-Pumpkin, Fluxion, Wifite, Bettercap, Airgeddon |
| 5 | 🧩 SQL注入 | 7 | Sqlmap, NoSqlMap, DSSS, SQLScan |
| 6 | 🎣 钓鱼攻击 | 17 | Setoolkit, SocialFish, Evilginx3, PyPhisher, HiddenEye, BlackEye |
| 7 | 🌐 Web攻击 | 20 | Nuclei, ffuf, Feroxbuster, Nikto, OWASP ZAP, Katana, Gobuster, Dirsearch, Arjun, Caido, mitmproxy |
| 8 | 🔧 后渗透 | 10 | pwncat-cs, Sliver, Havoc, PEASS-ng, Ligolo-ng, Chisel, Evil-WinRM, Mythic |
| 9 | 🕵 取证分析 | 8 | Autopsy, Wireshark, Volatility 3, Binwalk, pspy |
| 10 | 📦 Payload生成 | 8 | TheFatRat, MSFvenom, Venom, Spycam, Mob-Droid |
| 11 | 🧰 Exploit框架 | 4 | RouterSploit, WebSploit, Commix |
| 12 | 🔁 逆向工程 | 5 | Ghidra, Radare2, JadX, Androguard, Apk2Gold |
| 13 | ⚡ DDoS攻击 | 5 | SlowLoris, UFOnet, Asyncrone |
| 14 | 🖥 RAT | 1 | Stitch |
| 15 | 💥 XSS攻击 | 9 | — |
| 16 | 🖼 隐写术 | 4 | — |
| 17 | 🏢 Active Directory | 6 | 新增类别 |
| 18 | ☁ 云安全 | 4 | 新增类别 |
| 19 | 📱 移动安全 | 3 | 新增类别 |
| 20 | ✨ 其他工具 | 24 | — |

---

## 四、架构与实现

### 4.1 技术栈
- **核心语言**: Python 3.10+
- **交互方式**: 终端菜单式 TUI（类似 Kali Linux 的工具菜单）
- **安装方式**: 一键 curl / Docker / git clone
- **依赖管理**: 各工具独立安装（git clone + pip install / go install）

### 4.2 工作流
```
用户选择类别 → 子菜单选择工具 → 
  → 检查安装状态 → 未安装则自动安装 → 运行工具
```

### 4.3 新版本改进（v3+）
- 移除所有 Python 2 遗留代码
- 新增搜索、标签、推荐功能
- 新增 Active Directory / Cloud Security / Mobile Security 三大类别
- 智能更新检测（git/pip/go 三种方式）
- Docker 本地构建支持

---

## 五、优势分析

### 5.1 亮点
1. **一站式聚合**：185+ 工具统一入口，免逐一搜索和安装
2. **社区热度高**：58K+ Stars，渗透测试工具类 GitHub 项目 Top 3
3. **持续维护**：2020 年创建至今仍在更新（最近推送 2026-03-15）
4. **智能推荐**：场景化推荐降低了新手选工具的门槛
5. **安装状态可视**：✔/✘ 标识避免了"装了没装"的困惑
6. **批量安装**：分类 Option 97 一键安装，适合快速搭建测试环境
7. **跨平台适配**：macOS 自动过滤不兼容工具
8. **MIT 协议**：商业友好，允许修改和分发

### 5.2 适用场景
- **红队演练**：快速搭建渗透测试工具链
- **CTF 比赛**：一键安装常用比赛工具
- **安全教学**：学生可快速获得完整工具集
- **自动化测试**：批量安装后集成到 CI/CD 安全扫描流程

---

## 六、风险与局限

### 6.1 安全风险
| 风险 | 等级 | 说明 |
|------|------|------|
| **工具来源不可控** | ⚠️ 高 | 185+ 工具来自不同作者，部分已停止维护，存在供应链风险 |
| **一键 root 安装** | ⚠️ 高 | `curl | sudo bash` 无审查直接执行，可能被劫持 |
| **DDoS/RAT/钓鱼工具** | ⚠️ 中 | 包含明显恶意用途工具（SlowLoris, UFOnet, RAT），需严格管控使用场景 |
| **工具版本不统一** | ⚠️ 中 | 各工具独立 git clone，版本由上游控制，可能引入不兼容变更 |

### 6.2 技术局限
| 局限 | 说明 |
|------|------|
| **非专业框架** | 是工具聚合器而非编排框架，工具间无联动能力 |
| **安装质量参差** | 部分工具依赖复杂，批量安装可能失败 |
| **缺乏沙箱** | 工具直接运行在主机环境，无隔离机制 |
| **更新机制简单** | 仅 git pull / pip upgrade，无版本锁定 |
| **58 个 Open Issues** | 安装失败、兼容性、工具失效等问题较多 |

### 6.3 合规风险
- 包含 DDoS 攻击、钓鱼、RAT 等工具，**在中国境内未经授权使用属于违法行为**
- 企业使用需严格限制在授权渗透测试范围内
- 需配合安全合规流程（授权书、范围界定、结果保密）

---

## 七、竞品对比

| 项目 | Stars | 工具数 | 特色 | 定位 |
|------|-------|--------|------|------|
| **hackingtool** | 58K | 185+ | 菜单式 TUI，搜索+推荐 | 渗透测试工具聚合器 |
| **Katana** | 1.2K | — | 自动化爬取+侦察 | Web 侦察框架 |
| **Osmedeus** | 4.5K | — | 自动化侦察工作流 | 侦察自动化 |
| **Penetration-Testing-Tools** | 3K | 100+ | 工具清单文档 | 工具索引（不安装） |
| **Kali Linux** | — | 600+ | 完整 OS | 专业渗透测试发行版 |

**定位差异**：hackingtool 是"轻量版 Kali"，适合不想装完整 OS 但需要工具集的场景。

---

## 八、评估结论

### 总评：⭐⭐⭐⭐ (4/5)

**推荐使用场景**：
- ✅ 安全团队搭建渗透测试环境
- ✅ CTF 参赛者快速部署工具
- ✅ 安全研究人员工具试用

**不推荐场景**：
- ❌ 生产环境直接部署
- ❌ 未经授权的攻击行为
- ❌ 需要工具编排和自动化的专业红队

**建议**：
1. 优先在 Docker 环境中使用，避免直接安装到主机
2. 仅安装需要的分类，不要批量全装
3. 使用前审查每个工具的来源和版本
4. 严格遵守"仅用于授权渗透测试"原则
5. 企业环境建议配合合规流程使用

---

*报告完毕*