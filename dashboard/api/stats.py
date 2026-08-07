"""
Dashboard Statistics REST API.
"""
from fastapi import APIRouter
import psutil
from bot.client import bot

router = APIRouter(prefix="/api/stats", tags=["Stats"])


@router.get("")
async def get_stats():
    return {
        "status": "online",
        "guilds_count": len(bot.guilds),
        "total_users": sum(g.member_count for g in bot.guilds if g.member_count),
        "latency_ms": round(bot.latency * 1000) if bot.is_ready() else 0,
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "maintenance_mode": getattr(bot, "maintenance_mode", False),
    }
