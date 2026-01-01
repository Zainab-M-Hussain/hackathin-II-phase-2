# Implementation Plan: Phase II – Full-Stack Web Todo Application

**Branch**: `002-web-app` | **Date**: 2025-12-29
**Spec**: `/specs/002-web-app/spec-v2.md` (Implementation-Ready)
**Status**: Ready for Task Generation & Development

## Executive Summary

Build a production-ready full-stack web application with persistent PostgreSQL storage, clean REST API, and professional Next.js UI. The plan is organized around 9 concrete implementation phases with clear dependencies and deliverables.

**Key Focus**:
- Database schema design for scalability (Phase III AI-ready)
- SQLModel entities with validation
- FastAPI async REST endpoints
- Neon Serverless Postgres integration
- Next.js dashboard with filtering/sorting
- Full end-to-end integration testing

**Timeline**: 60-80 hours of development (TDD approach)
**Architecture**: 3-layer (Model → Service → API) + React UI
**Testing**: Red-Green-Refactor cycle (tests before implementation)

---

## Technical Context

**Backend**:
- Language: Python 3.9+
- Framework: FastAPI (async, auto-docs)
- ORM: SQLModel (Pydantic + SQLAlchemy)
- Testing: pytest, FastAPI TestClient
- Database: Neon Serverless Postgres

**Frontend**:
- Framework: Next.js 18+ with React 18+
- Language: TypeScript 5+
- Styling: Tailwind CSS (functional, not perfect)
- Data Fetching: SWR (polling every 5-10s)
- Testing: Jest, React Testing Library, Cypress

**Database**:
- Provider: Neon (serverless, auto-scaling)
- Connection: Pooled via SQLModel
- Schema: Hybrid (normalized + denormalized)
- Indexes: On frequently filtered/sorted columns

**API**:
- Protocol: REST with JSON
- Documentation: OpenAPI (FastAPI auto-generates)
- Validation: Pydantic schemas
- Error Handling: Structured error codes (E001-E005 from Phase I)

---

## Constitution Check

**From Phase I Constitution** (Inferred):
- ✅ **Library-First**: Phase I TodoService reusable; Phase II wraps via API
- ✅ **Clear Separation**: 3-layer maintained (Model → Service → HTTP API)
- ✅ **Test-First**: TDD enforced; tests before implementation
- ✅ **Integration Testing**: Full end-to-end workflows tested
- ✅ **Zero External Dependencies**: SQLModel, FastAPI are production-grade
- ✅ **Simplicity**: Direct API-to-Service mapping, no unnecessary abstraction

**Phase II Specific**:
- Zero redesign of Phase I service interface (backward compatible)
- Database schema designed for Phase III AI extensibility
- Audit logging for AI learning and compliance
- API contract frozen after Phase II (backward compatible in Phase III)

**Status**: ✅ **PASS** - No constitution violations

---

## Project Structure

### Documentation Files

```
specs/002-web-app/
├── spec.md              (clarified spec with decisions)
├── spec-v2.md           (implementation-ready detailed spec)
├── plan.md              (initial technical context)
├── plan-v2.md           (this file - detailed implementation plan)
├── data-model.md        (Phase 1 deliverable)
├── contracts/           (Phase 1 deliverable)
│   ├── openapi.json    (API specification)
│   └── README.md       (contract documentation)
├── quickstart.md        (Phase 1 deliverable - local dev setup)
└── tasks.md            (108 implementation tasks)
```

### Source Code Structure

```
backend/
├── src/
│   ├── main.py                          # FastAPI app entry point
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py                     # Task SQLModel entity
│   │   ├── tag.py                      # Tag SQLModel entity
│   │   ├── audit_log.py                # AuditLog for Phase III
│   │   └── base.py                     # Base model with common fields
│   ├── services/
│   │   ├── __init__.py
│   │   ├── db.py                       # Database session, connection pooling
│   │   ├── task_service.py             # Task CRUD business logic
│   │   └── tag_service.py              # Tag management
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py                   # Route aggregation
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── tasks.py               # Task endpoints
│   │   │   └── tags.py                # Tag endpoints
│   │   └── schemas/
│   │       ├── __init__.py
│   │       ├── task.py                # Task Pydantic schemas
│   │       └── tag.py                 # Tag Pydantic schemas
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                  # FastAPI config, env vars
│   │   ├── errors.py                  # Error handling, error codes
│   │   └── dependencies.py            # Dependency injection (session)
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py                    # pytest fixtures
│   ├── unit/
│   │   ├── test_models.py             # Model validation tests
│   │   ├── test_services.py           # Service logic tests
│   │   └── test_schemas.py            # Schema validation tests
│   └── integration/
│       ├── test_api_tasks.py          # Task endpoint tests
│       ├── test_api_tags.py           # Tag endpoint tests
│       ├── test_db_operations.py      # Database tests
│       └── test_full_workflow.py      # End-to-end workflow
├── requirements.txt
├── .env.example
├── Dockerfile
└── main.py                            # Entry point

frontend/
├── src/
│   ├── components/
│   │   ├── TaskList.tsx               # Main task list
│   │   ├── TaskCard.tsx               # Task display card
│   │   ├── TaskForm.tsx               # Create/edit form
│   │   ├── FilterBar.tsx              # Filter controls
│   │   ├── SearchBar.tsx              # Search input
│   │   ├── SortControls.tsx           # Sort selector
│   │   ├── DeleteConfirm.tsx          # Delete confirmation modal
│   │   └── Layout.tsx                 # App layout wrapper
│   ├── pages/
│   │   ├── index.tsx                  # Dashboard page
│   │   ├── _app.tsx                   # App wrapper
│   │   └── _document.tsx              # Document wrapper
│   ├── services/
│   │   ├── api.ts                     # HTTP client
│   │   └── taskService.ts             # Task API calls
│   ├── hooks/
│   │   ├── useTasks.ts                # Fetch tasks with SWR
│   │   ├── useFilters.ts              # Filter state
│   │   ├── useSearch.ts               # Search state
│   │   └── useSort.ts                 # Sort state
│   ├── types/
│   │   ├── index.ts                   # Core types
│   │   ├── task.ts                    # Task types
│   │   └── api.ts                     # API types
│   ├── styles/
│   │   ├── globals.css                # Global styles
│   │   └── components.css             # Component styles
│   ├── utils/
│   │   ├── constants.ts               # Constants & enums
│   │   ├── validators.ts              # Client validation
│   │   └── formatters.ts              # Date & text formatting
│   └── __init__.ts
├── tests/
│   ├── unit/
│   │   ├── components/
│   │   │   ├── TaskList.test.tsx
│   │   │   ├── TaskCard.test.tsx
│   │   │   ├── TaskForm.test.tsx
│   │   │   ├── FilterBar.test.tsx
│   │   │   └── SearchBar.test.tsx
│   │   ├── hooks/
│   │   │   ├── useTasks.test.ts
│   │   │   ├── useFilters.test.ts
│   │   │   └── useSearch.test.ts
│   │   └── services/
│   │       └── api.test.ts
│   └── integration/
│       ├── task-workflow.test.tsx     # Full workflow (Cypress)
│       ├── filter-sort.test.tsx       # Filter & sort (Cypress)
│       └── error-handling.test.tsx    # Error scenarios (Cypress)
├── public/                             # Static assets
├── package.json
├── tsconfig.json
├── next.config.js
├── jest.config.js
├── .env.example
├── Dockerfile
└── .eslintrc.json

docker-compose.yml                     # Local dev environment
.gitignore
.env.example
```

---

## Implementation Plan: 9 Concrete Phases

### Phase 1: Design Database Schema (Foundation)

**Goal**: Define comprehensive schema for Task, Tag, AuditLog entities with relationships and indexes

**Key Decisions**:
- Hybrid approach: normalized (tags, audit_log) + denormalized (priority) for performance
- Many-to-many for Task-Tag relationship via junction table
- Indexes on frequently filtered/sorted columns
- Audit logging for Phase III AI readiness

**Deliverables**:
1. **database-schema.sql**
   - CREATE TABLE tasks (id SERIAL PK, title VARCHAR(500) NOT NULL, description VARCHAR(500), status ENUM, priority ENUM, created_at TIMESTAMP, updated_at TIMESTAMP, due_date TIMESTAMP, metadata JSONB, scheduled_at TIMESTAMP, agent_state JSONB)
   - CREATE TABLE tags (id SERIAL PK, name VARCHAR(50) UNIQUE, created_at TIMESTAMP)
   - CREATE TABLE task_tags (task_id FK, tag_id FK, PRIMARY KEY)
   - CREATE TABLE audit_logs (id SERIAL PK, task_id FK, action VARCHAR, previous_state JSONB, new_state JSONB, actor VARCHAR, reason VARCHAR, timestamp TIMESTAMP, metadata JSONB)
   - CREATE INDEXES on (tasks.is_completed, tasks.priority, tasks.created_at), (tags.name), (tasks.created_at DESC)

2. **data-model.md** (design document)
   - Entity definitions with relationships
   - Field constraints and validations
   - Index strategy
   - Migration approach

**Success Criteria**:
- Schema supports all 35 functional requirements
- Indexes on query performance paths
- Ready for SQLModel entity mapping
- Audit trail captures all changes

---

### Phase 2: Implement SQLModel Entities (ORM Layer)

**Goal**: Create SQLModel models with Pydantic validation matching database schema

**Dependencies**: Phase 1 schema design complete

**Deliverables**:
1. **backend/src/models/base.py**
   - Base model with id, created_at, updated_at fields
   - Timestamp auto-generation

2. **backend/src/models/task.py**
   - Task entity: id, title, description, status, priority, created_at, updated_at, due_date, metadata, scheduled_at, agent_state
   - Relationships: tags (many-to-many), audit_logs (one-to-many)
   - Validators: title (required, max 500), description (max 500), due_date (valid date)
   - Fields enum for status (pending/complete), priority (Low/Medium/High)

3. **backend/src/models/tag.py**
   - Tag entity: id, name (unique, max 50), created_at
   - Relationship: tasks (many-to-many)

4. **backend/src/models/audit_log.py**
   - AuditLog entity: id, task_id, action, previous_state, new_state, actor, reason, timestamp, metadata
   - Relationship: task (one-to-many)

5. **backend/src/models/__init__.py**
   - Export all models

**Tests**:
- backend/tests/unit/test_models.py: Model instantiation, validation, constraints

**Success Criteria**:
- All entities instantiate correctly
- Pydantic validation works (rejects invalid title, description)
- Relationships defined and accessible
- Ready for service layer use

---

### Phase 3: Build FastAPI Backend Infrastructure (API Foundation)

**Goal**: Set up FastAPI app, database connections, configuration, error handling

**Dependencies**: Phase 2 entities complete

**Deliverables**:
1. **backend/src/core/config.py**
   - Environment variables: DATABASE_URL, SERVER_HOST, SERVER_PORT, ENVIRONMENT
   - FastAPI settings: debug mode, allowed hosts, CORS configuration
   - Logging configuration

2. **backend/src/core/errors.py**
   - Error code constants: E001-E005 (from Phase I)
   - Custom exception classes
   - Exception handlers for FastAPI

3. **backend/src/services/db.py**
   - SQLAlchemy session factory
   - Neon connection pooling configuration
   - Database initialization (create tables if needed)
   - Session dependency for API endpoints

4. **backend/src/api/dependencies.py**
   - Dependency injection functions
   - get_db() for database session
   - get_current_user() placeholder for future auth

5. **backend/src/main.py**
   - FastAPI app initialization
   - Router registration
   - Middleware setup (CORS, error handling)
   - Startup/shutdown events

6. **backend/src/core/__init__.py** & **backend/src/api/__init__.py**
   - Package initialization

7. **backend/requirements.txt**
   - fastapi, uvicorn, sqlmodel, pydantic, python-dotenv, psycopg2-binary, alembic
   - Testing: pytest, pytest-asyncio, httpx

8. **backend/.env.example**
   - DATABASE_URL=postgresql+psycopg2://user:password@neon-host/dbname
   - SERVER_PORT=8000
   - ENVIRONMENT=development

9. **backend/Dockerfile**
   - Multi-stage build for FastAPI
   - Python 3.9+ base image

**Tests**:
- backend/tests/unit/test_schemas.py: Pydantic schema validation
- Connection pool tests

**Success Criteria**:
- FastAPI app starts without errors
- Database connection works
- Error handling configured
- Ready for endpoint implementation

---

### Phase 4: Implement REST Endpoints (API Endpoints)

**Goal**: Create all 6+ REST endpoints for CRUD, filtering, searching, sorting

**Dependencies**: Phase 3 infrastructure complete

**Deliverables**:
1. **backend/src/api/schemas/task.py**
   - TaskCreate: title, description?, priority?, tags?, due_date?
   - TaskUpdate: all fields optional
   - TaskResponse: full task with id, created_at, updated_at
   - TaskListResponse: tasks + pagination metadata

2. **backend/src/api/schemas/tag.py**
   - TagCreate: name
   - TagResponse: id, name, created_at

3. **backend/src/services/task_service.py**
   - get_all_tasks(skip, limit, filters={status, priority, tag}, search_q, sort_by, order)
   - get_task_by_id(id)
   - create_task(title, description, priority, tags, due_date)
   - update_task(id, **updates)
   - delete_task(id)
   - update_task_status(id, status)

4. **backend/src/services/tag_service.py**
   - get_all_tags()
   - get_or_create_tag(name)

5. **backend/src/api/endpoints/tasks.py**
   - GET /api/tasks (list all, with filtering, searching, sorting, pagination)
   - POST /api/tasks (create)
   - GET /api/tasks/{id} (get single)
   - PUT /api/tasks/{id} (update)
   - DELETE /api/tasks/{id} (delete)
   - PATCH /api/tasks/{id}/status (toggle status)
   - GET /api/tasks/search (search by title/description)

6. **backend/src/api/endpoints/tags.py**
   - GET /api/tags (list all)
   - POST /api/tags (create)

7. **backend/src/api/router.py**
   - Aggregate all routers
   - Register with FastAPI app

8. **contracts/openapi.json**
   - Auto-generated by FastAPI, exported as OpenAPI 3.0

**Tests**:
- backend/tests/integration/test_api_tasks.py: All task endpoints
- backend/tests/integration/test_api_tags.py: Tag endpoints
- Test filtering, searching, sorting, pagination
- Test validation errors (400, 404, 500)

**Success Criteria**:
- All 6+ endpoints implemented
- CRUD operations work end-to-end
- Filtering, searching, sorting work correctly
- Error handling returns proper status codes
- OpenAPI documentation available at /docs

---

### Phase 5: Connect Neon Database (Persistence)

**Goal**: Configure Neon Serverless Postgres connection, run migrations, verify persistence

**Dependencies**: Phase 4 endpoints complete

**Deliverables**:
1. **Neon Project Setup**
   - Create Neon project if not exist
   - Get DATABASE_URL connection string
   - Configure connection pooling settings

2. **backend/src/alembic/ (Optional - or manual SQL)**
   - Database migration scripts
   - Or: Initialize schema using database-schema.sql from Phase 1

3. **backend/src/services/db.py (Update)**
   - SQLAlchemy engine with Neon connection pooling
   - Session management with retry logic
   - Connection pool configuration (pool_size=10, max_overflow=20)

4. **.env Configuration**
   - DATABASE_URL with Neon credentials
   - Test with: python -c "from backend.src.services.db import engine; engine.connect()"

5. **Verify Schema**
   - Tables exist in Neon: tasks, tags, task_tags, audit_logs
   - Indexes created
   - Verify with: psql $DATABASE_URL -c "\dt"

**Tests**:
- backend/tests/integration/test_db_operations.py
  - Create task in Neon → retrieve → verify
  - Update task → verify changes persisted
  - Delete task → verify removal persisted

**Success Criteria**:
- API connects to Neon successfully
- CRUD operations persist data to Postgres
- Data survives server restarts
- Connection pooling works under load

---

### Phase 6: Build Next.js Frontend (UI Foundation)

**Goal**: Initialize Next.js project, set up component structure, styling, TypeScript

**Dependencies**: Parallel with Phase 5; no hard dependency

**Deliverables**:
1. **frontend/package.json**
   - Dependencies: next, react, typescript, tailwindcss, swr
   - Dev: @types/react, jest, @testing-library/react, cypress

2. **frontend/tsconfig.json**
   - TypeScript configuration for Next.js

3. **frontend/next.config.js**
   - API base URL configuration
   - Image optimization settings

4. **frontend/src/types/index.ts**
   - TypeScript interfaces: Task, Tag, Priority (High/Medium/Low), Filter, Sort

5. **frontend/src/utils/constants.ts**
   - API_BASE_URL from environment
   - PRIORITIES, SORT_OPTIONS, FILTER_OPTIONS
   - Error messages, status labels

6. **frontend/src/services/api.ts**
   - HTTP client wrapper (fetch or axios)
   - Base URL configuration
   - Request/response interceptors

7. **frontend/src/services/taskService.ts**
   - getTasks(filters, search, sort, pagination)
   - createTask(data)
   - updateTask(id, data)
   - deleteTask(id)
   - updateTaskStatus(id, status)

8. **frontend/src/pages/_app.tsx**
   - App wrapper, global state setup

9. **frontend/src/pages/_document.tsx**
   - Next.js document setup

10. **frontend/src/pages/index.tsx**
    - Dashboard page shell (placeholder for TaskList component)

11. **frontend/src/styles/globals.css**
    - Global styles with Tailwind

12. **.env.example**
    - NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

13. **frontend/Dockerfile**
    - Node.js multi-stage build

**Tests**:
- frontend/tests/unit/components/: Component stubs
- Verify TypeScript compilation

**Success Criteria**:
- Next.js app starts: npm run dev
- Dashboard page loads at http://localhost:3000
- No TypeScript errors
- Tailwind styles work
- API service callable

---

### Phase 7: Integrate API with Frontend (Connect UI to Backend)

**Goal**: Build React components, hook up to API, implement CRUD workflows

**Dependencies**: Phase 6 frontend shell + Phase 4 API complete

**Deliverables**:
1. **frontend/src/hooks/useTasks.ts**
   - SWR hook: fetch tasks from GET /api/tasks
   - Polling every 5 seconds (revalidate on focus)
   - Error, loading, data states

2. **frontend/src/hooks/useFilters.ts**
   - State: selectedStatus, selectedPriority, selectedTags
   - Filter composition for API query

3. **frontend/src/hooks/useSearch.ts**
   - State: searchQuery
   - Debounced search to API

4. **frontend/src/hooks/useSort.ts**
   - State: sortBy (due_date, priority, title), order (asc, desc)
   - Sort composition for API query

5. **frontend/src/components/TaskList.tsx**
   - Use useTasks hook
   - Display array of TaskCard components
   - Empty state message
   - Loading spinner

6. **frontend/src/components/TaskCard.tsx**
   - Display task: title, description, status, priority, tags, due_date
   - Status checkbox for toggling
   - Edit and delete buttons
   - Visual indication for completed (strikethrough, color)

7. **frontend/src/components/TaskForm.tsx**
   - Form fields: title (text), description (textarea), priority (select), tags (multi-select), due_date (date picker)
   - Submit and cancel buttons
   - Client-side validation display
   - Loading state during submit

8. **frontend/src/components/FilterBar.tsx**
   - Checkboxes for status (complete/incomplete)
   - Dropdown for priority
   - Multi-select for tags
   - Clear filters button

9. **frontend/src/components/SearchBar.tsx**
   - Text input with placeholder "Search tasks..."
   - Debounced onChange handler

10. **frontend/src/components/SortControls.tsx**
    - Dropdown for sort field (due_date, priority, title)
    - Toggle button for order (asc/desc)

11. **frontend/src/components/DeleteConfirm.tsx**
    - Modal with confirmation message
    - Confirm and cancel buttons

12. **frontend/src/components/Layout.tsx**
    - Header with app title
    - Main content area
    - Sidebar or top controls area

13. **frontend/src/pages/index.tsx (Update)**
    - Import and render Layout, TaskForm, FilterBar, SearchBar, SortControls, TaskList
    - Wire up hooks for data flow

**Tests**:
- frontend/tests/unit/components/: Unit tests for each component
- frontend/tests/integration/task-workflow.test.tsx: Cypress e2e test
  - Load dashboard
  - Create task via form
  - Verify appears in list
  - Edit task
  - Delete task
  - Verify removed

**Success Criteria**:
- Dashboard loads and displays tasks from API
- Create form submits and task appears in list
- Edit form updates task
- Delete removes task
- Filters, search, sort work correctly
- Full CRUD workflow end-to-end

---

### Phase 8: Implement Filters & Sorting (Advanced Features)

**Goal**: Build filtering and sorting logic on both backend and frontend

**Dependencies**: Phase 7 API integration complete

**Backend Implementation**:
1. **backend/src/services/task_service.py (Update)**
   - Filter logic: status filter, priority filter, tag filter
   - AND logic: if multiple filters, only return tasks matching all
   - Search logic: title ILIKE or description ILIKE
   - Sort logic: ORDER BY due_date/priority/title ASC/DESC

2. **backend/src/api/endpoints/tasks.py (Update)**
   - Query parameters: status, priority, tag, q (search), sort_by, order, limit, offset
   - Validation: enum validation for status/priority/sort_by/order
   - Compose filters and pass to service

**Frontend Implementation**:
1. **frontend/src/hooks/useTasks.ts (Update)**
   - Update query params based on filters, search, sort
   - Revalidate on filter/search/sort change

2. **frontend/src/components/FilterBar.tsx (Update)**
   - onChange handlers call setFilters
   - Compose API query params

3. **frontend/src/components/SearchBar.tsx (Update)**
   - Debounce search query
   - Update useTasks hook

4. **frontend/src/components/SortControls.tsx (Update)**
   - onChange handlers update sort state
   - Trigger API revalidation

5. **frontend/src/pages/index.tsx (Update)**
   - Wire all filter/search/sort components to hooks

**Tests**:
- backend/tests/integration/test_api_tasks.py
  - Test filtering by status
  - Test filtering by priority
  - Test filtering by tag
  - Test multiple filters (AND logic)
  - Test search (title + description)
  - Test sorting (due_date, priority, title with direction)
  - Test pagination (limit, offset)

- frontend/tests/integration/filter-sort.test.tsx
  - Filter by status → only matching tasks show
  - Filter by priority → only matching tasks show
  - Apply multiple filters → AND logic
  - Search for keyword → matching tasks show
  - Sort by due_date → correct order
  - Sort by priority → correct order

**Success Criteria**:
- Filters work correctly (AND logic for multiple)
- Search works for title and description
- Sorting works for all options with direction
- Pagination works (limit, offset)
- All filter/sort combinations composable

---

### Phase 9: Test Full Workflow (Integration & Validation)

**Goal**: Comprehensive end-to-end testing, performance validation, edge case handling

**Dependencies**: All previous phases complete

**Deliverables**:
1. **backend/tests/integration/test_full_workflow.py**
   - Create task with all fields
   - Retrieve task
   - Update task fields
   - Update task status
   - Filter by all combinations
   - Search
   - Sort
   - Delete task
   - Verify audit log entries

2. **frontend/tests/integration/task-workflow.test.tsx (Cypress)**
   - Load dashboard
   - Verify empty state or existing tasks display
   - Create task with form
   - Verify task appears in list
   - Edit task
   - Verify updates display
   - Mark task complete
   - Verify visual indication
   - Filter tasks
   - Search tasks
   - Sort tasks
   - Delete task
   - Verify removed

3. **frontend/tests/integration/error-handling.test.tsx (Cypress)**
   - API connection failure → error message displays
   - Form validation errors display
   - Network error retry works

4. **Performance Tests**
   - Dashboard load time <2s with 100+ tasks
   - API response time <200ms
   - Search <500ms

5. **Load Testing (Manual or k6)**
   - Simulate 100+ concurrent users
   - Verify no errors
   - Monitor connection pool

6. **Database Verification**
   - Data persists across server restarts
   - Audit log has entries for all operations
   - No data corruption

7. **Documentation**
   - README.md with setup instructions
   - API documentation (OpenAPI)
   - Database schema documentation

**Tests**:
- All unit tests (backend, frontend)
- All integration tests
- End-to-end workflow
- Performance validation
- Error scenarios

**Success Criteria**:
- ✅ All user stories acceptance scenarios pass
- ✅ Full CRUD workflow works end-to-end
- ✅ Data persists across browser reloads
- ✅ API + UI connected correctly
- ✅ Filters, search, sort all work
- ✅ Performance targets met (<200ms API, <2s dashboard)
- ✅ Error handling works (network errors, validation)
- ✅ 100% of acceptance criteria verified
- ✅ Zero critical issues

---

## Technical Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Browser/Client                        │
│                  (Next.js React App)                     │
│  Dashboard → Forms → Filters → Search → Sort            │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ HTTP / JSON
                       │ REST API Calls
                       ↓
┌─────────────────────────────────────────────────────────┐
│                   FastAPI Backend                        │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Endpoints Layer (API)                              │ │
│  │ ├─ GET /api/tasks (list, filter, search, sort)    │ │
│  │ ├─ POST /api/tasks (create)                       │ │
│  │ ├─ PUT /api/tasks/{id} (update)                   │ │
│  │ ├─ DELETE /api/tasks/{id} (delete)                │ │
│  │ ├─ PATCH /api/tasks/{id}/status (toggle)          │ │
│  │ └─ GET /api/tags, POST /api/tags                  │ │
│  └────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Services Layer (Business Logic)                    │ │
│  │ ├─ TaskService (CRUD, filter, search, sort)       │ │
│  │ └─ TagService (tag management)                    │ │
│  └────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Models Layer (ORM)                                 │ │
│  │ ├─ Task (SQLModel entity)                          │ │
│  │ ├─ Tag (SQLModel entity)                           │ │
│  │ └─ AuditLog (for Phase III)                        │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ SQL / Connection Pooling
                       ↓
┌─────────────────────────────────────────────────────────┐
│         Neon Serverless PostgreSQL Database             │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Tables                                             │ │
│  │ ├─ tasks (id, title, description, status, ...)    │ │
│  │ ├─ tags (id, name)                                │ │
│  │ ├─ task_tags (task_id, tag_id)                    │ │
│  │ └─ audit_logs (task_id, action, actor, ...)      │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## Implementation Dependencies & Critical Path

```
Phase 1: Database Schema Design
    ↓
Phase 2: SQLModel Entities
    ↓
Phase 3: FastAPI Infrastructure
    ↓
Phase 4: REST Endpoints ──────────┐
    ↓                             │
Phase 5: Neon Connection          │ (Parallel)
    ↓                             │
Phase 6: Next.js Frontend ────────┘
    ↓
Phase 7: API Integration
    ↓
Phase 8: Filters & Sorting
    ↓
Phase 9: Full Workflow Testing
    ↓
    ✅ PRODUCTION READY
```

**Critical Path**: Phases 1→2→3→4→5 (backend) and 6 (frontend parallel) then 7→8→9

**Parallelization**: Phase 6 can start after Phase 4 API is ready (not blocking on Phase 5)

---

## TDD Approach (Red-Green-Refactor Cycle)

For each phase:

1. **RED**: Write tests (they fail, no implementation yet)
2. **GREEN**: Implement just enough to make tests pass
3. **REFACTOR**: Clean up code, optimize, improve

Example (Phase 4):
- RED: Write test for GET /api/tasks (will fail)
- GREEN: Implement endpoint that retrieves all tasks (minimal)
- REFACTOR: Add filtering, searching, sorting support

---

## Success Metrics (Definition of Done)

**Phase Complete When**:
- ✅ All acceptance scenarios for that phase pass
- ✅ Tests written and passing (unit + integration)
- ✅ Code reviewed and merged to branch
- ✅ Performance targets met (if applicable)
- ✅ No critical issues

**Project Complete When**:
- ✅ All 9 phases complete
- ✅ All 10 user stories fully implemented
- ✅ All 35+ functional requirements met
- ✅ All 17+ non-functional requirements met
- ✅ Full CRUD workflow working end-to-end
- ✅ Data persists reliably
- ✅ API + UI connected correctly
- ✅ Filters, search, sort all working
- ✅ Performance targets met
- ✅ Error handling working
- ✅ 100% test coverage (unit, integration, e2e)
- ✅ Zero critical bugs

---

## Timeline & Effort Estimation

| Phase | Tasks | Est. Hours | Cumulative |
|-------|-------|-----------|------------|
| 1. Schema Design | 1-2 | 3-4 | 3-4 |
| 2. SQLModel | 4-5 | 4-5 | 7-9 |
| 3. FastAPI Setup | 5-6 | 5-6 | 12-15 |
| 4. Endpoints | 6+ | 8-10 | 20-25 |
| 5. Neon Connection | 2-3 | 3-4 | 23-29 |
| 6. Next.js Setup | 6+ | 4-5 | 27-34 |
| 7. API Integration | 7-8 | 12-15 | 39-49 |
| 8. Filters & Sorting | 5-7 | 6-8 | 45-57 |
| 9. Full Testing | 3-5 | 10-15 | 55-72 |
| **Total** | **39-41** | **55-72** | **55-72** |

**Notes**:
- Estimates are for 1 developer with intermediate full-stack experience
- Assumes TDD approach (tests before implementation)
- Includes code review and refactoring
- Does NOT include styling perfection (functional is goal)

---

## Deployment Strategy

**Development**:
- Local: docker-compose up (PostgreSQL + FastAPI + Next.js)
- Testing: pytest (backend), Jest + Cypress (frontend)

**Staging** (optional):
- Backend: Docker image pushed to registry (AWS ECR, Docker Hub, etc.)
- Frontend: Deployed to Vercel or similar
- Database: Neon staging instance

**Production**:
- Backend: Serverless (AWS Lambda, Google Cloud Run, Fly.io) OR ECS
- Frontend: Vercel, Netlify, or static S3
- Database: Neon production instance (auto-managed)

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Database connection pool exhaustion | Neon handles; monitor pool metrics |
| Performance degradation with 100+ tasks | Index strategy; pagination; query optimization |
| API-Frontend integration issues | Contract-first: define API before implementation |
| Data loss | Neon backups (managed); audit log |
| Validation edge cases | Comprehensive test coverage |
| Network errors | Error handling + retry logic |

---

## Next Steps

1. **Generate Tasks** (`/sp.tasks 002-web-app`)
   - Creates 108+ actionable implementation tasks
   - One per function/component/test

2. **Begin Implementation** (`/sp.implement`)
   - Execute tasks in dependency order
   - TDD cycle: tests → implementation → refactor
   - Mark tasks complete as you go

3. **Monitor Progress**
   - Track completed tasks
   - Watch for blockers
   - Validate against acceptance criteria

---

## Conclusion

This implementation plan provides a clear, actionable roadmap for building a production-ready full-stack web application with 9 concrete phases, each with specific deliverables and success criteria. The plan prioritizes:

- **Clean Architecture**: 3-layer (Model → Service → API) + React UI
- **TDD Approach**: Tests before implementation for reliability
- **Scalability**: Database design ready for Phase III AI
- **Professional Quality**: Full test coverage, error handling, performance optimization

**Status**: ✅ **READY FOR TASK GENERATION & IMPLEMENTATION**

---

*Generated: 2025-12-29 | Phase II – Full-Stack Web Todo Application | 9-Phase Implementation Plan*
