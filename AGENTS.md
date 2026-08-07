# 🤖 AGENTS.md — Developer & AI Agent Guide for AriaBot

> **Note**: This file mirrors [`AGENT.md`](file:///workspaces/ariabot/AGENT.md).

Please refer to [`AGENT.md`](file:///workspaces/ariabot/AGENT.md) for the complete, authoritative guide for AI coding agents and developers working on **AriaBot**.

---

## Quick Reference Summary

- **Framework**: `discord.py` 2.x + `FastAPI` + `SQLAlchemy 2.0` (Async)
- **Database Access**: Repository pattern ONLY (`bot/database/repositories/`)
- **Plugin System**: 17 Cogs under `bot/cogs/` loaded dynamically in [`bot/client.py`](file:///workspaces/ariabot/bot/client.py)
- **Run Bot**: `python -m bot.main`
- **Run Dashboard**: `uvicorn dashboard.app:app --port 8000 --reload`
- **Run Tests**: `pytest`
- **Logging**: Use `from bot.utils.logger import logger` (Never `print()`)
