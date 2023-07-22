from fastapi import FastAPI
from .price import pricerouter

app = FastAPI(version="0.0.1")

app.include_router(pricerouter.router)

