#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
query_knowledge.py - KBI标准读接口

Usage:
  python query_knowledge.py --query "虚拟电厂"           # 模糊查询
  python query_knowledge.py --tag "可信数据空间"          # 按标签筛选
  python query_knowledge.py --min-quality 60             # 按质量阈值
  python query_knowledge.py --query "虚拟电厂" --format json  # JSON输出
  python query_knowledge.py --limit 10                    # 限制条数
"""

import sys
import json
import argparse
from tinydb import TinyDB, Query

sys.path.insert(0, __file__.rsplit('/', 2)[0])
from config import DB_PATH

db = TinyDB(DB_PATH)
tbl = db.table("knowledge")
K = Query()


def query_by_text(text, limit=None):
    """模糊查询"""
    results = tbl.search(
        (K.title.contains(text, caseless=True)) |
        (K.summary.contains(text, caseless=True)) |
        (K.tags.contains(text, caseless=True))
    )
    return results[:limit] if limit else results


def query_by_tag(tag, limit=None):
    """按标签筛选"""
    results = tbl.search(K.tags.any([tag]))
    return results[:limit] if limit else results


def query_by_quality(min_quality, limit=None):
    """按质量阈值筛选"""
    results = tbl.search(K.quality >= min_quality)
    return results[:limit] if limit else results


def query_by_id(uid):
    """按ID查询"""
    results = tbl.search(K.id == uid)
    return results[0] if results else None


def format_entry(e, fmt='text'):
    """格式化输出"""
    if fmt == 'json':
        return {
            'id': e.get('id'),
            'title': e.get('title'),
            'summary': e.get('summary'),
            'source': e.get('source'),
            'source_date': e.get('source_date'),
            'archive_url': e.get('archive_url'),
            'tags': e.get('tags'),
            'quality': e.get('quality'),
            'learned_date': e.get('learned_date'),
        }
    else:
        return f"[{e.get('id')}] {e.get('title', '')[:50]}\n  来源: {e.get('source', '')} | 质量: {e.get('quality', 0)} | 标签: {e.get('tags', [])}\n  摘要: {str(e.get('summary', ''))[:100]}..."


def main():
    parser = argparse.ArgumentParser(description='KBI标准读接口 - 查询知识库')
    parser.add_argument('--query', help='模糊查询关键词')
    parser.add_argument('--tag', help='按标签筛选')
    parser.add_argument('--min-quality', type=float, help='最小质量分')
    parser.add_argument('--id', help='按ID查询')
    parser.add_argument('--limit', type=int, help='限制返回条数')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='输出格式')
    args = parser.parse_args()

    if args.id:
        result = query_by_id(args.id)
        results = [result] if result else []
    elif args.query:
        results = query_by_text(args.query, args.limit)
    elif args.tag:
        results = query_by_tag(args.tag, args.limit)
    elif args.min_quality:
        results = query_by_quality(args.min_quality, args.limit)
    else:
        results = tbl.all()
        if args.limit:
            results = results[:args.limit]

    if args.format == 'json':
        print(json.dumps([format_entry(r, 'json') for r in results], ensure_ascii=False, indent=2))
    else:
        for r in results:
            print(format_entry(r, 'text'))
            print("---")

    print(f"\n共找到 {len(results)} 条记录")
    db.close()


if __name__ == '__main__':
    main()