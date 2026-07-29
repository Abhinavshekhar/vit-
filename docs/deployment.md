# AstraOS Deployment Guide

This repository is ready to be connected to hosted infrastructure, but deployment requires owner-controlled accounts and secrets. Codex cannot publish a live website without access to your Vercel/Railway/Supabase project credentials.

## Recommended Phase 1 hosting

- **Web:** Vercel project rooted at `apps/web`.
- **API:** Railway service rooted at `apps/api` running `uvicorn astra_os.main:app --host 0.0.0.0 --port $PORT`.
- **Database:** Supabase or Railway PostgreSQL with pgvector enabled.
- **Cache/queue:** Railway Redis.
- **Secrets:** Platform secret manager, never committed to Git.

## Web deployment steps

1. Create a Vercel project from this Git repository.
2. Set the project root directory to `apps/web`.
3. Use the included `apps/web/vercel.json` defaults.
4. Add environment variables when the web app starts calling the API:
   - `NEXT_PUBLIC_API_BASE_URL=https://<your-api-host>/api/v1`
5. Deploy from the current branch.

## API deployment steps

1. Create a Railway service from this Git repository.
2. Set the service root to `apps/api`.
3. Use this start command:

```bash
uvicorn astra_os.main:app --host 0.0.0.0 --port $PORT
```

4. Add required environment variables:
   - `DATABASE_URL`
   - `REDIS_URL`
   - `JWT_SECRET`
   - `OPENAI_API_KEY`
   - `GOOGLE_CLIENT_ID`
   - `GOOGLE_CLIENT_SECRET`
   - `ENCRYPTION_KEY_BASE64`
5. Run the schema in `apps/api/astra_os/db/schema.sql` against PostgreSQL before enabling live traffic.

## Go-live checklist

- [ ] Vercel web deployment succeeds.
- [ ] API `/health` returns `{"status":"ok","service":"astra-os-api"}`.
- [ ] PostgreSQL has `pgcrypto` and `vector` extensions enabled.
- [ ] Redis connection is healthy.
- [ ] All secrets are set in hosted secret managers.
- [ ] OAuth redirect URLs point at live domains.
- [ ] CI passes on the deployment branch.
- [ ] HTTPS is enforced for both web and API.


## Automated Vercel deployment

The repository includes `.github/workflows/deploy-web.yml` and `scripts/deploy_web.sh` for live web publishing once the owner adds `VERCEL_TOKEN`, `VERCEL_ORG_ID`, and `VERCEL_PROJECT_ID` as GitHub Actions secrets. Codex cannot create that token or access your Vercel account, but after the secrets are configured the workflow can be run manually from GitHub Actions or automatically on pushes to `main` that touch `apps/web/**`.

Manual local deployment is also available:

```bash
export VERCEL_TOKEN=<your-vercel-token>
export VERCEL_ORG_ID=<your-vercel-org-id>
export VERCEL_PROJECT_ID=<your-vercel-project-id>
./scripts/deploy_web.sh
```

The deploy script uses `vercel pull`, `vercel build`, and `vercel deploy --prebuilt` so CI has a linked project configuration and fails during build before attempting to publish.
