from pydantic import BaseModel


class TokenForm(BaseModel):
    media_url: str
    owner: str
