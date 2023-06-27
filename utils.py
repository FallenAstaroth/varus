def get_label_by_sex(label: str, sex: str):
    labels = {
        "join": {
            "male": "Присоединился к комнате",
            "female": "Присоединилась к комнате",
            "undefined": "Присоединилось к комнате"
        },
        "left": {
            "male": "Покинул комнату",
            "female": "Покинула комнату",
            "undefined": "Покинуло комнату"
        },
        "play": {
            "male": "Включил плеер",
            "female": "Включила плеер",
            "undefined": "Включило плеер"
        },
        "stop": {
            "male": "Остановил плеер",
            "female": "Остановила плеер",
            "undefined": "Остановило плеер"
        },
        "seek": {
            "male": "Перемотал плеер",
            "female": "Перемотала плеер",
            "undefined": "Перемотало плеер"
        }
    }

    return labels.get(label, {}).get(sex, "Undefined")
