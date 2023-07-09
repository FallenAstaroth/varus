from pydantic import BaseModel


class RoomGetRequest(BaseModel):
    code: str
