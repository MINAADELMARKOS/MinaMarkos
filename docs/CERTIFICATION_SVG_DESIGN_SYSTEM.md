# Certification SVG design system

Archived artwork: current cards use issuer logos. See `certification-redesign/README.md` for the current integration and tests. The SVG files remain available and unchanged.

Seven original portfolio illustrations, created on `design/certification-svg-system`. They are technical illustrations, not issuer badges, certificate reproductions or examination evidence. All original asset filenames, card titles, descriptions, order and credential links are preserved. The unused IBM asset is outside this seven-card collection and was left unchanged.

## Principles and composition

- 640 × 640 vector canvas, 40px identity padding, 30px outer radius, consistent panels and footer.
- Category at y=51, issuer at y=93, two-line title at y=151/202, technical panel y=221–439, four compact themes in two rows, outcome at y=554, footer y=607.
- Arial, Helvetica, sans-serif; title 45px, issuer 29px, themes 25px. No downloaded fonts, embedded raster graphics, JavaScript, seals, signatures, identifiers or official logos.
- Shared ink `#16253D`, secondary `#526176`, background `#F8FAFC`, border `#E2E8F0`. Restrained blue/violet, blue/green, teal/deep blue, indigo/violet, red/slate and cyan/teal topic accents.
- Primary titles and technical silhouettes carry the visual meaning at card size. Secondary theme/footer text is supporting information; the HTML title, description and explicit custom-art note remain readable and authoritative.

## Illustration rationale and evidence

| Credential | Original technical motif | Evidence boundary |
|---|---|---|
| Generative AI Leader | Intelligence network → checked responsibility boundary → value chart | Supplied award details and art direction; AI fundamentals, cloud AI, output quality and responsible AI are illustrative themes |
| Associate Cloud Engineer | Cloud → connected compute, Kubernetes and storage | Existing card mentions GCP, Kubernetes, IAM, networking and infrastructure |
| Google Business Intelligence | KPI/goal panel and connected trend | Existing card supports dashboards, storytelling and business questions; themes illustrative |
| Cloudera Data Engineer | Ingestion → transformation → query → storage → analytics, with reliability check | Existing description supports Spark, Airflow and enterprise pipelines |
| SI Architect | Business services, integration, data and infrastructure layers with security boundary | Existing card supports solution design and enterprise architecture; issuer remains explicitly unconfirmed |
| Vodafone Business Analytics | Telecom signal connected to KPI/trend interface | Existing card supports business analytics and decisions; telecom motif is contextual, not a claimed exam objective |
| Cloudera Data Analyst | Distributed storage → SQL → aggregated insight | Existing description supports SQL and large-scale analysis |

Official-objective verification requests to Google Cloud and the SI Credly page received network-policy 403 responses. Credential links are unchanged, but their remote availability was not established. No theme is described as a verified examination objective. The SI issuer must be confirmed from the credential before replacing “Issuer unconfirmed.” No employer endorsement is implied.

Relevant sources for future confirmation: Google Cloud Generative AI Leader and Associate Cloud Engineer certification guides, Google's Business Intelligence program curriculum, and each card's original credential page. Exact card records are in `certification-records.json`; art-specific themes and issuer status are in `certification-art-manifest.json`.

## Accessibility and integration

Each SVG has a unique document-local title and description referenced by `aria-labelledby`, and contains only local gradient references. HTML alt text identifies each custom illustration. The section states that artwork is not an issued badge and themes are illustrative. System fonts and strong shape silhouettes prevent meaning from depending on color alone.

All images retain the existing `object-fit: contain` rules and original paths. Intrinsic dimensions are consistently 640 × 640; the existing card bounds and responsive grid are retained. No certificate component or page redesign was introduced by this art commit. Earlier SEO changes are a separate commit.

## Validation

- Generated and inspected `certification-contact-sheet.png` before updating HTML integration.
- Rendered all seven at 640 × 640, 320 × 320, and 210 × 190 contain bounds: 21 successful PNG renders in `/tmp/certification-renders/`.
- XML checks: viewBox, title/description IDs, gradient references, no external resources, no scripting, under 15 KB each.
- Browser checks: all SVG text bounding boxes inside the canvas; loaded square assets with contain fitting and no section overflow at 375, 768, 1024 and 1440px.
- Records regression check: all seven titles, descriptions, credential URLs, paths and order preserved.
- Public Pages rendering and credential HTTP availability remain blocked by environment network policy; local rendering is not a claim of deployed verification.

Reproduce with `python3 tools/build_certification_art.py`, `node tools/render_certification_art.cjs`, `python3 tools/validate_certification_art.py`, then serve the repository and run `HUB_BASE_URL=http://127.0.0.1:8004/ node tools/check_certification_art.cjs`.

## Adding a future credential

Confirm the record and issuer first. Add a single DATA entry to `build_certification_art.py` with two short title lines, topic accents, four supported or explicitly illustrative themes, a concise outcome and an original technical diagram. Reuse the canvas coordinates, typography and footer. Render the contact sheet, inspect reduced-size text, validate references and compare the full collection before integrating. Never synthesize official badge claims or fabricate credential identifiers.
