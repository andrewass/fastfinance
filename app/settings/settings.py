from pydantic_settings import BaseSettings

from app.cache.persistence.memory_persistence import MemoryPersistence
from app.cache.persistence.persistence import Persistence


class Settings(BaseSettings):
    cache_enabled: bool = True
    persistence: Persistence = MemoryPersistence()


settings = Settings()
