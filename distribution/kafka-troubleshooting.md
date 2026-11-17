# Distribution draft — Kafka Production Troubleshooting: Diagnose Before Restarting

Prepared for manual review. Not posted or sent. No production-experience claims are implied.

## LinkedIn educational post

Connect lag, replica health, disk, network, and controller evidence to a safe next action.

A lag alert is a symptom, not a diagnosis. Identify the group, topic, partitions, event-time freshness, and business deadline. Record when the problem began and whether producer traffic changed. Compare rates over the same interval: a rising end offset with a flat committed offset differs from a quiet producer and a stalled source system.

A useful review question: Which metric distinguishes a slow sink from a producer traffic surge in your runbook?

Close with the cause, evidence, bounded change, and rollback conditions. “Restart fixed it” leaves the next responder without a model. Track recurrence and time to restore useful business data, not only time to restart the process.

Full article: https://minaadelmarkos.github.io/MinaMarkos/insights/kafka-troubleshooting.html
Code and validation scope: https://github.com/MINAADELMARKOS/MinaMarkos/tree/main/examples/kafka

## Short video script (approximately 60–90 seconds)

**0–10s / Hook:** Which metric distinguishes a slow sink from a producer traffic surge in your runbook?

**10–35s / System model:** A lag alert is a symptom, not a diagnosis. Identify the group, topic, partitions, event-time freshness, and business deadline. Record when the problem began and whether producer traffic changed. Compare rates over the same interval: a rising end offset with a flat committed offset differs from a quiet producer and a stalled source system.

**35–60s / Visual:** Draw these boundaries: Freshness / lag alert → Partition + client + broker evidence → Bounded change → rate recovery → business verification. Explain which operation crosses each boundary and which evidence would show it failed.

**60–90s / Decision:** Connect lag, replica health, disk, network, and controller evidence to a safe next action. Read the full article and check the linked validation scope before applying a configuration to production.

On-screen article: https://minaadelmarkos.github.io/MinaMarkos/insights/kafka-troubleshooting.html
On-screen code: https://github.com/MINAADELMARKOS/MinaMarkos/tree/main/examples/kafka

## Discussion questions

1. Which metric distinguishes a slow sink from a producer traffic surge in your runbook?
2. For “Start with impact and a time window”, what measurement in your workload would disprove the initial assumption?
3. For “Verify recovery against the original symptom”, which recovery or cost constraint would change your decision?
