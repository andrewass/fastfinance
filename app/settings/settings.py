from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    cache_enabled: bool = True
    #persistence_type Persistence = Persistence.IN_MEMORY


settings = Settings()
