"""
Tag model for task categorization.

Represents a category/label that can be assigned to multiple tasks.
"""

from typing import Optional, List
from pydantic import Field, validator
from sqlmodel import SQLModel, Relationship

from src.models.base import BaseModel


class TagBase(SQLModel):
    """Base tag schema for creation and updates"""

    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Tag name (required, 1-50 chars, unique)"
    )

    @validator("name")
    def name_not_empty(cls, v):
        """Validate name is not just whitespace"""
        if not v or not v.strip():
            raise ValueError("Tag name cannot be empty")
        return v.strip().lower()  # Normalize to lowercase


class Tag(BaseModel, TagBase, table=True):
    """
    Database model for tags.

    Represents a category/label for organizing tasks.
    """

    __tablename__ = "tags"

    # Relationships
    tasks: List["Task"] = Relationship(
        back_populates="tags"
    )


class TagRead(TagBase):
    """Schema for API responses when reading a tag"""

    id: int
    created_at: Optional[str] = None

    class Config:
        """Pydantic config"""
        from_attributes = True


class TagCreate(TagBase):
    """Schema for creating a new tag"""
    pass


class TagList(SQLModel):
    """Schema for tag list responses"""

    items: List[TagRead]
    total: int


# Avoid circular import by using string annotation
from src.models.task import Task  # noqa: E402, F401
from src.models.task_tag import TaskTag  # noqa: E402, F401
