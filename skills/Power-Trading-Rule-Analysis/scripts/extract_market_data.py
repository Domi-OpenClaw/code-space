#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电力市场月报/日报数据提取工具

功能：
1. 从 PDF 月报中提取关键数据（中长期签约比例、现货均价、辅助服务补偿等）
2. 从 PDF 日报中提取最新数据（日前/实时现货价、负荷、新能源出力等）
3. 输出 JSON 格式数据，供报告生成使用

依赖：
pip install pdfplumber pandas

使用示例：
python extract_market_data.py --province shandong --output data.json
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime, timedelta
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("错误：请先安装 pdfplumber 库")
    print("安装命令：pip install pdfplumber")
    sys.exit(1)


class MarketDataExtractor:
    """电力市场数据提取器"""
    
    def __init__(self, province: str, base_path: str = "/Users/ls/docs"):
        self.province = province
        self.base_path = Path(base_path)
        self.monthly_path = self.base_path / province / "monthly"
        self.daily_path = self.base_path / province / "daily"
        self.data = {
            "province": province,
            "extract_date": datetime.now().isoformat(),
            "monthly_data": {},
            "daily_data": {},
            "data_sources": []
        }
    
    def find_latest_monthly_report(self) -> Path:
        """查找最新月报"""
        if not self.monthly_path.exists():
            print(f"警告：月报目录不存在 {self.monthly_path}")
            return None
        
        pdf_files = list(self.monthly_path.glob("*.pdf"))
        if not pdf_files:
            print(f"警告：月报目录中没有 PDF 文件 {self.monthly_path}")
            return None
        
        # 按修改时间排序，取最新
        pdf_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        return pdf_files[0]
    
    def find_latest_daily_reports(self, count: int = 3) -> list:
        """查找最新 N 份日报"""
        if not self.daily_path.exists():
            print(f"警告：日报目录不存在 {self.daily_path}")
            return []
        
        pdf_files = list(self.daily_path.glob("*.pdf"))
        if not pdf_files:
            print(f"警告：日报目录中没有 PDF 文件 {self.daily_path}")
            return []
        
        # 按修改时间排序，取最新 N 个
        pdf_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        return pdf_files[:count]
    
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
            print(f"错误：无法解析 PDF {pdf_path}: {e}")
            return ""
    
    def extract_tables_from_pdf(self, pdf_path: Path) -> list:
        """从 PDF 提取所有表格"""
        try:
            tables = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_tables = page.extract_tables()
                    if page_tables:
                        tables.extend(page_tables)
            return tables
        except Exception as e:
            print(f"错误：无法提取 PDF 表格 {pdf_path}: {e}")
            return []
    
    def extract_percentage(self, text: str, keywords: list) -> str:
        """从文本中提取百分比数据"""
        for keyword in keywords:
            # 匹配"关键词 XX%"或"关键词 XX.X%"
            pattern = rf"{keyword}.*?(\d+\.?\d*)\s*%"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"{match.group(1)}%"
        return None
    
    def extract_price(self, text: str, keywords: list) -> str:
        """从文本中提取价格数据（元/kWh）"""
        for keyword in keywords:
            # 匹配"关键词 XX 元"或"关键词 XX.XX 元"
            pattern = rf"{keyword}.*?(\d+\.?\d*)\s*元"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"{match.group(1)}元/kWh"
        return None
    
    def extract_monthly_data(self, pdf_path: Path) -> dict:
        """从月报中提取关键数据"""
        if not pdf_path:
            return {}
        
        print(f"\n正在处理月报：{pdf_path.name}")
        text = self.extract_text_from_pdf(pdf_path)
        tables = self.extract_tables_from_pdf(pdf_path)
        
        if not text:
            print(f"  警告：无法从月报提取文本")
            return {}
        
        data = {}
        
        # 1. 中长期签约比例
        ratio = self.extract_percentage(text, ["中长期签约", "中长期合同", "签约电量占比"])
        if ratio:
            data["中长期签约比例"] = ratio
        
        # 2. 月度集中竞价均价
        price = self.extract_price(text, ["月度集中竞价", "集中竞价均价", "竞价均价"])
        if price:
            data["月度集中竞价均价"] = price
        
        # 3. 双边协商均价
        price = self.extract_price(text, ["双边协商", "协商均价"])
        if price:
            data["双边协商均价"] = price
        
        # 4. 现货月度均价
        price = self.extract_price(text, ["现货月度均价", "现货均价", "现货市场均价"])
        if price:
            data["现货月度均价"] = price
        
        # 5. 现货最高价
        price = self.extract_price(text, ["现货最高价", "最高出清价", "峰值电价"])
        if price:
            data["现货最高价"] = price
        
        # 6. 现货最低价
        price = self.extract_price(text, ["现货最低价", "最低出清价", "谷值电价"])
        if price:
            data["现货最低价"] = price
        
        # 7. 新能源弃电率
        wind_ratio = self.extract_percentage(text, ["风电弃电", "风电弃风"])
        pv_ratio = self.extract_percentage(text, ["光伏弃电", "光伏弃光"])
        if wind_ratio or pv_ratio:
            弃电率 = []
            if wind_ratio:
                弃电率.append(f"风电{wind_ratio}")
            if pv_ratio:
                弃电率.append(f"光伏{pv_ratio}")
            data["新能源弃电率"] = "，".join(弃电率)
        
        # 8. 调频补偿总额
        compensation = self.extract_money(text, ["调频补偿", "AGC 补偿"])
        if compensation:
            data["调频补偿总额"] = compensation
        
        # 9. 调峰补偿总额
        compensation = self.extract_money(text, ["调峰补偿", "备用补偿"])
        if compensation:
            data["调峰补偿总额"] = compensation
        
        # 10. 偏差考核电量
        energy = self.extract_energy(text, ["偏差考核电量", "考核电量"])
        if energy:
            data["偏差考核电量"] = energy
        
        # 11. 偏差考核费用
        money = self.extract_money(text, ["偏差考核费用", "考核费用"])
        if money:
            data["偏差考核费用"] = money
        
        # 12. 市场成员数量
        count = self.extract_count(text, ["售电公司", "市场主体"])
        if count:
            data["市场成员数量"] = count
        
        # 记录数据源
        data["数据来源"] = pdf_path.name
        data["提取时间"] = datetime.now().isoformat()
        
        return data
    
    def extract_daily_data(self, pdf_path: Path) -> dict:
        """从日报中提取关键数据"""
        if not pdf_path:
            return {}
        
        print(f"  正在处理日报：{pdf_path.name}")
        text = self.extract_text_from_pdf(pdf_path)
        
        if not text:
            return {}
        
        data = {}
        
        # 1. 日前现货均价
        price = self.extract_price(text, ["日前现货", "日前均价", "日前出清价"])
        if price:
            data["日前现货均价"] = price
        
        # 2. 实时现货均价
        price = self.extract_price(text, ["实时现货", "实时均价", "实时出清价"])
        if price:
            data["实时现货均价"] = price
        
        # 3. 最大负荷
        load = self.extract_load(text, ["最大负荷", "最高负荷", "负荷峰值"])
        if load:
            data["最大负荷"] = load
        
        # 4. 最小负荷
        load = self.extract_load(text, ["最小负荷", "最低负荷", "负荷谷值"])
        if load:
            data["最小负荷"] = load
        
        # 5. 新能源最大出力
        wind = self.extract_capacity(text, ["风电最大", "风电出力"])
        pv = self.extract_capacity(text, ["光伏最大", "光伏出力"])
        if wind or pv:
            出力 = []
            if wind:
                出力.append(f"风电{wind}")
            if pv:
                出力.append(f"光伏{pv}")
            data["新能源最大出力"] = "，".join(出力)
        
        # 6. 外受电电量
        energy = self.extract_energy(text, ["外受电", "外购电", "省外来电"])
        if energy:
            data["外受电电量"] = energy
        
        # 记录数据源
        data["数据来源"] = pdf_path.name
        data["提取时间"] = datetime.now().isoformat()
        
        return data
    
    def extract_money(self, text: str, keywords: list) -> str:
        """从文本中提取金额数据（万元/亿元）"""
        for keyword in keywords:
            # 匹配"关键词 XX 万元"或"关键词 XX 亿元"
            pattern = rf"{keyword}.*?(\d+\.?\d*)\s*(万元 | 亿元)"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"{match.group(1)}{match.group(2)}"
        return None
    
    def extract_energy(self, text: str, keywords: list) -> str:
        """从文本中提取电量数据（亿千瓦时/万千瓦时）"""
        for keyword in keywords:
            pattern = rf"{keyword}.*?(\d+\.?\d*)\s*(亿千瓦时 | 万千瓦时|MWh)"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"{match.group(1)}{match.group(2)}"
        return None
    
    def extract_load(self, text: str, keywords: list) -> str:
        """从文本中提取负荷数据（万千瓦/MW）"""
        for keyword in keywords:
            pattern = rf"{keyword}.*?(\d+\.?\d*)\s*(万千瓦|MW|GW)"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"{match.group(1)}{match.group(2)}"
        return None
    
    def extract_capacity(self, text: str, keywords: list) -> str:
        """从文本中提取容量/出力数据（万千瓦/MW）"""
        for keyword in keywords:
            pattern = rf"{keyword}.*?(\d+\.?\d*)\s*(万千瓦|MW|GW)"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"{match.group(1)}{match.group(2)}"
        return None
    
    def extract_count(self, text: str, keywords: list) -> str:
        """从文本中提取数量数据"""
        for keyword in keywords:
            pattern = rf"{keyword}.*?(\d+)\s*(家 | 个|户)"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"{match.group(1)}{match.group(2)}"
        return None
    
    def extract_all(self) -> dict:
        """提取所有数据（月报 + 日报）"""
        print(f"\n{'='*60}")
        print(f"电力市场数据提取工具 - {self.province}")
        print(f"{'='*60}")
        
        # 提取月报数据
        monthly_pdf = self.find_latest_monthly_report()
        if monthly_pdf:
            self.data["monthly_data"] = self.extract_monthly_data(monthly_pdf)
            self.data["data_sources"].append(str(monthly_pdf))
        else:
            print("警告：未找到月报文件，跳过月报数据提取")
        
        # 提取日报数据
        daily_pdfs = self.find_latest_daily_reports(count=3)
        if daily_pdfs:
            daily_data_list = []
            for pdf in daily_pdfs:
                daily_data = self.extract_daily_data(pdf)
                if daily_data:
                    daily_data_list.append(daily_data)
                    self.data["data_sources"].append(str(pdf))
            
            # 计算日报平均值
            if daily_data_list:
                self.data["daily_data"] = self.aggregate_daily_data(daily_data_list)
        else:
            print("警告：未找到日报文件，跳过日报数据提取")
        
        print(f"\n{'='*60}")
        print(f"数据提取完成")
        print(f"{'='*60}")
        
        return self.data
    
    def aggregate_daily_data(self, daily_data_list: list) -> dict:
        """聚合多份日报数据（取平均值或最新值）"""
        if not daily_data_list:
            return {}
        
        aggregated = {
            "日报数量": len(daily_data_list),
            "数据范围": f"{daily_data_list[-1].get('数据来源', '未知')} 至 {daily_data_list[0].get('数据来源', '未知')}"
        }
        
        # 对数值型数据取平均
        numeric_fields = ["日前现货均价", "实时现货均价"]
        for field in numeric_fields:
            values = []
            for daily in daily_data_list:
                if field in daily:
                    # 提取数值
                    match = re.search(r"(\d+\.?\d*)", daily[field])
                    if match:
                        values.append(float(match.group(1)))
            
            if values:
                avg = sum(values) / len(values)
                aggregated[f"{field}（平均）"] = f"{avg:.3f}元/kWh"
        
        # 其他字段取最新值
        for key in ["最大负荷", "最小负荷", "新能源最大出力", "外受电电量"]:
            if key in daily_data_list[0]:
                aggregated[key] = daily_data_list[0][key]
        
        return aggregated
    
    def save_to_json(self, output_path: str):
        """保存数据到 JSON 文件"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print(f"\n数据已保存到：{output_path}")
    
    def print_summary(self):
        """打印数据摘要"""
        print(f"\n{'='*60}")
        print("数据摘要")
        print(f"{'='*60}")
        
        if self.data.get("monthly_data"):
            print(f"\n【月报数据】{self.data['monthly_data'].get('数据来源', '未知')}")
            for key, value in self.data["monthly_data"].items():
                if key not in ["数据来源", "提取时间"]:
                    print(f"  {key}: {value}")
        
        if self.data.get("daily_data"):
            print(f"\n【日报数据】{self.data['daily_data'].get('数据范围', '未知')}")
            for key, value in self.data["daily_data"].items():
                if key not in ["日报数量", "数据范围"]:
                    print(f"  {key}: {value}")
        
        print(f"\n数据源文件:")
        for source in self.data.get("data_sources", []):
            print(f"  - {source}")


def main():
    parser = argparse.ArgumentParser(description="电力市场月报/日报数据提取工具")
    parser.add_argument("--province", type=str, required=True, help="省份名称（如 shandong）")
    parser.add_argument("--output", type=str, default="market_data.json", help="输出 JSON 文件路径")
    parser.add_argument("--base-path", type=str, default="/Users/ls/docs", help="基础路径")
    
    args = parser.parse_args()
    
    extractor = MarketDataExtractor(
        province=args.province,
        base_path=args.base_path
    )
    
    # 提取数据
    data = extractor.extract_all()
    
    # 打印摘要
    extractor.print_summary()
    
    # 保存到 JSON
    extractor.save_to_json(args.output)
    
    return data


if __name__ == "__main__":
    main()
