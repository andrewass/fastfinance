from .persistence import Persistence


class MemoryPersistence(Persistence):
    cache: dict[int, dict] = {}

    def __init__(self):
        pass

    def contains_function(self, function_id: int) -> bool:
        return self.cache.__contains__(function_id)

    def get_response_value(self, function_key: int, arguments_key: str):
        functionCache = self.cache.get(function_key)
        return functionCache.get(arguments_key)

    def remove_response_value(self, function_key: int, arguments_key: str):
        self.persistence.remove_response_value(function_key, arguments_key)

    def set_response_value(self, function_key: int, arguments_key: str, value: dict):
        function_cache = self.cache[function_key]
        function_cache[arguments_key] = value

    def set_function(self, function_key: int):
        self.cache[function_key] = {}

    def clear_storage(self):
        self.cache.clear()
