import aiohttp


class Scraper:
    def __init__(self):
        self.grand_total = 0
        self.step = 0
        self.request_notices = []

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
