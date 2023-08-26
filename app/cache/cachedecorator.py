import json
from collections import OrderedDict
from ..settings.settings import settings

CACHE = {}
KEYS = []


def sort(kwargs):
    sorted_dict = OrderedDict()
    for key, value in kwargs.items():
        if isinstance(value, dict):
            sorted_dict[key] = sort(value)
        else:
            sorted_dict[key] = value
    return sorted_dict


def simple_cache(duration: int = 600) -> callable:
    def _wrapper(function: callable):
        def __wrapper(*args, **kwargs):
            if settings.cache_enabled:
                cache_key = json.dumps([id(function), args, sort(kwargs)], separators=(",", ":"))
                return function
            else:
                return function
        return __wrapper
    return _wrapper
