# self.md — Domi 核心配置

## 基本原则（红线）

1. **保密红线** — 具体工作/Token/Key/个人信息绝对不对外分享
2. **配置文件红线** — openclaw.json 绝对不能改，其他配置文件改之前必须先给用户确认
3. **工具共用，数据隔离** — skills 各通道共用，自己的数据写到自己的目录
4. **任务分流铁律** — 评估 > 5 秒的复杂任务立即放 subagent，不阻塞对话
5. **重要工作单独记忆** — 工作待办记 BCF 章节，系统运维记 DCS 章节，不混用
6. **备份是生存本能（2026-04-24 事故后固化）** — 每次会话结束前确认核心文件已备份、TinyDB已写入；不相信"上次备份应该还在"，每次验证备份存在且可用

---

## 🔥 BCF 重要工作待办（业务层）

> 业务项目、重要决策、售前工作、客户跟进
> **原则**：只记重要事项，不记过程；完成后立即移除或归档

**当前项目：**

| 项目 | 阶段 | 优先级 | 备注 |
|------|------|--------|------|
| **power-commercial-api**（电力现货价格预测API） | ✅ 已上线 | 🔴 高 | `http://101.201.232.176:10129`，systemd开机自启，Key: sk-test-power-2026 |
| **new-energy-api**（新能源消纳预测API） | ✅ 已上线 | 🔴 高 | `http://101.201.232.176:10130`，systemd开机自启，Dashboard已部署 |
| 储能运营商价格预测API | ✅ 开发完成 | 🔴 高 | 28省覆盖，正式现货+试运行 |

**BCF 层纳管要求：**
- power-commercial-api + new-energy-api 均为业务产品
- API守护：心跳每30分钟检查，宕机自动重启（`workspace/scripts/api-watchdog.sh`）
- 日志：`workspace/memory/api-watchdog.log`
- 健康状态查询：`curl http://127.0.0.1:10129/health` / `10130/health`

**OpenClaw Cron 修复记录（2026-04-26）：**
- 新能源气象采集（08:00）：channel缺省 → 已加 `channel: dingtalk`
- 煤炭每日采集（08:30）：timeout 120s不够 → 已改为 300s
- 煤炭BSPI每周（周二/五09:00）：timeout 60s不够 → 已改为 300s
- 知识图谱每日同步（01:30）：缺 `bestEffort: true` → 已添加（推送失败不中断任务）

**pre-sales-workflow 完善计划：**
- 目标：8个 Tool 至少一次真实项目验证
- 状态：bd__customer_visit 已实战验证，其余待安排

---

## ⚙️ DCS 系统待办（日常运维）

> 系统稳定运行、技能健康、环境配置
> **原则**：常态监控，不占用BCF注意力；问题解决后移除

**💾 DCS待办：**
- 备份检查已内置心跳（HEARTBEAT.md v10.1），无需单独跟进

**服务状态（仅日常杂项，业务服务见BCF）：**
- rsshub-scan：公众号RSS（端口4000）
- rsshub-news：能源资讯（端口4001）

~~TraeClaw 集成进度：~~
~~- 服务器端：✅ trae-ide v0.3.0 已装，trae_status 可用~~

---

## 📁 PPF 个人事务

> PPF（Personal Private Files）= 个人技能体系，独立于 BCF/DCS
> 目录：`~/.openclaw/ppf/`
> **原则**：个人敏感数据（基金/保险/银行卡等）不存服务器、不写知识库，仅对话内处理

**个人技能：**
- fund-monitor（基金盯盘）
- toutiao-ops（头条运营，程序在 `~/.local/bin/toutiao-ops`）

**个人数据处理原则（2026-04-28 固化）：**
- 收到敏感截图 → 读取后立即删除原始文件
- 不写入 memory / knowledge / 任何知识库文件
- 仅在对话内呈现结果

