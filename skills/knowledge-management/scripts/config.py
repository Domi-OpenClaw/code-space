#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识管理配置
"""

import os

# 知识库路径
DB_PATH = os.path.expanduser("~/.openclaw/workspace/skills/knowledge-management/knowledge/db/knowledge-index.json")

# 知识退出机制（暂不启用）
EVICT_ENABLED = False
EVICT_MIN_QUALITY = 30  # 低于此分数触发退出审核
EVICT_MAX_AGE_DAYS = 365  # 超过此天数未引用触发退出审核

# 质量阈值
QUALITY_THRESHOLD_KEEP = 60  # 入库阈值
QUALITY_THRESHOLD_DROP = 40  # 丢弃阈值
QUALITY_THRESHOLD_FEISHU = 75  # 飞书导入阈值

# 豁免类型（免于质量评分审查）
EXEMPT_TYPES = ["policy", "standard", "official"]
EXEMPT_KEYWORDS = ["发改委", "能源局", "数据局", "招投标公告", "NDI-TR", "TC609"]

# 主题分类
TOPIC_MAP = {
    "虚拟电厂": ["虚拟电厂", "VPP", "需求响应", "负荷聚合商", "源网荷储", "可调负荷", "调峰调频", "辅助服务"],
    "充电桩": ["充电桩", "充换电", "V2G", "车网互动", "充电运营", "充电站", "有序充电"],
    "可信数据空间": ["可信数据空间", "数据空间", "TDP", "data space", "跨域互联"],
    "朗新科技": ["朗新科技", "朗新集团", "LongShine", "longshine", "新耀", "新电途"],
}

# 标签映射（用于飞书导入）
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

# 来源权重
SOURCE_WEIGHTS = {
    "data-market-insight": 1.0,
    "power-market-intel": 1.0,
    "energy-news-monitor": 0.8,
}

# info词（用于质量评分）
INFO_WORDS = [
    "数据要素", "数据市场", "数据资产", "数据产品", "数据流通",
    "政策", "试点", "管理办法", "实施意见", "行动方案",
    "交易", "挂牌", "登记", "估值", "入表",
    "可信数据空间", "数据交易所", "数据集团", "基础设施",
    "人工智能", "大模型", "高质量数据集",
    "千瓦时", "兆瓦", "新能源", "虚拟电厂", "碳中和",
]