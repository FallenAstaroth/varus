from flask import request, session

from random import choice
from string import ascii_uppercase

from varus.utils.enums import Providers


class Manager:

    def __init__(self, app, jutsu):
        self.__app = app
        self.__jutsu = jutsu
        self.__rooms = {}

    @property
    def rooms(self) -> dict:
        return self.__rooms

    def generate_room_code(self, length) -> str:
        while True:
            code = ''.join(choice(ascii_uppercase) for _ in range(length))
            if code in self.__rooms:
                continue
            return code

    def get_locale(self) -> str:
        language = session.get("language")

        if language:
            return language

        locale = request.accept_languages.best_match(self.__app.config["LANGUAGES"].keys())
        session.update({"language": locale})

        return locale
