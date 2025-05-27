# import asyncio
# import aio_pika


# async def publish_message():
#     # connection = await aio_pika.connect_robust("amqp://rabbitmq:rabbitmq@localhost/")
#     # async with connection:
#     #     channel = await connection.channel()
#     #     queue = await channel.declare_queue("my-queue", durable=True)

#     #     await channel.default_exchange.publish(
#     #         aio_pika.Message(body=b"Hello Rabbit!"),
#     #         routing_key=queue.name
#     #     )

#     conn = await aio_pika.connect_robust(
#         host="localhost",
#         port=5672,
#         login="rabbitmq",
#         password="rabbitmq"
#     )

#     async with conn:
#         channel = await conn.channel()
#         queue = await channel.declare_queue(
#             "test",
#             durable=True
#         )

#         await channel.default_exchange.publish(
#             aio_pika.Message(body=b"Hello World!"),
#             routing_key=queue.name
#         )



# async def read_messages():
#     conn = await aio_pika.connect_robust(
#         host="localhost",
#         port=5672,
#         login="rabbitmq",
#         password="rabbitmq"
#     )

#     async with conn:

#         channel = await conn.channel()
#         queue = await channel.declare_queue("test", durable=True)

#         async with queue.iterator() as queue_iter:

#             async for message in queue_iter:

#                 async with message.process():

#                     print(message.body.decode())

#                     # await message.nack()


from fastapi import FastAPI
from .loader import lifespan


app = FastAPI(lifespan=lifespan)
