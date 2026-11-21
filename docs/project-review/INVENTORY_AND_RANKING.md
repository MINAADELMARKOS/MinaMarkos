# Project inventory and prioritization

Source-reviewed public repositories and original portfolio artifacts. Numeric scores are editorial judgments (0–5), not business KPIs or runtime measurements. Weights: enterprise relevance 2, architecture 1, data depth 2, AI 1, business relevance 1, implementation evidence 2, documentation 1. Equal totals retain the reviewed ordering; InvestiNator and VerdaTrace are co-leading by score.

| Rank | Project | Weighted score / 50 | Enterprise relevance | Architecture complexity | Data engineering depth | AI integration | Business value relevance | Implementation evidence | Documentation quality | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | InvestiNator — DataOps Incident Investigation | 45 | 5 | 5 | 4 | 5 | 4 | 4 | 5 | Local demo; production release blocked |
| 2 | VerdaTrace — Governed Cloud Data Platform | 45 | 5 | 5 | 5 | 1 | 4 | 5 | 5 | Implemented reference platform; cloud deployment not verified |
| 3 | DataGuard-AI — Telecom Reliability Monitoring | 34 | 5 | 3 | 3 | 0 | 4 | 4 | 3 | Seeded monitoring MVP; not production SaaS |
| 4 | Banking Fraud Detection Pipeline | 32 | 4 | 4 | 4 | 3 | 3 | 2 | 2 | Educational integration prototype; runtime gaps |
| 5 | Airflow Employee Dimension ETL | 30 | 4 | 3 | 4 | 0 | 3 | 3 | 2 | Code-backed learning pipeline; external services not run |
| 6 | Databricks Customer Sales Analysis | 24 | 3 | 2 | 2 | 0 | 3 | 3 | 3 | Synthetic SQL analytics demonstration |
| 7 | Vodafone LLM-Powered SQL Analytics Assistant | 24 | 4 | 2 | 2 | 4 | 3 | 1 | 1 | Applied AI PoC; CV-reported implementation |
| 8 | SuperMarket Dashboard / Superstore Analysis | 19 | 2 | 1 | 2 | 0 | 2 | 3 | 2 | Educational notebook and dashboard artifacts |
| 9 | Execution Time Dashboard | 12 | 2 | 1 | 1 | 0 | 2 | 1 | 1 | Screenshot/document artifact; implementation unverified |
| 10 | Supply Chain Dashboard | 12 | 2 | 1 | 1 | 0 | 2 | 1 | 1 | Screenshot/document artifact; implementation unverified |
| 11 | AOM Dashboard | 9 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | Screenshot/document artifact; implementation unverified |

All ten existing projects are retained; Databricks SQL analysis is added from the supplied CV and an accessible repository. The CV’s banking-data-platform URL was not accessible; its embedded PDF hyperlink actually points to Banking-Fraud-Detection, so no second banking project was invented. The CV-listed alternate InvestiNator preview URL is preserved on its case study, while the repository-documented preview is used on the card.

## InvestiNator — DataOps Incident Investigation
- Business problem: Platform incidents scatter evidence across services, slowing the path from a symptom to an auditable recovery decision.
- Technical objective: Correlate telemetry and incident context, investigate with read-only tools, require approval, and verify recovery against evidence.
- Category / stack: AI & Intelligent Systems / Python · FastAPI · Next.js · PostgreSQL · Kafka · OpenAI (optional)
- Status: Local demo; production release blocked
- Repository: https://github.com/MINAADELMARKOS/Investinator-Enterprise-DataOps-Incident-Resolution
- Revision: 06d036da27704a00559503bbd28fc3ad6b28347a
- Preview: https://minaadelmarkos.github.io/Investinator-Enterprise-DataOps-Incident-Resolution/
- Screenshot: img/portfolio/Enterprise-DataOps-Incident-Resolution-Copilot.png
- Documentation / source: docs/architecture.md, docs/security.md, docs/ai-design.md, tests/test_workflow.py, tests/test_platform.py, scripts/smoke_demo.py, apps/showcase/src/App.tsx, src/incident_copilot/api.py
- Architecture: Local Kafka producer / consumer + simulated ReplayLab fault signals → FastAPI telemetry → threshold rules → topology correlation → PostgreSQL incident, evidence, approval and audit state → Next.js operator UI → Read-only tools → optional configured OpenAI Responses; model output cannot authorize writes → Policy / approval → allowlisted simulated recovery → metric verification

## VerdaTrace — Governed Cloud Data Platform
- Business problem: Heterogeneous datasets are difficult to use safely when quality, ownership, provenance and suitability are disconnected.
- Technical objective: Ingest and profile data through a shared pipeline that publishes normalized results, quality findings, lineage and explainable visualization recommendations.
- Category / stack: Enterprise Data Platforms / Python · Pub/Sub · GKE · BigQuery · GCS · Terraform
- Status: Implemented reference platform; cloud deployment not verified
- Repository: https://github.com/MINAADELMARKOS/VerdaTrace-Data-Platform-
- Revision: 69a94cf0f9baee525bbd57a51f6fa44644382b58
- Preview: https://minaadelmarkos.github.io/VerdaTrace-Data-Platform-/
- Screenshot: img/portfolio/VerdaTrace_Data Platform_Portoflio.png
- Documentation / source: verdatrace/registered.py, verdatrace/quality.py, verdatrace/security.py, data_pipeline.py, main.tf, deployment.yaml, tests/test_registered_pipeline.py, docs/architecture.md, docs/validation.md, frontend/data/platform_demo.json
- Architecture: Registered local / attributed sample datasets → bounded ingestion → Quality checks → catalog / semantics → analysis → task-suitability evaluation → Normalized results + lineage / governance → generated frontend portal payload → Cloud worker path: Pub/Sub → GKE Python worker → BigQuery curated tables + controlled GCS archive → Cross-cutting IAM / Workload Identity / secret redaction / audit / monitoring

## DataGuard-AI — Telecom Reliability Monitoring
- Business problem: Missing feeds, late batches and revenue variance can leave telecom teams acting on incomplete information.
- Technical objective: Classify feed and ETL health, generate owned alerts, and show transparent estimated revenue exposure beside operational evidence.
- Category / stack: Data Engineering / Python · HTTP API · JavaScript · Rule-based monitoring
- Status: Seeded monitoring MVP; not production SaaS
- Repository: https://github.com/MINAADELMARKOS/DataGuard-AI
- Revision: d76cbf63295fa69b6a0bc3333a57dc3187c9fbdc
- Preview: No independently established live application
- Screenshot: img/portfolio/DataGuard-AI.png
- Documentation / source: src/dataguard_ai/api.py, src/dataguard_ai/monitoring.py, src/dataguard_ai/seed.py, tests/test_monitoring.py, docs/product-plan.md
- Architecture: Seed feed, job and revenue records + fixed scenario clock → Rule-based classification / runtime thresholds / historical revenue baseline → Alerts + estimated impact in process memory → Python ThreadingHTTPServer JSON routes → static dashboard → Owners and recommended next checks accompany alerts; no implemented ML/LLM layer

## Banking Fraud Detection Pipeline
- Business problem: Explore how suspicious transaction signals can move from streaming ingestion to analyst-facing outputs.
- Technical objective: A repository combines synthetic ATM events, streaming model-inference code, storage artifacts and dashboard evidence.
- Category / stack: Data Engineering / Kafka · Spark Streaming · HDFS · HBase · NiFi · Power BI
- Status: Educational integration prototype; runtime gaps
- Repository: https://github.com/MINAADELMARKOS/Banking-Fraud-Detection
- Revision: ee0c5ac6954c5e4d9451f5280e4343c18fe24e7c
- Preview: No independently established live application
- Screenshot: img/portfolio/Banking-Fraud-Detection.png
- Documentation / source: readme.md, Kafka/kafka_source.py, spark/streaming/streaming.py, docker/docker-compose.yml, hbase/DDL.sh, powerbi/Fraud_Detection.pbix
- Architecture: Synthetic ATM producer → Kafka (legacy ZooKeeper deployment documented) → Spark Streaming / model references → HDFS bronze / silver → Documented NiFi transfer → HBase → Power BI artifacts → Connector configs, model files and complete runtime need validation

## Airflow Employee Dimension ETL
- Business problem: Keep changing employee attributes available for historical reporting rather than overwriting prior values.
- Technical objective: An hourly DAG extracts HR/finance data to S3, identifies changes and branches into Snowflake dimension updates and inserts.
- Category / stack: Data Engineering / Airflow · PostgreSQL · S3 · Python · Snowflake
- Status: Code-backed learning pipeline; external services not run
- Repository: https://github.com/MINAADELMARKOS/Airflow-Data-Pipeline-ETL
- Revision: 350b3988df426fbf1f52d2c9d9ab27cd20eae5d6
- Preview: No independently established live application
- Screenshot: img/portfolio/Airflow_Data_Pipeline_ETL.png
- Documentation / source: Dags/ETL_DAG.py, Includes/emp_dim_insert_update.py, Includes/queries.py, README.md, Output/1.png
- Architecture: PostgreSQL HR / finance → SqlToS3Operator → S3 CSV extracts → Python change detection → Airflow branching / XCom → Snowflake update / insert tasks → historical employee dimension

## Databricks Customer Sales Analysis
- Business problem: Explore customer value, geographic revenue concentration and purchase recency in a controlled sales dataset.
- Technical objective: SQL cohorts, country totals, recency flags and a dashboard turn synthetic customer records into inspectable analytical outputs.
- Category / stack: Business Intelligence / Databricks SQL · CSV · Customer analytics
- Status: Synthetic SQL analytics demonstration
- Repository: https://github.com/MINAADELMARKOS/DataBricks_Customer_Sales_Analysis
- Revision: 9f9d9fb1f708bd717e72bab926164e6853d4ca37
- Preview: No independently established live application
- Screenshot: img/portfolio/Databricks_Customer_Sales.png
- Documentation / source: README.md, SQL Queries, customer_sales_summary_small.csv, Customer_Sales_Dashboard.png
- Architecture: 100 synthetic customer records (repository documentation) → Databricks SQL cohort / revenue / recency queries → Dashboard screenshot → analytical interpretation

## Vodafone LLM-Powered SQL Analytics Assistant
- Business problem: Help business users explore data with natural-language questions.
- Technical objective: The supplied CV describes a text-to-SQL proof of concept with prompt controls and database context.
- Category / stack: AI & Intelligent Systems / Python · LangChain · Ollama · Streamlit · SQL
- Status: Applied AI PoC; CV-reported implementation
- Repository: Not established
- Revision: Not available
- Preview: No independently established live application
- Screenshot: img/portfolio/VodaFone_Assistant.png
- Documentation / source: Original linked document and supplied CV only
- Architecture: Source / ingestion / processing details not established → Available presentation artifact → reviewer → No production monitoring, governance or deployment inferred

## SuperMarket Dashboard / Superstore Analysis
- Business problem: Explore sales and profit patterns in sample retail data.
- Technical objective: An exploratory notebook and dashboard documents analyze sample-store categories and regions.
- Category / stack: Business Intelligence / Python · Notebook · Power BI
- Status: Educational notebook and dashboard artifacts
- Repository: https://github.com/MINAADELMARKOS/SuperSampleStore_Analysis
- Revision: 1cbd61a0e0e443df7c72debeb411fefa2217143f
- Preview: No independently established live application
- Screenshot: img/portfolio/SuperMarket.jpg
- Documentation / source: README.md, SuperStore_notebook.ipynb, Dashboard Part1.pdf, DashBoard Part2.pdf
- Architecture: Source / ingestion / processing details not established → Available presentation artifact → reviewer → No production monitoring, governance or deployment inferred

## Execution Time Dashboard
- Business problem: Review execution-time information in a dashboard.
- Technical objective: The existing portfolio provides a screenshot and Drive document, without an accessible implementation repository.
- Category / stack: Business Intelligence / Not established from accessible source
- Status: Screenshot/document artifact; implementation unverified
- Repository: Not established
- Revision: Not available
- Preview: No independently established live application
- Screenshot: img/portfolio/ETD.jpeg
- Documentation / source: Original linked document and supplied CV only
- Architecture: Source / ingestion / processing details not established → Available presentation artifact → reviewer → No production monitoring, governance or deployment inferred

## Supply Chain Dashboard
- Business problem: Present an operational supply-chain dashboard; its requirements are not documented.
- Technical objective: An operational dashboard presentation; its source pipelines and metric definitions are not documented.
- Category / stack: Business Intelligence / Not established from accessible source
- Status: Screenshot/document artifact; implementation unverified
- Repository: Not established
- Revision: Not available
- Preview: No independently established live application
- Screenshot: img/portfolio/Supplychain.jpg
- Documentation / source: Original linked document and supplied CV only
- Architecture: Source / ingestion / processing details not established → Available presentation artifact → reviewer → No production monitoring, governance or deployment inferred

## AOM Dashboard
- Business problem: Business problem is not documented in the accessible source.
- Technical objective: A dashboard presentation artifact; the available source does not document its implementation or data model.
- Category / stack: Business Intelligence / Not established from accessible source
- Status: Screenshot/document artifact; implementation unverified
- Repository: Not established
- Revision: Not available
- Preview: No independently established live application
- Screenshot: img/portfolio/AOM.jpeg
- Documentation / source: Original linked document and supplied CV only
- Architecture: Source / ingestion / processing details not established → Available presentation artifact → reviewer → No production monitoring, governance or deployment inferred
