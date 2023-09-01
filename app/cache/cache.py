from app.cache.persistence.memory_persistence import MemoryPersistence
from app.cache.persistence.persistence import Persistence
from app.cache.persistence.persistence_type import PersistenceType
from app.cache.persistence.redis_persistence import RedisPersistence


class Cache:
    persistence: Persistence

    def __init__(self, persistence_type: PersistenceType):
        self.__set_persistence(persistence_type)

    def contains_function(self, function_id: int):
        self.persistence.contains_function(function_id)

    def get_response_value(self, function_key: int, arguments_key: str):
        return self.persistence.get_response_value(function_key, arguments_key)

    def remove_response_value(self, function_key: int, arguments_key: str):
        self.persistence.remove_response_value(function_key, arguments_key)

    def set_response_value(self, function_key: int, arguments_key: str, value: dict):
        self.persistence.set_response_value(function_key, arguments_key, value)

    def set_function(self, function_key: int):
        self.persistence.set_function(function_key)

    def __set_persistence(self, persistence_type: PersistenceType):
        match persistence_type:
            case PersistenceType.REDIS:
                self.persistence = RedisPersistence()
            case PersistenceType.IN_MEMORY:
                self.persistence = MemoryPersistence()
