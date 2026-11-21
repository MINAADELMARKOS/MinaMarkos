# Homepage positioning redesign

## Audit and design decisions

The old homepage gave visitors a name and role, but no clear value proposition or project action in the hero. Large banner decoration competed with the introduction; portrait markup was duplicated; the long career timeline preceded project evidence. Mobile branding consumed 80% of the navigation width and forced the toggle onto another row. Legacy scroll handlers changed fixed-header behavior unnecessarily.

The redesign retains the existing violet/navy palette, professional logo, portrait and GitHub Pages architecture. It introduces no framework or external font dependency.

- Hero: Mina Adel Markos; **Senior Data Engineer | Enterprise Data Platforms & AI Architecture**; a concise, credible value proposition; one responsive WebP portrait; Explore My Projects, Download CV and Connect on LinkedIn actions.
- Six compact expertise areas immediately support the positioning.
- Engineering Value explains reliability, complexity, decisions, modernization and trusted AI as engineering objectives and approaches, not quantified achievements.
- Projects and engineering articles appear before the detailed biography and experience. Existing professional, project, certification and contact records are retained.
- Native sticky navigation replaces the old fixed-header scroll handler. Mobile toggle, Escape handling, close-on-link behavior and responsive reset are keyboard accessible. Navigation remains usable without JavaScript.

## Scope and source

`index.html` contains the revised hero, navigation, expertise/value sections and section order. `css/homepage-executive.css` holds the overrides; `tools/build_home_assets.cjs` includes them in the actual production `css/homepage.min.css`. Use `node tools/build_home_assets.cjs --css-only`; no blog, portrait or certificate rebuild is needed. `js/homepage.js` keeps native navigation and existing project filters.

Existing image files, identity metadata, Search Console verification token, career information, project descriptions, article URLs and certification section are retained. Some malformed legacy image attribute separators were corrected without changing their values. No future Solution Architect/Principal role is presented as a current job, and no numerical outcomes or new qualifications were invented.

The Download CV action uses Google's download endpoint with the same file ID as the existing CV link. It opens externally with secure attributes; the accessible HTML CV remains available through “View web CV.” Actual external download permissions and public availability require remote validation and are not inferred from the URL format.

## Verification

Run a local server, then:

```bash
HUB_BASE_URL=http://127.0.0.1:8011/ node tools/check_executive_homepage.cjs
python3 tools/validate_learning_hub.py
node --check js/homepage.js
```

Responsive browser checks cover 375, 768, 1024 and 1440px: one H1, all three CTAs, six expertise areas, five value areas, no horizontal overflow, loaded portrait with preserved proportions, desktop navigation on one row, mobile toggle on the brand row, keyboard open/Escape/close, project filters, no page errors/missing local assets, and no-JavaScript navigation. Regression assertions preserve the existing project, biography, experience, tools, articles, certification and contact sections, apart from correcting malformed image separators. The verification token is unchanged.

`accessibility.json` contains axe results scoped to the redesigned hero, expertise, Engineering Value and header. This is automated local coverage, not an accessibility conformance certification. Existing lower-page components are not represented as newly audited or repaired.

## Screenshots

- [Desktop before](screenshots/before-1440.png) / [Desktop after](screenshots/after-1440.png)
- [Mobile before](screenshots/before-375.png) / [Mobile after](screenshots/after-375.png)

Screenshots show the first viewport, including the introduction and the start of supporting content. They are local browser captures, not production screenshots.

## Deployment boundary

Target: `https://minaadelmarkos.github.io/MinaMarkos/`. The environment still blocks this host with network-policy HTTP 403 responses. The user-approved host additions were saved in the environment draft during the preceding task, but that did not activate them in this running instance. The GitHub Pages API and public CV/LinkedIn availability therefore remain unverified. A push is not evidence of a successful Pages build or reflected public content. Apply the saved network settings, then verify the deployed headline, hero actions, CSS and mobile navigation before marking deployment complete.
