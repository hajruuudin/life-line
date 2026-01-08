"""Google Drive controller."""
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from typing import List, Dict, Any
from app.services.n8n_service import N8NService
from app.services.google_drive_service import GoogleDriveService
from app.utils.dependencies import get_current_user

router = APIRouter()


@router.get("/files")
async def list_drive_files(current_user: dict = Depends(get_current_user)):
    """
    List files from the user's 'LifeLine Records' folder in Google Drive.
    
    Returns empty list if credentials not set up.
    """
    try:
        files = GoogleDriveService.list_files(current_user["id"])
        return {"files": files, "connected": True}
    except ValueError as e:
        # Credentials not found
        return {"files": [], "connected": False, "message": str(e)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing files: {str(e)}",
        )


@router.post("/upload")
async def upload_file_to_drive(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """
    Upload a file to the user's 'LifeLine Records' folder in Google Drive.
    """
    try:
        # Read file content before uploading
        file_content = await file.read()
        
        uploaded_file = GoogleDriveService.upload_file(
            user_id=current_user["id"],
            file=file.file,
            file_name=file.filename,
            mimetype=file.content_type
        )

        # Try to decode as text, fallback to base64 for binary files
        await file.seek(0)
        file_bytes = await file.read()

        N8NService.trigger_file_summary(
            user_email=current_user["email"],
            user_id=current_user["id"],
            file_name=file.filename,
            file_bytes=file_bytes,  # Send raw bytes, not text
            mimetype=file.content_type
        )

        return {"file": uploaded_file, "message": "File uploaded and processed successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading file: {str(e)}",
        )


@router.delete("/files/{file_id}")
async def delete_drive_file(file_id: str, current_user: dict = Depends(get_current_user)):
    """
    Delete a file from the user's 'LifeLine Records' folder in Google Drive.
    """
    try:
        GoogleDriveService.delete_file(user_id=current_user["id"], file_id=file_id)
        return {"message": "File deleted successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting file: {str(e)}",
        )

