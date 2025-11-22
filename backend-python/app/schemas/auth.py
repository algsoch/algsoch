"""Authentication schemas."""
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Login request schema."""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""
    refresh_token: str


class UserResponse(BaseModel):
    """User response schema."""
    id: int
    username: str
    email: str
    is_admin: bool
    is_active: bool
    
    class Config:
        from_attributes = True
