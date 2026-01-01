"""
Base model for all SQLModel entities.

Provides common fields: id, created_at, updated_at
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class TimestampMixin:
    """Mixin providing automatic timestamp fields"""

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when record was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when record was last updated"
    )


class BaseModel(SQLModel, TimestampMixin):
    """
    Base model for all database entities.

    Provides:
    - id: Auto-incrementing primary key
    - created_at: Automatic creation timestamp
    - updated_at: Automatic update timestamp (managed by database trigger)
    """

    id: Optional[int] = Field(default=None, primary_key=True)
