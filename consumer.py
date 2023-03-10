import ast
import datetime
import os

import pika
from dotenv import load_dotenv

from db import MongoDB

# Load variables from .env file
load_dotenv()


class RabbitMQConsumer:
    """
    A RabbitMQ consumer class that receives messages from a specified queue.

    Attributes:
        host (str): The RabbitMQ server host address. Default is 'localhost'.
        queue (str): The queue to consume messages from. Default is 'hello'.
        connection (pika.BlockingConnection): The RabbitMQ connection object.
        channel (pika.channel.Channel): The channel object used for message communication.

    """

    def __init__(
        self, host: str = os.getenv("RABBITMQ_HOST"), queue: str = "notices_queue"
    ) -> None:
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

    def connect(self) -> None:
        """
        Creates a blocking RabbitMQ connection object and channel object for the provided RabbitMQ server host.

        Args:
            None

        Returns:
            None
        """
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host)
        )
        self.channel = self.connection.channel()

    def callback(
        self,
        ch: pika.channel.Channel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes,
    ) -> None:
        """
        Callback function to handle incoming messages.

        Args:
            ch (pika.channel.Channel): The channel object.
            method (pika.spec.Basic.Deliver): The message delivery metadata.
            properties (pika.spec.BasicProperties): The message properties.
            body (bytes): The message body.

        Returns:
            None
        """

        # db.collection.update_many({}, {"$set": {"alert": False}})
        timestamp = datetime.datetime.now()
        print("Received message at:", timestamp)
        print("Received message:")
        notice = ast.literal_eval(body.decode())
        if notice["record_year"] == datetime.datetime.now().year:
            db = self.db.collection

            if not db.find_one({"entity_id": notice["entity_id"]}):
                print(notice["entity_id"])
                notice["timestamp"] = timestamp
                db.collection.insert_one(notice)
            else:
                db.update_one(
                    {"entity_id": notice["entity_id"]},
                    {"$set": {"timestamp": timestamp}},
                )

    def start_consuming(self) -> None:
        """
        Sets up a consumer to receive messages from the provided queue and starts consuming messages.

        Args:
            None

        Returns:
            None
        """
        self.channel.queue_declare(queue=self.queue)
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=self.callback, auto_ack=True
        )
        print("Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

    def close(self) -> None:
        """
        Closes the RabbitMQ connection.

        Args:
            None

        Returns:
            None
        """
        self.connection.close()
        self.connection = None
        self.channel = None


# Create a RabbitMQConsumer object and start consuming messages
if __name__ == "__main__":
    consumer = RabbitMQConsumer()
    consumer.connect()
    consumer.start_consuming()
