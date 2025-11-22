"""Contact endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_admin_user
from app.models.contact import Contact
from app.models.user import User
from app.schemas.contact import ContactCreate, ContactResponse
from app.services.activity import broadcast_activity

router = APIRouter(prefix="/api/contact", tags=["contact"])


@router.post("", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact_message(
    contact: ContactCreate,
    db: Session = Depends(get_db),
):
    """Submit a contact form message."""
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    
    await broadcast_activity({
        "event_type": "contact_received",
        "payload": {"id": db_contact.id, "name": db_contact.name, "subject": db_contact.subject}
    })
    
    return db_contact


@router.get("", response_model=List[ContactResponse])
async def list_contact_messages(
    skip: int = 0,
    limit: int = 100,
    read: bool = None,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """List all contact messages (admin only)."""
    query = db.query(Contact)
    
    if read is not None:
        query = query.filter(Contact.read == read)
    
    messages = query.order_by(Contact.created_at.desc()).offset(skip).limit(limit).all()
    return messages


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact_message(
    contact_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Get a specific contact message (admin only)."""
    message = db.query(Contact).filter(Contact.id == contact_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Contact message not found")
    
    # Mark as read
    if not message.read:
        message.read = True
        db.commit()
    
    return message


@router.patch("/{contact_id}/replied")
async def mark_as_replied(
    contact_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Mark a contact message as replied (admin only)."""
    message = db.query(Contact).filter(Contact.id == contact_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Contact message not found")
    
    message.replied = True
    message.read = True
    db.commit()
    
    return {"status": "success", "message": "Marked as replied"}


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact_message(
    contact_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Delete a contact message (admin only)."""
    message = db.query(Contact).filter(Contact.id == contact_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Contact message not found")
    
    db.delete(message)
    db.commit()
    
    return None
