#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
迁移 knowledge-index.md 到 TinyDB（JSON 数据库）
TinyDB: 纯 Python，无需编译，Python 3.6+ 内联可用
"""

import re
import os
import sys
import hashlib
import json
from datetime import datetime

# TinyDB via venv
from tinydb import TinyDB, Query

DB_DIR  = os.path.expanduser("~/.openclaw/workspace/skills/knowledge-management/knowledge/db")
DB_PATH = os.path.join(DB_DIR, "knowledge-index.json")
MD_PATH = os.path.expanduser("~/.openclaw/workspace/skills/knowledge-management/knowledge/knowledge-index.md")

os.makedirs(DB_DIR, exist_ok=True)

# ── 建库 ────────────────────────────────────────────────────────────────
db      = TinyDB(DB_PATH)
table   = db.table("knowledge")

# ── 解析 markdown ──────────────────────────────────────────────────────
with open(MD_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 按 "## 标题" 分割条目
entries = re.split(r"\n(?=## )", content)

inserted = 0
skipped  = 0

def get_field(entry, field):
    """支持缩进/非缩进的 **字段**: 值"""
    patterns = [
        rf"^\**{re.escape(field)}\*\*:\s*(.+)$",
        rf"^\s*-\s+\*\*{re.escape(field)}\*\*:\s*(.+)$",
    ]
    for pat in patterns:
        m = re.search(pat, entry, re.MULTILINE)
        if m:
            return m.group(1).strip()
    return ""

for entry in entries:
    if not entry.strip().startswith("## "):
        continue

    title = entry.strip().split("\n")[0].lstrip("# ").strip()

    raw_id      = get_field(entry, "知识点ID")
    source_raw  = get_field(entry, "来源")
    source_date = get_field(entry, "来源日期") or get_field(entry, "提炼时间") or ""
    archive_url = get_field(entry, "归档URL") or get_field(entry, "归档url") or ""
    summary     = get_field(entry, "摘要")
    tags_raw    = get_field(entry, "标签")
    quality_s   = get_field(entry, "质量")
    success_s   = get_field(entry, "success_rate")

    # 来源名字提取
    source_name = source_raw
    if "source://" in source_raw:
        m = re.search(r"source://([^)]+)", source_raw)
        source_name = m.group(1) if m else source_raw

    # ID
    if not raw_id:
        raw_id = hashlib.md5(title.encode("utf-8")).hexdigest()[:12]

    # 日期统一 YYYY-MM-DD
    if len(source_date) == 8 and source_date.isdigit():
        source_date = f"{source_date[:4]}-{source_date[4:6]}-{source_date[6:]}"

    try:
        quality_f = float(quality_s) if quality_s else 0
    except:
        quality_f = 0

    try:
        success_f = float(success_s) if success_s and success_s != "null" else None
    except:
        success_f = None

    record = {
        "id":          raw_id,
        "title":       title,
        "source":      source_name,
        "source_date": source_date,
        "archive_url": archive_url,
        "summary":     summary,
        "tags":        tags_raw,
        "quality":     quality_f,
        "success_rate": success_f,
        "learned_date": datetime.now().strftime("%Y-%m-%d"),
    }

    # upsert
    K = Query()
    existing = table.search(K.id == raw_id)
    if existing:
        table.update(record, K.id == raw_id)
    else:
        table.insert(record)
    inserted += 1

db.close()

# ── 验证 ────────────────────────────────────────────────────────────────
db2     = TinyDB(DB_PATH)
tbl     = db2.table("knowledge")
total   = len(tbl)
sources = len(set(r["source"] for r in tbl))

print(f"✅ 迁移完成")
print(f"   总条目: {total}")
print(f"   来源数: {sources}")
print(f"   跳过:   {skipped}")
print(f"   数据库: {DB_PATH}")

# ── 示例查询 ────────────────────────────────────────────────────────────
print(f"\n📋 示例查询（前3条 2026-04 以来的高权重条目）:")
K = Query()
recent = tbl.search(
    (K.source_date >= "2026-04-01") & (K.quality >= 80)
)
for r in sorted(recent, key=lambda x: x["source_date"], reverse=True)[:3]:
    print(f"   [{r['source_date']}] {r['title'][:40]}... (质量:{r['quality']})")

db2.close()
