"""
PM Copilot - Auth Pydantic Schemas
------------------------------------
Pydantic schemas define the SHAPE of API requests and responses.

Difference between models/user.py and schemas/auth.py:
  - models/user.py   → defines the DATABASE TABLE (SQLAlchemy)
  - schemas/auth.py  → defines the API JSON shape (Pydantic)

We never send the hashed_password back to the client.
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


# ---- Request Schemas (what the client sends) ----

class RegisterRequest(BaseModel):
    """Data required to create a new account."""
    name: str = Field(..., min_length=2, max_length=100, example="Rahul Sharma")
    email: EmailStr = Field(..., example="rahul@example.com")
    password: str = Field(..., min_length=6, example="securepassword123")


class LoginRequest(BaseModel):
    """Data required to log in."""
    email: EmailStr = Field(..., example="rahul@example.com")
    password: str = Field(..., example="securepassword123")


# ---- Response Schemas (what the server sends back) ----

class UserResponse(BaseModel):
    """Safe user data returned to the client — NO password."""
    id: str
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True  # Allows converting SQLAlchemy model → Pydantic schema


class TokenResponse(BaseModel):
    """JWT token returned after successful login or register."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
