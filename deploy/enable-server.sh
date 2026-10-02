#!/usr/bin/env bash
# Run as the Ubuntu account that cloned VODA and created its administrator.
set -euo pipefail

if [[ "$EUID" -eq 0 ]]; then
  echo 'Run this script as your normal SSH user, without sudo.' >&2
  exit 1
fi

site="${1:-voda-run.duckdns.org}"
if [[ ! "$site" =~ ^[a-z0-9]([a-z0-9.-]*[a-z0-9])?$ || "$site" != *.* ]]; then
  echo 'A valid lowercase domain name is required.' >&2
  exit 1
fi

app_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$app_dir"
if [[ "$app_dir" =~ [[:space:]\%\"\\] ]]; then
  echo 'Install VODA in a path without spaces, percent signs, quotes or backslashes.' >&2
  exit 1
fi
test -x .venv/bin/python
command -v caddy >/dev/null
test -f data/voda.sqlite3
.venv/bin/python - <<'PY'
import sqlite3
with sqlite3.connect('file:data/voda.sqlite3?mode=ro', uri=True) as db:
    if not db.execute('SELECT 1 FROM admins LIMIT 1').fetchone():
        raise SystemExit('Create an administrator with manage.py create-admin first.')
PY

sudo -v
server_user="$(id -un)"
config_stamp="$(date -u +%Y%m%dT%H%M%S)-$$"
if sudo test -f /etc/systemd/system/voda.service; then
  sudo cp -p /etc/systemd/system/voda.service "/etc/systemd/system/voda.service.backup-$config_stamp"
fi
if sudo test -f /etc/caddy/Caddyfile; then
  sudo cp -p /etc/caddy/Caddyfile "/etc/caddy/Caddyfile.backup-$config_stamp"
fi
chmod 700 "$app_dir/data"

sudo tee /etc/systemd/system/voda.service >/dev/null <<EOF
[Unit]
Description=VODA FastAPI website
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$server_user
WorkingDirectory=$app_dir
Environment=VODA_DATA_DIR=$app_dir/data
Environment=VODA_HTTPS=1
Environment=PYTHONDONTWRITEBYTECODE=1
ExecStart=$app_dir/.venv/bin/python -m uvicorn server:app --host 127.0.0.1 --port 8000 --proxy-headers --forwarded-allow-ips=127.0.0.1 --no-access-log
Restart=on-failure
RestartSec=5
UMask=0077
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=$app_dir/data

[Install]
WantedBy=multi-user.target
EOF

sudo tee /etc/caddy/Caddyfile >/dev/null <<EOF
$site {
    reverse_proxy 127.0.0.1:8000
}
EOF

sudo caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
sudo systemd-analyze verify /etc/systemd/system/voda.service
sudo systemctl daemon-reload
sudo systemctl enable voda.service caddy.service
sudo systemctl restart voda.service

.venv/bin/python - <<'PY'
import time
import urllib.request
for attempt in range(30):
    try:
        with urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=2) as response:
            if response.status == 200:
                print('VODA backend health: OK')
                break
    except OSError:
        time.sleep(1)
else:
    raise SystemExit('Backend did not start. Check: sudo journalctl -u voda -n 40 --no-pager')
PY

sudo systemctl restart caddy.service
sudo systemctl is-active voda.service caddy.service
echo "Services started. Caddy is obtaining the HTTPS certificate."
echo "Website: https://$site"
echo "Admin: https://$site/admin.html"
echo 'If HTTPS is not ready, check: sudo journalctl -u caddy -n 40 --no-pager'
