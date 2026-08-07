import pytest
from bot.client import bot


def test_bot_initialization():
    assert bot.command_prefix == "!"
    assert len(bot.initial_cogs) == 17

