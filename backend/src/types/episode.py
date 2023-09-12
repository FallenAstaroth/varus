from typing import List, Optional
from dataclasses import dataclass


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
