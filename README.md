<div align="center">

<img src="./assets/hero.svg" width="100%" alt="Trần Hoàng Long — Backend Java Developer. An isometric 3D server cluster: Spring Boot API, PostgreSQL, Redis and RabbitMQ exchanging packets on a floating platform." />

<a href="https://github.com/trhlow">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=19&duration=3200&pause=900&color=7EE0A1&center=true&vCenter=true&width=760&lines=Designing+backends+that+stay+correct+under+load;Spring+Boot+%E2%80%A2+PostgreSQL+%E2%80%A2+Redis+%E2%80%A2+RabbitMQ;Modular+monoliths%2C+transactional+outbox%2C+signed+releases;Currently+shipping+evts.id.vn+for+Tra+Vinh+University" alt="Typing intro" />
</a>

<p>
  <a href="https://evts.id.vn"><img src="https://img.shields.io/badge/live-evts.id.vn-7ee0a1?style=for-the-badge&logo=googlechrome&logoColor=white&labelColor=0b1228" alt="Live project" /></a>
  <a href="mailto:thlong190705@gmail.com"><img src="https://img.shields.io/badge/email-thlong190705-ff9d4d?style=for-the-badge&logo=gmail&logoColor=white&labelColor=0b1228" alt="Email" /></a>
  <img src="https://img.shields.io/badge/based_in-Vinh_Long,_VN-7fb2ff?style=for-the-badge&logo=googlemaps&logoColor=white&labelColor=0b1228" alt="Location" />
  <img src="https://komarev.com/ghpvc/?username=trhlow&style=for-the-badge&color=c49bff&label=profile+views" alt="Profile views" />
</p>

</div>

<br/>

<div align="center"><img src="./assets/titles/about.svg" width="70%" alt="01 — About me" /></div>

<table>
<tr>
<td width="52%" valign="top">

Xin chào! I'm **Long**, an IT student at **Tra Vinh University** who builds backends the way production
expects them: invariants guarded twice, tests running against real infrastructure, and releases that
can prove where they came from.

Most of my work is **Java + Spring Boot** behind a React or Flutter client. I like the hard parts —
concurrency, auth, messaging, deployment — and I write the docs so the next person doesn't have to
reverse-engineer them.

- 🔭 Shipping **[TVU Event & Ticket](https://github.com/trhlow/TVU-Event-Ticket)**, live at [evts.id.vn](https://evts.id.vn)
- 🌱 Going deeper on supply-chain security, observability and event-driven design
- 💬 Ask me about Spring Security, Redis, RabbitMQ, Flyway, Testcontainers
- ⚡ Fun fact: my Unity coursework was a **Snake game** — so a snake now eats my contribution graph below

</td>
<td width="48%" valign="top">

```java
var me = Developer.builder()
    .name("Trần Hoàng Long")
    .role("Backend Java Developer")
    .base("Vinh Long, Viet Nam")
    .school("Tra Vinh University · IT")
    .languages(List.of(
        "Java", "TypeScript", "Dart",
        "Python", "C#"))
    .backend(List.of(
        "Spring Boot", "Spring Security",
        "JPA", "WebSocket/STOMP"))
    .data(List.of(
        "PostgreSQL", "MongoDB",
        "Redis", "RabbitMQ"))
    .ops(List.of(
        "Docker", "Caddy", "GitHub Actions"))
    .motto("Correct first, then fast.")
    .build();
```

</td>
</tr>
</table>

<br/>

<div align="center"><img src="./assets/titles/flagship.svg" width="70%" alt="02 — Flagship project" /></div>

<div align="center">
  <a href="https://github.com/trhlow/TVU-Event-Ticket"><img src="./assets/cards/tvu-event-ticket.svg" width="62%" alt="TVU Event & Ticket — event management and e-ticketing for Tra Vinh University clubs" /></a>
</div>

<br/>

> Clubs publish events, students sign in with their university account, organizers approve within a fixed
> capacity, and every approved seat becomes a **cryptographically signed QR ticket** that scans exactly once.

| | What it takes | How it's built |
|:-:|---|---|
| 🎟️ | **Seats can never be oversold** | Approval — not submission — consumes inventory. Atomic Redis decrement + PostgreSQL optimistic locking. Load test: **500 concurrent approvals against 100 seats → exactly 100 tickets**. |
| 📬 | **No lost tickets** | Ticket + outbox row in one transaction → RabbitMQ `reservation.approved` → signed QR mailed by the notification module. |
| 🔐 | **Role-scoped access** | Microsoft Entra sign-in for students, mailed one-time codes for staff, Super Admin read-only across club scope — enforced in `SecurityConfig` *and* again in services. |
| 🧱 | **Modular monolith** | Consolidated from five microservices into four features talking via DTOs and domain events; Flyway `V1–V15` restored the foreign keys the split had ruled out. |
| 🛡️ | **Releases you can verify** | Build once in CI: Syft SBOM, Trivy scans, **11 Sigstore attestations**, a mutation-tested publish gate, deploy only by verified tag. |
| ✅ | **Tested for real** | 76 backend test classes on Testcontainers, 105 frontend tests, CodeQL on Java + TypeScript. |

<p align="center">
  <img src="https://skillicons.dev/icons?i=java,spring,react,ts,tailwind,postgres,redis,rabbitmq,docker,githubactions" alt="TVU Event & Ticket stack" />
</p>

<br/>

<div align="center"><img src="./assets/titles/projects.svg" width="70%" alt="03 — Projects" /></div>

<p align="center">
  <a href="https://github.com/trhlow/TraVinh-Shelter"><img src="./assets/cards/cong-tin-land.svg" width="48%" alt="Công Tín Land — real-estate platform for Tra Vinh" /></a>
  <a href="https://github.com/trhlow/chat-application"><img src="./assets/cards/inchat.svg" width="48%" alt="InChat — real-time chat system" /></a>
</p>
<p align="center">
  <a href="https://github.com/trhlow/EDUCYCLE"><img src="./assets/cards/educycle.svg" width="48%" alt="EduCycle — peer-to-peer marketplace for students' books" /></a>
  <a href="https://github.com/trhlow/Personal-Management"><img src="./assets/cards/personal-ai-manager.svg" width="48%" alt="Personal AI Manager — goals, tasks, finance and AI insights" /></a>
</p>
<p align="center">
  <a href="https://github.com/trhlow/taxiincomemanager"><img src="./assets/cards/taxi-income-manager.svg" width="48%" alt="Taxi Income Manager — income tracker for taxi drivers" /></a>
</p>

<br/>

<div align="center"><img src="./assets/titles/lab.svg" width="70%" alt="04 — Lab and coursework" /></div>

<p align="center">
  <a href="https://github.com/trhlow/vietfood67_dudoancalories"><img src="./assets/cards/vietfood-ai.svg" width="32%" alt="VietFood AI — Vietnamese food recognition with YOLO" /></a>
  <a href="https://github.com/trhlow/TKWeb"><img src="./assets/cards/am-thuc-mien-tay.svg" width="32%" alt="Ẩm Thực Miền Tây — Mekong Delta cuisine website" /></a>
  <a href="https://github.com/trhlow/CSN-TranHoangLong-110123025-SnakeGame"><img src="./assets/cards/snake-game.svg" width="32%" alt="Snake Game — Unity coursework" /></a>
</p>

<br/>

<div align="center"><img src="./assets/titles/stack.svg" width="70%" alt="05 — Tech stack" /></div>

<div align="center">
  <img src="./assets/stack.svg" width="100%" alt="Exploded isometric architecture: client, backend, data and infrastructure layers with the technologies used in each" />

  <br/><br/>

  <img src="https://skillicons.dev/icons?i=java,kotlin,ts,js,dart,python,cs&perline=7" alt="Languages" /><br/>
  <img src="https://skillicons.dev/icons?i=spring,maven,gradle,postgres,mongodb,redis,rabbitmq&perline=7" alt="Backend and data" /><br/>
  <img src="https://skillicons.dev/icons?i=react,vite,tailwind,html,css,flutter,unity&perline=7" alt="Frontend, mobile and game" /><br/>
  <img src="https://skillicons.dev/icons?i=docker,nginx,githubactions,git,linux,idea,postman&perline=7" alt="DevOps and tools" />
</div>

<br/>

<div align="center"><img src="./assets/titles/principles.svg" width="70%" alt="06 — How I build" /></div>

<table>
<tr>
<td width="50%" valign="top">

### 🎯 Correctness first
Invariants get two independent guards — a fast atomic counter and a database lock.
Write APIs take an `Idempotency-Key`, so a retry never double-books or double-charges.

</td>
<td width="50%" valign="top">

### 🧩 Modules by domain
`auth`, `event`, `ticket`, `booking`, `property`… each owns its data and talks through
DTOs and domain events, never through someone else's repository.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🔐 Secure by default
Argon2id hashing with transparent BCrypt upgrade, JWT `jti` revocation, persisted
refresh tokens, rate-limited logins and OTP stores that fail **closed**.

</td>
<td width="50%" valign="top">

### 🧪 Test against the real thing
Testcontainers for PostgreSQL and Redis, path-filtered CI, CodeQL, and load tests for the
paths where a race condition would actually hurt.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🚢 Ship with evidence
Docker Compose everywhere, Caddy for TLS, images built once in CI, signed, scanned,
and deployed only by a verified tag — with a backup before every migration.

</td>
<td width="50%" valign="top">

### 📚 Docs are part of the product
ADRs, runbooks and bilingual (EN/VI) READMEs, so setup takes minutes rather than
an afternoon of guessing.

</td>
</tr>
</table>

<br/>

<div align="center"><img src="./assets/titles/activity.svg" width="70%" alt="07 — GitHub activity" /></div>

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./profile-3d-contrib/profile-night-rainbow.svg" />
    <source media="(prefers-color-scheme: light)" srcset="./profile-3d-contrib/profile-gitblue.svg" />
    <img src="./profile-3d-contrib/profile-night-rainbow.svg" width="100%" alt="3D isometric contribution calendar" />
  </picture>

  <br/><br/>

  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/trhlow/trhlow/output/github-snake-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/trhlow/trhlow/output/github-snake.svg" />
    <img src="https://raw.githubusercontent.com/trhlow/trhlow/output/github-snake.svg" width="100%" alt="A snake eating my contribution graph" />
  </picture>
</div>

<br/>

<div align="center">

**Let's build something that holds up in production.**

<a href="mailto:thlong190705@gmail.com"><img src="https://img.shields.io/badge/Say_hi-thlong190705@gmail.com-ff9d4d?style=flat-square&logo=gmail&logoColor=white" alt="Email me" /></a>
<a href="https://github.com/trhlow?tab=repositories"><img src="https://img.shields.io/badge/All_repositories-trhlow-7fb2ff?style=flat-square&logo=github&logoColor=white" alt="Repositories" /></a>

<img src="./assets/footer.svg" width="100%" alt="" />

</div>
