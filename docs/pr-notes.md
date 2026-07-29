# AstraOS PR Notes

This branch intentionally replaces earlier PR metadata with a fresh PR because the previous review flow was updated outside Codex.

## Current scope

- Production-oriented monorepo scaffold for API, web, infra, docs, and tests.
- Deterministic scheduling engine for reproducible plans.
- Attendance, event recommendation, and morning briefing services.
- PostgreSQL/pgvector schema for academic, productivity, notification, analytics, and AI memory records.
- Next.js/Tailwind/PWA web shell for the AstraOS command center.

## Validation

Run the core Python checks with:

```bash
python -m pytest tests
```

Validate frontend JSON metadata with:

```bash
python -m json.tool apps/web/package.json >/tmp/package.json.check
python -m json.tool apps/web/public/manifest.json >/tmp/manifest.json.check
```
