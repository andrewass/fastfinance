class Persistence:

    def has_key(self, key: int) -> bool:
        """Check if key exists in cache"""
        pass

    def update(self, function_key: int, arguments_key: str, value: dict):
        """Update cache with key value pair"""
        pass

    def get_value(self, key: int):
        """Fetch perisistence value"""
        pass

    def clear_storage(self):
        """Clear persistence storage"""
        pass
