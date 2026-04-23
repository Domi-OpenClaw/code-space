#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
knowledge_learn.py - 知识提炼、归档、溯源

从原始采集文件中提炼知识点，生成 CDN 归档链接，写入 TinyDB。

Usage:
  python knowledge_learn.py                              # 处理当日 memory 文件
  python knowledge_learn.py --input <file>               # 指定输入文件
  python knowledge_learn.py --date 2026-04-24            # 指定日期
  python knowledge_learn.py --dry-run                    # 预览不写入
"""

import sys
import os
import json
import hashlib
import argparse
from datetime import datetime
from pathlib import Path
from tinydb import TinyDB, Query

sys.path.insert(0, __file__.rsplit('/', 2)[0])
from config import DB_PATH, TOPIC_MAP

db = TinyDB(DB_PATH)
tbl = db.table("knowledge")
K = Query()


def extract_knowledge_from_file(file_path):
    """从文件中提取知识点（简化版，需要按具体文件格式解析）"""
    # TODO: 根据实际文件格式（memory/YYYY-MM-DD-energy-news.md等）实现解析
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    entries = []
    # 简化版：按标题提取
    lines = content.split('\n')
    current_title = None
    current_body = []
    
    for line in lines:
        if line.startswith('#') or line.startswith('##'):
            if current_title and current_body:
                summary = ' '.join(current_body).strip()[:500]
                entry = {
                    'title': current_title,
                    'summary': summary,
                    'source': file_path,
                    'source_date': datetime.now().strftime('%Y-%m-%d'),
                    'archive_url': '',
                    'tags': [],
                    'learned_date': datetime.now().strftime('%Y-%m-%d'),
                }
                entry['id'] = hashlib.md5(entry['title'].encode()).hexdigest()[:12]
                entries.append(entry)
            current_title = line.lstrip('#').strip()
            current_body = []
        elif line.strip():
            current_body.append(line.strip())
    
    if current_title and current_body:
        summary = ' '.join(current_body).strip()[:500]
        entry = {
            'title': current_title,
            'summary': summary,
            'source': file_path,
            'source_date': datetime.now().strftime('%Y-%m-%d'),
            'archive_url': '',
            'tags': [],
            'learned_date': datetime.now().strftime('%Y-%m-%d'),
        }
        entry['id'] = hashlib.md5(entry['title'].encode()).hexdigest()[:12]
        entries.append(entry)
    
    return entries


def process_memory_files(date_str=None):
    """处理 memory 目录下的文件"""
    memory_dir = Path(os.path.expanduser("~/.openclaw/workspace/memory"))
    if not memory_dir.exists():
        print("⚠️  memory 目录不存在")
        return []
    
    files = []
    if date_str:
        for pattern in ['energy-news', 'wechat-articles']:
            f = memory_dir / f"{date_str}-{pattern}.md"
            if f.exists():
                files.append(f)
    else:
        # 处理今日文件
        today = datetime.now().strftime('%Y-%m-%d')
        for pattern in ['energy-news', 'wechat-articles']:
            f = memory_dir / f"{today}-{pattern}.md"
            if f.exists():
                files.append(f)
    
    all_entries = []
    for f in files:
        print(f"📄 处理: {f.name}")
        entries = extract_knowledge_from_file(f)
        all_entries.extend(entries)
    
    return all_entries


def main():
    parser = argparse.ArgumentParser(description='知识提炼 - 从原始文件提炼知识点')
    parser.add_argument('--input', help='指定输入文件')
    parser.add_argument('--date', help='指定日期 (YYYY-MM-DD)')
    parser.add_argument('--dry-run', action='store_true', help='预览不写入')
    args = parser.parse_args()
    
    entries = []
    
    if args.input:
        entries = extract_knowledge_from_file(args.input)
    else:
        entries = process_memory_files(args.date)
    
    if not entries:
        print("ℹ️  没有找到需要提炼的知识点")
        return
    
    print(f"\n📝 提炼到 {len(entries)} 条知识点")
    
    if args.dry_run:
        for e in entries:
            print(f"  [DRY-RUN] {e['title'][:50]}")
        return
    
    # 写入 TinyDB
    imported = 0
    skipped = 0
    for entry in entries:
        existing = tbl.search(K.id == entry['id'])
        if existing:
            skipped += 1
            continue
        tbl.insert(entry)
        imported += 1
    
    print(f"\n✅ 导入完成: 新增 {imported} 条, 跳过 {skipped} 条")
    db.close()


if __name__ == '__main__':
    main()