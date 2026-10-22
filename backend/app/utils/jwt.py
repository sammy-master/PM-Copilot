"""
PM Copilot - JWT Utility Functions
-------------------------------------
Handles creating and verifying JSON Web Tokens (JWTs).

WHAT IS A JWT?
  A JWT is a signed string that looks like: xxxxx.yyyyy.zzzzz
  - Header (algorithm used)
  - Payload (user data: user_id, expiry time)
  - Signature (proves the token wasn't tampered with)

The server creates it on login and the client sends it back
in every request header: "Authorization: Bearer <token>"

VIVA EXPLANATION:
  "We use JWT for stateless authentication. The server doesn't store
   sessions — it just signs a token with a secret key. Any request that
   includes a valid token is authenticated. We use python-jose to
   create and verify these tokens."
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.database import get_db

# This tells FastAPI that routes need an "Authorization: Bearer <token>" header
bearer_scheme = HTTPBearer()


def create_access_token(user_id: str) -> str:
    """
    Create a JWT token for a given user ID.

    The token payload contains:
      - sub: the user ID (subject)
      - exp: expiry timestamp
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {
        "sub": user_id,
        "exp": expire,
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> Optional[str]:
    """
    Decode and verify a JWT token.
    Returns the user_id if valid, raises an exception if not.
    """
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return user_id
    except JWTError:
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
):
    """
    FastAPI dependency — extracts the current user from the JWT token.

    Usage in any protected route:
        async def my_route(current_user = Depends(get_current_user)):
            # current_user is the User ORM object
            ...

    Raises HTTP 401 if token is missing, expired, or invalid.
    """
    from app.models.user import User  # Import here to avoid circular imports

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token. Please log in again.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Extract user_id from token
    user_id = decode_token(credentials.credentials)
    if user_id is None:
        raise credentials_exception

    # Fetch user from database
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user
