#!/bin/bash
# 政策依据检查脚本（new-power-subjects-rule）

REPORT_FILE="$1"

if [ -z "$REPORT_FILE" ]; then
    echo "用法：$0 <报告文件>"
    exit 1
fi

echo "检查政策依据：$REPORT_FILE"
echo "======================================"

# 计数政策文号（格式：〔20XX〕XX 号）
POLICY_COUNT=$(grep -oE "〔20[0-9]{2}〕[0-9]+号" "$REPORT_FILE" | sort -u | wc -l)

echo "政策文号数量：$POLICY_COUNT"

# 检查是否有政策依据
if grep -q "〔20" "$REPORT_FILE"; then
    echo "✅ 有政策依据"
else
    echo "❌ 无政策依据"
fi

echo "======================================"

if [ $POLICY_COUNT -ge 10 ]; then
    echo "✅ 通过（≥10 个文件）"
elif [ $POLICY_COUNT -ge 8 ]; then
    echo "⚠️  警告（$POLICY_COUNT/10）"
else
    echo "❌ 失败（$POLICY_COUNT/10）"
fi
