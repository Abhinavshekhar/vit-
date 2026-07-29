#!/usr/bin/env bash
set -euo pipefail

if ! command -v npx >/dev/null 2>&1; then
  echo "npx is required to deploy the web app with Vercel CLI." >&2
  exit 1
fi

if [[ -z "${VERCEL_TOKEN:-}" ]]; then
  echo "VERCEL_TOKEN must be set. Create it in Vercel account settings and export it before running." >&2
  exit 1
fi

cd "$(dirname "$0")/../apps/web"
npx vercel deploy --prod --yes --token "$VERCEL_TOKEN"
