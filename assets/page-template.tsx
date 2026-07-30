// Next.js 13+ App Router Page Template with GEO Optimization
// Copy this file, customize the content, and place in src/app/{route}/page.tsx
//
// This template includes:
// - Complete Schema.org JSON-LD (Organization + BreadcrumbList + page-specific)
// - Proper H1/H2 hierarchy (concentric circle model)
// - Server-side rendering (SSR) for AI crawler accessibility
// - Image alt text examples
// - FAQ section with static render

import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { JsonLd } from "@/components/json-ld";
import { createPageMetadata } from "@/lib/metadata";
import { contactInfo, siteUrl } from "@/data/site-data";

// === Page Metadata (SEO + GEO) ===
export const metadata = createPageMetadata({
  title: "页面标题 — 品牌名",  // MUST contain core keyword + brand
  description: "页面描述，1-2句话，含核心关键词",
  path: "/page-slug",
});

// === Schema.org Structured Data ===
const breadcrumbSchema = {
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  itemListElement: [
    { "@type": "ListItem", position: 1, name: "首页", item: siteUrl },
    { "@type": "ListItem", position: 2, name: "页面名称", item: `${siteUrl}/page-slug` },
  ],
};

// Use the most precise Schema type for this page
// Options: WebPage, AboutPage, ContactPage, CollectionPage, Service, Article, TechArticle, FAQPage
const pageSchema = {
  "@context": "https://schema.org",
  "@type": "WebPage",
  name: "页面标题 — 品牌名",  // MUST match H1
  description: "页面描述",
  url: `${siteUrl}/page-slug`,
};

// If this page has FAQ content, add FAQPage Schema
const faqSchema = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: [
    {
      "@type": "Question",
      name: "用客户的口吻写的完整问题？",
      acceptedAnswer: {
        "@type": "Answer",
        text: "第一句给结论。后面展开300字以内。避免框架术语。用比喻。给数字不给形容词。",
      },
    },
  ],
};

export default function Page() {
  return (
    <>
      {/* Inject Schema.org JSON-LD */}
      <JsonLd data={pageSchema} />
      <JsonLd data={breadcrumbSchema} />
      <JsonLd data={faqSchema} />

      <SiteHeader />
      
      <main className="site-page">
        {/* Hero section — H1 with core keyword + brand */}
        <section className="section page-hero">
          <div className="shell">
            <p className="eyebrow">板块标签</p>
            {/* H1: only ONE per page, contains core business keyword */}
            <h1>页面标题 — 品牌名</h1>
            <p className="hero-subtitle">
              一句话定位：品牌是品类里差异化定位的品牌
            </p>
          </div>
        </section>

        {/* Content section — H2 for each business dimension */}
        <section className="section">
          <div className="shell">
            {/* H2: write complete viewpoint sentences, not label phrases */}
            <h2>用户越来越少点开链接，越来越多相信AI回答</h2>
            <p>
              用事实替代形容词。少写"领先""卓越"，多放可查事实：
              服务客户数、覆盖城市、所获奖项。
            </p>

            {/* Card grid with H3 sub-titles */}
            <div className="card-grid">
              <article className="card">
                <h3>卡片标题</h3>
                <p>卡片内容</p>
              </article>
              <article className="card">
                <h3>卡片标题</h3>
                <p>卡片内容</p>
              </article>
            </div>
          </div>
        </section>

        {/* Comparison table — use thead + th scope for AI parsing */}
        <section className="section">
          <div className="shell">
            <h2>横向对比：我们和其他方案有什么不同</h2>
            <table>
              <thead>
                <tr>
                  <th scope="col">维度</th>
                  <th scope="col">传统方案</th>
                  <th scope="col">我们的方案</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th scope="row">价格</th>
                  <td>数据</td>
                  <td>数据</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        {/* Image with descriptive alt text */}
        <section className="section">
          <div className="shell">
            <h2>服务展示</h2>
            {/* alt MUST describe what's in the image, not repeat the title */}
            <img 
              src="/images/service-dashboard.png" 
              alt="品牌名 GEO优化仪表盘界面，展示AI提及率和品牌可见度数据" 
              width={800}
              height={450}
            />
          </div>
        </section>

        {/* FAQ section — static render, NO collapse/toggle */}
        <section className="section">
          <div className="shell">
            <h2>常见问题</h2>
            <div className="faq-list">
              <div className="faq-item">
                <h3>用客户的口吻写的完整问题？</h3>
                <p>
                  第一句给结论。后面展开300字以内。避免框架术语。
                  用比喻。给数字不给形容词。
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>

      <SiteFooter />
    </>
  );
}
