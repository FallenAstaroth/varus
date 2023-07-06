from flask import request, session

from random import choice
from string import ascii_uppercase


class Manager:

    def __init__(self, app):
        self.__app = app
        self.__rooms = {}

    @property
    def rooms(self):
        return self.__rooms

    def generate_room_code(self, length):
        while True:
            code = ''.join(choice(ascii_uppercase) for _ in range(length))
            if code in self.__rooms:
                continue
            return code

    def get_locale(self):
        language = session.get("language")

        if language:
            return language

        locale = request.accept_languages.best_match(self.__app.config["LANGUAGES"].keys())
        session.update({"language": locale})

        return locale
