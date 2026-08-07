# 🤖 AGENT.md — Developer & AI Agent Guide for AriaBot

Welcome to **AriaBot**! This document serves as the authoritative guide for AI coding agents (such as Antigravity, Cursor, Windsurf, Claude Code, GitHub Copilot) and human developers working on this repository.

---

## 📌 1. Repository Overview & Architecture

**AriaBot** is an enterprise-grade, asynchronous, modular AI-powered Discord Assistant and Web Management Platform built for community management, AI software engineering assistance, support tickets, leveling, economy, and server security for the **OpenDroid Community**.

### Tech Stack
- **Language & Runtime**: Python 3.12+
- **Discord Framework**: `discord.py` 2.x (`discord.ext.commands` & `app_commands`)
- **Web Dashboard & API**: `FastAPI` + `Uvicorn` + `Jinja2`
- **Database & ORM**: `SQLAlchemy 2.0` (Async) with `aiosqlite` (SQLite default) or `asyncpg` (PostgreSQL production)
- **Cache**: `Redis` (with graceful in-memory fallback)
- **Configuration & Validation**: `Pydantic 2.x` & `pydantic-settings`
- **Testing**: `pytest` & `pytest-asyncio`
- **Code Quality**: `ruff`, `black`, `mypy`

---

## 📁 2. Project Directory Layout

```
ariabot/
├── .github/
│   └── workflows/
│       └── ci.yml                   # CI pipeline (Ruff linting, Pytest execution)
├── bot/
│   ├── client.py                    # Main AriaBot class subclassing commands.Bot
│   ├── main.py                      # CLI entry point to launch the bot
│   ├── config/
│   │   └── settings.py              # Pydantic Settings configuration manager
│   ├── database/
│   │   ├── connection.py            # Async SQLAlchemy engine & session factory
│   │   ├── models/                  # SQLAlchemy ORM models (Guild, User, Mod, Ticket, etc.)
│   │   └── repositories/            # Type-safe Repository Pattern CRUD abstraction
│   ├── services/                    # Decoupled core services (AI, Cache, Captcha, Transcript, Scheduler)
│   ├── views/                       # Interactive Discord UI components (Buttons, Modals, Selects)
│   ├── utils/                       # Structured logger and formatting utilities
│   └── cogs/                        # 17 Feature Plugin Modules (AI, Mod, Leveling, Economy, etc.)
├── dashboard/
│   ├── app.py                       # FastAPI Backend Application entry point
│   ├── auth.py                      # Discord OAuth2 Authentication handler
│   ├── api/                         # REST API endpoints (Stats, Settings, Logs)
│   ├── static/                      # CSS/JS assets for glassmorphic management UI
│   └── templates/                   # Jinja2 HTML templates for Web Dashboard
├── docs/                            # Architectural specs and system documentation
├── tests/                           # Async pytest suite
├── .env.example                     # Environment variable template
├── Dockerfile                       # Container definition
├── docker-compose.yml               # Multi-container setup (Bot + Dashboard + Redis)
├── pyproject.toml                   # Project metadata, linters, and pytest options
└── requirements.txt                 # Dependencies specification
```

---

## 🛠️ 3. Quickstart & Command Reference

### Environment Setup
```bash
# Create and activate Python 3.12 virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Services
```bash
# 1. Run the Discord Bot
python -m bot.main

# 2. Run the Web Dashboard
uvicorn dashboard.app:app --host 0.0.0.0 --port 8000 --reload
```

### Running Tests & Linting
```bash
# Run test suite
pytest

# Run tests with verbose output
pytest -v

# Run linting and code quality checks
ruff check .
black --check .
mypy bot
```

### Docker Operations
```bash
# Build and launch all services with Docker Compose
docker compose up -d --build

# View container logs
docker compose logs -f bot
```

---

## 📐 4. Core Software Engineering Patterns & Rules

When modifying or adding code in this repository, agents MUST strictly adhere to these patterns:

### A. Asynchronous Execution (Non-Blocking I/O)
- **Discord Main Loop Safety**: Never perform blocking I/O (e.g., synchronous `requests`, `time.sleep()`, synchronous DB calls) inside async functions or event handlers.
- **Async Drivers**: Use `aiohttp` for HTTP calls, `asyncio.sleep()` for delays, and async SQLAlchemy sessions for database queries.

### B. Database Access via Repository Pattern
- **Repository Abstraction**: All database interactions MUST go through the repositories in `bot/database/repositories/`.
- **No Direct Sessions in Cogs**: Do NOT instantiate raw DB sessions or execute raw SQL queries inside cogs or UI views.
- **Example Usage**:
  ```python
  from bot.database.repositories.user_repo import UserRepo

  async with UserRepo() as repo:
      user = await repo.get_or_create_user(discord_id=user_id, guild_id=guild_id)
  ```

### C. Feature Isolation in Cogs
- Every feature module resides in `bot/cogs/<module>/<module>_cog.py`.
- Each cog inherits from `discord.ext.commands.Cog`.
- Keep cogs decoupled. If shared business logic is needed, place it in `bot/services/`.

### D. Structured Logging
- Do NOT use plain `print()` statements.
- Always use the centralized logger from `bot.utils.logger`:
  ```python
  from bot.utils.logger import logger

  logger.info("User %s triggered command %s", user_id, command_name)
  logger.error("Failed to process transaction: %s", str(err), exc_info=True)
  ```

### E. Configuration & Environment Variables
- All configurations MUST be defined in `bot/config/settings.py` using Pydantic `BaseSettings`.
- Access settings via `from bot.config.settings import settings`.
- Environment variables are sourced from `.env`. Never hardcode secrets or keys.

---

## 🚨 5. AI Agent Guardrails & Mandatory Guidelines

1. **Verify Before Concluding**: Always run `pytest` after making code modifications. Never declare success without empirical confirmation that tests pass.
2. **Preserve API Contracts**: When editing repository methods or service signatures, audit all call sites across `bot/cogs/` and `dashboard/` to prevent signature mismatches.
3. **Graceful Error Handling in Discord Interactions**:
   - Always catch known exceptions in slash command handlers.
   - Respond to users with descriptive `discord.Embed` messages.
   - Use `ephemeral=True` for error notifications when appropriate.
4. **Clean Git Hygiene & Formatting**:
   - Ensure code is compliant with Black line length (120 chars) and Ruff rules.
   - Preserve existing docstrings and type annotations.

---

## 🧩 6. Creating a New Cog — Step-by-Step Template

When creating a new feature module (e.g., `bot/cogs/myfeature/myfeature_cog.py`), follow this template:

```python
import discord
from discord import app_commands
from discord.ext import commands
from bot.utils.logger import logger


class MyFeatureCog(commands.Cog):
    """Description of MyFeature cog functionality."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="mycommand", description="Sample feature command")
    async def my_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            embed = discord.Embed(
                title="✨ Feature Output",
                description="Successfully executed feature action!",
                color=0x5865F2,
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Error in mycommand: {e}", exc_info=True)
            await interaction.followup.send("❌ An unexpected error occurred.", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(MyFeatureCog(bot))
```

To register the new cog, append `"bot.cogs.myfeature.myfeature_cog"` to `self.initial_cogs` in [bot/client.py](file:///workspaces/ariabot/bot/client.py).

---

## 🧪 7. Test Strategy & Guidelines

- **Location**: All unit and integration tests reside in `tests/`.
- **Framework**: `pytest` with `pytest-asyncio`.
- **Database Testing**: Tests use an in-memory SQLite database setup via async fixtures.
- **Rule**: When adding new functionality to `repositories` or `services`, add corresponding test functions in `tests/`.
