"""Timeline schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class TimelineBase(BaseModel):
    """Base timeline schema."""
    title: str
    organization: str
    description: str
    type: str
    start_date: date
    end_date: Optional[date] = None
    location: Optional[str] = None
    icon: Optional[str] = None
    order: int = 0


class TimelineCreate(TimelineBase):
    """Create timeline schema."""
    pass


class TimelineUpdate(BaseModel):
    """Update timeline schema."""
    title: Optional[str] = None
    organization: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    location: Optional[str] = None
    icon: Optional[str] = None
    order: Optional[int] = None


class TimelineResponse(TimelineBase):
    """Timeline response schema."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
