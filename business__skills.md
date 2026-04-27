# 业务专家 Skill 注册清单

> 版本：v1.8
> 归属：BCF（Business Capability Framework）独立管理
> 定位：业务专家型 Skill，按 SKILL-GUIDE 标准构建，六层架构不全的不归档

> BCF = Business Capability Framework，业务专家层。
> 与 DCS 的关系：DCS 提供系统运行保障，BCF 专注业务能力建设。

---

## BCF Skill 完整清单

### 🏭 BCF-Meta（1个）

| 名称 | 路径 | 功能 | 来源 | 七维 | 上次检查 |
|------|------|------|------|------|---------|
| bcf-meta | workspace/skills/bcf-meta/ | BCF Skill工厂（构建/质检/升级/记忆/图谱） | **自建** | ✅4.57 | 2026-04-09 |

### 📰 内容运营（1个）

| 名称 | 路径 | 功能 | 来源 | 纳管 | 上次检查 |
|------|------|------|------|------|---------|


### 💰 数据要素（1个）

| 名称 | 路径 | 功能 | 来源 | 纳管 | 上次检查 |
|------|------|------|------|------|---------|
| data-market-insight | workspace/skills/data-market-insight/ | 数据要素市场情报系统（六层完整v2.1) | **自建** | ✅4.13 | 2026-04-13 |

### ⚡ 电力市场（5个）

| 名称 | 路径 | 功能 | 来源 | 纳管 | 上次检查 |
|------|------|------|------|------|---------|
| power-market-intel | ~/.openclaw/skills/power-market-intel/ | 电力市场情报系统（5Agent协作） | **自建** | ✅六层完整 | 2026-04-11 |
| power-predict-mcp | workspace/servers/power-predict-mcp/ | 20省电价预测MCP（天气+煤价+负荷，P10/P50/P90分位数） | **自建** | ✅初建 | 2026-04-17 |
| energy-news-monitor | openclaw/skills/energy-news-monitor/ | 能源新闻采集（5网站→memory文件，01:30 cron） | **自建** | ✅六层完整 | 2026-04-11 |
| wechat-official-accounts-scan | openclaw/skills/wechat-official-accounts-scan/ | 公众号RSS采集（9个公众号，00:30 cron） | **自建** | ✅六层完整 | 2026-04-11 |
| Power-Trading-Rule-Analysis | ~/.openclaw/skills/Power-Trading-Rule-Analysis/ | 10大规则模块+8个独立Tool，省级专项报告+跨省对比 | **自建** | ✅六层完整+L0 memory | 2026-04-23 |
| new-power-subjects-rule | ~/.openclaw/skills/new-power-subjects-rule/ | 4类新型主体（独立储能/虚拟电厂/微电网/充电设施）规则解析 | **自建** | ✅六层完整+L0 memory | 2026-04-23 |

### 📅 会议办公（1个）

| 名称 | 路径 | 功能 | 来源 | 纳管 | 上次检查 |
|------|------|------|------|------|---------|
| tencent-meeting-mcp | openclaw/skills/tencent-meeting-mcp/ | 腾讯会议MCP（查会/创会/参会人/录制/转写） | 外部下载 | BCF纳管 | 2026-04-11 |

### 📋 售前全流程（1个）

| 名称 | 路径 | 功能 | 来源 | 纳管 | 上次检查 |
|------|------|------|------|------|---------|
| pre-sales-workflow | openclaw/skills/pre-sales-workflow/ | 售前全流程（BD拜访/SA汇报/立项/标前准备，8个Tool） | **自建** | ✅4.15 | 2026-04-10 |

### 🔍 业务研究（1个）

| 名称 | 路径 | 功能 | 来源 | 纳管 | 上次检查 |
|------|------|------|------|------|---------|
| business-research | openclaw/skills/business-research/ | 业务研究商业分析（六层架构，方法论+工具双定位） | **自建** | ✅六层完整 | 2026-04-23 |

### 📢 招投标情报（1个）

| 名称 | 路径 | 功能 | 来源 | 纳管 | 上次检查 |
|------|------|------|------|------|---------|
| bid-intel-collection | openclaw/skills/bid-intel-collection/ | 招投标情报采集（数据要素+新能源，每日2次） | **自建** | ✅初建 | 2026-04-16 |

### 🗄️ 知识管理（1个）

| 名称 | 路径 | 功能 | 来源 | 纳管 | 上次检查 |
|------|------|------|------|------|---------|
| knowledge-management | workspace/skills/knowledge-management/ | 统一知识管理体系（订阅BCF数据源→清洗→归档→图谱同步） | **自建** | ✅六层完整 | 2026-04-14 |

_（knowledge-graph 已迁移至 PersonalFiles 个人技能体系）_

---

## 构建标准（SKILL-GUIDE v1.0）

### 六层架构（必须）
- L1: SKILL.md（主文档）
- L2: long_term_memory.md（长期记忆）
- L3: examples/（范例库）
- L4: tools/（工具层）
- L5: scripts/（脚本层）
- L6: templates/（模板层）

### 四步强制工作流（必须）
1. 生成前检查 → 2. 按Tool生成 → 3. 生成后检查 → 4. 发送前自检

### 七维成熟度（目标 ≥4.0/5.0）
- 模块化 / 记忆机制 / 工作流约束 / 质量量化 / 可复用性 / 持续改进 / 文档完整性

### 三大红线（严禁）
- 数据真实性 / 完整性 / 准确性

---

## 状态说明

| 状态 | 含义 |
|------|------|
| ✅ 正常 | 正常运转，六层架构完整 |
| ⚠️ 异常 | 检查发现异常，已通知小海哥 |
| 🔧 补层中 | 正在补全缺失的层级 |
| ⏸️ 停用 | 已停用，等待卸载 |

---

## 统计

| 类别 | 数量 | 其中自建 |
|------|------|---------|
| BCF-Meta | 1 | 1 |
| 内容运营 | 1 | 0 |
| 数据要素 | 1 | 1 |
| 电力市场 | 5 | 4 |
| 会议办公 | 1 | 0 |
| 售前全流程 | 1 | 1 |
| 业务研究 | 1 | 1 |
| 招投标情报 | 1 | 1 |
| 知识管理 | 2 | 2 |
| **合计** | **15** | **13自建** |

---

_最后更新：2026-04-23_


