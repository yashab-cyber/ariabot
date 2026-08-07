"""
Dashboard Logs REST API.
"""
from fastapi import APIRouter
from pathlib import Path

router = APIRouter(prefix="/api/logs", tags=["Logs"])


@router.get("")
async def get_recent_logs():
    log_path = Path("logs/aria.log")
    if not log_path.exists():
        return {"logs": ["No log file found."]}

    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return {"logs": lines[-100:]}
