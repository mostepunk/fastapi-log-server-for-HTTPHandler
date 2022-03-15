from fastapi.routing import APIRouter
from app.core.settings import app_settings

from app.api import default

# === TAGS ===
PROD = app_settings.TAG_PROD
DEV = app_settings.TAG_DEV

# === DEVELOP ===
dev = APIRouter()
for app in app_settings.APPS:
    dev.include_router(default.router, prefix=f'/{app}', tags=[DEV, app])

# === PROD ===
prod = APIRouter()
for app in app_settings.APPS:
    prod.include_router(default.router, prefix=f'/{app}', tags=[PROD, app])
