"""Skill endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_admin_user
from app.models.skill import Skill
from app.models.user import User
from app.schemas.skill import SkillCreate, SkillUpdate, SkillResponse
from app.services.activity import broadcast_activity

router = APIRouter(prefix="/api/skills", tags=["skills"])


@router.get("", response_model=List[SkillResponse])
async def list_skills(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    db: Session = Depends(get_db),
):
    """List all skills with optional filtering."""
    query = db.query(Skill)
    
    if category:
        query = query.filter(Skill.category == category)
    
    skills = query.order_by(Skill.order.desc(), Skill.name).offset(skip).limit(limit).all()
    return skills


@router.get("/{skill_id}", response_model=SkillResponse)
async def get_skill(skill_id: int, db: Session = Depends(get_db)):
    """Get a specific skill by ID."""
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


@router.post("", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
async def create_skill(
    skill: SkillCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Create a new skill (admin only)."""
    db_skill = Skill(**skill.model_dump())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    
    await broadcast_activity({
        "event_type": "skill_created",
        "payload": {"id": db_skill.id, "name": db_skill.name}
    })
    
    return db_skill


@router.put("/{skill_id}", response_model=SkillResponse)
async def update_skill(
    skill_id: int,
    skill: SkillUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Update a skill (admin only)."""
    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    update_data = skill.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_skill, key, value)
    
    db.commit()
    db.refresh(db_skill)
    
    await broadcast_activity({
        "event_type": "skill_updated",
        "payload": {"id": db_skill.id, "name": db_skill.name}
    })
    
    return db_skill


@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(
    skill_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Delete a skill (admin only)."""
    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    name = db_skill.name
    db.delete(db_skill)
    db.commit()
    
    await broadcast_activity({
        "event_type": "skill_deleted",
        "payload": {"id": skill_id, "name": name}
    })
    
    return None
