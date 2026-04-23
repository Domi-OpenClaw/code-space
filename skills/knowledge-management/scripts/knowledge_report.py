#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
knowledge_report.py - 生成知识报告（日报/月报/年报）

Usage:
  python knowledge_report.py                            # 生成今日报告
  python knowledge_report.py --date 2026-04-24           # 指定日期
  python knowledge_report.py --type monthly               # 月报
  python knowledge_report.py --type yearly                # 年报
  python knowledge_report.py --output <file>              # 输出到文件
"""

import sys
import json
import argparse
from datetime import datetime, timedelta
from tinydb import TinyDB, Query
from collections import Counter

sys.path.insert(0, __file__.rsplit('/', 2)[0])
from config import DB_PATH

db = TinyDB(DB_PATH)
tbl = db.table("knowledge")
K = Query()


def generate_daily_report(date_str=None):
    """生成日报"""
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')
    
    results = tbl.search(K.learned_date == date_str)
    
    report = {
        'date': date_str,
        'type': 'daily',
        'total_entries': len(results),
        'topics': Counter(),
        'sources': Counter(),
        'entries': [],
    }
    
    for r in results:
        for t in r.get('topics', []):
            report['topics'][t] += 1
        report['sources'][r.get('source', 'unknown')] += 1
        report['entries'].append({
            'id': r.get('id'),
            'title': r.get('title'),
            'quality': r.get('quality_computed', 0),
        })
    
    return report


def generate_monthly_report(year=None, month=None):
    """生成月报"""
    now = datetime.now()
    year = year or now.year
    month = month or now.month
    
    start_date = f"{year}-{month:02d}-01"
    if month == 12:
        end_date = f"{year+1}-01-01"
    else:
        end_date = f"{year}-{month+1:02d}-01"
    
    results = tbl.search(
        (K.learned_date >= start_date) & (K.learned_date < end_date)
    )
    
    report = {
        'period': f"{year}-{month:02d}",
        'type': 'monthly',
        'total_entries': len(results),
        'topics': Counter(),
        'sources': Counter(),
        'quality_distribution': {'high': 0, 'mid': 0, 'low': 0},
        'entries': [],
    }
    
    for r in results:
        for t in r.get('topics', []):
            report['topics'][t] += 1
        report['sources'][r.get('source', 'unknown')] += 1
        q = r.get('quality_computed', 0)
        if q >= 60:
            report['quality_distribution']['high'] += 1
        elif q >= 40:
            report['quality_distribution']['mid'] += 1
        else:
            report['quality_distribution']['low'] += 1
        report['entries'].append({
            'id': r.get('id'),
            'title': r.get('title'),
            'quality': q,
        })
    
    return report


def format_report(report, fmt='text'):
    """格式化报告"""
    if fmt == 'json':
        return json.dumps(report, ensure_ascii=False, indent=2)
    
    lines = []
    lines.append(f"📊 知识报告 - {report.get('period', report.get('date', ''))} ({report['type']})")
    lines.append("=" * 50)
    lines.append(f"总知识点: {report['total_entries']}")
    
    if report.get('topics'):
        lines.append(f"\n📊 主题分布:")
        for topic, cnt in Counter(report['topics']).most_common():
            lines.append(f"  {topic}: {cnt}")
    
    if report.get('sources'):
        lines.append(f"\n📡 来源分布:")
        for source, cnt in Counter(report['sources']).most_common():
            lines.append(f"  {source}: {cnt}")
    
    if report.get('quality_distribution'):
        qd = report['quality_distribution']
        lines.append(f"\n✅ 质量分布: 高质={qd.get('high', 0)} 中质={qd.get('mid', 0)} 低质={qd.get('low', 0)}")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='知识报告生成')
    parser.add_argument('--date', help='指定日期 (YYYY-MM-DD)')
    parser.add_argument('--type', choices=['daily', 'monthly', 'yearly'], default='daily')
    parser.add_argument('--output', help='输出到文件')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    args = parser.parse_args()
    
    if args.type == 'daily':
        report = generate_daily_report(args.date)
    elif args.type == 'monthly':
        report = generate_monthly_report()
    else:
        print("⚠️  年报功能待实现")
        sys.exit(1)
    
    output = format_report(report, args.format)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"✅ 报告已输出到: {args.output}")
    else:
        print(output)
    
    db.close()


if __name__ == '__main__':
    main()