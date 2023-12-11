import json
import logging
import sys
from datetime import timedelta, datetime

from .cache import Cache
from .cacheresponse import CacheResponse
from ..settings.settings import settings

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

cache = Cache(persistence=settings.persistence)


def fetch_function_response(function: callable, expire: timedelta, *args, **kwargs):
    function_key = str(id(function))
    arguments_key = json.dumps([args, kwargs])
    combined_key = function_key + " " + arguments_key
    response_value = cache.get_response_value(combined_key)
    if response_value is not None:
        expiration = response_value.get("added") + expire.total_seconds()
        if expiration > datetime.now().timestamp():
            return response_value.get("data")
        else:
            cache.remove_response_value(combined_key)
    response = function(*args, **kwargs)
    cache.set_response_value(
        combined_key,
        CacheResponse(added=datetime.now(), data=response.model_dump()).model_dump()
    )
    return response


def simple_cache(expire: timedelta = timedelta(hours=1)) -> callable:
    def _wrapper(function: callable):
        def __wrapper(*args, **kwargs):
            if settings.cache_enabled:
                return fetch_function_response(function, expire, *args, **kwargs)
            else:
                return function(*args, **kwargs)

        return __wrapper

    return _wrapper
