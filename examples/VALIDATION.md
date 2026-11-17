# Learning hub validation record

Date: **17 November 2026**. All data and Kafka topics used for checks were synthetic and local. No production service was changed.

## Executed

| Check | Runtime / scope | Outcome |
|---|---|---|
| Java build | Maven 3.9.11, Temurin JDK 17.0.17, kafka-clients 4.1.1 | Packaging and dependency resolution passed. No unit tests are defined; packaging alone is not the functional check. |
| Java Kafka lab | Kafka 4.1.1 KRaft, one combined node, two topic partitions, RF=1 | Six unique payloads processed; key-to-partition consistency and committed next offsets asserted. Clean-path run and a second independent run passed. |
| Read-only Kafka diagnostics | Topic describe, group describe, under-replicated partitions, KRaft quorum status on 4.1.1 | Executed successfully. Two-partition local topic had leader/ISR=1; under-replicated list was empty; quorum reported leader 1. Completed lab group had no active members after topic cleanup. No broker failure was induced. |
| PySpark lab | Spark 3.5.7, Python 3.12.14, JDK 17.0.17, local[2] | Finance=200 and Networks=120 asserted; partition pruning, pushdown, broadcast join and exchange markers verified. |
| Additional Spark runtime | Same fixture, environment JRE 21.0.13 | Passed; JDK 17 remains the documented baseline. |
| Static pages | `python3 tools/validate_learning_hub.py` | 22 pages: 21 articles and blog. One H1, unique titles/IDs, canonical/robots/social metadata, JSON-LD, internal links/fragments, sitemap coverage, preserved legacy paragraphs, and 12 distribution drafts. |
| Browser flows | Chromium/Playwright, 375 / 768 / 1024 / 1440 px | Homepage desktop/mobile navigation, library filters/search/reset/empty state, representative article layouts/TOCs, and clipboard copying passed; no horizontal reading overflow. All 21 article routes served. |
| Progressive enhancement | JavaScript disabled | All 21 cards remain readable; static category anchor navigation works. |

## Explicitly not executed

- Kafka multi-broker failure/recovery, transaction abort/crash tests, dead-letter atomicity, external sink idempotency, throughput or latency benchmarks.
- Spark executor/driver OOM, cluster-scale skew/GC/network failures, performance comparisons, YARN, Cloudera, Kubernetes, or managed-cloud deployment.
- Existing VerdaTrace/InvestiNator project demos and migration exercises were not rerun; preserved project prose does not imply new execution evidence.
- Production incident commands or confidential infrastructure access.
- LinkedIn posting or video publication. Distribution files are review drafts only.
- Public Pages deployment and outbound documentation HTTP checks are blocked by the environment egress policy at the time of this record. Local link existence and Git repository access were checked; remote HTTP availability is not implied.

## Source review and originality

Reviewed repositories:

- `Apache-Kafka` at `52b8259`: README concepts and `Commands.txt`. Modernized CLI naming/options; the new Java lab is original.
- `Apache_Spark` at `d05fc04`: execution graph, lazy evaluation, shuffles, joins, and operational lecture topics. Corrected overly absolute simplifications (for example one action need not map to exactly one job).
- `Pyspark-_Tutorials` at `9fcdd47`: notebooks assume older Spark/Java, Google Colab and mounted Drive paths. The new lab is self-contained and avoids those assumptions.

No book passages or book diagrams were copied. Existing portfolio prose is retained in `content/existing_articles.json` and rendered on the original article URLs. New diagrams are original conceptual illustrations.

## Reproduce the website checks

```bash
python3 tools/build_learning_hub.py
python3 tools/validate_learning_hub.py
node --check js/learning-hub.js
python3 -m http.server 8002 --bind 127.0.0.1
# In another terminal with Playwright and Chromium installed:
node tools/check_learning_hub.cjs
```

Build and run each lab using its README. Browser checks default to the local server above; `HUB_BASE_URL` and `CHROMIUM_PATH` can override it. Screenshots are written to a temporary directory. Egress may need adjustment for public verification; do not bypass TLS or network controls.
