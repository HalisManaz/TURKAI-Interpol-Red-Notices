from consumer import RabbitMQConsumer


# Test the constructor
def test_constructor():
    """Test the constructor for local development""" ""
    consumer = RabbitMQConsumer()
    assert consumer.host == "localhost"
    assert consumer.queue == "notices_queue"
