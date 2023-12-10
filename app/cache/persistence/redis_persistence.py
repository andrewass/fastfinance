import redis
from redis.commands.json.path import Path

from .persistence import Persistence
from ...settings.redissettings import redis_settings


class RedisPersistence(Persistence):
    redis = redis.Redis(
        host="localhost",
        port=6379,
        password=redis_settings.password,
        decode_responses=True
    )

    def __init__(self):
        pass

    def get_response_value(self, key: str):
        return self.redis.json().get(key)

    def remove_response_value(self, key: str):
        self.redis.delete(key)

    def set_response_value(self, key: str, value: dict):
        self.redis.json().set(key, Path.root_path(), value)

    def clear_storage(self):
        self.redis.delete()
