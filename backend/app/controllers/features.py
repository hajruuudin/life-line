"""Feature flags controller."""
from fastapi import APIRouter
from app.config import settings

router = APIRouter()


@router.get("")
async def get_feature_flags():
    """Get all feature flags for the frontend."""
    return {
        "ai_chat_enabled": settings.feature_ai_chat_enabled,
        "ai_illness_suggestions_enabled": settings.feature_ai_illness_suggestions_enabled,
        "ai_drive_enabled": settings.feature_ai_drive_enabled,
    }
