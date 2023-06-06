def get_label_by_sex(label: str, sex: str):
    labels = {
        "join": {
            "male": "Присоединился",
            "female": "Присоединилась",
            "undefined": "Присоединилось"
        },
        "left": {
            "male": "Покинул",
            "female": "Покинула",
            "undefined": "Покинуло"
        }
    }

    return labels.get(label, {}).get(sex, "Undefined")
