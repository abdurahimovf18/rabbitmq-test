from typing import Awaitable, List, Callable
from aio_pika import connect_robust
from aio_pika.abc import AbstractRobustConnection


class LazyRabbitMQConnection:
    """
    Provides a lazy-initialized, cached connection to RabbitMQ using aio-pika's robust connection.

    This class manages a single connection instance that is created only upon the first request.
    Subsequent requests return the cached connection object. Connection parameters can be
    configured at initialization.

    Attributes:
        __connection (AbstractRobustConnection | None): Cached connection instance.
        kwargs (dict): Connection parameters for `aio_pika.connect_robust`.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5672,
        login: str = "guest",
        password: str = "guest",
        **kwargs
    ):
        """
        Initialize the LazyRabbitMQConnection with connection parameters.

        Args:
            host (str): RabbitMQ server hostname or IP address. Defaults to 'localhost'.
            port (int): RabbitMQ server port. Defaults to 5672.
            login (str): Username for authentication. Defaults to 'guest'.
            password (str): Password for authentication. Defaults to 'guest'.
            **kwargs: Additional keyword arguments forwarded to `aio_pika.connect_robust`.
        """
        self.__connection: AbstractRobustConnection | None = None
        self.kwargs = kwargs | dict(host=host, port=port, login=login, password=password)

    async def get_lazy_connection(self) -> AbstractRobustConnection:
        """
        Get the cached RabbitMQ connection or create it if not initialized.

        This method ensures the connection is established only once (lazy initialization).
        It returns the same connection instance on subsequent calls.

        Returns:
            AbstractRobustConnection: The established robust RabbitMQ connection.
        """
        if self.__connection is None:
            self.__connection = await self.make_connection()

        return self.__connection

    async def make_connection(self) -> AbstractRobustConnection:
        """
        Create a new robust RabbitMQ connection using stored connection parameters.

        Returns:
            AbstractRobustConnection: A new connection instance.
        """
        return await connect_robust(**self.kwargs)


class RabbitMQConsumerManager:
    """
    Central registry and manager for RabbitMQ consumer coroutine functions.

    Allows decorating async consumer functions that take a RabbitMQ connection,
    wrapping them into no-argument async callables that handle connection provisioning.

    Usage:
        @consumer_manager.register
        async def my_consumer(connection: AbstractRobustConnection):
            ...

        for task in consumer_manager.get_tasks():
            asyncio.create_task(task())
    """

    def __init__(
        self,
        connectionmaker: Callable[[], Awaitable[AbstractRobustConnection]]
    ):
        """
        Initialize with an async callable that returns a RabbitMQ connection.

        Args:
            connectionmaker: Async function returning a robust connection.
        """
        self.__connectionmaker = connectionmaker
        self.__registered_tasks: List[Callable[[], Awaitable[None]]] = []

    def register(
        self,
        rabbitmq_consumer: Callable[[AbstractRobustConnection], Awaitable[None]]
    ) -> Callable[[AbstractRobustConnection], Awaitable[None]]:
        """
        Decorator to register a RabbitMQ consumer coroutine function.

        Wraps the consumer so it receives a connection automatically when run.

        Args:
            rabbitmq_consumer: Async function accepting a connection.

        Returns:
            The original consumer function (decorator pattern).
        """

        async def consumer_task() -> None:
            connection = await self.__connectionmaker()
            await rabbitmq_consumer(connection)

        self.__registered_tasks.append(consumer_task)
        return rabbitmq_consumer
    
    def get_tasks(self) -> List[Callable[[], Awaitable[None]]]:
        """
        Retrieve all registered consumer tasks as zero-argument async callables.

        Returns:
            List of async functions which, when called, run the consumer with a connection.
        """
        return self.__registered_tasks
    