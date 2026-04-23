#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电力交易规则解析报告 - 内容完整性检查脚本

用途：检查生成的 Markdown 报告是否包含所有必需内容
触发场景：生成报告后自动执行，确保内容完整

检查项：
1. 章节结构完整性（8 章）
2. 必需表格（交易品种表、申报表、出清机制表等）
3. 必需公式（结算公式、套餐公式等）
4. 必需示例（计算示例、报价示例等）
5. 关键参数（燃煤基准价、容量补偿等）
6. 环保电价参数（脱硫/脱硝/除尘 - 强制固化项）
7. 政策依据（文号标注）
8. 内部信息检查（禁止包含编制说明、文件路径等）
9. 结算章节详细程度（7 类主体结算）
10. 省份特色检查（禁止跨省套用）

作者：Power-Trading-Rule-Analysis Skill
版本：V1.2 (2026-03-17) - 新增内部信息检查、结算章节检查、省份特色检查
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class ReportChecker:
    """报告内容完整性检查器"""
    
    def __init__(self, markdown_path: str):
        self.markdown_path = Path(markdown_path)
        self.content = self.markdown_path.read_text(encoding='utf-8')
        self.lines = self.content.split('\n')
        self.issues = []
        self.warnings = []
        self.passed = []
        
    def check_all(self) -> bool:
        """执行所有检查"""
        print(f"\n{'='*60}")
        print(f"报告内容完整性检查")
        print(f"文件：{self.markdown_path}")
        print(f"大小：{len(self.content):,} 字符 / {len(self.lines):,} 行")
        print(f"{'='*60}\n")
        
        # 首先检查报告大小（新增·最高优先级）
        self.check_report_size()
        
        # 执行检查
        self.check_chapter_structure()
        self.check_required_tables()
        self.check_required_formulas()
        self.check_required_examples()
        self.check_key_parameters()
        self.check_environmental_price()  # 新增：环保电价专项检查
        self.check_policy_citations()
        self.check_retail_packages()
        self.check_deviation_assessment()
        self.check_internal_info()  # 新增：内部信息检查
        self.check_settlement_details()  # 新增：结算章节详细程度检查
        self.check_province_specific_rules()  # 新增：省份特色检查
        self.check_content_reduction()  # 新增：防删减检查（最高优先级）
        
        # 输出结果
        self.print_result()
        
        return len(self.issues) == 0
    
    def check_report_size(self):
        """检查报告大小（新增·最高优先级）
        
        山东范例 V13.0：2109 行 / 72KB
        设置最小阈值：1500 行 / 50KB
        """
        min_lines = 1500  # 最小行数
        min_size_kb = 50  # 最小 KB 数
        
        actual_lines = len(self.lines)
        # 修复：使用字节数计算 KB，而不是字符数
        actual_size_bytes = self.markdown_path.stat().st_size
        actual_size_kb = actual_size_bytes / 1024
        
        if actual_lines < min_lines:
            self.issues.append(f"✗ 报告行数不足：{actual_lines} 行 < {min_lines} 行（山东范例 V13.0：2109 行）")
        else:
            self.passed.append(f"✓ 报告行数达标：{actual_lines} 行 ≥ {min_lines} 行")
        
        if actual_size_kb < min_size_kb:
            self.issues.append(f"✗ 报告大小不足：{actual_size_kb:.1f}KB < {min_size_kb}KB（山东范例 V13.0：72KB）")
        else:
            self.passed.append(f"✓ 报告大小达标：{actual_size_kb:.1f}KB ≥ {min_size_kb}KB")
    
    def check_chapter_structure(self):
        """检查章节结构完整性（8 章）
        
        山东范例 V13.0 章节结构：
        第一章 市场主体概览
        第二章 中长期交易规则
        第三章 现货市场规则
        第四章 零售市场规则
        第六章 绿电交易规则
        第七章 计量、结算与费用
        第八章 偏差考核与修正
        第九章 辅助服务市场
        """
        required_chapters = [
            ("第一章", "市场主体概览"),
            ("第二章", "中长期交易规则"),
            ("第三章", "现货市场规则"),
            ("第四章", "零售市场规则"),
            ("第六章", "绿电交易规则"),
            ("第七章", "计量、结算与费用"),
            ("第八章", "偏差考核与修正"),
            ("第九章", "辅助服务市场"),
        ]
        
        for chapter_num, chapter_name in required_chapters:
            pattern = f"{chapter_num}.*{chapter_name}"
            if re.search(pattern, self.content):
                self.passed.append(f"✓ 章节完整：{chapter_num} {chapter_name}")
            else:
                self.issues.append(f"✗ 缺失章节：{chapter_num} {chapter_name}")
    
    def check_required_tables(self):
        """检查必需表格
        
        山东范例 V13.0 实际表格形式：
        - 交易品种总览：章节标题"交易品种总览"，表格包含"交易品种 | 交易方式"
        - 交易标的表：章节标题"交易标的与曲线分解"，表格包含"D1 曲线"
        - 参与主体表：表格包含"主体类型 | 买方 | 卖方"或"申报角色"
        - 电量申报表：表格包含"最小申报电量"
        - 价格申报表：表格包含"申报价格"或"价格单位"
        - 出清机制表：章节标题"出清机制详解"，表格包含"集中竞价"或"双边协商"
        - 月度交易日历：章节标题"月度交易日历"，表格包含"交易日期"或"申报时间"
        - 政策依据表：章节标题"政策依据"，表格包含"政策名称"
        - 数据来源表：章节标题"数据来源"，表格包含"数据来源"
        """
        required_tables = [
            ("交易品种总览表", r"交易品种总览 | 交易品种.*交易方式"),
            ("交易标的表", r"交易标的与曲线分解|D1 曲线.*分解比例"),
            ("参与主体表", r"主体类型.*买方.*卖方 | 申报角色 | 参与主体表"),
            ("电量申报表", r"电量申报 | 最小申报电量"),
            ("价格申报表", r"价格申报 | 申报价格.*单位"),
            ("出清机制表", r"出清机制详解 | 集中竞价 | 双边协商"),
            ("月度交易日历", r"月度交易日历 | 交易日期.*申报时间"),
            ("政策依据表", r"## 政策依据 | 政策名称.*文号"),
            ("数据来源表", r"## 数据来源 | 数据来源"),
        ]
        
        for table_name, pattern in required_tables:
            if re.search(pattern, self.content, re.IGNORECASE):
                self.passed.append(f"✓ 表格完整：{table_name}")
            else:
                self.issues.append(f"✗ 缺失表格：{table_name}")
    
    def check_required_formulas(self):
        """检查必需公式"""
        required_formulas = [
            ("中长期结算公式", r"40%.*60%|中长期.*结算 | 合约.*结算"),
            ("零售套餐公式", r"零售电价.*=|套餐.*公式 | 电费.*=.*\+"),
            ("偏差考核公式", r"偏差.*考核 | 考核.*费用 | 免考核"),
            ("现货结算公式", r"现货.*结算 | 日前.*结算 | 实时.*结算"),
            ("容量补偿公式", r"容量补偿 | 补偿.*标准"),
        ]
        
        for formula_name, pattern in required_formulas:
            if re.search(pattern, self.content, re.IGNORECASE):
                self.passed.append(f"✓ 公式完整：{formula_name}")
            else:
                self.warnings.append(f"⚠ 可能缺失公式：{formula_name}")
    
    def check_required_examples(self):
        """检查必需示例"""
        required_examples = [
            ("600MW 机组报价示例", r"600MW.*机组 | 10 段.*报价 | 段 1.*段 10"),
            ("零售套餐计算示例", r"固定电价套餐.*示例计算 | 峰谷分时.*示例计算 | 价格联动.*示例计算"),
            ("偏差考核示例", r"正偏差.*示例 | 负偏差.*示例 | 示例.*正偏差 | 示例.*负偏差"),
            ("结算示例", r"发电企业.*结算.*示例 | 用户.*结算.*示例 | 售电.*结算.*示例"),
        ]
        
        for example_name, pattern in required_examples:
            if re.search(pattern, self.content, re.IGNORECASE):
                self.passed.append(f"✓ 示例完整：{example_name}")
            else:
                self.issues.append(f"✗ 缺失示例：{example_name}")
    
    def check_key_parameters(self):
        """检查关键参数"""
        key_params = [
            ("燃煤基准价", r"燃煤.*基准价.*\d+\.\d+.*元/kWh|基准价.*\d+\.\d+"),
            ("容量补偿", r"容量补偿.*\d+\.\d+.*元 | 补偿标准.*\d+"),
            ("现货价格上限", r"现货.*上限.*\d+\.\d+|价格上限.*\d+"),
            ("现货价格下限", r"现货.*下限 | 负电价 | 价格下限"),
            ("签约比例", r"签约比例.*\d+\.\d+%|中长期.*\d+%"),
        ]
        
        for param_name, pattern in key_params:
            if re.search(pattern, self.content):
                self.passed.append(f"✓ 参数完整：{param_name}")
            else:
                self.issues.append(f"✗ 缺失参数：{param_name}（应包含具体数值）")
    
    def check_environmental_price(self):
        """检查环保电价参数（强制固化项，不可省略）
        
        山东范例 V13.0 实际内容：
        - 脱硫电价 0.015 元/kWh
        - 脱硝电价 0.010 元/kWh
        - 除尘电价 0.003 元/kWh（注意：V13.0 是 0.003，不是 0.002）
        - 燃煤上网标杆价 0.4229 元/kWh（基准价 + 环保电价）
        
        注意：V13.0 没有"环保电价合计"这一行，检查脚本不应强制要求
        """
        # 环保电价参数项（基于 V13.0 实际内容）
        env_params = [
            ("脱硫电价", r"脱硫.*电价.*\d+\.\d+.*元/kWh|脱硫.*\d+.*分/kWh|脱硫.*0\.015"),
            ("脱硝电价", r"脱硝.*电价.*\d+\.\d+.*元/kWh|脱硝.*\d+.*分/kWh|脱硝.*0\.01"),
            ("除尘电价", r"除尘.*电价.*\d+\.\d+.*元/kWh|除尘.*\d+.*分/kWh|除尘.*0\.00[23]"),
            # 移除"环保电价合计"检查，因为 V13.0 没有这一行
            ("燃煤上网标杆价", r"燃煤.*上网.*\d+\.\d+.*元/kWh|上网标杆价.*0\.4229"),
        ]
        
        for param_name, pattern in env_params:
            if re.search(pattern, self.content, re.IGNORECASE):
                self.passed.append(f"✓ 环保电价：{param_name}")
            else:
                # 检查是否有"待核实"标注
                if re.search(f"{param_name}.*待核实 | 待核实.*{param_name}", self.content, re.IGNORECASE):
                    self.warnings.append(f"⚠ 环保电价：{param_name}（标注为待核实）")
                else:
                    self.issues.append(f"✗ 环保电价：缺失{param_name}（必须包含，查不到写'待核实'，不可省略）")
    
    def check_policy_citations(self):
        """检查政策依据文号"""
        # 检查是否有文号格式
        policy_patterns = [
            r"〔20\d{2}〕\d+号",  # 标准文号格式
            r"\[20\d{2}\]\d+号",
            r"鲁发改能源.*号",
            r"鲁电交.*号",
            r"晋能源规.*号",
            r"豫发改.*号",
        ]
        
        has_citation = False
        for pattern in policy_patterns:
            if re.search(pattern, self.content):
                has_citation = True
                break
        
        if has_citation:
            self.passed.append("✓ 政策依据：包含文号标注")
        else:
            self.warnings.append("⚠ 政策依据：未找到文号标注（建议添加）")
    
    def check_retail_packages(self):
        """检查零售套餐分类（禁止套用固定格式，山东除外）"""
        # 检查是否是山东报告（山东允许使用"3 大类 9 小类"）
        is_shandong = bool(re.search(r"山东 | 鲁发改能源", self.content))
        
        # 禁止项：套用固定格式（山东除外）
        prohibited_patterns = []
        
        # 如果不是山东报告，额外检查固定格式
        if not is_shandong:
            prohibited_patterns.extend([
                (r"3 大类 9 小类", "❌ 套用'3 大类 9 小类'固定格式（每个省都不一样，必须按该省实际规则写）"),
                (r"固定价格类.*峰谷分时类.*价格联动类", "❌ 套用固定分类框架（应查询该省实际规则）"),
                (r"9 小类套餐", "❌ 套用'9 小类'固定说法（应查询该省实际规则）"),
            ])
        
        for pattern, error_msg in prohibited_patterns:
            if re.search(pattern, self.content, re.IGNORECASE):
                self.issues.append(f"✗ 零售套餐：{error_msg}")
        
        # 检查是否有该省实际的零售套餐规则
        retail_patterns = [
            ("零售套餐", r"零售套餐 | 零售交易"),
            ("套餐类型", r"套餐类型 | 套餐分类"),
            ("固定价格", r"固定价格.*套餐 | 固定电价.*套餐"),
        ]
        
        for item_name, pattern in retail_patterns:
            if re.search(pattern, self.content, re.IGNORECASE):
                self.passed.append(f"✓ 零售套餐：包含{item_name}")
            else:
                self.warnings.append(f"⚠ 零售套餐：可能缺失{item_name}")
    
    def check_deviation_assessment(self):
        """检查偏差考核内容"""
        deviation_items = [
            ("偏差考核", r"偏差考核 | 考核.*范围"),
            ("豁免情形", r"豁免 | 免考核"),
            ("预警机制", r"预警 | 蓝色.*黄色.*橙色.*红色"),
        ]
        
        for item_name, pattern in deviation_items:
            if re.search(pattern, self.content, re.IGNORECASE):
                self.passed.append(f"✓ 偏差考核：{item_name}")
            else:
                self.issues.append(f"✗ 偏差考核：缺失{item_name}")
    
    def check_internal_info(self):
        """检查是否包含内部信息（禁止项）
        
        山东范例 V13.0 实际内容：
        - 包含"报告编号"和"编制单位"（在文件头部）
        - 这些不是内部信息，是报告的元数据
        
        真正应该禁止的内部信息：
        - 编制说明（单独的章节）
        - 文件路径（如/Users/ls/...）
        - 验证重点（单独的章节）
        """
        internal_info_patterns = [
            ("编制说明", r"\*\*编制说明\*\*|## 编制说明 | 编制说明："),
            ("文件路径", r"文件路径：|`/Users/ls/"),
            ("验证重点", r"\*\*验证重点\*\*|## 验证重点 | 验证重点："),
            # 移除"报告编号"和"编制单位"检查，因为 V13.0 包含这些
        ]
        
        for item_name, pattern in internal_info_patterns:
            if re.search(pattern, self.content, re.IGNORECASE):
                self.issues.append(f"✗ 内部信息：包含{item_name}（应删除）")
            else:
                self.passed.append(f"✓ 内部信息：已删除{item_name}")
    
    def check_settlement_details(self):
        """检查结算章节详细程度（成功经验固化）"""
        settlement_items = [
            ("发电企业结算", r"发电企业.*结算 | 燃煤机组.*结算 | 新能源.*结算"),
            ("电力用户结算", r"电力用户.*结算 | 批发用户.*结算 | 零售用户.*结算"),
            ("售电公司结算", r"售电公司.*结算"),
            ("独立储能结算", r"独立储能.*结算 | 储能.*结算"),
            ("虚拟电厂结算", r"虚拟电厂.*结算"),
            ("结算公式", r"结算公式 | 结算电费.*="),
            ("示例计算", r"示例计算 | 假设.*数据"),
        ]
        
        for item_name, pattern in settlement_items:
            if re.search(pattern, self.content, re.IGNORECASE):
                self.passed.append(f"✓ 结算章节：包含{item_name}")
            else:
                self.warnings.append(f"⚠ 结算章节：可能缺失{item_name}")
    
    def check_province_specific_rules(self):
        """检查省份特色规则（禁止跨省套用）"""
        # 检查是否错误套用山东 40%+60% 结算（山西、广东等其他省不得套用）
        is_shandong = bool(re.search(r"山东 | 鲁发改能源", self.content))
        
        if not is_shandong:
            # 非山东报告，检查是否错误套用 40%+60%
            if re.search(r"40%.*\+.*60%.*结算 | 40%.*中长期.*60%.*现货", self.content):
                # 但如果是说明山东特色则允许
                if not re.search(r"山东.*40%.*60%|40%.*60%.*山东.*独有", self.content):
                    self.issues.append("✗ 省份特色：错误套用山东 40%+60% 结算机制（山东独有，其他省不得套用）")
                else:
                    self.passed.append("✓ 省份特色：正确标注 40%+60% 为山东独有")
            else:
                self.passed.append("✓ 省份特色：未套用山东 40%+60% 结算机制")
        
        # 检查零售套餐是否套用固定格式
        if not is_shandong:
            if re.search(r"3 大类 9 小类", self.content):
                self.issues.append("✗ 省份特色：套用山东'3 大类 9 小类'零售套餐格式（山东独有，其他省不得套用）")
            else:
                self.passed.append("✓ 省份特色：未套用山东'3 大类 9 小类'零售套餐格式")
    
    def check_content_reduction(self, reference_path=None):
        """检查内容是否被私自删减（新增·最高优先级）
        
        血泪教训：之前多次出现报告缩水 50% 以上的情况
        防止方法：与范例版本对比行数和字符数
        
        用户要求（2026-03-18）：
        - 在各省范例中记录用户满意版本的行数
        - 如果当前报告行数无故减少 1/3 以上，启动纠错机制
        - 确认遗漏后重新生成报告
        
        重要规则：
        - 每个省份的范例行数独立记录，不能混用！
        - 必须根据报告文件名自动识别省份
        - 使用该省份对应的范例行数作为基准
        """
        # 从报告文件名识别省份
        province = None
        filename = self.markdown_path.name
        if "山东" in filename:
            province = "山东"
        elif "山西" in filename:
            province = "山西"
        elif "河南" in filename:
            province = "河南"
        elif "广东" in filename:
            province = "广东"
        elif "江苏" in filename:
            province = "江苏"
        elif "安徽" in filename:
            province = "安徽"
        elif "浙江" in filename:
            province = "浙江"
        elif "河北" in filename:
            province = "河北"
        elif "甘肃" in filename:
            province = "甘肃"
        elif "福建" in filename:
            province = "福建"
        elif "四川" in filename:
            province = "四川"
        elif "江西" in filename:
            province = "江西"
        elif "辽宁" in filename:
            province = "辽宁"
        elif "陕西" in filename:
            province = "陕西"
        elif "湖南" in filename:
            province = "湖南"
        elif "湖北" in filename:
            province = "湖北"
        elif "北京" in filename:
            province = "北京"
        elif "上海" in filename:
            province = "上海"
        elif "天津" in filename:
            province = "天津"
        elif "重庆" in filename:
            province = "重庆"
        elif "内蒙古" in filename:
            province = "内蒙古"
        elif "广西" in filename:
            province = "广西"
        elif "西藏" in filename:
            province = "西藏"
        elif "宁夏" in filename:
            province = "宁夏"
        elif "新疆" in filename:
            province = "新疆"
        elif "青海" in filename:
            province = "青海"
        elif "黑龙江" in filename:
            province = "黑龙江"
        elif "吉林" in filename:
            province = "吉林"
        elif "海南" in filename:
            province = "海南"
        elif "贵州" in filename:
            province = "贵州"
        elif "云南" in filename:
            province = "云南"
        
        if not reference_path:
            # 根据省份查找对应的范例文件（优先使用 V13.0 或最新版本）
            if province:
                possible_paths = [
                    Path(f"/Users/ls/.openclaw/workspace-commander/docs/{province}省电力交易规则解析报告（2026 版）_V13.0.md"),
                    Path(f"/Users/ls/.openclaw/workspace-commander/docs/{province}省电力交易规则解析报告（2026 版）_V1.0.md"),
                    Path(f"/Users/ls/.openclaw/workspace-commander/docs/{province}电力交易规则解析报告（2026 版）_V13.0.md"),
                    Path(f"/Users/ls/.openclaw/workspace-commander/docs/{province}电力交易规则解析报告（2026 版）_V1.0.md"),
                ]
            else:
                # 无法识别省份时，默认使用山东范例
                possible_paths = [
                    Path("/Users/ls/.openclaw/workspace-commander/docs/山东省电力交易规则解析报告（2026 版）_V13.0.md"),
                ]
            
            reference_path = None
            for p in possible_paths:
                if p.exists():
                    reference_path = p
                    break
            
            if not reference_path:
                if province:
                    self.warnings.append(f"⚠ 防删减检查：未找到{province}省范例文件，跳过检查")
                else:
                    self.warnings.append("⚠ 防删减检查：未找到范例文件，跳过检查")
                return
        
        reference_content = reference_path.read_text(encoding='utf-8')
        reference_lines = len(reference_content.split('\n'))
        reference_chars = len(reference_content)
        
        actual_lines = len(self.lines)
        actual_chars = len(self.content)
        
        line_ratio = actual_lines / reference_lines
        char_ratio = actual_chars / reference_chars
        
        min_ratio = 0.70  # 允许 30% 的差异（用户要求 2026-03-18）
        critical_ratio = 0.67  # 严重删减阈值（减少 1/3 以上）
        
        print(f"\n防删减检查（参考：{reference_path.name}）：")
        print(f"  范例：{reference_lines} 行 / {reference_chars:,} 字符")
        print(f"  当前：{actual_lines} 行 / {actual_chars:,} 字符")
        print(f"  行数比例：{line_ratio:.1%}（要求≥70%，严重删减阈值<67%）")
        print(f"  字符比例：{char_ratio:.1%}（要求≥70%，严重删减阈值<67%）")
        
        # 检查是否严重删减（减少 1/3 以上）
        if line_ratio < critical_ratio or char_ratio < critical_ratio:
            self.issues.append(f"🔴 严重删减警报：行数缩水 {line_ratio:.1%} < {critical_ratio:.0%}（范例{reference_lines}行 → 当前{actual_lines}行，减少{reference_lines - actual_lines}行）")
            self.issues.append(f"🔴 严重删减警报：字符缩水 {char_ratio:.1%} < {critical_ratio:.0%}（范例{reference_chars:,}字符 → 当前{actual_chars:,}字符）")
            self.issues.append(f"🔴 纠错机制：检测到严重删减，必须重新生成报告！")
            self.issues.append(f"🔴 纠错机制：请检查是否遗漏章节、表格、示例、政策依据等内容")
        elif line_ratio < min_ratio:
            self.issues.append(f"✗ 内容删减：行数缩水 {line_ratio:.1%} < {min_ratio:.0%}（范例{reference_lines}行 → 当前{actual_lines}行）")
        else:
            self.passed.append(f"✓ 内容完整：行数 {line_ratio:.1%} ≥ {min_ratio:.0%}")
        
        if char_ratio < min_ratio:
            self.issues.append(f"✗ 内容删减：字符缩水 {char_ratio:.1%} < {min_ratio:.0%}（范例{reference_chars:,}字符 → 当前{actual_chars:,}字符）")
        else:
            self.passed.append(f"✓ 内容完整：字符 {char_ratio:.1%} ≥ {min_ratio:.0%}")


    def print_result(self):
        """输出检查结果"""
        print(f"\n检查结果：\n")
        
        # 通过项
        if self.passed:
            print(f"✅ 通过项 ({len(self.passed)}):")
            for item in self.passed[:20]:  # 只显示前 20 项
                print(f"  {item}")
            if len(self.passed) > 20:
                print(f"  ... 还有 {len(self.passed) - 20} 项通过")
            print()
        
        # 警告项
        if self.warnings:
            print(f"⚠️  警告项 ({len(self.warnings)}):")
            for item in self.warnings:
                print(f"  {item}")
            print()
        
        # 问题项
        if self.issues:
            print(f"❌ 问题项 ({len(self.issues)}):")
            for item in self.issues:
                print(f"  {item}")
            print()
        
        # 总结
        print(f"{'='*60}")
        total = len(self.passed) + len(self.warnings) + len(self.issues)
        print(f"总计检查：{total} 项")
        print(f"通过：{len(self.passed)} 项 | 警告：{len(self.warnings)} 项 | 问题：{len(self.issues)} 项")
        
        if len(self.issues) == 0:
            print(f"\n✅ 报告内容完整性检查通过！")
        else:
            print(f"\n❌ 报告内容不完整，需要补充 {len(self.issues)} 项内容")
        
        print(f"{'='*60}\n")



def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python check_report_completeness.py <markdown 文件路径>")
        sys.exit(1)
    
    markdown_path = sys.argv[1]
    checker = ReportChecker(markdown_path)
    passed = checker.check_all()
    
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
