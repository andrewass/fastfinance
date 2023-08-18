from fastapi import FastAPI
from .price import pricerouter
from .financials import financialsrouter
from .holders import holdersrouter

app = FastAPI(version="0.0.1")

app.include_router(pricerouter.router)
app.include_router(financialsrouter.router)
app.include_router(holdersrouter.router)
