# 知识管理工具说明

> 基于 `knowledge-graph.md` 提炼，描述工具使用方法

---

## 一、工具概览

| 工具 | 类型 | 用途 |
|------|------|------|
| `learn.py` | 写入口 | 唯一写入口，将知识点写入 TinyDB |
| `query_knowledge.py` | 读接口 | KBI标准读接口，模糊查询知识库 |
| `knowledge_collect.py` | 采集 | 管理采集通道（能源网站/RSS） |
| `knowledge_clean.py` | 清洗 | 去重、质量评分 |
| `knowledge_learn.py` | 学习 | 知识提炼、归档、溯源 |
| `knowledge_read.py` | 读取 | 批量/单个知识点读取 |
| `knowledge_evaluate.py` | 评估 | 质量评估、主题分类 |
| `knowledge_report.py` | 报告 | 生成知识报告 |
| `knowledge_graph_update.py` | 图谱 | 同步 TinyDB → 知识图谱 |
| `config.py` | 配置 | EVICT_ENABLED=False 等配置 |

---

## 二、核心工具用法

### 2.1 learn.py（唯一写入口）

```bash
# 基本用法
python scripts/learn.py

# 指定知识点文件
python scripts/learn.py --input /path/to/knowledge-points.json

# 强制更新（覆盖已有）
python scripts/learn.py --input /path/to/knowledge-points.json --force

# Dry run（不实际写入）
python scripts/learn.py --dry-run
```

**输入格式**（JSON）：
```json
{
  "title": "虚拟电厂参与电力现货市场暂行规则",
  "summary": "国家发改委要求虚拟电厂...",
  "source": "国家发改委官网",
  "source_date": "2026-04-01",
  "archive_url": "https://cdn.jsdelivr.net/...",
  "tags": ["虚拟电厂", "电力现货"]
}
```

**输出**：写入 `knowledge/db/knowledge-index.json`

---

### 2.2 query_knowledge.py（KBI标准读接口）

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

# 组合筛选
python scripts/query_knowledge.py --tag "虚拟电厂" --min-quality 70
```

**返回字段**：id / title / summary / source / source_date / archive_url / tags / quality / learned_date

---

### 2.3 knowledge_evaluate.py（质量评估）

```bash
# 评估所有知识点
python scripts/knowledge_evaluate.py

# 评估并输出报告
python scripts/knowledge_evaluate.py --report

# 评估指定知识点
python scripts/knowledge_evaluate.py --id <知识点ID>
```

**评分规则**：
- `score_summary_length`：摘要长度评分（0-30）
- `score_content_richness`：内容丰富度（0-40）
- `score_source`：来源权威性（0-20）
- `score_recency`：时效性（0-10）

**主题分类**：
- 虚拟电厂（关键词：虚拟电厂/VPP/需求响应/负荷聚合商等）
- 充电桩（关键词：充电桩/充换电/V2G/充电运营等）
- 可信数据空间（关键词：可信数据空间/data space/跨域互联等）
- 朗新科技（关键词：朗新科技/LongShine/新电途等）

---

### 2.4 knowledge_graph_update.py（图谱同步）

```bash
# 同步 TinyDB → 知识图谱
python scripts/knowledge_graph_update.py

# 只更新增量
python scripts/knowledge_graph_update.py --incremental

# 查看当前图谱状态
python scripts/knowledge_graph_update.py --status
```

**输出**：
- `data.js`：图谱可视化数据
- `references/knowledge-graph.md`：实体关系文档更新

---

### 2.5 quality_gate.py（质量门禁）

```bash
# 运行质量门禁
python scripts/quality_gate.py

# 查看门禁报告
python scripts/quality_gate.py --report

# 更新 TinyDB 质量字段
python scripts/quality_gate.py --update
```

**门禁规则**：
- quality < 40：建议丢弃
- quality 40-60：待审核
- quality > 60：建议入库

**豁免类型**：政策文件原文、招投标公告、标准规范、企业官方资料

---

## 三、辅助工具

### 3.1 db_integrity_check.py（完整性检查）

```bash
# 双向同步检查
python scripts/db_integrity_check.py

# 自动迁移「有md没db」的条目
python scripts/db_integrity_check.py --auto-migrate
```

**检查点**：
1. TinyDB 中的 ID，在 knowledge-index.md 中是否也有
2. knowledge-index.md 中的 ID，是否都进了 TinyDB
3. 自动迁移「有 md 没 db」的条目

### 3.2 import_to_feishu.py（飞书导入）

```bash
# 导入质量>=75的知识点到飞书
python scripts/import_to_feishu.py

# 指定质量阈值
python scripts/import_to_feishu.py --min-quality 80

# 预览导入数量
python scripts/import_to_feishu.py --dry-run
```

**飞书Bitable字段映射**：
- 文本：title
- 单选：主题分类（TAG_MAP）
- 来源文件：source
- 归档URL：archive_url
- 摘要：summary
- 质量分：quality
- 日期：learned_date

---

## 四、配置说明

### 4.1 config.py

```python
# 知识退出机制
EVICT_ENABLED = False  # 暂不启用自动退出
EVICT_MIN_QUALITY = 30  # 低于此分数触发退出审核
EVICT_MAX_AGE_DAYS = 365  # 超过此天数未引用触发退出审核

# 数据库路径
DB_PATH = "~/.openclaw/workspace/skills/knowledge-management/knowledge/db/knowledge-index.json"

# 质量阈值
QUALITY_THRESHOLD_KEEP = 60  # 入库阈值
QUALITY_THRESHOLD_DROP = 40  # 丢弃阈值

# 豁免类型
EXEMPT_TYPES = ["policy", "standard", "official"]
```

---

## 五、路径速查

| 工具 | 路径 |
|------|------|
| TinyDB | `knowledge/db/knowledge-index.json` |
| learn.py | `scripts/learn.py` |
| query_knowledge.py | `scripts/query_knowledge.py` |
| knowledge_evaluate.py | `scripts/knowledge_evaluate.py` |
| knowledge_graph_update.py | `scripts/knowledge_graph_update.py` |
| quality_gate.py | `scripts/quality_gate.py` |
| db_integrity_check.py | `scripts/db_integrity_check.py` |
| import_to_feishu.py | `scripts/import_to_feishu.py` |

---

*工具使用说明基于 knowledge-graph.md 提炼*