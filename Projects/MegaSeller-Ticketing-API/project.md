---
id: mega-seller
title: MegaSeller — Concurrent Cinema Ticketing API
period: '2026'
status: complete
repos:
- https://github.com/Yisak-E/mega_seller_backend
tags:
- backend
- java
- spring-boot
- concurrency
- security
- rest
- sql
- docker
- real-time
- api
stack:
- Java 21
- Spring Boot
- Spring Security
- JWT
- Spring Data JPA
- PostgreSQL
- H2
- Server-Sent Events
- springdoc OpenAPI
- Actuator
- Docker
- Maven
summary: Movie-ticket sales backend built to stay correct when many buyers hit the same showtime at once.
bullets:
- text: Built a Spring Boot REST API for movies, showtimes, tickets and orders with layered controller/service/repository architecture and DTOs.
  tags:
  - backend
  - rest
  - spring-boot
- text: Prevented overselling under concurrent purchases with a fair per-showtime ReentrantLock (tryLock with timeout) plus database row locking inside a @Transactional purchase flow.
  tags:
  - concurrency
  - sql
  - java
- text: Streamed live seat inventory and per-thread lock/transaction state to clients over Server-Sent Events, turning concurrency behaviour into an observable dashboard.
  tags:
  - real-time
  - concurrency
- text: Secured endpoints with Spring Security and stateless JWT authentication, separate user and admin roles, and a token filter for SSE streams.
  tags:
  - security
  - spring-boot
- text: Containerised with a multi-stage Docker build (Maven → Temurin 21 JRE) for cloud deployment; documented the API with OpenAPI/Swagger.
  tags:
  - docker
  - devops
  - api
priority: 1
---

# MegaSeller — Concurrent Cinema Ticketing API

## Notes (not printed on resume)

Add: number of concurrent simulated buyers you tested with, and whether you load-tested it (JMeter?). Live URL if deployed on Render.

## Interview story (STAR)

- **Situation:** 
- **Task:** 
- **Action:** 
- **Result:** 
