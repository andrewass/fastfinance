import json
import logging
import sys
import time

from ..settings.settings import settings

CACHE: dict[int, dict] = {}
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def fetch_function_response(function: callable, function_id: int, expire: int, *args, **kwargs):
    function_dict = CACHE.get(function_id)
    arguments_key = json.dumps([args, kwargs])
    if arguments_key in function_dict:
        dict_value: dict = function_dict.get(arguments_key)
        expiration = dict_value.get("added") + expire
        if expiration > time.time():
            return dict_value.get("data")
        else:
            function_dict.pop(arguments_key)
    response = function(*args, **kwargs)
    function_dict.update({arguments_key: {"added": time.time(), "data": response}})
    return response


def simple_cache(expire: int = 600) -> callable:
    def _wrapper(function: callable):
        def __wrapper(*args, **kwargs):
            if settings.cache_enabled:
                function_id = id(function)
                if function_id not in CACHE:
                    CACHE.update({function_id: {}})
                return fetch_function_response(function, function_id, expire, *args, **kwargs)
            else:
                return function(*args, **kwargs)
        return __wrapper
    return _wrapper
