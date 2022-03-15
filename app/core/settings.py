from typing import List, Optional, Any
from pydantic import BaseSettings, validator, root_validator
from pydantic import SecretStr


class AppSettings(BaseSettings):
    PROJECT_NAME: str = "FastAPI example application"
    VERSION: str = "0.0.1"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    ALLOWED_HOSTS: List[str] = ["*"]
    DOCS: str = "/docs"
    REDOC: str = "/redoc"
    APPS: Any
    # Tags
    TAG_PROD: str = "prod"
    TAG_DEV: str = "dev"
    # Prefix
    PREFIX_PROD: str = "/prod"
    PREFIX_DEV: str = "/dev"

    @validator('APPS', pre=True)
    def validate_apps(cls, apps):
        apps = apps.split(',')
        return [app.strip() for app in apps]

    @validator(
        'PREFIX_PROD',
        'PREFIX_DEV',
        pre=True
    )
    def validate_prod_prefix(cls, prefix):
        if not prefix.startswith('/') and prefix.endswith('/'):
            return '/' + prefix.rstrip('/')

        if prefix.endswith('/'):
            return prefix.rstrip('/')

        if not prefix.startswith('/'):
            return '/' + prefix

        return prefix


class LogSettings(BaseSettings):
    WHEN: str = "D"
    INTERVAL: int = 1
    BACKUP_COUNT: int = 7
    AT_TIME: str = "midnight"
    FORMAT: str = "%(asctime)s : %(levelname)s : %(message)s"
    ROOT: str = "/logs"

    class Config:
        env_prefix = "LOG_"
        env_file_encoding = "utf-8"


app_settings = AppSettings()
log_settings = LogSettings()
