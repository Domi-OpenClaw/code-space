#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
knowledge_evaluate.py - 质量评估与主题分类

对知识库中的条目进行质量评估和主题分类。

Usage:
  python knowledge_evaluate.py                          # 评估所有知识点
  python knowledge_evaluate.py --report                   # 输出评估报告
  python knowledge_evaluate.py --id <id>                  # 评估指定知识点
  python knowledge_evaluate.py --update                   # 更新质量字段
"""

import sys
import re
import json
from datetime import datetime
from collections import Counter
from tinydb import TinyDB, Query

sys.path.insert(0, __file__.rsplit('/', 2)[0])
from config import (
    DB_PATH, TOPIC_MAP, INFO_WORDS, SOURCE_WEIGHTS,
    EXEMPT_KEYWORDS
)

db = TinyDB(DB_PATH)
tbl = db.table("knowledge")
K = Query()


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


def quality_score(entry):
    s = score_summary_length(entry.get("summary", "") or "")
    s += score_content_richness(entry.get("summary", "") or "")
    s += score_source(entry.get("source", ""))
    s += score_recency(entry.get("source_date", ""))
    return round(s, 1)


def get_topics(entry):
    text = ((entry.get("title", "") + " " + (entry.get("summary", "") or "")[:200])).lower()
    matched = []
    for topic, kws in TOPIC_MAP.items():
        if any(kw.lower() in text for kw in kws):
            matched.append(topic)
    return matched


def is_exempt(entry):
    source = entry.get('source', '') or ''
    title = entry.get('title', '') or ''
    for kw in EXEMPT_KEYWORDS:
        if kw in source or kw in title:
            return True
    return False


def evaluate_entry(entry):
    """评估单条知识点"""
    if is_exempt(entry):
        q = 100
    else:
        q = quality_score(entry)
    
    topics = get_topics(entry)
    return {
        'id': entry.get('id'),
        'title': entry.get('title', ''),
        'quality_computed': q,
        'topics': topics,
        'exempt': is_exempt(entry),
    }


def main():
    all_records = tbl.all()
    print(f"📦 总条目: {len(all_records)}")
    print()
    
    results = []
    for record in all_records:
        eval_result = evaluate_entry(record)
        results.append(eval_result)
        tbl.update({
            'quality_computed': eval_result['quality_computed'],
            'topics': eval_result['topics'],
        }, doc_ids=[record.doc_id])
    
    # 统计
    high = [r for r in results if r['quality_computed'] >= 60]
    mid = [r for r in results if 40 <= r['quality_computed'] < 60]
    low = [r for r in results if r['quality_computed'] < 40]
    
    print(f"✅ 高质(≥60): {len(high)} 条")
    print(f"⚠️  中质(40-60): {len(mid)} 条")
    print(f"❌ 低质(<40): {len(low)} 条")
    
    # 主题分布
    topic_counter = Counter()
    for r in results:
        for t in r.get('topics', []):
            topic_counter[t] += 1
    
    if topic_counter:
        print(f"\n📊 主题分布:")
        for topic, cnt in topic_counter.most_common():
            print(f"  {topic}: {cnt}")
    
    db.close()
    print(f"\n✅ TinyDB 已更新（quality_computed + topics 字段）")


if __name__ == '__main__':
    main()