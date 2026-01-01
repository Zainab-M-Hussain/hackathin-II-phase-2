-- Phase II Database Schema
-- Neon Serverless Postgres
-- Hybrid approach: normalized (tags, audit_log) + denormalized (priority) for performance

-- ============================================================================
-- Enums
-- ============================================================================

CREATE TYPE task_status AS ENUM ('pending', 'complete', 'archived');
CREATE TYPE task_priority AS ENUM ('LOW', 'MEDIUM', 'HIGH');
CREATE TYPE audit_action AS ENUM ('create', 'update', 'delete', 'complete', 'archive', 'tag_add', 'tag_remove');

-- ============================================================================
-- Core Tables
-- ============================================================================

-- Tasks table: Core todo items
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description VARCHAR(5000),
    status task_status DEFAULT 'pending' NOT NULL,
    priority task_priority DEFAULT 'MEDIUM' NOT NULL,
    due_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,

    -- Phase III AI Integration Fields (reserved, empty in Phase II)
    metadata JSONB DEFAULT '{}'::jsonb,           -- AI stores decisions, reasoning, confidence scores
    scheduled_at TIMESTAMP,                       -- AI can plan future task execution
    agent_state JSONB DEFAULT '{}'::jsonb,       -- AI marks tasks it's processing

    CONSTRAINT title_not_empty CHECK (title <> ''),
    CONSTRAINT title_max_length CHECK (char_length(title) <= 500),
    CONSTRAINT description_max_length CHECK (char_length(description) <= 5000)
);

-- Tags table: Categories for tasks
CREATE TABLE IF NOT EXISTS tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,

    CONSTRAINT tag_name_not_empty CHECK (name <> ''),
    CONSTRAINT tag_name_max_length CHECK (char_length(name) <= 50)
);

-- Task-Tag junction table: Many-to-many relationship
CREATE TABLE IF NOT EXISTS task_tags (
    task_id INT NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    tag_id INT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (task_id, tag_id)
);

-- Audit Log table: Complete history of all changes (Phase III AI learning)
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    task_id INT NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    action audit_action NOT NULL,
    previous_state JSONB,                  -- State before change
    new_state JSONB,                       -- State after change
    actor VARCHAR(255),                    -- User or AI agent ID
    reason VARCHAR(500),                   -- Why the change was made
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,    -- Additional context

    CONSTRAINT actor_not_empty CHECK (actor <> '')
);

-- ============================================================================
-- Indexes: Optimized for common queries
-- ============================================================================

-- Core performance indexes for task queries
CREATE INDEX idx_tasks_status_priority_created ON tasks(status, priority, created_at DESC);
CREATE INDEX idx_tasks_created_at_desc ON tasks(created_at DESC);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_priority ON tasks(priority);

-- Tag queries
CREATE INDEX idx_tags_name ON tags(name);

-- Task-Tag junction for filter performance
CREATE INDEX idx_task_tags_task_id ON task_tags(task_id);
CREATE INDEX idx_task_tags_tag_id ON task_tags(tag_id);

-- Audit log queries (for Phase III AI learning)
CREATE INDEX idx_audit_logs_task_id ON audit_logs(task_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp DESC);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_actor ON audit_logs(actor);

-- ============================================================================
-- Functions & Triggers
-- ============================================================================

-- Auto-update updated_at timestamp on task changes
CREATE OR REPLACE FUNCTION update_task_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_task_updated_at
BEFORE UPDATE ON tasks
FOR EACH ROW
EXECUTE FUNCTION update_task_updated_at();

-- Auto-log all task changes to audit_logs
CREATE OR REPLACE FUNCTION log_task_change()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_logs (task_id, action, new_state, actor, timestamp)
        VALUES (NEW.id, 'create', row_to_json(NEW), 'system', CURRENT_TIMESTAMP);
    ELSIF TG_OP = 'UPDATE' THEN
        -- Determine specific action based on what changed
        IF OLD.status != NEW.status AND NEW.status = 'complete' THEN
            INSERT INTO audit_logs (task_id, action, previous_state, new_state, actor, timestamp)
            VALUES (NEW.id, 'complete', row_to_json(OLD), row_to_json(NEW), 'system', CURRENT_TIMESTAMP);
        ELSIF OLD.status != NEW.status AND NEW.status = 'archived' THEN
            INSERT INTO audit_logs (task_id, action, previous_state, new_state, actor, timestamp)
            VALUES (NEW.id, 'archive', row_to_json(OLD), row_to_json(NEW), 'system', CURRENT_TIMESTAMP);
        ELSE
            INSERT INTO audit_logs (task_id, action, previous_state, new_state, actor, timestamp)
            VALUES (NEW.id, 'update', row_to_json(OLD), row_to_json(NEW), 'system', CURRENT_TIMESTAMP);
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_log_task_change
AFTER INSERT OR UPDATE ON tasks
FOR EACH ROW
EXECUTE FUNCTION log_task_change();

-- ============================================================================
-- Sample Data (for testing)
-- ============================================================================

-- Insert sample tags
INSERT INTO tags (name) VALUES
    ('urgent'),
    ('work'),
    ('personal'),
    ('shopping'),
    ('health')
ON CONFLICT (name) DO NOTHING;

-- ============================================================================
-- End of Schema
-- ============================================================================
