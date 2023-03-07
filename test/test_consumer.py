from consumer import RabbitMQConsumer


# Test the constructor
def test_constructor():
    """Test the constructor for local development""" ""
    consumer = RabbitMQConsumer()
    assert consumer.host == "localhost"
    assert consumer.queue == "notices_queue"


# Test the connect method
def test_connect():
    consumer = RabbitMQConsumer()
    consumer.connect()
    assert consumer.connection is not None
    assert consumer.channel is not None


# Test the close method
def test_close():
    consumer = RabbitMQConsumer()
    consumer.connect()
    consumer.close()
    assert consumer.connection is None
    assert consumer.channel is None
