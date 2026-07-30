// Next.js robots.ts template with AI crawler rules
// Place at: src/app/robots.ts
// This generates /robots.txt with rules for all major AI crawlers

import { MetadataRoute } from "next";
import { siteUrl } from "@/data/site-data";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      // ChatGPT / OpenAI
      {
        userAgent: "GPTBot",
        allow: "/",
        disallow: ["/admin/", "/api/"],
      },
      // OpenAI Search Bot
      {
        userAgent: "OAI-SearchBot",
        allow: "/",
        disallow: ["/admin/"],
      },
      // Claude / Anthropic
      {
        userAgent: "ClaudeBot",
        allow: "/",
        disallow: ["/admin/", "/api/"],
      },
      // Perplexity
      {
        userAgent: "PerplexityBot",
        allow: "/",
        disallow: ["/admin/", "/api/"],
      },
      // Google AI
      {
        userAgent: "Google-Extended",
        allow: "/",
        disallow: ["/admin/", "/api/"],
      },
      // Common Crawl (used by many AI models)
      {
        userAgent: "CCBot",
        allow: "/",
        disallow: ["/admin/", "/api/"],
      },
      // AI2 (Allen Institute)
      {
        userAgent: "AI2Bot",
        allow: "/",
        disallow: ["/admin/", "/api/"],
      },
      // Anthropic AI
      {
        userAgent: "anthropic-ai",
        allow: "/",
        disallow: ["/admin/", "/api/"],
      },
      // Baidu
      {
        userAgent: "Baiduspider",
        allow: "/",
        disallow: ["/admin/", "/api/"],
      },
      // ByteDance (Douyin/Toutiao)
      {
        userAgent: "Bytespider",
        allow: "/",
        disallow: ["/admin/", "/api/"],
      },
      // Kimi / Moonshot
      {
        userAgent: "KimiBot",
        allow: "/",
        disallow: ["/admin/", "/api/"],
      },
      // Catch-all: allow public content, block admin/api
      {
        userAgent: "*",
        allow: "/",
        disallow: ["/admin/", "/api/"],
      },
    ],
    sitemap: [
      `${siteUrl}/sitemap.xml`,
    ],
    host: siteUrl,
  };
}
