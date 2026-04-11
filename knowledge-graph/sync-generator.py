#!/usr/bin/env python3
"""
知识图谱 data.js 生成器 v3
从 knowledge-index.md 提取知识节点 → data.js
"""
import re, datetime

# URL映射表（jsDelivr 中文路径必须URL编码）
# 用法: f"https://cdn.jsdelivr.net/gh/Domi-OpenClaw/file-storage@main/{quote(folder)}/{quote(fname)}"
URLS = {
    "朗新科技集团中文画册-2025.pdf": "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/file-storage@main/%E5%85%B6%E4%BB%96/%E6%9C%97%E6%96%B0%E7%A7%91%E6%8A%80%E9%9B%86%E5%9B%A2%E4%B8%AD%E6%96%87%E7%94%BB%E5%86%8C-2025.pdf",
    "可信数据空间专题报告（2026年Q1版）.pdf": "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/file-storage@main/%E6%8A%A5%E5%91%8A/%E5%8F%AF%E4%BF%A1%E6%95%B0%E6%8D%AE%E7%A9%BA%E9%97%B4%E4%B8%93%E9%A2%98%E6%8A%A5%E5%91%8A%EF%BC%882026%E5%B9%B4Q1%E7%89%88%EF%BC%89.pdf",
    "可信数据空间营销合作方案V1.1.pdf": "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/file-storage@main/%E6%96%87%E6%A1%A3/%E5%8F%AF%E4%BF%A1%E6%95%B0%E6%8D%AE%E7%A9%BA%E9%97%B4%E8%90%A5%E9%94%80%E5%90%88%E4%BD%9C%E6%96%B9%E6%A1%88V1.1.pdf",
    "【数据产品】充电桩选址服务-产品说明书.pdf": "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/file-storage@main/%E6%96%87%E6%A1%A3/%E3%80%90%E6%95%B0%E6%8D%AE%E4%BA%A7%E5%93%81%E3%80%91%E5%85%85%E7%94%B5%E6%A1%A5%E5%9D%80%E5%9C%B0%E6%9C%8D%E5%8A%A1-%E4%BA%A7%E5%93%81%E8%AF%B4%E6%98%8E%E4%B9%A6.pdf",
    "虚拟电厂产品解决方案V1.0.2.pdf": "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/file-storage@main/%E6%96%87%E6%A1%A3/%E8%99%9A%E6%8B%9F%E7%94%B5%E5%8E%82%E4%BA%A7%E5%93%81%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88V1.0.2.pdf",
    "智慧能源方案1-1 基于智能微电网的园区能源运营服务解决方案1017.pdf": "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/file-storage@main/%E6%96%87%E6%A1%A3/%E6%99%BA%E6%85%A7%E8%83%BD%E6%BA%90%E6%96%B9%E6%A1%881-1%20%E5%9F%BA%E4%BA%8E%E6%99%BA%E8%83%BD%E5%BE%AE%E7%94%B5%E7%BD%91%E7%9A%84%E5%9B%AD%E5%8C%BA%E8%83%BD%E6%BA%90%E8%BF%90%E8%90%A5%E6%9C%8D%E5%8A%A1%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%881017.pdf",
    "南方电网公司数据开放目录（第一批）.pdf": "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/file-storage@main/%E6%96%87%E6%A1%A3/%E5%8D%97%E6%96%B9%E7%94%B5%E7%BD%91%E5%85%AC%E5%8F%B8%E6%95%B0%E6%8D%AE%E5%BC%80%E6%94%BE%E7%9B%AE%E5%BD%95%EF%BC%88%E7%AC%AC%E4%B8%80%E6%89%B9%EF%BC%89.pdf",
    "充电选址产品介绍PPT（外发）.pptx": "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/file-storage@main/%E5%85%B6%E4%BB%96/f8bd69e8-8c98-4210-a76e-50a52d0208ea.pptx",
    "大数据选址平台服务合作协议.docx": "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/file-storage@main/%E6%96%87%E6%A1%A3/3659b309-5355-4c6d-858a-9b1665850a7e.docx",
}

CATEGORIES = ["朗新科技", "可信数据空间", "充电桩", "虚拟电厂", "数据基础设施"]
CAT_PREFIX = {"朗新科技": "lx", "可信数据空间": "td", "充电桩": "cd", "虚拟电厂": "vp", "数据基础设施": "ndi"}

INDEX_FILE = "/home/admin/.openclaw/workspace/code-space/knowledge-graph/knowledge-index.md"
DATA_FILE = "/home/admin/.openclaw/workspace/code-space/knowledge-graph/data.js"

# Load existing nodes (for stable IDs)
existing = {}
existing_links = []
try:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        raw = f.read()
    for m in re.finditer(r'id:\s*"([^"]+)",\s*label:\s*"([^"]+)",\s*category:\s*"([^"]+)",\s*summary:\s*"([^"]+)",\s*source:\s*"([^"]+)",\s*url:\s*"([^"]+)",\s*connections:\s*(\d+)', raw):
        nid, label, cat, summary, source, url, conn = m.groups()
        existing[nid] = {"label": label, "category": cat, "connections": int(conn)}
    for m in re.finditer(r'source:\s*"([^"]+)",\s*target:\s*"([^"]+)",\s*relation:\s*"([^"]+)"', raw):
        existing_links.append((m.group(1), m.group(2), m.group(3)))
except:
    pass

# Load knowledge-index.md
with open(INDEX_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Parse blocks
blocks = []
current_title = None
current_lines = []
for line in content.split('\n'):
    if line.startswith('## '):
        if current_title is not None:
            blocks.append((current_title, current_lines))
        current_title = line[3:].strip()
        current_lines = []
    elif current_title is not None:
        current_lines.append(line)
if current_title is not None:
    blocks.append((current_title, current_lines))

SKIP_TITLES = {'📋 已归档文件清单', '🧠 知识提炼成果', '源文件映射'}

# Stable ID mapping
existing_ids = {
    "朗新科技集团中文画册（2025版）": "lx-1",
    "朗新科技企业概览与核心指标": "lx-2",
    "朗新AI研究院核心能力（2023年成立）": "lx-2",
    "朗新AI研究院核心能力": "lx-2",
    "朗新核心业务场景（能源互联网）": "lx-3",
    "朗新核心业务场景": "lx-3",
    "朗新科技发展历程": "lx-4",
    "可信数据空间市场特征（2026年Q1）": "td-3",
    "行业类可信数据空间招标项目（2026年Q1）": "td-4",
    "城市级可信数据空间招标项目（2026年Q1）": "td-5",
    "可信数据空间核心技术体系": "td-2",
    "可信数据空间定义与定位": "td-1",
    "充电桩选址大数据服务产品说明书": "cd-1",
    "充电AI智能选址产品介绍PPT": "cd-2",
    "大数据选址平台服务合作协议（朗新/乙方与甲方签署版）": "cd-3",
    "虚拟电厂产品解决方案 V1.0.2": "vp-1",
    "园区微电网能源运营服务解决方案": "vp-2",
    "南方电网公司数据开放目录（第一批）": "td-6",
    "南方能源行业可信数据空间 — 全套操作指引（13份）": "td-7",
    "国家数据基础设施技术文件 — NDI-TR系列核心标准（2025年2月发布，试运行6个月）": "ndi-3",
    "数据基础设施\"底座\"跨平台互联互通接口要求（草案）": "ndi-1",
    "数据领域常用名词解释（第一批+第二批）": "ndi-4",
    "可信数据空间2025年试点配套文件（DOCX模板）": "ndi-5",
    "2025年可信数据空间创新发展试点项目要素条件": "ndi-6",
    "数据提供合同示范文本（国家数据局，2025年4月征求意见稿）": "ndi-7",
    "数据委托处理合同示范文本（国家数据局，2025年4月征求意见稿）": "ndi-8",
    "数据融合开发合同示范文本（国家数据局，2025年4月征求意见稿）": "ndi-9",
    "数据中介合同示范文本（国家数据局，2025年4月征求意见稿）": "ndi-10",
}

# Stable links
LINKS = [
    {"source":"lx-2","target":"lx-3","relation":"研发支撑业务"},
    {"source":"lx-1","target":"lx-2","relation":"内容关联"},
    {"source":"lx-1","target":"lx-3","relation":"内容关联"},
    {"source":"lx-1","target":"lx-6","relation":"产品关联"},
    {"source":"lx-3","target":"lx-6","relation":"业务关联"},
    {"source":"lx-3","target":"lx-7","relation":"业务关联"},
    {"source":"lx-3","target":"lx-8","relation":"业务关联"},
    {"source":"lx-5","target":"vp-1","relation":"产品关联"},
    {"source":"lx-7","target":"td-3","relation":"市场关联"},
    {"source":"lx-3","target":"cd-2","relation":"业务关联"},
    {"source":"cd-2","target":"cd-1","relation":"产品关系"},
    {"source":"cd-1","target":"cd-3","relation":"商务关系"},
    {"source":"lx-3","target":"vp-1","relation":"业务关联"},
    {"source":"lx-3","target":"vp-2","relation":"业务关联"},
    {"source":"vp-1","target":"vp-2","relation":"方案关系"},
    {"source":"vp-1","target":"vp-3","relation":"业务关联"},
    {"source":"vp-2","target":"cd-1","relation":"场景关联"},
    {"source":"lx-5","target":"vp-2","relation":"产品关联"},
    {"source":"td-1","target":"td-2","relation":"包含关系"},
    {"source":"td-3","target":"td-4","relation":"市场机会"},
    {"source":"td-3","target":"td-5","relation":"市场机会"},
    {"source":"td-6","target":"td-3","relation":"数据支撑"},
    {"source":"td-6","target":"td-7","relation":"平台关联"},
    {"source":"td-3","target":"td-8","relation":"政策关联"},
    {"source":"ndi-1","target":"ndi-2","relation":"标准关联"},
    {"source":"ndi-1","target":"ndi-3","relation":"标准关联"},
    {"source":"ndi-1","target":"ndi-5","relation":"流程关联"},
    {"source":"ndi-4","target":"td-3","relation":"政策驱动"},
    {"source":"ndi-4","target":"td-8","relation":"政策驱动"},
    {"source":"td-2","target":"ndi-1","relation":"技术支撑"},
    {"source":"cd-2","target":"lx-2","relation":"AI能力支撑"},
    {"source":"vp-3","target":"lx-7","relation":"交易关联"},
    {"source":"lx-6","target":"vp-2","relation":"充电场景聚合"},
]

nodes_out = []
cat_counters = {c: 0 for c in CATEGORIES}

for title, lines in blocks:
    if not title or any(title.startswith(s) for s in SKIP_TITLES):
        continue

    cat = next((c for c in CATEGORIES if c in title), "数据基础设施")
    nid = existing_ids.get(title)
    if nid is None:
        prefix = CAT_PREFIX.get(cat, "ndi")
        cat_counters[cat] = cat_counters.get(cat, 0) + 1
        nid = f"{prefix}-{cat_counters[cat]}"

    body = '\n'.join(lines)

    # Extract 摘要 from bullet list
    summary = ""
    for ln in lines:
        ln = ln.strip()
        # Find the - 摘要： line
        if ln.startswith('- 摘要：') or ln.startswith('- 摘要:') or ln.startswith('摘要：') or ln.startswith('摘要:'):
            for sep in ['摘要：', '摘要:']:
                if sep in ln:
                    summary = ln.split(sep, 1)[1].strip()
                    break
            break

    # Extract source file
    src_file = ""
    for ln in lines:
        ln = ln.strip()
        if ln.startswith('- 来源文件：') or ln.startswith('来源文件：'):
            src_file = ln.split('：', 1)[1].strip() if '：' in ln else ''
            break

    url = URLS.get(src_file, "")

    if summary and len(summary) > 5:
        nodes_out.append({
            "id": nid, "label": title, "category": cat,
            "summary": summary[:180].replace('"', "'"),
            "source": "knowledge-index.md",
            "url": url, "connections": 0
        })

# Count connections
nid_set = {n["id"] for n in nodes_out}
for link in LINKS:
    if link["source"] in nid_set and link["target"] in nid_set:
        for n in nodes_out:
            if n["id"] == link["source"] or n["id"] == link["target"]:
                n["connections"] += 1

# Build data.js
CATEGORY_CONFIG = """const CATEGORY_CONFIG = {
  "朗新科技":     { "color": "#3B82F6", "emoji": "🏢" },
  "可信数据空间": { "color": "#10B981", "emoji": "🔐" },
  "充电桩":       { "color": "#F97316", "emoji": "⚡" },
  "虚拟电厂":     { "color": "#EF4444", "emoji": "⚡" },
  "数据基础设施": { "color": "#8B5CF6", "emoji": "🏛️" }
};
"""

ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
nodes_json = []
for n in nodes_out:
    nodes_json.append(
        '    {{\n      id: "{id}",\n      label: "{label}",\n      category: "{category}",\n      summary: "{summary}",\n      source: "{source}",\n      url: "{url}",\n      connections: {connections}\n    }}'.format(**n)
    )
links_json = []
for l in LINKS:
    if l["source"] in nid_set and l["target"] in nid_set:
        links_json.append(f'    {{ source: "{l["source"]}", target: "{l["target"]}", relation: "{l["relation"]}" }}')

data_js = "// Generated by sync-generator.py @ {ts}\n".format(ts=ts)
data_js += "const KNOWLEDGE_DATA = {{\n  nodes: [\n{nodes}\n  ],\n  links: [\n{links}\n  ]\n}};\n\n{cconfig}\n".format(
    nodes=',\n'.join(nodes_json),
    links=',\n'.join(links_json),
    cconfig=CATEGORY_CONFIG
)

with open(DATA_FILE, "w", encoding="utf-8") as f:
    f.write(data_js)

print(f"Generated: {len(nodes_out)} nodes, {len(links_json)} links")
print(f"Data.js size: {len(data_js)} bytes")
