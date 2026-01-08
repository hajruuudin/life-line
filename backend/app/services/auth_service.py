"""Authentication service."""
from typing import Dict, Any, Optional
from datetime import timedelta, timezone, datetime
import logging
import secrets
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from app.config import settings
from app.dao.user_dao import UserDAO
from app.dao.google_credentials_dao import GoogleCredentialsDAO
from app.services.google_drive_service import GoogleDriveService
from app.utils.jwt import create_access_token
from app.models.user import UserResponse

logger = logging.getLogger(__name__)


class AuthService:
    """Business logic for authentication."""
    
    @staticmethod
    def get_google_oauth_url() -> str:
        """Get Google OAuth authorization URL."""
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": settings.google_client_id,
                    "client_secret": settings.google_client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [settings.google_redirect_uri],
                }
            },
            scopes=[
                "openid",
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/drive",
                "https://www.googleapis.com/auth/calendar",
            ],
        )
        flow.redirect_uri = settings.google_redirect_uri
        authorization_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
        return authorization_url
    
    @staticmethod
    def handle_google_callback(code: str) -> Dict[str, Any]:
        """Handle Google OAuth callback and create/login user."""
        try:
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": settings.google_client_id,
                        "client_secret": settings.google_client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [settings.google_redirect_uri],
                    }
                },
                scopes=[
                    "openid",
                    "https://www.googleapis.com/auth/userinfo.email",
                    "https://www.googleapis.com/auth/userinfo.profile",
                    "https://www.googleapis.com/auth/drive",
                    "https://www.googleapis.com/auth/calendar",
                ],
            )
            flow.redirect_uri = settings.google_redirect_uri
            
            flow.fetch_token(code=code)
            
            credentials = flow.credentials
            
            user_info_service = build("oauth2", "v2", credentials=credentials)
            user_info = user_info_service.userinfo().get().execute()
            
            email = user_info.get("email")
            name = user_info.get("name")
            google_id = user_info.get("id")
            
            from app.database import db
            
            with db.get_connection() as conn:
                user = UserDAO.get_user_by_email(email, connection=conn)
                
                if not user:
                    user = UserDAO.create_user(
                        email=email,
                        name=name,
                        google_id=google_id,
                        google_oauth_token=credentials.token,
                        google_refresh_token=credentials.refresh_token,
                        connection=conn,
                    )
                else:
                    update_success = UserDAO.update_user_google_tokens(
                        user_id=user["id"],
                        google_oauth_token=credentials.token,
                        google_refresh_token=credentials.refresh_token,
                        connection=conn,
                    )
                    if not update_success:
                        error_msg = f"Failed to update user Google tokens for user ID: {user['id']}"
                        raise Exception(error_msg)
                
                token_expiry = credentials.expiry if credentials.expiry else datetime.now(timezone.utc) + timedelta(hours=24)
                
                GoogleCredentialsDAO.create_or_update_credentials(
                    user_id=user["id"],
                    access_token=credentials.token,
                    refresh_token=credentials.refresh_token,
                    token_expiry=token_expiry,
                    connection=conn,
                )

                # Find or create the Google Drive folder
                folder_id = GoogleDriveService.find_or_create_app_folder(user["id"], credentials, connection=conn)
                logger.info(f"Ensured Drive folder exists for user {user['id']} with folder ID {folder_id}")

                # Re-fetch the user to get the updated drive_folder_id
                user = UserDAO.get_user_by_id(user["id"], connection=conn)
            
            access_token = create_access_token(data={"sub": str(user["id"])})
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": user,
            }
        except Exception as e:
            raise

