<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/header-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/header-light.svg" />
  <img src="./assets/header-light.svg" width="100%" alt="Trần Hoàng Long, Backend Java Developer, Vinh Long, Viet Nam" />
</picture>

Xin chào! I'm Long, an IT student at Tra Vinh University. I build backends, mostly with Java and
Spring Boot, and I enjoy the hard parts: concurrency, auth, messaging and deployment.

## Projects

### [TVU Event & Ticket](https://github.com/trhlow/TVU-Event-Ticket)

Event management and e-ticketing for the student clubs of Tra Vinh University.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/flow-tvu-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/flow-tvu-light.svg" />
  <img src="./assets/flow-tvu-light.svg" width="100%" alt="Flow: register, organizer approves, signed QR ticket, one-time check-in" />
</picture>

- Seats cannot be oversold: a load test runs 500 concurrent approvals against 100 seats and requires exactly 100 tickets.
- Tickets go out through a transactional outbox and RabbitMQ, as signed QR codes that scan exactly once.
- Releases are built once in CI, scanned, signed with Sigstore and deployed only by a verified tag.

`Java 25` `Spring Boot 4` `React 19` `PostgreSQL` `Redis` `RabbitMQ`

### [Cambridge Exam Prep](https://github.com/trhlow/cambridge-exam-prep)

Computer-based exam system for the test room of Victory English Centre, covering A2 Key and B1 Preliminary for Schools.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/flow-cambridge-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/flow-cambridge-light.svg" />
  <img src="./assets/flow-cambridge-light.svg" width="100%" alt="Flow: import paper, open session, live proctoring, grading" />
</picture>

- Proctors watch the whole room live over SignalR: pause a candidate, add time, rewind the listening.
- The server owns the exam clock, and Safe Exam Browser is checked on every candidate request.
- Load-tested with 200 concurrent candidates, on top of 353 backend tests, 91 frontend tests and Playwright end-to-end tests.

`C#` `ASP.NET Core` `SignalR` `React` `TypeScript` `MySQL`

### [Công Tín Land](https://github.com/trhlow/TraVinh-Shelter)

Real-estate platform connecting buyers and renters with verified brokers in Tra Vinh.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/flow-cong-tin-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/flow-cong-tin-light.svg" />
  <img src="./assets/flow-cong-tin-light.svg" width="100%" alt="Flow: search listings, verify phone OTP, book a viewing, broker confirms" />
</picture>

- Viewing requests need an SMS one-time code first, which keeps out spam bookings.
- Organised by domain module, with flexible listing attributes stored as JSONB.
- Argon2id passwords, revocable JWTs and Redis-backed rate limiting.

`Java 25` `Spring Boot 4` `React 19` `PostgreSQL` `Redis`

## Stack

- **Languages:** Java, C#, TypeScript
- **Backend:** Spring Boot, Spring Security, ASP.NET Core
- **Data:** PostgreSQL, MySQL, MongoDB, Redis, RabbitMQ
- **Frontend:** React, Tailwind CSS
- **Infrastructure:** Docker, Caddy, GitHub Actions

## Contributions

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/trhlow/trhlow/output/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/trhlow/trhlow/output/github-snake.svg" />
  <img src="https://raw.githubusercontent.com/trhlow/trhlow/output/github-snake.svg" width="100%" alt="A snake moving across my contribution graph" />
</picture>

## Contact

[thlong190705@gmail.com](mailto:thlong190705@gmail.com)
