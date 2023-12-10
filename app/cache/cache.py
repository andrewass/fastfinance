from app.cache.persistence.persistence import Persistence


class Cache:
    persistence: Persistence

    def __init__(self, persistence: Persistence):
        self.persistence = persistence

    def get_response_value(self, key: str):
        return self.persistence.get_response_value(key)

    def remove_response_value(self, key: str):
        self.persistence.remove_response_value(key)

    def set_response_value(self, key: str, value: dict):
        self.persistence.set_response_value(key, value)
