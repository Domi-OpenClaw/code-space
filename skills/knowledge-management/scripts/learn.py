#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
learn.py - 唯一写入口，将知识点写入 TinyDB

调用路径：
  knowledge_learn.py → 提炼知识点 → learn.py → TinyDB

Usage:
  python learn.py --input <json_file>        # 指定文件
  python learn.py --input <json_file> --force  # 强制覆盖
  python learn.py --dry-run                  # 预览不写入
"""

import sys
import json
import argparse
from datetime import datetime
from tinydb import TinyDB, Query

sys.path.insert(0, __file__.rsplit('/', 2)[0])
from config import DB_PATH, QUALITY_THRESHOLD_KEEP, EXEMPT_KEYWORDS

db = TinyDB(DB_PATH)
tbl = db.table("knowledge")
K = Query()


def is_exempt(entry):
    """检查是否豁免质量审查"""
    source = entry.get('source', '') or ''
    title = entry.get('title', '') or ''
    for kw in EXEMPT_KEYWORDS:
        if kw in source or kw in title:
            return True
    return False


def learn_entry(entry, force=False):
    """写入单条知识点"""
    if not entry.get('title'):
        return {'status': 'skip', 'reason': 'no title'}

    # 检查是否已存在
    existing = tbl.search(K.id == entry.get('id'))
    if existing and not force:
        return {'status': 'skip', 'reason': 'already exists, use --force to overwrite'}

    # 质量检查
    if not is_exempt(entry):
        quality = entry.get('quality_computed') or entry.get('quality') or 0
        if quality < QUALITY_THRESHOLD_KEEP:
            return {'status': 'reject', 'reason': f'quality {quality} < {QUALITY_THRESHOLD_KEEP}'}

    # 设置learned_date
    if not entry.get('learned_date'):
        entry['learned_date'] = datetime.now().strftime('%Y-%m-%d')

    # 写入
    if existing:
        tbl.update(entry, K.id == entry.get('id'))
        return {'status': 'update', 'id': entry.get('id')}
    else:
        tbl.insert(entry)
        return {'status': 'insert', 'id': entry.get('id')}


def main():
    parser = argparse.ArgumentParser(description='唯一写入口 - 学习知识点')
    parser.add_argument('--input', required=True, help='知识点JSON文件路径')
    parser.add_argument('--force', action='store_true', help='强制覆盖已有')
    parser.add_argument('--dry-run', action='store_true', help='预览不写入')
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)

    entries = data if isinstance(data, list) else data.get('entries', [data])

    results = {'insert': 0, 'update': 0, 'skip': 0, 'reject': 0}
    for entry in entries:
        if args.dry_run:
            print(f"[DRY-RUN] {entry.get('title', '')[:50]} - would learn")
            continue
        r = learn_entry(entry, force=args.force)
        results[r['status']] = results.get(r['status'], 0) + 1

    if not args.dry_run:
        print(f"✅ learn.py 完成: insert={results['insert']}, update={results['update']}, skip={results['skip']}, reject={results['reject']}")

    db.close()


if __name__ == '__main__':
    main()