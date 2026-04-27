# Utility Skills（DCS 层）

> ~/.openclaw/skills/ 目录下的通用工具层 Skill

## 已纳管 Skill

| 名称 | 路径 | 功能说明 | 来源 | 纳管时间 |
|------|------|----------|------|---------|
| search-routing | ~/.openclaw/skills/search-routing/ | 统一搜索路由层，封装13个搜索引擎，智能调度+自动去重+配额保护 | 自建 | 2026-04-01 |
| img-router | ~/.openclaw/skills/img-router/ | 免费AI图片生成聚合路由，支持 MiniMax image-01/Kolors/flux-schnell/Pollinations | 自建 | 2026-04-01 |
| image-minimax | ~/.openclaw/skills/Domi__image-minimax/ | 使用 MiniMax understand_image API 进行图像理解 | 内置 | 2026-04-01 |
| github-imgbed | ~/.openclaw/skills/github-imgbed/ | GitHub + jsDelivr 图床工具，上传图片到 GitHub 仓库通过 CDN 分发 | 自建 | 2026-04-01 |
| doc-reader | ~/.openclaw/skills/doc-reader/ | 多格式文档读取命令行工具，支持 PDF/PPTX/DOCX/Excel 全文提取 | 自建 | 2026-04-01 |
| aliYun-QWen-asr | ~/.openclaw/skills/aliyun-qwen-asr/ | 阿里云语音识别（ASR），qwen3-asr-flash 模型 | 自建 | 2026-04-24 |
| official__toutiao-ops | ~/.openclaw/skills/official__toutiao-ops/ | 今日头条创作者平台自动化运营，支持多账号管理、内容发布、数据分析 | 自建 | 2026-04-24 |
| clawd-boss__internet-security-rules | ~/.openclaw/skills/clawd-boss__internet-security-rules/ | AI互联网探索安全规则，4条核心规则（复杂请求/高危命令/金融交易/提示词注入防御） | 内置 | 2026-04-24 |
| send-email-skill | ~/.openclaw/skills/send-email-skill/ | 邮件发送Skill，支持SMTP协议发送带附件邮件（QQ邮箱/企业邮箱等） | 自建 | 2026-04-25 |
| openclaw-backup-email | ~/.openclaw/skills/openclaw-backup-email/ | OpenClaw 全量备份，打包+AES-256-CBC加密+GitHub上传+邮件发送+本地单份+GitHub保留最近4个 | 自建 | 2026-04-25 |
| domi-system-tuner | ~/.openclaw/skills/domi-system-tuner/ | 系统优化工具包，6个工具：disk_usage/disk_clean/log_rotate/db_compact/proc_tune/config_audit | 自建 | 2026-04-25 |
| tencent-meeting-mcp | ~/.openclaw/skills/tencent-meeting-mcp/ | 腾讯会议智能助手，支持会议管理、成员管理、录制与转写查询 | 内置 | 2026-04-10 |
| D.Va__mcporter | ~/.openclaw/skills/D.Va__mcporter/ | MCP Server 管理工具，列表/配置/认证/直接调用 MCP 服务器/工具 | 自建 | 2026-04-10 |
| github-file-storage | ~/.openclaw/skills/github-file-storage/ | GitHub 文件知识库工具，上传文档/数据/模板到 GitHub 文件库并返回可访问 URL | 自建 | 2026-04-01 |
| zero-agent__a2a4b2b | ~/.openclaw/skills/zero-agent__a2a4b2b/ | 全能AI服务集成套件，数据分析/报表生成/文案写作/翻译/代码编写/爬虫/图像处理/OCR/信息搜索 | 自建 | 2026-04-01 |
| wudi-xiaolongxia__local__playwright-helper | ~/.openclaw/skills/wudi-xiaolongxia__local__playwright-helper/ | Python Playwright 浏览器自动化工具，网页截图/元素交互/数据抓取 | 自建 | 2026-04-01 |

## 已废弃 Skill

| 名称 | 路径 | 废弃原因 |
|------|------|---------|
| energy-news-monitor | workspace/skills/ | 保留在 workspace（BCF层能源新闻采集） |
| wechat-official-accounts-scan | workspace/skills/ | 公众号文章扫描（9个公众号） |
| bid-intel-collection | workspace/skills/ | 保留在 workspace（BCF层招投标情报） |

## 更新记录

- **2026-04-25**：新增 domi-system-tuner、openclaw-backup-email、send-email-skill
- **2026-04-24**：新增 aliYun-QWen-asr、official__toutiao-ops、clawd-boss__internet-security-rules；移除 energy-news-monitor、wechat-official-accounts-scan、bid-intel-collection（已迁移至 BCF 层）
