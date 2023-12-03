import json
import logging
import sys
import time
from datetime import timedelta

from .cache import Cache
from ..settings.settings import settings

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

cache = Cache(persistence=settings.persistence)


def fetch_function_response(function: callable, function_id: int, expire: timedelta, *args, **kwargs):
    arguments_key = json.dumps([args, kwargs])
    response_value = cache.get_response_value(function_id, arguments_key)
    if response_value is not None:
        expiration = response_value.get("added") + expire
        if expiration > time.time():
            return response_value.get("data")
        else:
            cache.remove_response_value(function_id, arguments_key)
    response = function(*args, **kwargs)
    cache.set_response_value(function_id, arguments_key, {"added": time.time(), "data": response})
    return response


def simple_cache(expire: timedelta = timedelta(hours=1)) -> callable:
    def _wrapper(function: callable):
        def __wrapper(*args, **kwargs):
            if settings.cache_enabled:
                function_id = id(function)
                if not cache.contains_function(function_id):
                    cache.update(function_id, {})
                return fetch_function_response(function, function_id, expire, *args, **kwargs)
            else:
                return function(*args, **kwargs)

        return __wrapper

    return _wrapper
