# Search visibility baseline — 17 November 2026

## Measurement status

No authenticated user Search Console, Bing Webmaster or analytics connection is available. No impressions, organic clicks, CTR, indexed-page count, query positions, branded/non-branded query totals, engagement or conversion counts were obtained. These values are **unavailable, not zero**. A generic runtime Google credential binding does not establish authorization to the user's Search Console property and was not repurposed.

Source inspection found 23 intended indexable pages before this task; the new HTML CV makes 24. This is a source inventory, **not an indexed-page count**. Local Lighthouse scores are not search-ranking measurements. See `measurements/source-before.json` and `lighthouse-before.json` for actual baseline evidence.

## Reporting framework

| Metric | Definition / source | Cadence |
|---|---|---|
| Impressions, clicks | Search Console Web search, exact URL-prefix property, same countries/devices/date range | Weekly, trailing 28 days |
| CTR | Total clicks / total impressions; never average row CTRs | Weekly |
| Average position | Search Console impression-weighted position as defined by Google; not an absolute rank guarantee | Weekly |
| Indexed pages | Search Console Page Indexing + sampled URL Inspection; Bing separately | Monthly |
| Branded queries | Case-insensitive query variants of Mina Adel Markos, Mina Markos, MINAADELMARKOS; retain the classification rule/version | Weekly |
| Non-branded queries | Remaining disclosed queries; anonymized query omissions mean query totals may not reconcile to page totals | Weekly |
| Blog engagement | Consented article page views and 50%/90% scroll events; scroll is not proof of comprehension | Weekly |
| Project engagement | `professional_interaction` with type `project`; count clicks, not distinct qualified people | Weekly |
| CV interactions | Type `cv` or `cv-original`; distinguish HTML page navigation from original-file opens | Weekly |
| Contact interactions | Type `contact`; intent click, not a delivered message or hiring conversion | Weekly |

`js/engagement.js` emits local `portfolio:engagement` CustomEvents only when `window.PORTFOLIO_MEASUREMENT_CONSENT === true`. No analytics provider, network collection, cookies, storage, personal identifiers, email addresses, external URLs or search terms are sent by this code. Default is disabled. Configure an approved collector and consent flow before reporting these events as collected data; set consent before loading the script. Deduplicate events at the collector if necessary. Page paths alone are emitted with event type and optional interaction category or scroll percentage.

## Follow-up

Export the first complete 28-day period after deployment; compare with the immediately preceding complete 28-day period using identical property, search type, time zone, dimensions and filters. Annotate publication, content and measurement changes. Keep field Core Web Vitals and local lab metrics separate. Use contact quality and relevant opportunities as business outcomes; do not infer professional qualification from a page view.

## Webmaster operations pending access

- Preserve the existing Google HTML verification token; verification does not itself prove indexing.
- Use a URL-prefix property for `https://minaadelmarkos.github.io/MinaMarkos/`; do not claim ownership of the shared `github.io` hostname.
- After public HTTPS validation, submit `sitemap.xml` in authorized Search Console and Bing Webmaster accounts. Neither submission was performed.
- IndexNow can support an explicitly scoped key location, but requires a publicly reachable ownership key and verified scope. No key, ownership claim or submission was created in this task. Do not deploy a root-host key or claim other GitHub Pages users' URLs.
- GitHub profile README already links to the official portfolio and relevant articles (read-only public inspection). LinkedIn editing/verification and other project README updates require the corresponding account/repository workflow; no external profiles were modified.
