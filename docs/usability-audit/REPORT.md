# Portfolio usability, accessibility and performance report

The existing professional identity, portrait, career history, project evidence, CV PDF, credential records and working URLs are retained. Improvements apply a shared visual layer to the homepage, library, CV and all generated case-study/article pages.

## Measured Lighthouse comparison

| Mobile lab page | Performance | Accessibility | Best Practices | SEO |
|---|---:|---:|---:|---:|
| / | 77 → 94 | 96 → 100 | 100 → 100 | 100 → 100 |
| blog.html | 100 → 100 | 100 → 100 | 100 → 100 | 100 → 100 |
| projects/investinator.html | 100 → 100 | 100 → 100 | 96 → 100 | 100 → 100 |
| cv.html | 100 → 100 | 100 → 100 | 100 → 100 | 100 → 100 |

Homepage FCP: 2.7s → 1.7s. LCP: 5.0s → 2.9s. TBT: 0ms → 0ms. CLS: 0 → 0. The final LCP is improved but still above the 2.5s “good” threshold.

Measurements used Lighthouse 13.0.3 with Chromium and its mobile simulated-throttling preset against a local HTTP server. One completed run per URL before/after; browser/CPU variability and local-server behavior limit inference. These are not field Core Web Vitals or statistically established user-experience gains. Configuration, exact timing, warnings and failed audits are retained in `../measurements/lighthouse-ux-before.json` and `lighthouse-ux-after.json`. Initial diagnostic reruns exposed footer-contrast and menu-layout regressions; those were corrected before the final after run.

## Visual system

`css/design-system.css` defines reusable palette, type, spacing, border, radius, shadow and focus tokens, with aliases for the existing library theme. Important pages use the `portfolio-ui` class; homepage-specific changes are scoped to `portfolio-home`.

| Token family | Values / intent |
|---|---|
| Identity | Navy ink #16253D; violet brand #6247CE; accessible link #4E3AA7; body text #526176 |
| Surfaces | White and #F7F8FC neutral sections; #DFE5EF borders |
| Spacing | 4, 8, 12, 16, 24, 32, 48, 64px scale |
| Shape | 14px cards; 7px controls; restrained shared shadows |
| Type | System font stack; normal-case headings; consistent readable line heights |
| Focus | 3px #2846A1 outlines and offset; light focus color inside code panels |

Cards, controls, section transitions, experience typography and footer/contact areas now share these values. Existing company logos were neither recolored nor modified.

## Navigation and accessibility

- All required destinations are in the main navigation: Home, About, Experience, Projects, Engineering Blog, Certifications and Contact.
- The obsolete HTML `hidden` toggle and Bootstrap data attributes were removed. CSS shows the toggle on small screens with JavaScript enabled; JavaScript-free visitors retain the visible link list.
- Open/Close accessible labels and aria-expanded stay synchronized. Escape returns focus, link selection closes the menu, resize resets disclosure state, and outside pointer interaction dismisses it.
- Hash navigation transfers keyboard focus to the destination heading. Sticky-header offsets keep targets usable; menus scroll inside short viewports.
- An early JS capability marker establishes the collapsed mobile layout before first paint, avoiding the expanded-then-collapsed CLS regression. If the homepage script cannot load, its error handler removes that marker so navigation remains visible.
- Former blue links failed 4.5:1 text contrast. Shared accessible link colors and distinct dark-footer colors resolve that issue without making buttons unreadable.
- Decorative icons are hidden from assistive technology; visible text/labels remain. Skip links have focusable main targets. The article discussion uses a section instead of an incorrectly nested complementary landmark.
- Case-study pages now declare a favicon; lazy project/case images reserve their intrinsic dimensions. Inspection found no remaining malformed image attribute separators in the active pages.

Axe checks passed with **zero detected violations** for the homepage plus blog, a case study, CV and a long tutorial at 375, 768, 1024 and 1440px (20 page/viewport combinations). Keyboard menu, focus, project-filter, reflow, short-height disclosure and no-JS checks passed. Results: `axe-before.json` and `axe-after.json`. Existing homepage/project regression tests and library/source-link validation also passed.

The target is WCAG 2.2 AA where applicable. Automated scores and this manual keyboard/reflow coverage are not a full WCAG conformance certification; no screen-reader/user research or exhaustive assistive-technology matrix was performed. Code and two-dimensional diagrams may retain contained scroll areas; no horizontal page scrolling occurred at the tested widths.

## Asset delivery and caching

The homepage CSS decreased from **251,911 bytes to 46,292 bytes** (about 82%). PurgeCSS removes unused legacy rules from the homepage build, followed by minification. Responsive/interactive selectors (`show`, `active`, readiness classes and project categories) are retained and exercised by browser tests. Full component sources remain available to other pages.

The homepage serves `css/homepage.18a2057a275a.min.css` and `js/homepage.1cc2a958bddf.js`. `content/homepage-assets.json` records their hashes and source inputs. Stable `homepage.min.css` and `homepage.js` aliases remain; the build emits content-addressed copies and updates only the homepage references. CSS and JS bytes match their recorded hashes, and repeated builds produce identical references.

GitHub Pages was observed returning `Cache-Control: max-age=600` and ETag for the existing CSS. Hosting cache/compression policies were not changed or invented. Content-addressed URLs prevent changed homepage assets from reusing stale browser entries while unchanged versions can remain cached. No unsupported `_headers` or server configuration was added.

The existing responsive WebP portrait, below-fold lazy loading and deferred scripts remain. System fonts require no external font service; retained icon fonts now use font-display: swap. Explicit image dimensions reduce unreserved image space. The deferred homepage script remains dependency-free; PurgeCSS is build-time tooling, not a site runtime framework.

## Reproduce

```bash
npm ci --prefix tools
node tools/update_image_dimensions.cjs
python3 tools/build_learning_hub.py
python3 tools/build_project_portfolio.py
python3 tools/build_professional_pages.py
node tools/build_home_assets.cjs --css-only
python3 tools/validate_learning_hub.py
python3 tools/audit_seo.py
python3 -m http.server 8013 --bind 127.0.0.1
# In another terminal:
node tools/check_usability.cjs
HUB_BASE_URL=http://127.0.0.1:8013/ node tools/check_executive_homepage.cjs
HUB_BASE_URL=http://127.0.0.1:8013/ node tools/check_project_portfolio.cjs
python3 tools/measure_seo.py --phase ux-after --base-url http://127.0.0.1:8013/ --lighthouse tools/node_modules/lighthouse/cli/index.js --paths "" blog.html projects/investinator.html cv.html
```

Run generators before the homepage asset build so the purge inventory reflects the final HTML. Fingerprinted assets are deployment artifacts; retain previously published versions for cached pages. The original Pages branch/root publication architecture remains unchanged.

## Screenshots

[Desktop before](screenshots/before-1440.png) / [Desktop after](screenshots/after-1440.png) · [Mobile before](screenshots/before-375.png) / [Mobile after](screenshots/after-375.png) · [Expanded mobile navigation](screenshots/mobile-navigation.png)

Screenshots and Lighthouse results are local-browser evidence. Publication is verified separately against the Pages build and public HTTPS assets in the final handoff.
