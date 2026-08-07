"""
FastAPI Dashboard Backend Application.
Serves REST API, WebSockets, and static frontend dashboard.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from dashboard.api import stats_router, settings_router, logs_router
from bot.config.settings import settings

app = FastAPI(
    title="Aria Discord Bot Dashboard",
    description="Control Panel & REST API for OpenDroid Aria AI Bot",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stats_router)
app.include_router(settings_router)
app.include_router(logs_router)

# Mount static frontend files
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("dashboard.app:app", host=settings.DASHBOARD_HOST, port=settings.DASHBOARD_PORT, reload=True)
