from aiohttp import ClientSession

from json import dumps
from typing import List

from backend.src.helpers import Episode, Link


class Anilibria:

    def __init__(self):
        self.__domain = "https://cache.libria.fun"
        self.__qualities = {
            "fhd": "1080",
            "hd": "720",
            "sd": "480"
        }

    @staticmethod
    async def __request(url: str) -> dict:
        """
        Makes a request and returns a response.

        Parameters:
        - url [str]: Request link.

        Returns:
        - dict: Request response.
        """
        async with ClientSession() as session:
            async with session.get(url) as response:
                result = await response.json()
                return result

    async def __extract_m3u8_links(self, data: dict) -> List[Episode]:
        """
        Returns an object with anime episodes data.

        Parameters:
        - data [dict]: Dictionary with data from the query response to Anilibria API.

        Returns:
        - list: List of episodes objects.
        """
        parsed_data = data["player"]
        result = []

        for index, item in enumerate(parsed_data["list"].values()):
            links = []

            for quality, link in item["hls"].items():

                if not link:
                    continue

                quality = self.__qualities.get(quality)
                link = f"{self.__domain}{link}"

                links.append(Link(quality, link))

            result.append(Episode(index, item["episode"], links, item.get("skips", {}).get("opening")))

        return result

    @staticmethod
    async def __create_links(episodes: list) -> str:
        """
        Returns a string of links to anime episodes with skips of openings in PlayerJs format.

        Parameters:
        - episodes [list]: Episode object list.

        Returns:
        - str: A string with all the episodes for PlayerJs.
        """
        result = []

        for episode in episodes:
            data = {}

            data.update({
                "title": f'{episode.name} episode',
                "file": ",".join([f'[{video.quality}p]{video.link}' for video in episode.links]),
                "id": f"id-{episode.id}"
            })

            if len(episode.opening) == 2:
                data.update({
                    "outside": [
                        {
                            "id": "skip-opening",
                            "from": episode.opening[0],
                            "to": episode.opening[1]
                        },
                        {
                            "id": "skip-opening-overlay",
                            "from": episode.opening[0],
                            "to": episode.opening[1]
                        }
                    ]
                })

            result.append(data)

        return dumps(result)

    @staticmethod
    async def __create_skips(episodes: list) -> dict:
        """
        Returns a dictionary with skip openings of all episodes with their ids.

        Parameters:
        - episodes [list]: Episode object list.

        Returns:
        - dict: Dictionary with skips of all episodes' openings.
        """
        result = {}

        for episode in episodes:
            result.update({
                f"id-{episode.id}": episode.opening
            })

        return result

    async def get_anime_by_code(self, code: str) -> dict:
        """
        Returns information about the anime.

        Parameters:
        - code [str]: Anime code from the link.

        Returns:
        - dict: Anime data.
        """
        result = await self.__request(f"https://api.anilibria.tv/v3/title?code={code}")
        return result

    async def get_data(self, code: str) -> tuple:
        """
        Returns episodes and skips data.

        Parameters:
        - code [str]: Anime code from the link.

        Returns:
        - tuple: Tuple of anime episodes and skips.
        """
        anime = await self.get_anime_by_code(code)
        episodes = await self.__extract_m3u8_links(anime)
        links = await self.__create_links(episodes)
        skips = await self.__create_skips(episodes)
        return links, skips
