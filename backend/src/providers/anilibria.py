from httpx import AsyncClient

from json import dumps


class Anilibria:

    def __init__(self):

        self.__video_domen = "https://cache.libria.fun"
        self.__qualities = {
            "fhd": "1080",
            "hd": "720",
            "sd": "480"
        }

    @staticmethod
    async def __request(url: str):
        async with AsyncClient() as client:
            result = await client.get(url)
            return result

    async def get_anime_by_code(self, code: str):
        result = await self.__request(f"https://api.anilibria.tv/v3/title?code={code}")
        return result.json()

    @staticmethod
    async def __format_links(episodes: list):
        return dumps([
            {
                "title": f'{episode["episode"]} episode',
                "file": ",".join([f'[{video["quality"]}p]{video["link"]}' for video in episode["links"]])
            }
            for episode in episodes]
        )

    async def __extract_m3u8_links(self, data: dict):
        parsed_data = data["player"]
        result = []

        for item in parsed_data["list"].values():
            links = []

            for quality, link in item["hls"].items():

                if not link:
                    continue

                quality = self.__qualities.get(quality)
                link = f"{self.__video_domen}{link}"

                links.append({"quality": quality, "link": link})

            result.append({"episode": item["episode"], "links": links})

        return result

    async def get_links(self, code: str):
        anime = await self.get_anime_by_code(code)
        episodes = await self.__extract_m3u8_links(anime)
        result = await self.__format_links(episodes)
        return result
