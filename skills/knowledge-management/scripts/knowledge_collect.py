#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
knowledge_collect.py - 采集通道管理

管理能源网站、RSS公众号等采集通道。

Usage:
  python knowledge_collect.py --source <source_name>   # 指定采集源
  python knowledge_collect.py --list                    # 列出所有采集源
  python knowledge_collect.py --status                  # 查看采集状态
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

sys.path.insert(0, __file__.rsplit('/', 2)[0])
from config import DB_PATH

# 采集源配置
SOURCES = {
    'energy_news': {
        'name': '能源新闻采集（energy-news-monitor）',
        'sources': ['北极星电力网', '中国能源新闻网', 'RMI落基山研究所', '能见Eknower', '中电联'],
        'schedule': '07:15 每日',
        'status': 'active',
    },
    'wechat_rss': {
        'name': '公众号RSS采集（wechat-official-accounts-scan）',
        'sources': ['RSS/Atom localhost:4000'],
        'schedule': '07:15 每日',
        'status': 'active',
    },
    'power_market_intel': {
        'name': '电力市场情报（power-market-intel 5Agent）',
        'sources': ['多Agent协作'],
        'schedule': 'cron定时',
        'status': 'active',
    },
}


def list_sources():
    """列出所有采集源"""
    for key, info in SOURCES.items():
        print(f"📡 {info['name']}")
        print(f"   来源: {', '.join(info['sources'])}")
        print(f"   调度: {info['schedule']}")
        print(f"   状态: {info['status']}")
        print()


def get_status():
    """查看采集状态"""
    print(f"📊 知识采集通道状态 ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
    print("=" * 50)
    for key, info in SOURCES.items():
        status_icon = "✅" if info['status'] == 'active' else "⚠️"
        print(f"{status_icon} {info['name']}: {info['status']}")


def main():
    parser = argparse.ArgumentParser(description='知识采集通道管理')
    parser.add_argument('--list', action='store_true', help='列出所有采集源')
    parser.add_argument('--status', action='store_true', help='查看采集状态')
    args = parser.parse_args()

    if args.list:
        list_sources()
    elif args.status:
        get_status()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()