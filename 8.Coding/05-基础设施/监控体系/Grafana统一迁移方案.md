# Grafana 统一迁移方案

> 来源：飞书文档 https://rqk9rsooi4.feishu.cn/wiki/C2J7wal5Uiv4WrkLRe2cGhtOnoe
> 同步时间：2026-03-30

---

## 背景

团队有两套 Grafana 分别部署在两人的笔记本上，不利于长期维护：

| 实例 | 地址 | 用途 | 数据源 |
|------|------|------|--------|
| Grafana-Pipeline | http://10.24.97.220:13000 | Pipeline 运行状况、趋势、轮值 Owner | MySQL (pipeline_db) |
| Grafana-Monitor | http://10.24.99.65:3000 | GitLab Runner 监控、HIL Job 历史、告警 | PostgreSQL + Prometheus + SQLite(弃用) |

**目标**：迁移到一台稳定的 runner x86 机器，统一数据源为 PostgreSQL，通过域名访问。

---

## 新 Grafana 访问信息

| 项目 | 值 |
|------|-----|
| 地址 | http://10.24.12.204（iKuai 路由器 80→3000 端口转发）|
| 域名 | http://hil-grafana.deeproute.ai（需配 hosts）|
| 用户 | admin |
| 密码 | hil_grafana_2026 |
| Grafana 版本 | 12.4.1 |

### hosts 配置

```bash
# macOS / Linux
sudo sh -c 'echo "10.24.12.204 hil-grafana.deeproute.ai" >> /etc/hosts'
```

---

## 进度总览

- ✅ **Phase 1**：部署新 Grafana（已完成）
- ✅ **Phase 2**：数据迁移 MySQL → PostgreSQL（已完成）
- ✅ **Phase 3**：Monitor 迁移 + 验证（已完成）
- ⏳ **Phase 4**：切换 + 旧系统下线（待执行，需稳定运行 ≥1 周）

---

## 部署位置（P03-2: 10.24.12.204）

```
/home/gitlab-runner/grafana-unified/      # Grafana + PG + Prometheus 容器栈
├── docker-compose.yml
├── prometheus.yml
├── grafana/provisioning/datasources/datasources.yml
└── postgres/init/01-schema.sql

/home/gitlab-runner/hil-grafana-sync/     # 同步服务
├── sync_to_pg.py                   # Pipeline: GitLab API → PostgreSQL 同步
├── sync_monitor_incremental.py     # Monitor: Grafana API → PostgreSQL 增量同步
├── sync_server_pg.py               # HTTP 触发服务 (:9123)
└── requirements.txt

/home/gitlab-runner/gitlab-runner-exporter.py  # Runner 指标 exporter (:9253)
```

---

## Crontab（P03-2）

```bash
# Pipeline 数据同步，每 2 小时
0 */2 * * * cd ~/hil-grafana-sync && source .env && python3 sync_to_pg.py >> sync_cron.log 2>&1

# Monitor 数据增量同步，每 5 分钟
*/5 * * * * cd ~/hil-grafana-sync && python3 sync_monitor_incremental.py >> sync_monitor.log 2>&1

# gitlab-runner-exporter 开机自启
@reboot nohup python3 ~/gitlab-runner-exporter.py > ~/runner_exporter.log 2>&1 &
```

---

## 数据一致性验证结果

| 数据 | 旧系统 | 新系统 | 状态 |
|------|--------|--------|------|
| pipeline_runs | 4,152 | 4,116 | 预期差异（同步周期内新增）|
| job_runs | 63,598 | 63,329 | 预期差异 |
| expected_triggers | 4,616 | 4,582 | 预期差异 |
| job_stages | 4,258 | 4,259 | 一致 |
| runner_alerts | 178 | 178 | 完全一致 |
| Prometheus targets | 3 | 3 | 全部 up |

---

## Phase 4 待办

- [ ] 确认新系统稳定运行 ≥1 周
- [ ] 通知团队配置 hosts（`10.24.12.204 hil-grafana.deeproute.ai`）
- [ ] 旧同步服务停止
- [ ] 保留旧系统 2 周作为回退
- [ ] 正式关闭旧 Grafana（10.24.97.220:13000 和 10.24.99.65:3000）
