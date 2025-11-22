"""Skill schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SkillBase(BaseModel):
    """Base skill schema."""
    name: str
    category: str
    icon: Optional[str] = None
    proficiency: int = 50
    order: int = 0


class SkillCreate(SkillBase):
    """Create skill schema."""
    pass


class SkillUpdate(BaseModel):
    """Update skill schema."""
    name: Optional[str] = None
    category: Optional[str] = None
    icon: Optional[str] = None
    proficiency: Optional[int] = None
    order: Optional[int] = None


class SkillResponse(SkillBase):
    """Skill response schema."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
