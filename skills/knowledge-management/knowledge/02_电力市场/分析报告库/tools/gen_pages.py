#!/usr/bin/env python3
"""Generate HTML pages for all province reports and update index."""
import os, re

PROVINCE_THEMES = {
    "北京":    {"gradient": "linear-gradient(135deg, #e53935 0%, #ff7043 100%)", "tag": "虚拟电厂", "icon": "🏙️", "accent": "#e53935"},
    "天津":    {"gradient": "linear-gradient(135deg, #0288d1 0%, #26c6da 100%)", "tag": "电力交易", "icon": "🌊", "accent": "#0288d1"},
    "安徽":    {"gradient": "linear-gradient(135deg, #7b1fa2 0%, #ea80fc 100%)", "tag": "虚拟电厂", "icon": "🏔️", "accent": "#7b1fa2"},
    "山东":    {"gradient": "linear-gradient(135deg, #388e3c 0%, #81c784 100%)", "tag": "电力交易", "icon": "🌊", "accent": "#388e3c"},
    "山东独立储能": {"gradient": "linear-gradient(135deg, #00695c 0%, #26a69a 100%)", "tag": "独立储能", "icon": "🔋", "accent": "#00695c"},
    "山东虚拟电厂": {"gradient": "linear-gradient(135deg, #f57c00 0%, #ffb74d 100%)", "tag": "虚拟电厂", "icon": "⚡", "accent": "#f57c00"},
    "山西":    {"gradient": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)", "tag": "电力交易", "icon": "⛰️", "accent": "#fa709a"},
    "河北":    {"gradient": "linear-gradient(135deg, #1565c0 0%, #42a5f5 100%)", "tag": "电力交易", "icon": "🌊", "accent": "#1565c0"},
    "内蒙古":  {"gradient": "linear-gradient(135deg, #f4511e 0%, #ffab91 100%)", "tag": "电力交易", "icon": "🏜️", "accent": "#f4511e"},
    "黑龙江":  {"gradient": "linear-gradient(135deg, #6d4c41 0%, #a1887f 100%)", "tag": "独立储能", "icon": "❄️", "accent": "#6d4c41"},
    "广西":    {"gradient": "linear-gradient(135deg, #6a1b9a 0%, #ce93d8 100%)", "tag": "电力交易", "icon": "🌴", "accent": "#6a1b9a"},
    "湖南":    {"gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)", "tag": "电力交易", "icon": "🏞️", "accent": "#f5576c"},
}

REPORTS_DIR = os.path.dirname(os.path.abspath(__file__))
KB_DIR = os.path.expanduser("~/.openclaw/kb/reports")

def _inline(text):
    text = re.sub(r'\'(.+?)\'\', r'<strong></strong>', text)
    text = re.sub(r'', r'<code></code>', text)
    text = re.sub(r'[\[(.+?)]\((.+?)\]', r'<a href=\'\'></a>', text)
    return text

def _make_table(lines):
    rows = []
    for l in lines:
        if re.match(r'^\|[\s\-:|<br>]+$'', l): continue
        cells = [c.strip() for c in l.strip().strip('\|').split('\|')]
        rows.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
    return '<table>' + ''.join(rows) + '</table>' if rows else ''

def md_to_html(content):
    title_match = re.search(r'^#\s+(.+)\$'', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "报告"
    meta_patterns = [
        (r'\*\*报告版本\*\*[:：]\s*v?(\d+[\d.]*)'', '版本'),
        (r'\*\*生成日期\*\*[:：]\s*([^
*]+)'', '日期'),
        (r'\*\*报告日期\*\*[:：]\s*([^
*]+)'', '日期'),
        (r'\*\*发布时间\*\*[:：]\s*([^
*]+)'', '发布时间'),
        (r'\*\*数据截止\*\*[:：]\s*([^
*]+)'', '数据截止'),
        (r'\*\*适用范围\*\*[:：]\s*([^
*]+)'', '适用范围'),
    ]
    meta_items = []
    for pattern, label in meta_patterns:
        m = re.search(pattern, content)
        if m and m.group(1).strip():
            meta_items.append(f'<div class="meta-item">📋 <strong>{label}</strong> {m.group(1).strip()}</div>')
    lines = content.split('
')
    html_lines, in_table, table_lines = [], False, []
    in_list, list_type = False, 'ul'
    in_code = False
    def flush_list():
        nonlocal in_list
        if in_list:
            html_lines.append(f'</{list_type}>')
            in_list = False
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith('''''):
            if not in_code:
                flush_list()
                in_code = True
                html_lines.append('<pre><code>')
            else:
                html_lines.append('</code></pre>')
                in_code = False
            i += 1
            continue
        if in_code:
            html_lines.append(line)
            i += 1
            continue
        if stripped.startswith('#### '):
            flush_list()
            html_lines.append(f'<h4>{_inline(stripped[5:])}</h4>')
        elif stripped.startswith('### '):
            flush_list()
            html_lines.append(f'<h3>{_inline(stripped[4:])}</h3>')
        elif stripped.startswith('## '):
            flush_list()
            html_lines.append(f'<h2>{_inline(stripped[3:])}</h2>')
        elif stripped.startswith('# '):
            pass
        elif stripped.startswith('|'):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(stripped)
        elif in_table:
            flush_list()
            html_lines.append(_make_table(table_lines))
            table_lines = []
            in_table = False
            continue
        elif re.match(r'^---+$'', stripped):
            flush_list()
            html_lines.append('<hr>')
        elif stripped.startswith('- ') or stripped.startswith('* '):
            if not in_list or list_type != 'ul':
                flush_list()
                html_lines.append('<ul>')
                in_list = True
                list_type = 'ul'
            html_lines.append(f'<li>{_inline(stripped[2:])}</li>')
        elif re.match(r'^\d+\.\s+'', stripped):
            if not in_list or list_type != 'ol':
                flush_list()
                html_lines.append('<ol>')
                in_list = True
                list_type = 'ol'
            html_lines.append(f'<li>{_inline(re.sub(r'^\d+\.\s+'', '', stripped))}</li>')
        else:
            flush_list()
            if stripped:
                html_lines.append(f'<p>{_inline(stripped)}</p>')
            else:
                html_lines.append('')
        i += 1
    flush_list()
    if in_table:
        html_lines.append(_make_table(table_lines))
    return title, meta_items, '
'.join(html_lines)
