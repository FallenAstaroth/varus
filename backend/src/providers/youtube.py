from json import dumps


class Youtube:

    def __init__(self):
        ...

    @staticmethod
    async def __create_links(links: list):
        """
        Returns a string of links to YouTube videos in PlayerJs format.

        Parameters:
        - episodes [list]: Episode object list.

        Returns:
        - str: A string with all the videos for PlayerJs.
        """
        return dumps([
            {
                "title": "Youtube",
                "file": link.split("?")[0]
            }
            for link in links]
        )

    async def get_data(self, links: list) -> str:
        """
        Returns videos.

        Parameters:
        - links [list]: List of YouTube links.

        Returns:
        - str: String of YouTube videos.
        """
        result = await self.__create_links(links)
        return result
