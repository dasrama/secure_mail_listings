from pydantic import BaseModel
from beanie import Document
from datetime import datetime
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str   

class TokenData(BaseModel):
    id: Optional[int]

class GoogleToken(Document):
    email: str
    access_token: str
    refresh_token: Optional[str]
    expires_in: int
    token_type: str
    scope: str
    created_at: datetime
