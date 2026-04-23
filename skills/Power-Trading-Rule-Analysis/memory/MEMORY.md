# Power-Trading-Rule-Analysis Skill 概要

## 核心定位
电力交易规则分析 BCF 层业务专家 Skill，支撑省级电力市场报告生成。

## 版本
V12.0.0

## 核心架构
**8 个独立 Tool**（各管一章，可独立调用）：
1. market-entities-analyzer — 市场主体（准入+注册）
2. medium-long-term-trading-analyzer — 中长期交易（9种方式+出清）
3. spot-market-analyzer — 现货市场（RUC/EC+LMP）
4. retail-package-analyzer — 零售市场（多维套餐+价格封顶）
5. green-power-trading-analyzer — 绿电交易（品种+认证）
6. metering-settlement-analyzer — 计量结算（流程+分摊）
7. deviation-assessment-analyzer — 偏差考核（四级预警+豁免）
8. ancillary-services-analyzer — 辅助服务（调频/备用/调峰）

## 关键规则
- 禁止跨省套用分类，每省按实际政策
- 政策标注须有文号，禁止模糊引用
- 零售套餐多维分类：价格机制×能源类型×周期×用户类型×特殊机制×结算方式

## 范例库
`examples/` 目录含山东/江苏/贵州/河南等省报告，生成前对标参数项数

## 质量标准
长报告（>800行）须主会话直接生成，不依赖子任务自动完成
