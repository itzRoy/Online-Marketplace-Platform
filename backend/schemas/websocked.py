from fastapi import WebSocket
from pydantic import BaseModel


class ConnectedUser(BaseModel):
    is_superuser: bool
    connection: WebSocket

    class Config:
        arbitrary_types_allowed = True
