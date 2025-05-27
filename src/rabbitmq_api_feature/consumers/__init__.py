import asyncio

from src.rabbitmq_api_feature.infrastructure.rabbitmq.setup import consumer_manager
from . import handlers


for task in consumer_manager.get_tasks():
    print(task)
    asyncio.create_task(task())
    