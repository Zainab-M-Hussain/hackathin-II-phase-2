"""
Task REST API endpoints.

Provides CRUD operations and advanced filtering, searching, sorting for tasks.
"""

from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlmodel import Session

from src.models import (
    Task,
    TaskRead,
    TaskReadList,
    TaskStatus,
    TaskPriority,
)
from src.api.dependencies import get_db
from src.services.task_service import TaskService
from src.core.errors import TaskNotFoundError, DatabaseError


# Create router
router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Task not found"}},
)


# ============================================================================
# List Tasks (with filtering, searching, sorting)
# ============================================================================

@router.get("", response_model=TaskReadList)
async def list_tasks(
    session: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of items to return"),
    status: Optional[TaskStatus] = Query(None, description="Filter by status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by priority"),
    tags: Optional[str] = Query(None, description="Comma-separated tag IDs to filter"),
    search: Optional[str] = Query(None, max_length=500, description="Search in title and description"),
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
):
    """
    List tasks with optional filtering, searching, and sorting.

    Query Parameters:
    - skip: Number of items to skip (default: 0)
    - limit: Number of items to return (default: 50, max: 100)
    - status: Filter by status (pending, complete, archived)
    - priority: Filter by priority (LOW, MEDIUM, HIGH)
    - tags: Comma-separated tag IDs (AND logic)
    - search: Search term for title and description
    - sort_by: Field to sort by (created_at, due_date, priority, title)
    - sort_order: Sort order (asc or desc)

    Example:
    GET /api/tasks?status=pending&priority=HIGH&sort_by=due_date&sort_order=asc
    """
    try:
        service = TaskService(session)

        # Parse tag_ids if provided
        tag_ids = None
        if tags:
            try:
                tag_ids = [int(t.strip()) for t in tags.split(",")]
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid tag IDs format"
                )

        # List tasks
        tasks, total = service.list_tasks(
            skip=skip,
            limit=limit,
            status=status,
            priority=priority,
            tag_ids=tag_ids,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        return TaskReadList(
            items=[TaskRead.from_orm(task) for task in tasks],
            total=total,
            skip=skip,
            limit=limit,
        )

    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# Get Single Task
# ============================================================================

@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: int = Query(..., ge=1, description="Task ID"),
    session: Session = Depends(get_db),
):
    """Get a single task by ID"""
    try:
        service = TaskService(session)
        task = service.get_task(task_id)
        return TaskRead.from_orm(task)

    except TaskNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# Create Task
# ============================================================================

@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: dict,
    session: Session = Depends(get_db),
):
    """
    Create a new task.

    Request Body:
    {
        "title": "Task title (required, 1-500 chars)",
        "description": "Detailed notes (optional, max 5000 chars)",
        "priority": "LOW|MEDIUM|HIGH (optional, default: MEDIUM)",
        "due_date": "2025-12-31T23:59:59Z (optional)",
        "tags": [1, 2, 3] (optional, tag IDs)
    }
    """
    try:
        service = TaskService(session)

        title = task_data.get("title", "").strip()
        if not title or len(title) > 500:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title is required and must be 1-500 characters"
            )

        description = task_data.get("description")
        if description:
            description = description.strip()
            if len(description) > 5000:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Description must be max 5000 characters"
                )

        priority = task_data.get("priority", TaskPriority.MEDIUM)
        due_date = task_data.get("due_date")
        tags = task_data.get("tags", [])

        task = service.create_task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            tag_ids=tags,
        )
        session.commit()

        return TaskRead.from_orm(task)

    except HTTPException:
        raise
    except DatabaseError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# Update Task
# ============================================================================

@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    task_data: dict,
    session: Session = Depends(get_db),
):
    """
    Update an existing task (partial update allowed).

    Request Body (all fields optional):
    {
        "title": "New title",
        "description": "New description",
        "priority": "HIGH",
        "due_date": "2025-12-31T23:59:59Z",
        "tags": [1, 2, 3]
    }
    """
    try:
        service = TaskService(session)

        # Extract fields, only update if provided
        title = task_data.get("title")
        if title is not None:
            title = title.strip()
            if not title or len(title) > 500:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Title must be 1-500 characters"
                )

        description = task_data.get("description")
        if description is not None:
            description = description.strip()
            if description and len(description) > 5000:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Description must be max 5000 characters"
                )

        priority = task_data.get("priority")
        due_date = task_data.get("due_date")
        tags = task_data.get("tags")

        task = service.update_task(
            task_id=task_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            tag_ids=tags,
        )
        session.commit()

        return TaskRead.from_orm(task)

    except TaskNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
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
# Update Task Status
# ============================================================================

@router.patch("/{task_id}/status", response_model=TaskRead)
async def update_task_status(
    task_id: int,
    status_data: dict,
    session: Session = Depends(get_db),
):
    """
    Update task status (complete, archive, etc.).

    Request Body:
    {
        "status": "complete|pending|archived",
        "reason": "Optional reason for change"
    }
    """
    try:
        service = TaskService(session)

        new_status = status_data.get("status")
        if not new_status:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status is required"
            )

        try:
            new_status = TaskStatus(new_status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {', '.join([s.value for s in TaskStatus])}"
            )

        reason = status_data.get("reason")

        task = service.update_task_status(
            task_id=task_id,
            status=new_status,
            reason=reason,
        )
        session.commit()

        return TaskRead.from_orm(task)

    except TaskNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
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
# Delete Task
# ============================================================================

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    session: Session = Depends(get_db),
):
    """Delete a task by ID"""
    try:
        service = TaskService(session)
        service.delete_task(task_id)
        session.commit()

    except TaskNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DatabaseError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# Task Statistics
# ============================================================================

@router.get("/stats/summary", response_model=dict)
async def get_statistics(session: Session = Depends(get_db)):
    """Get task statistics (total, completed, pending, completion rate)"""
    try:
        service = TaskService(session)
        stats = service.get_statistics()
        return stats

    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
