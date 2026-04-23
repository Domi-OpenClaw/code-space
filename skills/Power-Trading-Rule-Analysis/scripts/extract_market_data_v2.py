#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电力市场月报/日报数据提取工具（增强版 - 支持月度对比）

功能：
1. 从 PDF 月报中提取关键数据（中长期签约比例、现货均价、辅助服务补偿等）
2. 从 PDF 日报中提取最新数据（日前/实时现货价、负荷、新能源出力等）
3. 月度对比分析（月报历史趋势 + 日报当月对比）
4. 输出 JSON 格式数据，供报告生成使用

依赖：
pip install pdfplumber pandas

使用示例：
python extract_market_data_v2.py --province shandong --output data.json --compare
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import pdfplumber
except ImportError:
    print("错误：请先安装 pdfplumber 库")
    print("安装命令：pip install pdfplumber")
    sys.exit(1)


class MarketDataExtractor:
    """电力市场数据提取器（增强版）"""
    
    def __init__(self, province: str, base_path: str = "/Users/ls/docs"):
        self.province = province
        self.base_path = Path(base_path)
        self.monthly_path = self.base_path / province / "monthly"
        self.daily_path = self.base_path / province / "daily"
        self.data = {
            "province": province,
            "extract_date": datetime.now().isoformat(),
            "monthly_data": {},
            "monthly_comparison": {},  # 新增：月度对比
            "daily_data": {},
            "daily_comparison": {},    # 新增：日报当月对比
            "data_sources": []
        }
    
    def find_all_monthly_reports(self) -> List[Path]:
        """查找所有月份月报（按月排序）"""
        if not self.monthly_path.exists():
            print(f"⚠️ 月报目录不存在：{self.monthly_path}")
            return []
        
        reports = []
        pdf_files = list(self.monthly_path.glob("*.pdf"))
        print(f"📂 找到 {len(pdf_files)} 个月报 PDF 文件")
        
        for f in pdf_files:
            # 提取月份信息（如"2026 年 1 月份"）
            match = re.search(r'(\d{4})年(\d+)月', f.name)
            if match:
                year, month = int(match.group(1)), int(match.group(2))
                reports.append((year, month, f))
                print(f"  ✓ {f.name} → {year}年{month}月")
            else:
                print(f"  ⚠️ 无法解析月份：{f.name}")
        
        # 按年月排序
        reports.sort(key=lambda x: (x[0], x[1]))
        return [r[2] for r in reports]
    
    def find_latest_monthly_report(self) -> Optional[Path]:
        """查找最新月报"""
        reports = self.find_all_monthly_reports()
        return reports[-1] if reports else None
    
    def find_daily_reports_current_month(self) -> List[Path]:
        """查找当月所有日报"""
        if not self.daily_path.exists():
            return []
        
        current_month = datetime.now().strftime("%Y 年 %-m 月")
        reports = []
        for f in self.daily_path.glob("*.pdf"):
            # 检查是否属于当月
            if current_month in f.name:
                reports.append(f)
        
        # 按日期排序（从文件名提取日期）
        def extract_date(path):
            match = re.search(r'(\d{1,2}) 月 (\d{1,2}) 日', path.name)
            if match:
                return int(match.group(1)), int(match.group(2))
            return (0, 0)
        
        reports.sort(key=extract_date)
        return reports
    
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """从 PDF 提取文本"""
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            print(f"⚠️ 读取 PDF 失败：{pdf_path} - {e}")
            return ""
    
    def extract_monthly_data(self, pdf_path: Path) -> Dict:
        """从单个月报提取数据"""
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return {}
        
        # 提取月份
        month_match = re.search(r'(\d{4})年(\d+)月', pdf_path.name)
        month_str = f"{month_match.group(1)}-{int(month_match.group(2)):02d}" if month_match else "未知"
        
        data = {"月份": month_str, "数据来源": pdf_path.name}
        
        # 关键词匹配提取（简化版示例）
        patterns = {
            "中长期签约比例": r'中长期签约比例 [：:]\s*(\d+\.?\d*)\s*%',
            "月度集中竞价均价": r'月度集中竞价 [均价|价格][：:]\s*(\d+\.?\d*)\s*元/MWh',
            "现货月度均价": r'现货 [月度] 均价 [：:]\s*(\d+\.?\d*)\s*元/MWh',
            "新能源弃电率": r'新能源弃电率 [：:]\s*(\d+\.?\d*)\s*%',
            "偏差考核费用": r'偏差考核费用 [：:]\s*(\d+\.?\d*)\s*万元',
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, text)
            data[key] = float(match.group(1)) if match else None
        
        return data
    
    def extract_all_monthly_data(self) -> Dict:
        """提取所有月报数据并生成对比"""
        reports = self.find_all_monthly_reports()
        if not reports:
            return {}
        
        all_data = []
        for report in reports:
            data = self.extract_monthly_data(report)
            if data:
                all_data.append(data)
        
        # 生成对比分析
        comparison = self._generate_monthly_comparison(all_data)
        
        return {
            "reports": all_data,
            "comparison": comparison,
            "report_count": len(all_data)
        }
    
    def _generate_monthly_comparison(self, monthly_data: List[Dict]) -> Dict:
        """生成月度对比分析"""
        if len(monthly_data) < 2:
            return {"status": "数据不足，无法对比"}
        
        comparison = {
            "trend_analysis": {},
            "month_over_month": [],  # 环比
            "key_metrics": []
        }
        
        # 计算环比变化
        for i in range(1, len(monthly_data)):
            prev = monthly_data[i-1]
            curr = monthly_data[i]
            
            change = {
                "period": f"{prev.get('月份', '?')} → {curr.get('月份', '?')}",
                "metrics": {}
            }
            
            # 对比关键指标
            for key in ["中长期签约比例", "现货月度均价", "新能源弃电率", "偏差考核费用"]:
                if curr.get(key) and prev.get(key):
                    pct_change = ((curr[key] - prev[key]) / prev[key]) * 100
                    change["metrics"][key] = {
                        "prev": prev[key],
                        "curr": curr[key],
                        "change": round(pct_change, 2),
                        "trend": "↑" if pct_change > 0 else "↓" if pct_change < 0 else "→"
                    }
            
            comparison["month_over_month"].append(change)
        
        # 趋势分析
        if len(monthly_data) >= 3:
            comparison["trend_analysis"] = {
                "status": "已启用",
                "periods": len(monthly_data),
                "description": f"基于{len(monthly_data)}个月数据进行趋势分析"
            }
        
        return comparison
    
    def extract_daily_data(self) -> Dict:
        """提取当月日报数据并生成对比"""
        reports = self.find_daily_reports_current_month()
        if not reports:
            return {}
        
        all_data = []
        for report in reports:
            text = self.extract_text_from_pdf(report)
            if not text:
                continue
            
            # 提取日期
            date_match = re.search(r'(\d{1,2}) 月 (\d{1,2}) 日', report.name)
            date_str = f"{date_match.group(1)}-{date_match.group(2):02d}" if date_match else "未知"
            
            data = {"日期": date_str, "数据来源": report.name}
            
            # 关键词匹配
            patterns = {
                "日前现货均价": r'日前现货 [均价|价格][：:]\s*(\d+\.?\d*)\s*元/MWh',
                "实时现货均价": r'实时现货 [均价|价格][：:]\s*(\d+\.?\d*)\s*元/MWh',
                "最大负荷": r'最大负荷 [：:]\s*(\d+\.?\d*)\s*万千瓦',
                "新能源最大出力": r'新能源最大出力 [：:]\s*(\d+\.?\d*)\s*万千瓦',
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, text)
                data[key] = float(match.group(1)) if match else None
            
            all_data.append(data)
        
        # 生成当月对比
        comparison = self._generate_daily_comparison(all_data)
        
        return {
            "reports": all_data,
            "comparison": comparison,
            "report_count": len(all_data),
            "数据范围": f"当月 ({len(all_data)}天)"
        }
    
    def _generate_daily_comparison(self, daily_data: List[Dict]) -> Dict:
        """生成日报当月对比分析"""
        if len(daily_data) < 2:
            return {"status": "数据不足，无法对比"}
        
        comparison = {
            "daily_trend": [],
            "extremes": {},
            "volatility": {}
        }
        
        # 找出极值
        for key in ["日前现货均价", "实时现货均价", "最大负荷", "新能源最大出力"]:
            values = [(d["日期"], d[key]) for d in daily_data if d.get(key)]
            if values:
                max_val = max(values, key=lambda x: x[1])
                min_val = min(values, key=lambda x: x[1])
                comparison["extremes"][key] = {
                    "max": {"date": max_val[0], "value": max_val[1]},
                    "min": {"date": min_val[0], "value": min_val[1]},
                    "range": round(max_val[1] - min_val[1], 2)
                }
        
        # 计算波动率
        for key in ["日前现货均价", "实时现货均价"]:
            values = [d[key] for d in daily_data if d.get(key)]
            if len(values) >= 2:
                avg = sum(values) / len(values)
                std_dev = (sum((x - avg) ** 2 for x in values) / len(values)) ** 0.5
                comparison["volatility"][key] = {
                    "avg": round(avg, 2),
                    "std_dev": round(std_dev, 2),
                    "volatility_rate": round((std_dev / avg) * 100, 2) if avg else 0
                }
        
        return comparison
    
    def extract_all(self, compare: bool = True) -> Dict:
        """提取所有数据（可选对比分析）"""
        # 提取月报数据
        monthly_result = self.extract_all_monthly_data()
        if monthly_result:
            self.data["monthly_data"] = monthly_result["reports"][-1] if monthly_result["reports"] else {}
            if compare:
                self.data["monthly_comparison"] = monthly_result["comparison"]
        
        # 提取日报数据
        daily_result = self.extract_daily_data()
        if daily_result:
            self.data["daily_data"] = daily_result
            if compare:
                self.data["daily_comparison"] = daily_result["comparison"]
        
        # 记录数据源
        self.data["data_sources"] = [
            str(self.monthly_path),
            str(self.daily_path)
        ]
        
        return self.data
    
    def save_to_json(self, output_path: str):
        """保存到 JSON 文件"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print(f"✅ 数据已保存：{output_path}")
    
    def print_comparison_report(self):
        """打印对比分析报告"""
        print(f"\n{'='*80}")
        print("📊 电力市场月度对比分析报告")
        print(f"{'='*80}")
        
        # 月报对比
        if self.data.get("monthly_comparison"):
            print(f"\n【月报历史趋势】")
            comp = self.data["monthly_comparison"]
            if isinstance(comp, dict) and comp.get("status") == "数据不足，无法对比":
                print("  ⚠️ 数据不足，无法生成月度对比（需要至少 2 个月报）")
            else:
                mom = comp.get("month_over_month", [])
                for change in mom:
                    print(f"\n  {change['period']}:")
                    for metric, vals in change.get("metrics", {}).items():
                        print(f"    {metric}: {vals['prev']} → {vals['curr']} ({vals['trend']} {vals['change']:+.2f}%)")
        
        # 日报对比
        if self.data.get("daily_comparison"):
            print(f"\n【日报当月对比】")
            comp = self.data["daily_comparison"]
            if isinstance(comp, dict) and comp.get("status") == "数据不足，无法对比":
                print("  ⚠️ 数据不足，无法生成当月对比（需要至少 2 天日报）")
            else:
                extremes = comp.get("extremes", {})
                for metric, vals in extremes.items():
                    print(f"\n  {metric}:")
                    print(f"    最高：{vals['max']['value']} ({vals['max']['date']})")
                    print(f"    最低：{vals['min']['value']} ({vals['min']['date']})")
                    print(f"    波动范围：{vals['range']}")
                
                volatility = comp.get("volatility", {})
                for metric, vals in volatility.items():
                    print(f"\n  {metric} 波动分析:")
                    print(f"    平均值：{vals['avg']}")
                    print(f"    标准差：{vals['std_dev']}")
                    print(f"    波动率：{vals['volatility_rate']}%")
        
        print(f"\n{'='*80}\n")


def main():
    parser = argparse.ArgumentParser(description="电力市场月报/日报数据提取工具（增强版）")
    parser.add_argument("--province", type=str, required=True, help="省份名称（如 shandong）")
    parser.add_argument("--output", type=str, default="market_data.json", help="输出 JSON 文件路径")
    parser.add_argument("--base-path", type=str, default="/Users/ls/docs", help="基础路径")
    parser.add_argument("--compare", action="store_true", default=True, help="启用对比分析（默认开启）")
    parser.add_argument("--no-compare", action="store_true", help="禁用对比分析")
    
    args = parser.parse_args()
    
    extractor = MarketDataExtractor(
        province=args.province,
        base_path=args.base_path
    )
    
    # 提取数据
    compare = not args.no_compare
    data = extractor.extract_all(compare=compare)
    
    # 打印对比报告
    if compare:
        extractor.print_comparison_report()
    
    # 保存到 JSON
    extractor.save_to_json(args.output)
    
    return data


if __name__ == "__main__":
    main()
