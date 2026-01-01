"""
Tag REST API endpoints.

Provides CRUD operations for tags.
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlmodel import Session

from src.models import TagRead, Tag, TagList
from src.api.dependencies import get_db
from src.services.tag_service import TagService
from src.core.errors import DatabaseError, DuplicateResourceError


# Create router
router = APIRouter(
    prefix="/tags",
    tags=["tags"],
    responses={404: {"description": "Tag not found"}},
)


# ============================================================================
# List Tags
# ============================================================================

@router.get("", response_model=TagList)
async def list_tags(
    session: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of items to return"),
):
    """List all tags with pagination"""
    try:
        service = TagService(session)
        tags, total = service.list_tags(skip=skip, limit=limit)

        return TagList(
            items=[TagRead.from_orm(tag) for tag in tags],
            total=total,
        )

    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# Get Single Tag
# ============================================================================

@router.get("/{tag_id}", response_model=TagRead)
async def get_tag(
    tag_id: int = Query(..., ge=1, description="Tag ID"),
    session: Session = Depends(get_db),
):
    """Get a single tag by ID"""
    try:
        service = TagService(session)
        tag = service.get_tag(tag_id)
        return TagRead.from_orm(tag)

    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "not found" in str(e) else status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# Create Tag
# ============================================================================

@router.post("", response_model=TagRead, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_data: dict,
    session: Session = Depends(get_db),
):
    """
    Create a new tag.

    Request Body:
    {
        "name": "Tag name (required, 1-50 chars, unique)"
    }
    """
    try:
        service = TagService(session)

        name = tag_data.get("name", "").strip()
        if not name or len(name) > 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag name is required and must be 1-50 characters"
            )

        tag = service.create_tag(name)
        session.commit()

        return TagRead.from_orm(tag)

    except DuplicateResourceError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except HTTPException:
        raise
    except DatabaseError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# Delete Tag
# ============================================================================

@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: int,
    session: Session = Depends(get_db),
):
    """Delete a tag by ID"""
    try:
        service = TagService(session)
        service.delete_tag(tag_id)
        session.commit()

    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "not found" in str(e) else status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
