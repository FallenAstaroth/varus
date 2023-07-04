from typing import List
from dataclasses import dataclass


@dataclass
class Episode:
    name: str
    href: str
    id: int


@dataclass
class Season:
    name: str
    episodes: List[Episode]
