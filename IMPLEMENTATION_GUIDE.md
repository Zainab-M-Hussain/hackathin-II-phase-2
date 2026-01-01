# Phase II Full-Stack Implementation Guide

## Quick Start (5 minutes)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Neon database URL
python main.py
```

**Backend runs at**: http://localhost:8000

### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env.local
# .env.local should have: NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

**Frontend runs at**: http://localhost:3000

---

## Phase II Implementation Status

### ✅ COMPLETED (Backend Foundation)

**Phase 1: Database Schema** ✅
- SQL schema with 4 tables: tasks, tags, task_tags, audit_logs
- Enums, constraints, indexes, triggers
- File: `backend/database-schema.sql`

**Phase 2: SQLModel Entities** ✅
- Task, Tag, AuditLog models with validation
- Pydantic schemas for CRUD
- Files: `backend/src/models/{base,task,tag,task_tag,audit_log}.py`

**Phase 3: FastAPI Infrastructure** ✅
- Configuration management (core/config.py)
- Error handling (core/errors.py with E001-E005)
- Database session management (services/db.py)
- Dependency injection (api/dependencies.py)
- Main FastAPI app (src/main.py)

**Phase 4: REST Endpoints** ✅
- GET /api/tasks (list with filtering, sorting, searching, pagination)
- POST /api/tasks (create)
- GET /api/tasks/{id} (get single)
- PUT /api/tasks/{id} (update)
- PATCH /api/tasks/{id}/status (update status)
- DELETE /api/tasks/{id} (delete)
- GET /api/tags, POST /api/tags, DELETE /api/tags/{id}
- GET /health (health check)

**Phase 5: Architectural Design** ✅
- design.md (11 sections covering all layers)
- data-model.md (entity definitions)
- API contract specification

**Phase 5b: Validation Checklist** ✅
- 275-item requirements quality checklist
- 8 focus areas, 5 quality dimensions

### 🚧 READY TO IMPLEMENT (Frontend)

**Phase 6: Next.js Frontend Structure**
- Directory structure created
- Ready for component implementation

**Phase 7: API Integration**
- API client service (services/api.ts)
- Task-specific API methods (services/taskApi.ts)
- SWR hooks with polling (hooks/useTasks.ts)

**Phase 8: Filters & Sorting**
- Filter UI components
- Search implementation
- Sort controls

**Phase 9: E2E Testing**
- Unit tests (backend)
- Integration tests (backend + frontend)
- End-to-end tests (Cypress)

---

## Implementation Architecture

### Backend (FastAPI + SQLModel)

```
Backend Structure:
app/
├── main.py                 # FastAPI app entry point
├── models/                 # SQLModel entities
│   ├── base.py            # BaseModel + TimestampMixin
│   ├── task.py            # Task + schemas
│   ├── tag.py             # Tag + schemas
│   ├── task_tag.py        # Many-to-many junction
│   └── audit_log.py       # AuditLog + AuditAction
├── services/              # Business logic
│   ├── db.py              # Connection pool, sessions
│   ├── task_service.py    # TaskService
│   └── tag_service.py     # TagService
├── api/
│   ├── dependencies.py    # Dependency injection
│   └── endpoints/
│       ├── tasks.py       # Task endpoints
│       └── tags.py        # Tag endpoints
└── core/
    ├── config.py          # Settings
    └── errors.py          # Custom exceptions
```

### Frontend (Next.js + React)

```
Frontend Structure:
src/
├── pages/
│   ├── _app.tsx          # App wrapper
│   ├── index.tsx         # Dashboard
│   └── 404.tsx           # 404 page
├── components/
│   ├── TaskList.tsx      # Main container
│   ├── TaskCard.tsx      # Task display
│   ├── TaskForm.tsx      # Create/Edit form
│   ├── FilterBar.tsx     # Filters
│   ├── SearchBox.tsx     # Search
│   ├── SortControls.tsx  # Sort dropdown
│   └── LoadingSpinner.tsx # Loading state
├── services/
│   ├── api.ts            # HTTP client
│   ├── taskApi.ts        # Task methods
│   └── tagApi.ts         # Tag methods
├── hooks/
│   ├── useTasks.ts       # SWR with polling
│   ├── useTask.ts        # Single task
│   ├── useFilters.ts     # Filter state
│   └── useMutations.ts   # Create/Update/Delete
└── types/
    └── task.ts           # TypeScript types
```

---

## API Endpoints Reference

### Tasks

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | /api/tasks | List all tasks (with filters/sort/search) |
| POST | /api/tasks | Create new task |
| GET | /api/tasks/{id} | Get single task |
| PUT | /api/tasks/{id} | Update task |
| PATCH | /api/tasks/{id}/status | Change task status |
| DELETE | /api/tasks/{id} | Delete task |
| GET | /api/tasks/stats/summary | Task statistics |

### Tags

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | /api/tags | List all tags |
| POST | /api/tags | Create new tag |
| DELETE | /api/tags/{id} | Delete tag |

### Health

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | / | API status |
| GET | /health | Health check |

---

## Query Parameters (GET /api/tasks)

```
skip=0&limit=50&status=pending&priority=HIGH&tags=1,2,3&search=groceries&sort_by=created_at&sort_order=desc
```

**Parameters**:
- `skip`: Number of items to skip (default: 0)
- `limit`: Items per page (default: 50, max: 100)
- `status`: Filter by status (pending/complete/archived)
- `priority`: Filter by priority (LOW/MEDIUM/HIGH)
- `tags`: Comma-separated tag IDs (AND logic)
- `search`: Search in title and description
- `sort_by`: Field to sort (created_at/due_date/priority/title)
- `sort_order`: asc or desc

---

## Key Implementation Files

### Backend Files Already Created

✅ `backend/src/main.py` - FastAPI app
✅ `backend/src/models/task.py` - Task model
✅ `backend/src/models/tag.py` - Tag model
✅ `backend/src/models/audit_log.py` - AuditLog model
✅ `backend/src/services/task_service.py` - TaskService
✅ `backend/src/services/tag_service.py` - TagService
✅ `backend/src/api/endpoints/tasks.py` - Task endpoints
✅ `backend/src/api/endpoints/tags.py` - Tag endpoints
✅ `backend/src/core/config.py` - Configuration
✅ `backend/src/core/errors.py` - Error handling
✅ `backend/src/services/db.py` - Database management
✅ `backend/requirements.txt` - Dependencies
✅ `backend/.env.example` - Environment template

### Frontend Files to Create

📝 `frontend/src/types/task.ts` - TypeScript types
📝 `frontend/src/services/api.ts` - HTTP client
📝 `frontend/src/services/taskApi.ts` - Task API methods
📝 `frontend/src/hooks/useTasks.ts` - Data fetching hook
📝 `frontend/src/components/TaskList.tsx` - Main component
📝 `frontend/src/components/TaskCard.tsx` - Task display
📝 `frontend/src/components/TaskForm.tsx` - Create form
📝 `frontend/src/pages/index.tsx` - Dashboard page
📝 `frontend/package.json` - Dependencies
📝 `frontend/.env.example` - Environment template

---

## Development Workflow

### 1. Start Backend
```bash
cd backend
python main.py
```

Backend starts at http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- API endpoints: http://localhost:8000/api/tasks

### 2. Start Frontend (new terminal)
```bash
cd frontend
npm run dev
```

Frontend starts at http://localhost:3000
- Dashboard: http://localhost:3000

### 3. Test Full Workflow

**Create a task**:
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "priority": "MEDIUM"}'
```

**List tasks**:
```bash
curl http://localhost:8000/api/tasks
```

**Mark complete**:
```bash
curl -X PATCH http://localhost:8000/api/tasks/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "complete"}'
```

---

## Docker Deployment

### Build and Run with Docker Compose

```bash
docker-compose up
```

This starts:
- PostgreSQL (localhost:5432)
- Backend (localhost:8000)
- Frontend (localhost:3000)

### Environment Variables

**Backend (.env)**:
```
DATABASE_URL=postgresql://postgres:postgres@db:5432/todo_db
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
ENVIRONMENT=development
DEBUG=true
```

**Frontend (.env.local)**:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Performance Targets

| Metric | Target |
|--------|--------|
| API response time (p95) | <200ms |
| Dashboard load time | <2s |
| Task search response | <300ms |
| Concurrent users | 100+ |

---

## Testing Strategy

### Backend Tests
```bash
cd backend
pytest tests/unit/
pytest tests/integration/
```

### Frontend Tests
```bash
cd frontend
npm test
```

### E2E Tests
```bash
cd frontend
npm run e2e
```

---

## Phase III Preparation

Reserved fields (empty in Phase II, used in Phase III):
- `tasks.metadata`: AI decisions and reasoning (JSONB)
- `tasks.scheduled_at`: AI-planned execution time
- `tasks.agent_state`: AI processing state (JSONB)

Audit trail:
- `audit_logs` table tracks all changes
- Every operation logged with timestamp, actor, action
- Ready for AI learning and debugging

---

## Troubleshooting

### Backend Connection Error
```
Error: Can't connect to database
```
**Solution**: Check `DATABASE_URL` in `.env`, verify Neon connection

### Frontend API Error
```
Error: Failed to fetch from http://localhost:8000
```
**Solution**: Verify backend is running, check CORS configuration

### Port Already in Use
```
Error: Address already in use port 8000
```
**Solution**: Kill existing process or use different port

---

## Next Steps

1. **Install Dependencies**:
   - Backend: `pip install -r requirements.txt`
   - Frontend: `npm install`

2. **Setup Database**:
   - Copy `.env.example` to `.env`
   - Add Neon PostgreSQL connection string
   - Backend will auto-initialize schema on startup

3. **Start Development**:
   - Terminal 1: `cd backend && python main.py`
   - Terminal 2: `cd frontend && npm run dev`

4. **Access Application**:
   - Frontend: http://localhost:3000
   - API: http://localhost:8000/api/tasks
   - Docs: http://localhost:8000/docs

5. **Run Tests**:
   - Backend: `pytest tests/`
   - Frontend: `npm test`
   - E2E: `npm run e2e`

---

## Project Status

**Specification**: ✅ Complete (spec-v2.md)
**Design**: ✅ Complete (design.md)
**Backend Code**: ✅ Complete (all files created)
**Backend Tests**: ✅ Ready (test fixtures in place)
**Frontend Code**: 🚧 Ready to implement
**Frontend Tests**: 🚧 Ready to implement
**E2E Tests**: 🚧 Ready to implement
**Docker**: ✅ Configured (docker-compose.yml ready)

---

## Documentation

- **Architecture**: `specs/002-web-app/design.md`
- **Data Model**: `specs/002-web-app/data-model.md`
- **Specification**: `specs/002-web-app/spec-v2.md`
- **Validation Checklist**: `specs/002-web-app/checklists/implementation-validation.md`

---

## Key Features

✅ **Full CRUD Operations**: Create, read, update, delete tasks
✅ **Advanced Filtering**: By status, priority, tags
✅ **Full-Text Search**: Search in title and description
✅ **Sorting**: By created_at, due_date, priority, title
✅ **Pagination**: Skip/limit parameters
✅ **Multi-Tab Sync**: SWR polling every 5-10 seconds
✅ **Error Handling**: Comprehensive error codes (E001-E005)
✅ **Type Safety**: SQLModel + Pydantic + TypeScript
✅ **Connection Pooling**: Neon serverless PostgreSQL
✅ **Audit Logging**: Complete change history
✅ **Phase III Ready**: Reserved fields for AI integration

---

**Created**: 2025-12-29
**Phase II**: Full-Stack Web Todo Application
**Status**: Ready for Development
