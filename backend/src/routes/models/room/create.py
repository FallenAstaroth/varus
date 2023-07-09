from pydantic import BaseModel

from typing import Optional


class RoomCreateRequest(BaseModel):
    name: str
    color: str
    sex: str
    link: Optional[str] = None
