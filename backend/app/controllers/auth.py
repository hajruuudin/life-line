"""Authentication controller."""
import logging
from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel
from app.services.auth_service import AuthService
from app.models.auth import Token
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


class CallbackRequest(BaseModel):
    """Request model for OAuth callback."""
    code: str


@router.get("/google-login")
async def google_login():
    """Initiate Google OAuth login flow."""
    try:
        auth_url = AuthService.get_google_oauth_url()
        return {"auth_url": auth_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate authorization URL")


@router.post("/callback")
async def google_callback_post(request: CallbackRequest):
    """Handle Google OAuth callback via POST (from frontend)."""
    try:
        result = AuthService.handle_google_callback(request.code)
        return {
            "access_token": result["access_token"],
            "token_type": "bearer",
            "user": result["user"],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))