# Tasks: Console Todo Application (Phase I)

**Input**: Design documents from `specs/001-todo-app/`
**Prerequisites**: plan.md, spec-v2.md, data-model.md, contracts/task_service.md
**Organization**: 47 implementation tasks organized by 6 user stories (P1 priority first, then P2)
**Test-Driven**: Tests written first; all tests designed to FAIL before implementation

---

## Format: `- [ ] [TaskID] [P?] [Story] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: User story label (US1, US2, US3, US4, US5, US6)
- **File paths**: Absolute and specific; enables independent completion

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure ready for all layers

- [ ] T001 Create project directory structure per plan.md at repo root
- [ ] T002 [P] Create `src/` directory with `__init__.py`
- [ ] T003 [P] Create `src/models/` directory with `__init__.py`
- [ ] T004 [P] Create `src/services/` directory with `__init__.py`
- [ ] T005 [P] Create `src/cli/` directory with `__init__.py`
- [ ] T006 [P] Create `tests/` directory with `__init__.py`
- [ ] T007 [P] Create `tests/unit/` directory with `__init__.py`
- [ ] T008 [P] Create `tests/integration/` directory with `__init__.py`
- [ ] T009 Create `main.py` entry point stub with exception handling structure
- [ ] T010 [P] Create `requirements.txt` (empty - no external dependencies)
- [ ] T011 [P] Create `README.md` with quick start guide
- [ ] T012 [P] Create `ARCHITECTURE.md` documenting 3-layer design

**Checkpoint**: Project structure ready for implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data model and service interface MUST be complete before ANY user story work begins

⚠️ **CRITICAL**: No user story work can begin until this phase is 100% complete

### Error Handling & Structured Error Codes

- [ ] T013 [P] Create `src/services/exceptions.py` with error code class containing E001-E005 constants
- [ ] T014 [P] Create unit test `tests/unit/test_error_codes.py` with tests for all 5 error codes

### Task Data Model

- [ ] T015 [P] Write unit tests FIRST in `tests/unit/test_task_model.py` (15+ test cases)
- [ ] T016 Implement `src/models/task.py` Task class with all methods and validation

### Service Interface & In-Memory Implementation

- [ ] T017 [P] Write unit tests FIRST in `tests/unit/test_task_service.py` (18+ test cases)
- [ ] T018 Implement `src/services/task_service.py` TodoService class

### CLI Input Validation Layer

- [ ] T019 [P] Write unit tests FIRST in `tests/unit/test_cli_validation.py` (5+ test cases)
- [ ] T020 Create `src/cli/validators.py` with validation helper functions

**Checkpoint**: Foundation ready - all user stories can now proceed in parallel

---

## Phase 3: User Story 1 - Add Task (Priority: P1) MVP

**Goal**: Users can quickly add a new task with title and optional description; system assigns unique ID and stores in memory

**Independent Test**: Start app, select "Add Task", enter title, confirm, verify task appears in list with unique ID and incomplete status

### Unit Tests for User Story 1

- [ ] T021 [P] [US1] Write feature test for add_task_flow() in `tests/unit/test_add_task_cli.py`

### Implementation for User Story 1

- [ ] T022 [US1] Implement `add_task_flow()` method in `src/cli/app.py`
- [ ] T023 [US1] Implement `TodoApp.__init__()` and menu structure in `src/cli/app.py`

**Checkpoint**: User Story 1 complete - add_task functionality works independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Users can see all tasks in human-readable format showing ID, title, description, and completion status

**Independent Test**: Add multiple tasks with varied completion states, select "View Tasks", verify all tasks display correctly

### Unit Tests for User Story 2

- [ ] T024 [P] [US2] Write feature test for view_tasks_flow() in `tests/unit/test_view_tasks_cli.py`

### Implementation for User Story 2

- [ ] T025 [US2] Implement `view_tasks_flow()` method in `src/cli/app.py`

**Checkpoint**: User Stories 1 & 2 complete - users can add and view tasks independently

---

## Phase 5: User Story 3 - Mark Task Complete (Priority: P1)

**Goal**: Users can toggle task completion status by ID; completed tasks remain in list but visually distinct

**Independent Test**: Add task, mark complete, verify status changes in view, toggle back to incomplete, verify status reverts

### Unit Tests for User Story 3

- [ ] T026 [P] [US3] Write feature test for toggle_task_status_flow() in `tests/unit/test_toggle_status_cli.py`

### Implementation for User Story 3

- [ ] T027 [US3] Implement `toggle_task_status_flow()` method in `src/cli/app.py`

**Checkpoint**: User Stories 1, 2, & 3 complete - users can add, view, and toggle status (MVP!)

---

## Phase 6: User Story 4 - Update Task (Priority: P2)

**Goal**: Users can edit task title and/or description by ID without changing task ID

**Independent Test**: Create task, select "Update Task", enter ID and new values, verify changes appear in task list

### Unit Tests for User Story 4

- [ ] T028 [P] [US4] Write feature test for update_task_flow() in `tests/unit/test_update_task_cli.py`

### Implementation for User Story 4

- [ ] T029 [US4] Implement `update_task_flow()` method in `src/cli/app.py`

**Checkpoint**: User Stories 1-4 complete - users can add, view, toggle, and update tasks

---

## Phase 7: User Story 5 - Delete Task (Priority: P2)

**Goal**: Users can permanently remove task by ID with confirmation prompt

**Independent Test**: Create task, select "Delete Task", enter ID, confirm deletion, verify task no longer in list

### Unit Tests for User Story 5

- [ ] T030 [P] [US5] Write feature test for delete_task_flow() in `tests/unit/test_delete_task_cli.py`

### Implementation for User Story 5

- [ ] T031 [US5] Implement `delete_task_flow()` method in `src/cli/app.py`

**Checkpoint**: User Stories 1-5 complete - users can add, view, toggle, update, and delete tasks

---

## Phase 8: User Story 6 - Clean Exit (Priority: P1)

**Goal**: Users can cleanly close application with dedicated exit option; application terminates gracefully without crashing

**Independent Test**: Select "Exit" or press Ctrl+C, verify app terminates cleanly with goodbye message, no errors or crashes

### Unit Tests for User Story 6

- [ ] T032 [P] [US6] Write feature test for exit flow in `tests/unit/test_exit_cli.py`

### Implementation for User Story 6

- [ ] T033 [US6] Implement `TodoApp.run()` main loop method in `src/cli/app.py`
- [ ] T034 [US6] Implement `exit_flow()` method in `src/cli/app.py`
- [ ] T035 [US6] Implement main() function in `main.py`

**Checkpoint**: User Story 6 complete - full menu-driven application with clean exit

---

## Phase 9: Integration & End-to-End Testing

**Purpose**: Verify all user stories work together in complete workflows

### Integration Tests

- [ ] T036 [P] Write integration test in `tests/integration/test_app_workflow.py`
- [ ] T037 [P] Write error path tests in `tests/integration/test_error_handling.py`

### Validation & Entry Point

- [ ] T038 Verify `main.py` entry point works end-to-end

**Checkpoint**: All user stories integrated and working end-to-end

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Code quality, documentation, and production readiness

### Code Quality & Structure

- [ ] T039 [P] Review all code against Constitution principles
- [ ] T040 [P] Implement logging in `src/services/task_service.py`
- [ ] T041 [P] Add docstrings to all public methods
- [ ] T042 [P] Code formatting cleanup (PEP 8 compliance)

### Documentation

- [ ] T043 [P] Update `README.md` with feature overview and quick start
- [ ] T044 [P] Update `ARCHITECTURE.md` with diagrams and patterns
- [ ] T045 [P] Create `tests/README.md` with testing strategy

### Final Validation

- [ ] T046 Run all tests and verify 100% pass
- [ ] T047 [P] Manual end-to-end validation

**Checkpoint**: Phase I console Todo application fully complete and production-ready ✅

---

## Dependencies & Execution Order

### Phase Dependencies

1. **Setup (Phase 1)**: No dependencies - starts immediately
2. **Foundational (Phase 2)**: Depends on Setup complete - BLOCKS all user stories
3. **User Stories (Phases 3-8)**: All depend on Foundational complete
4. **Integration (Phase 9)**: Depends on all user stories complete
5. **Polish (Phase 10)**: Depends on integration complete

### Parallel Opportunities

- **Setup Phase**: T002-T012 (all marked [P]) can run in parallel
- **Foundational Phase**: T013-T014, T015-T016, T017-T018, T019-T020 can be strategically parallelized
- **User Story Phases**: All user story tests can run in parallel; US4 and US5 can be developed in parallel
- **Polish Phase**: T039-T045 (all marked [P]) can run in parallel

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Setup (Phase 1)
2. Complete Foundational (Phase 2)
3. Complete US1 (Phase 3)
4. **STOP and VALIDATE**: Run tests, test manually, verify core "Add Task" works
5. If good: proceed to US2-6

### Incremental Delivery

Build value incrementally - each story adds complete, independent functionality:

1. Setup + Foundational → Foundation ready
2. Add US1 (Add) → Users can add tasks (MVP!)
3. Add US2 (View) → Users can see tasks
4. Add US3 (Mark Complete) → Users can track progress
5. Add US4 (Update) → Users can fix mistakes
6. Add US5 (Delete) → Users can remove tasks
7. Add US6 (Exit) → Users can cleanly close
8. Polish → Production-ready

---

## Quality Gates

**Setup Phase Complete**: ✅ All directories and files exist per structure

**Foundational Phase Complete**: ✅ All 5 error codes defined, Task model validated, TodoService passes contract tests, validators ready

**Each User Story Complete**: ✅ User story tests PASS, feature works independently

**Integration Complete**: ✅ All user stories work together, error paths tested, no crashes

**Polish Complete**: ✅ Code reviewed, documented, tested (100% coverage), manual validation successful

---

## Notes

- Each task has specific file path - enables parallel work
- Tests written FIRST - red-green-refactor cycle
- [P] marked tasks can run in parallel (different files, no dependencies)
- [Story] labels map tasks to user stories for traceability
- Commit after each completed phase or logical task group
- Stop at any checkpoint to validate independently before proceeding

---

**Ready to start implementation!** Begin with Phase 1 (Setup) and proceed through phases sequentially.
