# knowledge-management Skill

> **名称**：knowledge-management  
> **描述**：知识中枢，统一管理BCF Skill知识采集→清洗→归档→评价全流程  
> **版本**：v1.0  
> **面向**：小海哥（李军召），能源/数据要素领域业务专家

---

## 一、架构概览

```
knowledge-management (SKILL)
├── memory/          ← L0: 记忆管理
├── SKILL.md        ← L1: 本文档（主文档）
├── references/     ← L?: 参考文档
├── tools/          ← L3: 工具说明
├── scripts/         ← L4: 脚本集合
├── templates/      ← L5: 模板
├── examples/       ← L2: 示例
└── knowledge/      ← 数据目录（原始文件+TinyDB）
```

---

## 二、7工具架构

| 工具 | 文件 | 用途 |
|------|------|------|
| **learn.py** | `scripts/learn.py` | **唯一写入口**，将知识点写入 TinyDB |
| **query_knowledge.py** | `scripts/query_knowledge.py` | **KBI标准读接口**，查询知识库 |
| **knowledge_collect.py** | `scripts/knowledge_collect.py` | 采集通道管理（能源网站/RSS） |
| **knowledge_clean.py** | `scripts/knowledge_clean.py` | 清洗去重、质量评分 |
| **knowledge_learn.py** | `scripts/knowledge_learn.py` | 知识提炼、归档、溯源 |
| **knowledge_read.py** | `scripts/knowledge_read.py` | 知识读取（批量/单个） |
| **knowledge_evaluate.py** | `scripts/knowledge_evaluate.py` | 质量评估、主题分类 |
| **knowledge_report.py** | `scripts/knowledge_report.py` | 生成知识报告 |
| **knowledge_graph_update.py** | `scripts/knowledge_graph_update.py` | 更新知识图谱 |
| **config.py** | `scripts/config.py` | 配置文件（EVICT_ENABLED=False等） |

---

## 三、KBI接口规范

### 标准读接口：query_knowledge.py

```bash
# 模糊查询
python scripts/query_knowledge.py --query "虚拟电厂"

# 按标签筛选
python scripts/query_knowledge.py --tag "可信数据空间"

# 按质量阈值筛选
python scripts/query_knowledge.py --min-quality 60

# 输出JSON格式
python scripts/query_knowledge.py --query "虚拟电厂" --format json

# 限制返回条数
python scripts/query_knowledge.py --query "电力市场" --limit 10
```

**返回字段**：

| 字段 | 说明 |
|------|------|
| `id` | 知识点唯一标识 |
| `title` | 标题 |
| `summary` | 摘要 |
| `source` | 来源 |
| `source_date` | 来源日期 |
| `archive_url` | CDN归档链接 |
| `tags` | 标签列表 |
| `quality` | 质量分 |
| `learned_date` | 入库日期 |

---

## 四、工作流

```
[采集] → [清洗] → [学习] → [消费] → [评价] → [报告] → [图谱]
   ↓         ↓        ↓        ↓         ↓        ↓        ↓
能源网站  去重/评分  learn.py  售前/投标  quality  日报/月报  可视化
RSS      主题分类   唯一写入口 应用场景  门禁    生成报告  GitHub Pages
```

### 4.1 采集层

- **能源新闻采集**：energy-news-monitor（5个能源网站，07:15每日）
- **公众号文章采集**：wechat-official-accounts-scan（RSS，07:15每日）
- **电力市场情报**：power-market-intel（5Agent协作，cron定时）

### 4.2 清洗层

- `knowledge_clean.py`：去重、质量评分（>60入库，<40丢弃）
- `knowledge_evaluate.py`：主题分类（虚拟电厂/充电桩/可信数据空间/朗新科技）

### 4.3 学习层（唯一写入口）

- `learn.py`：汇总所有BCF Skill的知识点，写入 TinyDB
- `knowledge_learn.py`：知识提炼 + CDN归档 + 溯源链接
- **执行时间**：每日23:00（cron驱动）

### 4.4 消费层

- **售前材料**：pre-sales-workflow 自动引用知识库
- **投标文档**：tender-bid-generator 匹配政策/案例
- **头条内容**：toutiao-ops 从知识点提炼可发布内容

### 4.5 评价层

- `quality_gate.py`：质量门禁，quality_computed 字段更新
- 主题分类：TOPIC_MAP（虚拟电厂/充电桩/可信数据空间/朗新科技）
- **豁免清单**：政策文件原文、招投标公告、标准规范、企业官方资料

### 4.6 报告层

- `knowledge_report.py`：生成知识报告（日报/月报）
- 知识库健康度：知识点增长、采集覆盖率、质量评分、引用热度

### 4.7 图谱层

- `knowledge_graph_update.py`：同步 TinyDB → data.js → GitHub Pages
- `knowledge-graph.md`：实体关系文档（60+实体、80+关系）

---

## 五、红线规定

### 5.1 写入口唯一

> **只有 `learn.py` 能写 TinyDB**，其他脚本只读不写。

违反后果：数据不一致、溯源丢失、图谱无法同步

### 5.2 溯源不可丢

> **所有知识点必须带 `archive_url` CDN链接**，禁止只写锚点。

违反后果：无法追溯原文、知识可信度下降

### 5.3 知识退出机制

```python
# config.py
EVICT_ENABLED = False  # 暂不启用自动退出
EVICT_MIN_QUALITY = 30  # 低于此分数触发退出审核
EVICT_MAX_AGE_DAYS = 365  # 超过此天数未引用触发退出审核
```

### 5.4 豁免清单

以下类型免于质量评分审查，直接入库：
- 政策文件原文（发改委/能源局/数据局）
- 招投标公告（行业关键词 + 公告类型双重判断）
- 标准规范（NDI-TR / TC609）
- 企业官方资料（朗新科技等）

---

## 六、关键路径

| 组件 | 路径 |
|------|------|
| **TinyDB知识库** | `knowledge/db/knowledge-index.json` |
| **知识沉淀入口** | `scripts/learn.py` |
| **KBI读接口** | `scripts/query_knowledge.py` |
| **知识图谱结构** | `references/knowledge-graph.md` |
| **知识体系规划** | `references/knowledge-system-plan.md` |
| **知识图谱可视化** | https://domi-openclaw.github.io/code-space/knowledge-graph/ |

---

## 七、数据统计

- **TinyDB记录数**：63条（2026-04-23）
- **知识图谱**：60+实体、80+关系
- **采集通道**：5个能源网站 + RSS公众号
- **cron任务**：07:15能源新闻、23:00知识沉淀

---

*本Skill基于 SKILL-GUIDE v1.0 六层+L0 标准重建*