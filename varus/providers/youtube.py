from json import dumps


class Youtube:

    def __init__(self):
        ...

    @staticmethod
    def __format_links(links: list):
        return dumps([
            {
                "title": "Youtube",
                "file": link
            }
            for link in links]
        )

    def get_links(self, links: list):
        return self.__format_links(links)
