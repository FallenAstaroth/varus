from requests import get

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
    def get_anime_by_code(code: str):
        return get(f"https://api.anilibria.tv/v3/title?code={code}").json()

    @staticmethod
    def __format_links(episodes: list):
        return dumps([
            {
                "title": f'{episode["episode"]} серия',
                "file": ",".join([f'[{video["quality"]}p]{video["link"]}' for video in episode["links"]])
            }
            for episode in episodes]
        )

    def __extract_m3u8_links(self, data: dict):
        parsed_data = data["player"]
        result = []

        for item in parsed_data['list'].values():
            episode = item['episode']
            links = []

            for quality, link in item['hls'].items():

                if not link:
                    continue

                quality = self.__qualities.get(quality)
                link = f"{self.__video_domen}{link}"

                links.append({"quality": quality, "link": link})

            result.append({'episode': episode, 'links': links})

        return result

    def get_links(self, code: str):
        anime = self.get_anime_by_code(code)
        episodes = self.__extract_m3u8_links(anime)
        return self.__format_links(episodes)
