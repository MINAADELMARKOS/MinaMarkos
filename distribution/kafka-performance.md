# Distribution draft — Kafka Performance Optimization Is a Capacity Trade-off

Prepared for manual review. Not posted or sent. No production-experience claims are implied.

## LinkedIn educational post

Balance throughput, tail latency, recovery headroom, storage, and cost instead of copying a universal configuration.

Begin with record size distribution, records per second, key distribution, consumer count, and p95/p99 end-to-end latency. A benchmark made of tiny uniformly distributed messages will not predict a production stream dominated by a few large keys. Include serialization, sink work, and acknowledgement policy in the measured path.

A useful review question: Would your cheapest steady-state configuration clear a one-hour backlog before the next business deadline?

Then test a controlled consumer outage and measure backlog clearance. Save configuration, software versions, hardware, rates, latency percentiles, errors, and cost assumptions with each result. These benchmark and failure experiments are not executed by the functional Java lab. Treat them as a workload-specific exercise; no universal performance uplift is claimed.

Full article: https://minaadelmarkos.github.io/MinaMarkos/insights/kafka-performance.html
Code and validation scope: https://github.com/MINAADELMARKOS/MinaMarkos/tree/main/examples/kafka

## Short video script (approximately 60–90 seconds)

**0–10s / Hook:** Would your cheapest steady-state configuration clear a one-hour backlog before the next business deadline?

**10–35s / System model:** Begin with record size distribution, records per second, key distribution, consumer count, and p95/p99 end-to-end latency. A benchmark made of tiny uniformly distributed messages will not predict a production stream dominated by a few large keys. Include serialization, sink work, and acknowledgement policy in the measured path.

**35–60s / Visual:** Draw these boundaries: Record rate × size × retention → Replication + compression + headroom → Throughput / p99 latency / recovery / cost decision. Explain which operation crosses each boundary and which evidence would show it failed.

**60–90s / Decision:** Balance throughput, tail latency, recovery headroom, storage, and cost instead of copying a universal configuration. Read the full article and check the linked validation scope before applying a configuration to production.

On-screen article: https://minaadelmarkos.github.io/MinaMarkos/insights/kafka-performance.html
On-screen code: https://github.com/MINAADELMARKOS/MinaMarkos/tree/main/examples/kafka

## Discussion questions

1. Would your cheapest steady-state configuration clear a one-hour backlog before the next business deadline?
2. For “Set the workload and latency budget”, what measurement in your workload would disprove the initial assumption?
3. For “An experiment with a decision rule”, which recovery or cost constraint would change your decision?
