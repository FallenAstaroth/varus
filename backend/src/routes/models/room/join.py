from pydantic import BaseModel

from typing import Optional


class RoomJoinRequest(BaseModel):
    name: str
    color: str
    sex: str
    code: Optional[str] = None
