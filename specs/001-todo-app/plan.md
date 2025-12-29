# Implementation Plan: Console Todo Application

**Branch**: `001-todo-app` | **Date**: 2025-12-29 | **Spec**: `/specs/001-todo-app/spec.md`

**Input**: Feature specification for Phase I foundational console Todo app with extensibility for Phases II-V.

## Summary

Build a fully functional in-memory console Todo application in Python 3.8+ that implements 5 core user stories (add, view, update, delete, mark complete) with a clean 3-layer architecture designed for extensibility toward web (Phase II), AI chatbot (Phase III), and cloud (Phase IV-V) implementations. All code will follow test-driven development, produce zero external dependencies, and include extensibility patterns locked in clarifications.

---

## Technical Context

**Language/Version**: Python 3.8+
**Primary Dependencies**: None (standard library only)
**Storage**: In-memory (Phase I); extensible to persistence in Phase IV
**Testing**: unittest (standard library)
**Target Platform**: Linux/macOS/Windows console
**Project Type**: Single console application with clean 3-layer architecture
**Performance Goals**: <100ms per operation (target: <10ms)
**Constraints**:
  - No persistent storage in Phase I
  - Single-user, single-session in Phase I
  - Single-threaded execution
  - In-memory task list as source of truth
**Scale/Scope**: Single-user, unlimited tasks (limited by available RAM)

---

## Constitution Check

**Applicable Principles** (from `.specify/memory/constitution.md`):

✅ **Library-First**: Phase I TodoService is a standalone, independently testable library
✅ **Clear Separation**: 3-layer architecture (Model → Service → CLI) enables independent testing
✅ **Test-First**: TDD mandatory; tests written before implementation; Red-Green-Refactor cycle
✅ **Integration Testing**: Contract tests for service interface; end-to-end workflows
✅ **Observability**: Structured error codes (E001–E005); logging interface defined
✅ **Simplicity**: YAGNI principle; no premature abstractions; start simple, extend via clarifications

**Gates Passed**: ✅ All gates clear. Implementation may proceed.

---

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-app/
├── spec.md                  # Feature specification (with clarifications)
├── plan.md                  # This file
├── data-model.md            # Phase 1 output (entity definitions)
├── contracts/               # Phase 1 output (service interface)
│   └── task_service.md      # TodoService interface contract
└── tasks.md                 # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── models/
│   ├── __init__.py
│   └── task.py              # Task entity with validation + extensibility fields
├── services/
│   ├── __init__.py
│   ├── task_service.py      # TodoService business logic (ITaskService interface)
│   └── exceptions.py        # Structured error codes (E001–E005)
└── cli/
    ├── __init__.py
    └── app.py               # TodoApp console interface

tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── test_task_model.py           # Task entity tests
│   ├── test_task_service.py         # TodoService tests
│   ├── test_cli_app.py              # CLI app tests
│   └── test_error_codes.py          # Error taxonomy tests
└── integration/
    ├── __init__.py
    └── test_app_workflow.py         # End-to-end workflow tests

main.py                     # Entry point
requirements.txt            # Dependencies (empty - no external libs)
README.md                   # User documentation
ARCHITECTURE.md             # Technical architecture
```

**Structure Decision**: Single project with clean 3-layer separation. Enables independent testing of data model, business logic, and UI. Phase II web layer can reuse TodoService (layer 2) via HTTP wrapper. Phase III AI layer can extend Task model with tags/metadata without Phase I changes.

---

## Implementation Strategy: 7 Steps

### Step 1: Define Task Data Model

**File**: `src/models/task.py`

**Entities**:
- **Task**: Single todo item with extended schema for Phase III/IV

**Schema** (matching JSON contract for Phase IV cloud):
```python
class Task:
    id: int                          # Auto-incrementing, unique within single-user context
    title: str                       # 1–500 chars, required, non-empty/non-whitespace
    description: str                 # 0–500 chars, optional
    is_completed: bool               # Default: False
    created_at: datetime             # Auto-generated on creation
    tags: List[str]                  # Optional, reserved for Phase III AI (Phase I ignores)
    metadata: Dict                   # Optional, reserved for Phase III+ (Phase I ignores)
```

**Validation** (mapped to error codes):
- Empty/whitespace title → E001 (invalid_title)
- Title > 500 chars → E001 (invalid_title)
- Description > 500 chars → E004 (invalid_description)
- Non-datetime created_at → Generic error

**Methods**:
- `mark_complete()` → Set is_completed to True
- `mark_incomplete()` → Set is_completed to False
- `update(title, description)` → Update fields with validation
- `to_dict()` → Serialize to JSON schema (Phase IV contract)
- `from_dict(d)` → Deserialize from JSON schema (Phase IV contract)

---

### Step 2: Implement In-Memory Task Store

**File**: `src/services/task_service.py` + `src/services/exceptions.py`

**Interface** (ITaskService contract for Phase II):
```python
class ITaskService:
    """Abstract interface for task management (enables Phase II HTTP wrapper)"""
    def add_task(title: str, description: str = "") -> Task
    def get_all_tasks() -> List[Task]
    def get_task(task_id: int) -> Task | None
    def update_task(task_id: int, title: str, description: str = "") -> Task
    def delete_task(task_id: int) -> bool
    def mark_complete(task_id: int) -> bool
    def mark_incomplete(task_id: int) -> bool
```

**Implementation** (TodoService):
- Private `_tasks: List[Task]` for in-memory storage
- Private `_next_id: int` for auto-incrementing IDs (starts at 1)
- Each method implements ITaskService contract
- Error handling uses structured error codes (E001–E005)

**Error Codes** (consistent across Phase II–V):
```python
class TaskError(Exception):
    E001 = "invalid_title"
    E002 = "task_not_found"
    E003 = "invalid_task_id"
    E004 = "invalid_description"
    E005 = "operation_failed"
```

**Logging Interface** (for Phase IV observability):
- Each operation logs: timestamp, error_code (if error), operation_name, context (task_id if applicable)
- Format: `{"timestamp": "ISO8601", "error_code": "E001", "operation": "add_task", "context": {...}}`

---

### Step 3: Build Menu-Driven CLI

**File**: `src/cli/app.py`

**Class**: TodoApp (stateless, depends on TodoService)

**Menu Options**:
```
1. Add Task
2. View All Tasks
3. Mark Complete/Incomplete
4. Update Task
5. Delete Task
6. Exit
```

**Main Loop** (`run()` method):
1. Display menu
2. Prompt for option (1–6)
3. Route to appropriate flow method
4. Handle errors gracefully
5. Repeat until user selects exit

---

### Step 4: Implement Each Feature Function

**Feature 1: Add Task** (`add_task_flow()`)
- Prompt for title (required)
- Prompt for description (optional)
- Call `service.add_task(title, description)`
- Display success with task ID or error message

**Feature 2: View Tasks** (`view_tasks_flow()`)
- Call `service.get_all_tasks()`
- Display "No tasks available" if empty
- For each task: display `[ID] STATUS TITLE` + description if present
- Status symbol: ✓ (complete) or ○ (incomplete)

**Feature 3: Mark Complete/Incomplete** (`toggle_task_status_flow()`)
- Prompt for task ID
- Check current status
- Toggle via `service.mark_complete()` or `service.mark_incomplete()`
- Display result or error

**Feature 4: Update Task** (`update_task_flow()`)
- Prompt for task ID
- Display current title and description
- Prompt for new title (press Enter to keep)
- Prompt for new description (press Enter to keep)
- Call `service.update_task()`
- Display result or error

**Feature 5: Delete Task** (`delete_task_flow()`)
- Prompt for task ID
- Display task to be deleted
- Request Y/N confirmation
- Call `service.delete_task()` if confirmed
- Display result or error

---

### Step 5: Add Input Validation

**Validation Points**:

1. **CLI Input**:
   - Menu selection: Must be 1–6
   - Task ID: Must be numeric
   - Title: Must not be empty/whitespace (delegate to Task model)

2. **Task Model Validation**:
   - Title: Non-empty, non-whitespace, max 500 chars
   - Description: Max 500 chars
   - Raise ValueError with error code for violations

3. **Service Layer Validation**:
   - Check task exists before update/delete
   - Return False or None for not-found (graceful degradation)
   - Raise ValueError for invalid operations

4. **Error Messages** (user-friendly):
   - `✗ Task title cannot be empty or contain only whitespace`
   - `✗ Task not found with ID {id}`
   - `✗ Invalid task ID. Please enter a number.`

---

### Step 6: Create Main Execution Loop

**File**: `main.py`

**Execution Flow**:
```python
def main():
    try:
        service = TodoService()
        app = TodoApp(service)
        app.run()  # Main loop
    except KeyboardInterrupt:
        print("\nGoodbye!")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
```

**Entry Point**: `python main.py`

---

### Step 7: Test Full Flow

**Test Strategy** (Test-First TDD):

1. **Unit Tests** (write before implementation):
   - Task model creation, validation, status changes
   - TodoService CRUD operations
   - CLI input parsing and routing
   - Error handling with error codes

2. **Integration Tests** (end-to-end workflows):
   - Add task → View tasks → Verify in list
   - Mark complete → View tasks → Verify status
   - Update task → Verify changes persist
   - Delete task → Verify removed
   - Full workflow: add → view → update → mark complete → delete

3. **Error Path Tests**:
   - Empty title rejection
   - Non-existent task handling
   - Invalid ID input
   - Rapid additions
   - Long text truncation

**Test Coverage Target**: 100% of user-facing functionality

---

## Extensibility Patterns (Clarifications-Locked)

### Pattern 1: Service Interface Isolation

**For Phase II Web**:
- TodoService implements ITaskService interface
- CLI calls methods; Phase II HTTP endpoints call same methods
- No CLI-specific code in service layer

### Pattern 2: JSON Serialization Contract

**For Phase IV Cloud**:
- Task.to_dict() → JSON matching spec schema
- Task.from_dict(json) → Reconstruct from JSON
- Phase IV cloud storage uses same schema

### Pattern 3: Structured Error Codes

**For Phase II–V Cross-Phase Debugging**:
- All errors use codes (E001–E005)
- Each error includes: timestamp, code, operation, context
- Phase IV logs use same codes

### Pattern 4: Extensibility Fields

**For Phase III AI Chatbot**:
- Task includes `tags` (List[str], optional) + `metadata` (Dict, optional)
- Phase I ignores; Phase III populates
- Phase IV can index/search tags

### Pattern 5: Multi-User Namespace

**For Phase II Web + Phase IV Cloud**:
- Phase I task IDs are unique within single-user context
- Document: Phase II adds `user_id:task_id` prefix
- Phase I ID generation unchanged; namespace added at Phase II layer

---

## Non-Functional Requirements

**Performance**:
- ✅ All operations < 10ms (target: < 100ms per spec)
- ✅ Memory: Negligible for console app (tested with 1000+ tasks)
- ✅ Startup: < 100ms

**Reliability**:
- ✅ Graceful error handling; no crashes on invalid input
- ✅ Data integrity: Task state never corrupted by operations
- ✅ Idempotency: Repeated same operation yields consistent result

**Maintainability**:
- ✅ 3-layer architecture enables independent testing
- ✅ Service interface enables Phase II HTTP wrapping
- ✅ Error codes and JSON schema enable Phase IV integration
- ✅ Extensibility fields enable Phase III AI features

---

## Definition of Done

Each layer is done when:
1. ✅ Acceptance scenarios all pass
2. ✅ Unit tests written and passing (100% of layer)
3. ✅ Integration tests pass (workflows involving layer)
4. ✅ Input validation prevents invalid states
5. ✅ Error messages are clear and use error codes
6. ✅ Code follows PEP 8 and has docstrings
7. ✅ Extensibility patterns are implemented (service interface, JSON schema, error codes, metadata fields)

---

## Risk Analysis

### Top 3 Risks

1. **Invalid input crashes** → Mitigated by comprehensive validation + error codes
2. **Data corruption from concurrent edits** → N/A (single-threaded, single-user); future: add locking at Phase II
3. **Phase II incompatibility** → Mitigated by service interface + JSON schema locked in Phase I

---

## Next Steps After Planning

1. **Phase 0 Research**: None needed; clarifications already resolved in `/sp.clarify`
2. **Phase 1 Design**: Generate `data-model.md`, `contracts/task_service.md`, `quickstart.md`
3. **Phase 2 Tasks**: Run `/sp.tasks` to generate 47 actionable tasks with dependencies
4. **Implementation**: Follow task breakdown; TDD all the way

---

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| **3-Layer Architecture** | Enables independent testing; Phase II can reuse service; Phase III can extend model |
| **ITaskService Interface** | Phase II HTTP layer wraps same interface; prevents service redesign |
| **JSON Schema + Error Codes** | Phase IV cloud adopts same format; enables seamless integration |
| **Extensibility Fields** | Tags/metadata for Phase III AI without Phase I changes |
| **Single-User ID Strategy** | Phase I simple; Phase II adds namespace; clear contract documented |
| **In-Memory Only** | Aligns with Phase I constraint; Phase IV adds persistence layer |

---

## Conclusion

Phase I is architected as a **foundational, extensible library** with clear separation of concerns. The 7-step implementation strategy incorporates clarifications and enables Phases II–V to build without redesigning Phase I logic. All code will be tested, documented, and production-ready.

**Ready for Phase 2 (Task Generation)**: `/sp.tasks`
