from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.cache.persistence.memory_persistence import MemoryPersistence
from app.cache.persistence.persistence import Persistence


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.local", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    cache_enabled: bool = True
    persistence: Persistence = MemoryPersistence()
    yf_impersonation_mode: Literal["auto", "chrome", "firefox", "none"] = "auto"


settings = Settings()
