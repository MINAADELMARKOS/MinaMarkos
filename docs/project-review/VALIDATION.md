# Project evidence and validation — 22 November 2026

Repository revisions, source paths, inventory, architectures and editorial rankings are recorded in `INVENTORY_AND_RANKING.md` and `content/projects.json`. The review cloned default branches read-only. It did not modify or deploy the project repositories.

## Executed local checks

| Project | Command / scope | Outcome |
|---|---|---|
| InvestiNator | Python `pytest -q`, reviewed main revision `06d036da2770` | **12 passed**. These exercise local backend behavior; not a Compose/Java/production connector or real-GPT evaluation. |
| VerdaTrace | Python `pytest -q`, revision `69a94cf0f9ba` | **83 passed, 1 skipped**. The external full data pack was unavailable, so its golden comparison did not run. |
| VerdaTrace frontend | `node --test tests/frontend_dataset_utils.test.js` | Passed; exact TAP results retained below. |
| DataGuard-AI | Python `pytest -q`, revision `d76cbf63295f` | **2 passed**. Feed/revenue-rule behavior, not revenue savings or production availability. |
| DataGuard API | Local health/dashboard/alerts HTTP requests | Healthy response, seeded dashboard structure and alert-count reconciliation verified. Synthetic clock/data; no real telecom feed. |

No cloud Terraform apply, real credentialed Airflow/Snowflake run, banking-model runtime, production incident action, Java feature-branch release, remote CI result, performance benchmark or financial uplift measurement was executed. CI workflow presence is reported separately from successful CI runs. Project-owned historical validation documents remain historical, author-reported evidence, not tests executed by this task.

## New CV

The supplied PDF is copied byte-for-byte to `assets/cv/Mina_Adel_Markos_Senior_Data_Engineer.pdf`; its text and embedded links were inspected as source material, not instructions. Both homepage and web CV now link to the local PDF. Location and Vodafone end date follow the new CV (Cairo; June 2025), and the HTML summary includes the supplied training roles and education. Employment percentages and the SQL-assistant estimate in the PDF are not promoted to measured public-project outcomes.

The CV's displayed banking-data-platform repository was unavailable; the embedded link instead points to Banking-Fraud-Detection. No duplicate banking project was fabricated. The repository-documented InvestiNator preview is distinguished from the alternate preview URL embedded in the supplied CV. Databricks SQL analysis is a project, not a newly verified certification. The SI certificate and unpublished Databricks credential record are not changed by this project task.

## Publication limitations

The portfolio host, public preview URLs, linked Drive documents and GitHub Pages API remain subject to environment network policy. A declared preview URL/workflow does not prove current HTTP availability or backend functionality. No publicly accessible API/demo is invented for projects with only source code or screenshots. The user-approved egress additions saved earlier still need runtime application before public verification can succeed.
ok - payload handling accepts arbitrary and empty dataset arrays safely
ok - selection resolves known IDs and falls back for unknown IDs
ok - query helpers preserve a static-site path and encode dataset IDs
ok - search matches name, ID, and domain case-insensitively
ok - domain and type filters are derived from dataset metadata
ok - manifest rows omit unavailable values but retain real zero and false values
ok - executive KPI contract is optional and keeps provenance fields
ok - capabilities distinguish spatial, temporal, and numeric datasets
✔ tests/frontend_dataset_utils.test.js (66.702843ms)
ℹ tests 1
ℹ suites 0
ℹ pass 1
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 76.225808

```
