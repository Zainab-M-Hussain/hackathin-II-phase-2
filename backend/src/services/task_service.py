"""
Task service layer.

Business logic for task CRUD operations, filtering, searching, and sorting.
Wraps database models and provides clean API for endpoints.
"""

from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select, and_, or_, func

from src.models import (
    Task,
    TaskCreate,
    TaskUpdate,
    TaskStatus,
    TaskPriority,
    AuditLog,
    AuditAction,
)
from src.core.errors import (
    TaskNotFoundError,
    InvalidTaskDataError,
    DatabaseError,
)


class TaskService:
    """Service for task operations"""

    def __init__(self, session: Session):
        """Initialize service with database session"""
        self.session = session

    # ========================================================================
    # CRUD Operations
    # ========================================================================

    def get_task(self, task_id: int) -> Task:
        """Get a single task by ID"""
        try:
            task = self.session.exec(
                select(Task).where(Task.id == task_id)
            ).first()

            if not task:
                raise TaskNotFoundError(task_id)

            return task
        except TaskNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to get task {task_id}", original_error=e)

    def list_tasks(
        self,
        skip: int = 0,
        limit: int = 50,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        tag_ids: Optional[List[int]] = None,
        search: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[List[Task], int]:
        """
        List tasks with filtering, searching, and sorting.

        Returns:
            Tuple of (tasks list, total count)
        """
        try:
            # Base query
            query = select(Task)

            # Apply filters
            filters = []

            if status:
                filters.append(Task.status == status)

            if priority:
                filters.append(Task.priority == priority)

            if search:
                search_term = f"%{search}%"
                filters.append(
                    or_(
                        Task.title.ilike(search_term),
                        Task.description.ilike(search_term),
                    )
                )

            if tag_ids:
                # Filter tasks that have all specified tags
                for tag_id in tag_ids:
                    query = query.join(Task.tags).where(Task.tags.any(Tag.id == tag_id))

            if filters:
                query = query.where(and_(*filters))

            # Get total count
            count_query = select(func.count()).select_from(Task)
            if filters:
                count_query = count_query.where(and_(*filters))
            total = self.session.exec(count_query).one()

            # Apply sorting
            sort_column = getattr(Task, sort_by, Task.created_at)
            if sort_order.lower() == "asc":
                query = query.order_by(sort_column.asc())
            else:
                query = query.order_by(sort_column.desc())

            # Apply pagination
            query = query.offset(skip).limit(limit)

            tasks = self.session.exec(query).all()
            return tasks, total

        except Exception as e:
            raise DatabaseError("Failed to list tasks", original_error=e)

    def create_task(
        self,
        title: str,
        description: Optional[str] = None,
        priority: TaskPriority = TaskPriority.MEDIUM,
        due_date: Optional[datetime] = None,
        tag_ids: Optional[List[int]] = None,
    ) -> Task:
        """Create a new task"""
        try:
            task = Task(
                title=title,
                description=description,
                priority=priority,
                due_date=due_date,
                status=TaskStatus.PENDING,
            )

            self.session.add(task)
            self.session.flush()  # Get task.id

            # Add tags if provided
            if tag_ids:
                from src.services.tag_service import TagService
                tag_service = TagService(self.session)
                for tag_id in tag_ids:
                    tag = tag_service.get_tag(tag_id)
                    task.tags.append(tag)

            self.session.add(task)
            return task

        except Exception as e:
            raise DatabaseError("Failed to create task", original_error=e)

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[TaskPriority] = None,
        due_date: Optional[datetime] = None,
        tag_ids: Optional[List[int]] = None,
    ) -> Task:
        """Update an existing task"""
        try:
            task = self.get_task(task_id)

            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if priority is not None:
                task.priority = priority
            if due_date is not None:
                task.due_date = due_date

            # Update tags if provided
            if tag_ids is not None:
                from src.services.tag_service import TagService
                tag_service = TagService(self.session)

                task.tags.clear()
                for tag_id in tag_ids:
                    tag = tag_service.get_tag(tag_id)
                    task.tags.append(tag)

            task.updated_at = datetime.utcnow()
            self.session.add(task)
            return task

        except TaskNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to update task {task_id}", original_error=e)

    def update_task_status(
        self,
        task_id: int,
        status: TaskStatus,
        reason: Optional[str] = None,
    ) -> Task:
        """Update task status (complete, archive, etc.)"""
        try:
            task = self.get_task(task_id)

            # Log the change (triggers audit log)
            old_status = task.status
            task.status = status
            task.updated_at = datetime.utcnow()

            # Optionally store reason in metadata for audit trail
            if reason:
                if not task.metadata:
                    task.metadata = {}
                task.metadata["last_reason"] = reason

            self.session.add(task)
            return task

        except TaskNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(
                f"Failed to update task {task_id} status",
                original_error=e
            )

    def delete_task(self, task_id: int) -> None:
        """Delete a task"""
        try:
            task = self.get_task(task_id)
            self.session.delete(task)

        except TaskNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to delete task {task_id}", original_error=e)

    # ========================================================================
    # Advanced Operations
    # ========================================================================

    def get_task_audit_history(self, task_id: int) -> List[AuditLog]:
        """Get audit history for a task"""
        try:
            self.get_task(task_id)  # Verify task exists

            audit_logs = self.session.exec(
                select(AuditLog)
                .where(AuditLog.task_id == task_id)
                .order_by(AuditLog.timestamp.desc())
            ).all()

            return audit_logs

        except TaskNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(
                f"Failed to get audit history for task {task_id}",
                original_error=e
            )

    def get_statistics(self) -> dict:
        """Get task statistics (total, completed, by priority)"""
        try:
            total = self.session.exec(select(func.count(Task.id))).one()
            completed = self.session.exec(
                select(func.count(Task.id)).where(Task.status == TaskStatus.COMPLETE)
            ).one()
            pending = self.session.exec(
                select(func.count(Task.id)).where(Task.status == TaskStatus.PENDING)
            ).one()

            return {
                "total": total,
                "completed": completed,
                "pending": pending,
                "completion_rate": (completed / total * 100) if total > 0 else 0,
            }

        except Exception as e:
            raise DatabaseError("Failed to get statistics", original_error=e)
