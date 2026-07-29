# AstraOS – AI Student Operating System

AstraOS is a production-oriented AI operating system for university students. It combines academic ingestion, task intelligence, attendance risk prediction, deterministic scheduling, notifications, analytics, and natural language assistance into one modular platform.

## Product promise

AstraOS answers: **"What should I do right now?"** It does this by collecting trusted academic signals, turning them into structured knowledge, optimizing a real schedule with constraints, and using AI only where language understanding, ranking, and explanation improve the experience.

## Architecture overview

- **Frontend:** Next.js, React, TypeScript, Tailwind CSS, PWA shell, accessible glassmorphism dashboard.
- **Backend:** FastAPI, SQLAlchemy, PostgreSQL, Redis, Celery workers, JWT sessions, Google OAuth.
- **AI layer:** OpenAI API, LangGraph-style agent orchestration, embeddings, RAG over emails, notes, events, and course material.
- **Scheduler:** deterministic constraint-based planner that optimizes tasks before an LLM explains the result.
- **Security:** OAuth-first integrations, encrypted sensitive payloads, audit logging, rate limiting, and policy-compliant platform access.

## Repository structure

```text
apps/api/        FastAPI backend, agents, scheduler, database, security
apps/web/        Next.js frontend shell and design system
infra/           Docker Compose and deployment primitives
docs/            System design, API specification, roadmap, security, testing
tests/           Unit and integration test placeholders
```

## Local development

```bash
cp .env.example .env
docker compose -f infra/docker-compose.yml up --build
```

Phase 1 targets a single user while preserving tenant, university, and integration boundaries for later scale.
