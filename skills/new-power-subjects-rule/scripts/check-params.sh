#!/bin/bash
# 参数完整性检查脚本（new-power-subjects-rule）

REPORT_FILE="$1"

if [ -z "$REPORT_FILE" ]; then
    echo "用法：$0 <报告文件>"
    exit 1
fi

echo "检查参数完整性：$REPORT_FILE"
echo "======================================"

# 计数参数项数（估算：表格行数 + 关键参数提及）
PARAM_COUNT=$(grep -E "^\|.*\|.*\|.*\|" "$REPORT_FILE" | wc -l)

echo "表格行数（估算参数）：$PARAM_COUNT"

# 检查关键参数提及
check_param() {
    if grep -q "$1" "$REPORT_FILE"; then
        echo "✅ $2: 已提及"
        return 0
    else
        echo "❌ $2: 缺失"
        return 1
    fi
}

TOTAL=0
PASS=0

# 检查核心参数
((TOTAL++))
check_param "聚合容量" "聚合容量门槛" && ((PASS++))

((TOTAL++))
check_param "注册资本" "注册资本要求" && ((PASS++))

((TOTAL++))
check_param "注册流程" "注册流程" && ((PASS++))

((TOTAL++))
check_param "中长期" "中长期交易" && ((PASS++))

((TOTAL++))
check_param "现货" "现货市场" && ((PASS++))

((TOTAL++))
check_param "辅助服务" "辅助服务" && ((PASS++))

((TOTAL++))
check_param "结算" "结算规则" && ((PASS++))

((TOTAL++))
check_param "考核" "考核规则" && ((PASS++))

echo "======================================"
echo "核心参数：$PASS/$TOTAL ($(( PASS * 100 / TOTAL ))%)"

if [ $PARAM_COUNT -ge 60 ]; then
    echo "✅ 参数总量达标（≥60 项）"
else
    echo "⚠️  参数总量不足（$PARAM_COUNT/60）"
fi

if [ $(( PASS * 100 / TOTAL )) -ge 80 ]; then
    echo "✅ 通过（≥80%）"
elif [ $(( PASS * 100 / TOTAL )) -ge 60 ]; then
    echo "⚠️  警告（60%-80%）"
else
    echo "❌ 失败（<60%）"
fi
