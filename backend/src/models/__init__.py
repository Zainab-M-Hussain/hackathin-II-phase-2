"""
SQLModel entity definitions.

Exports all models for use in services and API endpoints.
"""

from src.models.base import BaseModel, TimestampMixin
from src.models.task import (
    Task,
    TaskBase,
    TaskRead,
    TaskReadList,
    TaskUpdate,
    TaskStatusUpdate,
    TaskStatus,
    TaskPriority,
)
from src.models.tag import (
    Tag,
    TagBase,
    TagRead,
    TagCreate,
    TagList,
)
from src.models.task_tag import TaskTag
from src.models.audit_log import (
    AuditLog,
    AuditLogBase,
    AuditLogRead,
    AuditLogList,
    AuditAction,
)

__all__ = [
    # Base
    "BaseModel",
    "TimestampMixin",
    # Task
    "Task",
    "TaskBase",
    "TaskRead",
    "TaskReadList",
    "TaskUpdate",
    "TaskStatusUpdate",
    "TaskStatus",
    "TaskPriority",
    # Tag
    "Tag",
    "TagBase",
    "TagRead",
    "TagCreate",
    "TagList",
    # Junction
    "TaskTag",
    # Audit
    "AuditLog",
    "AuditLogBase",
    "AuditLogRead",
    "AuditLogList",
    "AuditAction",
]
