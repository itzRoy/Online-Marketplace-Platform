from odmantic import ObjectId
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str


class TokenPayload(BaseModel):
    sub: ObjectId | None = None
