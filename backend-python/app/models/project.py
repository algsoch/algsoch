"""Project model."""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class Project(Base):
    """Project database model."""
    
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    long_description = Column(Text)
    technologies = Column(JSON, default=[])  # List of tech stack
    badges = Column(JSON, default=[])  # List of badge objects
    github_url = Column(String)
    demo_url = Column(String)
    image_url = Column(String)
    category = Column(String)  # e.g., "AI/ML", "Full-Stack", "Backend"
    featured = Column(Integer, default=False)
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
