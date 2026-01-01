# PHASE II TODO APPLICATION - COMPREHENSIVE ARCHITECTURAL DESIGN

## Executive Summary

This document provides a detailed architectural design for Phase II of the Todo Application - a full-stack web platform combining FastAPI backend, PostgreSQL persistence, and Next.js frontend with SWR polling. The design balances simplicity, extensibility (for Phase III AI integration), and production-readiness.

**Key Characteristics**:
- 3-layer architecture (Models → Services → APIs) across both backend and frontend
- SQLModel entities with Pydantic validation providing type safety
- RESTful API with comprehensive filtering, sorting, and searching
- Audit logging foundation for Phase III AI learning
- TDD approach with clear test boundaries
- Multi-tab synchronization via 5-10 second polling intervals

---

## 1. ARCHITECTURE OVERVIEW

### 1.1 System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CLIENT LAYER (Browser)                             │
│  Next.js Application (React 18+ / TypeScript 5+)                           │
│  ├── Pages: /index, /tasks, /[taskId]                                     │
│  ├── Components: TaskList, TaskCard, TaskForm, FilterBar                   │
│  ├── Services: api.ts (HTTP client wrapper)                               │
│  ├── Hooks: useTasks (SWR with polling), useFilters, useSearch            │
│  └── State: React hooks + SWR caching                                      │
└─────────────────────────────┬───────────────────────────────────────────────┘
                              │ HTTPS/REST JSON
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│              FASTAPI BACKEND (3-Layer Architecture)                         │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  API LAYER (Endpoints)                                               │  │
│  │  ├── /api/tasks: CRUD + filtering/sorting/searching                │  │
│  │  ├── /api/tags: Tag management                                      │  │
│  │  └── Health checks                                                   │  │
│  ├─ Validation: Pydantic automatic                                      │  │
│  ├─ Error Handling: Custom exceptions → HTTP codes                     │  │
│  └─ DI: get_db (Session)                                               │  │
│                                                                        │  │
│  ┌──────────────────────────────────────────────────────────────────┐ │  │
│  │  SERVICE LAYER (Business Logic)                                 │ │  │
│  │  ├── TaskService: CRUD, list, filtering, audit                 │ │  │
│  │  └── TagService: tag operations                                │ │  │
│  └──────────────────────────────────────────────────────────────────┘ │  │
│                                                                        │  │
│  ┌──────────────────────────────────────────────────────────────────┐ │  │
│  │  DATA LAYER (SQLModel + Pydantic)                               │ │  │
│  │  ├── Task: Entity + schemas (Read/Create/Update)              │ │  │
│  │  ├── Tag: Entity + schemas                                    │ │  │
│  │  ├── AuditLog: Immutable history (Phase III prep)             │ │  │
│  │  └── Validation: Field validators                             │ │  │
│  └──────────────────────────────────────────────────────────────────┘ │  │
└─────────────────────────────┬───────────────────────────────────────────────┘
                              │ SQLAlchemy ORM + psycopg2
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  DATABASE LAYER                                                             │
│  ├── Connection Pool: 20 persistent + 10 overflow                         │
│  ├── Session Factory: Per-request isolation                               │
│  ├── Schema: 4 tables (tasks, tags, task_tags, audit_logs)               │
│  └── Indexes: Status, priority, due_date, created_at                     │
└─────────────────────────────┬───────────────────────────────────────────────┘
                              │
                              ▼
                    NEON SERVERLESS POSTGRESQL
```

### 1.2 Key Design Patterns

**MVC on Backend**:
- **Models**: SQLModel entities (Task, Tag, AuditLog)
- **Services**: Business logic (TaskService, TagService)
- **Controllers**: FastAPI endpoints (routes.py)

**Reactive on Frontend**:
- **Components**: React (TaskList, TaskCard, TaskForm)
- **Hooks**: Custom hooks with SWR for data (useTasks)
- **Services**: API client wrapper (api.ts)
- **State**: React local state + SWR cache

**Multi-Tab Sync**:
- SWR polling every 5-10 seconds
- Immediate revalidation on mutations
- Focus-aware revalidation

---

## 2. BACKEND ARCHITECTURE

### 2.1 File Structure

```
backend/
├── src/
│   ├── main.py                          # FastAPI app
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py                      # BaseModel + TimestampMixin
│   │   ├── task.py                      # Task + schemas
│   │   ├── tag.py                       # Tag + schemas
│   │   ├── task_tag.py                  # Many-to-many junction
│   │   └── audit_log.py                 # AuditLog + AuditAction
│   ├── services/
│   │   ├── __init__.py
│   │   ├── db.py                        # Connection pool, sessions
│   │   ├── task_service.py              # TaskService
│   │   └── tag_service.py               # TagService
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py              # get_db() DI
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       ├── tasks.py                 # Task endpoints
│   │       ├── tags.py                  # Tag endpoints
│   │       └── audit.py                 # Audit (Phase III)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                    # Settings
│   │   └── errors.py                    # Custom exceptions
│   └── __init__.py
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_schemas.py
│   └── integration/
│       ├── test_api_tasks.py
│       ├── test_api_tags.py
│       └── test_full_workflow.py
├── requirements.txt
├── .env.example
├── Dockerfile
└── main.py (entry point)
```

### 2.2 Service Layer

**TaskService**:
```python
class TaskService:
    def __init__(self, session: Session): ...

    # CRUD
    def get_task(task_id: int) -> Task
    def create_task(title, description, priority, due_date, tag_ids) -> Task
    def update_task(task_id, ...) -> Task
    def delete_task(task_id) -> None

    # Status Management
    def update_task_status(task_id, status, reason) -> Task

    # Querying
    def list_tasks(skip, limit, status, priority, tag_ids, search, sort_by, sort_order) -> tuple[List[Task], int]

    # Audit & Analytics
    def get_task_audit_history(task_id) -> List[AuditLog]
    def get_statistics() -> dict
```

**Key Features**:
- Session-based (dependency injection)
- Comprehensive filtering/sorting/searching
- Audit trail creation (via database triggers)
- Custom exception raising

---

## 3. FRONTEND ARCHITECTURE

### 3.1 File Structure

```
frontend/
├── src/
│   ├── pages/
│   │   ├── _app.tsx
│   │   ├── _document.tsx
│   │   ├── index.tsx                    # Dashboard
│   │   ├── [taskId].tsx                 # Details page
│   │   └── 404.tsx
│   ├── components/
│   │   ├── TaskList.tsx
│   │   ├── TaskCard.tsx
│   │   ├── TaskForm.tsx
│   │   ├── FilterBar.tsx
│   │   ├── SearchBox.tsx
│   │   ├── SortControls.tsx
│   │   ├── Pagination.tsx
│   │   ├── LoadingSpinner.tsx
│   │   ├── EmptyState.tsx
│   │   └── ErrorBoundary.tsx
│   ├── services/
│   │   ├── api.ts                       # HTTP client
│   │   ├── taskApi.ts                   # Task methods
│   │   └── tagApi.ts                    # Tag methods
│   ├── hooks/
│   │   ├── useTasks.ts                  # SWR with polling
│   │   ├── useTask.ts                   # Single task
│   │   ├── useFilters.ts                # Filter state
│   │   ├── useSearch.ts                 # Search state
│   │   └── useMutations.ts              # Create/Update/Delete
│   ├── types/
│   │   ├── task.ts
│   │   ├── api.ts
│   │   └── index.ts
│   ├── styles/
│   │   ├── globals.css
│   │   └── components.css
│   └── utils/
│       ├── formatters.ts
│       ├── validators.ts
│       └── constants.ts
├── __tests__/
│   ├── components/
│   ├── hooks/
│   ├── services/
│   └── utils/
├── .env.example
├── jest.config.js
├── next.config.js
├── tsconfig.json
└── package.json
```

### 3.2 SWR Polling Hook

```typescript
export function useTasks({
  skip = 0,
  limit = 50,
  status,
  priority,
  tags,
  search,
  sort_by = 'created_at',
  sort_order = 'desc',
  pollingInterval = 5000,  // 5 second default
}: UseTasksOptions = {}) {
  const queryString = new URLSearchParams(params).toString();
  const url = `/tasks?${queryString}`;

  const { data, error, isLoading, isValidating, mutate } = useSWR<TaskListResponse>(
    url,
    () => taskApi.list(params),
    {
      revalidateOnFocus: true,      // Multi-tab sync
      revalidateOnReconnect: true,
      dedupingInterval: 2000,
      focusThrottleInterval: 5000,
      refreshInterval: pollingInterval,
      errorRetryCount: 3,
    }
  );

  return {
    tasks: data?.items || [],
    total: data?.total || 0,
    isLoading,
    isValidating,
    error,
    mutate,
  };
}
```

**Multi-Tab Sync Flow**:
1. Tab A creates task → `mutate()` → immediate revalidation
2. Tab B polls every 5s → receives updated list
3. Both tabs show same data within 5-10 seconds

---

## 4. API CONTRACT

### 4.1 Endpoints Overview

```
GET    /api/tasks                    # List (with filters/sort/search)
POST   /api/tasks                    # Create
GET    /api/tasks/{id}               # Get single
PUT    /api/tasks/{id}               # Update
PATCH  /api/tasks/{id}/status        # Change status
DELETE /api/tasks/{id}               # Delete
GET    /api/tasks/stats/summary      # Statistics

GET    /api/tags                     # List tags
POST   /api/tags                     # Create tag
DELETE /api/tags/{id}                # Delete tag

GET    /                             # Status
GET    /health                       # Health check
```

### 4.2 Query Parameters

```
GET /api/tasks?skip=0&limit=50&status=pending&priority=HIGH&sort_by=due_date&sort_order=asc
```

**Query Parameters**:
| Param | Type | Default | Example |
|-------|------|---------|---------|
| skip | int | 0 | 0 |
| limit | int | 50 | 50 |
| status | string | null | pending/complete/archived |
| priority | string | null | LOW/MEDIUM/HIGH |
| tags | string | null | 1,2,3 (AND logic) |
| search | string | null | groceries |
| sort_by | string | created_at | due_date/priority/title |
| sort_order | string | desc | asc/desc |

### 4.3 Response Format

**Success (List)**:
```json
{
  "items": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "priority": "MEDIUM",
      "status": "pending",
      "due_date": "2025-12-31T23:59:59Z",
      "created_at": "2025-12-29T10:00:00Z",
      "updated_at": "2025-12-29T10:00:00Z",
      "tags": [
        { "id": 1, "name": "shopping" }
      ]
    }
  ],
  "total": 42,
  "skip": 0,
  "limit": 50
}
```

**Error (404)**:
```json
{
  "error_code": "E001",
  "error_type": "TaskNotFoundError",
  "detail": "Task with ID 999 not found",
  "timestamp": "2025-12-29T10:00:00Z",
  "path": "/api/tasks/999"
}
```

---

## 5. TESTING STRATEGY

### 5.1 Test Pyramid

```
        /\
       /  \  E2E (10-15%)
      /    \
     /------\
    /        \ Integration (20-25%)
   /          \
  /____________\
 /              \ Unit (60-70%)
/________________\

Target: 80%+ coverage
```

### 5.2 Unit Tests

**backend/tests/unit/test_models.py**:
- Task creation with validation
- Title length validation
- Status transitions
- Priority assignments

**backend/tests/unit/test_services.py**:
- Create/read/update/delete operations
- Filtering and sorting
- Pagination
- Error handling

### 5.3 Integration Tests

**backend/tests/integration/test_api_tasks.py**:
- POST /api/tasks (create)
- GET /api/tasks (list with filters)
- GET /api/tasks/{id} (get)
- PUT /api/tasks/{id} (update)
- PATCH /api/tasks/{id}/status (status change)
- DELETE /api/tasks/{id} (delete)

**backend/tests/integration/test_full_workflow.py**:
- Complete task lifecycle
- Multi-task filtering
- Error scenarios

### 5.4 Frontend Tests

**__tests__/components/TaskCard.test.tsx**:
- Render task information
- Display checkbox
- Toggle completion
- Apply styles

**__tests__/hooks/useTasks.test.ts**:
- Fetch tasks
- Handle errors
- Polling behavior

---

## 6. ERROR HANDLING

### 6.1 Error Codes (Phase I Reuse)

| Code | HTTP | Exception | Meaning |
|------|------|-----------|---------|
| E001 | 404 | TaskNotFoundError | Task doesn't exist |
| E002 | 400 | InvalidTaskDataError | Invalid input |
| E003 | 500 | DatabaseError | Database operation failed |
| E004 | 409 | DuplicateResourceError | Resource already exists |
| E005 | 422 | ValidationError | Schema/input validation |

### 6.2 Validation Chain

```
Frontend (React)
  ↓ Client-side validation
FastAPI Endpoint
  ↓ Pydantic validation
TaskService
  ↓ Business logic validation
SQLModel
  ↓ ORM validation
Database
  ↓ Constraint validation
```

---

## 7. DEPLOYMENT

### 7.1 Development

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py

# Frontend (new terminal)
cd frontend
npm install
npm run dev

# Visit http://localhost:3000
```

### 7.2 Docker Compose

```bash
docker-compose up
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

### 7.3 Production

**Environment**: Neon PostgreSQL + Vercel (frontend) / Render (backend)

**Environment Variables**:
```
NEXT_PUBLIC_API_URL=https://api.example.com
DATABASE_URL=postgresql://user:pass@neon.endpoint.neon.tech/todo_db
```

---

## 8. PERFORMANCE TARGETS

| Metric | Target | Strategy |
|--------|--------|----------|
| API response (p95) | <200ms | Connection pooling |
| Dashboard load | <2s | Next.js optimization |
| Search response | <300ms | Database indexes |
| Concurrent users | 100+ | Connection pool (20+10) |

**Optimizations**:
- Database indexes on frequently used columns
- Connection pooling with Neon
- Response pagination (default 50 items)
- SWR caching with polling

---

## 9. PHASE III PREPARATION

**Reserved Fields**:
- `metadata`: AI decisions and reasoning (JSONB)
- `scheduled_at`: AI-planned execution time
- `agent_state`: AI processing state (JSONB)

**Audit Trail**:
- Complete history in audit_logs table
- Every change tracked with actor, timestamp, action
- Immutable append-only design

---

## 10. CRITICAL SUCCESS FACTORS

1. **Type Safety**: Pydantic + SQLModel + TypeScript across all layers
2. **Performance**: Connection pooling + indexes + pagination
3. **Multi-Tab Sync**: SWR polling with focus-aware revalidation
4. **Error Handling**: Consistent error codes + clear messages
5. **Testing**: 80%+ coverage (unit + integration + E2E)
6. **Extensibility**: Clean layers for Phase III AI integration

---

## 11. NEXT STEPS

1. **Implement Frontend** (components, hooks, pages)
2. **Complete Testing** (unit + integration + E2E)
3. **Docker Setup** (Dockerfile + docker-compose.yml)
4. **Performance Testing** (load testing, response times)
5. **Production Deployment** (Neon + Vercel/Render)

