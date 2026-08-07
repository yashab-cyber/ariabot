# 🤖 Aria — Official AI Discord Bot for OpenDroid Community

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12%2B-blue?style=for-the-badge&logo=python" alt="Python 3.12+">
  <img src="https://img.shields.io/badge/discord.py-2.x-5865F2?style=for-the-badge&logo=discord" alt="discord.py">
  <img src="https://img.shields.io/badge/FastAPI-Dashboard-009688?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker" alt="Docker">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License MIT">
</p>

**Aria** is an enterprise-grade, modern, fully asynchronous, modular AI-powered Discord assistant built for community management, AI code & text assistance, support tickets, leveling, economy, and server security.

---

## ✨ Features Overview

- 🤖 **AI Assistant**: Multi-provider support (OpenAI, Anthropic Claude, Google Gemini, Groq, OpenRouter, Ollama, LM Studio), context memory, code streaming, bug fixing, reviews, translation, and topic classification.
- 🛡️ **Moderation & AutoMod**: Anti-invite links, mass mentions, bad words filtering, warnings, strikes, temporary mutes, kicks, softbans, bans, cases history, and mod notes.
- 👋 **Onboarding & Welcome**: Dynamic animated embeds, custom goodbye alerts, auto-roles, DM welcome messages.
- 🔒 **Security Verification**: Pillow-generated image Captchas and button verification to protect against raid bots & alt accounts.
- 📩 **Support Ticket System**: Category dropdowns, claim ticket, ticket closure, auto HTML transcript generator, and user feedback ratings.
- 📊 **Polls & Suggestions**: Interactive voting buttons, poll option analytics, community suggestions with staff review modals.
- 📈 **Leveling & Economy**: Chat XP, levels, rank cards, leaderboards, daily rewards, wallet/bank balances, and coin flip games.
- ⏰ **Reminders & Scheduler**: One-time and recurring scheduled reminders delivered via DM or server.
- 🎛️ **Owner Control Panel**: Dynamic cog hot-reloading, maintenance mode toggle, server announcements broadcast, cache flushing, and system metrics.
- 🌐 **Web Dashboard**: FastAPI REST API backend with a dark, glassmorphic responsive frontend for live server settings management and system log streaming.

---

## 📁 Repository Structure

```
ariabot/
├── bot/
│   ├── client.py                 # Core AriaBot client
│   ├── main.py                   # Entry point
│   ├── config/                   # Pydantic Settings
│   ├── database/                 # Async SQLAlchemy Models & Repositories
│   ├── services/                 # AI, Cache, Captcha, Transcript, Scheduler Services
│   ├── views/                    # Discord UI Views, Buttons, Dropdowns, Modals
│   ├── utils/                    # Structured Logger, Formatters
│   └── cogs/                     # 16 Isolated Feature Plugins (Cogs)
├── dashboard/                    # FastAPI Backend & Web Dashboard Frontend
├── tests/                        # Pytest Test Suite
├── docs/                         # Architecture, Command Index, Deployment Guides
├── Dockerfile                    # Production Docker Build
├── docker-compose.yml            # Multi-container Compose (PostgreSQL, Redis, Bot, Dashboard)
├── requirements.txt
└── README.md
```

---

## ⚡ Quick Start

### 1. Installation

```bash
git clone https://github.com/opendroid/ariabot.git
cd ariabot

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy `.env.example` to `.env` and fill in your Discord Bot Token and API keys:

```bash
cp .env.example .env
```

### 3. Running Aria Bot & Dashboard

Run the bot:
```bash
python bot/main.py
```

Run the dashboard:
```bash
uvicorn dashboard.app:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🐳 Docker Deployment

Run the complete production stack (PostgreSQL + Redis + Bot + Dashboard):

```bash
docker-compose up -d --build
```

---

## 🧪 Testing

Run pytest test suite:

```bash
pytest
```

---

## 📄 Documentation Links

- 📄 [Usage Guide, PRD & TRD Document](docs/USAGE.md)
- 📖 [Complete Slash Command Index](docs/COMMANDS.md)
- 🏗️ [Technical Architecture Guide](docs/ARCHITECTURE.md)
- 🚀 [Deployment Guide](docs/DEPLOYMENT.md)

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).