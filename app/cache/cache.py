from app.cache.persistence.memory_persistence import MemoryPersistence
from app.cache.persistence.persistence import Persistence
from app.cache.persistence.persistence_type import PersistenceType
from app.cache.persistence.redis_persistence import RedisPersistence


class Cache:
    persistence: Persistence

    def __init__(self, persistence_type: PersistenceType):
        self.__set_persistence(persistence_type)

    def get_value(self, key: str) -> dict:
        """Returns cache value based on key"""

    def insert(self, key: str, value: dict):
        """Insert a new key/value pair into the cache"""

    def __set_persistence(self, persistence_type: PersistenceType):
        match persistence_type:
            case PersistenceType.REDIS:
                self.persistence = RedisPersistence()
            case PersistenceType.IN_MEMORY:
                self.persistence = MemoryPersistence()



