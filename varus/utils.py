def get_label_by_sex(label: str, sex: str):
    labels = {
        "join": {
            "male": "присоединился к комнате",
            "female": "присоединилась к комнате",
            "undefined": "присоединилось к комнате"
        },
        "left": {
            "male": "покинул комнату",
            "female": "покинула комнату",
            "undefined": "покинуло комнату"
        },
        "play": {
            "male": "включил плеер",
            "female": "включила плеер",
            "undefined": "включило плеер"
        },
        "stop": {
            "male": "остановил плеер",
            "female": "остановила плеер",
            "undefined": "остановило плеер"
        },
        "seek": {
            "male": "перемотал плеер",
            "female": "перемотала плеер",
            "undefined": "перемотало плеер"
        }
    }

    return labels.get(label, {}).get(sex, "Undefined")
