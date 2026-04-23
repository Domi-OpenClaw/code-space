#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
knowledge_read.py - 知识读取（批量/单个）

用于从知识库中读取知识点，支持多种读取模式。

Usage:
  python knowledge_read.py --id <id>                    # 按ID读取
  python knowledge_read.py --all                          # 读取全部
  python knowledge_read.py --recent 7                     # 读取最近N天
  python knowledge_read.py --topic "虚拟电厂"              # 按主题读取
  python knowledge_read.py --format json                  # JSON格式输出
"""

import sys
import json
import argparse
from datetime import datetime, timedelta
from tinydb import TinyDB, Query

sys.path.insert(0, __file__.rsplit('/', 2)[0])
from config import DB_PATH

db = TinyDB(DB_PATH)
tbl = db.table("knowledge")
K = Query()


def read_by_id(uid):
    """按ID读取"""
    results = tbl.search(K.id == uid)
    return results[0] if results else None


def read_all(limit=None):
    """读取全部"""
    results = tbl.all()
    return results[:limit] if limit else results


def read_recent(days=7, limit=None):
    """读取最近N天的知识点"""
    cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    results = tbl.search(K.learned_date >= cutoff)
    return results[:limit] if limit else results


def read_by_topic(topic, limit=None):
    """按主题读取"""
    results = tbl.search(K.topics.any([topic]))
    return results[:limit] if limit else results


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
            'quality_computed': e.get('quality_computed'),
            'topics': e.get('topics'),
            'learned_date': e.get('learned_date'),
        }
    else:
        return (
            f"[{e.get('id')}] {e.get('title', '')}\n"
            f"  来源: {e.get('source', '')} | 日期: {e.get('source_date', '')}\n"
            f"  质量: {e.get('quality', 0)}/computed:{e.get('quality_computed', 0)} | 主题: {e.get('topics', [])}\n"
            f"  标签: {e.get('tags', [])}\n"
            f"  摘要: {str(e.get('summary', ''))[:200]}...\n"
            f"  归档: {e.get('archive_url', '')}"
        )


def main():
    parser = argparse.ArgumentParser(description='知识读取工具')
    parser.add_argument('--id', help='按ID读取')
    parser.add_argument('--all', action='store_true', help='读取全部')
    parser.add_argument('--recent', type=int, help='读取最近N天')
    parser.add_argument('--topic', help='按主题读取')
    parser.add_argument('--limit', type=int, help='限制条数')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='输出格式')
    args = parser.parse_args()
    
    results = []
    
    if args.id:
        r = read_by_id(args.id)
        results = [r] if r else []
    elif args.all:
        results = read_all(args.limit)
    elif args.recent:
        results = read_recent(args.recent, args.limit)
    elif args.topic:
        results = read_by_topic(args.topic, args.limit)
    else:
        results = read_all(10)  # 默认显示10条
    
    if args.format == 'json':
        print(json.dumps([format_entry(r, 'json') for r in results], ensure_ascii=False, indent=2))
    else:
        for r in results:
            print(format_entry(r, 'text'))
            print("---")
    
    print(f"\n共读取 {len(results)} 条记录")
    db.close()


if __name__ == '__main__':
    main()