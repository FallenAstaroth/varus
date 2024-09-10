from utils.enums import UserEvent


class Labeler:

    @staticmethod
    def get_event(label: UserEvent, sex: str) -> str:
        """
        Returns the text of the event.

        Parameters:
        - label [UserEvent]: Label for search.
        - sex [str]: The gender for which to find a label.

        Returns:
        - str: Event text.
        """
        labels = {
            UserEvent.CONNECT: {
                "male": "joined the room (male)",
                "female": "joined the room (female)",
                "undefined": "joined the room (undefined)"
            },
            UserEvent.DISCONNECT: {
                "male": "left the room (male)",
                "female": "left the room (female)",
                "undefined": "left the room (undefined)"
            },
            UserEvent.PLAY: {
                "male": "started the player (male)",
                "female": "started the player (female)",
                "undefined": "started the player (undefined)"
            },
            UserEvent.PAUSE: {
                "male": "paused the player (male)",
                "female": "paused the player (female)",
                "undefined": "paused the player (undefined)"
            },
            UserEvent.SEEK: {
                "male": "rewound the player (male)",
                "female": "rewound the player (female)",
                "undefined": "rewound the player (undefined)"
            },
            UserEvent.SKIP: {
                "male": "skipped the opening (male)",
                "female": "skipped the opening (female)",
                "undefined": "skipped the opening (undefined)"
            },
            UserEvent.SWITCH: {
                "male": "switched the episode (male)",
                "female": "switched the episode (female)",
                "undefined": "switched the episode (undefined)"
            }
        }

        return labels.get(label, {}).get(sex, "undefined")

    @staticmethod
    def get_error(error: str) -> str:
        """
        Returns the text of the error.

        Parameters:
        - error [str]: Error label for search.

        Returns:
        - str: Error text.
        """
        errors = {
            "name": "Enter a name",
            "code_not_specified": "Enter room code",
            "links": "Enter link",
            "code_not_exist": "Such a room does not exist"
        }

        return errors.get(error, "undefined")
