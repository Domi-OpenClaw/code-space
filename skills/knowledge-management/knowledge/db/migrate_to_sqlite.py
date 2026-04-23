#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
迁移 knowledge-index.md 到 SQLite 数据库
运行一次即可，数据库作为唯一数据源后，markdown 保留备查
"""

import re
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.expanduser("~/.openclaw/workspace/skills/knowledge-management/knowledge/db/knowledge-index.db")
MD_PATH = os.path.expanduser("~/.openclaw/workspace/skills/knowledge-management/knowledge/knowledge-index.md")

# ── 建表 ──────────────────────────────────────────────────────────────
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS knowledge (
    id              TEXT PRIMARY KEY,
    title           TEXT NOT NULL,
    source          TEXT,
    source_date     TEXT,
    archive_url     TEXT,
    summary         TEXT,
    tags            TEXT,
    quality         REAL DEFAULT 0,
    success_rate    REAL,
    learned_date    TEXT,
    raw_line        TEXT
)""")

c.execute("""CREATE INDEX IF NOT EXISTS idx_source ON knowledge(source)""")
c.execute("""CREATE INDEX IF NOT EXISTS idx_source_date ON knowledge(source_date)""")
c.execute("""CREATE INDEX IF NOT EXISTS idx_quality ON knowledge(quality)""")

# ── 解析 markdown ──────────────────────────────────────────────────────
with open(MD_PATH, "r", encoding="utf-8") as f:
    content = f.read()

entries = re.split(r"\n(?=## )", content)

inserted = 0
skipped = 0

for entry in entries:
    if not entry.strip().startswith("## "):
        continue

    # 解析标题
    m = re.match(r"## (.+)", entry.strip())
    if not m:
        skipped += 1
        continue
    title = m.group(1).strip()

    # 解析各字段
    def get(field):
        # 支持 "**字段**: 值" 和 "  - **字段**: 值" 两种格式
        patterns = [
            rf"^\**{re.escape(field)}\*\*:\s*(.+)$",
            rf"^\s*-\s+\*\*{re.escape(field)}\*\*:\s*(.+)$",
        ]
        for pat in patterns:
            m2 = re.search(pat, entry, re.MULTILINE)
            if m2:
                return m2.group(1).strip()
        return ""

    raw_id      = get("知识点ID")
    source_raw  = get("来源")
    source_date = get("来源日期") or get("提炼时间") or ""
    archive_url = get("归档URL") or get("归档url") or ""
    summary     = get("摘要")
    tags_raw    = get("标签")
    quality     = get("质量") or "0"
    success     = get("success_rate") or ""

    # 来源解析: "[data-market-insight](source://data-market-insight) - 20260413"
    source_name = source_raw
    if "source://" in source_raw:
        source_name = re.search(r"source://([^)]+)", source_raw)
        source_name = source_name.group(1) if source_name else source_raw

    # ID：如果没有就用标题hash
    if not raw_id:
        import hashlib
        raw_id = hashlib.md5(title.encode()).hexdigest()[:12]

    # 标签转JSON-like字符串
    tags = tags_raw

    # 日期统一转 YYYY-MM-DD
    if len(source_date) == 8 and source_date.isdigit():
        source_date = f"{source_date[:4]}-{source_date[4:6]}-{source_date[6:]}"

    try:
        quality_f = float(quality) if quality else 0
    except:
        quality_f = 0

    try:
        success_f = float(success) if success and success != "null" else None
    except:
        success_f = None

    c.execute("""INSERT OR REPLACE INTO knowledge
        (id, title, source, source_date, archive_url, summary, tags, quality, success_rate, learned_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (raw_id, title, source_name, source_date, archive_url, summary, tags,
         quality_f, success_f, datetime.now().strftime("%Y-%m-%d")))

    inserted += 1

conn.commit()

# ── 验证 ────────────────────────────────────────────────────────────────
c.execute("SELECT COUNT(*) FROM knowledge")
total = c.fetchone()[0]

c.execute("SELECT COUNT(DISTINCT source) FROM knowledge")
sources = c.fetchone()[0]

print(f"✅ 迁移完成")
print(f"   总条目: {total}")
print(f"   来源数: {sources}")
print(f"   跳过:   {skipped}")
print(f"   数据库: {DB_PATH}")

conn.close()
