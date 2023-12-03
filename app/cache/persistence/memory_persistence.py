from .persistence import Persistence


class MemoryPersistence(Persistence):
    cache: dict[int, dict] = {}

    def __init__(self):
        pass

    def contains_function(self, function_id: int) -> bool:
        self.cache.__contains__(function_id)

    def get_response_value(self, function_key: int, arguments_key: str):
        return self.cache.get(function_key)

    def remove_response_value(self, function_key: int, arguments_key: str):
        self.persistence.remove_response_value(function_key, arguments_key)

    def set_response_value(self, function_key: int, arguments_key: str, value: dict):
        self.persistence.set_function()

    def set_function(self, function_key: int):
        self.persistence.set_function()

    def clear_storage(self):
        self.cache.clear()
