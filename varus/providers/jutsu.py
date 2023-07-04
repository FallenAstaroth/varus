from requests import Session
from bs4 import BeautifulSoup

from varus.utils.dataclasses import Season, Episode


class JutSu:

    def __init__(self) -> None:
        self.__session = Session()
        self.__session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        })

    def set_headers(self, headers):
        self.__session.headers.update(headers)

    def get_all_seasons(self, url: str) -> list:
        slug = url.split("/")[3]
        main_page = self.__session.get(url)
        soup = BeautifulSoup(main_page.text, "html.parser")

        seasons = []
        for index, value in enumerate(soup.find_all("h2", {"class": "the-anime-season"})):
            season_episodes = soup.find_all("a", href=lambda href: href and href.startswith(f"/{slug}/season-{index + 1}/episode"))
            seasons.append(
                Season(
                    value.text,
                    [Episode(episode.text, f'https://jut.su{episode["href"]}', index + 1) for index, episode in enumerate(season_episodes)]
                )
            )

        return seasons

    def get_episode(self, href: str) -> list:
        episode_page = self.__session.get(href)
        soup = BeautifulSoup(episode_page.text, "html.parser")

        links = []
        for resolution in ["1080", "720", "480", "360"]:
            source = soup.find("source", {"res": resolution})
            source = source if source else soup.find("source")
            if source:
                links.append({"quality": resolution, "link": source.attrs["src"]})

        return links

    @staticmethod
    def format_links(files: list):
        return ",".join([f'[{file["quality"]}p]{file["link"]}' for file in files])

    @staticmethod
    def format_seasons(seasons):

        episodes = []

        for season in seasons:
            for episode in season.episodes:
                episodes.append({
                    "name": episode.name,
                    "link": episode.href
                })

        return episodes
