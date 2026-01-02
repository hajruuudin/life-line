"""Authentication DTOs."""
from pydantic import BaseModel


class Token(BaseModel):
    """DTO for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class GoogleAuthRequest(BaseModel):
    """DTO for Google OAuth request."""
    code: str

