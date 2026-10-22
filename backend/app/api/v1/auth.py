"""
PM Copilot - Authentication API Routes
-----------------------------------------
Defines the HTTP endpoints for register, login, and profile.

FastAPI automatically:
  - Validates request body against the Pydantic schema
  - Returns 422 Unprocessable Entity if validation fails
  - Generates documentation at /docs

ENDPOINTS:
  POST /api/v1/auth/register  → Create new account, returns JWT
  POST /api/v1/auth/login     → Login, returns JWT
  GET  /api/v1/auth/me        → Get current user info (protected)
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from app.services.auth_service import register_user, login_user
from app.utils.jwt import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Register a new user account.

    - Validates email format and password length
    - Hashes password with bcrypt
    - Returns a JWT token immediately (user is logged in after register)
    """
    user, token = await register_user(db, data)
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Login with email and password.

    - Verifies credentials
    - Returns a fresh JWT token valid for 24 hours
    """
    user, token = await login_user(db, data)
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    """
    Get the currently logged-in user's profile.

    This is a PROTECTED route — requires a valid JWT token
    in the Authorization header: "Bearer <token>"
    """
    return UserResponse.model_validate(current_user)
