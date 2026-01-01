"""
Tag service layer.

Business logic for tag CRUD operations and management.
"""

from typing import List, Optional
from sqlmodel import Session, select

from src.models import Tag
from src.core.errors import (
    DatabaseError,
    DuplicateResourceError,
)


class TagService:
    """Service for tag operations"""

    def __init__(self, session: Session):
        """Initialize service with database session"""
        self.session = session

    # ========================================================================
    # CRUD Operations
    # ========================================================================

    def get_tag(self, tag_id: int) -> Tag:
        """Get a single tag by ID"""
        try:
            tag = self.session.exec(
                select(Tag).where(Tag.id == tag_id)
            ).first()

            if not tag:
                raise DatabaseError(f"Tag with ID {tag_id} not found")

            return tag

        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to get tag {tag_id}", original_error=e)

    def get_tag_by_name(self, name: str) -> Optional[Tag]:
        """Get a tag by name (case-insensitive)"""
        try:
            name_lower = name.lower().strip()
            tag = self.session.exec(
                select(Tag).where(Tag.name == name_lower)
            ).first()
            return tag

        except Exception as e:
            raise DatabaseError(f"Failed to get tag by name '{name}'", original_error=e)

    def list_tags(self, skip: int = 0, limit: int = 50) -> tuple[List[Tag], int]:
        """List all tags with pagination"""
        try:
            # Get total count
            total = self.session.exec(select(func.count(Tag.id))).one()

            # Get paginated results
            tags = self.session.exec(
                select(Tag)
                .order_by(Tag.created_at.desc())
                .offset(skip)
                .limit(limit)
            ).all()

            return tags, total

        except Exception as e:
            raise DatabaseError("Failed to list tags", original_error=e)

    def create_tag(self, name: str) -> Tag:
        """Create a new tag"""
        try:
            name_lower = name.lower().strip()

            # Check for duplicates
            existing = self.get_tag_by_name(name_lower)
            if existing:
                raise DuplicateResourceError("Tag", "name", name_lower)

            tag = Tag(name=name_lower)
            self.session.add(tag)
            return tag

        except DuplicateResourceError:
            raise
        except Exception as e:
            raise DatabaseError("Failed to create tag", original_error=e)

    def delete_tag(self, tag_id: int) -> None:
        """Delete a tag"""
        try:
            tag = self.get_tag(tag_id)
            self.session.delete(tag)

        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to delete tag {tag_id}", original_error=e)

    # ========================================================================
    # Utility Operations
    # ========================================================================

    def get_or_create_tag(self, name: str) -> Tag:
        """Get existing tag or create new one"""
        try:
            tag = self.get_tag_by_name(name)
            if tag:
                return tag
            return self.create_tag(name)

        except Exception as e:
            raise DatabaseError(
                f"Failed to get or create tag '{name}'",
                original_error=e
            )


# Import for func in list_tags
from sqlalchemy import func
