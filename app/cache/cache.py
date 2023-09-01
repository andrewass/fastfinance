from app.cache.persistence.memory_persistence import MemoryPersistence
from app.cache.persistence.persistence import Persistence
from app.cache.persistence.persistence_type import PersistenceType
from app.cache.persistence.redis_persistence import RedisPersistence


class Cache:
    persistence: Persistence

    def __init__(self, persistence_type: PersistenceType):
        self.__set_persistence(persistence_type)

    def contains_function(self, function_id: int) -> bool:
        self.persistence

    def get_function_dict(self, function_id: int):
        return self.persistence.get_value(function_id)

    def get_value(self, key: str) -> dict:
        """Returns cache value based on key"""

    def update(self, function_key: int, arguments_key: str, value: dict):
        self.persistence.update()

    def __set_persistence(self, persistence_type: PersistenceType):
        match persistence_type:
            case PersistenceType.REDIS:
                self.persistence = RedisPersistence()
            case PersistenceType.IN_MEMORY:
                self.persistence = MemoryPersistence()
