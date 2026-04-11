#!/usr/bin/env python3
"""
知识图谱 data.js 生成器 v2
从 knowledge-index.md 提取知识节点 → data.js
稳定ID策略：基于 label 匹配已有节点
"""
import re, datetime

# URL映射表：来源文件 → CDN URL
URLS = {
    "朗新科技集团中文画册-2025.pdf": "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/file-storage@main/其他/朗新科技集团中文画册-2025.pdf",
    "朗新科技集团中文画册-2025-OCR.txt": "https://raw.githubusercontent.com/Domi-OpenClaw/file-storage/1416713a0c53dd461fd71fa2ff4113d89f97a902/%E6%9C%97%E6%96%B0%E7%A7%91%E6%8A%80%E9%9B%86%E5%9B%A2%E4%B8%AD%E6%96%87%E7%94%BB%E5%86%9C-2025-OCR.txt",
    "可信数据空间专题报告（2026年Q1版）.pdf": "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/file-storage@main/报告/可信数据空间专题报告（2026年Q1版）.pdf",
    "可信数据空间营销合作方案V1.1.pdf": "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/file-storage@main/文档/可信数据空间营销合作方案V1.1.pdf",
    "【数据产品】充电桩选址服务-产品说明书.pdf": "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/file-storage@main/文档/3590bcd2-8125-480d-aeb3-417ca44a231f.pdf",
    "虚拟电厂产品解决方案V1.0.2.pdf": "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/file-storage@main/文档/5b432fba-2c80-4db1-8793-ce121266f977.pdf",
    "智慧能源方案1-1 基于智能微电网的园区能源运营服务解决方案1017.pdf": "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/file-storage@main/文档/17ee1ae7-8500-4de4-ba95-34711a1d9b56.pdf",
    "南方电网公司数据开放目录（第一批）.pdf": "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/file-storage@main/文档/1d6892ee-26d6-4604-91de-efbb61d99435.pdf",
    "充电选址产品介绍PPT（外发）.pptx": "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/file-storage@main/其他/f8bd69e8-8c98-4210-a76e-50a52d0208ea.pptx",
    "大数据选址平台服务合作协议.docx": "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/file-storage@main/文档/3659b309-5355-4c6d-858a-9b1665850a7e.docx",
}

CATEGORIES = ["朗新科技", "可信数据空间", "充电桩", "虚拟电厂", "数据基础设施"]
CAT_PREFIX = {"朗新科技": "lx", "可信数据空间": "td", "充电桩": "cd", "虚拟电厂": "vp", "数据基础设施": "ndi"}

INDEX_FILE = "/home/admin/.openclaw/workspace/code-space/knowledge-graph/knowledge-index.md"
DATA_FILE = "/home/admin/.openclaw/workspace/code-space/knowledge-graph/data.js"

# ── Load existing nodes (for stable IDs) ────────────────────────────────────
existing = {}   # label → {id, category, connections}
existing_links = []  # [(source, target, relation)]
try:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        raw = f.read()
    # Parse nodes
    for m in re.finditer(r'id:\s*"([^"]+)",\s*label:\s*"([^"]+)",\s*category:\s*"([^"]+)",\s*summary:\s*"([^"]+)",\s*source:\s*"([^"]+)",\s*url:\s*"([^"]+)",\s*connections:\s*(\d+)', raw):
        nid, label, cat, summary, source, url, conn = m.groups()
        existing[label] = {"id": nid, "category": cat, "connections": int(conn), "url": url}
    # Parse links
    for m in re.finditer(r'source:\s*"([^"]+)",\s*target:\s*"([^"]+)",\s*relation:\s*"([^"]+)"', raw):
        existing_links.append((m.group(1), m.group(2), m.group(3)))
except Exception as e:
    print(f"Warning loading existing data: {e}")

# ── Parse knowledge-index.md ─────────────────────────────────────────────────
with open(INDEX_FILE, "r", encoding="utf-8") as f:
    raw = f.read()

# Split into node blocks by ## headers
blocks = []
for line in raw.split('\n'):
    if line.startswith('## '):
        blocks.append({"title": line[3:].strip(), "lines": []})
    elif blocks:
        blocks[-1]["lines"].append(line)

SKIP_TITLES = {'📋 已归档文件清单', '🧠 知识提炼成果', 'Source File', '来源文件', '提炼时间'}

nodes_out = []
cat_counters = {c: 0 for c in CATEGORIES}
id_to_label = {}

for block in blocks:
    title = block["title"]
    if not title or any(title.startswith(s) for s in SKIP_TITLES):
        continue

    body_text = '\n'.join(block["lines"])

    # Category
    cat = next((c for c in CATEGORIES if c in title), "数据基础设施")

    # Stable ID
    nid = None
    if title in existing:
        nid = existing[title]["id"]
        cat = existing[title]["category"]
    else:
        # Partial match
        for label, info in existing.items():
            if len(title) > 5 and len(label) > 5 and (title[:8] == label[:8] or title[:10] in label):
                nid = info["id"]
                cat = info["category"]
                break

    if nid is None:
        prefix = CAT_PREFIX.get(cat, "ndi")
        cat_counters[cat] = cat_counters.get(cat, 0) + 1
        nid = f"{prefix}-{cat_counters[cat]}"

    # Extract summary: first non-metadata line
    summary = ""
    for ln in block["lines"]:
        ln = ln.strip()
        if not ln:
            continue
        if any(ln.startswith(x) for x in ['- 来源文件', '来源文件：', '- 归档URL', '归档URL：', '- 提炼时间', '提炼时间：', '**来源', '- **', '---', '| ', '> ', '#']):
            break
        if len(ln) > 5:
            summary = ln[:180].replace('"', "'")
            break

    # Source file → URL
    src_m = re.search(r'来源文件[：:]\s*([^\n]+)', body_text)
    src_file = src_m.group(1).strip() if src_m else ""
    url = URLS.get(src_file, "")

    # Connections count
    conn = 0
    if title in existing:
        conn = existing[title].get("connections", 0)
    id_to_label[nid] = title

    if summary and len(summary) > 5:
        nodes_out.append({
            "id": nid, "label": title, "category": cat,
            "summary": summary, "source": "knowledge-index.md",
            "url": url, "connections": conn
        })

# Links: keep only those between surviving nodes
nid_set = {n["id"] for n in nodes_out}
links_out = []
for s, t, r in existing_links:
    if s in nid_set and t in nid_set:
        links_out.append(f'    {{ source: "{s}", target: "{t}", relation: "{r}" }}')

# ── Write data.js ────────────────────────────────────────────────────────────
ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

CATEGORY_CONFIG = """const CATEGORY_CONFIG = {
  "朗新科技":     { "color": "#3B82F6", "emoji": "🏢" },
  "可信数据空间": { "color": "#10B981", "emoji": "🔐" },
  "充电桩":       { "color": "#F97316", "emoji": "⚡" },
  "虚拟电厂":     { "color": "#EF4444", "emoji": "⚡" },
  "数据基础设施": { "color": "#8B5CF6", "emoji": "🏛️" }
};
"""

nodes_json = []
for n in nodes_out:
    nodes_json.append(
        '    {{\n      id: "{id}",\n      label: "{label}",\n      category: "{category}",\n      summary: "{summary}",\n      source: "{source}",\n      url: "{url}",\n      connections: {connections}\n    }}'.format(**n)
    )

data_js = "// Generated by sync-generator.py @ {ts}\n".format(ts=ts)
data_js += "const KNOWLEDGE_DATA = {{\n  nodes: [\n{nodes}\n  ],\n  links: [\n{links}\n  ]\n}};\n\n{cconfig}\n".format(
    nodes=',\n'.join(nodes_json),
    links=',\n'.join(links_out) if links_out else '    // links maintained manually',
    cconfig=CATEGORY_CONFIG
)

with open(DATA_FILE, "w", encoding="utf-8") as f:
    f.write(data_js)

print("Generated: {0} nodes, {1} links".format(len(nodes_out), len(links_out)))
