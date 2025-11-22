"""Project schemas."""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ProjectBase(BaseModel):
    """Base project schema."""
    title: str
    description: str
    long_description: Optional[str] = None
    technologies: List[str] = []
    badges: List[dict] = []
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    featured: bool = False
    order: int = 0


class ProjectCreate(ProjectBase):
    """Create project schema."""
    pass


class ProjectUpdate(BaseModel):
    """Update project schema."""
    title: Optional[str] = None
    description: Optional[str] = None
    long_description: Optional[str] = None
    technologies: Optional[List[str]] = None
    badges: Optional[List[dict]] = None
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    featured: Optional[bool] = None
    order: Optional[int] = None


class ProjectResponse(ProjectBase):
    """Project response schema."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
