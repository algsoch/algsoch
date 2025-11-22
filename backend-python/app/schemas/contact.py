"""Contact schemas."""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class ContactBase(BaseModel):
    """Base contact schema."""
    name: str
    email: EmailStr
    subject: str
    message: str


class ContactCreate(ContactBase):
    """Create contact schema."""
    pass


class ContactResponse(ContactBase):
    """Contact response schema."""
    id: int
    read: bool
    replied: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
