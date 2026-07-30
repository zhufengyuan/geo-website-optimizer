---
name: geo-website-optimizer
description: "GEO (Generative Engine Optimization) website optimization skill for building AI-friendly corporate websites that get cited by ChatGPT, Claude, Gemini, Perplexity, and Chinese AI engines (Doubao, Kimi, Wenxin). This skill should be used when: creating a new GEO-optimized website from scratch, auditing an existing website for GEO compliance, deploying Schema.org structured data, generating llms.txt/llms-full.txt/robots.txt/sitemap.xml, optimizing image alt text for AI crawlers, expanding FAQ for AI citation, or performing dual-server synchronized deployment. Covers the full lifecycle from audit to content optimization to Schema deployment to AI crawler configuration to server deployment to verification. Based on real-world deployment experience from a dual-server Next.js SSR corporate website achieving 100/100 GEO score."
agent_created: true
---

# GEO Website Optimizer

## Overview

This skill transforms any corporate website into a GEO-optimized site that AI
engines can discover, understand, and cite. It encapsulates the complete
methodology from two production documents (500+ pages combined) and real-world
dual-server deployment experience.

**Core principle**: GEO is not SEO. SEO optimizes for search engine ranking;
GEO optimizes for AI engine citation. The goal is not to rank #1 on Google,
but to be the brand AI mentions when users ask "which XX is good?"

## When to Use

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
- Creating a /tech-docs page with Schema templates as deployment demonstration

## Workflow

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
- Numbers over adjectives ("3 months 1:1, 6 months 1:5" not "gets better")
- Target 30-100+ FAQ entries covering 9+ categories
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

**De-jargonization** (three layers):
1. Delete framework codenames (K-DAF, GUIDE, AVIV → plain descriptions)
2. Replace jargon with metaphors (T2→T0/T1→T3 → "foundation→endorsement→reputation")
3. Give numbers not concepts ("month 1: invisible, month 3: 1:1, month 12: 1:10")

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
- Company overview, GEO definition, core services
- Technical capabilities, engine coverage
- Contact information, brand standard description
- Never include /admin links (security risk)

**sitemap.xml** — must include all pages, with image-sitemap entries

### Phase 5: Server Deployment

Follow `references/deployment-guide.md` for detailed operations.

**Dual-server architecture** (for redundancy):

| Role | Server | SSH Port | App Port | Domain |
|---|---|---|---|---|
| Primary | New server | 22 | 3000 | primary-domain.com |
| Secondary | Old server | 123 | 8333 | secondary-domain.com |

**Deployment script** (`scripts/deploy_geo_site.py`):
```python
python scripts/deploy_geo_site.py \
  --host 106.52.23.83 --port 22 --user root \
  --password 'PASSWORD' --project /srv/proj2 \
  --node-bin /root/.nvm/versions/node/v18.20.8/bin/node \
  --app-port 3000 --pm2-name yunding-geo-site
```

**Standard build sequence** (MUST follow this order):
```bash
cd /srv/proj2
rm -rf .next                          # 1. Clear cache (critical!)
{node_bin} node_modules/.bin/next build  # 2. Build
pm2 delete yunding-geo-site           # 3. Delete (not restart — avoids errored)
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
    md5_new = ssh_new.exec_command(f"md5sum /srv/proj2/{file}")[1].read().decode().split()[0]
    md5_old = ssh_old.exec_command(f"md5sum /srv/proj2/{file}")[1].read().decode().split()[0]
    assert md5_new == md5_old, f"MD5 mismatch: {file}"
```

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
