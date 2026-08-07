# 🚀 Deploying Aria AI Discord Bot

This guide provides instructions for deploying **Aria** across various hosting environments.

---

## 🐳 Option 1: Docker & Docker Compose (Recommended)

The easiest and most reliable way to run Aria in production (with PostgreSQL & Redis) is using Docker Compose.

### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/opendroid/ariabot.git
   cd ariabot
   ```

2. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and set DISCORD_TOKEN, API keys, etc.
   ```

3. Launch services:
   ```bash
   docker-compose up -d --build
   ```

4. Check logs:
   ```bash
   docker-compose logs -f bot
   ```

---

## ☁️ Option 2: VPS (Ubuntu / Debian Linux)

### 1. Install Dependencies:
```bash
sudo apt update && sudo apt install -y python3.12 python3.12-venv git redis-server
```

### 2. Setup Virtual Environment:
```bash
git clone https://github.com/opendroid/ariabot.git /opt/ariabot
cd /opt/ariabot
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Create Systemd Service (`/etc/systemd/system/aria.service`):
```ini
[Unit]
Description=Aria AI Discord Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/ariabot
ExecStart=/opt/ariabot/venv/bin/python bot/main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now aria
```

---

## 🌩️ Cloud Hosting (Railway, Render, Fly.io)

### Railway / Render:
1. Connect your GitHub repository to Railway or Render.
2. Set Environment Variables in the service settings dashboard.
3. Railway/Render will automatically pick up the `Dockerfile`.
