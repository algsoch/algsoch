"""Timeline endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_admin_user
from app.models.timeline import Timeline
from app.models.user import User
from app.schemas.timeline import TimelineCreate, TimelineUpdate, TimelineResponse
from app.services.activity import broadcast_activity

router = APIRouter(prefix="/api/timeline", tags=["timeline"])


@router.get("", response_model=List[TimelineResponse])
async def list_timeline(
    skip: int = 0,
    limit: int = 100,
    type: str = None,
    db: Session = Depends(get_db),
):
    """List all timeline events."""
    query = db.query(Timeline)
    
    if type:
        query = query.filter(Timeline.type == type)
    
    events = query.order_by(Timeline.start_date.desc()).offset(skip).limit(limit).all()
    return events


@router.get("/{event_id}", response_model=TimelineResponse)
async def get_timeline_event(event_id: int, db: Session = Depends(get_db)):
    """Get a specific timeline event."""
    event = db.query(Timeline).filter(Timeline.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Timeline event not found")
    return event


@router.post("", response_model=TimelineResponse, status_code=status.HTTP_201_CREATED)
async def create_timeline_event(
    event: TimelineCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Create a new timeline event (admin only)."""
    db_event = Timeline(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    await broadcast_activity({
        "event_type": "timeline_created",
        "payload": {"id": db_event.id, "title": db_event.title}
    })
    
    return db_event


@router.put("/{event_id}", response_model=TimelineResponse)
async def update_timeline_event(
    event_id: int,
    event: TimelineUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Update a timeline event (admin only)."""
    db_event = db.query(Timeline).filter(Timeline.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Timeline event not found")
    
    update_data = event.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_event, key, value)
    
    db.commit()
    db.refresh(db_event)
    
    await broadcast_activity({
        "event_type": "timeline_updated",
        "payload": {"id": db_event.id, "title": db_event.title}
    })
    
    return db_event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_timeline_event(
    event_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Delete a timeline event (admin only)."""
    db_event = db.query(Timeline).filter(Timeline.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Timeline event not found")
    
    title = db_event.title
    db.delete(db_event)
    db.commit()
    
    await broadcast_activity({
        "event_type": "timeline_deleted",
        "payload": {"id": event_id, "title": title}
    })
    
    return None
