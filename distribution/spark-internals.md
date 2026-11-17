# Distribution draft — Spark Internals: Why Shuffles and Partition Shape Dominate

Prepared for manual review. Not posted or sent. No production-experience claims are implied.

## LinkedIn educational post

Reason about narrow dependencies, redistribution, serialization, locality, and scheduling through the bytes each task must move.

A partition is a unit of parallel work, not a guarantee of equal load. Ten equally sized files may contain very different row widths or key distributions. Input partitions depend on file splits and source behavior; shuffle partitions depend on exchanges and adaptive decisions. Do not confuse storage partition directories with execution partitions.

A useful review question: Would your slowest stage improve by moving fewer bytes or by allocating more cores?

The checked-in lab validates the baseline plan and totals, not this scale experiment. Keep the experiment’s results separate and repeat it with the platform’s exact Spark build. Vendor patches, AQE behavior, storage connectors, and workload shape can change the best choice.

Full article: https://minaadelmarkos.github.io/MinaMarkos/insights/spark-internals.html
Code and validation scope: https://github.com/MINAADELMARKOS/MinaMarkos/tree/main/examples/spark

## Short video script (approximately 60–90 seconds)

**0–10s / Hook:** Would your slowest stage improve by moving fewer bytes or by allocating more cores?

**10–35s / System model:** A partition is a unit of parallel work, not a guarantee of equal load. Ten equally sized files may contain very different row widths or key distributions. Input partitions depend on file splits and source behavior; shuffle partitions depend on exchanges and adaptive decisions. Do not confuse storage partition directories with execution partitions.

**35–60s / Visual:** Draw these boundaries: Narrow scan / filter within partitions → Exchange serializes and redistributes keys → Reduce tasks → skewed tail → completion time. Explain which operation crosses each boundary and which evidence would show it failed.

**60–90s / Decision:** Reason about narrow dependencies, redistribution, serialization, locality, and scheduling through the bytes each task must move. Read the full article and check the linked validation scope before applying a configuration to production.

On-screen article: https://minaadelmarkos.github.io/MinaMarkos/insights/spark-internals.html
On-screen code: https://github.com/MINAADELMARKOS/MinaMarkos/tree/main/examples/spark

## Discussion questions

1. Would your slowest stage improve by moving fewer bytes or by allocating more cores?
2. For “Partitioning is a distribution of work”, what measurement in your workload would disprove the initial assumption?
3. For “A disciplined experiment”, which recovery or cost constraint would change your decision?
