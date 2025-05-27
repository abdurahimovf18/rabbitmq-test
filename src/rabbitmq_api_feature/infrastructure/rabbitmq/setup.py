from .utils import LazyRabbitMQConnection, RabbitMQConsumerManager


lazy_rabbitmq_connection = LazyRabbitMQConnection(
)    # here should be connection parameters


async def get_connection():
    """
    Retrieve a lazily initialized and cached RabbitMQ connection.

    This function returns a robust RabbitMQ connection instance managed by
    `LazyRabbitMQConnection`. The connection is established only on the first call,
    and subsequent calls return the cached connection, enabling centralized,
    efficient, and reusable access across different modules and functions.

    Returns:
        AbstractRobustConnection: An active RabbitMQ connection.
    """
    rabbitmq_connection = await lazy_rabbitmq_connection.get_lazy_connection()
    return rabbitmq_connection


consumer_manager = RabbitMQConsumerManager(
    connectionmaker=get_connection
)
