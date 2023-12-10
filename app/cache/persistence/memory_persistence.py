from .persistence import Persistence


class MemoryPersistence(Persistence):
    cache: dict[int, dict] = {}

    def __init__(self):
        pass

    def get_response_value(self, key: str):
        return self.cache.get(key)

    def remove_response_value(self, key: str):
        self.cache.pop(key)

    def set_response_value(self, key: str, value: dict):
        self.cache[key] = value

    def clear_storage(self):
        self.cache.clear()
