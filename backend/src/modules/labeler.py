class Labeler:

    @staticmethod
    def get_event(label: str, sex: str) -> str:
        """
        Returns the text of the event.

        Parameters:
        - label [str]: Label for search.
        - sex [str]: The gender for which to find a label.

        Returns:
        - str: Event text.
        """
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
            },
            "skip": {
                "male": "skipped the opening (male)",
                "female": "skipped the opening (female)",
                "undefined": "skipped the opening (undefined)"
            },
            "switch": {
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
