# Distribution draft — Spark Troubleshooting: Turn Symptoms Into Testable Hypotheses

Prepared for manual review. Not posted or sent. No production-experience claims are implied.

## LinkedIn educational post

A six-part investigation method for memory failures, shuffle delays, skew, GC, failed stages, contention, and small files.

Symptom: an executor disappears, tasks retry, or logs show heap exhaustion or a container memory kill. Likely causes include oversized partitions, a forced broadcast, large per-key state, Python worker memory, or insufficient overhead. Collect executor stderr, container exit reason, peak memory, spill, task input sizes, and the physical plan.

A useful review question: What evidence would distinguish heap exhaustion from a container overhead kill on your platform?

The local lab provides a healthy reference plan; none of these production failures was induced in this task. Practice a bounded failure drill in a disposable environment, then confirm both infrastructure health and the dataset’s business cutoff after remediation. A completed retry is insufficient if the published totals or freshness remain wrong.

Full article: https://minaadelmarkos.github.io/MinaMarkos/insights/spark-troubleshooting.html
Code and validation scope: https://github.com/MINAADELMARKOS/MinaMarkos/tree/main/examples/spark

## Short video script (approximately 60–90 seconds)

**0–10s / Hook:** What evidence would distinguish heap exhaustion from a container overhead kill on your platform?

**10–35s / System model:** Symptom: an executor disappears, tasks retry, or logs show heap exhaustion or a container memory kill. Likely causes include oversized partitions, a forced broadcast, large per-key state, Python worker memory, or insufficient overhead. Collect executor stderr, container exit reason, peak memory, spill, task input sizes, and the physical plan.

**35–60s / Visual:** Draw these boundaries: Symptom → scope / application ID → Logs + plan + task distributions → Hypothesis → bounded change → correctness and deadline checks. Explain which operation crosses each boundary and which evidence would show it failed.

**60–90s / Decision:** A six-part investigation method for memory failures, shuffle delays, skew, GC, failed stages, contention, and small files. Read the full article and check the linked validation scope before applying a configuration to production.

On-screen article: https://minaadelmarkos.github.io/MinaMarkos/insights/spark-troubleshooting.html
On-screen code: https://github.com/MINAADELMARKOS/MinaMarkos/tree/main/examples/spark

## Discussion questions

1. What evidence would distinguish heap exhaustion from a container overhead kill on your platform?
2. For “Executor out-of-memory”, what measurement in your workload would disprove the initial assumption?
3. For “A repeatable investigation record”, which recovery or cost constraint would change your decision?
