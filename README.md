# GEO Website Optimizer

面向 AI 搜索引擎的企业官网 GEO 优化工具包。让 ChatGPT、Claude、Gemini、豆包、Kimi、文心一言、DeepSeek 等 11 个 AI 引擎在回答"XX 哪家好"时引用你的品牌。

> **生产验证**：xcloud-top.com（云顶时代科技 GEO 官网）— 24 页、14 种 Schema、115+ FAQ、双服务器架构，GEO 审计满分 100/100。
> 全套方法论来自 500+ 页实战文��。

[![GEO Score](https://img.shields.io/badge/GEO_Score-100%2F100-brightgreen)](https://github.com/zhufengyuan/geo-website-optimizer)

---

## GEO ≠ SEO

| | SEO | GEO |
|---|---|---|
| **目标** | 搜索引擎排名 | AI 引擎引用 |
| **受众** | 用户点击 | AI 抓取 + 训练语料 |
| **核心手段** | 关键词、外链 | 结构化数据、FAQ、内容资产 |
| **衡量标准** | 排名第几 | 被 AI 引用了吗 |

**核心原则**：不是让用户在 Google 搜到你，而是让 AI 在回答问题时提到你。

---

## 六大阶段 + 架构参考

```
Phase 0: 行业理解 → Phase 1: GEO 审计 → Phase 2: 内容优化
    → Phase 3: Schema 部署 → Phase 4: AI 爬虫配置
        → Phase 5: 服务器部署 → Phase 6: 验证
              ↕
         生产架构参考（24 页官网实战蓝图）
```

### Phase 0 — 理解客户行业

在应用任何 GEO 技术之前，先理解客户业务。不限行业 — 制造、SaaS、医疗、金融、教育、地产、零售均可。结构优化技术通用，只需调整客户领域的内容。

### Phase 1-6 — 从审计到验证的全流程

详见 [SKILL.md](./SKILL.md)，涵盖：
- **5 维度 50+ 项审计**（技术可达/结构化数据/内容资产/信任背书/域名一致性）
- **FAQ 为第一战场**（去术语化三层、结论先行、数字优于形容词）
- **14 种 Schema 精确映射**（按页面类型选择最精准类型）
- **11 个 AI 爬虫配置**（GPTBot / ClaudeBot / PerplexityBot / KimiBot 等）
- **双服务器部署**（paramiko SFTP + PM2 cluster + 参数化配置）
- **9 项验证指标**（双站 MD5 一致性校验）

### ✨ 生产架构参考 — 新增

基于 xcloud-top.com 的真实架构，文档中新增了完整参考章节：

| 模块 | 内容 |
|---|---|
| **24 页站点结构** | 首页→服务→诊断→FAQ(115+)→案例→技术文档→术语表→定价→博客→关于→联系→洞察(5篇)→行业(3个) |
| **数据流架构** | JSON 文件存储 + data-store.ts 数据访问层 + Content REST API，前后端数据实时联动，无需数据库 |
| **设计体系** | Design Token（CSS 变量）+ 编辑式叙事结构（Hero→故事→论述→断点→服务→CTA→FAQ）+ Pill Button 4 变体 |
| **双服务器架构** | 主备两台独立服务器，参数化部署脚本，差异化 Node 路径/端口/PM2 配置 |
| **工程模式速查** | PM2 errored 恢复、.next 缓存陷阱、ESLint 构建阻断、f-string/JSX 花括号冲突、paramiko 编码等 13 个实战坑点 |

---

## 文件结构

```
├── SKILL.md                          # 完整技能文档（含生产架构参考）
├── assets/                           # 即用模板
│   ├── llms-template.txt
│   ├── page-template.tsx            # Next.js App Router 页面（含完整 Schema）
│   ├── robots-template.ts
│   └── sitemap-template.ts
├── references/                       # 参考文档
│   ├── content-strategy.md          # 内容策略（FAQ/去术语化/同心圆结构）
│   ├── deployment-guide.md          # 双服务器部署完整指南
│   ├── geo-optimization-checklist.md # 5 维度 50+ 项检查清单
│   └── schema-templates.md          # 14 种 Schema.org 类型模板
└── scripts/                          # 可执行脚本
    ├── geo_audit.py                 # GEO 合规审计
    └── deploy_geo_site.py           # 双服务器部署
```

**补充参考文档**（在 [zhufengyuan/geo_file](https://github.com/zhufengyuan/geo_file)）：
- 官网GEO内容优化开发笔记.md — 内容层实战经验（FAQ 扩写、Schema 全覆盖、内容矩阵批量部署、PM2 恢复）
- 官网建设项目实施指南.md — 工程层全景（8 模块开发、数据流架构、设计体系、双服务器、避坑实录）

---

## 快速开始

### 审计现有网站
```bash
python scripts/geo_audit.py --url https://你的域名.com
```

### 从零建站

1. 确定技术栈：Next.js SSR（推荐）或 EJS/PHP/JSP 服务端渲染
2. 按 `SKILL.md` Phase 0-6 逐步推进
3. 用 `assets/page-template.tsx` 快速生成符合 GEO 规范的页面
4. 参考 `SKILL.md` 中「生产架构参考」章节的 24 页站点结构、数据流架构和设计体系

### 验证部署
```bash
# 双服务器部署
python scripts/deploy_geo_site.py --host {IP} --port {SSH} --project /srv/{name}

# 验证 9 项指标
curl http://localhost:{port}/ | grep -c "BreadcrumbList"  # >= 1
curl http://localhost:{port}/faq | grep -c "question"       # >= 30
curl http://localhost:{port}/robots.txt | grep -c "User-agent"  # >= 11
```

---

## 适用场景

- 企业官网想被 ChatGPT / 豆包 / Kimi / DeepSeek 等 AI 引用
- 不知道网站被 AI 收录了多少、缺什么
- 需要 Schema.org 但不知道从哪开始
- 从零搭建 GEO 满分的官网
- 双服务器架构需要同步部署和验证
- 需要一个经过生产验证的官网架构蓝图

## License

MIT
