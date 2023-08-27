import json

from ..settings.settings import settings

CACHE: dict[int, dict] = {}


def fetch_function_response(function, function_id, *args, **kwargs):
    function_dict = CACHE.get(function_id)
    arguments_key = json.dumps([args, kwargs])
    if arguments_key in function_dict:
        return function_dict.get(arguments_key)
    else:
        response = function(*args, **kwargs)
        function_dict.update({arguments_key: response})
        return response


def simple_cache(limit: int = 600) -> callable:
    def _cached(function: callable):
        def __cached(*args, **kwargs):
            if settings.cache_enabled:
                function_id = id(function)
                if function_id not in CACHE:
                    CACHE.update({function_id: {}})
                return fetch_function_response(function, function_id, *args, **kwargs)
            else:
                return function(*args, **kwargs)
        return __cached
    return _cached
