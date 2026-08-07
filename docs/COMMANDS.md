# 📖 Aria Complete Slash Command Reference

This document provides a comprehensive, production-grade specification for every slash command available in **Aria**.

---

## 🤖 AI Assistant Module (`bot/cogs/ai/ai_cog.py`)

| Command | Arguments | Permission | Description |
|---|---|---|---|
| `/ask` | `question: str` | Everyone | Ask Aria AI any question with automatic topic classification. |
| `/chat` | `message: str` | Everyone | Have a multi-turn interactive conversation with Aria. |
| `/explain` | `concept: str` | Everyone | Explain a complex technical concept or code snippet simply. |
| `/debug` | `code_or_error: str` | Everyone | Analyze stack traces or code to identify bugs and solutions. |
| `/fix` | `code: str` | Everyone | Automatically fix syntax and logical errors in code snippets. |
| `/review` | `code: str` | Everyone | Perform a comprehensive code review (security, performance). |
| `/code` | `requirement: str` | Everyone | Generate clean, production-ready code with type annotations. |
| `/translate` | `target_language: str, text: str` | Everyone | Translate text into any specified language. |
| `/summarize` | `text: str` | Everyone | Generate concise bulleted summaries of long text or articles. |
| `/rewrite` | `text: str, tone: str (optional)` | Everyone | Rewrite text for a specific tone (professional, casual, etc.). |
| `/grammar` | `text: str` | Everyone | Correct grammar, spelling, and punctuation errors. |
| `/brainstorm` | `topic: str` | Everyone | Generate innovative ideas for a project or topic. |
| `/ai_reset` | *None* | Everyone | Clear your active conversation memory for the channel. |
| `/ai_provider` | `provider: str` | Everyone | Set preferred AI provider (OpenAI, Anthropic, Groq, OpenRouter, Ollama). |
| `/ai_model` | `model_name: str` | Everyone | Set preferred AI model name (e.g. gpt-4o, claude-3-5-sonnet). |

---

## 🛡️ Moderation & AutoMod (`bot/cogs/moderation/moderation_cog.py`)

| Command | Arguments | Permission | Description |
|---|---|---|---|
| `/warn` | `user: Member, reason: str` | `Manage Messages` | Issue a formal warning to a user and log Case. |
| `/warnings` | `user: Member` | `Manage Messages` | View all historical warnings for a specific user. |
| `/timeout` | `user: Member, minutes: int, reason: str` | `Moderate Members` | Apply temporary mute/timeout to a user. |
| `/unmute` | `user: Member, reason: str` | `Moderate Members` | Remove active timeout from a user. |
| `/kick` | `user: Member, reason: str` | `Kick Members` | Kick a member from the server. |
| `/ban` | `user: Member, reason: str` | `Ban Members` | Ban a member permanently from the server. |
| `/softban` | `user: Member, reason: str` | `Ban Members` | Ban and immediately unban to purge recent messages. |
| `/unban` | `user_id: str, reason: str` | `Ban Members` | Remove ban for a user by User ID. |
| `/cases` | `user: Member` | `Manage Messages` | View all moderation cases (warns, mutes, bans) for a user. |
| `/modnotes` | `user: Member, note: str` | `Manage Messages` | Add a staff private note for a user. |
| `/appeal` | `case_number: int, explanation: str` | Everyone | Submit a moderation appeal for review. |

---

## 👋 Welcome & Onboarding (`bot/cogs/welcome/welcome_cog.py`)

| Command | Arguments | Permission | Description |
|---|---|---|---|
| `/setup_welcome` | `channel: TextChannel, message: str` | `Administrator` | Configure server welcome channel and message template. |

---

## 🛡️ Security Verification (`bot/cogs/verification/verification_cog.py`)

| Command | Arguments | Permission | Description |
|---|---|---|---|
| `/setup_verification` | `role: Role, verification_type: str` | `Administrator` | Deploy Pillow image Captcha or Button verification panel. |

---

## 📩 Ticket Support System (`bot/cogs/tickets/tickets_cog.py`)

| Command | Arguments | Permission | Description |
|---|---|---|---|
| `/setup_tickets` | `category: CategoryChannel` | `Administrator` | Deploy support ticket launch panel under specified category. |
| `/ticket_add` | `user: Member` | `Manage Messages` | Add a member to an active support ticket channel. |
| `/ticket_remove` | `user: Member` | `Manage Messages` | Remove a member from an active support ticket channel. |

---

## 🎭 Reaction Roles (`bot/cogs/roles/reaction_roles_cog.py`)

| Command | Arguments | Permission | Description |
|---|---|---|---|
| `/setup_reaction_roles` | `title: str, role_1: Role, role_2..5: Role` | `Administrator` | Deploy an interactive role assignment dropdown panel. |

---

## 📊 Poll System (`bot/cogs/polls/polls_cog.py`)

| Command | Arguments | Permission | Description |
|---|---|---|---|
| `/poll` | `question: str, option_1..5: str, anonymous: bool` | Everyone | Create an interactive button-based poll with live results. |

---

## 💡 Suggestions System (`bot/cogs/suggestions/suggestions_cog.py`)

| Command | Arguments | Permission | Description |
|---|---|---|---|
| `/setup_suggestions` | `channel: TextChannel` | `Administrator` | Set the target channel for community suggestions. |
| `/suggest` | `idea: str` | Everyone | Submit a suggestion for community upvoting and staff review. |

---

## 📈 Leveling & XP (`bot/cogs/leveling/leveling_cog.py`)

| Command | Arguments | Permission | Description |
|---|---|---|---|
| `/rank` | `user: Member (optional)` | Everyone | Display current level, XP, prestige, and progress bar. |
| `/leaderboard` | *None* | Everyone | Display top 10 server XP leaderboard. |
| `/prestige` | *None* | Everyone | Reset level 50+ to earn +1 Prestige rank. |

---

## 💰 Economy System (`bot/cogs/economy/economy_cog.py`)

| Command | Arguments | Permission | Description |
|---|---|---|---|
| `/balance` | `user: Member (optional)` | Everyone | Check wallet and bank balance. |
| `/daily` | *None* | Everyone | Claim daily coin reward with streak multiplier. |
| `/coinflip` | `choice: str (heads/tails), bet: int` | Everyone | Gamble coins on a coin flip game. |
| `/pay` | `recipient: Member, amount: int` | Everyone | Transfer coins to another community member. |
| `/shop` | *None* | Everyone | Browse items available in the community shop. |
| `/inventory` | *None* | Everyone | View your owned badges and items. |

---

## ⏰ Reminders & Scheduler (`bot/cogs/reminders/reminders_cog.py`)

| Command | Arguments | Permission | Description |
|---|---|---|---|
| `/remind` | `minutes: int, message: str` | Everyone | Schedule a reminder delivered via DM. |
| `/reminders` | *None* | Everyone | View your active scheduled reminders. |

---

## 📢 Community Management (`bot/cogs/community/community_cog.py`)

| Command | Arguments | Permission | Description |
|---|---|---|---|
| `/faq` | `query: str (optional)` | Everyone | Search or list community knowledge base topics. |
| `/announce` | `channel: TextChannel, title: str, message: str` | `Administrator` | Broadcast an official server announcement embed. |

---

## 🛠️ Utility Commands (`bot/cogs/utility/utility_cog.py`)

| Command | Arguments | Permission | Description |
|---|---|---|---|
| `/ping` | *None* | Everyone | Check bot WebSocket latency in milliseconds. |
| `/botinfo` | *None* | Everyone | View system stats, Python version, CPU, and RAM metrics. |
| `/userinfo` | `member: Member (optional)` | Everyone | View account creation, join date, and roles for a member. |
| `/serverinfo` | *None* | Everyone | Display guild owner, member count, and channel statistics. |
| `/help` | *None* | Everyone | Open interactive paginated command directory. |

---

## 🎲 Fun & Entertainment (`bot/cogs/fun/fun_cog.py`)

| Command | Arguments | Permission | Description |
|---|---|---|---|
| `/8ball` | `question: str` | Everyone | Ask the Magic 8-Ball a question. |
| `/dice` | `sides: int (optional)` | Everyone | Roll a die (default 6 sides). |
| `/joke` | *None* | Everyone | Get a random tech or programming joke. |
| `/fact` | *None* | Everyone | Get a random coding or technology fact. |

---

## 📈 Analytics (`bot/cogs/analytics/analytics_cog.py`)

| Command | Arguments | Permission | Description |
|---|---|---|---|
| `/analytics` | *None* | `Manage Guild` | View real-time server activity overview and system health. |

---

## 🔐 Owner Controls (`bot/cogs/owner/owner_cog.py`)

| Command | Arguments | Permission | Description |
|---|---|---|---|
| `/reload` | `extension: str` | Bot Owner / Guild Owner | Hot-reload a cog/plugin without restarting process. |
| `/maintenance` | `enabled: bool` | Bot Owner / Guild Owner | Toggle global bot maintenance mode. |
| `/broadcast` | `message: str` | Bot Owner / Guild Owner | Broadcast a message to all connected server system channels. |
| `/clear_cache` | *None* | Bot Owner / Guild Owner | Flush all in-memory and Redis cache entries. |
| `/health` | *None* | Bot Owner / Guild Owner | Detailed system health metrics (CPU, RAM, Uptime). |
