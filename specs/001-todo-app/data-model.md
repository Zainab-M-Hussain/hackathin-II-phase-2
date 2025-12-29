# Data Model: Console Todo Application

**Date**: 2025-12-29 | **Phase**: Phase 1 Design | **Input**: plan.md

## Entity: Task

Represents a single todo item with complete schema for Phase I–V lifecycle.

### Fields

| Field | Type | Required | Constraints | Purpose |
|-------|------|----------|-------------|---------|
| `id` | `int` | ✅ | Auto-incremented, unique within single-user context, ≥ 1 | Unique task identifier; Phase II will namespace with user_id |
| `title` | `str` | ✅ | 1–500 chars, non-empty, non-whitespace | Task name/description shown in list |
| `description` | `str` | ❌ | 0–500 chars, optional | Extended task details |
| `is_completed` | `bool` | ✅ | Default: `false` | Completion status (✓ or ○) |
| `created_at` | `datetime` | ✅ | Auto-generated on creation, ISO 8601 | Audit trail for Phase IV cloud logs |
| `tags` | `List[str]` | ❌ | Optional, reserved for Phase III AI | Keywords for search/categorization (Phase I ignores) |
| `metadata` | `Dict[str, Any]` | ❌ | Optional, extensible key-value pairs | Future use by Phase III+ (Phase I ignores) |

### Validation Rules

| Field | Rule | Error Code | User Message |
|-------|------|-----------|--------------|
| `title` | Non-empty after strip | E001 | Task title cannot be empty or contain only whitespace |
| `title` | Max 500 characters | E001 | Task title cannot exceed 500 characters |
| `description` | Max 500 characters | E004 | Task description cannot exceed 500 characters |
| `id` | Positive integer | E003 | Invalid task ID. Please enter a number. |
| `is_completed` | Boolean only | E005 | Operation failed: invalid completion status |

### State Transitions

```
┌─────────────────────────────────────┐
│  Initial State: is_completed=false  │
└──────────────┬──────────────────────┘
               │
        mark_complete()
               │
               ▼
┌─────────────────────────────────────┐
│  Completed State: is_completed=true │
└──────────────┬──────────────────────┘
               │
       mark_incomplete()
               │
               ▼
┌─────────────────────────────────────┐
│ Back to Initial: is_completed=false │
└─────────────────────────────────────┘
```

### Methods

#### `__init__(task_id: int, title: str, description: str = "")`

**Purpose**: Create a new Task instance.

**Parameters**:
- `task_id`: Auto-assigned integer (≥ 1)
- `title`: Task title (required, validated)
- `description`: Optional description (default: empty string)

**Returns**: Task instance

**Raises**: `ValueError` if title invalid (maps to E001)

**Example**:
```python
task = Task(1, "Buy groceries", "Milk, eggs, bread")
# task.id = 1
# task.title = "Buy groceries"
# task.description = "Milk, eggs, bread"
# task.is_completed = False
# task.created_at = datetime.now()
```

---

#### `mark_complete() -> None`

**Purpose**: Mark task as completed.

**Side Effects**: Sets `is_completed = True`

**Example**:
```python
task.mark_complete()
assert task.is_completed == True
```

---

#### `mark_incomplete() -> None`

**Purpose**: Mark task as incomplete (revert to incomplete state).

**Side Effects**: Sets `is_completed = False`

**Example**:
```python
task.mark_incomplete()
assert task.is_completed == False
```

---

#### `update(title: str, description: str = "") -> None`

**Purpose**: Update task title and description.

**Parameters**:
- `title`: New title (validated)
- `description`: New description (optional, default: empty string)

**Raises**: `ValueError` if title invalid (maps to E001)

**Side Effects**: Updates `title` and `description` fields

**Example**:
```python
task.update("Buy groceries & cook", "Milk, eggs, bread, chicken")
assert task.title == "Buy groceries & cook"
assert task.description == "Milk, eggs, bread, chicken"
```

---

#### `to_dict() -> Dict[str, Any]`

**Purpose**: Serialize Task to JSON-compatible dictionary (Phase IV cloud contract).

**Returns**: Dictionary matching JSON schema

**Example**:
```python
json_data = task.to_dict()
# {
#   "id": 1,
#   "title": "Buy groceries",
#   "description": "Milk, eggs, bread",
#   "is_completed": False,
#   "created_at": "2025-12-29T10:30:00.000Z",
#   "tags": None,
#   "metadata": None
# }
```

---

#### `from_dict(data: Dict[str, Any]) -> Task` (classmethod)

**Purpose**: Deserialize Task from JSON dictionary (Phase IV cloud contract).

**Parameters**: Dictionary matching JSON schema

**Returns**: Reconstructed Task instance

**Raises**: `ValueError` if data invalid

**Example**:
```python
json_data = {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "is_completed": False,
    "created_at": "2025-12-29T10:30:00.000Z",
    "tags": None,
    "metadata": None
}
task = Task.from_dict(json_data)
assert task.title == "Buy groceries"
```

---

### Relationships

**Phase I**: Standalone entity; no foreign keys (single-user context).

**Phase II**: Will be namespaced with `user_id` at HTTP layer.
```
user_id:task_id  (e.g., "user_123:task_5")
```

**Phase III**: Will populate `tags` and `metadata` for AI context.

**Phase IV**: Will store in database with additional schema columns:
- `user_id` (FK to users table)
- `tenant_id` (multi-tenant support)
- Database indexes on `user_id`, `created_at`, `tags`

---

## JSON Schema Contract (Phase IV Cloud Format)

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "minimum": 1,
      "description": "Unique task ID within single-user context"
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 500,
      "description": "Task title"
    },
    "description": {
      "type": "string",
      "maxLength": 500,
      "description": "Optional task description"
    },
    "is_completed": {
      "type": "boolean",
      "default": false,
      "description": "Completion status"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 creation timestamp"
    },
    "tags": {
      "type": ["array", "null"],
      "items": {"type": "string"},
      "description": "Optional tags for Phase III AI and Phase IV search"
    },
    "metadata": {
      "type": ["object", "null"],
      "description": "Optional extensible metadata for Phase III+"
    }
  },
  "required": ["id", "title", "is_completed", "created_at"]
}
```

---

## Validation Error Mapping

| Error Code | Error Message | Scenario | Recovery |
|-----------|--------------|----------|----------|
| E001 | Task title cannot be empty or contain only whitespace | User inputs empty/whitespace-only title | Prompt for valid title |
| E001 | Task title cannot exceed 500 characters | User inputs > 500 chars | Truncate or reject |
| E002 | Task not found with ID {id} | User references non-existent task | Show available tasks |
| E003 | Invalid task ID. Please enter a number. | User inputs non-numeric ID | Prompt for numeric ID |
| E004 | Task description cannot exceed 500 characters | User inputs description > 500 chars | Truncate or reject |
| E005 | Operation failed | Generic operation error | Retry or contact support |

---

## Design Rationale

### Why Include `tags` and `metadata` in Phase I?

- **Phase III AI Chatbot**: Needs to attach context (reminders, priorities) to tasks
- **Phase IV Cloud**: Can index tags for search functionality
- **Phase I**: Ignores these fields entirely; ensures forward compatibility
- **Benefit**: Eliminates redesign when Phase III arrives; Phase III can populate immediately

### Why Structured Error Codes?

- **Phase II Web**: HTTP API needs consistent error responses for all clients
- **Phase IV Cloud**: Logs must use same codes across all services for debugging
- **Phase I**: Console uses codes internally; displays user-friendly messages
- **Benefit**: Single error taxonomy eliminates translation/mapping overhead in downstream phases

### Why JSON Schema in Phase I?

- **Phase IV Cloud**: Must persist to database with known structure
- **Phase II Web**: HTTP endpoints must serialize to JSON; Phase I defines schema
- **Data Migration**: Phase I → Phase IV doesn't require reformatting
- **Benefit**: Eliminates schema conflicts at Phase IV; enables early validation

### Why Single-User Task IDs?

- **Phase I**: Simple auto-incrementing IDs (1, 2, 3…)
- **Phase II Web**: Adds `user_id` namespace at HTTP layer (user_123:task_1)
- **Phase IV Cloud**: Stores `user_id` as separate field in database
- **Benefit**: Phase I stays simple; Phase II adds complexity only where needed

---

## Future Evolution

### Phase II (Web App)

- Extend Task with `user_id` field
- API endpoints return Task as JSON (uses `to_dict()`)
- Database schema mirrors JSON structure
- `tags` field enables search/filter endpoints

### Phase III (AI Chatbot)

- Populate `tags` with AI-inferred categories ("work", "personal", "urgent")
- Populate `metadata` with reminders ({"reminder_at": "2025-12-30T09:00:00Z"})
- Query tasks by tags for chatbot context
- No Phase I changes required

### Phase IV (Cloud)

- Store Task entities in multi-tenant database
- Use JSON schema for validation on INSERT/UPDATE
- Create indices on `user_id`, `created_at`, `tags`
- Error codes (E001–E005) drive logging and monitoring

---

## Implementation Notes

- **Immutability**: Task ID and `created_at` are immutable after creation
- **Timezone**: `created_at` always stored in UTC (ISO 8601)
- **Serialization**: `to_dict()` must handle None values for tags/metadata
- **Deserialization**: `from_dict()` must validate all fields before construction
- **Testing**: All state transitions tested; all error codes mapped to tests
