/**
 * Unit tests for useTasks hook
 */

import { renderHook, waitFor } from '@testing-library/react';
import useSWR from 'swr';
import { useTasks, useMutations } from '@/hooks/useTasks';
import * as taskApi from '@/services/taskApi';

// Mock SWR
jest.mock('swr');

// Mock task API
jest.mock('@/services/taskApi', () => ({
  taskApi: {
    list: jest.fn(),
    get: jest.fn(),
    create: jest.fn(),
    update: jest.fn(),
    updateStatus: jest.fn(),
    delete: jest.fn(),
  },
}));

describe('useTasks Hook', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should fetch tasks with default options', () => {
    const mockTasks = {
      items: [
        { id: 1, title: 'Task 1', status: 'pending', priority: 'MEDIUM' },
        { id: 2, title: 'Task 2', status: 'complete', priority: 'HIGH' },
      ],
      total: 2,
      skip: 0,
      limit: 50,
    };

    (useSWR as jest.Mock).mockReturnValue({
      data: mockTasks,
      error: null,
      isLoading: false,
      isValidating: false,
      mutate: jest.fn(),
    });

    const { result } = renderHook(() => useTasks());

    expect(result.current.tasks).toEqual(mockTasks.items);
    expect(result.current.total).toBe(2);
    expect(result.current.isLoading).toBe(false);
  });

  it('should handle loading state', () => {
    (useSWR as jest.Mock).mockReturnValue({
      data: undefined,
      error: null,
      isLoading: true,
      isValidating: false,
      mutate: jest.fn(),
    });

    const { result } = renderHook(() => useTasks());

    expect(result.current.isLoading).toBe(true);
    expect(result.current.tasks).toEqual([]);
  });

  it('should handle errors', () => {
    const mockError = new Error('API Error');
    (useSWR as jest.Mock).mockReturnValue({
      data: undefined,
      error: mockError,
      isLoading: false,
      isValidating: false,
      mutate: jest.fn(),
    });

    const { result } = renderHook(() => useTasks());

    expect(result.current.error).toBe(mockError);
    expect(result.current.tasks).toEqual([]);
  });

  it('should apply filters', () => {
    const mockTasks = {
      items: [{ id: 1, title: 'Pending Task', status: 'pending', priority: 'HIGH' }],
      total: 1,
      skip: 0,
      limit: 50,
    };

    (useSWR as jest.Mock).mockReturnValue({
      data: mockTasks,
      error: null,
      isLoading: false,
      isValidating: false,
      mutate: jest.fn(),
    });

    const { result } = renderHook(() =>
      useTasks({ status: 'pending', priority: 'HIGH' })
    );

    expect(result.current.tasks).toEqual(mockTasks.items);
  });

  it('should support pagination', () => {
    const mockTasks = {
      items: [{ id: 51, title: 'Task 51', status: 'pending', priority: 'MEDIUM' }],
      total: 100,
      skip: 50,
      limit: 50,
    };

    (useSWR as jest.Mock).mockReturnValue({
      data: mockTasks,
      error: null,
      isLoading: false,
      isValidating: false,
      mutate: jest.fn(),
    });

    const { result } = renderHook(() => useTasks({ skip: 50, limit: 50 }));

    expect(result.current.skip).toBe(50);
    expect(result.current.limit).toBe(50);
  });

  it('should support search', () => {
    const mockTasks = {
      items: [{ id: 1, title: 'Buy groceries', status: 'pending', priority: 'MEDIUM' }],
      total: 1,
      skip: 0,
      limit: 50,
    };

    (useSWR as jest.Mock).mockReturnValue({
      data: mockTasks,
      error: null,
      isLoading: false,
      isValidating: false,
      mutate: jest.fn(),
    });

    const { result } = renderHook(() => useTasks({ search: 'groceries' }));

    expect(result.current.tasks[0].title).toContain('groceries');
  });

  it('should support sorting', () => {
    const mockTasks = {
      items: [
        { id: 1, title: 'A Task', status: 'pending', priority: 'MEDIUM' },
        { id: 2, title: 'B Task', status: 'pending', priority: 'MEDIUM' },
      ],
      total: 2,
      skip: 0,
      limit: 50,
    };

    (useSWR as jest.Mock).mockReturnValue({
      data: mockTasks,
      error: null,
      isLoading: false,
      isValidating: false,
      mutate: jest.fn(),
    });

    const { result } = renderHook(() =>
      useTasks({ sort_by: 'title', sort_order: 'asc' })
    );

    expect(result.current.tasks[0].title).toBe('A Task');
    expect(result.current.tasks[1].title).toBe('B Task');
  });
});

describe('useMutations Hook', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should create task', async () => {
    const mockTask = { id: 1, title: 'New Task', status: 'pending', priority: 'MEDIUM' };
    (taskApi.taskApi.create as jest.Mock).mockResolvedValue(mockTask);

    const { result } = renderHook(() => useMutations());

    const newTask = await result.current.createTask({
      title: 'New Task',
      priority: 'MEDIUM',
    });

    expect(newTask).toEqual(mockTask);
    expect(taskApi.taskApi.create).toHaveBeenCalledWith({
      title: 'New Task',
      priority: 'MEDIUM',
    });
  });

  it('should update task', async () => {
    const mockTask = { id: 1, title: 'Updated Task', status: 'pending', priority: 'HIGH' };
    (taskApi.taskApi.update as jest.Mock).mockResolvedValue(mockTask);

    const { result } = renderHook(() => useMutations());

    const updated = await result.current.updateTask(1, {
      title: 'Updated Task',
      priority: 'HIGH',
    });

    expect(updated).toEqual(mockTask);
  });

  it('should update task status', async () => {
    const mockTask = { id: 1, title: 'Task', status: 'complete', priority: 'MEDIUM' };
    (taskApi.taskApi.updateStatus as jest.Mock).mockResolvedValue(mockTask);

    const { result } = renderHook(() => useMutations());

    const updated = await result.current.updateStatus(1, 'complete');

    expect(updated.status).toBe('complete');
  });

  it('should delete task', async () => {
    (taskApi.taskApi.delete as jest.Mock).mockResolvedValue(undefined);

    const { result } = renderHook(() => useMutations());

    await result.current.deleteTask(1);

    expect(taskApi.taskApi.delete).toHaveBeenCalledWith(1);
  });
});
