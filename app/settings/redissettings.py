from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    host: str = "redis"
    port: int = 6379
    user: str = "default"
    password: str = "redisDockerTestPassword"


redis_settings = RedisSettings()
