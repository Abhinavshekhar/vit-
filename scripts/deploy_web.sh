#!/usr/bin/env bash
set -euo pipefail

if ! command -v npx >/dev/null 2>&1; then
  echo "npx is required to deploy the web app with Vercel CLI." >&2
  exit 1
fi

missing=0
for name in VERCEL_TOKEN VERCEL_ORG_ID VERCEL_PROJECT_ID; do
  if [[ -z "${!name:-}" ]]; then
    echo "$name must be set for non-interactive Vercel deployment." >&2
    missing=1
  fi
done
if [[ "$missing" -ne 0 ]]; then
  exit 1
fi

cd "$(dirname "$0")/../apps/web"

# Pull project settings so CI has the same framework/output settings as Vercel.
npx vercel pull --yes --environment=production --token "$VERCEL_TOKEN"

# Build first and deploy the prebuilt output. This fails earlier and with clearer logs than
# directly invoking a remote deploy from CI.
npx vercel build --prod --token "$VERCEL_TOKEN"
npx vercel deploy --prebuilt --prod --token "$VERCEL_TOKEN"
