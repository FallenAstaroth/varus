from typing import List, Optional
from dataclasses import dataclass, asdict, field


@dataclass
class Link:
    quality: str
    link: str


@dataclass
class Episode:
    id: int
    name: str
    links: List[Link]
    opening: Optional[List[int]]


@dataclass
class User:
    room: str
    name: str
    color: str
    sex: str

    def dict(self):
        return {key: value for key, value in asdict(self).items()}
