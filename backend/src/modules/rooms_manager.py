from random import choice
from string import ascii_letters, digits


class RoomsManager:

    def __init__(self):
        self.__rooms = {}
        self.__symbols = ascii_letters + digits

    @property
    def rooms(self):
        return self.__rooms

    async def __generate_room_code(self, length):
        while True:
            code = ''.join(choice(self.__symbols) for _ in range(length))
            if code in self.__rooms:
                continue
            return code

    async def create_room(self, videos: str):
        code = await self.__generate_room_code(10)
        self.__rooms.update({
            code: {
                "count": 0,
                "videos": videos,
                "last_message_id": 1,
                "languages": set()
            }
        })
        return code

    async def get_room(self, code: str):
        return self.__rooms.get(code, None)

    async def check_room(self, code: str):
        room = self.__rooms.get(code, None)
        return True if room else False
