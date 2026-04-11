// 知识库图谱数据
// 由 knowledge-index.md 自动生成
const KNOWLEDGE_DATA = {
  nodes: [
    // ========== 朗新科技 ==========
    {
      id: "lx-1",
      label: "朗新科技集团中文画册（2025版）",
      category: "朗新科技",
      summary: "总部位于无锡，拥有1.4万政企客户、5亿用户覆盖、31省区、15个国家业务布局",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#lx-1",
      connections: 3
    },
    {
      id: "lx-2",
      label: "朗新AI研究院核心能力",
      category: "朗新科技",
      summary: "2023年成立，专注于时序预测、大模型、多模态、AIGC等核心能力，充电站收益增长15%",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#lx-2",
      connections: 3
    },
    {
      id: "lx-3",
      label: "朗新核心业务场景",
      category: "朗新科技",
      summary: "涵盖聚合充电（新电途）、电力市场化交易、虚拟电厂、光伏云等核心业务场景",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#lx-3",
      connections: 5
    },
    {
      id: "lx-4",
      label: "朗新科技发展历程",
      category: "朗新科技",
      summary: "1996北京创立→2006无锡→2013创业板上市→2017支付宝合作→2019双轨战略→2023 AI研究院",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#lx-4",
      connections: 1
    },
    {
      id: "lx-5",
      label: "朗新虚拟电厂产品",
      category: "朗新科技",
      summary: "城市新型基础设施，支持负荷型/电源型/混合型，收益来源：电力市场+辅助服务+需求响应",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#lx-5",
      connections: 2
    },

    // ========== 可信数据空间 ==========
    {
      id: "td-1",
      label: "可信数据空间定义与定位",
      category: "可信数据空间",
      summary: "国家级数据流通基础设施，实现「供得出、流得动、用得好、保安全」四大目标",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#td-1",
      connections: 2
    },
    {
      id: "td-2",
      label: "可信数据空间核心技术体系",
      category: "可信数据空间",
      summary: "包含可信管控（区块链+智能合约）、隐私计算（TEE/MPC/联邦学习）、连接器、数据治理",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#td-2",
      connections: 2
    },
    {
      id: "td-3",
      label: "可信数据空间市场特征",
      category: "可信数据空间",
      summary: "单项目规模2000万+，政策密集出台，技术门槛高，目标2028年建设100个可信数据空间",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#td-3",
      connections: 5
    },
    {
      id: "td-4",
      label: "行业类可信数据空间招标项目",
      category: "可信数据空间",
      summary: "典型项目：国家管网1664万、山西2500万、湖南TEE+MPC技术路线",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#td-4",
      connections: 1
    },
    {
      id: "td-5",
      label: "城市级可信数据空间招标项目",
      category: "可信数据空间",
      summary: "典型项目：雄安3200万、德州2087万、呼和浩特3591万",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#td-5",
      connections: 1
    },
    {
      id: "td-6",
      label: "南网数据开放目录(149项)",
      category: "可信数据空间",
      summary: "发布于dm.csg.cn，涵盖治理、经济、绿色低碳、民生四大类，160+跨行业数据",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#td-6",
      connections: 2
    },
    {
      id: "td-7",
      label: "南网可信数据空间注册入驻",
      category: "可信数据空间",
      summary: "入驻平台data.csg.cn，需邀请码，3工作日内完成审核",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#td-7",
      connections: 1
    },

    // ========== 充电桩 ==========
    {
      id: "cd-1",
      label: "充电桩选址大数据服务",
      category: "充电桩",
      summary: "基于城市经济、新能源车保有量、热力图、供需缺口分析，提供定容推荐服务",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#cd-1",
      connections: 3
    },
    {
      id: "cd-2",
      label: "充电AI智能选址产品",
      category: "充电桩",
      summary: "多维时空大数据+AI模型融合，秒出选址报告，智能推荐最优位置",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#cd-2",
      connections: 3
    },
    {
      id: "cd-3",
      label: "充电桩选址合作协议",
      category: "充电桩",
      summary: "2000次查询额度，合同期1年，违约金每日万分之五",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#cd-3",
      connections: 1
    },

    // ========== 虚拟电厂 ==========
    {
      id: "vp-1",
      label: "虚拟电厂产品解决方案",
      category: "虚拟电厂",
      summary: "源网荷储一体化，实现削峰填谷、辅助服务、电力市场化交易三大功能",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#vp-1",
      connections: 3
    },
    {
      id: "vp-2",
      label: "园区微电网能源运营",
      category: "虚拟电厂",
      summary: "聚合光伏、储能、充电桩，度电成本从0.85元降至0.57元",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#vp-2",
      connections: 2
    },

    // ========== 数据基础设施标准 ==========
    {
      id: "ndi-1",
      label: "NDI互联互通基本要求",
      category: "数据基础设施",
      summary: "数据登记→上架→目录上报→下发→发现→交互，6步标准化流程",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#ndi-1",
      connections: 3
    },
    {
      id: "ndi-2",
      label: "NDI用户身份管理规范",
      category: "数据基础设施",
      summary: "覆盖接入主体、连接器、平台身份注册认证全链路",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#ndi-2",
      connections: 1
    },
    {
      id: "ndi-3",
      label: "数据基础设施区域功能节点",
      category: "数据基础设施",
      summary: "具备身份管理、标识管理、目录管理等核心能力",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#ndi-3",
      connections: 1
    },
    {
      id: "ndi-4",
      label: "「数据要素×」三年行动计划",
      category: "数据基础设施",
      summary: "目标2026年建设300+示范场景，数据产业年均增速超20%",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#ndi-4",
      connections: 2
    },

    // ========== 补充扩展节点（丰富图谱） ==========
    {
      id: "lx-6",
      label: "新电途聚合充电网络",
      category: "朗新科技",
      summary: "覆盖全国主要城市的聚合充电网络，连接多家运营商，提供统一支付和服务",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#lx-6",
      connections: 2
    },
    {
      id: "lx-7",
      label: "电力市场化交易平台",
      category: "朗新科技",
      summary: "支持电力现货交易、中长期交易、辅助服务交易的全场景交易平台",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#lx-7",
      connections: 2
    },
    {
      id: "lx-8",
      label: "光伏云平台",
      category: "朗新科技",
      summary: "分布式光伏电站监控、运维、发电预测的一体化云平台",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#lx-8",
      connections: 1
    },
    {
      id: "td-8",
      label: "数据要素市场政策体系",
      category: "可信数据空间",
      summary: "国家数据局主导的「数据要素×」行动计划，构建数据流通顶层设计",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#td-8",
      connections: 2
    },
    {
      id: "vp-3",
      label: "负荷聚合商运营",
      category: "虚拟电厂",
      summary: "聚合工业负荷、商业负荷、居民负荷，参与电网调峰调频",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#vp-3",
      connections: 2
    },
    {
      id: "ndi-5",
      label: "数据登记与确权",
      category: "数据基础设施",
      summary: "数据资产登记、数据确权、数据质量评估全流程规范",
      source: "knowledge-index.md",
      url: "https://cdn.jsdelivr.net/gh/Domi-OpenClaw/code-space@main/knowledge-index.md#ndi-5",
      connections: 1
    }
  ],

  links: [
    // 朗新科技内部关联
    { source: "lx-2", target: "lx-3", relation: "研发支撑业务" },
    { source: "lx-1", target: "lx-2", relation: "内容关联" },
    { source: "lx-1", target: "lx-3", relation: "内容关联" },
    { source: "lx-1", target: "lx-6", relation: "产品关联" },
    { source: "lx-3", target: "lx-6", relation: "业务关联" },
    { source: "lx-3", target: "lx-7", relation: "业务关联" },
    { source: "lx-3", target: "lx-8", relation: "业务关联" },
    { source: "lx-5", target: "vp-1", relation: "产品关联" },
    { source: "lx-7", target: "td-3", relation: "市场关联" },

    // 充电桩业务关联
    { source: "lx-3", target: "cd-2", relation: "业务关联" },
    { source: "cd-2", target: "cd-1", relation: "产品关系" },
    { source: "cd-1", target: "cd-3", relation: "商务关系" },

    // 虚拟电厂关联
    { source: "lx-3", target: "vp-1", relation: "业务关联" },
    { source: "lx-3", target: "vp-2", relation: "业务关联" },
    { source: "vp-1", target: "vp-2", relation: "方案关系" },
    { source: "vp-1", target: "vp-3", relation: "业务关联" },
    { source: "vp-2", target: "cd-1", relation: "场景关联" },
    { source: "lx-5", target: "vp-2", relation: "产品关联" },

    // 可信数据空间关联
    { source: "td-1", target: "td-2", relation: "包含关系" },
    { source: "td-3", target: "td-4", relation: "市场机会" },
    { source: "td-3", target: "td-5", relation: "市场机会" },
    { source: "td-6", target: "td-3", relation: "数据支撑" },
    { source: "td-6", target: "td-7", relation: "平台关联" },
    { source: "td-3", target: "td-8", relation: "政策关联" },

    // 数据基础设施标准关联
    { source: "ndi-1", target: "ndi-2", relation: "标准关联" },
    { source: "ndi-1", target: "ndi-3", relation: "标准关联" },
    { source: "ndi-1", target: "ndi-5", relation: "流程关联" },
    { source: "ndi-4", target: "td-3", relation: "政策驱动" },
    { source: "ndi-4", target: "td-8", relation: "政策驱动" },

    // 跨类关联
    { source: "td-2", target: "ndi-1", relation: "技术支撑" },
    { source: "cd-2", target: "lx-2", relation: "AI能力支撑" },
    { source: "vp-3", target: "lx-7", relation: "交易关联" },
    { source: "lx-6", target: "vp-2", relation: "充电场景聚合" }
  ]
};

// 分类配置
const CATEGORY_CONFIG = {
  "朗新科技": { color: "#3B82F6", emoji: "🏢" },
  "可信数据空间": { color: "#10B981", emoji: "🔐" },
  "充电桩": { color: "#F97316", emoji: "⚡" },
  "虚拟电厂": { color: "#EF4444", emoji: "⚡" },
  "数据基础设施": { color: "#8B5CF6", emoji: "🏛️" }
};

// 获取所有分类
function getCategories() {
  return Object.keys(CATEGORY_CONFIG);
}

// 获取分类颜色
function getCategoryColor(category) {
  return CATEGORY_CONFIG[category]?.color || "#6B7280";
}

// 获取分类emoji
function getCategoryEmoji(category) {
  return CATEGORY_CONFIG[category]?.emoji || "📄";
}
