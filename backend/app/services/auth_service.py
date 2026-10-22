"""
PM Copilot - Authentication Service
--------------------------------------
Business logic for user registration and login.

Separating business logic into a "service" layer keeps route handlers clean.
Routes handle HTTP — services handle logic.

VIVA EXPLANATION:
  "I use bcrypt to hash passwords. Bcrypt adds a random 'salt' to the
   password before hashing so two identical passwords produce different
   hashes. This protects users even if the database is leaked."
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest
from app.utils.jwt import create_access_token

# bcrypt context — handles hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if a plain password matches its stored hash."""
    return pwd_context.verify(plain_password, hashed_password)


async def register_user(db: AsyncSession, data: RegisterRequest) -> tuple[User, str]:
    """
    Register a new user.

    Steps:
      1. Check if email already exists
      2. Hash the password
      3. Save user to database
      4. Return user + JWT token

    Raises:
      400 Bad Request if email is already registered
    """
    # Step 1: Check for duplicate email
    result = await db.execute(select(User).where(User.email == data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists.",
        )

    # Step 2: Hash the password — NEVER store plain text
    hashed = hash_password(data.password)

    # Step 3: Create and save the user
    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hashed,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)  # Refresh to get the auto-generated id and timestamps

    # Step 4: Create a JWT token so the user is instantly logged in
    token = create_access_token(user.id)

    return user, token


async def login_user(db: AsyncSession, data: LoginRequest) -> tuple[User, str]:
    """
    Authenticate a user and return a JWT token.

    Steps:
      1. Find user by email
      2. Verify password against stored hash
      3. Return user + new JWT token

    Raises:
      401 Unauthorized if credentials are wrong
    """
    # Step 1: Find user by email
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    # Step 2: Verify password
    # Note: We give the same error for "user not found" and "wrong password"
    # so attackers can't determine which emails are registered
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )

    # Step 3: Create and return a fresh JWT token
    token = create_access_token(user.id)

    return user, token
