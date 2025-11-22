"""Timeline model."""
from sqlalchemy import Column, Integer, String, Text, Date, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Timeline(Base):
    """Timeline event database model."""
    
    __tablename__ = "timeline"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    organization = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    type = Column(String, nullable=False)  # "education", "work", "achievement"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)  # null if ongoing
    location = Column(String)
    icon = Column(String)
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
