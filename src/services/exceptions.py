"""
Error handling and error codes for the Todo application.

Defines structured error codes for consistent error handling across all layers.
"""


class ErrorCode:
    """Error code constants for Todo application."""
    
    # Error code mappings per contracts/task_service.md
    INVALID_TITLE = "E001"  # Title validation failed (empty, whitespace, >500 chars)
    TASK_NOT_FOUND = "E002"  # Referenced task doesn't exist
    INVALID_TASK_ID = "E003"  # Non-numeric ID provided
    INVALID_DESCRIPTION = "E004"  # Description validation failed (>500 chars)
    OPERATION_FAILED = "E005"  # Generic operation failure


class TodoException(Exception):
    """Base exception for Todo application."""
    
    def __init__(self, message: str, error_code: str = None):
        """
        Initialize TodoException.
        
        Args:
            message: User-friendly error message
            error_code: Structured error code (E001-E005)
        """
        self.message = message
        self.error_code = error_code or ErrorCode.OPERATION_FAILED
        super().__init__(self.message)
    
    def __str__(self):
        """Return error message."""
        return self.message


class InvalidTitleError(TodoException):
    """Raised when task title is invalid."""
    
    def __init__(self, message: str = "Title must be 1-500 characters and not empty/whitespace"):
        super().__init__(message, ErrorCode.INVALID_TITLE)


class TaskNotFoundError(TodoException):
    """Raised when task with given ID is not found."""
    
    def __init__(self, task_id: int):
        message = f"Task with ID {task_id} not found"
        super().__init__(message, ErrorCode.TASK_NOT_FOUND)


class InvalidTaskIdError(TodoException):
    """Raised when task ID is not numeric."""
    
    def __init__(self, task_id: str):
        message = f"Task ID must be numeric, got: {task_id}"
        super().__init__(message, ErrorCode.INVALID_TASK_ID)


class InvalidDescriptionError(TodoException):
    """Raised when task description is invalid."""
    
    def __init__(self, message: str = "Description must be 0-500 characters"):
        super().__init__(message, ErrorCode.INVALID_DESCRIPTION)
