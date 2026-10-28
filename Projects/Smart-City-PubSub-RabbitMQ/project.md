---
id: smart-city-pubsub
title: Smart City Event Bus — Secure Multi-Broker Pub/Sub
period: '2026'
status: complete
repos:
- https://github.com/Yisak-E/Quic_lab
tags:
- backend
- java
- distributed
- messaging
- security
- rabbitmq
stack:
- Java
- RabbitMQ (AMQP)
- Topic exchanges
- AES
- HMAC
- Maven
- SLF4J
summary: Distributed publish/subscribe system routing traffic, weather and utility events across several RabbitMQ brokers.
bullets:
- text: Designed a publish/subscribe system across three RabbitMQ brokers (traffic, weather, utilities) using topic exchanges and routing-key based subscriptions.
  tags:
  - distributed
  - messaging
- text: Implemented a topic routing service and load balancer that resolve each event to the right broker, with per-broker message metrics.
  tags:
  - distributed
  - backend
- text: Protected messages end to end with AES encryption for confidentiality and an HMAC for integrity verification at subscribers.
  tags:
  - security
priority: 2
---

# Smart City Event Bus — Secure Multi-Broker Pub/Sub

## Notes (not printed on resume)

Course lab (Distributed Systems?). Add throughput / latency numbers if you measured them.

## Interview story (STAR)

- **Situation:** 
- **Task:** 
- **Action:** 
- **Result:** 
