from enum import Enum


class PersistenceType(Enum):
    REDIS = "REDIS"
    IN_MEMORY = "IN_MEMORY"
