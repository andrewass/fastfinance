from pydantic_settings import BaseSettings
from enum import Enum


class Persistence(Enum):
    REDIS = "REDIS"
    IN_MEMORY = "IN_MEMORY"


class Settings(BaseSettings):
    cache_enabled: bool = True
    persistence: Persistence = Persistence.IN_MEMORY


settings = Settings()
