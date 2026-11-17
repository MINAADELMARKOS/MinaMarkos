# SEO audit — 17 November 2026

The audit inspected the checkout at `04ca162` and measured local HTTP pages with Lighthouse 13.0.3, Chromium, mobile simulated throttling. Search engines, Search Console, Bing data and the public Pages host could not be inspected through the current network policy. No indexed count or ranking is inferred.

## Baseline findings

- Homepage identity used the shorter name; its Person/WebSite/ProfilePage graph was disconnected from the articles' author objects.
- Blog and 21 article URLs already existed in the sitemap. The prompt's sitemap omission had been addressed by Task 2; it was not still a defect.
- No HTML CV page existed. CV buttons led to the existing Drive document.
- 14 broken local references occurred in two noindex legacy templates; important canonical pages had no broken local references.
- Homepage had 40 images, 39 without explicit dimensions, 22 empty alt attributes (some legitimately decorative), and 14 script requests including unused Maps and UI libraries.
- Homepage Lighthouse: performance 66, accessibility 83, best practices 96, SEO 100; FCP 3.8s, LCP 31.7s, TBT 0ms, CLS 0. About 9,003 KiB transferred. Blog and Spark performance tutorial scored 100 in all four categories.
- Google Fonts and Maps were blocked during the baseline. Lab results describe this environment, not public user experience. One run per URL is a directional lab comparison, not a statistically controlled experiment or field Core Web Vitals.

## Implemented remediation

Connected identity graphs, descriptive canonical metadata, HTML CV, explicit dimensions, responsive WebP portraits, below-fold lazy loading, reduced homepage scripts, minified local stylesheet, heading/contrast/accessible-link corrections, project-to-explanation links, and local consent-gated measurement hooks. Original sources and legacy vendor files are retained. Template navigation is repaired while templates remain noindex.

Robots at `/MinaMarkos/robots.txt` documents the project's intent but does not control crawler behavior: crawlers fetch `/robots.txt` at the origin root. This project does not claim control of that shared-host root. Page-level robots and canonical metadata remain the actionable controls here.

See machine-readable before/after source inventories and Lighthouse records in `measurements/`. Remaining unused CSS is reported rather than removed speculatively; the shared framework contains states needed by responsive components. Hosting compression/cache headers and field performance require public testing and hosting support.

No guarantee of indexing, ranking, AI-search citation, or qualified traffic is made. Clear crawlable content, identity and provenance improve understandability; they do not force a search engine to include it.
