package dev.minamarkos;

import java.time.Duration;
import java.util.*;
import java.util.concurrent.TimeUnit;
import org.apache.kafka.clients.admin.*;
import org.apache.kafka.clients.consumer.*;
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.common.serialization.*;

/** Bounded, repeatable local lab; not a production payments consumer. */
public final class OrdersLab {
  public static void main(String[] args) throws Exception {
    String bootstrap = args.length > 0 ? args[0] : "localhost:9092";
    String topic = "orders-lab-" + UUID.randomUUID();
    Properties adminProps = new Properties();
    adminProps.put("bootstrap.servers", bootstrap);
    try (Admin admin = Admin.create(adminProps)) {
      admin.createTopics(List.of(new NewTopic(topic, 2, (short) 1))).all().get(30, TimeUnit.SECONDS);
      System.out.println("Created " + topic + " with 2 partitions (local RF=1)");
      try {
      Properties producerProps = new Properties();
      producerProps.put("bootstrap.servers", bootstrap);
      producerProps.put("key.serializer", StringSerializer.class.getName());
      producerProps.put("value.serializer", StringSerializer.class.getName());
      producerProps.put("acks", "all");
      producerProps.put("enable.idempotence", "true");
      producerProps.put("request.timeout.ms", "10000");
      producerProps.put("linger.ms", "5");
      producerProps.put("delivery.timeout.ms", "30000");
      try (KafkaProducer<String, String> producer = new KafkaProducer<>(producerProps)) {
        for (int i = 0; i < 6; i++) {
          var result = producer.send(new ProducerRecord<>(topic, "customer-" + (i % 2), "order-" + i)).get(35, TimeUnit.SECONDS);
          System.out.printf("Produced order-%d partition=%d offset=%d%n", i, result.partition(), result.offset());
        }
      }
      Properties consumerProps = new Properties();
      consumerProps.put("bootstrap.servers", bootstrap);
      consumerProps.put("group.id", "orders-lab-" + UUID.randomUUID());
      consumerProps.put("key.deserializer", StringDeserializer.class.getName());
      consumerProps.put("value.deserializer", StringDeserializer.class.getName());
      consumerProps.put("auto.offset.reset", "earliest");
      consumerProps.put("enable.auto.commit", "false");
      consumerProps.put("max.poll.records", "10");
      Set<String> seen = new HashSet<>();
      Map<String, Integer> keyPartitions = new HashMap<>();
      Map<TopicPartition, OffsetAndMetadata> processed = new HashMap<>();
      try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(consumerProps)) {
        consumer.subscribe(List.of(topic));
        long deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(45);
        while (seen.size() < 6 && System.nanoTime() < deadline) {
          for (ConsumerRecord<String, String> record : consumer.poll(Duration.ofSeconds(1))) {
            // Replace with an idempotent durable write BEFORE committing in a real application.
            Integer previous = keyPartitions.putIfAbsent(record.key(), record.partition());
            if (previous != null && previous != record.partition()) throw new IllegalStateException("Key moved partition");
            if (!seen.add(record.value())) throw new IllegalStateException("Unexpected duplicate in clean run");
            processed.put(new TopicPartition(topic, record.partition()), new OffsetAndMetadata(record.offset() + 1));
            System.out.printf("Processed %s key=%s partition=%d offset=%d%n", record.value(), record.key(), record.partition(), record.offset());
          }
          if (!processed.isEmpty()) consumer.commitSync(processed, Duration.ofSeconds(10));
        }
        if (seen.size() != 6) throw new IllegalStateException("Expected 6 records; got " + seen.size());
        for (var entry : processed.entrySet()) {
          var committed = consumer.committed(Set.of(entry.getKey())).get(entry.getKey());
          if (committed == null || committed.offset() != entry.getValue().offset()) throw new IllegalStateException("Commit mismatch");
        }
        System.out.println("PASS: 6 unique orders, stable key routing, committed next offsets");
      }
      } finally {
        admin.deleteTopics(List.of(topic)).all().get(30, TimeUnit.SECONDS);
      }
    } catch (Exception failure) {
      System.err.println("Lab failed: " + failure + "; inspect bootstrap address, broker logs, and advertised listeners.");
      throw failure;
    }
  }
}
