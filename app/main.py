from fastapi import FastAPI

from .holders import holdersrouter
from .price import pricerouter
from .statistics import statisticsrouter
from .profile import profilerouter

app = FastAPI(version="0.0.1")

app.include_router(pricerouter.router)
app.include_router(statisticsrouter.router)
app.include_router(holdersrouter.router)
app.include_router(profilerouter.router)
