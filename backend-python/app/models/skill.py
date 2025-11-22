"""Skill model."""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Skill(Base):
    """Skill database model."""
    
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # e.g., "Backend", "Frontend", "AI/ML"
    icon = Column(String)  # Icon identifier or URL
    proficiency = Column(Integer, default=50)  # 0-100
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
