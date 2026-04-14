#!/usr/bin/env python3
"""
知识图谱 data.js 生成器 v4
从 knowledge-index.md（knowledge-management 格式）提取知识节点 → data.js
支持：date字段、直接CDN URL、分类emoji
"""
import re, datetime

INDEX_FILE = "/home/admin/.openclaw/workspace/code-space/knowledge-graph/knowledge-index.md"
DATA_FILE = "/home/admin/.openclaw/workspace/code-space/knowledge-graph/data.js"

# 分类配置
CC = {
    "朗新科技":       { "color": "#3B82F6", "emoji": "🏢" },
    "可信数据空间":   { "color": "#10B981", "emoji": "🔐" },
    "充电桩":         { "color": "#F97316", "emoji": "⚡" },
    "虚拟电厂":       { "color": "#EF4444", "emoji": "🔋" },
    "数据基础设施":   { "color": "#8B5CF6", "emoji": "🏛️" },
    "default":        { "color": "#6B7280", "emoji": "📄" }
}

# === 解析 knowledge-index.md ===
with open(INDEX_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# 按 ## [标题] 分割块
blocks = []
current_title = None
current_lines = []
in_block = False

for line in content.split('\n'):
    if line.startswith('## ['):
        if current_title:
            blocks.append((current_title, current_lines))
        m = re.match(r'^##\s*\[([^\]]+)\]', line)
        current_title = m.group(1) if m else None
        current_lines = [line]
        in_block = True
    elif in_block:
        current_lines.append(line)

if current_title:
    blocks.append((current_title, current_lines))

print(f"Parsed {len(blocks)} knowledge blocks")

# === 提取节点数据 ===
nodes_out = []
for title, lines in blocks:
    # Extract category (from tags or default)
    cat = "数据基础设施"
    for ln in lines:
        ln_s = ln.strip()
        if ln_s.startswith('- **标签**') or ln_s.startswith('- 标签:'):
            for c in CC:
                if c in ln_s and c != "default":
                    cat = c
                    break
            break

    # Extract summary
    summary = ""
    for ln in lines:
        ln_s = ln.strip()
        if '**摘要**' in ln_s or ln_s.startswith('- 摘要'):
            for sep in ['**摘要**:', '**摘要:**', '摘要：', '摘要:']:
                if sep in ln_s:
                    summary = ln_s.split(sep, 1)[1].strip()
                    break
            if not summary and '摘要' in ln_s:
                m = re.search(r'[\*\*]*摘要[\*\*：:]\s*(.+)', ln_s)
                if m:
                    summary = m.group(1).strip()
            break

    # Extract CDN url
    url = ""
    for ln in lines:
        ln_s = ln.strip()
        if ln_s.startswith('- **归档URL**') or ln_s.startswith('- 归档URL:'):
            if ':' in ln_s:
                url = ln_s.split(':', 1)[1].strip().strip('*').strip()
            break

    # Extract date
    date_str = ""
    for ln in lines:
        if '提炼时间' in ln:
            m = re.search(r'(\d{8})', ln)
            if m:
                d = m.group(1)
                date_str = f"{d[:4]}-{d[4:6]}-{d[6:8]}"
            break

    # Extract source (skill name)
    source = "knowledge-index.md"
    for ln in lines:
        if '**来源**' in ln:
            m = re.search(r'\*\*来源\*\*:\s*\[([^\]]+)\]', ln)
            if m:
                source = m.group(1)
            break

    # Extract success_rate
    success_rate = None
    for ln in lines:
        if '**success_rate**' in ln:
            m = re.search(r'\*\*success_rate\*\*:\s*(\S+)', ln)
            if m:
                v = m.group(1)
                success_rate = None if v == 'null' else float(v)
            break

    if summary and len(summary) > 5:
        # 复用已有ID或生成新ID（基于category计数器）
        nid = None
        nodes_out.append({
            "id": nid,  # 暂时为空，后面统一生成
            "label": title,
            "category": cat,
            "summary": summary[:180].replace('"', "'"),
            "source": source,
            "url": url,
            "date": date_str,
            "connections": 0,
            "success_rate": success_rate
        })

# 生成稳定ID（按category排序，保证顺序一致）
from collections import OrderedDict
cat_counters = OrderedDict()
for n in nodes_out:
    cat = n["category"]
    if cat not in cat_counters:
        cat_counters[cat] = 0
    cat_counters[cat] += 1
    prefix = {"朗新科技":"lx","可信数据空间":"td","充电桩":"cd","虚拟电厂":"vp","数据基础设施":"ndi"}.get(cat, "xx")
    n["id"] = f"{prefix}-{cat_counters[cat]}"

# 关系（从 ## 关联 or ### 相关 中提取，暂不实现，保持简单）
links_out = []

# === 生成 data.js ===
ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
nodes_json = []
for n in nodes_out:
    sr = n["success_rate"] if n["success_rate"] is not None else "null"
    nodes_json.append(
        '    {{ id: "{id}", label: "{label}", category: "{cat}", source: "{source}", url: "{url}", date: "{date}", connections: {conn}, success_rate: {sr} }}'.format(
            id=n["id"],
            label=n["label"].replace('"', '\\"'),
            cat=n["category"],
            source=n["source"],
            url=n["url"],
            date=n["date"],
            conn=n["connections"],
            sr=sr
        )
    )

links_json = []
for l in links_out:
    links_json.append(f'    {{ source: "{l["source"]}", target: "{l["target"]}", relation: "{l["relation"]}" }}')

cconfig_lines = []
for name, cfg in CC.items():
    if name != "default":
        cconfig_lines.append(f'  "{name}": {{ "color": "{cfg["color"]}", "emoji": "{cfg["emoji"]}" }}')

data_js = f"""// Generated by sync-generator.py @ {ts}
// Source: {INDEX_FILE}
const KNOWLEDGE_DATA = {{
  nodes: [
{nodes_json}
  ],
  links: [
{links_json}
  ]
}};

const CATEGORY_CONFIG = {{
{','.join(cconfig_lines)}
}};
"""

# Also generate summaries.js (full summary content for lazy loading)
summaries_js = "const SUMMARIES = {\n"
for n in nodes_out:
    s = n["summary"].replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    summaries_js += f'  "{n["id"]}": "{s}",\n'
summaries_js += "};"
summaries_file = DATA_FILE.replace("data.js", "summaries.js")
with open(summaries_file, "w", encoding="utf-8") as f:
    f.write(summaries_js)

with open(DATA_FILE, "w", encoding="utf-8") as f:
    f.write(data_js)

print(f"Generated: {len(nodes_out)} nodes, {len(links_out)} links")
print(f"Data.js size: {len(data_js)} bytes")
