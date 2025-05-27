from typing import Annotated
from fastapi import Depends
from aio_pika.abc import AbstractRobustConnection

from src.rabbitmq_api_feature.infrastructure.rabbitmq.setup import get_connection


async def __rabbitmq_connection_denedency():
    return await get_connection()


rabbitmq_connection = Annotated[AbstractRobustConnection, Depends(__rabbitmq_connection_denedency)]
