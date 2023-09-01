class Persistence:

    def contains_function(self, function_id: int) -> bool:
        """"""
        pass

    def get_response_value(self, function_key: int, arguments_key: str):
        """"""
        pass

    def remove_response_value(self, function_key: int, arguments_key: str):
        """"""
        pass

    def set_response_value(self, function_key: int, arguments_key: str, value: dict):
        """"""
        pass

    def set_function(self, function_key: int):
        """"""
        pass

    def clear_storage(self):
        """Clear persistence storage"""
        pass
