from pydantic_settings import BaseSettings
from ..cache.persistence.persistence_type import PersistenceType


class Settings(BaseSettings):
    cache_enabled: bool = True
    persistence_type: PersistenceType = PersistenceType.IN_MEMORY


settings = Settings()
