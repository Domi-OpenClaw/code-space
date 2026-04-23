#!/usr/bin/env python3
"""
Import knowledge-index.json entries to Feishu Bitable
Filters: quality >= 75, skip duplicates
"""

import json
import time
import urllib.request
import urllib.error

# === CONFIG ===
APP_TOKEN = 'JuBMbNKr5aSAeHslwd4c7jinnZf'
TABLE_ID = 'tblC1mFD3EOL5Rbn'
BASE_URL = 'https://open.feishu.cn/open-apis/bitable/v1'

# Feishu app credentials from openclaw.json
APP_ID = 'cli_a94d4db833f89cb6'
APP_SECRET = 'Ypb6qrerYB72GoEGB1K4OT1AXQMHN1wv'

# === LOAD KNOWLEDGE ===
with open('/home/admin/.openclaw/workspace/skills/knowledge-management/knowledge/db/knowledge-index.json') as f:
    data = json.load(f)

entries = data['knowledge']
print(f"Total entries: {len(entries)}")

# Filter quality >= 75
filtered = {}
for k, v in entries.items():
    q = v.get('quality_computed') or v.get('quality') or 0
    if q >= 75:
        filtered[k] = v
print(f"Entries with quality >= 75: {len(filtered)}")

# === TAG/TOPIC MAPPING ===
TAG_MAP = {
    'policy': '数据政策',
    'market': '数据市场',
    'finance': '金融',
    'gov': '政府',
    'bidding': '招标',
    '可信数据空间': '可信数据空间',
    '朗新科技': '朗新科技',
    '充电桩': '充电桩',
    '虚拟电厂': '虚拟电厂',
    '数据基础设施': '数据基础设施',
}
TOPIC_VALS = {'可信数据空间', '数据市场', '能源电力', '充电桩', '虚拟电厂', '数据基础设施'}

def map_single_select(entry):
    tags = entry.get('tags')
    # tags can be a list or a comma-separated string
    if isinstance(tags, list):
        tag_list = [str(t).strip() for t in tags if t]
    elif isinstance(tags, str):
        tag_list = [t.strip() for t in tags.split(',') if t.strip()]
    else:
        tag_list = []
    
    for tag in tag_list:
        if tag in TAG_MAP:
            return TAG_MAP[tag]
    return '其他'

def map_topic(entry):
    topics = entry.get('topics')
    if isinstance(topics, list) and topics:
        first = str(topics[0]).strip()
        if first in TOPIC_VALS:
            return first
        if first in TAG_MAP:
            return TAG_MAP[first]
        return first
    return map_single_select(entry)

def map_quality(entry):
    return entry.get('quality_computed') or entry.get('quality') or 0

def parse_learned_date(date_str):
    if not date_str:
        return None
    try:
        from datetime import datetime
        dt = datetime.strptime(str(date_str), '%Y-%m-%d')
        return int(dt.timestamp() * 1000)
    except:
        return None

def build_fields(entry):
    title = entry.get('title', '')
    summary = entry.get('summary', '') or ''
    fields = {
        '文本': title,
        '单选': map_single_select(entry),
        '主题': map_topic(entry),
        '来源文件': entry.get('source', '') or '',
        '归档URL': {
            'link': entry.get('archive_url', '') or '',
            'text': title
        },
        '摘要': summary[:200] if summary else '',
        '质量分': map_quality(entry),
    }
    date_ts = parse_learned_date(entry.get('learned_date'))
    if date_ts:
        fields['日期'] = date_ts
    return fields

# === GET TENANT TOKEN ===
def get_tenant_token():
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    body = json.dumps({'app_id': APP_ID, 'app_secret': APP_SECRET}).encode()
    req = urllib.request.Request(url, data=body, method='POST')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            if result.get('code') == 0:
                return result.get('tenant_access_token')
            else:
                print(f"Failed to get tenant token: {result}")
                return None
    except Exception as e:
        print(f"Error getting tenant token: {e}")
        return None

tenant_token = get_tenant_token()
print(f"Tenant token obtained: {bool(tenant_token)}")

# === API HELPER ===
def feishu_request(method, path, body=None):
    url = f"{BASE_URL}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header('Authorization', f'Bearer {tenant_token}')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        try:
            err_json = json.loads(err_body)
            return {'error': e.code, 'body': err_json}
        except:
            return {'error': e.code, 'body': err_body}

# === GET EXISTING RECORDS ===
print("Fetching existing records from Bitable...")
all_records = []
page_token = None
while True:
    path = f'/apps/{APP_TOKEN}/tables/{TABLE_ID}/records?page_size=500'
    if page_token:
        path += f'&page_token={page_token}'
    resp = feishu_request('GET', path)
    items = resp.get('data', {}).get('items', [])
    all_records.extend(items)
    if not resp.get('data', {}).get('has_more'):
        break
    page_token = resp.get('data', {}).get('page_token')

existing_titles = set()
for rec in all_records:
    fields = rec.get('fields', {})
    title = fields.get('文本', '')
    if title:
        existing_titles.add(title)

print(f"Existing records: {len(all_records)}, unique titles: {len(existing_titles)}")

# === DEDUP ===
to_import = []
skipped_duplicate = 0
for k, entry in filtered.items():
    title = entry.get('title', '')
    if title in existing_titles:
        skipped_duplicate += 1
    else:
        to_import.append(entry)

print(f"To import: {len(to_import)}, skipped (duplicate): {skipped_duplicate}")

# === IMPORT ===
results = {'success': 0, 'error': 0, 'errors': []}

for i in range(0, len(to_import), 20):
    batch = to_import[i:i+20]
    print(f"\nBatch {i//20 + 1}: importing {len(batch)} records...")
    
    for entry in batch:
        fields = build_fields(entry)
        body = {'fields': fields}
        resp = feishu_request('POST', f'/apps/{APP_TOKEN}/tables/{TABLE_ID}/records', body)
        
        if 'error' in resp:
            err_code = resp.get('error')
            err_detail = resp.get('body', '')
            print(f"  ERROR '{entry.get('title', '')[:40]}': {err_code} {str(err_detail)[:100]}")
            results['error'] += 1
            results['errors'].append({'title': entry.get('title', ''), 'code': err_code})
        else:
            print(f"  OK: '{entry.get('title', '')[:40]}'")
            results['success'] += 1
        
        time.sleep(0.35)

print(f"\n=== IMPORT COMPLETE ===")
print(f"Total entries in JSON: {len(entries)}")
print(f"Quality >= 75: {len(filtered)}")
print(f"Skipped (duplicate): {skipped_duplicate}")
print(f"To import: {len(to_import)}")
print(f"Success: {results['success']}")
print(f"Errors: {results['error']}")
if results['errors']:
    print("First 10 errors:")
    for e in results['errors'][:10]:
        print(f"  {e['title'][:50]}: {e['code']}")
