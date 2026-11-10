#!/usr/bin/env bash
set -e

echo "=== Setting up OCI ARM Catcher Dashboard API Service ==="

if ! sudo test -f /etc/catcher-api.env; then
    echo "Create /etc/catcher-api.env with DASHBOARD_API_KEY first (see README.md)." >&2
    exit 1
fi

APP_DIR="/home/ubuntu/oci-arm-dashboard-backend"
mkdir -p "$APP_DIR"
cp "$(dirname "$0")/main.py" "$APP_DIR/"
cp "$(dirname "$0")/requirements.txt" "$APP_DIR/"

sudo apt update && sudo apt install -y python3-pip python3-venv

python3 -m venv "$APP_DIR/venv"
"$APP_DIR/venv/bin/pip" install --upgrade pip
"$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt"

# Create systemd service
cat <<EOF | sudo tee /etc/systemd/system/catcher-api.service
[Unit]
Description=OCI ARM Catcher Dashboard API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=$APP_DIR
EnvironmentFile=/etc/catcher-api.env
ExecStart=$APP_DIR/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Open firewall port 8000 on iptables if needed (Ubuntu cloud image uses iptables)
sudo iptables -I INPUT -p tcp --dport 8000 -j ACCEPT 2>/dev/null || true

sudo systemctl daemon-reload
sudo systemctl enable catcher-api
sudo systemctl restart catcher-api

echo "=== Service catcher-api is running on port 8000! ==="
curl -s http://localhost:8000/api/health
echo ""
