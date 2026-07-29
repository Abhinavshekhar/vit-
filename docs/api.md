# AstraOS API Specification

All routes are prefixed with `/api/v1` and return JSON. Authenticated routes require `Authorization: Bearer <jwt>`.

## System

- `GET /health` — service health.
- `GET /brief/today` — current morning-style brief with priorities and alerts.

## Planning

- `POST /planner/schedule` — creates an optimized schedule from tasks, busy blocks, day boundaries, and energy profile.

## Tasks

- `GET /tasks?status=&course_id=&from=&to=` — list tasks.
- `POST /tasks` — create a manual or extracted task.
- `PATCH /tasks/{id}` — update status, estimate, deadline, priority, or risk.
- `POST /tasks/{id}/split` — invoke Deadline Agent task splitting.

## Attendance

- `GET /courses/{id}/attendance` — current and forecast attendance.
- `POST /courses/{id}/attendance/forecast` — simulate attend, skip, OD, or leave choices.

## Agents

- `POST /agents/gmail/sync` — enqueue Gmail sync.
- `POST /agents/calendar/sync` — enqueue calendar sync.
- `POST /agents/vtop/sync` — enqueue supported VTOP sync/export parsing.
- `POST /agents/vitcc/sync` — enqueue supported VITCC sync/export parsing.
- `GET /agents/runs/{id}` — inspect status, findings, warnings, and confidence.

## Assistant

- `POST /chat` — grounded AI chat over tasks, attendance, calendar, events, and memory.
- `GET /search?q=` — global search across assignments, subjects, emails, events, faculty, and notes.

## Notifications

- `GET /notifications` — list pending and sent notifications.
- `POST /notifications/brief/morning` — generate morning brief.
- `POST /notifications/summary/evening` — generate evening summary.
- `POST /notifications/report/weekly` — generate weekly report.
