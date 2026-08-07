# 📖 Aria Command Reference

Complete list of slash commands available in **Aria**.

---

## 🤖 AI Assistant (`cogs/ai`)
- `/ask <question>` — Ask Aria any question.
- `/chat <message>` — Interactive conversation.
- `/explain <concept>` — Explain technical concepts simply.
- `/debug <code_or_error>` — Debug code or stack trace errors.
- `/fix <code>` — Automatically fix errors in code.
- `/review <code>` — Comprehensive code review.
- `/code <requirement>` — Generate clean production code.
- `/translate <target_language> <text>` — Translate text into any language.
- `/summarize <text>` — Provide bulleted summaries.
- `/rewrite <text> [tone]` — Rewrite text with custom tone.
- `/grammar <text>` — Check grammar & spelling.
- `/brainstorm <topic>` — Generate innovative ideas.
- `/ai_reset` — Clear active conversation memory.

---

## 🛡️ Moderation (`cogs/moderation`)
- `/warn <user> <reason>` — Issue a formal warning.
- `/warnings <user>` — View warning history.
- `/timeout <user> <minutes> [reason]` — Apply temp timeout.
- `/unmute <user> [reason]` — Remove timeout.
- `/kick <user> [reason]` — Kick member.
- `/ban <user> [reason]` — Ban member.
- `/softban <user> [reason]` — Ban and unban to purge messages.
- `/unban <user_id> [reason]` — Unban user by ID.
- `/cases <user>` — View moderation cases history.

---

## 👋 Welcome & Verification (`cogs/welcome`, `cogs/verification`)
- `/setup_welcome <channel> [message]` — Configure welcome embed.
- `/setup_verification <role> [type]` — Deploy captcha/button verification panel.

---

## 📩 Ticket System (`cogs/tickets`)
- `/setup_tickets <category>` — Deploy ticket launch panel.

---

## 📊 Polls & Suggestions (`cogs/polls`, `cogs/suggestions`)
- `/poll <question> <option_1> <option_2> ...` — Create interactive poll.
- `/setup_suggestions <channel>` — Set community suggestions channel.
- `/suggest <idea>` — Submit a community suggestion.

---

## 📈 Leveling & Economy (`cogs/leveling`, `cogs/economy`)
- `/rank [user]` — Display rank card and XP progress.
- `/leaderboard` — View server XP leaderboard.
- `/balance [user]` — Check wallet & bank balance.
- `/daily` — Claim daily coin reward.
- `/coinflip <heads|tails> <bet>` — Bet coins on a coin flip.

---

## ⏰ Reminders & Community (`cogs/reminders`, `cogs/community`)
- `/remind <minutes> <message>` — Set a scheduled reminder.
- `/reminders` — List active scheduled reminders.
- `/faq [topic]` — Search community knowledge base.
- `/announce <channel> <title> <message>` — Post official announcement.

---

## 🛠️ Utility & Fun (`cogs/utility`, `cogs/fun`)
- `/help` — Interactive paginated help directory.
- `/ping` — View WebSocket latency.
- `/botinfo` — System specs, uptime, and stats.
- `/userinfo [user]` — View member profile details.
- `/serverinfo` — View guild details.
- `/8ball <question>` — Magic 8-Ball response.
- `/dice [sides]` — Roll a die.
- `/joke` — Get a tech joke.
- `/fact` — Get a random coding fact.

---

## 🔐 Owner Panel (`cogs/owner`)
- `/reload <extension>` — Dynamic cog hot-reload.
- `/maintenance <enabled>` — Toggle maintenance mode.
- `/broadcast <message>` — System announcement broadcast.
- `/clear_cache` — Flush Redis and in-memory cache.
- `/health` — Server health metrics.
