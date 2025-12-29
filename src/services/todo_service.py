"""Business logic for todo application."""

from typing import List, Optional
from src.models.task import Task


class TodoService:
    """Service for managing tasks in memory.

    Provides all CRUD operations and task status management.
    Stores tasks in memory with auto-incrementing IDs.
    """

    def __init__(self):
        """Initialize TodoService with empty task list."""
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task to the list.

        Args:
            title: Task title
            description: Optional task description

        Returns:
            The newly created Task object

        Raises:
            ValueError: If title is invalid
        """
        task = Task(self._next_id, title, description)
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks.

        Returns:
            List of all Task objects in creation order
        """
        return self._tasks.copy()

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a specific task by ID.

        Args:
            task_id: The task ID to find

        Returns:
            The Task object if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: str, description: str = "") -> Task:
        """Update an existing task.

        Args:
            task_id: The task ID to update
            title: New task title
            description: New task description

        Returns:
            The updated Task object

        Raises:
            ValueError: If task not found or title is invalid
        """
        task = self.get_task(task_id)
        if task is None:
            raise ValueError(f"Task not found with ID {task_id}")

        task.update(title, description)
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: The task ID to delete

        Returns:
            True if task was deleted, False if not found
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                self._tasks.pop(i)
                return True
        return False

    def mark_complete(self, task_id: int) -> bool:
        """Mark a task as completed.

        Args:
            task_id: The task ID to mark complete

        Returns:
            True if task was marked complete, False if not found
        """
        task = self.get_task(task_id)
        if task is None:
            return False

        task.mark_complete()
        return True

    def mark_incomplete(self, task_id: int) -> bool:
        """Mark a task as incomplete.

        Args:
            task_id: The task ID to mark incomplete

        Returns:
            True if task was marked incomplete, False if not found
        """
        task = self.get_task(task_id)
        if task is None:
            return False

        task.mark_incomplete()
        return True
