from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.local", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    host: str = "redis"
    port: int = 6379
    user: str = "default"
    password: str = "redisDockerTestPassword"


redis_settings = RedisSettings()
