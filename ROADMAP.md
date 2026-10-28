# Career Roadmap

> Draft built on 2026-10-28 from your GitHub (~90 repos) and LinkedIn export. Edit it freely. It's yours.
> Tick boxes as you go and commit; `git log ROADMAP.md` becomes your progress record.

## Where you are (Oct 2026)

- **Role:** Software Engineering Intern @ nanoVOLTZ (since Jan 2026). B.Sc. Software Engineering @ Abu Dhabi University (started Aug 2023).
- **Strongest evidence:** Java/Spring Boot backends (MegaSeller: concurrency + JWT + SSE + Docker), NestJS/MongoDB APIs with RBAC, a RabbitMQ distributed pub/sub system, and many Next.js/React frontends.
- **Gaps recruiters will notice:** most repos have boilerplate READMEs, no live demos, few tests, no CI pipelines, no cloud or Java certification (your 16 Credly badges are strong on data/Python/SQL, but none covers backend Java or cloud), and experience entries with no descriptions.

## Target

**Junior Backend / Full-Stack Software Engineer (Java · Spring Boot, or Node · NestJS) in the UAE**, by graduation (expected 2027). Internship → return offer or graduate role.

---

## Phase 0: Fix this week (high impact, low effort)

- [ ] **SECURITY: remove committed secrets from public repos.** `email_client/.env` contains Gmail IMAP/SMTP password fields. `typing_club_server/.env` has `SECRET_KEY` / `JWT_SECRET_KEY`. Also check `quiz_gen_api/.env`, `tracker/.env`, `Secondary_school_management/.env` and `university/.env`. **Rotate the Gmail app password first**, then delete the files, add `.env` to `.gitignore`, and purge them from history (`git filter-repo` or BFG).
- [ ] Fix the LinkedIn badge in your GitHub profile README (the link is malformed markdown) and replace the placeholder `your-portfolio-link.com` with https://yisakmeta.online.
- [ ] Pin 6 repos on GitHub: mega_seller_backend, Makeda_Threads_backend, Quic_lab, advanced_typing_backend, quiz_gen_api, General_purpose_webapp.
- [ ] Write real READMEs for those 6: what it is, architecture diagram, how to run, screenshots, what you learned.
- [ ] Add nanoVOLTZ, CodSoft, CodeAlpha and Peer Tutor bullets to `Work-Experience/experience.yml` **and** to LinkedIn.
- [ ] Add details for ROAR, NLP Sentiment Analysis and JMeter Load Testing (`Projects/*/project.md`).
- [x] Import 16 verified Credly badges into the vault (done 2026-10-28).
- [ ] Add issue dates and credential links for the 5 LinkedIn-only certifications.
- [ ] Add the Credly badges to LinkedIn → Licenses & certifications (most are missing there).

## Phase 1: Next 3 months (Nov 2026 – Jan 2027): make the best projects production-grade

- [ ] **MegaSeller:** add a JMeter load-test plan (e.g. 500 concurrent buyers on one showtime) and record that zero tickets oversell plus p95 latency. This one step also fills the JMeter Load Testing project.
- [ ] Add tests: JUnit 5 + Mockito + Testcontainers (Spring), Jest + Supertest (NestJS). Target 60%+ coverage on service layers.
- [ ] Add GitHub Actions CI (build + test + Docker image) to the pinned repos.
- [ ] Deploy MegaSeller and Makeda Threads with live URLs (Render / Railway / Azure free tier) and put them on the resume.
- [ ] Merge the three Spring Boot templates into one documented `spring-boot-starter` repo.
- [ ] LeetCode: 2–3 problems/week, mostly medium arrays/graphs/DP. Track the count in Achievements.

## Phase 2: 3–6 months (Feb – Apr 2027): depth and credentials

- [ ] Certification (pick one first):
  - [ ] **Oracle Certified Professional: Java SE 17 Developer**: strongest signal for Java backend roles
  - [ ] **AWS Certified Cloud Practitioner → Developer Associate**, or **Microsoft Azure AZ-900** (Azure is common with UAE employers)
- [ ] Learn and apply: Kubernetes basics, Redis caching, Kafka (compare with your RabbitMQ project), OpenAPI-first design.
- [ ] One "flagship" project combining the above: microservices + messaging + CI/CD + observability.
- [ ] Graduation project: choose something that extends the flagship or solves a real problem at nanoVOLTZ.

## Phase 3: 6–12 months (May – Dec 2027): land the role

- [ ] Apply 10+/week from Aug 2027. Track every one in `applications/`.
- [ ] Prepare 5 STAR stories (in each project's notes): concurrency bug, security fix, teamwork (UAE Connect), teaching (Peer Tutor), internship impact.
- [ ] System design basics: URL shortener, ticketing system (you've built one), chat.
- [ ] Ask nanoVOLTZ about a return offer / graduate role.

---

## Skill matrix (update as you grow)

| Area | Now | Target 2027 | Next step |
|---|---|---|---|
| Java / Spring Boot | Working–strong | Strong + OCP | Tests, Testcontainers, OCP Java 17 |
| Node / NestJS | Strong | Strong | Jest/Supertest, CI |
| Databases | Working | Strong | Indexing, query plans, migrations |
| Distributed / messaging | Working | Working–strong | Kafka, idempotency, retries |
| Testing / QA | Familiar | Working | JUnit, JMeter, coverage gates |
| DevOps / Cloud | Familiar | Working | GitHub Actions, AWS/Azure cert, K8s basics |
| Frontend (React/Next) | Strong | Strong | Keep current. Not the main focus. |
