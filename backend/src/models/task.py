"""
Task model for todo items.

Represents a single task with title, description, status, priority, and tags.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import Field, validator
from sqlmodel import SQLModel, Relationship, Column, String

from src.models.base import BaseModel


class TaskStatus(str, Enum):
    """Task status values"""
    PENDING = "pending"
    COMPLETE = "complete"
    ARCHIVED = "archived"


class TaskPriority(str, Enum):
    """Task priority values"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TagLink(SQLModel, table=False):
    """Reference to a tag (for API responses)"""
    id: int
    name: str


class TaskBase(SQLModel):
    """
    Base task schema for creation and updates.

    Used by: POST /api/tasks, PUT /api/tasks/{id}
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Task title/summary (required, 1-500 chars)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Detailed task description (optional, max 5000 chars)"
    )
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM,
        description="Task priority: LOW, MEDIUM, or HIGH"
    )
    due_date: Optional[datetime] = Field(
        default=None,
        description="Task deadline (optional)"
    )

    @validator("title")
    def title_not_empty(cls, v):
        """Validate title is not just whitespace"""
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @validator("description")
    def description_not_empty(cls, v):
        """Validate description if provided is not just whitespace"""
        if v is not None:
            if not v.strip():
                raise ValueError("Description cannot be empty or whitespace")
            return v.strip()
        return v

    @validator("due_date")
    def due_date_valid(cls, v):
        """Validate due_date is in the future (optional check)"""
        if v is not None and v < datetime.utcnow():
            # Allow past dates for completed tasks, just validate type
            pass
        return v


class TaskUpdate(TaskBase):
    """Schema for updating an existing task (all fields optional except relationships)"""

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=500,
        description="Task title/summary (optional for updates)"
    )
    status: Optional[TaskStatus] = Field(
        default=None,
        description="Task status (optional for updates)"
    )


class TaskStatusUpdate(SQLModel):
    """Schema for toggling task completion status"""

    status: TaskStatus = Field(
        ...,
        description="New task status"
    )
    reason: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Reason for status change (for audit log)"
    )


class Task(BaseModel, TaskBase, table=True):
    """
    Database model for tasks.

    Represents a todo item with full state and relationships.
    """

    __tablename__ = "tasks"

    # Status and priority (with database-level defaults)
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        sa_column=Column(String, nullable=False),
        description="Task state: pending, complete, or archived"
    )

    # Phase III AI Integration Fields (reserved, empty in Phase II)
    scheduled_at: Optional[datetime] = Field(
        default=None,
        description="Reserved for Phase III: AI-planned execution time"
    )

    # Relationships (populated via foreign keys)
    tags: List["Tag"] = Relationship(
        back_populates="tasks"
    )
    audit_logs: List["AuditLog"] = Relationship(
        back_populates="task",
        cascade_delete=True
    )


class TaskRead(TaskBase):
    """Schema for API responses when reading a task"""

    id: int
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    tags: List[TagLink] = []

    class Config:
        """Pydantic config"""
        from_attributes = True


class TaskReadList(SQLModel):
    """Schema for list responses (pagination)"""

    items: List[TaskRead]
    total: int
    skip: int
    limit: int


# Avoid circular import by using string annotations
from src.models.tag import Tag  # noqa: E402, F401
from src.models.audit_log import AuditLog  # noqa: E402, F401
from src.models.task_tag import TaskTag  # noqa: E402, F401
