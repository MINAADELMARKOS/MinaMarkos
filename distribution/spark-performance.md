# Distribution draft — Spark Performance Optimization: Read the Physical Plan First

Prepared for manual review. Not posted or sent. No production-experience claims are implied.

## LinkedIn educational post

Validate pruning, pushdown, join strategy, AQE, caching, and file layout against a reproducible PySpark result.

Use the linked orders_lab.py with PySpark 3.5.7, Python 3.10–3.12, and JDK 17. The validation record states the actual runtime tested. The script creates its own temporary Parquet fixture and removes it afterward, so it can be rerun without relying on private data or a metastore. Install the pinned dependency in a virtual environment and run the commands below.

A useful review question: Which plan feature would prove your filter reduced input work rather than only filtering after the scan?

The local lab verifies result correctness and the expected plan features. Its four-row fixture cannot establish a speedup. Benchmark claims require representative scale and repeated measurements, and production changes require the platform’s own compatibility and rollout checks. The operational goal is a reliable publication deadline at acceptable cost.

Full article: https://minaadelmarkos.github.io/MinaMarkos/insights/spark-performance.html
Code and validation scope: https://github.com/MINAADELMARKOS/MinaMarkos/tree/main/examples/spark

## Short video script (approximately 60–90 seconds)

**0–10s / Hook:** Which plan feature would prove your filter reduced input work rather than only filtering after the scan?

**10–35s / System model:** Use the linked orders_lab.py with PySpark 3.5.7, Python 3.10–3.12, and JDK 17. The validation record states the actual runtime tested. The script creates its own temporary Parquet fixture and removes it afterward, so it can be rerun without relying on private data or a metastore. Install the pinned dependency in a virtual environment and run the commands below.

**35–60s / Visual:** Draw these boundaries: Prune partitions + columns + eligible predicates → Broadcast small dimension → aggregate exchange → Check final plan + output totals + runtime evidence. Explain which operation crosses each boundary and which evidence would show it failed.

**60–90s / Decision:** Validate pruning, pushdown, join strategy, AQE, caching, and file layout against a reproducible PySpark result. Read the full article and check the linked validation scope before applying a configuration to production.

On-screen article: https://minaadelmarkos.github.io/MinaMarkos/insights/spark-performance.html
On-screen code: https://github.com/MINAADELMARKOS/MinaMarkos/tree/main/examples/spark

## Discussion questions

1. Which plan feature would prove your filter reduced input work rather than only filtering after the scan?
2. For “A runnable baseline”, what measurement in your workload would disprove the initial assumption?
3. For “Choose a change by its evidence”, which recovery or cost constraint would change your decision?
