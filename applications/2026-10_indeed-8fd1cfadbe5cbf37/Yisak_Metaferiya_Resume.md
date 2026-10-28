# Yisak Metaferiya
**Junior Software Engineer | Backend Developer (Java · Spring Boot · Node.js)**

United Arab Emirates · yisakdemelash7@gmail.com · [GitHub](https://github.com/Yisak-E) · [LinkedIn](https://www.linkedin.com/in/yisak-isaac-ma2027) · [Portfolio](https://yisakmeta.online)

## Summary
Backend-focused software engineering student (Abu Dhabi University) and software engineering intern at nanoVOLTZ. Builds secure REST APIs in Java/Spring Boot (Spring Security, JWT, JPA, PostgreSQL), Node.js/NestJS (MongoDB, RBAC, Swagger) and Python/Flask (SQLAlchemy, Celery, Redis). Has implemented concurrency control for high-contention ticket sales, real-time updates over Server-Sent Events, and an encrypted multi-broker RabbitMQ pub/sub system. Ships with Docker and Git.

## Technical Skills
- **Languages:** Java, TypeScript, JavaScript, Python, SQL, C, Kotlin, Go
- **Backend:** Spring Boot, Spring Security + JWT, Spring Data JPA / Hibernate, NestJS, Node.js, Flask, REST API design, Role-based access control (RBAC)
- **Databases & Data:** PostgreSQL, MySQL, MongoDB / Mongoose, Firebase / Firestore, Redis, SQLAlchemy / Alembic, pandas / Jupyter
- **DevOps & Tools:** Git / GitHub, Docker (multi-stage builds), Docker Compose, Maven, GitHub Actions / Pages, Cloud deployment (Render)
- **Testing & Quality:** pytest, JUnit 5

## Experience
### Software Engineering Intern — nanoVOLTZ
*Internship · United Arab Emirates · Jan 2026 – Present*


### Project Intern — CodSoft
*Internship · United Arab Emirates (remote) · Dec 2024 – Jan 2025*


### Project Intern — CodeAlpha
*Internship · Remote · Dec 2024 – Jan 2025*


### Peer Tutor — Abu Dhabi University
*Part-time · Abu Dhabi, UAE · Feb 2024 – Jan 2025*


## Projects
### [MegaSeller — Concurrent Cinema Ticketing API](https://github.com/Yisak-E/mega_seller_backend)
*Java 21, Spring Boot, Spring Security, JWT, Spring Data JPA, PostgreSQL, H2, Server-Sent Events* · 2026

- Built a Spring Boot REST API for movies, showtimes, tickets and orders with layered controller/service/repository architecture and DTOs.
- Prevented overselling under concurrent purchases with a fair per-showtime ReentrantLock (tryLock with timeout) plus database row locking inside a @Transactional purchase flow.
- Secured endpoints with Spring Security and stateless JWT authentication, separate user and admin roles, and a token filter for SSE streams.

### [Spring Boot API Starters — JWT Auth & RBAC Templates](https://github.com/Yisak-E/spring_boot_templete)
*Java, Spring Boot, Spring Security, JWT (jjwt), Spring Data JPA, MySQL, H2, Lombok* · 2025–2026

- Built reusable Spring Boot starters with stateless JWT authentication filters, custom UserDetailsService and role enums, used as the base for new APIs such as MegaSeller.
- Configured Spring Data JPA persistence for MySQL (production) and H2 (local/testing) with Actuator health endpoints.

### [Smart City Event Bus — Secure Multi-Broker Pub/Sub](https://github.com/Yisak-E/Quic_lab)
*Java, RabbitMQ (AMQP), Topic exchanges, AES, HMAC, Maven, SLF4J* · 2026

- Designed a publish/subscribe system across three RabbitMQ brokers (traffic, weather, utilities) using topic exchanges and routing-key based subscriptions.
- Implemented a topic routing service and load balancer that resolve each event to the right broker, with per-broker message metrics.
- Protected messages end to end with AES encryption for confidentiality and an HMAC for integrity verification at subscribers.

### [Makeda Threads — E-commerce Platform (NestJS + React)](https://github.com/Yisak-E/Makeda_Threads_backend)
*TypeScript, NestJS, MongoDB, Mongoose, Passport JWT, bcrypt, Swagger, Docker Compose* · 2026

- Built a modular NestJS backend (users, auth, products, orders, notifications) on MongoDB with DTO validation via class-validator.
- Implemented JWT authentication with Passport and bcrypt password hashing, plus role decorators and guards for admin-only routes.
- Added order processing with notification logging, database seeding scripts and Swagger API documentation; ran services with Docker Compose.

## Education
### B.Sc. Software Engineering — Abu Dhabi University
*Abu Dhabi, UAE · Aug 2023 – Expected 2027*

Relevant coursework: Object-Oriented Programming & Design Patterns (Java), Data Structures & Algorithms, Operating Systems (multithreading in C), Distributed Systems (messaging, pub/sub), Web & Mobile Application Development

## Certifications
- Visual Elements of User Interface Design — CalArts (Coursera)
- Introduction to Next.js
- Introduction to Ethical Hacking Principles
- Create a Supermarket App using Java OOP
- Python GUI Development with Tkinter
