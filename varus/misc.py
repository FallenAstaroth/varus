from flask import Flask
from flask_babel import Babel
from flask_socketio import SocketIO

from os import path

from modules import Manager, Translator
from providers import Youtube, Anilibria
from config import SECRET_KEY, LANGUAGES


app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["LANGUAGES"] = LANGUAGES
app.config["BABEL_TRANSLATION_DIRECTORIES"] = path.join(path.abspath(path.dirname(__file__)), "i18n")

socketio = SocketIO(app)
translator = Translator()
manager = Manager(app)
babel = Babel(app, locale_selector=manager.get_locale)
youtube = Youtube()
anilibria = Anilibria()
