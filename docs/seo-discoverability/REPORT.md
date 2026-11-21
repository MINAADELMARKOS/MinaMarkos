# Technical SEO and discoverability audit — 22 November 2026

This change improves evidence-linked discovery of Mina Adel Markos's engineering work while preserving the established identity, design, verified credential links and GitHub Pages architecture. It does not claim rankings, indexing or AI recommendations.

## Audit and priorities

| Priority | Finding | Resolution / boundary |
| --- | --- | --- |
| P1 | Case-study JSON-LD identified the page, but not its authored technical content. | Added a connected CreativeWork for each of 11 engineering case studies, with author, abstract, project implementation status, actual screenshot and reviewed-revision citation where available. The work represents the written case study, not a claim of sole authorship or production readiness of the underlying system. |
| P1 | Tutorials and project evidence were weakly connected. | Added eight editorially selected article/case-study pairs with links in both directions; added explicit linked case-study author attribution. The homepage generator now also emits its three intended technical-explanation links and VerdaTrace's existing public sample portal. |
| P1 | The homepage project generator matched obsolete markup and silently failed to update cards. | Match the actual section ID and require exactly one replacement. All 11 project previews now carry measured intrinsic dimensions. The resulting descriptions and deduplicated links agree with the existing source-reviewed project data. |
| P1 | Production CSS discarded the early mobile-navigation guard, causing a lab-observed layout shift. | Added the runtime `js` class to the CSS safelist and terminated a custom property in source CSS to avoid the minifier's comment-parsing failure. Build now fails on minifier warnings or missing navigation guard. Rebuilt the served hashed bundle and alias. |
| P2 | Project previews reused the portrait in Open Graph/Twitter metadata. | Use each project's existing screenshot with encoded URLs, meaningful alt text, large-image Twitter cards and measured Open Graph dimensions. All 35 canonical pages now expose measured social-image dimensions. No synthetic artwork or new achievement claims. |
| P2 | A legacy CV-listed InvestiNator preview URL returns HTTP 404. | Removed that obsolete action from the generated case study; preserved the working synthetic demo and source links. The original supplied PDF is unchanged and still contains its historical URL. No redirect was added in another repository. |
| P2 | GitHub's profile website field is empty; full name differs from the established alias. | Documented the exact optional profile update in the measurement plan; retained both verified name forms in Person data. No external account settings were changed. |
| P2 | Search/traffic measurements and webmaster account access are unavailable. | Added explicit KPI definitions, baseline status, follow-up windows and account-side verification/submission steps. No baseline numbers or verification tokens invented. |

## Correct existing implementations preserved

- 35 distinct canonical pages: homepage, blog, CV, 21 articles and 11 case studies. All have one H1, unique titles and descriptions, self-consistent Open Graph URLs, and index/follow source directives. Topics are expressed naturally in existing titles, biography, expertise and article text; no keyword lists were inserted into visible prose.
- Connected Person, WebSite, ProfilePage, Blog, BlogPosting and BreadcrumbList data already use the exact professional name, Senior Data Engineer role, established GitHub/LinkedIn URLs and consistent entity IDs. These were retained. Article publication dates remain 17 November 2026; only the eight articles with new contextual links show the actual 22 November modification date in both visible text and JSON-LD.
- All canonical content, project status boundaries, architecture explanations and author information are server-rendered static HTML and readable without JavaScript. No framework, crawler-specific content, rating/review markup, fabricated metrics or AI-discovery promises were added.
- `sitemap.xml` already contains exactly the 35 canonical HTTPS URLs, with no duplicate, query, fragment or excluded template entries. Its bytes did not need changing. `/index.html` consolidates through its root canonical; blog category query controls use the blog canonical.
- The two inherited example templates remain `noindex` and absent from the sitemap. Canonicalization and noindex handle alternate/legacy pages without deleting working routes.
- Existing Google verification token is unchanged (SHA-256 comparison). Certification links, uploaded CV bytes, optimized responsive portraits, lazy-loaded supporting images, static navigation and content filenames remain intact.

## Crawl configuration and public checks

The project-level `https://minaadelmarkos.github.io/MinaMarkos/robots.txt` returns HTTP 200 and points to the correct sitemap. Crawlers consult **origin-root** `https://minaadelmarkos.github.io/robots.txt`, which currently returns HTTP 404. This is not a robots exclusion; the project subdirectory file does not provide host-wide crawler policy. No root-host file was fabricated or deployed from this project repository. Sitemap discovery can be supplied through authorized webmaster tools; a root robots file would require the separate origin-root site workflow if wanted.

Public HTTPS checks before changes returned 200 for all 81 sampled site resources. Core outbound checks returned 200 for GitHub, six Credly destinations and both current project demos. The two LinkedIn destinations could not be retrieved (curl exit 56, no HTTP status); this does not establish broken profiles. Credly HTTP reachability does not independently revalidate credential ownership. The only confirmed 404 in the sampled outbound set was the legacy InvestiNator preview described above. External documentation/evidence URLs were not exhaustively live-crawled; all local references and fragments were checked.

## Validation evidence

- `source-before.json` and `source-after.json`: 37 HTML pages audited, 35 indexable in source, zero broken local references. Homepage images lacking intrinsic dimensions fell from 11 to zero; other indexable pages already had dimensions. Titles/descriptions were already unique and were preserved.
- `python3 tools/validate_discoverability.py`: exact sitemap/canonical coverage, connected identity, case-study authors/status/citations, social image files/dimensions, heading progression, reciprocal links and verification-token preservation.
- `python3 tools/validate_learning_hub.py`: all 22 learning-hub pages pass, including original prose, links/fragments, schema, headings, sitemap and distribution-draft preservation.
- `browser-checks.json`: all 35 canonical pages tested at 375, 768, 1024 and 1440px without JavaScript; no horizontal overflow. Four representative templates pass automated WCAG-tagged Axe checks with no violations. Keyboard article→case-study and author→biography links work. A deliberately delayed navigation controller verifies stable first-paint layout. Automated checks are not a complete accessibility certification.
- `../measurements/lighthouse-discoverability-final.json`: local mobile Lighthouse 13.0.3 snapshots for home, InvestiNator and Kafka troubleshooting. SEO, Accessibility and Best Practices score 100 on all three; Performance scores 95/100/100, CLS 0 on all three. These are local single-run lab snapshots, not field Core Web Vitals or search-ranking data. The earlier diagnostic report retains the homepage CLS 0.237 finding before the production-CSS correction; it is not an old-live-versus-new performance benchmark. No claim of statistically measured speed improvement is made.
- JSON-LD syntax and local semantic references were validated. No authenticated Google Rich Results Test or Search Console validation was performed; a supported Schema.org type does not guarantee a Google rich-result feature.

## Changed files and reproducibility

Shared metadata: `tools/seo_metadata.py`; editorial link source: `content/discovery-links.json`; page generators: `tools/build_learning_hub.py`, `tools/build_project_portfolio.py`; image/build pipeline: `tools/update_image_dimensions.cjs`, `tools/build_home_assets.cjs`; source CSS: `css/design-system.css`; served CSS: `css/homepage.min.css` and `css/homepage.f73c1cc2bde4.min.css`. Generated HTML: homepage, blog, CV, 21 articles and 11 case studies. Supporting manifests: `content/article-index.json`, `content/image-dimensions.json`, `content/homepage-assets.json`. New validation tools and this audit directory contain the evidence and measurement plan. Previously published hashed assets remain available to cached HTML.

```sh
node tools/update_image_dimensions.cjs
python3 tools/build_project_portfolio.py
python3 tools/build_learning_hub.py
python3 tools/build_professional_pages.py
node tools/build_home_assets.cjs --css-only
python3 tools/audit_seo.py --output docs/seo-discoverability/source-after.json
python3 tools/validate_discoverability.py
python3 tools/validate_learning_hub.py
# Serve the repository at localhost:8014, then:
node tools/check_discoverability.cjs
# After the matching main commit has a successful GitHub Pages build:
python3 tools/verify_public_discoverability.py --compare --output /tmp/portfolio-public-deployment.json
```

Public site: https://minaadelmarkos.github.io/MinaMarkos/ . Publication requires a successful Pages build and exact-source public HTTP verification, not only a commit. See the deployment record added after validation. Search account tasks and unmeasured KPIs are detailed in [MEASUREMENT_PLAN.md](MEASUREMENT_PLAN.md).
