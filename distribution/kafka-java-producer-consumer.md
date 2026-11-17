# Distribution draft — Kafka Producer and Consumer Tutorial in Java

Prepared for manual review. Not posted or sent. No production-experience claims are implied.

## LinkedIn educational post

Run a bounded Java lab that creates a topic, sends keyed orders, checks partition routing, and verifies committed offsets.

Use Kafka 4.1.1 in KRaft mode, its matching Java client, JDK 17 or 21, and Maven 3.9.x. The accompanying source is intentionally small enough to inspect. It creates a unique topic with two partitions and replication factor one, sends six synthetic orders, consumes them with a unique group, checks routing and commits, then deletes the topic. Run it only against a disposable local broker with topic-create and topic-delete permissions.

A useful review question: Where would you put a deduplication record if the sink were a relational database?

Connection timeouts suggest a stopped broker, an unreachable advertised listener, or a wrong port. Topic authorization failures require permissions, not more retries. A consumer that sees no data may be in an old group with committed positions, reading another topic, or waiting for assignment. This lab uses fresh identifiers to remove those ambiguities. If a run fails before cleanup, inspect and remove only its uniquely named orders-lab topic.

Full article: https://minaadelmarkos.github.io/MinaMarkos/insights/kafka-java-producer-consumer.html
Code and validation scope: https://github.com/MINAADELMARKOS/MinaMarkos/tree/main/examples/kafka

## Short video script (approximately 60–90 seconds)

**0–10s / Hook:** Where would you put a deduplication record if the sink were a relational database?

**10–35s / System model:** Use Kafka 4.1.1 in KRaft mode, its matching Java client, JDK 17 or 21, and Maven 3.9.x. The accompanying source is intentionally small enough to inspect. It creates a unique topic with two partitions and replication factor one, sends six synthetic orders, consumes them with a unique group, checks routing and commits, then deletes the topic. Run it only against a disposable local broker with topic-create and topic-delete permissions.

**35–60s / Visual:** Draw these boundaries: Admin creates 2-partition topic → Producer → keyed orders → broker → Consumer processes → commits next offsets → assertions. Explain which operation crosses each boundary and which evidence would show it failed.

**60–90s / Decision:** Run a bounded Java lab that creates a topic, sends keyed orders, checks partition routing, and verifies committed offsets. Read the full article and check the linked validation scope before applying a configuration to production.

On-screen article: https://minaadelmarkos.github.io/MinaMarkos/insights/kafka-java-producer-consumer.html
On-screen code: https://github.com/MINAADELMARKOS/MinaMarkos/tree/main/examples/kafka

## Discussion questions

1. Where would you put a deduplication record if the sink were a relational database?
2. For “Prerequisites and scope”, what measurement in your workload would disprove the initial assumption?
3. For “Expected results and failure diagnosis”, which recovery or cost constraint would change your decision?
