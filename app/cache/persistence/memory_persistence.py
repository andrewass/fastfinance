from .persistence import Persistence


class MemoryPersistence(Persistence):
    cache: dict[int, dict] = {}

    def has_key(self, key: int) -> bool:
        return key in self.cache

    def get_value(self, key: int):
        return self.cache.get(key)

    def update(self, function_key: int, arguments_key: str, value: dict):
        self.cache.update({function_key: value})

    def clear_storage(self):
        self.cache.clear()
