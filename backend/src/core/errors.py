"""
Error codes and exception classes.

Reuses error codes from Phase I for consistency.
"""

from enum import Enum
from typing import Optional, Any, Dict
from fastapi import HTTPException, status


# ============================================================================
# Error Codes (from Phase I)
# ============================================================================

class ErrorCode(str, Enum):
    """Error codes for consistent error handling"""
    E001 = "E001"  # Task not found
    E002 = "E002"  # Invalid task data
    E003 = "E003"  # Duplicate resource
    E004 = "E004"  # Database error
    E005 = "E005"  # Validation error


# Error code to HTTP status mapping
ERROR_CODE_TO_STATUS = {
    ErrorCode.E001: status.HTTP_404_NOT_FOUND,         # Task not found
    ErrorCode.E002: status.HTTP_400_BAD_REQUEST,       # Invalid data
    ErrorCode.E003: status.HTTP_409_CONFLICT,          # Duplicate resource
    ErrorCode.E004: status.HTTP_500_INTERNAL_SERVER_ERROR,  # Database error
    ErrorCode.E005: status.HTTP_400_BAD_REQUEST,       # Validation error
}


# ============================================================================
# Custom Exceptions
# ============================================================================

class TodoException(Exception):
    """Base exception for all todo app errors"""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.E004,
        status_code: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code or ERROR_CODE_TO_STATUS.get(code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.details = details or {}
        super().__init__(self.message)


class TaskNotFoundError(TodoException):
    """Raised when a task is not found"""

    def __init__(self, task_id: int):
        super().__init__(
            message=f"Task with ID {task_id} not found",
            code=ErrorCode.E001,
            details={"task_id": task_id}
        )


class InvalidTaskDataError(TodoException):
    """Raised when task data is invalid"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code=ErrorCode.E002,
            details=details
        )


class DuplicateResourceError(TodoException):
    """Raised when a duplicate resource is created"""

    def __init__(self, resource_type: str, field: str, value: Any):
        super().__init__(
            message=f"{resource_type} with {field}='{value}' already exists",
            code=ErrorCode.E003,
            details={"resource_type": resource_type, "field": field, "value": value}
        )


class DatabaseError(TodoException):
    """Raised on database operation failures"""

    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(
            message=message,
            code=ErrorCode.E004,
            details={"original_error": str(original_error)} if original_error else {}
        )


class ValidationError(TodoException):
    """Raised on validation failures"""

    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(
            message=message,
            code=ErrorCode.E005,
            details={"field": field} if field else {}
        )


# ============================================================================
# Error Response Schema
# ============================================================================

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error response schema"""

    error: str
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    path: Optional[str] = None
    timestamp: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "error": "NotFound",
                "code": "E001",
                "message": "Task with ID 999 not found",
                "details": {"task_id": 999},
                "path": "/api/tasks/999",
                "timestamp": "2025-12-29T10:30:00Z"
            }
        }


# ============================================================================
# Exception to HTTP Response Converter
# ============================================================================

def exception_to_http_response(exc: TodoException, path: str = None) -> ErrorResponse:
    """Convert a TodoException to an HTTP error response"""
    from datetime import datetime

    return ErrorResponse(
        error=exc.code.name if hasattr(exc.code, 'name') else type(exc).__name__,
        code=exc.code.value if hasattr(exc.code, 'value') else str(exc.code),
        message=exc.message,
        details=exc.details if exc.details else None,
        path=path,
        timestamp=datetime.utcnow().isoformat() + "Z"
    )
