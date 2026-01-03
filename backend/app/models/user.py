"""User DTOs."""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """DTO for creating a user."""
    email: EmailStr
    name: Optional[str] = None
    google_id: Optional[str] = None
    google_oauth_token: Optional[str] = None
    google_refresh_token: Optional[str] = None
    drive_folder_id: Optional[str] = None
    api_key: Optional[str] = None


class UserResponse(BaseModel):
    """DTO for user response."""
    id: int
    email: str
    name: Optional[str]
    created_at: datetime
    updated_at: datetime
    drive_folder_id: Optional[str] = None
    api_key: Optional[str] = None


    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """DTO for user login request."""
    email: EmailStr

