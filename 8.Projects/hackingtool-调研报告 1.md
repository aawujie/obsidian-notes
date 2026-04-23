# Hackingtool 项目调研报告

> 项目地址：https://github.com/Z4nzu/hackingtool
> 调研日期：2026-04-22

## 一、项目概览

| 指标 | 值 |
|------|-----|
| **Stars** | 58,952 |
| **Forks** | 6,661 |
| **Watchers** | 1,300 |
| **语言** | Python |
| **许可证** | MIT |
| **创建时间** | 2020-04-11 |
| **最新推送** | 2026-03-15 |
| **Open Issues** | 58 |
| **主要贡献者** | Z4nzu (121 commits), cclauss (85), Greatest125 (69) |

**定位**：ALL IN ONE Hacking Tool — 渗透测试/安全审计工具合集，面向安全研究人员和红队。

## 二、功能架构

### 20 个工具分类，185+ 工具

| # | 分类 | 工具数 | 说明 |
|---|------|--------|------|
| 1 | 🛡 Anonymously Hiding | 2 | 匿名 Surf, Multitor |
| 2 | 🔍 Information Gathering | 26 | nmap, theHarvester, Amass, Masscan, Shodan, ReconSpider 等 |
| 3 | 📚 Wordlist Generator | 7 | Cupp, Hashcat, John, Goblin 等 |
| 4 | 📶 Wireless Attack | 13 | WiFi-Pumpkin, Fluxion, Bettercap, Airgeddon 等 |
| 5 | 🧩 SQL Injection | 7 | Sqlmap, NoSqlMap, DSSS 等 |
| 6 | 🎣 Phishing Attack | 17 | Setoolkit, SocialFish, Evilginx3, BlackEye 等 |
| 7 | 🌐 Web Attack | 20 | Nuclei, ffuf, OWASP ZAP, Nikto, Katana 等 |
| 8 | 🔧 Post Exploitation | 10 | pwncat, Sliver, Havoc, PEASS-ng, Chisel 等 |
| 9 | 🕵 Forensics | 8 | Wireshark, Volatility 3, Binwalk, pspy 等 |
| 10 | 📦 Payload Creation | 8 | FatRat, Venom, MSFvenom 等 |
| 11 | 🧰 Exploit Framework | 4 | RouterSploit, WebSploit, Commix 等 |
| 12 | 🔁 Reverse Engineering | 5 | Ghidra, Radare2, Androguard 等 |
| 13 | ⚡ DDOS Attack | 5 | SlowLoris, UFOnet, GoldenEye 等 |
| 14 | 🖥 RAT | 1 | Stitch |
| 15 | 💥 XSS Attack | 9 | DalFox, XSStrike, XSpear 等 |
| 16 | 🖼 Steganography | 4 | SteganoHide, StegoCracker 等 |
| 17 | 🏢 Active Directory | 6 | BloodHound, NetExec, Impacket, Certipy 等 |
| 18 | ☁ Cloud Security | 4 | Prowler, ScoutSuite, Pacu, Trivy |
| 19 | 📱 Mobile Security | 3 | MobSF, Frida, Objection |
| 20 | ✨ Other Tools | 24 | Sherlock, Hash Buster, Gospider 等 |

### 新版 v2.0.0 特性（2026-03-15）

- **Python 3.10+**：移除所有 Python 2 代码
- **OS 感知菜单**：Linux 工具在 macOS 自动隐藏
- **搜索功能**：`/` 搜索工具名/描述/关键词
- **Tag 过滤**：`t` 按 19 个标签筛选（osint, web, c2, cloud, mobile...）
- **推荐系统**：`r` 输入意图 → 推荐相关工具
- **安装状态**：✔/✘ 显示每个工具是否已安装
- **批量安装**：97 一键安装分类下所有工具
- **智能更新**：自动检测 git pull / pip upgrade / go install
- **Docker 支持**：本地构建，无未验证外部镜像

## 三、安装方式

```bash
# 一行安装
curl -sSL https://raw.githubusercontent.com/Z4nzu/hackingtool/master/install.sh | sudo bash

# 手动安装
git clone https://github.com/Z4nzu/hackingtool.git
cd hackingtool
sudo python3 install.py
hackingtool

# Docker
docker build -t hackingtool .
docker run -it --rm hackingtool
```

### 依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| Python | 3.10+ | 核心 |
| Go | 1.21+ | nuclei, ffuf, amass, httpx, katana, dalfox, gobuster, subfinder |
| Ruby | any | haiti, evil-winrm |
| Docker | any | Mythic, MobSF（可选） |

## 四、项目活跃度分析

| 维度 | 评价 |
|------|------|
| **社区热度** | ⭐⭐⭐⭐⭐ (58k stars，安全工具类排名前列) |
| **维护频率** | ⭐⭐⭐⭐ (2026-03-15 v2.0.0 大更新) |
| **Issue 处理** | ⭐⭐⭐ (58 open issues，响应不太及时) |
| **代码质量** | ⭐⭐⭐ (Python 3.10+，有 PR 模板和 CI) |
| **文档完善** | ⭐⭐⭐⭐⭐ (README 详尽，每个工具有链接和描述) |

### 近期重要更新

- **2026-03-15**：v2.0.0 大重构 — 新增 35 个工具，3 个新分类（AD、Cloud、Mobile），Rich UI 菜单
- **2025-10-14**：Rich UI 菜单改进
- **2025-03-03**：社区贡献合并

## 五、与同类项目对比

| 项目 | Stars | 工具数 | 语言 | 特点 |
|------|-------|--------|------|------|
| **hackingtool** | 58.9k | 185+ | Python | 全品类覆盖，搜索/推荐/标签 |
| **Katana** (onyx-point) | 1.2k | 50+ | Go | 轻量，专注自动化攻击链 |
| **Penetration-Testing-Stuff** | 6.5k | - | - | 资源合集，非工具框架 |
| **Cybersecurity-Playbook** | 3.5k | - | - | 方法论，非工具 |

**hackingtool 的差异化**：
1. **交互式菜单系统**（不是简单脚本列表）
2. **搜索+推荐+标签**（智能推荐工具）
3. **安装状态追踪**（✔/✘ 标记）
4. **批量安装+智能更新**（运维友好）
5. **Docker 支持**（隔离安全环境）

## 六、适用场景

| 场景 | 适合度 |
|------|--------|
| **安全审计/渗透测试** | ⭐⭐⭐⭐⭐ |
| **CTF 比赛** | ⭐⭐⭐⭐ |
| **红队演练** | ⭐⭐⭐⭐⭐ |
| **安全教学/实验** | ⭐⭐⭐⭐ |
| **企业合规检测** | ⭐⭐⭐ |
| **日常安全运维** | ⭐⭐⭐⭐ |

## 七、风险与注意事项

1. **法律合规**：仅用于授权安全测试，未授权使用违法
2. **DDoS 工具**：含 SlowLoris、UFOnet 等攻击工具，使用需谨慎
3. **钓鱼工具**：含 Setoolkit、Evilginx3 等，需严格授权场景
4. **一键安装**：`curl | sudo bash` 存在供应链风险
5. **工具来源**：185+ 工具来自不同作者，质量参差
6. **权限要求**：部分工具需要 root 权限

## 八、结论

**hackingtool 是目前最全面的渗透测试工具合集项目**：

- ✅ 58k+ Stars，社区认可度高
- ✅ v2.0.0 大重构，代码现代化
- ✅ 20 个分类覆盖完整攻击链
- ✅ 搜索/推荐/标签提升使用效率
- ✅ Docker 支持安全隔离
- ⚠️ 含攻击性工具（DDoS、钓鱼），需授权使用
- ⚠️ 一行安装存在供应链风险

**推荐用途**：安全审计、渗透测试、CTF、安全教学实验。**严禁未授权使用**。

---

> 调研人：温境城 | 日期：2026-04-22