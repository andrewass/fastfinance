import hashlib
import logging
import sys
from datetime import timedelta, datetime
from typing import Any, Callable

from .cache import Cache
from .cacheresponse import CacheResponse
from ..settings.settings import settings

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

cache: Cache | None = None


def configure_cache(cache_instance: Cache):
    global cache
    cache = cache_instance


def clear_cache():
    global cache
    cache = None


def get_cache() -> Cache:
    global cache
    if cache is None:
        cache = Cache(persistence=settings.persistence)
    return cache


def fetch_function_response(function: Callable[..., Any], expire: timedelta, *args, **kwargs):
    active_cache = get_cache()
    cache_key = create_cache_key(function, args, kwargs)
    response_value = active_cache.get_response_value(cache_key)
    if response_value is not None:
        expiration = response_value.get("added") + expire.total_seconds()
        if expiration > datetime.now().timestamp():
            return response_value.get("data")
        else:
            active_cache.remove_response_value(cache_key)
    response = function(*args, **kwargs)
    active_cache.set_response_value(
        cache_key,
        CacheResponse(added=datetime.now(), data=response.model_dump()).model_dump()
    )
    return response


def simple_cache(expire: timedelta = timedelta(hours=1)) -> callable:
    def _wrapper(function: Callable[..., Any]):
        def __wrapper(*args, **kwargs):
            if settings.cache_enabled:
                return fetch_function_response(function, expire, *args, **kwargs)
            else:
                return function(*args, **kwargs)

        return __wrapper

    return _wrapper


def create_cache_key(function: Callable[..., Any], *args, **kwargs) -> str:
    function_key = hashlib.md5(function.__name__.encode("utf-8")).hexdigest()
    args_key = hashlib.md5(f"{args}{kwargs}".encode("utf-8")).hexdigest() if args or kwargs else ""
    return f"{function_key}.{args_key}"
