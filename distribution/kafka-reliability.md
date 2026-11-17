# Distribution draft — Kafka Reliability and Message Delivery: Follow the Failure Window

Prepared for manual review. Not posted or sent. No production-experience claims are implied.

## LinkedIn educational post

Use crash timing to reason about at-most-once, at-least-once, idempotence, transactions, and dead-letter handling.

Imagine a consumer that writes an invoice and then commits its offset. Crash after the write but before the commit and the invoice event returns. Commit first, then crash before the write, and the invoice is lost from the application’s perspective. These two windows explain more than a delivery-label checklist.

A useful review question: What is the atomic boundary of your system’s exactly-once claim?

The Java lab verifies clean-path offsets and routing. It does not execute these transaction, crash, or dead-letter scenarios; they remain explicitly unexecuted exercises. Do not promote its PASS line into a claim of exactly-once production behavior. The business measure is duplicate or missing outcomes after recovery, not simply a flat lag chart.

Full article: https://minaadelmarkos.github.io/MinaMarkos/insights/kafka-reliability.html
Code and validation scope: https://github.com/MINAADELMARKOS/MinaMarkos/tree/main/examples/kafka

## Short video script (approximately 60–90 seconds)

**0–10s / Hook:** What is the atomic boundary of your system’s exactly-once claim?

**10–35s / System model:** Imagine a consumer that writes an invoice and then commits its offset. Crash after the write but before the commit and the invoice event returns. Commit first, then crash before the write, and the invoice is lost from the application’s perspective. These two windows explain more than a delivery-label checklist.

**35–60s / Visual:** Draw these boundaries: Read event → durable sink write → Crash window → replay possible → Commit next offset → recover from saved position. Explain which operation crosses each boundary and which evidence would show it failed.

**60–90s / Decision:** Use crash timing to reason about at-most-once, at-least-once, idempotence, transactions, and dead-letter handling. Read the full article and check the linked validation scope before applying a configuration to production.

On-screen article: https://minaadelmarkos.github.io/MinaMarkos/insights/kafka-reliability.html
On-screen code: https://github.com/MINAADELMARKOS/MinaMarkos/tree/main/examples/kafka

## Discussion questions

1. What is the atomic boundary of your system’s exactly-once claim?
2. For “The commit boundary defines replay”, what measurement in your workload would disprove the initial assumption?
3. For “A failure test worth running”, which recovery or cost constraint would change your decision?
