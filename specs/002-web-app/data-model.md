# Data Model: Phase II – Full-Stack Web Todo Application

**Created**: 2025-12-29
**Purpose**: Define entities, relationships, constraints, and indexes for Phase II persistence layer

---

## Overview

The data model uses a **hybrid approach**:
- **Normalized**: Tags table with many-to-many junction, separate audit_logs table
- **Denormalized**: Priority field in tasks table for performance on common filters

This design balances:
- Query performance (frequently filtered columns indexed)
- Data integrity (normalized relationships prevent duplication)
- Phase III AI readiness (metadata, scheduled_at, agent_state fields reserved)

---

## Core Entities

### 1. Task (Core Entity)

**Purpose**: Represents a todo item with full state and audit trail

**Fields**:

| Field | Type | Constraints | Purpose |
|-------|------|-----------|---------|
| `id` | SERIAL | PRIMARY KEY | Unique identifier |
| `title` | VARCHAR(500) | NOT NULL, non-empty | Task name/summary |
| `description` | VARCHAR(5000) | Optional | Detailed task notes |
| `status` | ENUM | DEFAULT 'pending', NOT NULL | State: pending / complete / archived |
| `priority` | ENUM | DEFAULT 'MEDIUM', NOT NULL | Urgency: LOW / MEDIUM / HIGH |
| `due_date` | TIMESTAMP | Optional | Task deadline |
| `created_at` | TIMESTAMP | DEFAULT NOW(), NOT NULL | Creation timestamp (immutable) |
| `updated_at` | TIMESTAMP | DEFAULT NOW(), NOT NULL | Last modification timestamp |
| `metadata` | JSONB | DEFAULT '{}' | **Phase III**: AI decisions & reasoning |
| `scheduled_at` | TIMESTAMP | Optional | **Phase III**: AI-planned execution time |
| `agent_state` | JSONB | DEFAULT '{}' | **Phase III**: AI processing state |

**Relationships**:
- **One-to-Many** with `audit_logs`: Every change logged
- **Many-to-Many** with `tags`: Via `task_tags` junction table

**Indexes**:
- `idx_tasks_status_priority_created`: Composite index for common filtering + sorting
- `idx_tasks_created_at_desc`: For "recent tasks" queries
- `idx_tasks_due_date`: For "upcoming tasks" queries
- `idx_tasks_status`, `idx_tasks_priority`: Individual filter performance

**Validation**:
- Title: Required, 1-500 characters (CHECK constraint)
- Description: Optional, max 5000 characters (CHECK constraint)
- Status: Must be one of 3 enum values (ENUM type validation)
- Priority: Must be one of 3 enum values (ENUM type validation)
- Due date: Must be valid timestamp (type validation)

**Lifecycle**:
- **Created**: Status = 'pending', priority defaults to 'MEDIUM'
- **Updated**: Bulk operations on tasks update `updated_at` via trigger
- **Completed**: Status → 'complete', audit logged with 'complete' action
- **Archived**: Status → 'archived', audit logged with 'archive' action
- **Deleted**: Cascade deletes from `task_tags` and `audit_logs` tables

---

### 2. Tag (Categorization Entity)

**Purpose**: Represent task categories/labels for organization and filtering

**Fields**:

| Field | Type | Constraints | Purpose |
|-------|------|-----------|---------|
| `id` | SERIAL | PRIMARY KEY | Unique identifier |
| `name` | VARCHAR(50) | UNIQUE, NOT NULL, non-empty | Tag name (e.g., "urgent", "work") |
| `created_at` | TIMESTAMP | DEFAULT NOW(), NOT NULL | Creation timestamp |

**Relationships**:
- **Many-to-Many** with `tasks`: Via `task_tags` junction table

**Indexes**:
- `idx_tags_name`: For tag lookup and autocomplete

**Validation**:
- Name: Required, unique, 1-50 characters (UNIQUE constraint + CHECK constraint)

**Lifecycle**:
- **Created**: When first used in a POST /api/tags or added to a task
- **Reused**: Multiple tasks can reference same tag
- **Deleted**: Only when explicitly removed (soft delete pattern in Phase III)

---

### 3. Task-Tag Junction (Relationship Table)

**Purpose**: Many-to-many relationship between tasks and tags

**Fields**:

| Field | Type | Constraints | Purpose |
|-------|------|-----------|---------|
| `task_id` | INT FK | REFERENCES tasks(id), CASCADE | Task reference |
| `tag_id` | INT FK | REFERENCES tags(id), CASCADE | Tag reference |
| `created_at` | TIMESTAMP | DEFAULT NOW(), NOT NULL | When tag was added to task |

**Primary Key**: Composite `(task_id, tag_id)` — prevents duplicate relationships

**Indexes**:
- `idx_task_tags_task_id`: For "find all tags for a task" queries
- `idx_task_tags_tag_id`: For "find all tasks with a tag" queries

**Cascade Behavior**:
- If task deleted → all task_tags rows deleted
- If tag deleted → all task_tags rows deleted

---

### 4. Audit Log (Immutable History)

**Purpose**: Complete, immutable history of all task changes for audit trail and AI learning

**Fields**:

| Field | Type | Constraints | Purpose |
|-------|------|-----------|---------|
| `id` | SERIAL | PRIMARY KEY | Event identifier |
| `task_id` | INT FK | REFERENCES tasks(id), CASCADE | Which task changed |
| `action` | ENUM | NOT NULL | What happened: create/update/delete/complete/archive/tag_add/tag_remove |
| `previous_state` | JSONB | Optional | Task JSON before change |
| `new_state` | JSONB | Optional | Task JSON after change |
| `actor` | VARCHAR(255) | NOT NULL | Who made the change (user ID, AI agent ID, or 'system') |
| `reason` | VARCHAR(500) | Optional | Why the change was made (user comment or AI reasoning) |
| `timestamp` | TIMESTAMP | DEFAULT NOW(), NOT NULL | When change occurred (UTC) |
| `metadata` | JSONB | DEFAULT '{}' | Additional context (request ID, source, etc.) |

**Relationships**:
- **Many-to-One** with `tasks`: Foreign key to task.id

**Indexes**:
- `idx_audit_logs_task_id`: For "get full history of a task"
- `idx_audit_logs_timestamp`: For "recent changes" queries
- `idx_audit_logs_action`: For "find all completions" queries (AI learning)
- `idx_audit_logs_actor`: For "find all AI agent actions" queries

**Validation**:
- Task ID: Must reference existing task (FK constraint)
- Action: Must be one of 7 enum values
- Actor: Required, non-empty (CHECK constraint)

**Immutability**:
- Audit logs are APPEND-ONLY (no UPDATE or DELETE)
- Enables legal audit trail and AI learning without data loss

**Auto-Logging Triggers**:
- **INSERT on tasks**: Logged as 'create' with new_state
- **UPDATE on tasks** (status changed to 'complete'): Logged as 'complete'
- **UPDATE on tasks** (status changed to 'archived'): Logged as 'archive'
- **UPDATE on tasks** (other changes): Logged as 'update' with before/after state
- **INSERT on task_tags**: Logged as 'tag_add' via API layer
- **DELETE on task_tags**: Logged as 'tag_remove' via API layer

---

## Relationship Diagram

```
┌─────────────────┐
│     TASKS       │
├─────────────────┤
│ id (PK)         │
│ title           │
│ description     │
│ status          │───────┐
│ priority        │       │ (1)
│ due_date        │       │
│ created_at      │       │
│ updated_at      │       │
│ metadata        │       │
│ scheduled_at    │       │
│ agent_state     │       │
└─────────────────┘       │
         │                │
         │ (*)            │ (*)
         │                │
    ┌────────────────┐    │
    │  TASK_TAGS     │    │
    ├────────────────┤    │
    │ task_id (FK) ──┼────┤
    │ tag_id (FK) ───┼──┐ │
    │ created_at     │  │ │
    └────────────────┘  │ │
                        │ │
                        │ └──────────┐
                        │           │
                        │    ┌──────────────┐
                        └────│    TAGS      │
                             ├──────────────┤
                             │ id (PK)      │
                             │ name (UNIQUE)│
                             │ created_at   │
                             └──────────────┘

┌─────────────────┐
│  AUDIT_LOGS     │
├─────────────────┤
│ id (PK)         │
│ task_id (FK) ───┼────────────┐
│ action          │            │ (1)
│ previous_state  │            │
│ new_state       │            │
│ actor           │    ┌──────────────┐
│ reason          │    │    TASKS     │
│ timestamp       │    └──────────────┘
│ metadata        │ (*)
└─────────────────┘
```

---

## Index Strategy

### Query Performance Paths

| Use Case | Index | Why |
|----------|-------|-----|
| "Show all pending tasks, sorted by priority" | `idx_tasks_status_priority_created` | Matches WHERE status + ORDER BY priority + created_at |
| "Show tasks due today, ordered by priority" | `idx_tasks_due_date` | Efficient range query on due_date |
| "Find all tasks with 'urgent' tag" | `idx_task_tags_tag_id` + `idx_tags_name` | Joins through task_tags using tag_id |
| "Get audit history of task #42" | `idx_audit_logs_task_id` | Fast lookup of all changes to a specific task |
| "Recent AI agent actions" | `idx_audit_logs_actor` + `idx_audit_logs_timestamp` | Filter by AI actor, sort by timestamp DESC |

### Composite Index Design

**Rationale for `idx_tasks_status_priority_created`**:
- Most common query: "Show tasks WHERE status = ? AND priority = ? ORDER BY created_at DESC"
- Single composite index covers all three columns
- Prevents separate index lookups
- Example: `SELECT * FROM tasks WHERE status = 'pending' AND priority = 'HIGH' ORDER BY created_at DESC`

---

## Constraints & Validation

### CHECK Constraints (Data Integrity)

```sql
-- Title validation
CONSTRAINT title_not_empty CHECK (title <> '')
CONSTRAINT title_max_length CHECK (char_length(title) <= 500)

-- Description validation
CONSTRAINT description_max_length CHECK (char_length(description) <= 5000)

-- Tag validation
CONSTRAINT tag_name_not_empty CHECK (name <> '')
CONSTRAINT tag_name_max_length CHECK (char_length(name) <= 50)

-- Audit validation
CONSTRAINT actor_not_empty CHECK (actor <> '')
```

### ENUM Constraints

- **task_status**: Restricted to {'pending', 'complete', 'archived'}
- **task_priority**: Restricted to {'LOW', 'MEDIUM', 'HIGH'}
- **audit_action**: Restricted to {'create', 'update', 'delete', 'complete', 'archive', 'tag_add', 'tag_remove'}

### Foreign Key Constraints (Referential Integrity)

- `task_tags.task_id` → `tasks.id` (ON DELETE CASCADE)
- `task_tags.tag_id` → `tags.id` (ON DELETE CASCADE)
- `audit_logs.task_id` → `tasks.id` (ON DELETE CASCADE)

---

## Triggers & Automation

### Trigger 1: Auto-Update `updated_at`

**Trigger Name**: `trigger_update_task_updated_at`
**Event**: BEFORE UPDATE on tasks
**Action**: Set `updated_at = NOW()`
**Purpose**: Maintains accurate modification timestamps without app logic

### Trigger 2: Auto-Log Task Changes

**Trigger Name**: `trigger_log_task_change`
**Event**: AFTER INSERT or UPDATE on tasks
**Action**: Insert corresponding row into `audit_logs`
**Purpose**: Automatic audit trail creation; enables Phase III AI learning without app intervention

**Behavior**:
- On INSERT: Logs 'create' action with new_state
- On UPDATE (status → 'complete'): Logs 'complete' action
- On UPDATE (status → 'archived'): Logs 'archive' action
- On UPDATE (other): Logs 'update' action with before/after states

---

## Storage & Performance Estimates

| Table | Avg Row Size | Expected Rows (1 Year) | Storage (est.) | Notes |
|-------|-------------|----------------------|-----------------|-------|
| tasks | 2 KB | 10,000 | 20 MB | Main workload |
| tags | 100 B | 50-100 | <1 MB | Reused across tasks |
| task_tags | 16 B | 30,000 | 500 KB | Many-to-many relationships |
| audit_logs | 1 KB | 50,000 | 50 MB | Complete history; append-only |
| **Total** | — | — | **~70 MB** | Well within Neon free tier |

---

## Migration & Evolution

### Phase II → Phase III Readiness

**Reserved Fields** (empty in Phase II, used in Phase III):
- `tasks.metadata`: AI stores decisions and reasoning
- `tasks.scheduled_at`: AI plans future task execution
- `tasks.agent_state`: AI marks processing status

**Non-Breaking Additions**:
- New audit_action values (e.g., 'ai_scheduled', 'ai_completed')
- New tables can be added without migrating existing data
- Backward compatibility maintained through JSON fields

### Safe Evolution Path

1. **Phase II**: Deploy schema with reserved fields (ignored)
2. **Phase III Prep**: Add indexes on metadata and agent_state if needed
3. **Phase III**: Populate reserved fields via API updates
4. **Phase IV**: Add new audit actions and logging logic

---

## Security Considerations

### Data Protection

- **Audit Trail**: Immutable append-only log prevents data tampering
- **Foreign Keys**: Cascade rules prevent orphaned records
- **Input Validation**: CHECK constraints at database level
- **Parameterized Queries**: ORM prevents SQL injection (SQLModel/Pydantic)

### Query Safety

- All queries use parameterized inputs (SQLAlchemy ORM)
- No direct SQL construction from user input
- Prepared statements cached by database driver

---

## Testing Checklist

- [ ] Schema creates without errors on fresh Neon database
- [ ] All enums enforce valid values
- [ ] All CHECK constraints reject invalid data
- [ ] Foreign key constraints prevent orphaned records
- [ ] Cascade deletes work correctly (delete task → deletes task_tags & audit_logs)
- [ ] Triggers auto-update `updated_at` on task changes
- [ ] Triggers auto-log all task changes to `audit_logs`
- [ ] Indexes perform efficiently (EXPLAIN ANALYZE on common queries)
- [ ] Sample data inserts successfully
- [ ] Audit log captures full state before/after for all operations

---

## Files

- **Schema**: `backend/database-schema.sql` (SQLAlchemy will also generate via models)
- **Migrations**: `backend/alembic/versions/` (when ready)
- **Model Code**: `backend/src/models/{base.py, task.py, tag.py, audit_log.py}`

