# Distribution draft — Understanding Kafka Through Real Business Problems

Prepared for manual review. Not posted or sent. No production-experience claims are implied.

## LinkedIn educational post

Choose event streaming by the decision deadline, replay requirement, and cost of coupling—not by message volume alone.

A telecom usage event is useful for billing tomorrow and for fraud detection now. A nightly export can satisfy the first requirement while making the second impossible. Before choosing Kafka, write down who needs the event, the latest useful arrival time, and what happens if a consumer is unavailable. Those three answers define the service you need more precisely than “real time.”

A useful review question: Which decision in your organization becomes less valuable while a batch schedule waits?

Pilot one event type with a deliberate consumer outage and a replay. Measure catch-up capacity while new traffic continues. If arrival rate is 1,000 records/s and sustainable consumption is 1,200 records/s, only 200 records/s are available to clear backlog. A 720,000-record backlog therefore needs about an hour, assuming stable rates. That recovery budget may change the capacity decision more than steady-state latency.

Full article: https://minaadelmarkos.github.io/MinaMarkos/insights/kafka-business-problems.html
Code and validation scope: https://github.com/MINAADELMARKOS/MinaMarkos/tree/main/examples/kafka

## Short video script (approximately 60–90 seconds)

**0–10s / Hook:** Which decision in your organization becomes less valuable while a batch schedule waits?

**10–35s / System model:** A telecom usage event is useful for billing tomorrow and for fraud detection now. A nightly export can satisfy the first requirement while making the second impossible. Before choosing Kafka, write down who needs the event, the latest useful arrival time, and what happens if a consumer is unavailable. Those three answers define the service you need more precisely than “real time.”

**35–60s / Visual:** Draw these boundaries: Source transaction → Durable event log → Independent risk / analytics / notification consumers. Explain which operation crosses each boundary and which evidence would show it failed.

**60–90s / Decision:** Choose event streaming by the decision deadline, replay requirement, and cost of coupling—not by message volume alone. Read the full article and check the linked validation scope before applying a configuration to production.

On-screen article: https://minaadelmarkos.github.io/MinaMarkos/insights/kafka-business-problems.html
On-screen code: https://github.com/MINAADELMARKOS/MinaMarkos/tree/main/examples/kafka

## Discussion questions

1. Which decision in your organization becomes less valuable while a batch schedule waits?
2. For “Begin with the time between an event and a decision”, what measurement in your workload would disprove the initial assumption?
3. For “A practical adoption decision”, which recovery or cost constraint would change your decision?
