from db.models import *
from pydantic import BaseModel


class TokenForm(BaseModel):
    media_url: str
    owner: str


class TokenInDB(BaseModel):
    id: int
    unique_hash: str
    tx_hash: str = None
    media_url: str
    owner: str

    class Config:
        orm_mode = True
