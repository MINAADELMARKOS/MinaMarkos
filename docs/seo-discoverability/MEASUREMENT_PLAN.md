# Search visibility measurement plan — 22 November 2026

No authorized Search Console, Bing Webmaster Tools or analytics dataset was available in this session. Every search/traffic baseline below is **unavailable, not zero**. Source eligibility and successful HTTP responses do not establish indexing, rankings or AI citations. Existing consent-gated events in `js/engagement.js` remain disabled by default; they are not an installed analytics service.

| KPI | Baseline | Follow-up definition / source |
| --- | --- | --- |
| Indexed pages | Unavailable | Search Console Page Indexing; inspect home, blog, an article and a case study; compare submitted sitemap URLs with indexed canonical URLs. Report Bing separately. |
| Organic impressions | Unavailable | Search Console Web search impressions for the exact URL-prefix property; Bing separately. |
| Search clicks | Unavailable | Same property, search type and complete date range as impressions. |
| Search CTR | Unavailable | Total clicks divided by total impressions; do not average row percentages. |
| Brand-name visibility | Unavailable | Branded impressions, clicks, CTR and disclosed queries matching case-insensitive `Mina Adel Markos`, `Mina Markos` or `MINAADELMARKOS`. Keep the classification rule fixed. |
| Non-branded visibility | Unavailable | Remaining disclosed queries, grouped by engineering topic (Spark, Kafka, Cloudera, enterprise/cloud data platforms and AI architecture). Query anonymization prevents exact reconciliation with overall totals. |
| Organic portfolio visits | Unavailable | Consented analytics sessions attributed to organic search, filtered to `/MinaMarkos/`. Define a session and bot/internal-traffic filters with the selected provider before collecting. |
| Project page traffic | Unavailable | Organic-search sessions and views with landing/page path `/MinaMarkos/projects/*.html`; separate views from homepage-to-project clicks. |

Record the deployment date and commit. Once access is configured, export the immediately preceding complete 28 days as the historical baseline (if retained), then compare with the first complete 28 days after deployment. Use matching property, time zone, search type, devices, country filters and channel definitions. Review weekly on a rolling 28-day window; review indexing monthly. Annotate new publications, analytics setup and taxonomy changes. Keep pre-existing records in `docs/SEARCH_VISIBILITY_BASELINE.md` as historical snapshots, not the current page inventory.

Search Console page/query CSVs and the selected analytics export should be retained with export date, filters and metric definitions. Average position is an impression-based Search Console metric, not a guaranteed rank. Track qualified professional enquiries separately from CV/contact clicks; a click is not a delivered enquiry.

## Account-side actions

1. In your authorized Google Search Console account, add or select the **URL-prefix** property `https://minaadelmarkos.github.io/MinaMarkos/`. Preserve and use the existing homepage HTML verification token. Do not create a Domain property claiming ownership of all `github.io`.
2. Submit `https://minaadelmarkos.github.io/MinaMarkos/sitemap.xml`. Inspect the canonical homepage, blog, one article and one case study; check Google's selected canonical and indexing exclusions. Request indexing only where appropriate. A successful submission is not proof of indexing.
3. In your Bing Webmaster Tools account, import the verified property or complete Bing's offered verification method. Submit the same sitemap and review Site Explorer / URL Inspection. No Bing verification token was invented or deployed.
4. If analytics measurement is wanted, choose an approved provider, implement its required consent configuration and validate collection before reporting traffic. The existing local CustomEvents alone collect no server-side data.
5. In GitHub profile settings, optionally set Name to `Mina Adel Markos` and Website to `https://minaadelmarkos.github.io/MinaMarkos/`. The public API currently reports Name `Mina Markos` and an empty Website field. The alias is already represented in Person schema. Confirm LinkedIn displays the same professional name, current headline and portfolio URL using your signed-in account; its established URL was preserved, but could not be retrieved here.

No account verification, sitemap submission, external-profile edit or analytics collection was performed. These steps require the corresponding account access; implementation and public deployment do not require waiting for them.
