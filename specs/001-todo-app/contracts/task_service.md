# Service Interface Contract: ITaskService

**Date**: 2025-12-29 | **Phase**: Phase 1 Design | **Purpose**: Enable Phase II HTTP wrapping without redesign

## Overview

`ITaskService` is the abstract interface that defines the contract for task management. This interface enables multiple implementations:
- **Phase I**: Console CLI via `TodoService` (in-memory)
- **Phase II**: HTTP API wrapper around Phase I `TodoService`
- **Phase IV**: Cloud-backed implementation (database layer)

All implementations MUST satisfy this contract to ensure compatibility across all phases.

---

## Interface Definition

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.task import Task

class ITaskService(ABC):
    """Abstract interface for task management operations.

    All implementations must:
    - Use structured error codes (E001–E005) for errors
    - Return consistent data types
    - Preserve Task entity invariants
    """

    @abstractmethod
    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task to the system.

        Args:
            title: Task title (required, 1-500 chars, non-empty/non-whitespace)
            description: Optional task description (0-500 chars)

        Returns:
            Newly created Task object with auto-assigned ID

        Raises:
            ValueError: If title is invalid (maps to E001)
        """
        pass

    @abstractmethod
    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks in the system.

        Returns:
            List of Task objects in creation order (oldest first)
            Empty list if no tasks exist
        """
        pass

    @abstractmethod
    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a specific task by ID.

        Args:
            task_id: Task ID (must be positive integer)

        Returns:
            Task object if found, None if not found
            Does not raise exception for missing tasks (graceful)
        """
        pass

    @abstractmethod
    def update_task(self, task_id: int, title: str, description: str = "") -> Task:
        """Update an existing task's title and description.

        Args:
            task_id: Task ID (must exist)
            title: New task title (required, 1-500 chars, non-empty/non-whitespace)
            description: New task description (optional, 0-500 chars)

        Returns:
            Updated Task object

        Raises:
            ValueError: If task_id not found (maps to E002) or title invalid (E001)
        """
        pass

    @abstractmethod
    def delete_task(self, task_id: int) -> bool:
        """Delete a task from the system.

        Args:
            task_id: Task ID to delete

        Returns:
            True if task was deleted
            False if task not found (graceful, no exception)
        """
        pass

    @abstractmethod
    def mark_complete(self, task_id: int) -> bool:
        """Mark a task as completed.

        Args:
            task_id: Task ID to mark complete

        Returns:
            True if marked successfully
            False if task not found (graceful, no exception)
        """
        pass

    @abstractmethod
    def mark_incomplete(self, task_id: int) -> bool:
        """Mark a task as incomplete (revert completed status).

        Args:
            task_id: Task ID to mark incomplete

        Returns:
            True if marked successfully
            False if task not found (graceful, no exception)
        """
        pass
```

---

## Method Contracts

### `add_task(title: str, description: str = "") -> Task`

**Purpose**: Create a new task in the system.

**Input Validation**:
- Title: Non-empty, non-whitespace, max 500 chars
- Description: Max 500 chars (optional)

**Preconditions**:
- Title must not be None or empty after strip()
- Description can be empty string or None

**Postconditions**:
- Task created with unique auto-incremented ID
- Task marked as incomplete (`is_completed = False`)
- `created_at` timestamp set to current time (UTC)
- Task added to list in creation order

**Error Handling**:
- Invalid title → Raise `ValueError` (error code E001)
- Invalid description → Raise `ValueError` (error code E004)

**Example**:
```python
service = TodoService()
task = service.add_task("Buy groceries", "Milk, eggs, bread")
assert task.id == 1
assert task.title == "Buy groceries"
assert task.is_completed == False
```

---

### `get_all_tasks() -> List[Task]`

**Purpose**: Retrieve all tasks in the system.

**Input Validation**: None (no parameters)

**Preconditions**: None

**Postconditions**:
- Returns all tasks in creation order (oldest first)
- If no tasks exist, returns empty list (not None)
- Returned list is a copy (modifications don't affect internal state)

**Error Handling**: None (no errors possible)

**Example**:
```python
service = TodoService()
service.add_task("Task 1")
service.add_task("Task 2")
tasks = service.get_all_tasks()
assert len(tasks) == 2
assert tasks[0].title == "Task 1"
```

---

### `get_task(task_id: int) -> Task | None`

**Purpose**: Retrieve a single task by ID.

**Input Validation**:
- task_id: Must be integer (or int-compatible)

**Preconditions**: None

**Postconditions**:
- If task exists, returns Task object
- If task doesn't exist, returns None (not raises exception)

**Error Handling**:
- Invalid task_id type → Caller responsibility (may raise TypeError before method call)
- Task not found → Returns None (graceful, no exception)

**Example**:
```python
service = TodoService()
task = service.add_task("Task 1")
found = service.get_task(task.id)
assert found.title == "Task 1"
missing = service.get_task(999)
assert missing is None
```

---

### `update_task(task_id: int, title: str, description: str = "") -> Task`

**Purpose**: Modify an existing task's title and description.

**Input Validation**:
- task_id: Must reference existing task
- title: Non-empty, non-whitespace, max 500 chars
- description: Max 500 chars (optional)

**Preconditions**:
- Task with given task_id must exist

**Postconditions**:
- Task's title and description updated
- Task ID and `created_at` unchanged
- Task's completion status unchanged (not affected by update)

**Error Handling**:
- Task not found → Raise `ValueError` (error code E002)
- Invalid title → Raise `ValueError` (error code E001)
- Invalid description → Raise `ValueError` (error code E004)

**Example**:
```python
service = TodoService()
task = service.add_task("Old title")
updated = service.update_task(task.id, "New title", "New description")
assert updated.title == "New title"
assert updated.id == task.id  # ID unchanged
```

---

### `delete_task(task_id: int) -> bool`

**Purpose**: Remove a task from the system permanently.

**Input Validation**:
- task_id: Must be integer

**Preconditions**: None

**Postconditions**:
- If task existed, it is removed from the system
- If task didn't exist, no state change
- Subsequent `get_task(task_id)` returns None

**Error Handling**:
- Task not found → Returns `False` (graceful, no exception)
- Invalid task_id type → Caller responsibility

**Example**:
```python
service = TodoService()
task = service.add_task("Task to delete")
success = service.delete_task(task.id)
assert success == True
assert service.get_task(task.id) is None
missing = service.delete_task(999)
assert missing == False
```

---

### `mark_complete(task_id: int) -> bool`

**Purpose**: Mark a task as completed.

**Input Validation**:
- task_id: Must be integer

**Preconditions**: None

**Postconditions**:
- If task exists, `is_completed` set to `True`
- Other task fields unchanged

**Error Handling**:
- Task not found → Returns `False` (graceful, no exception)

**Example**:
```python
service = TodoService()
task = service.add_task("Task")
assert task.is_completed == False
success = service.mark_complete(task.id)
assert success == True
assert service.get_task(task.id).is_completed == True
```

---

### `mark_incomplete(task_id: int) -> bool`

**Purpose**: Revert a completed task to incomplete status.

**Input Validation**:
- task_id: Must be integer

**Preconditions**: None

**Postconditions**:
- If task exists, `is_completed` set to `False`
- Other task fields unchanged

**Error Handling**:
- Task not found → Returns `False` (graceful, no exception)

**Example**:
```python
service = TodoService()
task = service.add_task("Task")
service.mark_complete(task.id)
assert service.get_task(task.id).is_completed == True
success = service.mark_incomplete(task.id)
assert success == True
assert service.get_task(task.id).is_completed == False
```

---

## Error Code Reference

All methods use structured error codes for consistency across Phases II–V:

| Code | Name | Context | HTTP Status (Phase II) |
|------|------|---------|----------------------|
| E001 | `invalid_title` | Title empty/whitespace/too long | 400 Bad Request |
| E002 | `task_not_found` | Referenced task doesn't exist | 404 Not Found |
| E003 | `invalid_task_id` | Task ID non-numeric or invalid | 400 Bad Request |
| E004 | `invalid_description` | Description too long | 400 Bad Request |
| E005 | `operation_failed` | Generic operation error | 500 Internal Server Error |

---

## Implementation Notes

### Phase I (Console)

`TodoService` implements `ITaskService` with in-memory storage:
- Tasks stored in `List[Task]`
- IDs auto-incremented from counter
- All operations O(n) linear search (acceptable for console)

### Phase II (Web)

HTTP API wrapper implements `ITaskService` (or delegates to Phase I instance):
- `/api/tasks` (GET) → `get_all_tasks()`
- `/api/tasks` (POST) → `add_task()`
- `/api/tasks/{id}` (GET) → `get_task()`
- `/api/tasks/{id}` (PUT) → `update_task()`
- `/api/tasks/{id}` (DELETE) → `delete_task()`
- `/api/tasks/{id}/complete` (POST) → `mark_complete()`
- `/api/tasks/{id}/incomplete` (POST) → `mark_incomplete()`

### Phase IV (Cloud)

Database-backed implementation:
- Tasks stored in SQL/NoSQL database
- IDs managed by database (auto-increment or UUID)
- Error codes mapped to HTTP status codes
- `to_dict()` / `from_dict()` used for ORM serialization

---

## Testing Requirements

Every implementation must pass these contract tests:

1. **Add Task**:
   - ✓ Success case: valid title + description
   - ✓ Error: empty title
   - ✓ Error: whitespace-only title
   - ✓ Auto-increment IDs

2. **Get All Tasks**:
   - ✓ Empty list when no tasks
   - ✓ All tasks returned in creation order
   - ✓ Returned list is copy (mutations don't affect internal state)

3. **Get Task**:
   - ✓ Success: existing task returned
   - ✓ Not found: None returned (no exception)

4. **Update Task**:
   - ✓ Success: title and description updated
   - ✓ ID unchanged
   - ✓ Error: task not found
   - ✓ Error: invalid title

5. **Delete Task**:
   - ✓ Success: task removed
   - ✓ Not found: False returned (no exception)

6. **Mark Complete**:
   - ✓ Success: is_completed set to True
   - ✓ Not found: False returned

7. **Mark Incomplete**:
   - ✓ Success: is_completed set to False
   - ✓ Not found: False returned

---

## Compatibility Matrix

| Phase | Implementation | Storage | Extension Point |
|-------|---------------|---------|-----------------|
| **Phase I** | `TodoService` | In-memory list | CLI app (src/cli/app.py) |
| **Phase II** | HTTP wrapper | Same `TodoService` | HTTP endpoints, user_id namespace |
| **Phase III** | Extends Task | Same schema | AI chatbot uses tags/metadata |
| **Phase IV** | Database impl | PostgreSQL/Firestore | Cloud infrastructure |
| **Phase V** | Scaling layer | Distributed cache | Multi-region deployment |

All phases use this contract to ensure compatibility.
