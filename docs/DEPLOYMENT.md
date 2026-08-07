# 🚀 Production Deployment Guide for Aria

This guide details deployment procedures for **Aria** across various cloud and infrastructure environments.

---

## 🐳 Option 1: Docker & Docker Compose (Recommended)

Running Aria with Docker Compose provisions the complete stack including **Aria Bot**, **FastAPI Dashboard**, **PostgreSQL 16**, and **Redis 7**.

### Steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/opendroid/ariabot.git
   cd ariabot
   ```

2. **Configure Production Environment**:
   ```bash
   cp .env.example .env
   # Open .env and set your production DISCORD_TOKEN, SECRET_KEY, and API Keys
   nano .env
   ```

3. **Start the Stack**:
   ```bash
   docker-compose up -d --build
   ```

4. **Verify Container Status**:
   ```bash
   docker-compose ps
   ```

5. **Monitor Logs**:
   ```bash
   # Bot logs
   docker-compose logs -f bot

   # Dashboard logs
   docker-compose logs -f dashboard
   ```

---

## ☁️ Option 2: Linux VPS (Ubuntu 22.04 / 24.04 LTS)

### 1. Install System Dependencies:
```bash
sudo apt update && sudo apt install -y python3.12 python3.12-venv git redis-server postgresql postgresql-contrib
```

### 2. Configure PostgreSQL Database:
```bash
sudo -u postgres psql -c "CREATE DATABASE ariabot;"
sudo -u postgres psql -c "CREATE USER aria WITH PASSWORD 'your_secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ariabot TO aria;"
```

### 3. Setup Project & Virtual Environment:
```bash
sudo git clone https://github.com/opendroid/ariabot.git /opt/ariabot
cd /opt/ariabot
sudo python3.12 -m venv venv
sudo /opt/ariabot/venv/bin/pip install --upgrade pip
sudo /opt/ariabot/venv/bin/pip install -r requirements.txt
```

### 4. Create Systemd Service for Bot (`/etc/systemd/system/aria-bot.service`):
```ini
[Unit]
Description=Aria AI Discord Bot Service
After=network.target postgresql.service redis-server.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/ariabot
EnvironmentFile=/opt/ariabot/.env
ExecStart=/opt/ariabot/venv/bin/python bot/main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 5. Create Systemd Service for Dashboard (`/etc/systemd/system/aria-dashboard.service`):
```ini
[Unit]
Description=Aria FastAPI Web Dashboard Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/ariabot
EnvironmentFile=/opt/ariabot/.env
ExecStart=/opt/ariabot/venv/bin/uvicorn dashboard.app:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 6. Enable and Start Services:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now aria-bot
sudo systemctl enable --now aria-dashboard
```

---

## 🌩️ Option 3: PaaS Deployments (Railway, Render, Fly.io)

### Railway Deployment:
1. Connect your GitHub repository to **Railway**.
2. Add a **PostgreSQL** and **Redis** database plugin to your project.
3. Railway automatically detects the `Dockerfile`.
4. Set `DISCORD_TOKEN`, `OPENAI_API_KEY`, etc. in the Railway variables tab.

### Render Deployment:
1. Create a new **Web Service** pointing to your repository.
2. Select **Docker** environment.
3. Add Environment Variables under Service Settings.

---

## 💾 Database Backup & Maintenance

To create an automated database backup of PostgreSQL:

```bash
pg_dump -U aria -h localhost ariabot > aria_backup_$(date +%Y%m%m).sql
```
