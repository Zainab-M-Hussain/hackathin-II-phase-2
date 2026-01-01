# Feature Specification: Phase II – Full-Stack Web Todo Application (Implementation-Ready)

**Feature Branch**: `002-web-app`
**Created**: 2025-12-29
**Status**: Implementation-Ready (Detailed Spec)
**Scope**: Build production-ready full-stack web application with persistent storage and AI-agent readiness

## Context & Goals

**Primary Objectives**:
- Build real production-ready web application with persistent PostgreSQL storage
- Clean REST API design for future AI agent control (Phase III)
- Professional, functional UI (Bootstrap/Tailwind, styling acceptable)
- Reusable 3-layer architecture (Model → Service → API)

**Non-Goals**:
- User authentication or multi-user support (single session assumed)
- Styling perfection (functional > beautiful)
- Real-time sync via WebSocket (polling acceptable)

---

## User Scenarios & Testing

### User Story 1 – View All Tasks (Priority: P1)

**Narrative**: As a user, I can view all my tasks in a clean dashboard, seeing their title, description, status, priority, tags, due date, and when created.

**Why P1**: Core functionality; users must see tasks before acting on them.

**Independent Test**: Load dashboard → verify 5+ tasks display with all fields → navigate away and return → data persists

**Acceptance Scenarios**:

1. **Given** 5 tasks exist in database, **When** user loads dashboard, **Then** all 5 appear with title, description, status, priority, tags, due_date, created_at
2. **Given** no tasks exist, **When** user loads dashboard, **Then** empty state message displays
3. **Given** tasks in database, **When** user navigates away and returns, **Then** same tasks appear (data persisted)
4. **Given** 1000+ tasks in database, **When** dashboard loads, **Then** displays in <2 seconds (p95 latency)
5. **Given** multiple tasks with different statuses, **When** viewing list, **Then** status displays clearly (e.g., badge, color, icon)

---

### User Story 2 – Add a New Task (Priority: P1)

**Narrative**: As a user, I can create a new task with title (required), description (optional), priority, tags, and due date.

**Why P1**: Essential CRUD; users cannot use system without creating tasks.

**Independent Test**: Fill form → submit → verify task appears in list → create rapid succession → all persist

**Acceptance Scenarios**:

1. **Given** form with title required field, **When** user enters "Buy groceries" and submits, **Then** task created with auto-incremented ID and appears in list
2. **Given** empty title field, **When** user tries to submit, **Then** validation error displays (max 500 chars, non-empty)
3. **Given** form with optional fields, **When** user fills title only, **Then** task created with defaults (priority=Medium, due_date=null, tags=empty)
4. **Given** form with priority dropdown, **When** user selects "High", **Then** task created with priority=High
5. **Given** tags input field, **When** user enters "work, urgent", **Then** task associated with both tags
6. **Given** due date picker, **When** user selects tomorrow's date, **Then** task.due_date set correctly

---

### User Story 3 – Mark Task Complete/Incomplete (Priority: P1)

**Narrative**: As a user, I can toggle a task's status between incomplete and complete with visual indication.

**Why P1**: Task completion is primary value delivery; core user interaction.

**Independent Test**: Create task → mark complete → verify status changes visually → toggle back → verify reverts

**Acceptance Scenarios**:

1. **Given** incomplete task in list, **When** user clicks status checkbox, **Then** task marked complete, status updates immediately, visual indication appears (strikethrough or color change)
2. **Given** completed task, **When** user clicks checkbox again, **Then** reverts to incomplete, visual indication removed
3. **Given** multiple tasks with mixed statuses, **When** toggling each individually, **Then** each updates independently without affecting others
4. **Given** task toggled to complete, **When** user navigates away and returns, **Then** status persists as complete
5. **Given** database has task in pending state, **When** API receives PATCH complete request, **Then** status updates in database and subsequent GET returns new status

---

### User Story 4 – Filter Tasks (Priority: P2)

**Narrative**: As a user, I can filter tasks by status (complete/incomplete), priority (High/Medium/Low), and tag to narrow results.

**Why P2**: Organizational feature; valuable but not blocking MVP.

**Independent Test**: Apply single filter → verify matching tasks show → apply multiple filters → verify AND logic

**Acceptance Scenarios**:

1. **Given** 10 tasks with mixed statuses, **When** user filters by status=incomplete, **Then** only incomplete tasks display
2. **Given** 10 tasks with mixed priorities, **When** user filters by priority=High, **Then** only high-priority tasks display
3. **Given** 10 tasks with mixed tags, **When** user filters by tag=work, **Then** only work-tagged tasks display
4. **Given** multiple filters applied, **When** user selects status=incomplete AND priority=High, **Then** only tasks matching ALL criteria display (AND logic)
5. **Given** active filters, **When** user clicks clear/reset, **Then** all tasks display again
6. **Given** filters applied, **When** new matching task created, **Then** appears in list immediately; new non-matching task does not appear

---

### User Story 5 – Search Tasks (Priority: P2)

**Narrative**: As a user, I can search tasks by title and description text to find specific tasks quickly.

**Why P2**: Convenience feature for finding tasks; less critical than CRUD.

**Independent Test**: Type search term → verify matching tasks display → clear search → all tasks reappear

**Acceptance Scenarios**:

1. **Given** 20 tasks with various titles, **When** user searches "grocery", **Then** all tasks containing "grocery" in title or description appear
2. **Given** no tasks matching search term, **When** user searches "xyzabc", **Then** empty state message displays
3. **Given** 50+ tasks, **When** user searches, **Then** results display in <500ms (acceptable latency)
4. **Given** active search, **When** user clears search box, **Then** all tasks display again
5. **Given** search results, **When** user creates new matching task, **Then** task appears in search results immediately
6. **Given** search results, **When** user filters by priority=High, **Then** search results AND priority filter applied (composable)

---

### User Story 6 – Sort Tasks (Priority: P2)

**Narrative**: As a user, I can sort tasks by due date (ascending/descending), priority (High to Low), or title alphabetically.

**Why P2**: Organizational feature; useful for specific workflows.

**Independent Test**: Select sort option → verify order changes → select different sort → order changes correctly

**Acceptance Scenarios**:

1. **Given** tasks with various due dates, **When** user sorts by due_date ascending, **Then** earliest due date appears first
2. **Given** tasks with mixed priorities, **When** user sorts by priority descending, **Then** High priority tasks appear first
3. **Given** tasks with varied titles, **When** user sorts alphabetically, **Then** tasks appear A-Z by title
4. **Given** active sort, **When** user creates new task, **Then** new task appears in correct sorted position
5. **Given** sort applied, **When** user changes sort, **Then** order updates immediately without reloading

---

### User Story 7 – Edit Task (Priority: P2)

**Narrative**: As a user, I can edit a task's title, description, priority, tags, or due date after creation.

**Why P2**: Enables task refinement; necessary for practical use.

**Independent Test**: Create task → open edit form → change field → save → verify changes persist

**Acceptance Scenarios**:

1. **Given** existing task, **When** user clicks edit and changes title, **Then** updated title persists and displays in list
2. **Given** task with description, **When** user clears description field and saves, **Then** description removed
3. **Given** task with priority=Low, **When** user changes to priority=High and saves, **Then** priority updates in database and list
4. **Given** edit form open, **When** user attempts to save with empty title, **Then** validation error displays
5. **Given** multiple users viewing same task (hypothetical Phase IV), **When** one user edits, **Then** other users see update on refresh

---

### User Story 8 – Delete Task (Priority: P2)

**Narrative**: As a user, I can delete a task after confirming, removing it from the list.

**Why P2**: Cleanup capability; necessary for task list maintenance.

**Independent Test**: Create task → delete with confirmation → verify removed from list

**Acceptance Scenarios**:

1. **Given** task in list, **When** user clicks delete, **Then** confirmation dialog appears
2. **Given** confirmation dialog, **When** user confirms, **Then** task removed from list immediately
3. **Given** confirmation dialog, **When** user cancels, **Then** task remains in list
4. **Given** deleted task, **When** user navigates away and returns, **Then** task does not reappear (deletion persisted)
5. **Given** multiple tasks, **When** user deletes one, **Then** others unaffected

---

### User Story 9 – Create/Edit Forms (Priority: P2)

**Narrative**: As a user, I can use clean, intuitive forms to create and edit tasks with all fields (title, description, priority, tags, due date) and clear submit/cancel buttons.

**Why P2**: UX requirement; forms are primary interaction for task creation.

**Independent Test**: Fill form → verify all fields work → submit → verify in list

**Acceptance Scenarios**:

1. **Given** create form, **When** user fills title="Test" and submits, **Then** task created with default values for optional fields
2. **Given** edit form with existing task data, **When** form loads, **Then** all fields pre-populated with current values
3. **Given** form with required field empty, **When** user tries submit, **Then** clear validation message displays identifying required field
4. **Given** form open, **When** user clicks cancel, **Then** form closes without creating/modifying task
5. **Given** form with character limits, **When** user enters text exceeding limits, **Then** truncated or error message displayed

---

### User Story 10 – Data Persistence & Refresh (Priority: P1)

**Narrative**: As a user, I can reload the page or close/reopen browser, and all tasks remain in database with same data, status, and properties.

**Why P1**: Essential; users expect data to persist.

**Independent Test**: Create tasks → close browser → reopen → verify all tasks present with correct data

**Acceptance Scenarios**:

1. **Given** 10 tasks created and visible, **When** user presses F5 to reload page, **Then** all 10 tasks display exactly as before
2. **Given** tasks in database, **When** user closes browser and reopens, **Then** same tasks appear
3. **Given** task marked as complete, **When** page reloaded, **Then** task still marked complete with visual indication
4. **Given** filters or sort applied, **When** page reloaded, **Then** new tasks match filters (not saved state, fresh query)
5. **Given** new task created, **When** another browser window with app open, **Then** new task visible on their refresh (within 5-10s polling interval)

---

### Edge Cases

- **Concurrent edits**: User A edits task title while User B views (Phase IV consideration); resolved with last-write-wins + audit log
- **Bulk operations**: Deleting 100+ tasks rapidly; system handles gracefully with progress indication
- **Invalid due dates**: Past due dates; system accepts but may warn in UI (optional)
- **Empty tags**: Task created without tags; system allows (tags optional)
- **Long text fields**: Title/description at 500 char limit; system truncates in list view, shows full in detail
- **Network errors**: API call fails; client shows error message and prompts retry
- **Database connection loss**: Neon connection pool reconnects automatically; user sees temporary error, recovers

---

## Requirements

### Functional Requirements

**Backend (FastAPI)**:

- **FR-001**: System MUST provide REST endpoint GET /api/tasks to retrieve all tasks with optional pagination
- **FR-002**: System MUST provide REST endpoint POST /api/tasks to create new task with title (required), description, priority, tags, due_date (optional)
- **FR-003**: System MUST provide REST endpoint GET /api/tasks/{id} to retrieve single task by ID
- **FR-004**: System MUST provide REST endpoint PUT /api/tasks/{id} to update task title, description, priority, tags, due_date
- **FR-005**: System MUST provide REST endpoint DELETE /api/tasks/{id} to delete task
- **FR-006**: System MUST provide REST endpoint PATCH /api/tasks/{id}/status to toggle task status (incomplete ↔ complete)
- **FR-007**: System MUST support filtering by status (complete/incomplete), priority (High/Medium/Low), tag via query parameters
- **FR-008**: System MUST support searching by title and description via query parameter (text matching)
- **FR-009**: System MUST support sorting by due_date, priority, title via query parameters with ascending/descending order
- **FR-010**: System MUST validate task title (required, non-empty, max 500 characters)
- **FR-011**: System MUST validate task description (optional, max 500 characters)
- **FR-012**: System MUST validate due_date if provided (valid date format, optional)
- **FR-013**: System MUST persist all task data to PostgreSQL (via Neon) with ACID properties
- **FR-014**: System MUST return appropriate HTTP status codes (201 Created, 200 OK, 404 Not Found, 400 Bad Request, 500 Error)
- **FR-015**: System MUST implement async endpoints using FastAPI async/await for high concurrency

**Frontend (Next.js)**:

- **FR-016**: Frontend MUST display task dashboard showing all tasks with columns for title, description, status, priority, tags, due_date, created_at
- **FR-017**: Frontend MUST provide create task form with fields: title (required), description (optional), priority (dropdown), tags (multi-select), due_date (date picker)
- **FR-018**: Frontend MUST provide edit task form with same fields pre-populated for existing task
- **FR-019**: Frontend MUST provide delete confirmation dialog before deleting task
- **FR-020**: Frontend MUST provide filter UI with checkboxes/dropdowns for status, priority, tag filtering
- **FR-021**: Frontend MUST provide search input field for text search by title/description
- **FR-022**: Frontend MUST provide sort selector with options: due_date (asc/desc), priority (high→low), title (A→Z)
- **FR-023**: Frontend MUST display task status visually (badge, color, strikethrough for completed)
- **FR-024**: Frontend MUST refresh task list automatically after create/edit/delete operations
- **FR-025**: Frontend MUST display loading state while fetching tasks from API
- **FR-026**: Frontend MUST display error messages when API calls fail

**Data Model**:

- **FR-027**: Task entity MUST have fields: id (int, auto-increment), title (str, max 500), description (str, max 500, optional)
- **FR-028**: Task entity MUST have fields: status (enum: pending/complete), priority (enum: Low/Medium/High, default Medium)
- **FR-029**: Task entity MUST have fields: tags (many-to-many relationship with Tag entity), created_at (datetime, auto)
- **FR-030**: Task entity MUST have fields: due_date (datetime, optional), updated_at (datetime, auto-update)
- **FR-031**: Tag entity MUST have fields: id (int, auto-increment), name (str, max 50, unique), created_at (datetime)
- **FR-032**: Task-Tag relationship MUST be many-to-many with junction table for flexible tag association

**Integration**:

- **FR-033**: API MUST be accessible from frontend at configured base URL (via environment variable)
- **FR-034**: API responses MUST be JSON format with consistent structure
- **FR-035**: API MUST handle CORS requests from frontend domain

### Non-Functional Requirements

**Performance**:
- **NFR-001**: API endpoints MUST respond in <200ms (p95) for typical queries
- **NFR-002**: Dashboard MUST load and display 100+ tasks in <2 seconds (p95)
- **NFR-003**: Search/filter queries MUST complete in <500ms for datasets up to 5000 tasks
- **NFR-004**: Database queries MUST use indexes for common filter/sort operations

**Scalability**:
- **NFR-005**: System MUST handle 100+ concurrent users without performance degradation
- **NFR-006**: Database connection pooling MUST manage concurrent connections efficiently
- **NFR-007**: API MUST be horizontally scalable (stateless design)

**Reliability**:
- **NFR-008**: Data MUST persist reliably; zero data loss during normal operations
- **NFR-009**: Database connections MUST auto-reconnect on transient failures (Neon handles)
- **NFR-010**: API MUST handle and report errors gracefully with meaningful messages

**Security**:
- **NFR-011**: API endpoints MUST validate and sanitize all input (prevent SQL injection, XSS)
- **NFR-012**: Queries MUST use parameterized statements (SQLModel/Pydantic provide this)
- **NFR-013**: HTTPS MUST be enforced in production
- **NFR-014**: Sensitive configuration (DATABASE_URL) MUST be environment-based, never in code

**Maintainability**:
- **NFR-015**: Code MUST be organized in 3-layer architecture (Model → Service → API)
- **NFR-016**: API MUST be auto-documented with OpenAPI/Swagger
- **NFR-017**: Database migrations MUST be version-controlled

---

## Key Entities

**Task**:
- Represents a todo item with title, description, status, priority, tags, dates
- Status: pending (incomplete) or complete
- Priority: Low, Medium (default), High
- Due date: optional future or past date
- Tags: many-to-many association with Tag entity

**Tag**:
- Represents a category/label for organizing tasks
- Name: unique, max 50 characters
- Associated with zero or more tasks

**Audit Log** (for Phase III AI readiness):
- Tracks all task changes with actor, timestamp, previous/new state
- Enables AI learning and human auditing

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: All CRUD operations work end-to-end: create task → list shows it → edit it → changes persist → delete removes it
- **SC-002**: Data persists across browser reloads: create 10 tasks → reload page → all 10 still present
- **SC-003**: API fully connected to UI: UI forms submit to API → API updates database → list updates via API GET
- **SC-004**: Filtering works correctly: apply filter → results match criteria AND logic for multiple filters
- **SC-005**: Search works correctly: type "grocery" → only tasks with "grocery" in title/description appear
- **SC-006**: Sorting works correctly: sort by due_date → earliest/latest date first depending on selection
- **SC-007**: Performance targets met: API <200ms, dashboard <2s, search <500ms
- **SC-008**: Form validation works: empty title rejected, long text handled, optional fields work
- **SC-009**: UI updates immediately: create task → appears in list without page reload
- **SC-010**: Database persists reliably: no data loss, audit trail complete

---

## Constraints & Assumptions

**Technical Constraints**:
- Backend: FastAPI with Python 3.9+
- Frontend: Next.js 18+ with React 18+, TypeScript
- Database: Neon Serverless Postgres via SQLModel ORM
- API: REST JSON endpoints
- No user authentication (single session)

**Data Constraints**:
- Task title: required, max 500 characters
- Task description: optional, max 500 characters
- Due date: optional, future or past dates allowed
- Tags: optional, max 10 per task, max 50 chars per name
- Priorities: High, Medium (default), Low (fixed set)

**Operational Assumptions**:
- Single user per session (no authentication, no multi-user sync)
- Always-connected internet (polling-based sync, not offline-first)
- Database always available (Neon managed)
- Polling every 5-10 seconds for multi-window sync

---

## Implementation-Ready Technical Specifications

### Backend Structure

```
backend/
├── src/
│   ├── main.py                 # FastAPI app initialization
│   ├── models/
│   │   ├── task.py            # SQLModel Task entity
│   │   ├── tag.py             # SQLModel Tag entity
│   │   ├── audit_log.py       # Audit logging for Phase III
│   │   └── __init__.py
│   ├── services/
│   │   ├── task_service.py    # Task business logic
│   │   ├── tag_service.py     # Tag management
│   │   ├── db.py              # Database session management
│   │   └── __init__.py
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── tasks.py       # Task CRUD endpoints
│   │   │   ├── tags.py        # Tag endpoints
│   │   │   └── __init__.py
│   │   ├── schemas/
│   │   │   ├── task.py        # Pydantic schemas for Task
│   │   │   ├── tag.py         # Pydantic schemas for Tag
│   │   │   └── __init__.py
│   │   ├── dependencies.py    # Dependency injection
│   │   ├── router.py          # Route aggregation
│   │   └── __init__.py
│   ├── core/
│   │   ├── config.py          # Configuration
│   │   ├── errors.py          # Error handling
│   │   └── __init__.py
│   └── __init__.py
├── tests/
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_schemas.py
│   ├── integration/
│   │   ├── test_api_tasks.py
│   │   └── test_db_ops.py
│   └── conftest.py
├── requirements.txt
└── Dockerfile
```

### Frontend Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── TaskList.tsx       # Main task list component
│   │   ├── TaskCard.tsx       # Individual task display
│   │   ├── TaskForm.tsx       # Create/edit form
│   │   ├── FilterBar.tsx      # Filter UI
│   │   ├── SearchBar.tsx      # Search input
│   │   ├── SortControls.tsx   # Sort selector
│   │   └── DeleteConfirm.tsx  # Delete confirmation modal
│   ├── pages/
│   │   ├── index.tsx          # Dashboard
│   │   ├── _app.tsx           # App wrapper
│   │   └── _document.tsx      # Document wrapper
│   ├── services/
│   │   ├── api.ts             # API client
│   │   └── taskService.ts     # Task-specific API calls
│   ├── hooks/
│   │   ├── useTasks.ts        # Fetch and manage tasks
│   │   ├── useFilters.ts      # Filter state management
│   │   └── useSearch.ts       # Search state management
│   ├── types/
│   │   ├── index.ts           # TypeScript interfaces
│   │   ├── task.ts            # Task type definitions
│   │   └── api.ts             # API types
│   ├── styles/
│   │   ├── globals.css        # Global styles
│   │   └── components.css     # Component-specific styles
│   └── utils/
│       ├── constants.ts       # Constants and enums
│       └── validators.ts      # Client-side validation
├── tests/
│   ├── unit/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── services/
│   └── integration/
│       └── task-workflow.test.tsx  # Cypress tests
├── package.json
├── tsconfig.json
└── Dockerfile
```

### API Endpoints (Detailed)

**List Tasks**:
```
GET /api/tasks?status=complete&priority=High&tag=work&sort_by=due_date&order=asc&limit=50&offset=0
Response: { tasks: [Task], total: int, limit: int, offset: int }
```

**Create Task**:
```
POST /api/tasks
Body: { title: string, description?: string, priority?: "Low"|"Medium"|"High", tags?: [string], due_date?: date }
Response: 201 Created, { id: int, ...full task }
```

**Update Task**:
```
PUT /api/tasks/{id}
Body: { title?: string, description?: string, priority?: string, tags?: [string], due_date?: date }
Response: 200 OK, { ...updated task }
```

**Delete Task**:
```
DELETE /api/tasks/{id}
Response: 204 No Content
```

**Toggle Status**:
```
PATCH /api/tasks/{id}/status
Body: { status: "pending" | "complete" }
Response: 200 OK, { ...task with new status }
```

**Search**:
```
GET /api/tasks/search?q=grocery&limit=50
Response: { tasks: [Task], total: int }
```

---

## Clarifications Resolved

- ✅ **Data Model**: Hybrid normalized (tags, audit_log) + denormalized (priority) for balance
- ✅ **AI Readiness**: Query-based API + audit logging for Phase III agent control
- ✅ **Real-time Sync**: Polling every 5-10 seconds (SWR hook) - sufficient for MVP
- ✅ **State Management**: Soft enforcement (allow transitions, track in audit_log)
- ✅ **Field Definitions**: title, description, status (pending/complete), priority, tags, due_date, created_at

---

## Next Steps

1. **Run `/sp.plan`** to finalize architecture and design
2. **Run `/sp.tasks`** to generate implementation task list
3. **Run `/sp.implement`** to begin development using TDD (RED → GREEN → REFACTOR)

**Status**: ✅ IMPLEMENTATION-READY SPECIFICATION COMPLETE
