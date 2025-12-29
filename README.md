# Console Todo Application

A fully functional, in-memory console-based Todo application built with Python 3 using Spec-Driven Development (SDD) methodology.

## Features

✅ **Add Task** - Create new tasks with title and optional description
✅ **View All Tasks** - See all tasks with ID, title, description, and completion status
✅ **Mark Complete/Incomplete** - Toggle task completion status
✅ **Update Task** - Edit existing task title and description
✅ **Delete Task** - Remove tasks with confirmation
✅ **In-Memory Storage** - All data stored in memory (no database needed)
✅ **Input Validation** - Prevents empty titles and validates all user input
✅ **User-Friendly Interface** - Menu-driven console interface
✅ **Comprehensive Testing** - 77 unit and integration tests (100% passing)

## Quick Start

### Running the Application

```bash
python main.py
```

### Menu Options

```
WELCOME TO TODO APPLICATION
==================================================

1. Add Task                  - Create a new task
2. View All Tasks          - Display all tasks
3. Mark Complete/Incomplete - Toggle task status
4. Update Task             - Edit task details
5. Delete Task             - Remove a task
6. Exit                    - Close the application
```

### Example Usage

```
Select an option (1-6): 1

--- Add New Task ---
Enter task title: Buy groceries
Enter task description (optional): Milk, eggs, bread
✓ Task added successfully (ID: 1)

--- All Tasks ---

[1] ○ Buy groceries
     └─ Milk, eggs, bread
```

## Project Structure

```
D:\zainab\hackathon II/
├── main.py                      # Application entry point
├── requirements.txt             # Dependencies (empty - no external libs)
├── README.md                    # This file
├── ARCHITECTURE.md              # Architecture documentation
│
├── specs/001-todo-app/          # SDD specification documents
│   ├── spec.md                  # Feature requirements
│   ├── plan.md                  # Implementation plan
│   └── tasks.md                 # Task breakdown
│
├── src/                         # Application source code
│   ├── models/
│   │   └── task.py             # Task data model
│   ├── services/
│   │   └── todo_service.py     # Business logic layer
│   └── cli/
│       └── app.py              # Console interface
│
└── tests/                       # Test suite
    ├── unit/
    │   ├── test_task_model.py       # Task model tests (20 tests)
    │   ├── test_todo_service.py     # TodoService tests (21 tests)
    │   └── test_cli_app.py          # CLI app tests (23 tests)
    └── integration/
        └── test_app_workflow.py     # End-to-end workflows (13 tests)
```

## Architecture Overview

### Layer 1: Data Model (`src/models/task.py`)
- **Task Class**: Immutable data model representing a single todo item
- Properties: id, title, description, is_completed, created_at
- Validation: Non-empty title, max 500 chars for title/description
- Methods: mark_complete(), mark_incomplete(), update()

### Layer 2: Business Logic (`src/services/todo_service.py`)
- **TodoService Class**: In-memory task management
- Auto-incrementing task IDs
- CRUD operations: add_task, get_task, update_task, delete_task
- Status management: mark_complete, mark_incomplete
- List operations: get_all_tasks

### Layer 3: Console Interface (`src/cli/app.py`)
- **TodoApp Class**: Menu-driven CLI
- User input handling and validation
- Task formatting and display
- Error messages and user feedback
- Main application loop

### Layer 4: Entry Point (`main.py`)
- Bootstraps TodoService and TodoApp
- Handles top-level exception handling
- Starts the main application loop

## Development Methodology

This project follows **Spec-Driven Development (SDD)**:

1. **Specification** (`spec.md`)
   - 5 user stories with acceptance scenarios
   - Functional requirements and edge cases
   - Success criteria

2. **Planning** (`plan.md`)
   - Architecture decisions
   - Data model design
   - Technical context and constraints

3. **Task Breakdown** (`tasks.md`)
   - 47 actionable tasks organized by phase
   - Dependencies and execution order
   - Parallel opportunities identified

4. **Implementation**
   - Code generated from specifications
   - All acceptance criteria addressed
   - 100% test coverage of requirements

## Testing

### Run All Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Run Unit Tests Only

```bash
python -m unittest discover -s tests/unit -p "test_*.py" -v
```

### Run Integration Tests Only

```bash
python -m unittest discover -s tests/integration -p "test_*.py" -v
```

### Test Coverage

- **Total Tests**: 77
- **Unit Tests**: 64
  - Task Model: 20 tests
  - TodoService: 21 tests
  - CLI App: 23 tests
- **Integration Tests**: 13 tests
- **Pass Rate**: 100%

### Test Categories

1. **Model Tests** - Task creation, validation, status changes
2. **Service Tests** - CRUD operations, task management
3. **CLI Tests** - User input handling, menu flows
4. **Workflow Tests** - End-to-end user scenarios
5. **Error Handling** - Invalid inputs, edge cases

## Requirements

- **Python**: 3.8+
- **Dependencies**: None (uses only Python standard library)
- **Storage**: In-memory only (no database)
- **Platform**: Windows, macOS, Linux

## Features in Detail

### Add Task
- Creates a new task with auto-incremented ID
- Title is required (non-empty, non-whitespace)
- Description is optional
- Returns success confirmation with task ID

### View All Tasks
- Displays all tasks in creation order
- Shows status (✓ complete, ○ incomplete)
- Displays task ID, title, and description
- Shows "No tasks available" when empty

### Mark Complete/Incomplete
- Toggle task completion status
- Shows current status before toggling
- Provides feedback on completion state change
- Status visible in task list view

### Update Task
- Edit task title and description
- Shows current values for reference
- Press Enter to keep existing value
- Validates title is not empty

### Delete Task
- Shows task before deletion
- Requires Y/N confirmation
- Safely removes task from list
- Shows cancellation feedback

## Usage Examples

### Add a task with description

```
Select an option (1-6): 1

--- Add New Task ---
Enter task title: Learn Python
Enter task description (optional): Complete tutorial and practice
✓ Task added successfully (ID: 1)
```

### View all tasks

```
Select an option (1-6): 2

--- All Tasks ---

[1] ○ Learn Python
     └─ Complete tutorial and practice
[2] ○ Finish project
[3] ✓ Buy groceries
     └─ Milk, eggs, bread
```

### Mark task as complete

```
Select an option (1-6): 3

--- Mark Task Complete/Incomplete ---
Enter task ID: 1
✓ Task 1 marked as complete
```

### Update a task

```
Select an option (1-6): 4

--- Update Task ---
Enter task ID: 2

Current title: Finish project
Enter new title (or press Enter to keep): Finish Python project
Current description: (none)
Enter new description (or press Enter to keep): Due by Friday
✓ Task 2 updated successfully
```

### Delete a task

```
Select an option (1-6): 5

--- Delete Task ---
Enter task ID: 1

Task to delete: [1] ✓ Learn Python
     └─ Complete tutorial and practice
Are you sure you want to delete this task? (Y/N): Y
✓ Task 1 deleted successfully
```

## Input Validation

The application validates all user inputs:

- **Task Titles**: Required, non-empty, non-whitespace, max 500 characters
- **Task Descriptions**: Optional, max 500 characters
- **Task IDs**: Must be numeric, must exist in the system
- **Menu Selections**: Must be 1-6, shows error for invalid selections
- **Confirmations**: Accepts Y/N for delete confirmation

## Error Handling

All errors are gracefully handled with user-friendly messages:

```
✗ Error: Task title cannot be empty or contain only whitespace
✗ Task not found with ID 999
✗ Invalid task ID. Please enter a number.
✗ Invalid option. Please select 1-6.
```

## Implementation Highlights

✅ **No External Dependencies** - Uses only Python standard library
✅ **Clean Architecture** - Separation of concerns with 3 layers
✅ **Comprehensive Testing** - 77 tests ensure reliability
✅ **Input Validation** - Prevents invalid states
✅ **Error Messages** - Clear, actionable feedback
✅ **Code Quality** - PEP 8 compliant, well-documented
✅ **Maintainability** - Clear naming and structure

## Future Enhancements

Possible features for future versions:

- File persistence (save/load tasks)
- Due dates for tasks
- Task categories/tags
- Task priority levels
- Search functionality
- Recurring tasks
- Task notes/comments

## Author

Built using Spec-Driven Development methodology with automated task generation and test-first implementation.

## License

This is a demonstration project for SDD methodology.
