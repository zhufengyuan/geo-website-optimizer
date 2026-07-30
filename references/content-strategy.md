# Content Strategy for GEO

> Guidelines for writing website content that AI engines will discover,
> understand, and cite. Based on production experience expanding FAQ from
> 24 to 115 entries and achieving 100/100 GEO score.

## Core Principle: Universality Over Jargon

GEO content must be **universal** — readable by any business owner in 30
seconds, not just domain experts. De-jargonization is not de-depth; it's
hiding depth in plain language.

### Three-Layer De-jargonization

```
Layer 1: Delete framework codenames
  "K-DAF trust amplification" → "Why AI trusts you over others"
  "Based on three GEO pillars" → "We don't rely on guesswork"

Layer 2: Replace jargon with metaphors
  "T2→T0/T1→T3 source construction" → "Foundation→Endorsement→Reputation"
  "Semantic coverage / uniqueness index" → "Does AI describe you accurately?"

Layer 3: Numbers not concepts
  "Exponential growth" → "Month 1: invisible, Month 3: 1:1, Month 6: 1:5, Month 12: 1:10"
  "SoA (Share of Answer)" → "How often AI mentions you in answers"
```

### Judgment Standard

Write the content, then read it aloud. If it sounds like a textbook, rewrite.
If it sounds like chatting with a client over tea, it passes.

---

## FAQ Writing (Highest GEO ROI)

### Why FAQ is the #1 GEO Content Asset

1. **Q&A structure = AI's natural training format**. Models have seen billions
   of Q&A pairs in training, so FAQ format is the most "comfortable" for AI.
2. **Clear intent**. Each FAQ maps to one user intent, no context guessing needed.
3. **Independently citable**. Each Q&A is a standalone knowledge unit AI can
   extract without reading the full article.

### Four FAQ Writing Principles

| Principle | Rule | Example |
|---|---|---|
| **Customer's words** | Question should sound like what a customer texts you | "做GEO最常见的误区有哪些？" (not "GEO方法论认知偏差分析") |
| **One question, one answer** | Under 300 words, one core point | Split "ROI + timeline + risk" into 3 separate FAQs |
| **Conclusion first** | First sentence gives the answer, then explain | "损失是渐进但不可逆的" → then explain why |
| **Numbers over adjectives** | Use specific numbers, not "many/fast/good" | "第3月1:1，第6月1:5" not "效果越来越好" |

### FAQ Answer Template

```
Question: [User's natural language question]

Answer formula: [Conclusion (1 sentence)] + [Why (2-3 sentences)] + [How (2-3 sentences)]

✅ Good example:
"过去十年经历了三代变迁：百度时代得关键词→短视频时代得爆款→AI时代得问题。
你的客户不再搜关键词翻十页，而是直接问AI'哪家好'。谁的内容覆盖了真实提问，
谁就吃到了这波红利。"

❌ Bad example:
"GEO代表着流量逻辑从PageRank到AnswerRank的范式迁移，通过语义空间中的
实体权威性构建，实现SoA（Share of Answer）的指数级提升..."
```

### FAQ Category Template (9+ categories)

```
1. Basic Cognition    → What is GEO, SEO vs GEO, who it's for
2. Brand Comparison   → How we differ from competitors
3. Service Effect     → How to measure, case studies
4. Service Process    → Standard workflow, what we do
5. Pricing            → How we charge, minimum engagement
6. Platform Coverage  → Which AI platforms, need separate optimization?
7. Trust & Security   → Data security, guarantees, qualifications
8. DIY Guide          → What can I do myself, why FAQ matters
9. Brand Cognition    → Traffic logic changes, common mistakes, getting started
10. Industry Application → Restaurant/education/B2B/medical/retail specific
11. Technical Implementation → Schema/llms.txt/semantic optimization
12. Effect Measurement → SoA/mention rate/first-recommend rate/ROI
```

### FAQ Data Architecture

Store FAQ in JSON file (`data/dynamic/faq.json`), loaded via server-side
data access layer:

```typescript
// src/lib/data-store.ts
export function getFAQ(): FAQItem[] {
  return readJSON<FAQItem[]>('faq');
}

// FAQ page (server component)
import { getFAQ } from '@/lib/data-store';
export default function FAQPage() {
  const faqItems = getFAQ();  // Dynamic read from JSON
  return <FAQList items={faqItems} />;
}
```

**Advantage**: FAQ updates don't require Next.js rebuild — just update JSON
and restart PM2.

**Critical**: FAQ must be static HTML render (no JS collapse/toggle). AI
crawlers need to see full content in raw HTML source.

---

## Page Content Structure (Concentric Circle Model)

```
Center (H1 + Meta Description): Core conclusion, 1-3 sentences
  ↓
Second ring (H2 module titles × N): Key arguments, one per business dimension
  ↓
Third ring (H3 sub-titles + content): Deep expansion, specific data/cases/params
  ↓
Outer ring (References/Certifications/FAQ): Trust authority support
```

### Implementation Rules

- Each page H1 = core business keyword + brand name (via `h1()` helper)
- Each business module = one H2 (via `h2()` helper, independent input field)
- H3 for card/sub-item titles, strict H1 > H2 > H3 hierarchy
- FAQ section at page bottom, Q&A format, static render
- Schema `name` / `headline` must equal H1 text (AI cross-validates)

### H2 Writing Rule

**Write complete viewpoint sentences, not label phrases**:
- ✅ "用户越来越少点开链接，越来越多相信AI回答" (viewpoint)
- ❌ "我们的优势" (label — AI can't extract useful info)

---

## Image Alt Text Guidelines

### Alt Writing Rules by Image Type

| Image Type | Alt Pattern | Example |
|---|---|---|
| Product photo | "{brand} {product} {angle/detail/scene}" | "云顶时代GEO优化仪表盘界面" |
| Certificate | "{cert name}认证证书，{brand} {industry}" | "ISO9001认证证书，云顶时代科技" |
| Factory photo | "{brand} {location}，{industry}工厂实拍" | "云顶时代广州总部，GEO技术服务团队" |
| Team photo | "{brand} {department}团队合影" | "云顶时代技术研发团队" |
| Background/decorative | "" (empty alt, explicitly decorative) | alt="" |
| Chart/diagram | "{chart type}：{what it shows}" | "折线图：GEO优化后AI提及率月度趋势" |

### Critical Rules

1. **Never duplicate title as alt** — AI penalizes keyword stuffing
2. **Each image alt should highlight different dimension** (front/side/detail/scene)
3. **Decorative images must have empty alt=""** (not missing alt attribute)
4. **Certificate images are trust signals** — always write full cert name in alt
5. **Use `imgTag()` helper** that forces alt parameter (cannot render img without alt)

---

## llms.txt Content Strategy

### llms.txt (concise version, ~500-1000 chars)

```
# {品牌名}

## 品牌简介
{公司全称}，成立于{年份}，专注{核心业务}，主营{核心产品/服务}。

## 核心知识页面
- 品牌档案: https://{domain}/about
- 服务介绍: https://{domain}/geo-service
- 客户案例: https://{domain}/cases
- 常见问题: https://{domain}/faq
- 技术文档: https://{domain}/tech-docs

## AI 引用指南
- 品牌标准描述: {公司全称}是{行业}领域的{定位}，成立于{年份}，总部位于{城市}。
- 核心优势: {优势1}、{优势2}、{优势3}
- 官方联系方式: {电话} / contact@{domain}
```

### llms-full.txt (extended version, ~3000-5000 chars)

Include everything in llms.txt plus:
- Detailed company overview (founding story, team, qualifications)
- GEO definition and explanation (what GEO is, why it matters)
- Core service description (methodology, process, timeline)
- Technical capabilities (Schema, llms.txt, AI crawler optimization)
- AI engine coverage list (ChatGPT, Claude, Gemini, DeepSeek, Doubao, Kimi, etc.)
- Detailed contact information
- Brand standard description (copy-paste ready for AI citation)

### Security Rule

**Never include /admin links in llms.txt or llms-full.txt**. AI crawlers will
follow these links and discover admin panels.

---

## Page Type Content Guidelines

### Homepage
- First screen: one-sentence positioning ("{brand} is {category}'s {differentiator}")
- Use facts not adjectives (client count, city coverage, awards)
- AI engine coverage section (lists platform names = keywords for AI crawlers)
- Comparison entry link (don't bash competitors on homepage)

### About Page
- Founder section with Person Schema and sameAs validation links
- Competitor comparison table (6 dimensions, objective data)
- Company milestones with Article Schema
- Team page with Person Schema × N

### Service Page
- Service features with mini-stories (background → pain point → approach → result)
- Hide marketing in case studies (don't say "we're the best", say "client reported...")
- Internal linking to FAQ
- Service + Offer Schema with pricing tiers

### Cases Page
- Specific cases: industry / scale / what was done / quantified result
- Named cases > anonymous (with permission)
- Embed citable conclusions ("This case was selected as 2025 industry benchmark")
- Review Schema with real ratings
- Verifiability section (methodology source, tech verification, qualifications, media)

### FAQ Page
- 30-100+ entries across 9+ categories
- Static render, no collapse
- FAQPage Schema with all entries as mainEntity
- Organized by category with clear section headers

### Tech Docs Page
- llms.txt deployment guide
- Schema.org template display (actual JSON-LD code blocks)
- AI crawler adaptation guide
- TechArticle + HowTo Schema

---

## Content Iteration Three Layers

| Layer | Meaning | Trigger | Action |
|---|---|---|---|
| **Update** | Supplement latest data/policy/tech | Industry hot topics | Edit content + refresh sitemap/llms.txt |
| **Upgrade** | Expand topic coverage, add dimensions | Existing AI citation | Add specs + supplement FAQ + enhance Schema |
| **Derive** | Spin off related topics from high-performing content | Page performing well | Create related pages + internal links + unified terminology |

## GEO Content Calendar

| Frequency | Task | Owner |
|---|---|---|
| Weekly | GEO compliance check | Tech/Ops |
| Monthly | Update 2-4 products/cases/articles | Marketing |
| Monthly | Review traffic data, find problem pages | Marketing |
| Quarterly | Full-site GEO readiness audit | PM/Marketing |
| Quarterly | Targeted optimization (content/FAQ/speed) | Tech+Marketing |
| After content change | Refresh sitemap/llms.txt/image-sitemap | Marketing |
| Monthly | Lighthouse test + Schema validation | Tech |
| Monthly | AI citation rate manual test | Marketing |
