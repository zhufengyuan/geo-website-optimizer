# GEO Website Optimizer

面向 AI 搜索引擎（ChatGPT、Claude、Gemini、Perplexity、豆包、Kimi、文心一言、元宝、千问、智谱、纳米等）的企业官网 GEO 优化工具包。不是做 SEO 排名，而是让 AI 在回答"XX 哪家好"时引用你的品牌。

[![GEO Score](https://img.shields.io/badge/GEO_Score-100%2F100-brightgreen)](https://github.com/zhufengyuan/geo-website-optimizer)

## GEO ≠ SEO

| | SEO | GEO |
|---|---|---|
| **目标** | 搜索引擎排名 | AI 引擎引用 |
| **受众** | 用户点击 | AI 抓取 + 训练语料 |
| **核心手段** | 关键词、外链 | 结构化数据、FAQ、内容资产 |
| **衡量标准** | 排名第几 | 被 AI 引用了吗 |

**核心原则**：不是让用户在 Google 搜到你，而是让 AI 在回答问题时提到你。

## 六大阶段全覆盖

```
Phase 0: 行业理解 → Phase 1: GEO 审计 → Phase 2: 内容优化
    → Phase 3: Schema 部署 → Phase 4: AI 爬虫配置
        → Phase 5: 服务器部署 → Phase 6: 验证
```

### Phase 0 — 理解客户行业

在应用任何 GEO 技术之前，先理解客户业务：
- 什么行业？（制造、SaaS、医疗、金融、教育……）
- AI 需要知道什么才能引用这个品牌？
- 目标客户问什么问题？（用真实客户语言写 FAQ）
- 有哪些外部验证？（政府注册、媒体报道、行业奖项、平台档案）

### Phase 1 — GEO 审计

```bash
python scripts/geo_audit.py --url https://你的域名.com
```

5 维度 50+ 项评分：
- **技术可达性**（15 分）— GEO 四文件、SSR、HTTP 200、Alt 覆盖率
- **结构化数据**（25 分）— Schema 类型覆盖、日期、精度
- **内容资产**（20 分）— 页面数、FAQ 深度、文章数、H1 唯一性
- **信任背书**（20 分）— Person Schema、sameAs 链接、对比表格
- **域名一致性**（20 分）— canonical、sitemap、内容对等

### Phase 2 — 内容优化

- **FAQ 写作**（GEO 回报最高）：用客户自然语言提问，结论先行，数字优于形容词，目标 30-100+ 条
- **页面结构**（同心圆模型）：H1 = 核心业务关键词，严格 H1 → H2 → H3 层级
- **图片 Alt 文本**：产品图 `{品牌} {产品} {角度}` | 证书 `{证书名} 认证` | 装饰图 `alt=""`
- **去术语化**（三层）：删除内部代号 → 用日常比喻替换行话 → 给数字不给概念

### Phase 3 — Schema.org 结构化数据

页面到 Schema 的精确映射：
- 首页 → Organization + Service + FAQPage + BreadcrumbList + WebSite
- 文章 → Article + BreadcrumbList（必须含 datePublished/dateModified）
- 技术文档 → TechArticle + HowTo
- 关于 → AboutPage + Organization + Person + BreadcrumbList
- FAQ 页 → FAQPage + BreadcrumbList

**关键规则**：Schema `name` = 页面 H1（AI 交叉验证） | BreadcrumbList 每页必须有 | sameAs 4-10 个外部链接

### Phase 4 — AI 爬虫配置

四件套一键配置：
- **robots.txt** — 11 个 AI 爬虫白名单 + sitemap 引用
- **llms.txt** — AI 专属站点导航（品牌摘要 + 核心链接 + 引用指南）
- **llms-full.txt** — 扩展知识库（公司概览、产品、认证、案例）
- **sitemap.xml** — 完整页面索引 + 图片条目

### Phase 5 — 服务器部署

```bash
python scripts/deploy_geo_site.py \
  --host {服务器IP} --port {SSH端口} --user {用户名} \
  --password '{密码}' --project /srv/{项目名} \
  --node-bin {Node路径} --app-port {应用端口} --pm2-name {进程名}
```

**标准构建顺序**（不可跳过）：
1. 清除 `.next` 缓存
2. `next build`
3. PM2 delete（不是 restart — errored 状态 sticky）
4. PM2 start
5. 等待预热
6. curl 验证

### Phase 6 — 验证

每台服务器至少验证 9 项：
- 首页 200 | 所有路由 200 | llms.txt > 500B | llms-full.txt > 2000B
- robots.txt >= 11 个 User-agent | sitemap >= 12 个 URL
- FAQ >= 30 条 | BreadcrumbList 每页 >= 1 个 | Alt 文本覆盖

双服务器 MD5 校验确保文件一致性。

## 文件结构

```
├── SKILL.md                          # WorkBuddy 技能入口
├── assets/                           # 即用模板
│   ├── llms-template.txt            # llms.txt 模板
│   ├── page-template.tsx            # Next.js App Router 页面模板（含完整 Schema）
│   ├── robots-template.ts           # robots.ts 动态生成
│   └── sitemap-template.ts          # sitemap.ts 动态生成
├── references/                       # 参考文档
│   ├── content-strategy.md          # 内容策略（FAQ/文章/去术语化/Alt 文本）
│   ├── deployment-guide.md          # 双服务器部署完整指南
│   ├── geo-optimization-checklist.md # 5 维度 50+ 项检查清单
│   └── schema-templates.md          # 全部 Schema.org 类型模板
└── scripts/                          # 可执行脚本
    ├── geo_audit.py                 # GEO 合规审计
    └── deploy_geo_site.py           # 双服务器部署
```

## 适用场景

- 企业官网想被 ChatGPT / 豆包 / Kimi 等 AI 引用
- 不知道网站被 AI 收录了多少、缺什么
- 需要 Schema.org 但不知道从哪开始
- 从零搭建 GEO 满分的官网
- 双服务器架构需要同步部署和验证

## 行业通用

不限行业 — 制造、SaaS、医疗、金融、教育、地产、零售均可。结构优化技术通用，只需调整客户领域的内容。

## 生产验证

某 Next.js SSR 双服务器企业官网，本工具审计得分 **100/100**。全套方法论来自 500+ 页实战文档和真实部署经验。

## License

MIT
