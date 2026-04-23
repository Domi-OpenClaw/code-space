---
name: new-power-subjects-rule
description: 电力市场新型主体规则解析。聚焦独立储能、虚拟电厂、智能微电网、电动汽车充电设施运营商 4 类主体，面向产品经理、售前、销售及电力行业研究者，提供进阶专业级规则解析。覆盖国家 + 全部省份政策、电网公司"两细则"、电力交易中心规则。支持关键词查询 + 关联引导 + 专项报告输出。
metadata:
  version: 2.2.0
  created: 2026-03-11
  updated: 2026-03-27 11:10
  based_on: 省级范例库方法（移植自 Power-Trading-Rule-Analysis）+ 7 章标准结构 + 核心参数对标检查机制 + 虚拟电厂分类各省不同原则
---

# 电力市场新型主体规则解析（V2.2.0·记忆库版）

---

## 核心规则

### 虚拟电厂分类 — 各省不同，禁止跨省套用

虚拟电厂的分类方式因省而异（如山东 4 类 vs 河南 3 类），必须查询该省实际政策文件，分类方式须有明确文号支撑。无法确认时标注"待核实"。详见 `long_term_memory.md`。

---

## 第零章 记忆库使用规范（最高优先级）

> **本 Skill 的报告 = 记忆体。图谱作导航层，报告作详情层。**

### 0.1 知识库结构（独立于 Skill，独立于 Agent）

```
~/.openclaw/kb/                    # 独立知识库（所有 agent 共享）
├── index.md                      # 人类友好型索引
├── ontology/                    # 图谱导航层
│   ├── schema.yaml              # 实体类型定义
│   ├── graph.jsonl              # 实体+关系数据
│   └── README.md
└── reports/                     # 报告详情层（永久保存）
    ├── 北京市虚拟电厂分析报告.md
    ├── 山东省虚拟电厂规则解析报告_20260324.md
    ├── 山东省独立储能与储能类虚拟电厂对比分析报告_20260324.md
    └── 黑龙江省独立储能规则解析报告_20260325.md
```

### 0.2 二次分析工作流（图谱导航模式）

```
1. 【图谱定位】
   python3 scripts/ontology.py query --type ProvinceVPP --where '{"subject":"虚拟电厂"}'
   ↓
2. 【确认报告】
   python3 scripts/ontology.py related --id {实体ID} --rel report_located_at
   ↓
3. 【读报告取详情】
   read ~/.openclaw/kb/reports/{目标报告}.md
   ↓
4. 【标注来源】
   引用时注明：「来源：{报告文件名} 第X章 X节」
```

> **原则**：图谱回答"在哪找"，报告回答"具体内容"。图谱不存详细参数（避免重复维护），详情一律读报告。

### 0.3 快捷查询场景

| 想问的问题 | 用什么方式 |
|-----------|-----------|
| "哪些省有虚拟电厂？" | `ontology.py query ProvinceVPP` |
| "山东有哪些VPP主体？" | `ontology.py related province_sd has_vpp_entity` |
| "黑龙江储能准入门槛是什么？" | 读报告 |
| "对比各省储能类VPP的分类方式" | 图谱找实体 → 读各报告第一章 |

### 0.4 生成新报告前 — 必须先查图谱/索引

生成新省份报告前，**必须先查图谱**，确认：
- 该省**已有实体** → 直接复用，不重复生成
- 该省**无实体** → 再走第一章 4 步生成流程

### 0.5 新报告归档流程（同时更新图谱+索引）

```
1. 将报告复制到 ~/.openclaw/kb/reports/ 目录
2. 复制文件命名：{省份}_{主体类型}_规则解析报告_{YYYYMMDD}.md
3. 在 ~/.openclaw/kb/ontology/graph.jsonl 末尾追加：
   - ProvinceVPP 实体（核心摘要，不超过10个字段）
   - ReportFile 实体
   - 关系：has_vpp_entity + report_located_at
4. 在 ~/.openclaw/kb/index.md 末尾追加索引条目
5. 注明 status：confirmed（已核实）/ partial（部分）/ unconfirmed（待核实）
```

### 0.6 三层存储分工

| 层 | 存什么 | 用什么工具 |
|---|--------|---------|
| **图谱层** ontology/ | 实体摘要 + 关系 + 报告定位 | ontology.py / 直接编辑 graph.jsonl |
| **索引层** index.md | 关键参数速查 + 章节位置 | read 直接读 |
| **报告层** reports/ | 完整规则原文，零损耗 | read 工具 |
| **长期记忆** long_term_memory.md | 方法论、分类教训 | read 直接读 |

---

## 第一章 工作流规范（最高优先级）

> **核心原则**：工作流是强制约束，不是可选建议。必须按顺序执行 4 步，严禁跳过！

### 第一步：生成前检查（必须执行·记录到 memory/日期.md）

**强制检查清单**（逐项打勾，记录到 memory/日期.md）：

```markdown
## 生成前检查清单（{省份}{主体}报告·{日期}）

- [ ] 已读主 Skill 文档（SKILL.md）
- [ ] 已读长期记忆（long_term_memory.md）
- [ ] ⭐ 已查 ~/.openclaw/kb/index.md，确认该省无现有报告（若有报告则直接复用，不生成）
- [ ] 已读 7 个 Tool 文档
- [ ] 已搜索核心参数（聚合容量、注册资本等）
- [ ] 已检查本地政策文件存储
- [ ] 已确认该省分类方式（未跨省套用）← 最高优先级
```

---

### 第二步：按 Tool 生成（必须执行·强制调用 7 个 Tool）

**Tool 调用映射表**：

| 章节 | Tool 名称 | 文件 | 必须调用 | 输出标准 |
|------|---------|------|---------|---------|
| 第一章 | subject-basics-analyzer | tools/subject-basics-analyzer.md | ✅ | 定义 + 分类表 + 与售电公司差异 |
| 第二章 | market-access-analyzer | tools/market-access-analyzer.md | ✅ | 准入条件 + 注册流程 + 材料清单 |
| 第三章 | trading-rules-analyzer | tools/trading-rules-analyzer.md | ✅ | 交易品种 + 申报规则 + 出清机制 |
| 第四章 | dispatch-operation-analyzer | tools/dispatch-operation-analyzer.md | ✅ | 调度管理 + 运营要求 |
| 第五章 | settlement-rules-analyzer | tools/settlement-rules-analyzer.md | ✅ | 结算流程 + 费用分摊 |
| 第六章 | local-policy-analyzer | tools/local-policy-analyzer.md | ✅ | 地方补贴 + 规则红利分析 |
| 第七章 | practical-guide-analyzer | tools/practical-guide-analyzer.md | ✅ | 实操案例 + 风险提示 |

---

### 第三步：生成后检查（必须执行·记录到 memory/日期.md）

**强制检查清单**：

```markdown
## 生成后检查清单

- [ ] 章节完整性（7 章完整）← check-chapters.sh
- [ ] 参数完整性（≥60 项）← check-params.sh
- [ ] 政策依据（≥10 个文件）← check-policy-count.sh
- [ ] 记录到 memory/日期.md
```

---

### 第四步：发送前自检（必须执行·质量达标才发送）

**质量标准**：

```markdown
## 发送前自检

- [ ] Markdown ≥50KB
- [ ] PDF ≥25 页
- [ ] 用户确认
```

---

## 第二章 核心规范

### 2.1 严禁跨省套用分类方式

每份报告必须基于目标省份的实际政策文件，禁止将一省的分类方式套用到另一省。详见上方核心规则。

### 2.2 核心参数搜索确认流程

**必须搜索的核心参数**：
| 参数 | 搜索关键词 | 优先级 |
|------|-----------|-------|
| 聚合容量门槛 | `{省份} 虚拟电厂 聚合容量 门槛` | 🔴 最高 |
| 注册资本要求 | `{省份} 虚拟电厂 注册资本` | 🟠 高 |
| 人员资质要求 | `{省份} 虚拟电厂 人员 资质` | 🟠 高 |
| 中长期签约比例 | `{省份} 新型主体 中长期 签约比例` | 🟠 高 |

**严禁行为**：
- ❌ 未搜索核心参数直接生成报告
- ❌ 核心参数写"待明确"
- ❌ 查不到不标注参考值

### 2.3 质量标准量化

| 检查项 | 量化标准 | 检查方法 |
|--------|---------|---------|
| 参数完整性 | ≥60 项 | check-params.sh |
| 政策依据 | ≥10 个文件 | check-policy-count.sh |
| 章节完整性 | 7 章完整 | check-chapters.sh |
| Markdown 大小 | ≥50KB | ls -lh |
| PDF 质量 | ≥25 页 | mdls 或目测 |

**防删减机制**：
- ≥80%：通过
- 60%-80%：警告（允许正常波动）
- <60%：失败（触发纠错机制，报告作废）

---

## 第三章 Tool 调用指引

### 3.1 Tool 列表

| Tool | 职责 | 文件 |
|------|------|------|
| `subject-basics-analyzer` | 基本情况解析 | tools/subject-basics-analyzer.md |
| `market-access-analyzer` | 市场准入规则 | tools/market-access-analyzer.md |
| `trading-rules-analyzer` | 交易规则 | tools/trading-rules-analyzer.md |
| `dispatch-operation-analyzer` | 调度与运营 | tools/dispatch-operation-analyzer.md |
| `settlement-rules-analyzer` | 结算规则 | tools/settlement-rules-analyzer.md |
| `local-policy-analyzer` | 地方政策红利 | tools/local-policy-analyzer.md |
| `practical-guide-analyzer` | 实操要点 | tools/practical-guide-analyzer.md |

### 3.2 调用示例

```markdown
**输入**：
- 省份：山东省
- 主体类型：虚拟电厂
- 政策文件：[鲁监能市场规〔2025〕57 号，...]

**执行**：
1. 调用 subject-basics-analyzer → 第一章
2. 调用 market-access-analyzer → 第二章
3. 调用 trading-rules-analyzer → 第三章
4. 调用 dispatch-operation-analyzer → 第四章
5. 调用 settlement-rules-analyzer → 第五章
6. 调用 local-policy-analyzer → 第六章
7. 调用 practical-guide-analyzer → 第七章
```

---

## 第四章 文件管理

### 4.1 文件结构

```
new-power-subjects-rule/
├── SKILL.md                          # L1: 主文档（含第零章记忆库使用规范）
├── long_term_memory.md               # L2: 长期记忆（方法论/分类教训）
├── memory/                           # L3: Skill 内部记忆（仅存临时日志）
│   └── YYYY-MM-DD.md                # 每日工作记录
├── examples/                         # L4: 范例库（质量范本，对标参考）
│   └── README.md
├── tools/                            # L5: Tool 文档（7 个）
│   ├── subject-basics-analyzer.md
│   ├── market-access-analyzer.md
│   ├── trading-rules-analyzer.md
│   ├── dispatch-operation-analyzer.md
│   ├── settlement-rules-analyzer.md
│   ├── local-policy-analyzer.md
│   └── practical-guide-analyzer.md
├── scripts/                          # L6: 检查脚本（3 个）
│   ├── check-params.sh
│   ├── check-chapters.sh
│   └── check-policy-count.sh
└── templates/                        # L7: 任务模板
    └── provincial_report_template.md
```

### 4.2 长期记忆

**文件**：`long_term_memory.md`
**读取**：每次生成报告前必须读取，记录到检查清单。
**内容**：虚拟电厂分类教训、政策标注规则、规则红利框架、范例库索引。
**更新**：仅追加，不删除。

---

## 第五章 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| V2.4.0 | 2026-03-27 11:35 | 知识库迁移至 ~/.openclaw/kb/（独立于 Skill 和 Agent）；所有报告+图谱统一存储，跨 Skill 共享 |
| V2.3.0 | 2026-03-27 11:25 | 新增图谱导航层 memory/ontology/：图谱+报告双层架构；图谱作导航层定位报告，报告作详情层取数据 |
| V2.2.0 | 2026-03-27 11:10 | 新增记忆库（memory/reports/）：报告=记忆体，二次分析直读；新增第零章工作流；更新文件结构 |
| V2.1.0 | 2026-03-24 17:46 | 文档瘦身：删除重复内容、口语化规范化，long_term_memory 从 259→44 行 |
| V2.0.0 | 2026-03-22 01:45 | 架构重构：拆分为 7 个 Tool + 创建长期记忆 + 4 步工作流 |
| V1.2.0 | 2026-03-18 15:45 | 移植 Power-Trading-Rule-Analysis 范例库方法 |
| V1.0.0 | 2026-03-11 | 初始版本 |

---

**文档维护**：每次 Skill 更新后，必须更新本章版本历史表。
