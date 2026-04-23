#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
knowledge_clean.py - 知识清洗（去重、质量评分、主题分类）

对采集到的原始知识进行清洗处理。

Usage:
  python knowledge_clean.py                          # 清洗所有未处理知识点
  python knowledge_clean.py --input <file>             # 指定输入文件
  python knowledge_clean.py --output <file>            # 指定输出文件
"""

import sys
import json
import re
from datetime import datetime
from tinydb import TinyDB, Query

sys.path.insert(0, __file__.rsplit('/', 2)[0])
from config import (
    DB_PATH, TOPIC_MAP, EXEMPT_KEYWORDS,
    QUALITY_THRESHOLD_KEEP, QUALITY_THRESHOLD_DROP, INFO_WORDS
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


def clean_record(entry):
    """清洗单条记录"""
    if not is_exempt(entry):
        entry['quality_computed'] = quality_score(entry)
    else:
        entry['quality_computed'] = 100  # 豁免类直接给满分
    
    entry['topics'] = get_topics(entry)
    
    # 标准化日期
    if entry.get('source_date'):
        try:
            dt = entry['source_date'][:10]
            datetime.strptime(dt, "%Y-%m-%d")
            entry['source_date'] = dt
        except:
            pass
    
    return entry


def main():
    # TODO: 实现从外部输入文件清洗
    # 当前默认清洗知识库中所有记录
    all_records = tbl.all()
    print(f"📦 总记录数: {len(all_records)}")
    
    cleaned = []
    for record in all_records:
        cleaned_record = clean_record(record)
        cleaned.append(cleaned_record)
        tbl.update({
            'quality_computed': cleaned_record['quality_computed'],
            'topics': cleaned_record['topics'],
        }, doc_ids=[record.doc_id])
    
    # 统计
    keep = [r for r in cleaned if r.get('quality_computed', 0) >= QUALITY_THRESHOLD_KEEP]
    drop = [r for r in cleaned if r.get('quality_computed', 0) < QUALITY_THRESHOLD_DROP]
    review = [r for r in cleaned if QUALITY_THRESHOLD_DROP <= r.get('quality_computed', 0) < QUALITY_THRESHOLD_KEEP]
    
    print(f"\n✅ 清洗完成:")
    print(f"  建议入库: {len(keep)} 条")
    print(f"  待审核: {len(review)} 条")
    print(f"  建议丢弃: {len(drop)} 条")
    
    # 主题分布
    from collections import Counter
    topic_counter = Counter()
    for r in cleaned:
        for t in r.get('topics', []):
            topic_counter[t] += 1
    if topic_counter:
        print(f"\n📊 主题分布:")
        for topic, cnt in topic_counter.most_common():
            print(f"  {topic}: {cnt}")
    
    db.close()


if __name__ == '__main__':
    main()