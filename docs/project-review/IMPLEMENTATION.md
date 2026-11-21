# Engineering portfolio implementation

## Delivered

- Eleven project cards: all ten original projects plus the Databricks SQL project in the supplied CV. Each card includes category, business problem, solution, stack, evidence-bounded development status, source links and a case-study action.
- Eleven dedicated case-study pages, each with the ten requested sections. Source-reviewed flow diagrams use semantic HTML/CSS so they remain readable on phones without a diagram library. Cases with insufficient evidence say which components are unknown instead of fabricating a production topology.
- Evidence-first prioritization: InvestiNator and VerdaTrace co-lead the weighted assessment; DataGuard-AI follows. Numeric rubric values are explicitly editorial judgments, not project performance data. See `INVENTORY_AND_RANKING.md`.
- All original project source and related article links remain in the homepage. GitHub repositories are not invented for document-only projects. Only the repository-documented InvestiNator preview is linked as a preview, explicitly synthetic. Its alternate CV-listed preview is retained in the case study with an unverified-availability label.
- The supplied CV is served locally and linked from both homepage and CV summary. The web summary follows its current location, selected experience dates, training and education. Existing certifications are not upgraded or added based on a CV line alone.

## Sources and maintenance

`content/project_cases.py` contains the authored content. `content/project-review-revisions.json` records the reviewed repository commits; `content/projects.json` is the generated inventory. Review new source revisions before updating these evidence snapshots. `content/project-original-links.json` captures the original ten cards and their source/article links.

Run `python3 tools/build_project_portfolio.py` to regenerate project cards, cases, inventory and sitemap. It uses committed review snapshots rather than requiring network access or cloned repositories for normal regeneration. `css/project-portfolio.css` is used directly by cases and included in the homepage's existing production bundle. Rebuild that bundle with `node tools/build_home_assets.cjs --css-only`. Run `python3 tools/build_professional_pages.py` for the current HTML CV summary. No framework or website runtime dependency was added.

The original project screenshot files are retained; a Databricks dashboard screenshot from the reviewed repository is added. Screenshots are evidence artifacts and are never labeled as new live runs. The original PDF is retained byte-for-byte; its SHA-256 is in `cv-sha256.txt`.

## Verification

- Featured repositories: InvestiNator 12 tests passed; VerdaTrace 83 passed / 1 explicitly skipped; DataGuard 2 passed. VerdaTrace frontend utility tests passed. DataGuard local health/dashboard/alerts HTTP payloads passed assertions.
- Responsive browser tests at 375, 768, 1024 and 1440px: filters, all case-study actions, loaded images, keyboard focus, readable featured cases, navigation and no horizontal overflow.
- All eleven pages have the ten requested sections, meaningful H1, canonical/social metadata, JSON-LD and sitemap entries. The source crawl covered 37 HTML pages with zero broken local references or JSON-LD parse errors.
- Homepage regression checks and the existing library validation passed. The supplied PDF returned HTTP 200 locally with a PDF signature. Source equality proves the original project links remain.
- Browser checks found no page errors or missing local assets. JavaScript-disabled visitors can still read all cards and cases.

Commands: `node tools/check_project_portfolio.cjs`, `HUB_BASE_URL=http://127.0.0.1:8012/ node tools/check_executive_homepage.cjs`, `python3 tools/validate_learning_hub.py`, and `python3 tools/audit_seo.py`. See `VALIDATION.md` for scope and unexecuted deployment/security/performance checks.

[Desktop project view](screenshots/projects-1440.png) · [Mobile project view](screenshots/projects-375.png)

## Publication and remaining evidence

The existing Pages publication path is retained. Public HTTPS, preview behavior and Pages build status require access to `minaadelmarkos.github.io` and `api.github.com`; prior approved domain additions were saved but were not active in the running environment at review time. Git repository access works. A push alone is not deployment confirmation.

Live cloud operation, production security, model quality, latency/throughput improvements, incident-time reductions and financial outcomes are not established by these local checks. Document-only projects need source packages, metric definitions and reproducible instructions before stronger implementation claims. The banking prototype needs its legacy runtime/configuration/model dependencies resolved. The Java feature branch in InvestiNator is not treated as a released production implementation.
