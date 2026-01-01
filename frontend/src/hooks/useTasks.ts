/**
 * SWR hook for fetching tasks with polling for multi-tab synchronization
 * Revalidates every 5-10 seconds to keep all tabs in sync
 */

import useSWR, { SWRConfiguration } from 'swr';
import { taskApi } from '@/services/taskApi';
import { Task, TaskListResponse, TaskStatus, TaskPriority } from '@/types/task';

interface UseTasksOptions {
  skip?: number;
  limit?: number;
  status?: TaskStatus | null;
  priority?: TaskPriority | null;
  tags?: string;
  search?: string;
  sort_by?: string;
  sort_order?: string;
  pollingInterval?: number;
}

/**
 * Hook for fetching and syncing tasks across tabs
 * Uses SWR with 5-second polling for eventual consistency
 */
export function useTasks({
  skip = 0,
  limit = 50,
  status = null,
  priority = null,
  tags,
  search,
  sort_by = 'created_at',
  sort_order = 'desc',
  pollingInterval = 5000,
}: UseTasksOptions = {}) {
  // Build query parameters
  const params = {
    skip,
    limit,
    ...(status && { status }),
    ...(priority && { priority }),
    ...(tags && { tags }),
    ...(search && { search }),
    sort_by,
    sort_order,
  };

  // Build URL for SWR key
  const queryString = new URLSearchParams(
    params as Record<string, string>
  ).toString();
  const url = `/tasks?${queryString}`;

  // SWR configuration for multi-tab sync
  const swrConfig: SWRConfiguration = {
    revalidateOnFocus: true, // Revalidate when browser gains focus (multi-tab)
    revalidateOnReconnect: true, // Revalidate on network reconnect
    dedupingInterval: 2000, // Don't fetch twice in 2s window
    focusThrottleInterval: 5000, // Min 5s between focus revalidations
    refreshInterval: pollingInterval, // 5-10s polling for eventual consistency
    errorRetryCount: 3, // Retry failed requests 3 times
    errorRetryInterval: 1000, // Wait 1s between retries
  };

  const { data, error, isLoading, isValidating, mutate } =
    useSWR<TaskListResponse>(url, () => taskApi.list(params), swrConfig);

  return {
    tasks: data?.items || [],
    total: data?.total || 0,
    skip: data?.skip || skip,
    limit: data?.limit || limit,
    isLoading,
    isValidating,
    error,
    mutate, // Manual revalidation trigger
  };
}

/**
 * Hook for fetching a single task
 */
export function useTask(taskId: number | null) {
  const { data, error, isLoading, mutate } = useSWR(
    taskId ? `/tasks/${taskId}` : null,
    taskId ? () => taskApi.get(taskId) : null,
    {
      revalidateOnFocus: true,
      refreshInterval: 5000,
    }
  );

  return {
    task: data || null,
    isLoading,
    error,
    mutate,
  };
}

/**
 * Hook for task mutations (create, update, delete)
 */
export function useMutations() {
  const createTask = async (task: any) => {
    return taskApi.create(task);
  };

  const updateTask = async (id: number, task: any) => {
    return taskApi.update(id, task);
  };

  const updateStatus = async (id: number, status: string, reason?: string) => {
    return taskApi.updateStatus(id, { status: status as any, reason });
  };

  const deleteTask = async (id: number) => {
    return taskApi.delete(id);
  };

  return {
    createTask,
    updateTask,
    updateStatus,
    deleteTask,
  };
}
