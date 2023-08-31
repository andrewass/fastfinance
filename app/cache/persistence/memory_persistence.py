from persistence import Persistence


class MemoryPersistence(Persistence):
    cache: dict[int, dict] = {}

    def get_value(self):

    def clear_storage(self):
        """Clear persistence storage"""
        self.cache.
        pass
