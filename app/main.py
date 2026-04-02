from contextlib import asynccontextmanager

from fastapi import FastAPI

from .cache.cache import Cache
from .cache.cachedecorator import configure_cache, clear_cache
from .errors.problem import register_problem_handlers
from .holders import holdersrouter
from .price import pricerouter
from .profile import profilerouter
from .settings.settings import settings
from .statistics import statisticsrouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    app_cache = Cache(persistence=settings.persistence)
    app.state.cache = app_cache
    configure_cache(app_cache)
    try:
        yield
    finally:
        clear_cache()
        settings.persistence.close()


app = FastAPI(version="0.0.1", lifespan=lifespan)
register_problem_handlers(app)

app.include_router(pricerouter.router)
app.include_router(statisticsrouter.router)
app.include_router(holdersrouter.router)
app.include_router(profilerouter.router)
