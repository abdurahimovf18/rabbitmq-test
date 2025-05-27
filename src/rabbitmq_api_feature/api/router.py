from fastapi import APIRouter
from aio_pika import Message

from src.rabbitmq_api_feature.services.dependencies import rabbitmq_connection


router = APIRouter(prefix="")


@router.post("/add/task")
async def add_task(
    rabbitmq: rabbitmq_connection
):
    
    channel = await rabbitmq.channel()
    queue = await channel.declare_queue("test.hello_world.sent", durable=True)

    await channel.default_exchange.publish(
        message=Message(body=b"Hello world"),
        routing_key=queue.name
    )

