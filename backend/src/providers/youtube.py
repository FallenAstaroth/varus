from json import dumps


class Youtube:

    def __init__(self):
        ...

    @staticmethod
    async def __format_links(links: list):
        return dumps([
            {
                "title": "Youtube",
                "file": link
            }
            for link in links]
        )

    async def get_links(self, links: list):
        result = await self.__format_links(links)
        return result
