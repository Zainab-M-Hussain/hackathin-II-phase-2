"""Task data model for todo application."""

from datetime import datetime


class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique task identifier (auto-generated)
        title: Task title (1-500 characters, required)
        description: Optional task description (0-500 characters)
        is_completed: Whether task is marked as complete
        created_at: Timestamp when task was created
    """

    def __init__(self, task_id: int, title: str, description: str = ""):
        """Initialize a new Task.

        Args:
            task_id: Unique task identifier
            title: Task title (will be stripped and validated)
            description: Optional task description (default: empty string)

        Raises:
            ValueError: If title is empty or contains only whitespace
        """
        # Validate and set title
        cleaned_title = title.strip() if title else ""
        if not cleaned_title or len(cleaned_title) == 0:
            raise ValueError("Task title cannot be empty or contain only whitespace")

        if len(cleaned_title) > 500:
            raise ValueError("Task title cannot exceed 500 characters")

        # Validate and set description
        cleaned_description = description.strip() if description else ""
        if len(cleaned_description) > 500:
            raise ValueError("Task description cannot exceed 500 characters")

        self.id = task_id
        self.title = cleaned_title
        self.description = cleaned_description
        self.is_completed = False
        self.created_at = datetime.now()

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def mark_incomplete(self) -> None:
        """Mark this task as incomplete."""
        self.is_completed = False

    def update(self, title: str, description: str = "") -> None:
        """Update task title and description.

        Args:
            title: New task title
            description: New task description

        Raises:
            ValueError: If title is empty or invalid
        """
        # Validate new title
        cleaned_title = title.strip() if title else ""
        if not cleaned_title or len(cleaned_title) == 0:
            raise ValueError("Task title cannot be empty or contain only whitespace")

        if len(cleaned_title) > 500:
            raise ValueError("Task title cannot exceed 500 characters")

        # Validate new description
        cleaned_description = description.strip() if description else ""
        if len(cleaned_description) > 500:
            raise ValueError("Task description cannot exceed 500 characters")

        self.title = cleaned_title
        self.description = cleaned_description

    def __repr__(self) -> str:
        """Return string representation of task."""
        status = "✓" if self.is_completed else "○"
        return f"[{self.id}] {status} {self.title}"
