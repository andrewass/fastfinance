from .persistence import Persistence


class MemoryPersistence(Persistence):
    def __init__(self):
        self.cache: dict[str, dict] = {}

    def get_response_value(self, key: str):
        return self.cache.get(key)

    def remove_response_value(self, key: str):
        self.cache.pop(key, None)

    def set_response_value(self, key: str, value: dict):
        self.cache[key] = value

    def close(self):
        self.cache.clear()
