from pydantic import BaseModel, EmailStr, Field
from beanie import Document
from typing import Optional, Any
from datetime import datetime


class Email(Document, BaseModel):
    email_address: EmailStr
    subject : str = " "
    timestamp: datetime = Field(default_factory=datetime.now)
    documents: Optional[Any]

class CreateEmail(BaseModel):
    email_address: EmailStr
    subject: str = " "
    documents: Optional[Any] = None
