import asyncio
import datetime
import os
import time

import aiohttp
import pika
from dotenv import load_dotenv

from db import MongoDB

# Load variables from .env file
load_dotenv()


class Scraper:
    def __init__(
        self, host: str = os.getenv("RABBITMQ_HOST"), queue: str = "notices_queue"
    ):
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

    def organize_notices_data(self, notices: list) -> list:
        organized_notices = []

        for notice in notices:
            try:
                entity_id = notice["entity_id"]
                forename = notice["forename"]
                name = notice["name"]
                record_year = int(notice["entity_id"].split("/")[0])
                record_id = int(notice["entity_id"].split("/")[1])

                if notice["date_of_birth"] is None:
                    age = 0
                elif len(notice["date_of_birth"]) == 4:
                    age = datetime.datetime.now().year - int(notice["date_of_birth"])
                else:
                    age = (
                        datetime.datetime.now().year
                        - datetime.datetime.strptime(
                            notice["date_of_birth"], "%Y/%m/%d"
                        )
                        .date()
                        .year
                    )

                if notice["nationalities"] is not None:
                    nationality = notice["nationalities"][0]
                else:
                    nationality = "Unknown"
                image_url = notice["_links"]["thumbnail"]["href"]

            except KeyError as e:
                if str(e) == "'thumbnail'":
                    image_url = "https://www.interpol.int/bundles/interpolfront/images/photo-not-available.png"

            finally:
                notice_data = {
                    "entity_id": entity_id,
                    "forename": forename,
                    "name": name,
                    "record_year": record_year,
                    "record_id": record_id,
                    "age": age,
                    "nationality": nationality,
                    "image_url": image_url,
                    "alert": True,
                }
                organized_notices.append(notice_data)
        return organized_notices

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


def main():
    while True:
        try:
            loop = asyncio.get_event_loop()
            producer = Scraper()
            producer.connect()
            notices = loop.run_until_complete(producer.get_notices(loop))
            notices = producer.organize_notices_data(notices)
            db = MongoDB()
            db.collection.update_many({}, {"$set": {"alert": False}})
            producer.publish(notices=notices)
            producer.close()
            time.sleep(int(os.getenv("INTERVAL")))
            print("API successfully scraped. Restarting in 1 hour...")
        except Exception as e:
            print("Unexpected error:")
            print(e)
            print("Restarting in 60 seconds...")
            time.sleep(60)


if __name__ == "__main__":
    main()
