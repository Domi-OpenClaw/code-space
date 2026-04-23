#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
knowledge_graph_update.py - 知识图谱同步

从 TinyDB 同步数据到知识图谱（data.js + knowledge-graph.md）。

Usage:
  python knowledge_graph_update.py                       # 全量同步
  python knowledge_graph_update.py --incremental           # 增量同步
  python knowledge_graph_update.py --status                # 查看当前状态
"""

import sys
import json
import argparse
from datetime import datetime
from tinydb import TinyDB, Query

sys.path.insert(0, __file__.rsplit('/', 2)[0])
from config import DB_PATH

db = TinyDB(DB_PATH)
tbl = db.table("knowledge")
K = Query()


def get_graph_status():
    """查看图谱状态"""
    total = len(tbl.all())
    
    # 统计各主题数量
    topics = {}
    for r in tbl.all():
        for t in r.get('topics', []):
            topics[t] = topics.get(t, 0) + 1
    
    print("📊 知识图谱状态")
    print("=" * 40)
    print(f"总知识点: {total}")
    print(f"主题分布:")
    for topic, cnt in sorted(topics.items()):
        print(f"  {topic}: {cnt}")


def export_graph_data():
    """导出图谱数据"""
    entries = tbl.all()
    
    # 简化版：只导出实体和基础关系
    entities = []
    relations = []
    
    for entry in entries:
        # 实体
        entity = {
            'id': entry.get('id'),
            'name': entry.get('title', ''),
            'type': 'knowledge',
            'topics': entry.get('topics', []),
            'source': entry.get('source', ''),
        }
        entities.append(entity)
        
        # 关系：知识点与主题的关系
        for topic in entry.get('topics', []):
            relations.append({
                'from': entry.get('id'),
                'to': topic,
                'type': 'belongs_to',
            })
    
    return {
        'entities': entities,
        'relations': relations,
        'export_date': datetime.now().strftime('%Y-%m-%d'),
    }


def main():
    parser = argparse.ArgumentParser(description='知识图谱同步')
    parser.add_argument('--incremental', action='store_true', help='增量同步')
    parser.add_argument('--status', action='store_true', help='查看状态')
    args = parser.parse_args()
    
    if args.status:
        get_graph_status()
        db.close()
        return
    
    graph_data = export_graph_data()
    
    print(f"📊 导出图谱数据:")
    print(f"  实体: {len(graph_data['entities'])}")
    print(f"  关系: {len(graph_data['relations'])}")
    
    # TODO: 实际同步到 GitHub Pages / code-space
    # 当前仅输出到控制台
    print("\n⚠️  图谱同步到 GitHub Pages 功能待实现")
    print("   需要同步到: code-space/knowledge-graph/data.js")
    
    db.close()


if __name__ == '__main__':
    main()