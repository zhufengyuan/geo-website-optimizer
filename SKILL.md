---
name: geo-website-optimizer
description: "GEO (Generative Engine Optimization) website optimization skill for building AI-friendly corporate websites that get cited by ChatGPT, Claude, Gemini, Perplexity, and Chinese AI engines (Doubao, Kimi, Wenxin). This skill should be used when: creating a new GEO-optimized website from scratch, auditing an existing website for GEO compliance, deploying Schema.org structured data, generating llms.txt/llms-full.txt/robots.txt/sitemap.xml, optimizing image alt text for AI crawlers, expanding FAQ for AI citation, or performing dual-server synchronized deployment. Covers the full lifecycle from audit to content optimization to Schema deployment to AI crawler configuration to server deployment to verification. Based on real-world deployment experience from a dual-server Next.js SSR corporate website achieving 100/100 GEO score."
agent_created: true
---

# GEO Website Optimizer

## Overview

This skill transforms **any company's corporate website** (regardless of
industry — manufacturing, SaaS, healthcare, finance, education, retail, real
estate, etc.) into a GEO-optimized site that AI engines can discover, understand,
and cite. It encapsulates the complete methodology from two production documents
(500+ pages combined) and real-world dual-server deployment experience.

**Core principle**: GEO is not SEO. SEO optimizes for search engine ranking;
GEO optimizes for AI engine citation. The goal is not to rank #1 on Google,
but to be the brand AI mentions when users ask "which XX is good?"

**Universal applicability**: The techniques in this skill — Schema.org structured
data, FAQ optimization, llms.txt generation, AI crawler configuration, content
de-jargonization — apply to corporate websites in any industry. The key is tailoring
the **content** to the client's domain while following the same **structural** GEO
principles.

## When to Use

**Any company, any industry** — this skill works for corporate websites in
manufacturing, healthcare, finance, SaaS, education, real estate, retail,
and beyond. The structural optimization techniques are universal; you'll
tailor the content to the client's domain.

- Building a new corporate website with GEO optimization from scratch
- Auditing an existing website's GEO compliance (5 dimensions, 50+ checks)
- Deploying or fixing Schema.org structured data (Organization, FAQPage,
  Article, BreadcrumbList, Person, Service, etc.)
- Generating llms.txt / llms-full.txt for AI crawler guidance
- Configuring robots.txt for AI crawlers (GPTBot, ClaudeBot, PerplexityBot,
  OAI-SearchBot, Baiduspider, Bytespider, KimiBot, etc.)
- Expanding FAQ for maximum AI citation coverage
- Performing dual-server synchronized deployment via SSH/SFTP
- Optimizing image alt text for AI image recognition
- Creating a knowledge base or documentation page with Schema templates

## Workflow

### Phase 0: Understand the Client's Industry

Before applying any GEO technique, understand the client's business context:

1. **What industry?** (manufacturing, SaaS, healthcare, finance, education, etc.)
2. **What does AI need to know to cite this brand?** (products, certifications, case studies, founders, locations)
3. **What questions do target customers ask?** (translate real customer language into FAQ)
4. **What external validation exists?** (government registrations, media reports, industry awards, platform profiles)

This industry-agnostic step ensures the GEO techniques are tailored to the
client's domain rather than blindly applying templates.

### Phase 1: GEO Audit (if existing site)

Run the audit script to assess current GEO compliance:

```
python scripts/geo_audit.py --url https://example.com
```

The audit checks 5 dimensions (see `references/geo-optimization-checklist.md`):
1. **Technical Reachability** (15 pts) — GEO 4-files, SSR, HTTP 200, Alt coverage
2. **Structured Data** (25 pts) — Schema types coverage, Article dates, precision
3. **Content Assets** (20 pts) — Page count, FAQ depth, articles, unique H1
4. **Trust Endorsement** (20 pts) — Person Schema, sameAs, comparison tables
5. **Domain Consistency** (20 pts) — canonical, sitemap, email, content parity

**Three iron rules for audit scripts**:
1. Read URLs dynamically from sitemap.xml — never hardcode page lists
2. Check each page for each Schema type — Article Schema lives on article pages
3. Bypass proxy with `ProxyHandler({})` — sandbox proxies cause false negatives

### Phase 2: Content Optimization

Follow `references/content-strategy.md` for:

**FAQ Writing (highest GEO ROI)**:
- Use customer's natural language for questions (not academic terms)
- One question = one answer, under 300 words
- Conclusion first, then explanation
- Numbers over adjectives ("reduces cost by 30%" not "cost-effective")
- Target 30-100+ FAQ entries covering the client's product/service/industry
- FAQ must be static HTML (no JS collapse) — AI crawlers need full content

**Page Content Structure** (concentric circle model):
- H1 = core business keyword + brand name (only 1 per page)
- H2 = key business dimensions (module titles)
- H3 = card/sub-item titles (strict H1 > H2 > H3 hierarchy)
- FAQ section at page bottom, Q&A format, static render

**Image Alt Text**:
- Product images: "{brand} {product} {angle/detail/scene}"
- Certificates: "{certificate name} certification, {brand} {industry}"
- Factory photos: "{brand} {location}, {industry} factory floor"
- Decorative images: empty alt="" (explicitly marked as decoration)
- Never duplicate title as alt — AI penalizes keyword stuffing

**De-jargonization** (three layers, applies to any industry):
1. Delete internal framework codenames → replace with plain business descriptions
2. Replace industry jargon with everyday metaphors → "AI-driven predictive analytics" → "uses data to predict what customers want next"
3. Give numbers not concepts → "improves efficiency" → "cuts processing time from 2 hours to 15 minutes"

### Phase 3: Schema.org Structured Data

Follow `references/schema-templates.md` for complete JSON-LD templates.

**Page-to-Schema mapping** (precision over quantity):

| Page Type | Schema Types | Key Rule |
|---|---|---|
| Homepage | Organization + Service + FAQPage + BreadcrumbList + WebSite | Most complete Org Schema (18+ fields) |
| Service page | Service + Offer + BreadcrumbList | Don't use WebPage |
| Article list | CollectionPage + ItemList + BreadcrumbList | Don't use WebPage |
| Article detail | Article + BreadcrumbList | Must have datePublished/dateModified |
| Tech docs | TechArticle + HowTo + BreadcrumbList | More precise than Article |
| About page | AboutPage + Organization + Person + BreadcrumbList | Founder with sameAs links |
| Contact page | ContactPage + Organization + BreadcrumbList | email field required |
| FAQ page | FAQPage + BreadcrumbList | All Q&A as mainEntity |
| Cases | Article + Review + CollectionPage + BreadcrumbList | Review must be real |
| Glossary | DefinedTermSet + BreadcrumbList | For term definitions |

**Critical Schema rules**:
- Schema `name` must equal page H1 (AI cross-validates)
- BreadcrumbList on EVERY page including homepage (1-level for home)
- Article Schema must have datePublished + dateModified + author + publisher.logo
- Organization sameAs should have 4-10 external validation links (T0 government,
  T1 media/knowledge platforms, T2 business info platforms)
- Person Schema for founders with sameAs (Tianyancha, Qichacha, media reports)

### Phase 4: AI Crawler Configuration

**robots.txt** — allow all major AI crawlers, block /admin/ and /api/:

```
User-agent: GPTBot
Allow: /
Disallow: /admin/
Disallow: /api/

User-agent: ClaudeBot
Allow: /
Disallow: /admin/

User-agent: PerplexityBot
Allow: /
Disallow: /admin/

User-agent: OAI-SearchBot
Allow: /

User-agent: Baiduspider
Allow: /

User-agent: Bytespider
Allow: /

User-agent: KimiBot
Allow: /

User-agent: CCBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: *
Disallow: /admin/
Disallow: /api/
Allow: /

Sitemap: https://{domain}/sitemap.xml
```

**llms.txt** — AI-specific site navigation (at domain root):
- Brand summary (1-2 sentences with core keywords)
- Core knowledge page links
- AI citation guide (standard brand description, core advantages, contact)

**llms-full.txt** — extended AI knowledge base:
- Company overview, core products/services, industry positioning
- Technical capabilities, certifications, case studies
- Contact information, brand standard description
- Never include /admin links (security risk)

**sitemap.xml** — must include all pages, with image-sitemap entries

### Phase 5: Server Deployment

Follow `references/deployment-guide.md` for detailed operations.

**Dual-server architecture** (for redundancy, configurable per client):

| Role | SSH Port | App Port | Domain |
|---|---|---|---|
| Primary | 22 | {primary_port} | primary-domain.com |
| Secondary | {secondary_ssh} | {secondary_port} | secondary-domain.com |

**Deployment script** (`scripts/deploy_geo_site.py`):
```python
python scripts/deploy_geo_site.py \
  --host {server_ip} --port {ssh_port} --user {ssh_user} \
  --password '{ssh_password}' --project /srv/{project_name} \
  --node-bin {node_binary_path} \
  --app-port {app_port} --pm2-name {pm2_process_name}
```

**Standard build sequence** (MUST follow this order):
```bash
cd /srv/{project_name}
rm -rf .next                          # 1. Clear cache (critical!)
{node_bin} node_modules/.bin/next build  # 2. Build
pm2 delete {pm2_name}                 # 3. Delete (not restart — avoids errored)
pm2 start ecosystem.config.js         # 4. Fresh start
sleep 5                               # 5. Wait for warmup
curl -s -o /dev/null -w "%{http_code}" http://localhost:{port}/  # 6. Verify
```

**PM2 errored state recovery**:
- `pm2 restart` from errored state does NOT work
- Must `pm2 delete` then `pm2 start` (errored is sticky)
- Check `.next/BUILD_ID` exists after build

**Key pitfalls** (see `references/deployment-guide.md` for full list):
- `.next` cache not cleared → CSS/component changes don't take effect
- PM2 restart from errored → stays errored, must delete + start
- Python f-string `{{` conflicts with JSX `{{ }}` → use `.replace()` templates
- paramiko SFTP `read()` returns bytes → must `.decode('utf-8')`
- Password with `$0` in bash → shell interprets as `/usr/bin/bash`, use Python file
- ESLint blocks build → set `eslint: { ignoreDuringBuilds: true }` in next.config.js
- Node version mismatch → Next.js 14+ needs Node 18+; Node 16 max Next.js 13.4.x

### Phase 6: Verification

**Verification checklist** (per server):

| Check | Command | Expected |
|---|---|---|
| Homepage 200 | `curl -s -o /dev/null -w "%{http_code}" http://localhost:{port}/` | 200 |
| All routes 200 | `curl -s -o /dev/null -w "%{http_code}" http://localhost:{port}/{route}` | 200 |
| llms.txt | `curl -s http://localhost:{port}/llms.txt \| wc -c` | > 500 |
| llms-full.txt | `curl -s http://localhost:{port}/llms-full.txt \| wc -c` | > 2000 |
| robots.txt | `curl -s http://localhost:{port}/robots.txt \| grep -c "User-agent"` | >= 11 |
| sitemap URLs | `curl -s http://localhost:{port}/sitemap.xml \| grep -c "<loc>"` | >= 12 |
| FAQ entries | `curl -s http://localhost:{port}/faq \| grep -c "question"` | >= 30 |
| Empty alt count | `curl -s http://localhost:{port}/ \| grep -c 'alt=""'` | decorative only |
| BreadcrumbList | `curl -s http://localhost:{port}/{route} \| grep -c "BreadcrumbList"` | >= 1 |

**Dual-server parity check**:
```python
# Source file MD5 must match
for file in modified_files:
    md5_primary = ssh_primary.exec_command(f"md5sum /srv/{project_name}/{file}")[1].read().decode().split()[0]
    md5_secondary = ssh_secondary.exec_command(f"md5sum /srv/{project_name}/{file}")[1].read().decode().split()[0]
    assert md5_primary == md5_secondary, f"MD5 mismatch: {file}"
```

## Production Architecture Reference

> Based on the live GEO-optimized website at **https://xcloud-top.com** (24 pages,
> 14 Schema types, 115+ FAQ entries, dual-server deployment). This section
> documents the real architecture so new GEO site builds can replicate the
> proven patterns.

### Site Architecture (24-Page Structure)

The reference site uses Next.js 13.4 SSR on Node 16 + PM2 cluster mode,
with all content rendered server-side and all Schema injected as JSON-LD
in `<head>`. Full page map:

```
Homepage (/)                          ← Organization + Service + FAQPage + WebSite+SearchAction
├── /geo-service                      ← Service + Offer
├── /ai-visibility-diagnosis          ← WebPage (diagnosis tool)
├── /faq (115+ entries)               ← FAQPage
├── /cases                            ← Article×3 + Review×3 + CollectionPage
├── /tech-docs (57K chars)            ← TechArticle + HowTo
├── /glossary (30 terms)              ← DefinedTermSet
├── /pricing                          ← Service + Offer×3
├── /blog                             ← CollectionPage
├── /about                            ← AboutPage + Organization + Person
│   ├── /about/team                   ← Person×3
│   └── /about/milestones             ← Article
├── /contact                          ← ContactPage + Organization
├── /insights                         ← CollectionPage + ItemList
│   ├── /insights/geo-vs-seo          ← Article + FAQPage
│   ├── /insights/ai-brand-recommendation   ← Article + FAQPage
│   ├── /insights/geo-content-architecture  ← Article + FAQPage
│   ├── /insights/source-pyramid      ← Article + FAQPage
│   └── /insights/geo-roi-model       ← Article + FAQPage
├── /industries                       ← CollectionPage
│   ├── /industries/restaurant        ← Article + FAQPage
│   ├── /industries/education         ← Article + FAQPage
│   └── /industries/b2b               ← Article + FAQPage
├── /geo-vs-seo (legacy redirect)     ← FAQPage
└── /admin (robots disallowed)        ← Dashboard + CRUD management
```

**Design rule**: Every page has BreadcrumbList. No exception — including the homepage (1-level: Home → Home).

### Data Flow Architecture (Frontend-Backend Linkage)

The reference site uses a **JSON file storage + data access layer + Content API**
pattern instead of a traditional database. This keeps deployment lightweight
(zero database dependency) while enabling dynamic content management.

```
┌──────────────┐     REST API      ┌──────────────┐     fs.readFile     ┌──────────────┐
│  Admin Panel │ ── GET/POST/PUT ─→│ Content API   │ ────────────────→ │ data/dynamic/ │
│  (/admin)    │                   │ /api/content  │                    │ *.json files  │
└──────────────┘                   └──────────────┘                    └──────────────┘
                                         ↑                                    ↑
                                    data-store.ts                      Single Source
                                    (read/write)                       of Truth
                                         ↑
                                   ┌──────────────┐
                                   │ SSR Pages     │
                                   │ (Server Comp) │
                                   └──────────────┘
```

**Core files**:
| File | Role |
|---|---|
| `src/lib/data-store.ts` | Unified read/write layer: `getFAQ()`, `saveFAQ()`, `getCases()`, etc. |
| `src/app/api/content/route.ts` | REST API with `?type=faq|cases|hero|contact|brandSignals|all` |
| `data/dynamic/faq.json` | 115+ FAQ entries (main entity data) |
| `data/dynamic/cases.json` | Customer case studies |
| `data/dynamic/hero.json` | Hero section content |
| `data/dynamic/contact.json` | Contact info (phone/email/address) |
| `data/dynamic/brandSignals.json` | Trust metrics (clients/cities/industries) |
| `src/lib/site-data.ts` | Static fallback (client-safe, no `fs` imports) |

**Critical rule**: `data-store.ts` uses Node.js `fs` module — it MUST only be
imported by Server Components or API Routes. Client components (like site-header)
import `site-data.ts` for static data. Never cross the boundary.

### Design System

The reference site uses a **Design Token + Editorial Narrative + Visual Hierarchy**
system rather than template-based design. This ensures AI-friendly semantic
structure while maintaining brand differentiation.

**Design Tokens (CSS Custom Properties)**:
```css
:root {
  --ink: #1a2b32;           /* Primary text */
  --muted: #6b7d85;         /* Secondary text */
  --line: #e2e8f0;          /* Borders */
  --surface: #f8fafb;       /* Page background */
  --card: #ffffff;          /* Card background */
  --brand: #2ab39f;         /* Brand accent (teal) */
  --brand-light: #e8f8f5;   /* Brand light bg */
  --brand-dark: #1e8a7a;    /* Brand hover/active */
}
```

**Typography system**:
- **Serif** (STSong/Songti SC) — Hero titles, large headings
- **Sans-serif** (PingFang SC) — Body text, descriptions
- **Monospace** (IBM Plex Mono) — Tags, metadata, code
- **`clamp()` scaling** — No media query breakpoints; fluid scaling

**Editorial narrative structure** (per page):
```
Hero (H1 + lead paragraph)
  → Story segment (context & problem)
  → Thesis blocks (key arguments, H2 × N)
  → Visual break (dark section with radial gradient)
  → Service cards (Service + Offer cards)
  → Form/CTA section
  → FAQ section (static render, all Q&A visible)
```

**Component library**:
| Component | Purpose | Variants |
|---|---|---|
| Shell | Page container | — |
| Pill Button | CTAs | dark (primary) / light (secondary, light bg) / ghost (secondary, dark bg) / accent (form submit) |
| Editorial Hero | Page opening | with/without background image |
| Story Grid | Narrative content | 1-col / 2-col / 3-col |
| Article Block | Insight/article cards | with/without image |
| Service Card | Service offerings | with icon grid |
| FAQ Card | FAQ entries | numbered card, H3 question + P answer |
| Footer Grid | Site footer | company info + nav + trust signals |

**Design rules**:
- No hardcoded color values — all colors via `:root` CSS variables
- H2 titles are complete opinion statements, not labels ("用户越来越少点链接" not "我们的优势")
- Every content section has an Eyebrow label above the title
- Hero height: 68vh desktop, 58vh mobile (not 100vh)
- Dark section every 2-3 light sections (with radial gradient glow)
- Navbar: `position: sticky; backdrop-filter: blur(18px)` with scroll-triggered background

### Content Matrix Deployment Pattern

When deploying multiple new pages at once, use a **parameterized template +
batch generation** pattern rather than hand-writing each page:

```python
# Template function generates page content from parameters
def make_industry_page(slug, name, emoji, challenges, solutions, faq_list):
    template = '''export default function Page() {
  return (<div>
    <SiteHeader />
    <EditorialHero title="{name}行业GEO优化方案" />
    <StoryGrid items={challenges} />
    <ServiceCard items={solutions} />
    <FAQCard items={faq_list} />
    <JsonLd data={articleSchema} />
    <JsonLd data={breadcrumbSchema} />
    <SiteFooter />
  </div>);
}'''
    return (template
        .replace("{slug}", slug)
        .replace("{name}", name)
        .replace("{emoji}", emoji)
    )

# Batch deploy via SFTP
for industry in ["restaurant", "education", "b2b"]:
    content = make_industry_page(industry, name, emoji, ...)
    sftp.putfo(io.BytesIO(content.encode()), f"/srv/proj2/src/app/industries/{industry}/page.tsx")
```

**After batch deployment, always update**:
1. `sitemap.ts` — add new routes
2. `robots.ts` — verify no new blocks needed
3. Rebuild (`rm -rf .next && build && pm2 delete && pm2 start`)

**JSX/Python gotcha**: Python f-string `{{` conflicts with JSX `{{ }}`.
Use `.replace()` templates, not f-strings, when generating JSX.

### Dual-Server Architecture

The reference site runs on two independent servers for redundancy:

| | Primary Server | Secondary Server |
|---|---|---|
| IP | 106.52.23.83 | 1.117.188.4 |
| SSH Port | 22 | 123 |
| App Port | 3000 | 8333 |
| Node Path | `/root/.nvm/versions/node/v18.20.8/bin/node` | `/usr/bin/node` |
| Domain | xcloud-top.com | sunfitness123.xyz:8333 |
| PM2 Name | `yunding-geo-site` | `yunding-geo-site` |

**Sync workflow**:
1. Deploy & build on primary server first
2. Read modified source files from primary via SFTP
3. Write to secondary server corresponding paths
4. Build on secondary server
5. Verify both servers independently (HTTP 200, Schema check, FAQ count, sitemap URL count)

**Parameterized deployment** — each server has different Node path, port, and
ecosystem.config.js settings. Use a config dict in the deployment script, not
hardcoded paths.

### Engineering Patterns Reference

From real-world production experience (see reference docs for full details):

| Pattern | File/Context | Key Insight |
|---|---|---|
| **PM2 errored recovery** | deployment | `pm2 restart` from `errored` does NOT work; must `pm2 delete` + `pm2 start` |
| **.next cache clearing** | deployment | CSS/component changes don't take effect unless `rm -rf .next` before build |
| **ESLint build blocking** | next.config.js | Set `eslint: { ignoreDuringBuilds: true }` to prevent ESLint from blocking production builds |
| **Python f-string + JSX** | page generation | f-string `{{` conflicts with JSX `{{ }}` — use `.replace()` templates |
| **CRLF line endings** | git/cross-platform | `.gitattributes`: `* text=auto eol=lf`; Linux scripts must be LF |
| **Chinese quote contamination** | JSX editing | `grep -P '[\x{201C}\x{201D}]'` to find full-width quotes in code |
| **paramiko encoding** | remote ops | SFTP `read()` returns bytes → always `.decode('utf-8')` |
| **Password special chars** | bash inline Python | `$0` in password → shell interprets as `/usr/bin/bash`; use Python file |
| **Multi-line text replace** | JSX content editing | Never assume text is single-line; use `sed -n` to check actual format first |
| **PM2 cluster warmup** | verification | `sleep 5` after `pm2 start` before `curl` validation |
| **Component version drift** | dual-server | Two servers may have different component versions → adapt layout.tsx per server |
| **Server component boundary** | Next.js App Router | `fs`-using code (data-store.ts) must ONLY be imported by Server Components or API Routes |
| **Large file GitHub API** | deployment tools | GitHub Contents API returns empty for files > 1MB; use Git Blob API instead |

### When to Use Each Reference Document

The skill is supplemented by two production documents that provide deeper
context from real-world build experience:

| Document | Focus | When to Load |
|---|---|---|
| **官网GEO内容优化开发笔记.md** | Content-layer optimization: FAQ writing, de-jargonization, Schema coverage, sameAs expansion, content matrix deployment, PM2 recovery, encoding gotchas | When doing content work, Schema deployment, FAQ expansion, or debugging deployment issues |
| **官网建设项目实施指南.md** | Project management & architecture: 8-module development sequence, data flow architecture, design system, dual-server patterns, visual design, engineering pitfalls | When planning a new site build, architecting data flow, or setting up design systems |

Both are in the `zhufengyuan/geo_file` repository on GitHub.

## Resources

### references/

- **`geo-optimization-checklist.md`** — Complete 5-dimension, 50+ item GEO audit
  checklist with scoring model and verification commands. Load when performing
  GEO audits or preparing for deployment verification.

- **`schema-templates.md`** — Complete JSON-LD templates for all Schema.org types
  (Organization, FAQPage, Article, BreadcrumbList, Person, Service, CollectionPage,
  TechArticle, HowTo, Review, DefinedTermSet, WebSite+SearchAction). Load when
  implementing or fixing structured data.

- **`deployment-guide.md`** — Dual-server deployment operations guide including
  paramiko SSH/SFTP patterns, PM2 management, build sequence, pitfall list, and
  dual-server sync workflow. Load when deploying to production servers.

- **`content-strategy.md`** — Content writing guidelines including FAQ writing
  principles, page content structure (concentric circle model), image alt text
  rules, llms.txt content strategy, and de-jargonization methodology. Load when
  writing or optimizing website content.

### scripts/

- **`geo_audit.py`** — Automated GEO audit script. Fetches sitemap.xml, checks
  each page for Schema coverage, Alt text, H1 uniqueness, and GEO file existence.
  Outputs a score report. Run with: `python geo_audit.py --url https://example.com`

- **`deploy_geo_site.py`** — Dual-server deployment script. SSH connect, SFTP
  upload modified files, build, PM2 restart, and verify. Supports parameterized
  node binary path, app port, and PM2 process name for different server configs.

### assets/

- **`page-template.tsx`** — Next.js 13+ App Router page template with complete
  Schema.org JSON-LD, BreadcrumbList, proper H1/H2 hierarchy, and component
  imports. Copy and customize for new pages.

- **`llms-template.txt`** — llms.txt template with brand summary, core page
  links, and AI citation guide sections.

- **`robots-template.ts`** — Next.js robots.ts template with 11+ AI crawler
  rules and sitemap references.

- **`sitemap-template.ts`** — Next.js sitemap.ts template with route array,
  priority/changefreq settings, and image entries.
