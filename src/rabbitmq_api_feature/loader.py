from contextlib import asynccontextmanager
from fastapi import FastAPI

from .api.router import router
from src.rabbitmq_api_feature.infrastructure.rabbitmq import setup as rabbitmq

from . import consumers


@asynccontextmanager
async def lifespan(app: FastAPI):

    app.include_router(router)

    async with await rabbitmq.get_connection():

        yield

