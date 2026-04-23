# 知识管理体系核心摘要

> 面向小海哥（李军召），以 OpenClaw 为知识中枢，支撑能源/数据要素领域全链路知识管理

---

## 7工具架构

| 工具 | 用途 | 关键路径 |
|------|------|---------|
| **learn.py** | 唯一写入口，将知识点写入 TinyDB | `scripts/learn.py` |
| **query_knowledge.py** | KBI标准读接口，查询知识库 | `scripts/query_knowledge.py` |
| **knowledge_collect.py** | 采集通道管理（能源网站/RSS） | `scripts/knowledge_collect.py` |
| **knowledge_clean.py** | 清洗去重、质量评分 | `scripts/knowledge_clean.py` |
| **knowledge_learn.py** | 知识提炼、归档、溯源 | `scripts/knowledge_learn.py` |
| **knowledge_read.py** | 知识读取（批量/单个） | `scripts/knowledge_read.py` |
| **knowledge_evaluate.py** | 质量评估、主题分类 | `scripts/knowledge_evaluate.py` |

---

## KBI接口规范

**标准读接口**：`query_knowledge.py`

```bash
# 查询知识点（模糊匹配）
python scripts/query_knowledge.py --query "虚拟电厂"

# 按标签筛选
python scripts/query_knowledge.py --tag "可信数据空间"

# 按质量阈值筛选
python scripts/query_knowledge.py --min-quality 60

# 输出格式（JSON）
python scripts/query_knowledge.py --query "虚拟电厂" --format json
```

**返回字段**：id / title / summary / source / source_date / archive_url / tags / quality / learned_date

---

## 数据流程

```
采集层（energy-news-monitor / wechat-official-accounts-scan）
    ↓
原始数据（memory/YYYY-MM-DD-*.md）
    ↓ knowledge_collect.py
清洗层（去重/质量评分/主题分类）
    ↓ knowledge_clean.py + knowledge_evaluate.py
提炼层（知识点提炼 → knowledge-index.json）
    ↓ knowledge_learn.py（唯一写入口 learn.py）
知识库（TinyDB: knowledge/db/knowledge-index.json）
    ↓
应用层（pre-sales-workflow / tender-bid-generator / toutiao-ops）
    ↓
图谱层（知识图谱可视化 + knowledge-graph.md）
    ↓ knowledge_graph_update.py
```

---

## 核心规范

1. **写入口唯一**：只有 `learn.py` 能写 TinyDB
2. **溯源不可丢**：每条知识点必须含 `archive_url` CDN链接
3. **质量门禁**：quality < 40 丢弃，40-60 待审，> 60 入库
4. **知识退出机制**：EVICT_ENABLED=False（暂不启用自动退出）
5. **每日23:00定时沉淀**：cron驱动

---

## 关键文件路径

| 组件 | 路径 |
|------|------|
| **TinyDB知识库** | `knowledge/db/knowledge-index.json` |
| **知识沉淀入口** | `scripts/learn.py` |
| **KBI读接口** | `scripts/query_knowledge.py` |
| **知识图谱结构** | `references/knowledge-graph.md` |
| **知识体系规划** | `references/knowledge-system-plan.md` |