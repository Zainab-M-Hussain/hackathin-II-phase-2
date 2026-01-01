"""
AuditLog model for tracking all changes.

Provides immutable append-only audit trail for Phase III AI learning and compliance.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field, Column, String, JSON, Relationship

from src.models.base import BaseModel


class AuditAction(str, Enum):
    """Types of actions that can be audited"""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    COMPLETE = "complete"
    ARCHIVE = "archive"
    TAG_ADD = "tag_add"
    TAG_REMOVE = "tag_remove"


class AuditLogBase(SQLModel):
    """Base audit log schema"""

    action: AuditAction = Field(
        ...,
        description="Type of action performed"
    )
    actor: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="User ID, AI agent ID, or 'system' that performed the action"
    )
    reason: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Optional reason/comment for the action"
    )


class AuditLog(BaseModel, AuditLogBase, table=True):
    """
    Database model for audit logs.

    Provides immutable, append-only history of all task changes.
    Used for compliance, debugging, and Phase III AI learning.
    """

    __tablename__ = "audit_logs"

    # Core fields
    task_id: int = Field(
        foreign_key="tasks.id",
        description="Reference to the task that was modified"
    )
    action: AuditAction = Field(
        sa_column=Column(String, nullable=False),
        description="Type of action performed"
    )

    # State tracking (JSONB for flexibility)
    previous_state: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON),
        description="Task state before the change (null for CREATE actions)"
    )
    new_state: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON),
        description="Task state after the change"
    )

    # Metadata
    actor: str = Field(
        ...,
        max_length=255,
        nullable=False,
        description="User ID, AI agent ID, or 'system' that performed the action"
    )
    reason: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Optional reason/comment for the action"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        sa_column=Column(JSON, nullable=False),
        description="Additional context (request ID, source, IP, etc.)"
    )

    # Relationship to Task
    task: Optional["Task"] = Relationship(
        back_populates="audit_logs"
    )


class AuditLogRead(AuditLogBase):
    """Schema for API responses when reading audit logs"""

    id: int
    task_id: int
    action: AuditAction
    previous_state: Optional[Dict[str, Any]]
    new_state: Optional[Dict[str, Any]]
    timestamp: datetime
    metadata: Optional[Dict[str, Any]]

    class Config:
        """Pydantic config"""
        from_attributes = True


class AuditLogList(SQLModel):
    """Schema for audit log list responses"""

    items: list[AuditLogRead]
    total: int
    task_id: int


# Avoid circular import by using string annotation
from src.models.task import Task  # noqa: E402, F401
