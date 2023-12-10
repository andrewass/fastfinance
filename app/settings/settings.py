from pydantic_settings import BaseSettings

from app.cache.persistence.persistence import Persistence
from app.cache.persistence.redis_persistence import RedisPersistence


class Settings(BaseSettings):
    cache_enabled: bool = True
    persistence: Persistence = RedisPersistence()


settings = Settings()
