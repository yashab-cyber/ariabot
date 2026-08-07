"""
Main Entry point for running Aria Discord Bot.
"""
import sys
import asyncio
from bot.client import bot
from bot.config.settings import settings
from bot.utils.logger import logger


def main():
    if settings.DISCORD_TOKEN == "mock_token_for_testing" or not settings.DISCORD_TOKEN:
        logger.warning("DISCORD_TOKEN is not configured in .env file. Running in dry-run mode.")
        print("Please configure DISCORD_TOKEN in .env to connect to Discord.")
        return

    try:
        bot.run(settings.DISCORD_TOKEN)
    except Exception as e:
        logger.critical(f"Bot execution failed: {e}")


if __name__ == "__main__":
    main()
