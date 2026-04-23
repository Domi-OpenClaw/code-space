#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库质量门禁 + 主题分类 v2
功能：
  1. 质量评分（<40丢弃，>60入库）
  2. 主题分类（宽松匹配，一条可属多主题）
  3. 写入更新后的 TinyDB 记录
"""

import sys
import re
from datetime import datetime

from tinydb import TinyDB

DB_PATH = "/home/admin/.openclaw/workspace/skills/knowledge-management/knowledge/db/knowledge-index.json"

# ── 评分函数 ──────────────────────────────────────────────────────────
INFO_WORDS = [
    "数据要素", "数据市场", "数据资产", "数据产品", "数据流通",
    "政策", "试点", "管理办法", "实施意见", "行动方案",
    "交易", "挂牌", "登记", "估值", "入表",
    "可信数据空间", "数据交易所", "数据集团", "基础设施",
    "人工智能", "大模型", "高质量数据集",
    "千瓦时", "兆瓦", "新能源", "虚拟电厂", "碳中和",
]

SOURCE_WEIGHTS = {
    "data-market-insight": 1.0,
    "power-market-intel":  1.0,
}

def score_summary_length(s):
    if not s: return 0
    l = len(s)
    if l < 10: return 0
    elif l < 30: return l * 0.5
    elif l < 80: return 15 + (l - 30) * 0.25
    elif l < 150: return 27.5 + (l - 80) * 0.07
    else: return 30

def score_content_richness(s):
    if not s: return 0
    score = 0
    sentences = [x.strip() for x in re.split(r'[。！？；\n]', s) if x.strip()]
    n = len(sentences)
    score += min(10, n * 2)
    info_count = sum(1 for w in INFO_WORDS if w in s)
    score += min(15, info_count * 2.5)
    score += (1 if re.search(r'\d+', s) else 0) * 5
    score += (1 if re.search(r'号|文|规|办|局', s) else 0) * 5
    if n >= 2 and len(set(sentences)) / n < 0.5:
        score *= 0.5
    return min(40, score)

def score_source(source):
    s = source.lower() if source else ""
    if not s: return 5
    if s in SOURCE_WEIGHTS:
        return SOURCE_WEIGHTS[s] * 20
    if any(k in s for k in ["数据局", "发改委", "工信部", "gov"]): return 18
    if any(k in s for k in ["交易所", "数据交易所"]): return 16
    if any(k in s for k in ["公众号", "微信"]): return 8
    if any(k in s for k in ["百家号", "头条", "微博", "雪球", "知乎"]): return 6
    return 10

def score_recency(date_str):
    if not date_str: return 0
    try:
        d = datetime.strptime(date_str[:10], "%Y-%m-%d")
        days = (datetime.now() - d).days
        if days <= 0: return 10
        elif days <= 7: return 9
        elif days <= 30: return 7
        elif days <= 90: return 5
        elif days <= 180: return 3
        elif days <= 365: return 1
        else: return 0
    except: return 0

def quality_score(r):
    s = score_summary_length(r.get("summary","") or "")
    s += score_content_richness(r.get("summary","") or "")
    s += score_source(r.get("source",""))
    s += score_recency(r.get("source_date",""))
    return round(s, 1)

# ── 主题分类（宽松，一条可属多主题）───────────────────────────────
TOPIC_MAP = {
    "虚拟电厂": ["虚拟电厂", "VPP", "需求响应", "负荷聚合商", "源网荷储", "可调负荷", "调峰调频", "辅助服务", "电力用户侧", "需求侧资源"],
    "充电桩": ["充电桩", "充换电", "V2G", "车网互动", "充电运营", "充电服务商", "充电站", "有序充电", "大功率充电", "超级充电", "充电网络"],
    "可信数据空间": ["可信数据空间", "数据空间", "TDP", "data space", "跨域互联", "数据互联互通"],
    "朗新科技": ["朗新科技", "朗新集团", "LongShine", "longshine", "新耀", "新电途"],
}

def get_topics(r):
    """返回主题列表（可空），宽松匹配"""
    text = ((r.get("title","") + " " + (r.get("summary","") or "")[:200])).lower()
    matched = []
    for topic, kws in TOPIC_MAP.items():
        if any(kw.lower() in text for kw in kws):
            matched.append(topic)
    return matched  # 空列表 = 无特定主题（即"数据基础设施"）

# ── 主逻辑 ─────────────────────────────────────────────────────────
db = TinyDB(DB_PATH)
tbl = db.table("knowledge")
all_records = tbl.all()

print(f"总条目: {len(all_records)}")
print()

keep, drop = [], []
for r in all_records:
    q = quality_score(r)
    topics = get_topics(r)
    r["quality_computed"] = q
    r["topics"] = topics
    if q < 40:
        drop.append(r)
    else:
        keep.append(r)

# 写回 TinyDB（更新 quality_computed 和 topics 字段）
for r in keep:
    tbl.update({
        "quality_computed": r["quality_computed"],
        "topics": r["topics"],
    }, doc_ids=[r.doc_id])

print(f"建议入库: {len(keep)} 条")
print(f"建议丢弃: {len(drop)} 条")
if drop:
    print(f"丢弃条目: {[r.get('title','')[:40] for r in drop]}")

# 主题分布
from collections import Counter
topic_counter = Counter()
for r in keep:
    tops = r.get("topics", [])
    if tops:
        for t in tops:
            topic_counter[t] += 1
    else:
        topic_counter["数据基础设施"] += 1

print(f"\n主题分布（入水库）:")
for topic, cnt in topic_counter.most_common():
    print(f"  {topic}: {cnt}")

db.close()
print(f"\n✅ TinyDB 已更新（quality_computed + topics 字段）")
