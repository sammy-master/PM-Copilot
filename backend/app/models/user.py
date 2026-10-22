"""
PM Copilot - User Database Model
----------------------------------
Defines the 'users' table in PostgreSQL using SQLAlchemy ORM.

VIVA EXPLANATION:
  "SQLAlchemy ORM lets us define database tables as Python classes.
   Each class attribute maps to a column in the table.
   We never write raw SQL — SQLAlchemy generates it for us."
"""

import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"

    # Primary key — UUID is better than auto-increment integers
    # because it's globally unique and doesn't expose record counts
    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # We NEVER store plain passwords — only the bcrypt hash
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Timestamps — set automatically by the database
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"
