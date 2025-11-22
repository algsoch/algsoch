"""Main application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging

from app.core.config import settings
from app.core.database import init_db, get_db
from app.core.security import get_password_hash
from app.models.user import User

# Import routers
from app.api import auth, projects, skills, timeline, blogs, contact, realtime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Complete portfolio platform API with real-time features",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include routers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(skills.router)
app.include_router(timeline.router)
app.include_router(blogs.router)
app.include_router(contact.router)
app.include_router(realtime.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database and create default admin user."""
    logger.info("Starting application...")
    
    # Initialize database tables
    init_db()
    logger.info("Database tables initialized")
    
    # Create default admin user if not exists
    db = next(get_db())
    try:
        admin = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
        if not admin:
            admin = User(
                username=settings.ADMIN_USERNAME,
                email=settings.ADMIN_EMAIL,
                hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
                is_admin=True,
                is_active=True,
            )
            db.add(admin)
            db.commit()
            logger.info(f"Created default admin user: {settings.ADMIN_USERNAME}")
        else:
            logger.info("Admin user already exists")
    finally:
        db.close()
    
    logger.info("Application started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down application...")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/api/health")
async def api_health():
    """API health check."""
    return {
        "status": "healthy",
        "service": "api",
    }
