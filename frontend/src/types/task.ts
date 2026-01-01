/**
 * TypeScript types for Phase II Todo Application
 * Mirrors backend SQLModel schemas for type safety
 */

export enum TaskStatus {
  PENDING = "pending",
  COMPLETE = "complete",
  ARCHIVED = "archived"
}

export enum TaskPriority {
  LOW = "LOW",
  MEDIUM = "MEDIUM",
  HIGH = "HIGH"
}

export interface Tag {
  id: number;
  name: string;
  created_at: string;
}

export interface Task {
  id: number;
  title: string;
  description?: string;
  priority: TaskPriority;
  status: TaskStatus;
  due_date?: string;
  created_at: string;
  updated_at: string;
  tags: Tag[];
}

export interface TaskCreateRequest {
  title: string;
  description?: string;
  priority?: TaskPriority;
  due_date?: string;
  tags?: number[];
}

export interface TaskUpdateRequest {
  title?: string;
  description?: string;
  priority?: TaskPriority;
  due_date?: string;
  tags?: number[];
}

export interface TaskStatusUpdateRequest {
  status: TaskStatus;
  reason?: string;
}

// API Response types
export interface TaskListResponse {
  items: Task[];
  total: number;
  skip: number;
  limit: number;
}

export interface ErrorResponse {
  error_code: string;
  error_type: string;
  detail: string;
  timestamp: string;
  path: string;
}

// Filter state
export interface FilterState {
  status?: TaskStatus | null;
  priority?: TaskPriority | null;
  tags?: number[] | null;
}

// Component props
export interface TaskCardProps {
  task: Task;
  onStatusChange?: () => void;
  onDelete?: () => void;
}

export interface TaskListProps {
  onTaskCreated?: () => void;
}

export interface TaskFormProps {
  onSubmit: (task: TaskCreateRequest) => Promise<void>;
  isLoading?: boolean;
  initialTask?: Task;
}
