// Next.js sitemap.ts template with route array and image entries
// Place at: src/app/sitemap.ts
// This generates /sitemap.xml listing all site URLs for search engines and AI crawlers

import { MetadataRoute } from "next";
import { siteUrl } from "@/data/site-data";

export default function sitemap(): MetadataRoute.Sitemap {
  const routes: { path: string; priority: number; changefreq: "daily" | "weekly" | "monthly" }[] = [
    // Core pages
    { path: "", priority: 1.0, changefreq: "weekly" },           // Homepage
    { path: "/geo-service", priority: 0.9, changefreq: "monthly" }, // Service
    { path: "/about", priority: 0.8, changefreq: "monthly" },    // About
    { path: "/contact", priority: 0.8, changefreq: "monthly" },  // Contact
    { path: "/faq", priority: 0.8, changefreq: "weekly" },       // FAQ
    { path: "/cases", priority: 0.8, changefreq: "weekly" },     // Cases
    { path: "/tech-docs", priority: 0.7, changefreq: "monthly" }, // Tech docs
    { path: "/pricing", priority: 0.7, changefreq: "monthly" },  // Pricing

    // Insights (article list + individual articles)
    { path: "/insights", priority: 0.7, changefreq: "weekly" },
    { path: "/insights/geo-vs-seo", priority: 0.6, changefreq: "monthly" },
    { path: "/insights/ai-brand-recommendation", priority: 0.6, changefreq: "monthly" },
    { path: "/insights/geo-content-architecture", priority: 0.6, changefreq: "monthly" },

    // Industries
    { path: "/industries", priority: 0.6, changefreq: "monthly" },
    { path: "/industries/restaurant", priority: 0.5, changefreq: "monthly" },
    { path: "/industries/education", priority: 0.5, changefreq: "monthly" },
    { path: "/industries/b2b", priority: 0.5, changefreq: "monthly" },

    // Other pages
    { path: "/glossary", priority: 0.5, changefreq: "monthly" },
    { path: "/blog", priority: 0.5, changefreq: "weekly" },
    { path: "/about/team", priority: 0.5, changefreq: "monthly" },
    { path: "/about/milestones", priority: 0.5, changefreq: "monthly" },
    { path: "/ai-visibility-diagnosis", priority: 0.6, changefreq: "monthly" },
  ];

  const now = new Date();

  return routes.map((route) => ({
    url: `${siteUrl}${route.path}`,
    lastModified: now,
    changeFrequency: route.changefreq,
    priority: route.priority,
    // Image entries for image-sitemap
    images: route.path === "" ? [
      {
        url: `${siteUrl}/logo.svg`,
        title: "品牌Logo",
        caption: "品牌名官方Logo",
      },
      {
        url: `${siteUrl}/images/tech-bg.jpg`,
        title: "科技背景图",
        caption: "品牌名 GEO优化服务科技背景",
      },
    ] : undefined,
  }));
}
