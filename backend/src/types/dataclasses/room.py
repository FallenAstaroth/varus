from typing import Optional
from dataclasses import dataclass


@dataclass
class Last:
    id: int
    user: str
    event: str


@dataclass
class Messages:
    last: Last
    count: int


@dataclass
class Users:
    count: int


@dataclass
class Room:
    users: Users
    messages: Messages
    videos: str
    skips: Optional[dict]
