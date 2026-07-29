# AstraOS Complete Architecture

## 1. Complete software architecture

AstraOS is split into five independently scalable planes:

1. **Experience plane:** Next.js PWA dashboard, AI chat, calendar, task board, analytics, focus timer, and notification settings.
2. **API plane:** FastAPI REST APIs for tasks, events, attendance, planning, agents, search, analytics, and auth.
3. **Automation plane:** Celery workers pull supported integrations, classify content, generate tasks, recalculate plans, and emit notifications.
4. **Intelligence plane:** independent agents produce structured facts; deterministic services score, schedule, and forecast; LLMs classify, summarize, and explain.
5. **Data plane:** PostgreSQL for source-of-truth records, Redis for queues/cache/locks, vector storage for semantic memory and RAG.

## 2. System design

Events enter through OAuth integrations, supported exports, webhooks, or user input. Raw external records are stored with provenance, hashes, and sync state. Agents convert raw records into normalized tasks, events, attendance facts, deadlines, and recommendations. The scheduling engine creates an optimized plan using constraints. The assistant explains, answers questions, and requests clarification only when required.

### Core bounded contexts

- **Identity:** users, sessions, OAuth accounts, tenant and university metadata.
- **Academic graph:** courses, timetable, attendance, marks, assignments, exams, faculty announcements.
- **Productivity graph:** tasks, subtasks, dependencies, deadlines, effort estimates, focus sessions.
- **Opportunity graph:** events, hackathons, placements, internships, coding contests, workshops.
- **Planning graph:** calendars, availability windows, energy profile, schedule blocks, conflicts.
- **Memory graph:** preferences, habits, embeddings, summaries, performance trends.

## 3. Database schema

The production schema is defined in `apps/api/astra_os/db/schema.sql`. It covers users, OAuth accounts, courses, attendance, tasks, events, deadlines, emails, assignments, calendar items, notifications, preferences, analytics, audit logs, and AI memory.

## 4. API specification

See `docs/api.md` for versioned REST endpoints. All endpoints are tenant-aware, authenticated unless explicitly public, and return typed JSON envelopes.

## 5. Folder structure

```text
apps/api/astra_os/agents       Gmail, calendar, VTOP, VITCC, deadlines, attendance, event, planner agents
apps/api/astra_os/api          FastAPI routers
apps/api/astra_os/core         settings, logging, observability
apps/api/astra_os/db           SQLAlchemy session and SQL schema
apps/api/astra_os/scheduler    deterministic planning engine
apps/api/astra_os/security     auth, encryption, rate limiting
apps/api/astra_os/services     business services
apps/web/src/app               Next.js routes
apps/web/src/components        dashboard components
apps/web/src/lib               API client and utilities
infra                          Docker Compose and deploy assets
```

## 6. UI wireframes

### Dashboard

```text
┌──────────────────────────────────────────────────────────────┐
│ AstraOS  Search...                         Sync • Chat • Me  │
├───────────────┬──────────────────────────────┬───────────────┤
│ Now           │ Today's Perfect Plan          │ Attendance    │
│ 09:00 Deep    │ 08:00 Breakfast + commute     │ Physics 78%   │
│ Work: DSA     │ 09:00 DSA assignment          │ DBMS 86%      │
│               │ 11:00 Class                   │ Safe bunks: 2 │
├───────────────┼──────────────────────────────┼───────────────┤
│ Deadlines     │ Focus Timer                   │ AI Assistant  │
│ CAT Fri       │ 48:32                         │ Ask anything  │
│ Lab Mon       │ Start / Pause                 │               │
└───────────────┴──────────────────────────────┴───────────────┘
```

### Weekly analytics

```text
Productivity ring | Attendance heat map | Study hours by course | Burnout risk | OD usage
```

## 7. AI workflow

1. Ingest raw records with source metadata.
2. Classify and extract structured fields with confidence scores.
3. Store normalized facts and uncertain candidates separately.
4. Generate tasks, dependencies, deadlines, risk levels, and recommendations.
5. Run deterministic scheduling and forecasting services.
6. Use the LLM to explain decisions, answer natural language questions, and cite evidence.

## 8. Agent workflow

Each agent implements `Agent.run(context) -> AgentResult`. Agents are idempotent and write only normalized outputs through services.

- **Gmail Agent:** ignores spam, categorizes email, extracts assignments, quizzes, fees, placements, scholarships, internships, deadlines, urgency, and confidence.
- **Calendar Agent:** merges classes, meetings, hackathons, birthdays, travel, and personal events; reports conflicts.
- **VTOP Agent:** collects attendance, timetable, assignments, announcements, marks, labs, quizzes, CAT, and FAT only through supported integration methods.
- **VITCC Agent:** collects campus events, OD approvals, leave requests, workshops, club registrations, and volunteer opportunities.
- **Deadline Agent:** splits every deliverable into early subtasks and never plans first progress on the due date.
- **Attendance Agent:** predicts future attendance, minimum attendance, safe bunk count, and attend/skip/OD recommendations.
- **Event Recommendation Agent:** scores networking, placement value, growth, interest, attendance impact, deadline conflict, travel, and OD usage.
- **Productivity Planner:** combines all facts with energy, sleep, weather, travel, and class timing to produce the perfect day.

## 9. Scheduling algorithm

The planner is a constraint optimizer, not a prompt. It:

1. Builds availability windows from calendar events, classes, sleep, meals, travel, and fixed commitments.
2. Expands tasks into dependency-respecting work units.
3. Scores candidate placements using priority, deadline urgency, risk, energy fit, preferred time, location, and context switching cost.
4. Applies hard constraints: no overlaps, dependency order, fixed events, minimum sleep, no work after deadline.
5. Applies soft constraints: deep work preservation, batching, health breaks, early deadline completion, low context switching.
6. Produces schedule blocks and unresolved conflicts.
7. Sends the final plan to the LLM only for explanation and conversational reasoning.

## 10. Backend architecture

FastAPI exposes routers, delegates to services, and never embeds provider-specific logic in controllers. Celery queues are separated by priority: sync, extraction, planning, notifications, analytics. PostgreSQL transactions preserve consistency and Redis locks prevent duplicate sync jobs.

## 11. Frontend architecture

Next.js server components load initial dashboard data. Client components handle chat, drag-and-drop planning, focus timers, and optimistic task updates. Tailwind tokens implement dark glassmorphism with accessible contrast and reduced-motion support.

## 12. Security model

- Google OAuth for Google data; no password scraping.
- VTOP/VITCC access only through supported integration methods or user-provided exports.
- AES-256-GCM encryption for tokens and sensitive raw payloads.
- JWT access tokens, rotating refresh tokens, CSRF protection for cookie flows.
- Row-level tenant filters, least-privilege service roles, audit logging.
- XSS prevention through React escaping and strict Content Security Policy.
- SQL injection prevention through SQLAlchemy parameters.
- Rate limiting for auth, chat, and sync endpoints.

## 13. Deployment guide

Phase 1 can run on Vercel for the frontend, Railway/Supabase for API/PostgreSQL/Redis, and GitHub Actions for CI. Production uses separate API, worker, beat, web, database, and Redis services with secrets stored in platform secret managers.

## 14. Testing strategy

- Unit tests for scheduling, attendance forecasts, scoring, extraction parsers, and permission checks.
- Integration tests for API contracts, database migrations, OAuth callback flows, and queue jobs.
- E2E tests for dashboard, AI chat, sync status, task completion, and notification settings.
- Security tests for auth bypass, CSRF, XSS payloads, rate limits, and encrypted fields.

## 15. Future scalability

AstraOS evolves from one user to multi-university by adding tenant IDs, university connectors, provider capability registries, data retention controls, sharded job queues, partitioned analytics tables, and per-campus configuration.

## 16. Complete implementation roadmap

1. Foundation: monorepo, schema, auth, settings, Docker.
2. Core productivity: tasks, courses, attendance, calendar, manual input.
3. Planning engine: deterministic scheduler, task splitting, conflict detection.
4. Google integrations: Gmail, Calendar, Tasks, Drive via OAuth.
5. AI extraction: classifiers, confidence gates, review queue, RAG memory.
6. Notifications: morning brief, evening summary, weekly report.
7. Analytics: scores, heat maps, forecasts.
8. Campus integrations: supported VTOP/VITCC flows.
9. Multi-user hardening: tenants, quotas, observability, compliance.

## 17. Development milestones

- **M1:** schema, API skeleton, dashboard shell, Docker.
- **M2:** task, calendar, attendance CRUD and planning engine tests.
- **M3:** Gmail and Google Calendar sync with extraction review.
- **M4:** AI chat grounded in database and vector memory.
- **M5:** notifications, analytics, offline PWA.
- **M6:** production security, observability, deployment automation.

## 18. Production checklist

- [ ] All secrets managed outside source control.
- [ ] OAuth scopes minimized and reviewed.
- [ ] Database migrations tested forward and backward.
- [ ] Scheduler benchmarked on realistic semester data.
- [ ] Background jobs idempotent and observable.
- [ ] Audit logs immutable enough for incident response.
- [ ] Backups, restore drills, and retention policies configured.
- [ ] Accessibility and mobile PWA checks complete.

## 19. Technology decisions with justification

- **FastAPI:** typed Python APIs align with AI, scheduling, and data science workloads.
- **PostgreSQL:** strong relational model for academic records and scheduling constraints.
- **Redis + Celery:** reliable background sync, planning, notifications, and cache primitives.
- **Next.js:** production React framework with PWA support and strong deployment path.
- **OpenAI API:** robust language classification, summarization, assistant explanations, embeddings.
- **LangGraph-style orchestration:** explicit stateful agent workflows with retries and observability.

## 20. Production-ready code module strategy

Implementation begins with stable contracts: database schema, service interfaces, agent base classes, and scheduler primitives. Each module ships with tests before live integrations are enabled.
