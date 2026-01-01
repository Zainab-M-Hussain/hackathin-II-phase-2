/**
 * Task API service
 * Task-specific API methods that call backend endpoints
 */

import { apiClient } from './api';
import {
  Task,
  TaskListResponse,
  TaskCreateRequest,
  TaskUpdateRequest,
  TaskStatusUpdateRequest,
} from '@/types/task';

export const taskApi = {
  /**
   * List tasks with optional filtering, searching, sorting, and pagination
   */
  list: async (params?: {
    skip?: number;
    limit?: number;
    status?: string;
    priority?: string;
    tags?: string;
    search?: string;
    sort_by?: string;
    sort_order?: string;
  }): Promise<TaskListResponse> => {
    return apiClient.get<TaskListResponse>('/tasks', { params });
  },

  /**
   * Get a single task by ID
   */
  get: async (id: number): Promise<Task> => {
    return apiClient.get<Task>(`/tasks/${id}`);
  },

  /**
   * Create a new task
   */
  create: async (data: TaskCreateRequest): Promise<Task> => {
    return apiClient.post<Task>('/tasks', data);
  },

  /**
   * Update an existing task
   */
  update: async (id: number, data: TaskUpdateRequest): Promise<Task> => {
    return apiClient.put<Task>(`/tasks/${id}`, data);
  },

  /**
   * Update task status (complete, archive, etc.)
   */
  updateStatus: async (
    id: number,
    data: TaskStatusUpdateRequest
  ): Promise<Task> => {
    return apiClient.patch<Task>(`/tasks/${id}/status`, data);
  },

  /**
   * Delete a task
   */
  delete: async (id: number): Promise<void> => {
    return apiClient.delete(`/tasks/${id}`);
  },

  /**
   * Get task statistics
   */
  getStats: async (): Promise<any> => {
    return apiClient.get('/tasks/stats/summary');
  },
};
