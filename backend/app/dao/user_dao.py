"""User Data Access Object."""
from typing import Optional, Dict, Any
import logging
from app.database import db

logger = logging.getLogger(__name__)


class UserDAO:
    """Data access operations for users."""
    
    @staticmethod
    def create_user(email: str, name: Optional[str] = None, google_id: Optional[str] = None,
                    google_oauth_token: Optional[str] = None, google_refresh_token: Optional[str] = None,
                    drive_folder_id: Optional[str] = None,
                    connection=None) -> Dict[str, Any]:
        """Create a new user."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                INSERT INTO users (email, name, google_id, google_oauth_token, google_refresh_token, drive_folder_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, email, name, google_id, drive_folder_id, created_at, updated_at
            """, (email, name, google_id, google_oauth_token, google_refresh_token, drive_folder_id))
            result = dict(cursor.fetchone())
            return result
    
    @staticmethod
    def get_user_by_email(email: str, connection=None) -> Optional[Dict[str, Any]]:
        """Get user by email."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                SELECT id, email, name, google_id, google_oauth_token, google_refresh_token, drive_folder_id, created_at, updated_at
                FROM users
                WHERE email = %s
            """, (email,))
            result = cursor.fetchone()
            if result:
                return dict(result)
            else:
                return None
    
    @staticmethod
    def get_user_by_id(user_id: int, connection=None) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                SELECT id, email, name, google_id, google_oauth_token, google_refresh_token, drive_folder_id, created_at, updated_at
                FROM users
                WHERE id = %s
            """, (user_id,))
            result = cursor.fetchone()
            if result:
                return dict(result)
            else:
                return None
    
    @staticmethod
    def get_user_by_google_id(google_id: str, connection=None) -> Optional[Dict[str, Any]]:
        """Get user by Google ID."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                SELECT id, email, name, google_id, google_oauth_token, google_refresh_token, drive_folder_id, created_at, updated_at
                FROM users
                WHERE google_id = %s
            """, (google_id,))
            result = cursor.fetchone()
            if result:
                logger.info(f"User found with Google ID {google_id}, ID: {result['id']}")
                return dict(result)
            else:
                logger.info(f"No user found with Google ID: {google_id}")
                return None

    @staticmethod
    def get_user_by_api_key(api_key: str, connection=None) -> Optional[Dict[str, Any]]:
        """Get user by API key."""
        with db.get_cursor(connection=connection) as cursor:
            # TODO: Implement API key column if needed
            return None

    @staticmethod
    def update_user_google_tokens(user_id: int, google_oauth_token: str, google_refresh_token: str,
                                  connection=None) -> bool:
        """Update user's Google OAuth tokens. Returns True if update was successful."""
        logger.info(f"Updating Google tokens for user ID: {user_id}")
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                UPDATE users
                SET google_oauth_token = %s, google_refresh_token = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (google_oauth_token, google_refresh_token, user_id))
            success = cursor.rowcount > 0
            if success:
                logger.info(f"Google tokens updated successfully for user ID: {user_id}")
            else:
                logger.error(f"Failed to update Google tokens for user ID: {user_id} (user not found)")
            return success


    @staticmethod
    def update_drive_folder_id(user_id: int, drive_folder_id: str, connection=None) -> bool:
        """Update user's Google Drive folder ID."""
        logger.info(f"Updating drive_folder_id for user ID: {user_id}")
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                UPDATE users
                SET drive_folder_id = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (drive_folder_id, user_id))
            success = cursor.rowcount > 0
            if success:
                logger.info(f"drive_folder_id updated successfully for user ID: {user_id}")
            else:
                logger.error(f"Failed to update drive_folder_id for user ID: {user_id} (user not found)")
            return success
    
    @staticmethod
    def update_api_key(user_id: int, api_key: str, connection=None) -> bool:
        """Update user's API key."""
        # TODO: Implement API key column if needed
        return False
