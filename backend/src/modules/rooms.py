from typing import Union
from random import choice
from string import ascii_letters, digits

from backend.src.types.enums import UserEvent
from backend.src.types.dataclasses import Room, Users, Messages, Last


class RoomsManager:

    def __init__(self):
        self.__rooms = {}
        self.__symbols = ascii_letters + digits

    @property
    def rooms(self) -> dict:
        return self.__rooms

    async def __generate_room_code(self, length: int) -> str:
        """
        Generates a unique room code.

        Parameters:
        - length [int]: Length of generated code.

        Returns:
        - str: Unique room code.
        """
        while True:
            code = ''.join(choice(self.__symbols) for _ in range(length))

            if code in self.__rooms:
                continue

            return code

    async def create_room(self, videos: str) -> str:
        """
        Creates a new room.

        Parameters:
        - videos [str]: Videos of the current room in PlayerJs str format.

        Returns:
        - str: Code of the created room.
        """
        code = await self.__generate_room_code(10)

        self.__rooms.update({
            code: Room(
                videos=videos,
                skips={},
                users=Users(count=0),
                messages=Messages(Last(id=1, user="", event=UserEvent.DEFAULT), count=0)
            )
        })

        return code

    async def get_room(self, code: str) -> Union[dict, None]:
        """
        Returns the room data.

        Parameters:
        - code [str]: Room code for search.

        Returns:
        - dict: Room data.
        """
        return self.__rooms.get(code, None)

    async def check_room(self, code: str) -> bool:
        """
        Checks if the room exists.

        Parameters:
        - code [str]: Room code for search.

        Returns:
        - bool: True if it exists, False if it doesn't.
        """
        room = self.__rooms.get(code, None)
        return True if room else False
