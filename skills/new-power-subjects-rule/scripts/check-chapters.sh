#!/bin/bash
# 章节完整性检查脚本（new-power-subjects-rule）

REPORT_FILE="$1"

if [ -z "$REPORT_FILE" ]; then
    echo "用法：$0 <报告文件>"
    exit 1
fi

echo "检查章节完整性：$REPORT_FILE"
echo "======================================"

TOTAL=7
PASS=0

# 检查 7 章
check_chapter() {
    if grep -q "$1" "$REPORT_FILE"; then
        echo "✅ 第$2 章：$3"
        ((PASS++))
        return 0
    else
        echo "❌ 第$2 章：$3 缺失"
        return 1
    fi
}

check_chapter "第一章\|第 1 章" "1" "新型主体基本情况"
check_chapter "第二章\|第 2 章" "2" "市场准入规则"
check_chapter "第三章\|第 3 章" "3" "交易规则"
check_chapter "第四章\|第 4 章" "4" "调度与运营"
check_chapter "第五章\|第 5 章" "5" "结算规则"
check_chapter "第六章\|第 6 章" "6" "地方政策红利"
check_chapter "第七章\|第 7 章" "7" "实操要点"

echo "======================================"
echo "章节完整性：$PASS/$TOTAL ($(( PASS * 100 / TOTAL ))%)"

if [ $(( PASS * 100 / TOTAL )) -ge 100 ]; then
    echo "✅ 通过（7 章完整）"
elif [ $(( PASS * 100 / TOTAL )) -ge 80 ]; then
    echo "⚠️  警告（缺少$((TOTAL-PASS)) 章）"
else
    echo "❌ 失败（缺少$((TOTAL-PASS)) 章）"
fi
