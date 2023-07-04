from flask_babel import gettext, force_locale


def get_label_by_sex(label: str, sex: str, locale: str):
    labels = {
        "connect": {
            "male": "joined the room (male)",
            "female": "joined the room (female)",
            "undefined": "joined the room (undefined)"
        },
        "disconnect": {
            "male": "left the room (male)",
            "female": "left the room (female)",
            "undefined": "left the room (undefined)"
        },
        "play": {
            "male": "started the player (male)",
            "female": "started the player (female)",
            "undefined": "started the player (undefined)"
        },
        "pause": {
            "male": "paused the player (male)",
            "female": "paused the player (female)",
            "undefined": "paused the player (undefined)"
        },
        "seek": {
            "male": "rewound the player (male)",
            "female": "rewound the player (female)",
            "undefined": "rewound the player (undefined)"
        }
    }

    with force_locale(locale):
        return gettext(labels.get(label, {}).get(sex, "undefined"))


def get_error(error: str):
    errors = {
        "name": gettext("Enter a name"),
        "code_not_specified": gettext("Enter room code"),
        "links": gettext("Enter link"),
        "code_not_exist": gettext("Such a room does not exist")
    }

    return errors.get(error, "undefined")
