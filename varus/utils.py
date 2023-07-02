from flask_babel import gettext


def get_label_by_sex(label: str, sex: str):
    labels = {
        "join": {
            "male": gettext("joined the room (male)"),
            "female": gettext("joined the room (female)"),
            "undefined": gettext("joined the room (undefined)")
        },
        "left": {
            "male": gettext("left the room (male)"),
            "female": gettext("left the room (female)"),
            "undefined": gettext("left the room (undefined)")
        },
        "play": {
            "male": gettext("started the player (male)"),
            "female": gettext("started the player (female)"),
            "undefined": gettext("started the player (undefined)")
        },
        "stop": {
            "male": gettext("paused the player (male)"),
            "female": gettext("paused the player (female)"),
            "undefined": gettext("paused the player (undefined)")
        },
        "seek": {
            "male": gettext("rewound the player (male)"),
            "female": gettext("rewound the player (female)"),
            "undefined": gettext("rewound the player (undefined)")
        }
    }

    return labels.get(label, {}).get(sex, "undefined")


def get_error(error: str):
    errors = {
        "name": gettext("Enter a name"),
        "code_not_specified": gettext("Enter room code"),
        "links": gettext("Enter link"),
        "code_not_exist": gettext("Such a room does not exist")
    }

    return errors.get(error, "undefined")
