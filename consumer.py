import ast
import datetime
import json

import pika

from db import MongoDB


class RabbitMQConsumer:
    """
    A RabbitMQ consumer class that receives messages from a specified queue.

    Attributes:
        host (str): The RabbitMQ server host address. Default is 'localhost'.
        queue (str): The queue to consume messages from. Default is 'hello'.
        connection (pika.BlockingConnection): The RabbitMQ connection object.
        channel (pika.channel.Channel): The channel object used for message communication.

    """

    def __init__(self, host: str = "localhost", queue: str = "notices_queue") -> None:
        """
        Initializes the RabbitMQConsumer class with the provided RabbitMQ server host and queue.

        Args:
            host (str): The RabbitMQ server host address. Default is 'localhost'.
            queue (str): The queue to consume messages from. Default is 'hello'.

        Returns:
            None
        """
        self.host = host
        self.queue = queue
        self.connection = None
        self.channel = None
        self.db = MongoDB()
