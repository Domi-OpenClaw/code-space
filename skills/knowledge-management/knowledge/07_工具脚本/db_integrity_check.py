#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TinyDB ↔ knowledge-index.md 双向完整性检查
检查点：
1. TinyDB 中的 ID，在 knowledge-index.md 中是否也有（两边一致）
2. knowledge-index.md 中的 ID，是否都进了 TinyDB（从 md 迁到 db）
3. 自动迁移「有 md 没 db」的条目

TinyDB 是唯一数据源，knowledge-index.md 仅备查。
"""
import re
import os
import sys
import json
from datetime import datetime

from tinydb import TinyDB, Query

DB_PATH  = os.path.expanduser("~/.openclaw/workspace/skills/knowledge-management/knowledge/db/knowledge-index.json")
MD_PATH  = os.path.expanduser("~/.openclaw/workspace/skills/knowledge-management/knowledge/knowledge-index.md")

# ── TinyDB ────────────────────────────────────────────────────────────
db   = TinyDB(DB_PATH)
tbl  = db.table("knowledge")
db_ids = {r["id"] for r in tbl.all()}
db.close()
print(f"📦 TinyDB 记录数: {len(db_ids)}")

# ── knowledge-index.md ─────────────────────────────────────────────────
def get_field(entry, field):
    patterns = [
        rf"^\**{re.escape(field)}\*\*:\s*(.+)$",
        rf"^\s*-\s+\*\*{re.escape(field)}\*\*:\s*(.+)$",
    ]
    for pat in patterns:
        m = re.search(pat, entry, re.MULTILINE)
        if m:
            return m.group(1).strip()
    return ""

def parse_md_entries(path):
    """解析 knowledge-index.md，返回 {id: record} dict"""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    entries = re.split(r"\n(?=## )", content)
    records = {}

    for entry in entries:
        if not entry.strip().startswith("## "):
            continue

        title = entry.strip().split("\n")[0].lstrip("# ").strip()
        raw_id  = get_field(entry, "知识点ID")
        source  = get_field(entry, "来源")
        date    = get_field(entry, "提炼时间") or get_field(entry, "来源日期") or ""
        url     = get_field(entry, "归档URL") or get_field(entry, "归档url") or ""
        summary = get_field(entry, "摘要")
        tags    = get_field(entry, "标签")
        quality = get_field(entry, "质量")
        sr      = get_field(entry, "success_rate")

        if not raw_id:
            import hashlib
            raw_id = hashlib.md5(title.encode("utf-8")).hexdigest()[:12]

        # 标准化日期
        if len(date) == 8 and date.isdigit():
            date = f"{date[:4]}-{date[4:6]}-{date[6:]}"

        records[raw_id] = {
            "id":           raw_id,
            "title":       title,
            "source":      source,
            "source_date":  date,
            "archive_url":  url,
            "summary":     summary,
            "tags":        tags,
            "quality":     float(quality) if quality else 0,
            "success_rate": float(sr) if sr and sr != "null" else None,
            "learned_date": date or datetime.now().strftime("%Y-%m-%d"),
        }

    return records

md_records = parse_md_entries(MD_PATH)
md_ids = set(md_records.keys())
print(f"📄 knowledge-index.md 条目数: {len(md_ids)}")

# ── 对比 ───────────────────────────────────────────────────────────────
in_both     = db_ids & md_ids
only_in_db  = db_ids - md_ids
only_in_md  = md_ids - db_ids

print(f"\n✅ 两边都有（一致）: {len(in_both)}")
print(f"🔵 仅 TinyDB:       {len(only_in_db)}")
print(f"🔴 仅 knowledge-index.md: {len(only_in_md)}")

if only_in_md:
    print(f"\n⚠️  发现 {len(only_in_md)} 条「有 md 没 db」的条目，开始迁移...")
    db2   = TinyDB(DB_PATH)
    tbl2  = db2.table("knowledge")
    K     = Query()
    migrated = 0
    for mid in only_in_md:
        rec = md_records[mid]
        existing = tbl2.search(K.id == rec["id"])
        if existing:
            tbl2.update(rec, K.id == rec["id"])
            print(f"  🔄 更新: {rec['title'][:50]}")
        else:
            tbl2.insert(rec)
            print(f"  ➕ 新增: {rec['title'][:50]}")
        migrated += 1
    db2.close()
    print(f"\n✅ 迁移完成，共 {migrated} 条")
elif only_in_db:
    print(f"\nℹ️  有 {len(only_in_db)} 条仅在 TinyDB 中，knowledge-index.md 是旧数据，正常。")

# ── 最终状态 ───────────────────────────────────────────────────────────
db3  = TinyDB(DB_PATH)
tbl3 = db3.table("knowledge")
print(f"\n📊 最终 TinyDB 总记录数: {len(tbl3)}")
db3.close()
