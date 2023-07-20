from fastapi import FastAPI
from .routers import price

app = FastAPI(version="0.0.1")

app.include_router(price.router)

