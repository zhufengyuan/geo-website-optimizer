# GEO Optimization Checklist

> Complete 5-dimension, 50+ item audit checklist for GEO (Generative Engine
> Optimization) compliance. Based on real-world dual-server deployment achieving
> 100/100 GEO score.

## Scoring Model

| Dimension | Weight | Full Score Condition |
|---|---|---|
| Technical Reachability | 15 pts | GEO 4-files complete + SSR + all pages 200 + Alt coverage |
| Structured Data | 25 pts | Organization + FAQPage + Person + Article + BreadcrumbList full coverage + Article dates |
| Content Assets | 20 pts | 12+ pages + FAQ >= 20 entries + 3+ insight articles + 3+ cases + unique H1 per page |
| Trust Endorsement | 20 pts | Person Schema + sameAs validation + comparison table + business info consistency + email domain unified |
| Domain Consistency | 20 pts | canonical unified + sitemap self-report unified + email unified + content byte-identical + llms.txt no admin |

**Score interpretation**: 90+ excellent, 80-89 good, 70-79 needs work, <70 critical.

---

## Dimension 1: Technical Reachability (15 pts)

### 1.1 GEO Four Files (6 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 1 | robots.txt exists | `curl -s -o /dev/null -w "%{http_code}" {url}/robots.txt` returns 200 | 1.5 |
| 2 | sitemap.xml exists | `curl -s -o /dev/null -w "%{http_code}" {url}/sitemap.xml` returns 200 | 1.5 |
| 3 | llms.txt exists | `curl -s -o /dev/null -w "%{http_code}" {url}/llms.txt` returns 200 | 1.5 |
| 4 | llms-full.txt exists | `curl -s -o /dev/null -w "%{http_code}" {url}/llms-full.txt` returns 200 | 1.5 |

### 1.2 SSR / HTML Direct Output (3 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 5 | Core content in HTML source | `curl -s {url} \| grep "brand_name"` — brand name appears in raw HTML (not JS-rendered) | 3 |

### 1.3 All Pages HTTP 200 (3 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 6 | All sitemap URLs return 200 | Read sitemap.xml, curl each URL, all return 200 | 3 |

### 1.4 Image Alt Coverage (3 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 7 | No empty alt (except decorative) | `curl -s {url} \| grep -c '<img[^>]*alt=""'` — only decorative images have empty alt | 1.5 |
| 8 | All images have alt attribute | `curl -s {url} \| grep -c '<img[^>]*(?!alt)'` — should be 0 | 1.5 |

---

## Dimension 2: Structured Data (25 pts)

### 2.1 Schema Type Coverage (10 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 9 | Organization Schema | `curl -s {url} \| grep '"@type":"Organization"'` on homepage/about/contact | 2 |
| 10 | FAQPage Schema | `curl -s {url}/faq \| grep '"@type":"FAQPage"'` | 2 |
| 11 | Article Schema | Each article page has Article with datePublished + dateModified | 2 |
| 12 | BreadcrumbList Schema | EVERY page has BreadcrumbList (check all sitemap URLs) | 2 |
| 13 | Person Schema | About page has Person Schema with sameAs | 2 |

### 2.2 Schema Precision (5 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 14 | Page type precision | Service page uses Service (not WebPage), tech docs uses TechArticle (not Article) | 2 |
| 15 | CollectionPage for lists | /insights, /cases, /blog use CollectionPage + ItemList | 1.5 |
| 16 | AboutPage / ContactPage | About uses AboutPage, Contact uses ContactPage (not WebPage) | 1.5 |

### 2.3 Article Dates (4 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 17 | datePublished present | Each Article Schema has datePublished | 2 |
| 18 | dateModified present | Each Article Schema has dateModified | 1 |
| 19 | publisher.logo present | Each Article Schema has publisher.logo ImageObject | 1 |

### 2.4 Schema Consistency (6 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 20 | Schema name === H1 | Schema "name" or "headline" matches page H1 text | 2 |
| 21 | Organization core fields consistent | name, url, email, logo same across all pages | 2 |
| 22 | sameAs has 4+ validation links | Organization sameAs includes T0/T1/T2 sources | 2 |

---

## Dimension 3: Content Assets (20 pts)

### 3.1 Page Count (4 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 23 | 12+ pages in sitemap | `curl -s {url}/sitemap.xml \| grep -c "<loc>"` >= 12 | 4 |

### 3.2 FAQ Depth (5 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 24 | FAQ >= 20 entries | `curl -s {url}/faq \| grep -c '"question"'` >= 20 | 3 |
| 25 | FAQ covers 5+ categories | Categories: basics, comparison, service, pricing, trust | 2 |

### 3.3 Content Articles (4 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 26 | 3+ insight articles | /insights/* pages exist with Article Schema | 2 |
| 27 | 3+ case studies | /cases page with 3+ case entries | 2 |

### 3.4 H1 Uniqueness (4 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 28 | One H1 per page | For each page: `curl -s {url} \| grep -c '<h1'` == 1 | 2 |
| 29 | H1 contains brand keyword | H1 text includes core business keyword | 2 |

### 3.5 FAQ Static Render (3 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 30 | FAQ not JS-collapsed | FAQ content visible in raw HTML (not hidden behind JS toggle) | 3 |

---

## Dimension 4: Trust Endorsement (20 pts)

### 4.1 Founder/Person Schema (5 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 31 | Person Schema on about page | `curl -s {url}/about \| grep '"@type":"Person"'` | 2 |
| 32 | Person has sameAs | Person Schema sameAs includes 3+ external validation links | 2 |
| 33 | Person worksFor Organization | Person Schema has worksFor pointing to Organization | 1 |

### 4.2 sameAs Validation Sources (5 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 34 | T0 government source | sameAs includes gov.cn link | 1.5 |
| 35 | T1 media/knowledge | sameAs includes 36kr/zhihu/media | 2 |
| 36 | T2 business info | sameAs includes Tianyancha/Qichacha/Qixin | 1.5 |

### 4.3 Comparison Content (4 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 37 | Competitor comparison table | About or dedicated page has comparison table with thead | 2 |
| 38 | Review Schema (if cases) | Cases page has Review Schema with real ratings | 2 |

### 4.4 Business Info Consistency (3 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 39 | Company name consistent | Same legal name in Schema, footer, about page | 1.5 |
| 40 | Contact info consistent | Same phone/email/address across all pages | 1.5 |

### 4.5 Email Domain Unified (3 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 41 | Email uses primary domain | `grep -r "old_domain" /srv/proj2/src/` returns nothing | 3 |

---

## Dimension 5: Domain Consistency (20 pts)

### 5.1 Canonical (4 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 42 | All pages have canonical | Each page HTML has `<link rel="canonical">` | 2 |
| 43 | Canonical points to primary domain | All canonical URLs use primary domain | 2 |

### 5.2 Sitemap Self-Report (4 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 44 | Sitemap URLs all primary domain | `curl -s {url}/sitemap.xml \| grep "loc"` — all primary domain | 2 |
| 45 | Sitemap includes /faq and /cases | Both present in sitemap | 2 |

### 5.3 Content Parity (5 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 46 | Dual-server HTML byte-identical | MD5/byte count match between servers | 3 |
| 47 | Source file MD5 match | All modified files have same MD5 on both servers | 2 |

### 5.4 llms.txt Security (4 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 48 | llms.txt has no /admin links | `curl -s {url}/llms.txt \| grep -c "admin"` == 0 | 2 |
| 49 | llms.txt has brand description | Contains standard brand description + core advantages | 2 |

### 5.5 301 Redirect (3 pts)

| # | Check | Verification | Points |
|---|---|---|---|
| 50 | Old domain 301 to new | `curl -sI http://old-domain/ \| grep HTTP` returns 301 | 2 |
| 51 | 301 uses statusCode not permanent | Source code uses `statusCode: 301` not `permanent: true` | 1 |

---

## Audit Script Iron Rules

1. **Read URLs from sitemap dynamically** — never hardcode page lists. Sitemap
   has N URLs, check N URLs.
2. **Check each page for each Schema type** — Article Schema lives on article
   pages, not homepage. Don't only check homepage.
3. **Bypass proxy** — sandbox may have proxy configured. Use:
   ```python
   opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
   ```

## Audit Frequency

- **Structure + Technical**: Monthly (sitemap/robots/llms.txt/Schema coverage)
- **Content**: Bi-weekly (FAQ count, article updates, case additions)
- **AI citation rate**: Bi-weekly (12-question sample test on major AI platforms)
