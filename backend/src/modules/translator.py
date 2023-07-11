class Translator:

    @staticmethod
    def get_event(label: str, sex: str):
        labels = {
            "join": {
                "male": "joined the room (male)",
                "female": "joined the room (female)",
                "undefined": "joined the room (undefined)"
            },
            "left": {
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

        return labels.get(label, {}).get(sex, "undefined")

    @staticmethod
    def get_error(error: str):
        errors = {
            "name": "Enter a name",
            "code_not_specified": "Enter room code",
            "links": "Enter link",
            "code_not_exist": "Such a room does not exist"
        }

        return errors.get(error, "undefined")