# Distribution draft — Kafka Architecture Explained: Partitions, Replicas and KRaft

Prepared for manual review. Not posted or sent. No production-experience claims are implied.

## LinkedIn educational post

Follow a record from producer to partition leader to consumer, then separate data replication from metadata consensus.

A topic names a stream; partitions divide its log into independent ordered sequences. Brokers store replicas of those partitions. The producer learns metadata, chooses a partition, and sends to its leader. Followers replicate the leader’s log. A replication factor of three means three replicas total, not three followers. Spread replicas across failure domains when the deployment supports rack awareness.

A useful review question: If the controller quorum is healthy but one partition cannot elect a leader, which evidence would you inspect next?

Kafka 4.x no longer uses ZooKeeper. Older deployments may still have ZooKeeper-based operational procedures, so do not copy their failure diagnosis into a KRaft runbook. A one-node combined broker/controller is appropriate for the lab. Production role separation and quorum membership depend on the Kafka version and availability requirements. During an incident, identify which plane is failing before restarting anything.

Full article: https://minaadelmarkos.github.io/MinaMarkos/insights/kafka-architecture.html
Code and validation scope: https://github.com/MINAADELMARKOS/MinaMarkos/tree/main/examples/kafka

## Short video script (approximately 60–90 seconds)

**0–10s / Hook:** If the controller quorum is healthy but one partition cannot elect a leader, which evidence would you inspect next?

**10–35s / System model:** A topic names a stream; partitions divide its log into independent ordered sequences. Brokers store replicas of those partitions. The producer learns metadata, chooses a partition, and sends to its leader. Followers replicate the leader’s log. A replication factor of three means three replicas total, not three followers. Spread replicas across failure domains when the deployment supports rack awareness.

**35–60s / Visual:** Draw these boundaries: Producer → partition leader → follower replicas → Controller quorum → cluster metadata → Consumer group → assigned partitions → committed offsets. Explain which operation crosses each boundary and which evidence would show it failed.

**60–90s / Decision:** Follow a record from producer to partition leader to consumer, then separate data replication from metadata consensus. Read the full article and check the linked validation scope before applying a configuration to production.

On-screen article: https://minaadelmarkos.github.io/MinaMarkos/insights/kafka-architecture.html
On-screen code: https://github.com/MINAADELMARKOS/MinaMarkos/tree/main/examples/kafka

## Discussion questions

1. If the controller quorum is healthy but one partition cannot elect a leader, which evidence would you inspect next?
2. For “The data path: topics, partitions, brokers”, what measurement in your workload would disprove the initial assumption?
3. For “KRaft is the metadata plane”, which recovery or cost constraint would change your decision?
