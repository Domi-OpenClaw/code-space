# 系统架构文档

> 重要更新：2026-04-28 确立三層體系，架構固化

---

## 核心定位

OpenClaw 技能系统采用三层架构，各自独立、互不混淆：

| 层级 | 简称 | 全称 | 目录 | 定位 |
|-----|------|------|------|------|
| Business Capability Framework | **BCF** | 业务专家层 | `workspace/skills/` | B端售前、电力市场、情报系统等业务能力 |
| Dynamic Capability System | **DCS** | 通用工具层 | `~/.openclaw/skills/` | 搜索路由、图像识别、邮件、图床等通用工具 |
| Personal Private Files | **PPF** | 个人事务层 | `~/.openclaw/ppf/` | 基金盯盘、头条运营等私人事务 |

---

## 目录结构

```
~/.openclaw/
├── workspace/                    # 工作区
│   ├── skills/                  # BCF 技能（13个）
│   │   ├── bcf-meta/
│   │   ├── power-market-intel/
│   │   ├── energy-news-monitor/
│   │   ├── pre-sales-workflow/
│   │   ├── business-research/
│   │   ├── knowledge-management/
│   │   ├── knowledge-graph/
│   │   ├── wechat-official-accounts-scan/
│   │   ├── bid-intel-collection/
│   │   ├── power-retail-analyzer/
│   │   ├── Power-Trading-Rule-Analysis/
│   │   ├── new-power-subjects-rule/
│   │   └── ...
│   ├── memory/                  # 工作记忆
│   ├── knowledge/              # 工作知识库
│   ├── AGENTS.md               # 核心原则
│   ├── ARCHITECTURE.md         # 本文档
│   └── ...
│
├── skills/                      # DCS 技能（通用工具）
│   ├── search-routing/         # 统一搜索路由
│   ├── img-router/             # 图片生成聚合
│   ├── image-minimax/          # 图像理解
│   ├── github-imgbed/          # GitHub图床
│   ├── github-file-storage/    # GitHub文件库
│   ├── tencent-meeting-mcp/    # 腾讯会议
│   ├── send-email-skill/       # 邮件发送
│   ├── openclaw-backup-email/  # 备份工具
│   ├── domi-system-tuner/      # 系统优化
│   └── ...
│
└── pf/                         # PPF 个人事务
    ├── SKILL.md                # PPF管理体系
    ├── MEMORY.md               # PPF记忆
    └── skills/
        ├── fund-monitor/       # 基金盯盘
        └── ...
```

---

## 注册表

| 注册表文件 | 对应层级 | 路径 |
|------------|---------|------|
| `business__skills.md` | BCF | `workspace/` |
| `utility-skills.md` | DCS | `workspace/` |
| `ppf/SKILL.md` | PPF | `~/.openclaw/ppf/` |

---

## 备份策略

| 数据类型 | 备份位置 |
|---------|---------|
| 全量备份 + 文件归档 | **Gitee** |
| 图床 + 代码库 | **GitHub** |

> 备份架构固化于 2026-04-28，不可混用

---

## 触发规则

- 用户提及业务关键词 → 激活 BCF skill
- 用户提及私人事务关键词（基金、头条） → 激活 PPF skill
- 通用工具（搜索、图像、邮件） → DCS skill，可被任意层调用

---

## 架构原则

1. **目录即身份**：`workspace/skills/` 里的 skill 必然是 BCF，绝不放入个人技能
2. **数据隔离**：PPF 的数据在 `ppf/skills/xxx/memory/`，不进入 workspace 知识体系
3. **注册表即权威**：三层各自的注册表是唯一事实来源，路径必须与之一一对应
4. **备份分离**：Gitee 和 GitHub 各司其职，不混用

---

*v1.0 | 2026-04-28 | 架构固化，三层体系正式确立*
