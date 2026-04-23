# Power-Trading-Rule-Analysis Skill V8.0.0

**电力市场规则分析 Skill** - 省级电力交易规则解析与实操落地

---

## 版本信息

- **当前版本**: V8.0.0（Tool 架构版）
- **发布日期**: 2026-03-20
- **文档量**: ~200 行（主 Skill）+ ~41KB（8 个 Tool）+ ~98KB（15 个范例）

---

## 核心能力

- **5 大核心能力模块**：政策解析、参数提取、规则对比、红利分析、报告生成
- **6 大规则解析维度**：市场主体、中长期、现货、零售、绿电、辅助服务
- **9 大应用场景**：省级报告、跨省对比、规则红利、投资分析等

---

## Tool 架构（V8.0.0）

### 8 个独立 Tool

| # | 章节 | Tool 名称 | 文件 | 大小 | 范例数 |
|---|------|---------|------|------|--------|
| 1 | 第一章 | Market Entities Analyzer | `tools/market-entities-analyzer.md` | 4.4KB | 2 个 |
| 2 | 第二章 | Medium-Long Term Trading Analyzer | `tools/medium-long-term-trading-analyzer.md` | 5.1KB | 2 个 |
| 3 | 第三章 | Spot Market Analyzer | `tools/spot-market-analyzer.md` | 5.1KB | 2 个 |
| 4 | 第四章 | Retail Package Analyzer | `tools/retail-package-analyzer.md` | 7.0KB | 2 个 |
| 5 | 第五章 | Green Power Trading Analyzer | `tools/green-power-trading-analyzer.md` | 4.2KB | 2 个 |
| 6 | 第六章 | Metering & Settlement Analyzer | `tools/metering-settlement-analyzer.md` | 4.7KB | 2 个 |
| 7 | 第七章 | Deviation Assessment Analyzer | `tools/deviation-assessment-analyzer.md` | 5.5KB | 2 个 |
| 8 | 第八章 | Ancillary Services Analyzer | `tools/ancillary-services-analyzer.md` | 5.2KB | 2 个 |

**总计**：8 个 Tool，约**41KB**文档，**15 个范例文件**

---

## 架构图

```
Power-Trading-Rule-Analysis Skill V8.0.0
│
├── SKILL.md (主 Skill·~200 行)
│   └── 负责架构设计、Tool 调度、报告生成
│
├── tools/ (8 个独立 Tool)
│   ├── market-entities-analyzer.md (4.4KB)
│   ├── medium-long-term-trading-analyzer.md (5.1KB)
│   ├── spot-market-analyzer.md (5.1KB)
│   ├── retail-package-analyzer.md (7.0KB)
│   ├── green-power-trading-analyzer.md (4.2KB)
│   ├── metering-settlement-analyzer.md (4.7KB)
│   ├── deviation-assessment-analyzer.md (5.5KB)
│   └── ancillary-services-analyzer.md (5.2KB)
│
├── examples/ (15 个范例文件·~98KB)
│   ├── retail-package/ (2 个：山东 + 贵州)
│   ├── market-entities/ (2 个：山东 + 贵州)
│   ├── medium-long-term/ (2 个：山东 + 贵州)
│   ├── spot-market/ (2 个：山东 + 贵州)
│   ├── green-power/ (2 个：山东 + 贵州)
│   ├── metering-settlement/ (2 个：山东 + 贵州)
│   ├── deviation-assessment/ (2 个：山东 + 贵州)
│   └── ancillary-services/ (2 个：山东 + 贵州)
│
└── templates/ (报告模板)
    └── provincial_report_template.md
```

---

## 调用示例

### 生成省级报告（完整 8 章）

```markdown
# 输入
省份：山东省
报告类型：完整详尽版
输出格式：Markdown + PDF

# 执行流程
1. 主 Skill 调用 8 个 Tool（按章节顺序）
2. 每个 Tool 输出对应章节内容
3. 主 Skill 整合所有章节，生成完整报告
4. PDF 转换（npx mdpdf）

# 输出
- 山东省电力交易规则解析报告（2026 版）_V37.0_完整详尽版.md (85.7KB)
- 山东省电力交易规则解析报告（2026 版）_V37.0_完整详尽版.pdf (2.81MB)
```

### 调用单个 Tool（如零售套餐分析）

```markdown
# 输入
Tool: retail-package-analyzer
省份：贵州省
参考范例：贵州省零售套餐分析范例.md

# 执行流程
1. 读取 Tool 文档（tools/retail-package-analyzer.md）
2. 按 Tool 流程分析（5 步强制流程）
3. 输出零售套餐章节内容
4. 执行检查清单

# 输出
- 零售套餐章节（约 5-8KB）
- 检查清单结果
```

---

## 核心原则

### 数据来源真实性（最高优先级）

- ❌ 严禁填写未实际获取的数据来源
- ❌ 严禁捏造月报/日报/公告名称
- ✅ 如无法获取官方文件，明确标注"数据待补充"
- ✅ 核心参数必须搜索确认，但需标注来源

### 零售套餐分类原则（最高优先级）

- ❌ 严禁预设分类（固定价格、峰谷分时、价格联动等）
- ❌ 严禁跨省套用（不能用山东/安徽/广东分类套用到其他省）
- ✅ 必须查询该省实际政策文件
- ✅ 按该省规则原文呈现
- ✅ 每个套餐类型必须有政策文号支撑

### 中长期签约比例（最高优先级）

- ✅ **正确**: 电量占比要求（年度≥80%、月度累计≥90%）
- ❌ **错误**: 零售套餐价格联动比例（10%-30% 联动）
- ⚠️ **山东特例**: 每月公告（3 月：用电侧 29.8%-59.8%）

---

## 省份差异原则

### 山东型（成熟市场）

- 政策文件丰富（8-14 个）
- 规则详细（价格封顶、偏差豁免、RUC+EC 出清）
- 数据完整（现货价格限价、负电价、月度公告）
- 市场特征：40%+60% 结算、价格联动免考核、节点电价

### 贵州型（过渡中市场）

- 政策文件较少（6-8 个）
- 规则相对简单（待细则较多）
- 南方区域统一规则（SCUC+SCED、统一结算点）
- 市场特征：1.5 倍保底电价、午间谷段、批零倒挂案例

---

## 质量检查

### 生成前检查清单

- [ ] 核心参数已搜索确认（燃煤基准价、容量补偿、现货限价等）
- [ ] 政策文件清单完整（≥12 个）
- [ ] 范例文件已加载（该省对应 Tool 范例）
- [ ] 参数完整性对标（≥80 项）

### 生成后检查清单

- [ ] 9 章结构完整（不跳过任何章节）
- [ ] 关键参数汇总表完整（9 大类≥60 项）
- [ ] 每项参数有政策文号支撑
- [ ] 数据来源真实（无捏造）
- [ ] 防删减检查≥80%

---

## 更新日志

### V8.0.0（2026-03-20）- Tool 架构版

**重大升级**：
- ✅ 创建 8 个独立 Tool，每个 Tool 负责一个章节
- ✅ 主 Skill 精简至~200 行（-71%）
- ✅ 创建 15 个范例文件（山东 + 贵州，~98KB）
- ✅ 新增 Tool 调用指引和检查清单

**架构优势**：
- 模块化：8 个独立 Tool，职责清晰
- 可复用：Tool 可被其他 Skill 调用
- 易维护：规则变化只需更新对应 Tool
- 轻量化：主 Skill 专注架构和 Tool 调度

### V7.0.0（2026-03-19）- 中长期签约比例修正版

**核心修正**：
- ✅ 新增中长期签约比例概念（电量占比 vs 价格联动比例）
- ✅ 新增防删减机制（≥80% 检查阈值）
- ✅ 新增关键参数汇总表格式（一张完整表格）

### V6.0.0（2026-03-18）- 数据来源真实性版

**核心原则**：
- ✅ 数据来源真实性原则（严禁捏造月报/日报）
- ✅ 核心参数搜索确认流程
- ✅ 参数完整性检查清单（≥60 项）

---

## 文件结构

```
Power-Trading-Rule-Analysis/
├── SKILL.md                          # 主体 Skill（V8.0.0·Tool 架构版）
├── long_term_memory.md               # 长期记忆文档
├── README.md                         # 本文档
├── tools/                            # Tool 目录（8 个 Tool）
│   ├── market-entities-analyzer.md
│   ├── medium-long-term-trading-analyzer.md
│   ├── spot-market-analyzer.md
│   ├── retail-package-analyzer.md
│   ├── green-power-trading-analyzer.md
│   ├── metering-settlement-analyzer.md
│   ├── deviation-assessment-analyzer.md
│   └── ancillary-services-analyzer.md
├── examples/                         # 范例目录（15 个范例）
│   ├── retail-package/
│   ├── market-entities/
│   ├── medium-long-term/
│   ├── spot-market/
│   ├── green-power/
│   ├── metering-settlement/
│   ├── deviation-assessment/
│   └── ancillary-services/
└── templates/                        # 报告模板
    └── provincial_report_template.md
```

---

## 联系方式

- **Skill 作者**: commander Agent
- **问题反馈**: 提交至 OpenClaw workspace
- **文档更新**: 2026-03-20 22:50

---

*Last Updated: 2026-03-20 22:52*
