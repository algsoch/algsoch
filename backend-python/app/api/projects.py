"""Project endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_admin_user
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.activity import broadcast_activity

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("", response_model=List[ProjectResponse])
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    featured: bool = None,
    db: Session = Depends(get_db),
):
    """List all projects with optional filtering."""
    query = db.query(Project)
    
    if category:
        query = query.filter(Project.category == category)
    if featured is not None:
        query = query.filter(Project.featured == featured)
    
    projects = query.order_by(Project.order.desc(), Project.created_at.desc()).offset(skip).limit(limit).all()
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get a specific project by ID."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Create a new project (admin only)."""
    db_project = Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    # Broadcast activity
    await broadcast_activity({
        "event_type": "project_created",
        "payload": {"id": db_project.id, "title": db_project.title}
    })
    
    return db_project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project: ProjectUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Update a project (admin only)."""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_data = project.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
    
    db.commit()
    db.refresh(db_project)
    
    # Broadcast activity
    await broadcast_activity({
        "event_type": "project_updated",
        "payload": {"id": db_project.id, "title": db_project.title}
    })
    
    return db_project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Delete a project (admin only)."""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    title = db_project.title
    db.delete(db_project)
    db.commit()
    
    # Broadcast activity
    await broadcast_activity({
        "event_type": "project_deleted",
        "payload": {"id": project_id, "title": title}
    })
    
    return None
