from fastapi import APIRouter, Depends, HTTPException
from app.services.n8n_service import N8NService
from app.utils.dependencies import get_user_by_api_key

router = APIRouter()

@router.post("/n8n/summarize")
async def summarize_file(file_id: str, user: dict = Depends(get_user_by_api_key)):
    n8n_service = N8NService()
    summary = await n8n_service.summarize_file(user["id"], file_id)
    return {"summary": summary}
