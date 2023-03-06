import aiohttp
import pika


class Scraper:
    def __init__(self, host: str = "localhost", queue: str = "notices_queue"):
        self.grand_total = 0
        self.step = 0
        self.request_notices = []
        self.host = host
        self.queue = queue
        self.connection = None
        self.channel = None

    async def get_notices(self, loop, start: str = "", break_point: int = float("inf")):
        letters = [char for char in "AMSRIOEGBLUKHDCNTPVZFYJQW ÑX-ÁÓÉÍÀÚ&/'"] + ["/."]
        async with aiohttp.ClientSession(loop=loop) as session:
            for letter in letters:
                regex_string = "^" + start + letter + ".*$"
                url = f"https://ws-public.interpol.int/notices/v1/red"
                parameters = {"name": regex_string, "resultPerPage": 160}
                async with session.get(url, params=parameters) as response:
                    response_json = await response.json()
                    total = response_json["total"]
                    if break_point == 0:
                        break
                    elif total > 160:
                        await self.get_notices(
                            loop, start=start + letter, break_point=total
                        )
                        break_point -= total
                    elif total > 0 and total < 160:
                        break_point -= total
                        self.grand_total += total
                        self.step += 1
                        print(self.step, regex_string, total, self.grand_total)
                        self.request_notices += response_json["_embedded"]["notices"]
                    else:
                        continue
            return self.request_notices

    def connect(self) -> None:
        """
        Connects to the RabbitMQ broker and creates a channel and queue.
        """
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

    def publish(self, notices: list) -> None:
        """
        Publishes a notices to the queue.

        Args:
            notices (list): The notices to be sent to the queue.
        """
        for notice in notices:
            self.channel.basic_publish(
                exchange="", routing_key=self.queue, body=str(notice)
            )

    def close(self) -> None:
        """
        Closes the connection to the RabbitMQ broker.
        """
        self.connection.close()
