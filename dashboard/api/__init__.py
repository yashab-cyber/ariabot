from dashboard.api.stats import router as stats_router
from dashboard.api.settings import router as settings_router
from dashboard.api.logs import router as logs_router

__all__ = ["stats_router", "settings_router", "logs_router"]
