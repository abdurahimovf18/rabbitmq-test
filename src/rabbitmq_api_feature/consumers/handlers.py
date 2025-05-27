from aio_pika.abc import AbstractRobustConnection
from src.rabbitmq_api_feature.infrastructure.rabbitmq.setup import consumer_manager
import orjson


@consumer_manager.register
async def hello_world_consumer(connection: AbstractRobustConnection):
    channel = await connection.channel()
    queue = await channel.declare_queue("test.hello_world.sent", durable=True)

    async with queue.iterator() as queue_iterator:

        async for message in queue_iterator:

            async with message.process():

                body = message.body.decode()

                print(body)
