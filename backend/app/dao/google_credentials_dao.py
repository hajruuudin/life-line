"""Google Credentials Data Access Object."""
from typing import Optional, Dict, Any
from datetime import datetime
import logging
from app.database import db

logger = logging.getLogger(__name__)


class GoogleCredentialsDAO:
    """Data access operations for Google credentials."""
    
    @staticmethod
    def create_or_update_credentials(user_id: int, access_token: str, refresh_token: str, 
                                     token_expiry: datetime, connection=None) -> Dict[str, Any]:
        """Create or update Google credentials for a user."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                INSERT INTO user_google_credentials (user_id, access_token, refresh_token, token_expiry)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (user_id) 
                DO UPDATE SET 
                    access_token = EXCLUDED.access_token,
                    refresh_token = EXCLUDED.refresh_token,
                    token_expiry = EXCLUDED.token_expiry,
                    updated_at = CURRENT_TIMESTAMP
                RETURNING id, user_id, access_token, refresh_token, token_expiry, created_at, updated_at
            """, (user_id, access_token, refresh_token, token_expiry))
            result = dict(cursor.fetchone())
            return result
    
    @staticmethod
    def get_credentials_by_user_id(user_id: int, connection=None) -> Optional[Dict[str, Any]]:
        """Get Google credentials for a user."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                SELECT id, user_id, access_token, refresh_token, token_expiry, created_at, updated_at
                FROM user_google_credentials
                WHERE user_id = %s
            """, (user_id,))
            result = cursor.fetchone()
            if result:
                return dict(result)
            else:
                return None
    
    @staticmethod
    def delete_credentials(user_id: int, connection=None) -> bool:
        """Delete Google credentials for a user."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                DELETE FROM user_google_credentials
                WHERE user_id = %s
            """, (user_id,))
            success = cursor.rowcount > 0
            return success