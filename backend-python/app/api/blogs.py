"""Blog endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_admin_user
from app.models.blog import Blog
from app.models.user import User
from app.schemas.blog import BlogCreate, BlogUpdate, BlogResponse
from app.services.activity import broadcast_activity

router = APIRouter(prefix="/api/blogs", tags=["blogs"])


@router.get("", response_model=List[BlogResponse])
async def list_blogs(
    skip: int = 0,
    limit: int = 100,
    published: bool = None,
    db: Session = Depends(get_db),
):
    """List all blogs."""
    query = db.query(Blog)
    
    if published is not None:
        query = query.filter(Blog.published == published)
    
    blogs = query.order_by(Blog.created_at.desc()).offset(skip).limit(limit).all()
    return blogs


@router.get("/{blog_id}", response_model=BlogResponse)
async def get_blog(blog_id: int, db: Session = Depends(get_db)):
    """Get a specific blog post."""
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    # Increment views
    blog.views += 1
    db.commit()
    
    return blog


@router.get("/slug/{slug}", response_model=BlogResponse)
async def get_blog_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get a blog post by slug."""
    blog = db.query(Blog).filter(Blog.slug == slug).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    # Increment views
    blog.views += 1
    db.commit()
    
    return blog


@router.post("", response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
async def create_blog(
    blog: BlogCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Create a new blog post (admin only)."""
    # Check if slug already exists
    existing = db.query(Blog).filter(Blog.slug == blog.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Blog with this slug already exists")
    
    db_blog = Blog(**blog.model_dump())
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    
    await broadcast_activity({
        "event_type": "blog_created",
        "payload": {"id": db_blog.id, "title": db_blog.title}
    })
    
    return db_blog


@router.put("/{blog_id}", response_model=BlogResponse)
async def update_blog(
    blog_id: int,
    blog: BlogUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Update a blog post (admin only)."""
    db_blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not db_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    update_data = blog.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_blog, key, value)
    
    db.commit()
    db.refresh(db_blog)
    
    await broadcast_activity({
        "event_type": "blog_updated",
        "payload": {"id": db_blog.id, "title": db_blog.title}
    })
    
    return db_blog


@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(
    blog_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Delete a blog post (admin only)."""
    db_blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not db_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    title = db_blog.title
    db.delete(db_blog)
    db.commit()
    
    await broadcast_activity({
        "event_type": "blog_deleted",
        "payload": {"id": blog_id, "title": title}
    })
    
    return None
