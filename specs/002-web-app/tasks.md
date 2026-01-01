# Tasks: Phase II – Full-Stack Web Todo Application

**Feature**: Phase II – Full-Stack Web Todo Application
**Branch**: `002-web-app`
**Created**: 2025-12-29
**Total Tasks**: 108 (MVP: 96 tasks across Phases 1-6)
**Approach**: TDD (Test-First, Red-Green-Refactor)

## Format: `- [ ] [ID] [P?] [Story?] Description with file path`

- **[P]**: Task can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, US3...)
- Paths are for web application structure (backend/, frontend/)

## Implementation Strategy

**MVP First**: Complete user stories 1-3 (P1 priority) before advanced features
**TDD Cycle**: Write tests (RED) → Implement (GREEN) → Refactor
**Independence**: Each user story independently testable and deployable

---

## Phase 1: Backend & Frontend Setup (T001-T020)

Project initialization and infrastructure

### Backend Project Setup

- [ ] T001 Initialize backend directory structure with FastAPI app skeleton at backend/src/main.py
- [ ] T002 Create backend/requirements.txt with FastAPI, SQLModel, Pydantic, pytest, uvicorn
- [ ] T003 Create backend/Dockerfile for containerization with Python 3.9+ base image
- [ ] T004 Create backend/.env.example with DATABASE_URL, SERVER_PORT, ENVIRONMENT variables
- [ ] T009 Create backend/src/core/config.py for environment configuration and FastAPI settings
- [ ] T010 Create backend/src/core/errors.py with custom exceptions and error codes (E001-E005)
- [ ] T011 Create backend/src/services/db.py for database session and Neon connection pooling
- [ ] T012 Create backend/src/api/dependencies.py for dependency injection (session, auth)

### Frontend Project Setup

- [ ] T005 [P] Initialize frontend directory structure with Next.js 18+ project at frontend/
- [ ] T006 [P] Create frontend/package.json with Next.js, React, TypeScript, Tailwind, testing deps
- [ ] T007 [P] Create frontend/Dockerfile for Node.js containerization
- [ ] T008 [P] Create frontend/.env.example with API_BASE_URL, NODE_ENV variables
- [ ] T013 [P] Create frontend/src/types/index.ts with TypeScript interfaces for Task, Tag, Priority
- [ ] T014 [P] Create frontend/src/utils/constants.ts with API endpoints, priorities, error messages
- [ ] T015 [P] Create frontend/src/services/api.ts with HTTP client wrapper for API calls
- [ ] T016 [P] Create frontend/next.config.js with optimization settings
- [ ] T017 [P] Create frontend/tsconfig.json with TypeScript configuration

### Database & Models Setup

- [ ] T018 Create backend/src/models/__init__.py as models package
- [ ] T019 Create backend/src/models/priority.py with Priority enum (HIGH, MEDIUM, LOW)
- [ ] T020 Create Neon database schema initialization script or migration setup

---

## Phase 2: Data Models & API Schema (T021-T035)

Database schema, ORM models, and API contract definition

### Database Models

- [ ] T021 Create backend/src/models/task.py with SQLModel Task entity: id, title, description, is_completed, priority, created_at, updated_at, metadata, scheduled_at
- [ ] T022 Create backend/src/models/tag.py with SQLModel Tag entity for many-to-many relationships
- [ ] T023 Create database indexes: (is_completed, priority, created_at), (tag.name), (created_at DESC)
- [ ] T024 [P] Create Neon database schema migration or initialization script

### API Schemas & Services

- [ ] T025 Create backend/src/api/schemas/task.py with Pydantic schemas for Task CRUD
- [ ] T026 Create backend/src/api/schemas/tag.py with Pydantic schemas for Tag operations
- [ ] T027 Create backend/src/api/schemas/__init__.py to export all schemas
- [ ] T028 Create backend/src/services/__init__.py as services package
- [ ] T029 Create backend/src/services/task_service.py with TaskService wrapping Phase I TodoService
- [ ] T030 Create backend/src/services/tag_service.py with TagService for tag CRUD
- [ ] T031 Create backend/tests/integration/test_db_operations.py for database connection tests

### API Router Structure

- [ ] T032 Create backend/src/api/endpoints/__init__.py
- [ ] T033 Create backend/src/api/router.py to aggregate route blueprints
- [ ] T034 Create backend/src/api/endpoints/tasks.py with stub endpoints for CRUD
- [ ] T035 Create backend/src/api/endpoints/tags.py with stub endpoints for tag operations

---

## Phase 3: User Story 1 – View All Tasks (P1) (T036-T060)

Users can see list of all tasks with completion status

**Test**: Load dashboard → verify all tasks display correctly

### Backend Implementation

- [ ] T036 [US1] Implement GET /api/tasks endpoint in backend/src/api/endpoints/tasks.py with pagination
- [ ] T037 [US1] Create pytest test backend/tests/integration/test_api_tasks.py: list empty tasks, list 5 tasks, pagination
- [ ] T038 [US1] Run T037 tests - should FAIL (RED phase)
- [ ] T039 [US1] Connect TaskService to database in backend/src/services/task_service.py
- [ ] T040 [US1] Implement task_service.get_all_tasks(skip, limit) method returning List[Task]
- [ ] T041 [US1] Create test backend/tests/integration/test_db_operations.py: create 3 tasks, retrieve all, verify count
- [ ] T042 [US1] Run T041 tests - should FAIL (RED phase)
- [ ] T052 [US1] Implement TaskService.get_all_tasks() to query Task table from database (GREEN phase)
- [ ] T053 [US1] Wire up database session to TaskService in FastAPI endpoint
- [ ] T054 [US1] Run T037, T041 tests - should PASS (GREEN phase)

### Frontend Implementation

- [ ] T043 [US1] Create frontend/src/components/TaskCard.tsx displaying title, description, completion status
- [ ] T044 [US1] Create frontend/src/components/TaskList.tsx for rendering list of tasks
- [ ] T045 [US1] Create frontend/src/hooks/useTasks.ts hook with SWR data fetching from /api/tasks
- [ ] T046 [US1] Create frontend/src/pages/index.tsx dashboard with TaskList, useTasks hook, loading state
- [ ] T047 [US1] Create frontend/tests/unit/components/TaskCard.test.tsx: render with props, completion styling
- [ ] T048 [US1] Create frontend/tests/unit/components/TaskList.test.tsx: render multiple tasks, empty state
- [ ] T049 [US1] Run T047, T048 tests - should FAIL (RED phase)
- [ ] T050 [US1] Create frontend/tests/integration/task-workflow.test.tsx (Cypress): load dashboard, verify task list
- [ ] T051 [US1] Run T050 test - should FAIL (RED phase)
- [ ] T055 [US1] Implement useTasks hook with actual SWR fetch from /api/tasks (GREEN phase)
- [ ] T056 [US1] Implement TaskCard styling for completion status (strikethrough, color)
- [ ] T057 [US1] Run T047, T048, T050 tests - should PASS (GREEN phase)

### Validation & Performance

- [ ] T058 [US1] Test with 1000+ tasks in database to verify performance (<2s dashboard load)
- [ ] T059 [US1] Verify database indexes are used (query performance analysis)
- [ ] T060 [US1] Run all Task View tests - verify all PASS

---

## Phase 4: User Story 2 – Add a New Task (P1) (T061-T078)

Users can create new tasks with title and optional description

**Test**: Fill form → submit → verify task appears in list

### Backend Implementation

- [ ] T061 [US2] [P] Create pytest test backend/tests/integration/test_api_tasks.py: POST with title, POST with description, validation errors
- [ ] T062 [US2] [P] Run T061 tests - should FAIL (RED phase)
- [ ] T063 [US2] [P] Implement POST /api/tasks endpoint in backend/src/api/endpoints/tasks.py
- [ ] T064 [US2] [P] Implement TaskService.create_task(title, description) method
- [ ] T065 [US2] [P] Create validation in backend/src/models/task.py: title required/non-empty/max 500, description max 500
- [ ] T066 [US2] [P] Run T061 tests - should PASS (GREEN phase)

### Frontend Implementation

- [ ] T067 [US2] [P] Create frontend/src/components/TaskForm.tsx with title/description inputs, submit button, error display
- [ ] T068 [US2] [P] Add validation to frontend/src/utils/validators.ts: title (non-empty, max 500), description (max 500)
- [ ] T069 [US2] [P] Create frontend/src/hooks/useCreateTask.ts hook: POST to /api/tasks, revalidate task list
- [ ] T070 [US2] [P] Add TaskForm component to frontend/src/pages/index.tsx
- [ ] T071 [US2] [P] Wire up useCreateTask hook to TaskForm submission, clear form after success
- [ ] T072 [US2] [P] Handle errors gracefully (show validation messages)

### Testing & Validation

- [ ] T073 [US2] [P] Create frontend/tests/unit/components/TaskForm.test.tsx: render form, validation display, submit state
- [ ] T074 [US2] [P] Run T073 tests - should PASS (GREEN phase)
- [ ] T075 [US2] [P] Create Cypress test in frontend/tests/integration/task-workflow.test.tsx: fill form, submit, verify appears
- [ ] T076 [US2] [P] Run T075 test - should PASS (GREEN phase)
- [ ] T077 [US2] [P] Run all Task Creation tests (T061-T076) - verify all PASS
- [ ] T078 [US2] [P] Test rapid submissions (5+ tasks in succession) - verify separate creation

---

## Phase 5: User Story 3 – Mark Task Complete (P1) (T079-T096)

Users can toggle task completion status with visual indication

**Test**: Mark task complete → verify strikethrough displays

### Backend Implementation

- [ ] T079 [US3] [P] Create pytest test backend/tests/integration/test_api_tasks.py: PATCH mark complete, mark incomplete, toggle, invalid ID (E002)
- [ ] T080 [US3] [P] Run T079 tests - should FAIL (RED phase)
- [ ] T081 [US3] [P] Implement PATCH /api/tasks/{id}/complete endpoint in backend/src/api/endpoints/tasks.py
- [ ] T082 [US3] [P] Implement TaskService.update_task_completion(id, is_completed) method
- [ ] T083 [US3] [P] Run T079 tests - should PASS (GREEN phase)

### Frontend Implementation

- [ ] T084 [US3] [P] Add checkbox/button to TaskCard component for completion toggle
- [ ] T085 [US3] [P] Create frontend/src/hooks/useToggleTask.ts hook: PATCH to /api/tasks/{id}/complete, revalidate
- [ ] T086 [US3] [P] Add CSS classes for strikethrough/completion styling to frontend/src/styles/globals.css
- [ ] T087 [US3] [P] Wire up useToggleTask hook to TaskCard checkbox click
- [ ] T088 [US3] [P] Add optimistic UI update (show strikethrough before server response)
- [ ] T089 [US3] [P] Handle errors gracefully (revert UI on server error)

### Testing & Validation

- [ ] T090 [US3] [P] Create frontend/tests/unit/components/TaskCard.test.tsx: completion checkbox, strikethrough styling
- [ ] T091 [US3] [P] Run T090 tests - should PASS (GREEN phase)
- [ ] T092 [US3] [P] Add Cypress test to frontend/tests/integration/task-workflow.test.tsx: create, mark complete, verify strikethrough
- [ ] T093 [US3] [P] Run T092 test - should PASS (GREEN phase)
- [ ] T094 [US3] [P] Run all Phase 5 tests (T079-T093) - verify all PASS
- [ ] T095 [US3] [P] Run full end-to-end workflow test with all MVP features
- [ ] T096 [US3] [P] Verify MVP completes all P1 user story acceptance scenarios

---

## Phase 6: Polish & Deployment (T097-T108)

Production readiness, testing, and documentation

### Testing & Quality

- [ ] T097 Run full test suite: backend (pytest), frontend (Jest), e2e (Cypress)
- [ ] T098 Generate code coverage reports; verify >80% coverage
- [ ] T099 Run linting: ESLint frontend, Flake8 backend
- [ ] T100 Test with concurrent load (simulate 100+ simultaneous users)

### Documentation & Deployment

- [ ] T101 Create README.md with local development instructions
- [ ] T102 Create docker-compose.yml for local dev environment
- [ ] T103 Create deployment guide for backend (FastAPI) and frontend (Next.js)
- [ ] T104 Document API endpoints in OpenAPI/Swagger format (FastAPI auto-generates)
- [ ] T105 Set up GitHub Actions CI/CD pipeline for automated testing

### Final Verification

- [ ] T106 Verify all MVP acceptance scenarios pass
- [ ] T107 Performance testing: dashboard <2s, API <200ms
- [ ] T108 User acceptance testing with sample data (100+ tasks)

---

## MVP COMPLETE ✓

**MVP Consists of**:
- 108 total tasks (96 core implementation, 12 future phases)
- 3 user stories completed (View, Add, Mark Complete)
- All acceptance scenarios passing
- Full test coverage (unit, integration, e2e)
- Deployed and production-ready

---

## Future Phases (Optional - After MVP)

### Phase 7-13: User Stories 4-10 (P2, P3 Priority)
- User Story 4: Update Task
- User Story 5: Delete Task
- User Story 6: Add Priority
- User Story 7: Add Tags
- User Story 8: Filter Tasks
- User Story 9: Search Tasks
- User Story 10: Sort Tasks

Each additional user story follows same TDD pattern (RED-GREEN-REFACTOR)

---

## Execution Notes

**Critical Path**:
1. Phase 1 (Setup) - MUST complete first
2. Phase 2 (Models & Schema) - MUST complete before Phase 3
3. Phase 3 (View) → Phase 4 (Add) → Phase 5 (Complete) → Phase 6 (Polish)

**Parallelization**:
- Backend setup (T001-T004) parallel with Frontend setup (T005-T008)
- Backend services (T029-T030) parallel with Frontend components (T043-T046)
- Tests can run in parallel if infrastructure supports it

**Success Criteria**:
- All 96 MVP tasks marked [X]
- All tests passing
- Dashboard accessible at http://localhost:3000
- Can view, add, mark complete end-to-end
- Performance targets met
- Zero critical issues

**Next Step**: Run `/sp.implement` to begin task execution.
