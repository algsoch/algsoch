"""Blog schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BlogBase(BaseModel):
    """Base blog schema."""
    title: str
    slug: str
    content: str
    excerpt: Optional[str] = None
    tags: Optional[str] = None
    published: bool = False


class BlogCreate(BlogBase):
    """Create blog schema."""
    pass


class BlogUpdate(BaseModel):
    """Update blog schema."""
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    tags: Optional[str] = None
    published: Optional[bool] = None


class BlogResponse(BlogBase):
    """Blog response schema."""
    id: int
    views: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
