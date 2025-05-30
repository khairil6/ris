#!/usr/bin/env sh
set -eux   # -e exit on error, -u undefined vars are errors, -x echo each command

cd /app

# 1) Scaffold once if missing (ignore any TTY errors)
if [ ! -f package.json ] || [ ! -d node_modules ]; then
  echo "⟳ Scaffolding Nuxt 3 (template=v3)…"
  npx nuxi init . \
    --force \
    --template v3 \
    --packageManager npm \
    --gitInit false \
    --no-install \
  || echo "⚠ nuxi init failed (TTY); but continuing anyway"
fi

# 2) Install (or re-install) dependencies
echo "⟳ Installing npm packages…"
npm install --verbose

# 3) Launch the dev server as PID 1 (keeps container alive)
echo "⟳ Starting Nuxt dev server…"
exec npm run dev -- --hostname 0.0.0.0 --port 3000
