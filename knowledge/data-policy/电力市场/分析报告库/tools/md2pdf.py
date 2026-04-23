#!/usr/bin/env python3
"""Convert markdown reports to PDF using WeasyPrint."""

import sys
import re
import os
import markdown
from weasyprint import HTML, CSS

def md_to_html(md_text):
    """Convert markdown to HTML with table styling."""
    # Use python-markdown with extensions
    html_body = markdown.markdown(
        md_text,
        extensions=['tables', 'fenced_code', 'toc', 'nl2br']
    )
    return html_body

def wrap_html(body_html, title):
    """Wrap HTML body in a full document with styles."""
    css = """
    @page {
        size: A4;
        margin: 2cm 1.8cm 2.5cm 1.8cm;
        @bottom-center {
            content: "第 " counter(page) " 页";
            font-size: 9px;
            color: #888;
        }
    }
    body {
        font-family: 'Noto Sans CJK SC', 'Noto Sans SC', 'WenQuanYi Micro Hei', 'Microsoft YaHei', 'PingFang SC', sans-serif;
        font-size: 10.5px;
        line-height: 1.7;
        color: #222;
    }
    h1 {
        font-size: 20px;
        color: #1a3c6e;
        border-bottom: 2px solid #1a3c6e;
        padding-bottom: 6px;
        margin-top: 30px;
        page-break-before: auto;
    }
    h1:first-of-type {
        page-break-before: avoid;
    }
    h2 {
        font-size: 16px;
        color: #2a5ca8;
        border-bottom: 1px solid #ddd;
        padding-bottom: 4px;
        margin-top: 25px;
    }
    h3 {
        font-size: 13px;
        color: #3a6eb5;
        margin-top: 18px;
    }
    h4 {
        font-size: 11.5px;
        color: #444;
        margin-top: 14px;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0 14px 0;
        font-size: 9.5px;
        page-break-inside: auto;
    }
    tr {
        page-break-inside: avoid;
    }
    th {
        background-color: #2a5ca8;
        color: white;
        padding: 6px 8px;
        text-align: left;
        font-weight: bold;
        border: 1px solid #1a3c6e;
    }
    td {
        padding: 5px 8px;
        border: 1px solid #ddd;
        vertical-align: top;
    }
    tr:nth-child(even) {
        background-color: #f5f8fc;
    }
    tr:hover {
        background-color: #eef3fa;
    }
    code {
        background-color: #f4f4f4;
        padding: 1px 4px;
        border-radius: 3px;
        font-size: 9px;
        font-family: 'Courier New', monospace;
    }
    pre {
        background-color: #f8f9fa;
        border: 1px solid #e1e4e8;
        border-radius: 4px;
        padding: 12px;
        overflow-x: auto;
        font-size: 9px;
        line-height: 1.5;
        white-space: pre-wrap;
        word-wrap: break-word;
        page-break-inside: avoid;
    }
    pre code {
        background: none;
        padding: 0;
    }
    blockquote {
        border-left: 4px solid #2a5ca8;
        margin: 12px 0;
        padding: 8px 16px;
        background-color: #f0f4f9;
        color: #444;
    }
    blockquote p {
        margin: 4px 0;
    }
    strong {
        color: #1a3c6e;
    }
    hr {
        border: none;
        border-top: 1px solid #ccc;
        margin: 20px 0;
    }
    ul, ol {
        padding-left: 20px;
    }
    li {
        margin: 3px 0;
    }
    .watermark {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-45deg);
        font-size: 60px;
        color: rgba(180, 180, 180, 0.15);
        z-index: 9999;
        white-space: nowrap;
        pointer-events: none;
    }
    /* Cover page */
    .cover {
        text-align: center;
        padding-top: 120px;
        page-break-after: always;
    }
    .cover h1 {
        font-size: 28px;
        border: none;
        color: #1a3c6e;
        margin-bottom: 20px;
    }
    .cover .subtitle {
        font-size: 14px;
        color: #666;
        margin: 10px 0;
    }
    .cover .meta {
        font-size: 11px;
        color: #999;
        margin-top: 40px;
        line-height: 2;
    }
    /* TOC */
    .toc {
        page-break-after: always;
    }
    .toc h2 {
        text-align: center;
        border: none;
    }
    .toc ul {
        list-style: none;
        padding: 0;
    }
    .toc li {
        padding: 4px 0;
        border-bottom: 1px dotted #ddd;
    }
    .toc a {
        color: #2a5ca8;
        text-decoration: none;
    }
    /* Warning boxes */
    p > strong:first-child {
        color: #c0392b;
    }
    """
    
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <style>{css}</style>
</head>
<body>
{body_html}
</body>
</html>"""
    return html


def create_cover(title, subtitle, meta_lines):
    """Create a cover page HTML."""
    meta_html = "<br>".join(meta_lines)
    return f"""
<div class="cover">
    <h1>{title}</h1>
    <p class="subtitle">{subtitle}</p>
    <div class="meta">
        {meta_html}
    </div>
</div>
"""


def convert_report(md_path, pdf_path, title):
    """Convert a markdown file to PDF."""
    print(f"Converting: {md_path} -> {pdf_path}")
    
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    # Convert markdown to HTML
    body_html = md_to_html(md_text)
    
    # Build cover page
    cover_html = create_cover(
        title,
        "电力市场规则解析报告",
        [
            f"报告名称：{title}",
            "生成日期：2026年3月24日",
            "数据截止：2026年3月",
            "分析工具：OpenClaw Agent · 新型主体规则解析 Skill V2.0.0",
            "声明：本报告基于公开政策文件整理，仅供商业决策参考",
        ]
    )
    
    # Combine
    full_html = wrap_html(cover_html + body_html, title)
    
    # Generate PDF
    HTML(string=full_html).write_pdf(pdf_path)
    
    # Check file size
    size = os.path.getsize(pdf_path)
    print(f"Done! PDF size: {size/1024:.1f} KB")


if __name__ == '__main__':
    base = '/home/bd-67015/openclaw/workspace/reports'
    
    # Report 1
    convert_report(
        os.path.join(base, '山东省虚拟电厂规则解析报告_20260324.md'),
        os.path.join(base, '山东省虚拟电厂规则解析报告_20260324.pdf'),
        '山东省虚拟电厂电力市场规则解析报告'
    )
    
    # Report 2
    convert_report(
        os.path.join(base, '山东省独立储能与储能类虚拟电厂对比分析报告_20260324.md'),
        os.path.join(base, '山东省独立储能与储能类虚拟电厂对比分析报告_20260324.pdf'),
        '山东省独立储能与储能类虚拟电厂对比分析报告'
    )
    
    print("\nAll reports converted!")
