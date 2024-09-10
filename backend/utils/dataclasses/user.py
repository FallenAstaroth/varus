from dataclasses import dataclass, asdict


@dataclass
class User:
    room: str
    name: str
    color: str
    sex: str

    async def dict(self):
        return {key: value for key, value in asdict(self).items()}
