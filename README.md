# GEO Website Optimizer

面向 AI 搜索引擎（ChatGPT、Claude、Gemini、Perplexity、豆包、Kimi、文心一言等）的企业官网 GEO 优化工具包。不是做 SEO 排名，而是让 AI 在回答"XX 哪家好"时引用你的品牌。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GEO Score](https://img.shields.io/badge/GEO_Score-100%2F100-brightgreen)](https://github.com/zhufengyuan/geo-website-optimizer)

## 一句话说清楚

**GEO ≠ SEO** — SEO 优化搜索引擎排名，GEO 优化 AI 引擎引用。这整套工具帮你把企业官网从"AI 看不见"变成"AI 主动引用"，从审计到部署全覆盖。

## 核心能力

| 模块 | 做什么 | 输出 |
|---|---|---|
| **GEO 审计** | 5 维度 50+ 检查项，打分量化 | 审计报告 + 修复清单 |
| **结构化数据** | Schema.org 完整部署（Organization、FAQPage、Article 等） | 可复制即用的 Schema 模板 |
| **AI 爬虫配置** | llms.txt / robots.txt / sitemap.xml 四件套 | 即插即用的配置文件 |
| **内容优化** | FAQ 扩展、alt 文本、对比表格 | 内容改造��案 |
| **部署脚本** | SFTP 双服务器同步部署 | 一键部署命令 |

## 快���开始

### GEO 审计（现有站点）

```bash
python scripts/geo_audit.py --url https://你的域名.com
```

审计结果包含 5 个维度：
- **技术可达性**（15 分）— GEO 四文件、SSR、HTTP 状态、Alt 覆盖率
- **结构化数据**（25 分）— Schema 类型覆盖、发布日期、精度
- **内容资产**（20 分）— 页面数、FAQ 深度、文章数、唯一 H1
- **信任背书**（20 分）— Person Schema、sameAs、对比表格
- **域名一致性**（20 分）— canonical、sitemap、邮箱、内容对等

### 从零建站

参考 `references/content-strategy.md` 中的完整建站流程，包含页面模板和 FAQ 策略。

### 部署

```bash
python scripts/deploy_geo_site.py
```

## 文件结构

```
├── SKILL.md                          # 技能入口（WorkBuddy 格式）
├── assets/                           # 即用模板文件
│   ├── llms-template.txt            # AI Crawler 引导文件模板
│   ├── page-template.tsx            # Next.js SSR 页面模板
│   ├── robots-template.ts           # robots.txt 动态生成
│   └── sitemap-template.ts          # sitemap.xml 动态生成
├── references/                       # 参考文档
│   ├── content-strategy.md          # 内容策略（FAQ/文章/对比表）
│   ├── deployment-guide.md          # 双服务器部署指南
│   ├── geo-optimization-checklist.md # 50+ 项检查清单
│   └── schema-templates.md          # Schema.org 完整模板库
└── scripts/                          # 可执行脚本
    ├── geo_audit.py                 # GEO 合规审计工具
    └── deploy_geo_site.py           # 部署脚本
```

## 适用场景

- 企业官网想被 ChatGPT/豆包/Kimi 等 AI 搜索引擎引用
- 现有网站不知道被 AI 收录了多少、还缺什么
- 需要部署 Schema.org 结构化数据但不知道从哪开始
- 想从零搭建一个 GEO 满分的企业官网

## 生产验证

本工具包基于真实项目验证 —— 某 Next.js SSR 双服务器企业官网，审计得分 **100/100**，AI 引擎引用覆盖率达标。全套方法论来自 500+ 页实战文档。

## License

MIT
