#!/usr/bin/env sh
set -eu

echo "[entrypoint] Boot start"

# Wait for DB
if [ -n "${DB_HOST:-}" ] && [ -n "${DB_PORT:-}" ]; then
  echo "[entrypoint] Waiting for DB at ${DB_HOST}:${DB_PORT}..."
  python - <<'PYCODE'
import os, socket, time, sys
host = os.environ.get("DB_HOST"); port = int(os.environ.get("DB_PORT", "3306"))
deadline = time.time() + 60
while time.time() < deadline:
    s = socket.socket(); s.settimeout(2)
    try:
        s.connect((host, port)); s.close(); sys.exit(0)
    except Exception:
        time.sleep(1)
print("DB not reachable within 60s", file=sys.stderr); sys.exit(1)
PYCODE
  echo "[entrypoint] DB is up."
fi

echo "[entrypoint] Running migrations..."
python -m django migrate --noinput

echo "[entrypoint] collectstatic..."
python -m django collectstatic --noinput

echo "[entrypoint] Starting Gunicorn..."
# Make WSGI module configurable; default to app.wsgi
exec gunicorn ${DJANGO_WSGI_MODULE:-app.wsgi}:application -c gunicorn.conf.py
