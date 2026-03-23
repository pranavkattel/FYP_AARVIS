"""Auth request models."""

from typing import Optional

from pydantic import BaseModel


class RegisterRequest(BaseModel):
    """Register request body."""

    username: str
    email: str
    password: str
    full_name: str
    location: str
    interests: str = ""
    face_embeddings: Optional[list] = None


class LoginRequest(BaseModel):
    """Login request body."""

    username: str
    password: str
