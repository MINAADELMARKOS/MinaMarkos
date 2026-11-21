# Issuer-logo certification section

The redesign changes only `#Certificate`, its scoped CSS, the generated homepage stylesheet, and relevant build/test documentation. The seven original certificate records and credential URLs are retained. No original SVG artwork or brand-image files were changed or deleted.

## Published record order

1. Google Cloud Certified — Generative AI Leader
2. Cloudera Data Engineer Professional Certificate
3. SI Architect Certification
4. Associate Cloud Engineer Certification
5. Cloudera Data Analyst Professional Certificate
6. Google Business Intelligence Certificate
7. Data Analytics Professional - Vodafone Business

Databricks belongs in position 2 of the requested eight-card sequence, but is **not published**. Its exact supplied title, issuer, description and existing logo path are retained in `content/certification-drafts.json`. Supply the verified earned credential URL before publishing it. No credential ID, date or URL was invented.

## Assets and evidence

| Issuer | Asset/status | Inspection |
|---|---|---|
| Google Cloud | `img/brands/google-cloud.png` | Existing 600 × 600 PNG, transparent multicolor Cloud mark; adequate at 84px display height |
| Cloudera | `img/brands/Cloudera_Logo.png` | Existing 2363 × 647 image, orange company wordmark; actual file format is JPEG despite filename; left unchanged |
| Vodafone Business | `img/vodafone-logo.png` | Existing 2400 × 2400 PNG with Vodafone company symbol/wordmark; used without alteration |
| Databricks | `img/brands/Databricks_Logo.png` | Existing 1122 × 629 transparent PNG company mark; inspected but not published in the earned-credential section |
| Google | Plain neutral text fallback | Official Google-hosted wordmark download returned HTTP 403; do not substitute the Google Cloud mark for Google |
| SI Architect | Plain neutral text fallback | No issuer established in the existing record; Credly request blocked; do not guess a Cloudera or other issuer |

Existing logos were visually inspected and are recognizable company marks, not partner or certification badges. Their original acquisition/license provenance and current brand policies could not be independently revalidated while issuer sites are blocked. Assets remain unchanged: no recoloring, cropping, distortion, tracing or AI-generated logos. Neutral white panels provide clear space. A section note identifies logos as issuer identity only, without employment, sponsorship or endorsement.

The Google text label is not presented as an authentic Google wordmark. It is a temporary limitation until an authorized official asset is accessible. The SI issuer must be confirmed before selecting a logo. Existing Google Cloud Associate links use a Credly earner route and the Cloudera Data Analyst link is a LinkedIn post; both are preserved as requested, but their public credential-verification suitability remains to be checked.

## Design and integration

- Three columns from 1200px, two from 768px, one below 768px.
- Equal-height desktop/tablet cards with aligned buttons. Stacked mobile cards fit their content to avoid large empty areas.
- Consistent 120px white logo panels, 84px logo bounds, and `object-fit: contain` preserve logo proportions.
- Explicit issuer labels, unchanged titles/descriptions and existing verified-date information, consistent Verify Credential buttons, and secure external-link attributes.
- Visible keyboard outlines override the legacy theme's `outline: none !important`; focus outlines are immediate rather than animated.
- All selectors are scoped to `#Certificate`. The certification-only commit left homepage markup outside this section unchanged. The subsequent homepage redesign preserves this entire certification section byte-for-byte; its regression test now checks that boundary.
- `css/style.css` is the source; `css/homepage.min.css` is the served result. Run `node tools/build_home_assets.cjs --css-only` to regenerate CSS without rebuilding portraits, image inventories or blog pages.
- Historical SVG files and generator are retained. Their former integration tests now point to the current logo-card test; the archived SVG XML check remains available.

## Verification

Run `node tools/check_certificate_logos.cjs` against the local server (default port 8010, override with `HUB_BASE_URL`). Results are saved in `validation.json`.

Passed: 375/768/1024/1440px grid checks, equal heights where cards share rows, loaded local logos, contain fitting, no section overflow, keyboard tab sequence and visible focus, secure links, unchanged seven titles/descriptions/URLs, Databricks absent from rendered HTML, no local missing assets or browser page errors. CSS minification completed without errors; existing 22-page library markup/link validation and archived SVG XML validation also passed. This is local validation, not a W3C conformance certification.

Before/after screenshots:

- [Desktop before](screenshots/before-1440.png) / [Desktop after](screenshots/after-1440.png)
- [Mobile before](screenshots/before-375.png) / [Mobile after](screenshots/after-375.png)
- Additional after screenshots: [768px](screenshots/after-768.png), [1024px](screenshots/after-1024.png)

Screenshots hide the sticky header only in the capture; the live source is unchanged. Baseline captures use the HTML and CSS from commit `5ae0eed` without checking out or overwriting working files.

## Outstanding external checks

Google logo download, issuer confirmation, credential HTTP checks, Pages build status and deployed rendering remain blocked by the running environment's network policy. User approval for the five requested domains was received and the allowlist was saved in the environment draft. Runtime status still reports no added allowed hosts; saving that draft did not activate the policy. The user must apply the saved environment settings before those checks can succeed. No environment publication was performed.

Do not treat a Git push or these local tests as live-page verification. Public target: `https://minaadelmarkos.github.io/MinaMarkos/#Certificate`.
