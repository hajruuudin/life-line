import requests
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class N8NService:
    @staticmethod
    def trigger_file_summary(user_email: str, user_id: int, file_name: str, file_bytes: bytes, mimetype: str):
        try:
            webhook_url = f"{settings.n8n_url}/webhook/summarize"
            
            # Non-file data goes here
            data = {
                "user_id": str(user_id),
                "user_email": user_email,
            }
            
            # The actual file goes here
            files = {
                "file": (file_name, file_bytes, mimetype)
            }
            
            headers = {
                "Authorization": f"Bearer {settings.n8n_webhook_auth_key}"
            }
            
            # Use 'data=' for JSON-like fields and 'files=' for the binary file
            response = requests.post(webhook_url, data=data, files=files, headers=headers, timeout=10)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Failed to trigger n8n: {str(e)}")
            return False