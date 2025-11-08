from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware
from .core.settings import AppSettings, get_settings
from .routes import (
    testroute
)

config: AppSettings = get_settings()
api_prefix: str = config.api_prefix

origins: List = ["http://localhost:8000"]

@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """Asynchronous context manager for managing the lifespan of a FastAPI application."""
    await startup()
    from .core.db import init_database
    init_database()
    yield
    await shutdown()


app = FastAPI(
    title=f"stantech",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def startup():
    """Server startup function, run whatever is required to start with server startup"""
    app.config = config
    

async def shutdown():
    """Server shutdown function, terminates all connections to resources"""
    pass


app.include_router(testroute.router, prefix=f"{api_prefix}/testroute", tags=["TestRoute"])
