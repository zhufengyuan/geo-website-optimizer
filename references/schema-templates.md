# Schema.org JSON-LD Templates

> Complete templates for all Schema.org structured data types used in GEO
> optimization. Copy, customize values, and inject via `<script type="application/ld+json">`.

## Page-to-Schema Mapping

| Page Type | Schema Types | Priority |
|---|---|---|
| Homepage | Organization + Service + FAQPage + BreadcrumbList + WebSite | Most complete |
| Service page | Service + Offer + BreadcrumbList | High |
| Article list | CollectionPage + ItemList + BreadcrumbList | Medium |
| Article detail | Article + BreadcrumbList | High (needs dates) |
| Tech docs | TechArticle + HowTo + BreadcrumbList | Medium |
| About page | AboutPage + Organization + Person + BreadcrumbList | High |
| Contact page | ContactPage + Organization + BreadcrumbList | Medium |
| FAQ page | FAQPage + BreadcrumbList | High |
| Cases | Article + Review + CollectionPage + BreadcrumbList | Medium |
| Glossary | DefinedTermSet + BreadcrumbList | Low |
| Industry pages | Article + FAQPage + BreadcrumbList | Medium |
| Pricing | Service + Offer (x3) + BreadcrumbList | Medium |

---

## Organization Schema (Homepage — Most Complete)

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://{domain}/#organization",
  "name": "{公司全称}",
  "alternateName": "{品牌简称}",
  "legalName": "{法定全称}",
  "url": "https://{domain}",
  "logo": "https://{domain}/logo.svg",
  "description": "{一句话品牌描述，含核心品类关键词}",
  "foundingDate": "2024",
  "founder": {
    "@type": "Person",
    "name": "{创始人姓名}"
  },
  "foundingLocation": {
    "@type": "Place",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "{城市}",
      "addressCountry": "CN"
    }
  },
  "address": {
    "@type": "PostalAddress",
    "addressCountry": "CN",
    "addressLocality": "{城市}",
    "streetAddress": "{详细地址}"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+86-{电话}",
    "email": "contact@{domain}",
    "contactType": "customer service"
  },
  "email": "contact@{domain}",
  "areaServed": "中国及海外",
  "knowsAbout": ["{核心领域1}", "{核心领域2}", "{核心领域3}"],
  "numberOfEmployees": "{员工规模}",
  "sameAs": [
    "https://www.tianyancha.com/company/{id}",
    "https://www.qcc.com/firm/{id}",
    "https://www.qixin.com/company/{id}",
    "https://aiqicha.baidu.com/company/{id}",
    "https://www.zhihu.com/org/{slug}",
    "https://www.36kr.com/company/{id}",
    "https://xueqiu.com/S/{id}",
    "https://www.sohu.com/a/{article_id}",
    "https://www.woshipm.com/{path}",
    "https://www.digitalchina.gov.cn/{path}"
  ]
}
```

### sameAs Source Tiers

| Tier | Source Type | Examples | AI Validation Value |
|---|---|---|---|
| T0 | Government | digitalchina.gov.cn, gov.cn | Highest authority |
| T1 | Media/Knowledge | 36kr.com, zhihu.com, sohu.com | Perplexity/ChatGPT high weight |
| T2 | Business info | Tianyancha, Qichacha, Qixin, Baidu Aiqicha | Baidu AI (Wenxin) high weight |

---

## FAQPage Schema

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "用客户的口吻写的完整问题？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "第一句给结论。后面展开300字以内。避免框架术语。用比喻。给数字不给形容词。"
      }
    },
    {
      "@type": "Question",
      "name": "另一个高频问题？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "结论在前，展开在后。"
      }
    }
  ]
}
```

**FAQ writing rules**:
- Question = customer's natural language (not academic terms)
- Answer = conclusion first, then explanation, under 300 words
- Use numbers not adjectives ("3 months 1:1, 6 months 1:5")
- Target 30-100+ entries across 9+ categories
- Must be static HTML (no JS collapse)

---

## Article Schema (with dates — MANDATORY)

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "文章标题（与页面H1一致）",
  "description": "文章摘要，1-2句话",
  "datePublished": "2026-07-20",
  "dateModified": "2026-07-29",
  "author": {
    "@type": "Organization",
    "name": "{公司全称}"
  },
  "publisher": {
    "@type": "Organization",
    "name": "{公司全称}",
    "logo": {
      "@type": "ImageObject",
      "url": "https://{domain}/logo.svg"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://{domain}/insights/article-slug"
  },
  "about": ["关键词1", "关键词2"],
  "mentions": ["industry", "scale", "clientLabel"]
}
```

**Critical**: `datePublished` and `dateModified` are MANDATORY. AI engines
(especially Perplexity, Google AI Overview) use dates to judge content
freshness. Articles without dates may be deprioritized.

---

## BreadcrumbList Schema (EVERY page)

### Homepage (1 level)
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "首页", "item": "https://{domain}/"}
  ]
}
```

### First-level page (2 levels)
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "首页", "item": "https://{domain}/"},
    {"@type": "ListItem", "position": 2, "name": "常见问题", "item": "https://{domain}/faq"}
  ]
}
```

### Second-level page (3 levels)
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "首页", "item": "https://{domain}/"},
    {"@type": "ListItem", "position": 2, "name": "专题洞察", "item": "https://{domain}/insights"},
    {"@type": "ListItem", "position": 3, "name": "GEO vs SEO", "item": "https://{domain}/insights/geo-vs-seo"}
  ]
}
```

---

## Person Schema (Founder)

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "{创始人姓名}",
  "jobTitle": "法定代表人 / 执行董事兼总经理",
  "worksFor": {
    "@type": "Organization",
    "name": "{公司全称}"
  },
  "sameAs": [
    "https://www.tianyancha.com/company/{id}",
    "https://www.qcc.com/firm/{id}",
    "https://www.qixin.com/company/{id}",
    "https://www.sohu.com/a/{article_id}"
  ]
}
```

**Rules**: Only include publicly verifiable facts (business registration, media
reports). Do NOT fabricate education, awards, or titles without sources.

---

## Service + Offer Schema

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "GEO 生成式引擎优化服务",
  "serviceType": "AI搜索引擎优化",
  "provider": {
    "@type": "Organization",
    "name": "{公司全称}"
  },
  "areaServed": "中国及海外",
  "offers": [
    {
      "@type": "Offer",
      "name": "基础版",
      "price": "9800",
      "priceCurrency": "CNY",
      "description": "适合刚起步的企业"
    },
    {
      "@type": "Offer",
      "name": "专业版",
      "price": "29800",
      "priceCurrency": "CNY",
      "description": "适合成长期企业"
    },
    {
      "@type": "Offer",
      "name": "企业版",
      "price": "59800",
      "priceCurrency": "CNY",
      "description": "适合成熟期企业"
    }
  ]
}
```

---

## CollectionPage + ItemList Schema (List pages)

```json
{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "专题洞察",
  "url": "https://{domain}/insights",
  "hasPart": {
    "@type": "ItemList",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "url": "https://{domain}/insights/geo-vs-seo",
        "name": "GEO vs SEO 深度对比"
      },
      {
        "@type": "ListItem",
        "position": 2,
        "url": "https://{domain}/insights/ai-brand-recommendation",
        "name": "AI 品牌推荐机制"
      }
    ]
  }
}
```

---

## TechArticle + HowTo Schema (Tech docs page)

```json
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "技术文件专栏：llms.txt 部署与 Schema 模板",
  "datePublished": "2026-07-26",
  "dateModified": "2026-07-29",
  "author": {"@type": "Organization", "name": "{公司全称}"},
  "publisher": {
    "@type": "Organization",
    "name": "{公司全称}",
    "logo": {"@type": "ImageObject", "url": "https://{domain}/logo.svg"}
  }
}
```

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "如何部署 llms.txt",
  "step": [
    {"@type": "HowToStep", "position": 1, "name": "创建 llms.txt", "text": "在网站根目录创建 llms.txt 文件..."},
    {"@type": "HowToStep", "position": 2, "name": "配置路由", "text": "在 Next.js 中创建 /llms.txt/route.ts..."},
    {"@type": "HowToStep", "position": 3, "name": "验证", "text": "curl -s https://{domain}/llms.txt"}
  ]
}
```

---

## Review Schema (Cases page)

```json
{
  "@context": "https://schema.org",
  "@type": "Review",
  "itemReviewed": {
    "@type": "Organization",
    "name": "{公司全称}"
  },
  "author": {
    "@type": "Person",
    "name": "某B2B技术服务客户"
  },
  "datePublished": "2026-06-15",
  "reviewBody": "合作3个月后，AI搜索中品牌提及率从0提升到38%...",
  "reviewRating": {
    "@type": "Rating",
    "ratingValue": "5",
    "bestRating": "5"
  }
}
```

**Red line**: Reviews must be based on real customer feedback. AI cross-validates.
Fake reviews are worse than no reviews — if detected as fake, brand trust score
drops significantly.

---

## WebSite + SearchAction Schema (Homepage)

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "url": "https://{domain}",
  "name": "{品牌名}",
  "publisher": {
    "@type": "Organization",
    "name": "{公司全称}"
  },
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://{domain}/search?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
```

---

## DefinedTermSet Schema (Glossary)

```json
{
  "@context": "https://schema.org",
  "@type": "DefinedTermSet",
  "name": "GEO 术语表",
  "hasDefinedTerm": [
    {
      "@type": "DefinedTerm",
      "name": "GEO",
      "description": "生成式引擎优化，让AI搜索引擎在回答用户问题时引用你的品牌"
    },
    {
      "@type": "DefinedTerm",
      "name": "SoA",
      "description": "Share of Answer，AI回答中提到你的比例"
    }
  ]
}
```

---

## Next.js JsonLd Component Pattern

```tsx
// src/components/json-ld.tsx
export function JsonLd({ data }: { data: Record<string, unknown> }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}

// Usage in page.tsx
import { JsonLd } from "@/components/json-ld";

export default function Page() {
  const organizationSchema = { /* ... */ };
  const breadcrumbSchema = { /* ... */ };
  
  return (
    <>
      <JsonLd data={organizationSchema} />
      <JsonLd data={breadcrumbSchema} />
      {/* page content */}
    </>
  );
}
```

**Multiple Schema on one page**: Use multiple `<JsonLd data={...} />` tags.
Next.js will render each as a separate `<script type="application/ld+json">`.
