class Persistence:

    def get_response_value(self, key: str):
        raise NotImplementedError

    def remove_response_value(self, key: str):
        raise NotImplementedError

    def set_response_value(self, key: str, value: dict):
        raise NotImplementedError

    def close(self):
        return None
