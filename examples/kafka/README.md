# Kafka Java learning lab

Tested with Kafka broker/client **4.1.1**, Temurin **JDK 17.0.17**, Maven **3.9.11** on Linux. Java source targets release 17. JDK 21 can run the broker; the documented client lab was built and run with JDK 17.

Prerequisites: a full JDK (not just a JRE), Maven, and the Apache Kafka 4.1.1 binary distribution. Use the [official downloads](https://archive.apache.org/dist/kafka/4.1.1/) and verify the archive against its published SHA-512 checksum. Keep TLS and checksum verification enabled.

## Start a disposable local broker

From the extracted Kafka directory, **only for a fresh local data directory**:

```bash
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
bin/kafka-storage.sh format --standalone -t "$KAFKA_CLUSTER_ID" -c config/server.properties
bin/kafka-server-start.sh config/server.properties
```

Keep the server running in that terminal. Do not format existing broker storage. The bundled combined broker/controller configuration has one node and no broker failure tolerance. It is not a production recommendation.

## Build and execute

From the portfolio checkout:

```bash
cd examples/kafka
mvn -B package dependency:copy-dependencies
java -cp 'target/classes:target/dependency/*' dev.minamarkos.OrdersLab
```

Optional first argument: a bootstrap server, for example `localhost:9092`. Run against a disposable broker with topic create/delete permissions. The lab creates a uniquely named `orders-lab-*` topic with two partitions, RF=1; uses a fresh consumer group; processes six keyed records; verifies committed next offsets; and deletes its topic. It performs no external business side effect. An interrupted process can leave its unique topic behind; inspect before removing it.

Expected final line:

```text
PASS: 6 unique orders, stable key routing, committed next offsets
```

Partition IDs and UUIDs vary. Two different keys may hash to the same partition. The assertions intentionally test stable routing, not a fictional one-key-per-partition guarantee. Send futures and a bounded polling deadline propagate failures as a nonzero exit. Maven packaging has no unit-test suite; **running the lab is the functional check**.

## Configuration reasoning

- `acks=all`, `enable.idempotence=true`: explicit producer retry/acknowledgement policy; RF=1 still means only one data copy.
- `request.timeout.ms=10000`, `linger.ms=5`, `delivery.timeout.ms=30000`: delivery timeout exceeds request timeout plus linger. These are lab bounds, not a tuning recommendation.
- `group.id`: unique per run so previous offsets cannot hide data.
- `enable.auto.commit=false`: commits follow processing, never precede it.
- `auto.offset.reset=earliest`: starts from the beginning only when no usable committed offset exists.
- `max.poll.records=10`: bounds a poll batch for this small fixture.
- Commit value is processed offset **plus one**, checked against broker state.

## Troubleshooting

- **Timeout / disconnect:** check broker startup logs, advertised listeners, client reachability, and bootstrap port. Container `localhost` has a different scope from host `localhost`.
- **No records:** inspect assignment, topic, group, and committed offsets. The fixture uses fresh identifiers to avoid stale group state.
- **Authorization failure:** grant only the required local topic/group permissions; retrying cannot repair authorization.
- **Compiler release unsupported:** inspect `mvn -version`, `java -version`, and `javac -version`; select a full JDK 17 or 21.
- **TLS validation failure in a managed proxy:** use the administrator-provided trusted CA store. In this environment Maven needed its HTTPS proxy configuration and `-Djavax.net.ssl.trustStore=/etc/ssl/certs/java/cacerts` when using the downloaded JDK. Never disable certificate validation. Proxy settings are environment-specific and are not committed.
- **Failure after a durable external write:** implement sink-side idempotency before adapting this example; console processing cannot demonstrate exactly-once external effects.

[Validation scope](../VALIDATION.md) · [Original educational repository](https://github.com/MINAADELMARKOS/Apache-Kafka) · [Full tutorial](https://minaadelmarkos.github.io/MinaMarkos/insights/kafka-java-producer-consumer.html)
