"""Google Drive service."""
from typing import List, Dict, Any, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from app.config import settings
from app.dao.google_credentials_dao import GoogleCredentialsDAO
from app.dao.user_dao import UserDAO
from datetime import datetime, timezone, timedelta
import io
import logging

logger = logging.getLogger(__name__)


class GoogleDriveService:
    """Business logic for Google Drive integration."""
    
    @staticmethod
    def _ensure_naive_utc(dt: Optional[datetime]) -> Optional[datetime]:
        """Ensure datetime is naive UTC (Google auth library expects naive UTC)."""
        if dt is None:
            return None
        if dt.tzinfo is not None:
            # Convert to UTC and remove timezone info
            return dt.astimezone(timezone.utc).replace(tzinfo=None)
        return dt
    
    @staticmethod
    def get_credentials(user_id: int) -> Optional[Credentials]:
        """Get Google credentials for a user."""
        creds_data = GoogleCredentialsDAO.get_credentials_by_user_id(user_id)
        if not creds_data:
            return None
        
        # Google auth library expects naive UTC datetime for expiry
        token_expiry = GoogleDriveService._ensure_naive_utc(creds_data["token_expiry"])
        
        return Credentials(
            token=creds_data["access_token"],
            refresh_token=creds_data["refresh_token"],
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.google_client_id,
            client_secret=settings.google_client_secret,
            scopes=[
                "https://www.googleapis.com/auth/drive",
                "https://www.googleapis.com/auth/calendar",
            ],
            expiry=token_expiry,
        )
    
    @staticmethod
    def _refresh_credentials_if_needed(credentials: Credentials, user_id: int) -> Credentials:
        """Refresh credentials if expired or expiring soon (within 5 minutes)."""
        if not credentials.refresh_token:
            logger.warning(f"No refresh token available for user {user_id}")
            return credentials
        
        needs_refresh = False
        now = datetime.utcnow()  # Use naive UTC to match Google's internal comparison
        
        # Check if expired or expiring soon
        if credentials.expiry:
            time_until_expiry = credentials.expiry - now
            if time_until_expiry.total_seconds() < 300:  # Less than 5 minutes
                needs_refresh = True
                if time_until_expiry.total_seconds() <= 0:
                    logger.info(f"Credentials expired for user {user_id}, refreshing...")
                else:
                    logger.info(f"Credentials expiring soon for user {user_id}, refreshing...")
        elif credentials.expired:
            needs_refresh = True
            logger.info(f"Credentials marked as expired for user {user_id}, refreshing...")
        
        if needs_refresh:
            try:
                credentials.refresh(Request())
                # Store expiry as-is (naive UTC) since that's what Google returns
                GoogleCredentialsDAO.create_or_update_credentials(
                    user_id=user_id,
                    access_token=credentials.token,
                    refresh_token=credentials.refresh_token or credentials._refresh_token,
                    token_expiry=credentials.expiry if credentials.expiry else datetime.utcnow() + timedelta(hours=1),
                )
                logger.info(f"Successfully refreshed credentials for user {user_id}")
            except Exception as e:
                logger.error(f"Failed to refresh credentials for user {user_id}: {e}")
                raise
        
        return credentials

    @staticmethod
    def find_or_create_app_folder(user_id: int, credentials: Optional[Credentials], connection=None) -> str:
        """Find or create the 'LifeLine Records' folder and return its ID."""
        if not credentials:
            raise ValueError("Google credentials not found. Please authenticate first.")

        service = build("drive", "v3", credentials=credentials)
        
        # Search for the folder
        query = "name='LifeLine Records' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = service.files().list(q=query, spaces="drive", fields="files(id, name)").execute()
        files = results.get("files", [])
        
        if files:
            # Folder exists
            folder_id = files[0].get("id")
            UserDAO.update_drive_folder_id(user_id, folder_id, connection=connection)
            return folder_id
        else:
            # Folder does not exist, create it
            file_metadata = {
                "name": "LifeLine Records",
                "mimeType": "application/vnd.google-apps.folder"
            }
            folder = service.files().create(body=file_metadata, fields="id").execute()
            folder_id = folder.get("id")
            UserDAO.update_drive_folder_id(user_id, folder_id, connection=connection)
            return folder_id

    
    @staticmethod
    def list_files(user_id: int) -> List[Dict[str, Any]]:
        """
        List files from the user's 'LifeLine Records' folder in Google Drive.
        """
        credentials = GoogleDriveService.get_credentials(user_id)
        if not credentials:
            raise ValueError("Google credentials not found. Please authenticate first.")

        user = UserDAO.get_user_by_id(user_id)
        if not user or not user.get("drive_folder_id"):
            # This should ideally not happen if the login flow is correct
            raise ValueError("Drive folder ID not found for user.")

        drive_folder_id = user["drive_folder_id"]

        # Refresh token if needed
        credentials = GoogleDriveService._refresh_credentials_if_needed(credentials, user_id)
        
        service = build("drive", "v3", credentials=credentials)
        query = f"'{drive_folder_id}' in parents and trashed=false"
        results = service.files().list(q=query, pageSize=100, fields="files(id, name, mimeType, createdTime, modifiedTime)").execute()
        files = results.get("files", [])
        
        return files
    
    @staticmethod
    def upload_file(user_id: int, file: Any, file_name: str, mimetype: str) -> Dict[str, Any]:
        """
        Upload a file to the user's 'LifeLine Records' folder in Google Drive.
        """
        credentials = GoogleDriveService.get_credentials(user_id)
        if not credentials:
            raise ValueError("Google credentials not found. Please authenticate first.")

        user = UserDAO.get_user_by_id(user_id)
        if not user or not user.get("drive_folder_id"):
            raise ValueError("Drive folder ID not found for user.")

        drive_folder_id = user["drive_folder_id"]
        
        # Refresh token if needed
        credentials = GoogleDriveService._refresh_credentials_if_needed(credentials, user_id)
        
        service = build("drive", "v3", credentials=credentials)
        file_metadata = {"name": file_name, "parents": [drive_folder_id]}
        media = MediaIoBaseUpload(file, mimetype=mimetype, resumable=True)
        
        file = service.files().create(body=file_metadata, media_body=media, fields="id, name, mimeType").execute()
        return file

    @staticmethod
    def delete_file(user_id: int, file_id: str):
        """Delete a file from Google Drive."""
        credentials = GoogleDriveService.get_credentials(user_id)
        if not credentials:
            raise ValueError("Google credentials not found. Please authenticate first.")

        # Refresh token if needed
        credentials = GoogleDriveService._refresh_credentials_if_needed(credentials, user_id)

        service = build("drive", "v3", credentials=credentials)
        service.files().delete(fileId=file_id).execute()

    @staticmethod
    async def download_file(user_id: int, file_id: str) -> bytes:
        """Download a file from Google Drive."""
        credentials = GoogleDriveService.get_credentials(user_id)
        if not credentials:
            raise ValueError("Google credentials not found. Please authenticate first.")

        # Refresh token if needed
        credentials = GoogleDriveService._refresh_credentials_if_needed(credentials, user_id)

        service = build("drive", "v3", credentials=credentials)
        request = service.files().get_media(fileId=file_id)
        file_data = io.BytesIO()
        downloader = MediaIoBaseDownload(file_data, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            logger.debug(f"Download {int(status.progress() * 100)}%")
        return file_data.getvalue()

