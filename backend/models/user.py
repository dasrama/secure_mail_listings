from pydantic import BaseModel, Field, EmailStr
from beanie import Document
from datetime import datetime


class User(Document, BaseModel):
    email: EmailStr
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.now)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class CreateUser(UserLogin):
    pass
