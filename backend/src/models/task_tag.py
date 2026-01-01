"""
TaskTag junction table model.

Represents the many-to-many relationship between tasks and tags.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class TaskTag(SQLModel, table=True):
    """
    Junction table for many-to-many relationship between tasks and tags.

    A task can have multiple tags, and a tag can be applied to multiple tasks.
    """

    __tablename__ = "task_tags"

    task_id: int = Field(
        foreign_key="tasks.id",
        primary_key=True,
        description="Reference to task"
    )
    tag_id: int = Field(
        foreign_key="tags.id",
        primary_key=True,
        description="Reference to tag"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="When the tag was added to the task"
    )
