from aiohttp import ClientSession

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
    async def __request(url: str) -> dict:
        async with ClientSession() as session:
            async with session.get(url) as response:
                result = await response.json()
                return result

    async def get_anime_by_code(self, code: str) -> dict:
        result = await self.__request(f"https://api.anilibria.tv/v3/title?code={code}")
        return result

    @staticmethod
    async def __format_links(episodes: list) -> str:
        result = []
        for episode in episodes:
            data = {}
            data.update({
                "title": f'{episode["episode"]} episode',
                "file": ",".join([f'[{video["quality"]}p]{video["link"]}' for video in episode["links"]]),
                "id": episode["id"]
            })
            if len(episode["opening"]) == 2:
                data.update({
                    "outside": [{"id": "skip-opening", "from": episode["opening"][0], "to": episode["opening"][1]},
                                {"id": "skip-opening-overlay", "from": episode["opening"][0],
                                 "to": episode["opening"][1]}]
                })
            result.append(data)

        return dumps(result)

    @staticmethod
    async def __get_skips(episodes: list) -> dict:
        result = {}

        for episode in episodes:
            result.update({
                episode["id"]: episode["opening"]
            })

        return result

    async def __extract_m3u8_links(self, data: dict) -> list:
        parsed_data = data["player"]
        result = []

        for index, item in enumerate(parsed_data["list"].values()):
            links = []

            for quality, link in item["hls"].items():

                if not link:
                    continue

                quality = self.__qualities.get(quality)
                link = f"{self.__video_domen}{link}"

                links.append({"quality": quality, "link": link})

            result.append({"id": index, "episode": item["episode"], "links": links, "opening": item.get("skips", {}).get("opening")})

        return result

    async def get_links(self, code: str) -> tuple:
        anime = await self.get_anime_by_code(code)
        episodes = await self.__extract_m3u8_links(anime)
        links = await self.__format_links(episodes)
        skips = await self.__get_skips(episodes)
        return links, skips
