#!/usr/bin/env python3
"""
GEO Audit Script — Automated GEO compliance checker for corporate websites.

Checks 5 dimensions:
1. Technical Reachability (GEO 4-files, SSR, HTTP 200, Alt coverage)
2. Structured Data (Schema types, Article dates, precision)
3. Content Assets (Page count, FAQ depth, articles, H1 uniqueness)
4. Trust Endorsement (Person Schema, sameAs, comparison content)
5. Domain Consistency (canonical, sitemap, email, llms.txt security)

Usage:
    python geo_audit.py --url https://example.com
    python geo_audit.py --url https://example.com --verbose
"""

import argparse
import json
import re
import sys
import urllib.request
from urllib.parse import urljoin, urlparse

# Bypass proxy (sandbox environments may have proxy configured)
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
urllib.request.install_opener(opener)


def fetch(url, timeout=15):
    """Fetch URL content, return (status_code, html_text)."""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; GEO-Audit-Bot/1.0)'
        })
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.getcode(), resp.read().decode('utf-8', errors='replace')
    except urllib.error.HTTPError as e:
        return e.code, ''
    except Exception as e:
        return 0, str(e)


def fetch_sitemap_urls(base_url):
    """Read sitemap.xml and return list of all URLs."""
    status, xml = fetch(urljoin(base_url, '/sitemap.xml'))
    if status != 200 or not xml:
        # Try common sitemap locations
        status, xml = fetch(urljoin(base_url, '/sitemap-0.xml'))
        if status != 200 or not xml:
            return [base_url]
    
    urls = re.findall(r'<loc>(.*?)</loc>', xml)
    # Filter to page URLs (not image sitemap URLs)
    page_urls = [u for u in urls if not u.endswith(('.jpg', '.png', '.svg', '.webp'))]
    return page_urls if page_urls else [base_url]


def extract_jsonld_blocks(html):
    """Extract all JSON-LD blocks from HTML."""
    pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
    blocks = re.findall(pattern, html, re.DOTALL)
    results = []
    for block in blocks:
        try:
            data = json.loads(block.strip())
            if isinstance(data, list):
                results.extend(data)
            else:
                results.append(data)
        except json.JSONDecodeError:
            pass
    return results


def get_schema_types(jsonld_blocks):
    """Get set of all @type values from JSON-LD blocks."""
    types = set()
    for block in jsonld_blocks:
        if '@type' in block:
            t = block['@type']
            if isinstance(t, list):
                types.update(t)
            else:
                types.add(t)
    return types


def count_empty_alt(html):
    """Count images with empty alt attribute (should be decorative only)."""
    # Match img tags with alt="" 
    empty_alt = len(re.findall(r'<img[^>]*alt\s*=\s*["\']["\']', html, re.IGNORECASE))
    # Match img tags without alt at all
    all_imgs = len(re.findall(r'<img[^>]*>', html, re.IGNORECASE))
    no_alt = len(re.findall(r'<img(?![^>]*\salt\s*=)[^>]*>', html, re.IGNORECASE))
    return empty_alt, no_alt, all_imgs


def count_h1(html):
    """Count H1 tags in HTML."""
    return len(re.findall(r'<h1[\s>]', html, re.IGNORECASE))


def audit_dimension_1(base_url, sitemap_urls):
    """Technical Reachability (15 pts)."""
    score = 0
    details = []
    
    # 1.1 GEO Four Files (6 pts)
    for filename, pts in [('robots.txt', 1.5), ('sitemap.xml', 1.5), ('llms.txt', 1.5), ('llms-full.txt', 1.5)]:
        status, content = fetch(urljoin(base_url, '/' + filename))
        ok = status == 200 and len(content) > 50
        score += pts if ok else 0
        details.append(f"  {'✅' if ok else '❌'} /{filename}: HTTP {status}, {len(content)} bytes")
    
    # 1.2 SSR check (3 pts) — check if brand name appears in raw HTML
    status, html = fetch(base_url)
    # Heuristic: if page has substantial text content in raw HTML
    text_length = len(re.sub(r'<[^>]+>', '', html).strip())
    ssr_ok = text_length > 1000
    score += 3 if ssr_ok else 0
    details.append(f"  {'✅' if ssr_ok else '❌'} SSR/HTML content: {text_length} chars in raw HTML")
    
    # 1.3 All pages HTTP 200 (3 pts)
    all_ok = True
    for url in sitemap_urls:
        status, _ = fetch(url)
        if status != 200:
            all_ok = False
            details.append(f"  ❌ {url}: HTTP {status}")
    score += 3 if all_ok else 0
    details.append(f"  {'✅' if all_ok else '❌'} All {len(sitemap_urls)} sitemap URLs return 200")
    
    # 1.4 Image Alt coverage (3 pts)
    status, html = fetch(base_url)
    empty_alt, no_alt, total_imgs = count_empty_alt(html)
    alt_ok = no_alt == 0  # No images missing alt entirely
    score += 1.5 if alt_ok else 0
    score += 1.5 if total_imgs > 0 and empty_alt < total_imgs * 0.5 else 0
    details.append(f"  {'✅' if alt_ok else '❌'} Alt coverage: {total_imgs} imgs, {empty_alt} empty alt, {no_alt} missing alt")
    
    return score, details


def audit_dimension_2(base_url, sitemap_urls):
    """Structured Data (25 pts)."""
    score = 0
    details = []
    
    # Check each page for Schema types
    page_schemas = {}
    for url in sitemap_urls:
        status, html = fetch(url)
        if status == 200:
            blocks = extract_jsonld_blocks(html)
            types = get_schema_types(blocks)
            page_schemas[url] = types
    
    all_types = set()
    for types in page_schemas.values():
        all_types.update(types)
    
    # 2.1 Schema Type Coverage (10 pts)
    homepage_url = base_url.rstrip('/') + '/' if base_url.endswith('/') else base_url
    homepage_types = page_schemas.get(homepage_url, set()) or page_schemas.get(base_url, set())
    
    org_ok = 'Organization' in all_types
    faq_ok = 'FAQPage' in all_types
    article_ok = 'Article' in all_types or 'TechArticle' in all_types
    breadcrumb_ok = 'BreadcrumbList' in all_types
    person_ok = 'Person' in all_types
    
    score += 2 if org_ok else 0
    score += 2 if faq_ok else 0
    score += 2 if article_ok else 0
    score += 2 if breadcrumb_ok else 0
    score += 2 if person_ok else 0
    
    details.append(f"  {'✅' if org_ok else '❌'} Organization Schema")
    details.append(f"  {'✅' if faq_ok else '❌'} FAQPage Schema")
    details.append(f"  {'✅' if article_ok else '❌'} Article Schema")
    details.append(f"  {'✅' if breadcrumb_ok else '❌'} BreadcrumbList Schema")
    details.append(f"  {'✅' if person_ok else '❌'} Person Schema")
    
    # 2.2 BreadcrumbList on every page (2 pts)
    pages_without_breadcrumb = [url for url, types in page_schemas.items() if 'BreadcrumbList' not in types]
    breadcrumb_all = len(pages_without_breadcrumb) == 0
    score += 2 if breadcrumb_all else 0
    if not breadcrumb_all:
        details.append(f"  ❌ {len(pages_without_breadcrumb)} pages missing BreadcrumbList")
    else:
        details.append(f"  ✅ BreadcrumbList on all {len(sitemap_urls)} pages")
    
    # 2.3 Schema precision (3 pts)
    has_service = 'Service' in all_types
    has_collection = 'CollectionPage' in all_types
    has_tech_article = 'TechArticle' in all_types
    has_about_page = 'AboutPage' in all_types
    has_contact_page = 'ContactPage' in all_types
    
    precision_count = sum([has_service, has_collection, has_tech_article, has_about_page, has_contact_page])
    score += min(3, precision_count * 0.6)
    details.append(f"  Schema precision: Service={has_service}, CollectionPage={has_collection}, TechArticle={has_tech_article}, AboutPage={has_about_page}, ContactPage={has_contact_page}")
    
    # 2.4 Article dates (4 pts)
    article_pages = [url for url, types in page_schemas.items() if 'Article' in types or 'TechArticle' in types]
    articles_with_dates = 0
    for url in article_pages:
        status, html = fetch(url)
        blocks = extract_jsonld_blocks(html)
        for block in blocks:
            if block.get('@type') in ('Article', 'TechArticle'):
                if 'datePublished' in block:
                    articles_with_dates += 1
                    break
    
    if article_pages:
        date_ratio = articles_with_dates / len(article_pages)
        score += 4 * date_ratio
        details.append(f"  {'✅' if date_ratio == 1 else '❌'} Article dates: {articles_with_dates}/{len(article_pages)} have datePublished")
    else:
        score += 4
        details.append("  ⚠️ No Article pages found (skipping date check)")
    
    # 2.5 Organization sameAs (4 pts)
    status, html = fetch(base_url)
    blocks = extract_jsonld_blocks(html)
    for block in blocks:
        if block.get('@type') == 'Organization' and 'sameAs' in block:
            sameas_count = len(block['sameAs']) if isinstance(block['sameAs'], list) else 1
            score += min(4, sameas_count * 0.4)
            details.append(f"  ✅ Organization sameAs: {sameas_count} links")
            break
    else:
        details.append("  ❌ Organization sameAs not found")
    
    # 2.6 Schema name === H1 consistency (2 pts)
    h1_count = count_h1(html)
    h1_ok = h1_count == 1
    score += 2 if h1_ok else 0
    details.append(f"  {'✅' if h1_ok else '❌'} Homepage H1 count: {h1_count}")
    
    return score, details


def audit_dimension_3(base_url, sitemap_urls):
    """Content Assets (20 pts)."""
    score = 0
    details = []
    
    # 3.1 Page count (4 pts)
    page_count = len(sitemap_urls)
    score += min(4, page_count / 3)
    details.append(f"  Sitemap URLs: {page_count} ({'✅' if page_count >= 12 else '❌'} need 12+)")
    
    # 3.2 FAQ depth (5 pts)
    faq_url = urljoin(base_url, '/faq')
    status, html = fetch(faq_url)
    faq_count = html.count('"question"') if status == 200 else 0
    # Also check FAQPage mainEntity count
    blocks = extract_jsonld_blocks(html)
    for block in blocks:
        if block.get('@type') == 'FAQPage' and 'mainEntity' in block:
            faq_count = max(faq_count, len(block['mainEntity']))
    
    score += min(3, faq_count / 7)  # 20+ = 3 pts
    score += 2 if faq_count >= 20 else 0
    details.append(f"  FAQ entries: {faq_count} ({'✅' if faq_count >= 20 else '❌'} need 20+)")
    
    # 3.3 H1 uniqueness per page (4 pts)
    h1_issues = 0
    for url in sitemap_urls[:10]:  # Check first 10 pages
        status, html = fetch(url)
        if status == 200:
            h1_count = count_h1(html)
            if h1_count != 1:
                h1_issues += 1
                details.append(f"  ❌ {url}: {h1_count} H1 tags")
    
    score += 2 if h1_issues == 0 else 0
    
    # 3.4 FAQ static render (3 pts)
    if status == 200:
        # Check if FAQ content is in raw HTML (not JS-rendered)
        faq_static = 'question' in html or 'Question' in html
        score += 3 if faq_static else 0
        details.append(f"  {'✅' if faq_static else '❌'} FAQ static render (visible in raw HTML)")
    
    # 3.5 Content articles (4 pts)
    insights_url = urljoin(base_url, '/insights')
    status, html = fetch(insights_url)
    has_insights = status == 200 and len(html) > 1000
    score += 2 if has_insights else 0
    details.append(f"  {'✅' if has_insights else '❌'} /insights page exists")
    
    cases_url = urljoin(base_url, '/cases')
    status, html = fetch(cases_url)
    has_cases = status == 200 and len(html) > 1000
    score += 2 if has_cases else 0
    details.append(f"  {'✅' if has_cases else '❌'} /cases page exists")
    
    return score, details


def audit_dimension_4(base_url, sitemap_urls):
    """Trust Endorsement (20 pts)."""
    score = 0
    details = []
    
    # 4.1 Person Schema on about page (5 pts)
    about_url = urljoin(base_url, '/about')
    status, html = fetch(about_url)
    blocks = extract_jsonld_blocks(html)
    has_person = 'Person' in get_schema_types(blocks)
    score += 2 if has_person else 0
    details.append(f"  {'✅' if has_person else '❌'} Person Schema on /about")
    
    # Check Person sameAs
    person_sameas = 0
    for block in blocks:
        if block.get('@type') == 'Person' and 'sameAs' in block:
            person_sameas = len(block['sameAs']) if isinstance(block['sameAs'], list) else 1
    score += 2 if person_sameas >= 3 else (1 if person_sameas > 0 else 0)
    score += 1 if person_sameas > 0 else 0
    details.append(f"  Person sameAs: {person_sameas} links")
    
    # 4.2 Organization sameAs with T0/T1/T2 (5 pts)
    status, html = fetch(base_url)
    blocks = extract_jsonld_blocks(html)
    org_sameas = []
    for block in blocks:
        if block.get('@type') == 'Organization' and 'sameAs' in block:
            org_sameas = block['sameAs'] if isinstance(block['sameAs'], list) else [block['sameAs']]
    
    has_t0 = any('gov.cn' in s for s in org_sameas)
    has_t1 = any(d in ' '.join(org_sameas) for d in ['36kr', 'zhihu', 'sohu'])
    has_t2 = any(d in ' '.join(org_sameas) for d in ['tianyancha', 'qcc', 'qixin', 'aiqicha'])
    
    score += 1.5 if has_t0 else 0
    score += 2 if has_t1 else 0
    score += 1.5 if has_t2 else 0
    details.append(f"  sameAs tiers: T0(gov)={has_t0}, T1(media)={has_t1}, T2(business)={has_t2}")
    
    # 4.3 Review Schema (4 pts)
    cases_url = urljoin(base_url, '/cases')
    status, html = fetch(cases_url)
    blocks = extract_jsonld_blocks(html)
    has_review = 'Review' in get_schema_types(blocks)
    score += 2 if has_review else 0
    details.append(f"  {'✅' if has_review else '❌'} Review Schema on /cases")
    
    # Check comparison table (thead)
    has_thead = '<thead' in html.lower() if status == 200 else False
    # Also check about page
    status_about, html_about = fetch(about_url)
    has_thead = has_thead or '<thead' in html_about.lower()
    score += 2 if has_thead else 0
    details.append(f"  {'✅' if has_thead else '❌'} Comparison table (thead) found")
    
    # 4.4 Email domain consistency (3 pts)
    # Check if email uses the same domain as the site
    domain = urlparse(base_url).netloc
    if status_about == 200:
        emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', html_about)
        email_domain_ok = any(domain in e for e in emails) if emails else False
        score += 3 if email_domain_ok else 0
        details.append(f"  {'✅' if email_domain_ok else '❌'} Email uses site domain ({domain})")
    else:
        details.append("  ❌ Cannot verify email domain (about page not accessible)")
    
    # 4.5 Business info consistency (3 pts)
    # Check if company name appears consistently
    if status_about == 200:
        # Look for company name in Schema
        for block in blocks:
            if block.get('@type') == 'Organization' and 'name' in block:
                company_name = block['name']
                name_in_footer = company_name in html_about
                score += 1.5 if name_in_footer else 0
                details.append(f"  {'✅' if name_in_footer else '❌'} Company name in Schema matches page content")
                break
    
    # Contact info consistency
    contact_url = urljoin(base_url, '/contact')
    status_contact, html_contact = fetch(contact_url)
    if status_contact == 200:
        contact_blocks = extract_jsonld_blocks(html_contact)
        for block in contact_blocks:
            if block.get('@type') == 'Organization' and 'email' in block:
                score += 1.5
                details.append(f"  ✅ Contact page Organization Schema has email")
                break
        else:
            details.append(f"  ❌ Contact page Organization Schema missing email")
    else:
        details.append(f"  ❌ Contact page not accessible")
    
    return score, details


def audit_dimension_5(base_url, sitemap_urls):
    """Domain Consistency (20 pts)."""
    score = 0
    details = []
    domain = urlparse(base_url).netloc
    
    # 5.1 Canonical (4 pts)
    status, html = fetch(base_url)
    has_canonical = 'rel="canonical"' in html or "rel='canonical'" in html
    canonical_primary = False
    if has_canonical:
        canonical_match = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', html, re.IGNORECASE)
        if canonical_match:
            canonical_url = canonical_match.group(1)
            canonical_primary = domain in canonical_url
    
    score += 2 if has_canonical else 0
    score += 2 if canonical_primary else 0
    details.append(f"  {'✅' if has_canonical else '❌'} Canonical tag present")
    details.append(f"  {'✅' if canonical_primary else '❌'} Canonical points to primary domain")
    
    # 5.2 Sitemap self-report (4 pts)
    sitemap_urls_list = sitemap_urls
    all_primary = all(domain in url for url in sitemap_urls_list)
    score += 2 if all_primary else 0
    details.append(f"  {'✅' if all_primary else '❌'} All sitemap URLs use primary domain")
    
    has_faq = any('/faq' in url for url in sitemap_urls_list)
    has_cases = any('/cases' in url for url in sitemap_urls_list)
    score += 1 if has_faq else 0
    score += 1 if has_cases else 0
    details.append(f"  Sitemap includes: /faq={has_faq}, /cases={has_cases}")
    
    # 5.3 llms.txt security (4 pts)
    status, content = fetch(urljoin(base_url, '/llms.txt'))
    if status == 200:
        has_admin = 'admin' in content.lower()
        score += 2 if not has_admin else 0
        details.append(f"  {'✅' if not has_admin else '❌'} llms.txt has no /admin links")
        
        has_brand_desc = any(kw in content for kw in ['品牌', '简介', 'brand', 'summary'])
        score += 2 if has_brand_desc else 0
        details.append(f"  {'✅' if has_brand_desc else '❌'} llms.txt has brand description")
    else:
        details.append("  ❌ llms.txt not accessible")
    
    # 5.4 Organization email in Schema (4 pts)
    blocks = extract_jsonld_blocks(html)
    org_has_email = False
    for block in blocks:
        if block.get('@type') == 'Organization' and 'email' in block:
            org_has_email = True
            score += 2
            # Check email domain matches site
            if domain in block['email']:
                score += 2
                details.append(f"  ✅ Organization Schema email matches site domain")
            else:
                details.append(f"  ❌ Organization Schema email domain mismatch")
            break
    if not org_has_email:
        details.append(f"  ❌ Organization Schema missing email field")
    
    # 5.5 All pages have JSON-LD (4 pts)
    pages_without_jsonld = 0
    for url in sitemap_urls[:15]:  # Check first 15
        status, html = fetch(url)
        if status == 200:
            blocks = extract_jsonld_blocks(html)
            if not blocks:
                pages_without_jsonld += 1
                details.append(f"  ❌ {url}: no JSON-LD found")
    
    score += 4 if pages_without_jsonld == 0 else 0
    details.append(f"  {'✅' if pages_without_jsonld == 0 else '❌'} All checked pages have JSON-LD")
    
    return score, details


def main():
    parser = argparse.ArgumentParser(description='GEO Website Audit Tool')
    parser.add_argument('--url', required=True, help='Base URL to audit (e.g., https://example.com)')
    parser.add_argument('--verbose', action='store_true', help='Show detailed output')
    args = parser.parse_args()
    
    base_url = args.url.rstrip('/')
    
    print(f"\n{'='*60}")
    print(f"  GEO Audit Report: {base_url}")
    print(f"{'='*60}\n")
    
    # Fetch sitemap
    print("Fetching sitemap...")
    sitemap_urls = fetch_sitemap_urls(base_url)
    print(f"Found {len(sitemap_urls)} URLs in sitemap\n")
    
    # Run 5 dimension audits
    total_score = 0
    
    dimensions = [
        ("1. Technical Reachability (15 pts)", audit_dimension_1),
        ("2. Structured Data (25 pts)", audit_dimension_2),
        ("3. Content Assets (20 pts)", audit_dimension_3),
        ("4. Trust Endorsement (20 pts)", audit_dimension_4),
        ("5. Domain Consistency (20 pts)", audit_dimension_5),
    ]
    
    for title, audit_fn in dimensions:
        print(f"--- {title} ---")
        score, details = audit_fn(base_url, sitemap_urls)
        total_score += score
        print(f"  Score: {score:.1f} pts")
        if args.verbose:
            for detail in details:
                print(detail)
        print()
    
    print(f"{'='*60}")
    print(f"  TOTAL SCORE: {total_score:.1f} / 100")
    
    if total_score >= 90:
        print(f"  Rating: ✅ Excellent")
    elif total_score >= 80:
        print(f"  Rating: ✅ Good")
    elif total_score >= 70:
        print(f"  Rating: ⚠️ Needs Work")
    else:
        print(f"  Rating: ❌ Critical")
    
    print(f"{'='*60}\n")
    
    return 0 if total_score >= 80 else 1


if __name__ == '__main__':
    sys.exit(main())
