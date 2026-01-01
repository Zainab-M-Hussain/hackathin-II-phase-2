/**
 * Dashboard Page - Main page for Phase II Todo Application
 * Modern, Beautiful UI with improved styling
 */

import React, { useState, useEffect } from 'react';
import { useTasks, useMutations } from '@/hooks/useTasks';
import { Task, TaskCreateRequest, TaskStatus, TaskPriority, FilterState } from '@/types/task';
import styles from '@/styles/Dashboard.module.css';

export default function Dashboard() {
  const [mounted, setMounted] = useState(false);
  const [filters, setFilters] = useState<FilterState>({});
  const [search, setSearch] = useState('');
  const [sortBy, setSortBy] = useState('created_at');
  const [sortOrder, setSortOrder] = useState('desc');
  const [page, setPage] = useState(0);
  const [isCreating, setIsCreating] = useState(false);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');
  const [newTaskPriority, setNewTaskPriority] = useState(TaskPriority.MEDIUM);

  useEffect(() => {
    setMounted(true);
  }, []);

  const { tasks, total, isLoading, mutate } = useTasks({
    skip: page * 50,
    limit: 50,
    status: filters.status || undefined,
    priority: filters.priority || undefined,
    search: search || undefined,
    sort_by: sortBy,
    sort_order: sortOrder as 'asc' | 'desc',
  });

  const { createTask, updateStatus, deleteTask } = useMutations();

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return;

    setIsCreating(true);
    try {
      await createTask({
        title: newTaskTitle,
        description: newTaskDescription || undefined,
        priority: newTaskPriority,
      });
      setNewTaskTitle('');
      setNewTaskDescription('');
      setNewTaskPriority(TaskPriority.MEDIUM);
      await mutate();
    } catch (error) {
      console.error('Failed to create task:', error);
    } finally {
      setIsCreating(false);
    }
  };

  const handleToggleStatus = async (task: Task) => {
    try {
      const newStatus =
        task.status === TaskStatus.PENDING
          ? TaskStatus.COMPLETE
          : TaskStatus.PENDING;
      await updateStatus(task.id, newStatus);
      await mutate();
    } catch (error) {
      console.error('Failed to update task:', error);
    }
  };

  const handleDelete = async (taskId: number) => {
    if (!confirm('Are you sure you want to delete this task?')) return;
    try {
      await deleteTask(taskId);
      await mutate();
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  };

  const getTasksByStatus = () => {
    const completed = tasks.filter(t => t.status === TaskStatus.COMPLETE).length;
    const pending = tasks.filter(t => t.status === TaskStatus.PENDING).length;
    return { completed, pending };
  };

  const { completed, pending } = getTasksByStatus();

  if (!mounted) {
    return <div className={styles.loadingContainer}>Loading...</div>;
  }

  return (
    <div className={styles.container}>
      {/* Header */}
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <div>
            <h1 className={styles.title}>✨ Todo Dashboard</h1>
            <p className={styles.subtitle}>Stay organized and productive with Phase II</p>
          </div>
          <div className={styles.statsContainer}>
            <div className={styles.statCard}>
              <div className={styles.statNumber}>{total}</div>
              <div className={styles.statLabel}>Total Tasks</div>
            </div>
            <div className={styles.statCard}>
              <div className={styles.statNumber} style={{ color: '#10B981' }}>{completed}</div>
              <div className={styles.statLabel}>Completed</div>
            </div>
            <div className={styles.statCard}>
              <div className={styles.statNumber} style={{ color: '#F59E0B' }}>{pending}</div>
              <div className={styles.statLabel}>Pending</div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className={styles.main}>
        {/* Create Task Form */}
        <section className={styles.createSection}>
          <h2 className={styles.sectionTitle}>➕ Create New Task</h2>
          <form onSubmit={handleCreateTask} className={styles.form}>
            <div className={styles.formGroup}>
              <input
                type="text"
                placeholder="What needs to be done?"
                value={newTaskTitle}
                onChange={(e) => setNewTaskTitle(e.target.value)}
                disabled={isCreating}
                className={styles.titleInput}
              />
            </div>

            <div className={styles.formRow}>
              <textarea
                placeholder="Add a description (optional)"
                value={newTaskDescription}
                onChange={(e) => setNewTaskDescription(e.target.value)}
                disabled={isCreating}
                className={styles.descriptionInput}
                rows={2}
              />

              <select
                value={newTaskPriority}
                onChange={(e) => setNewTaskPriority(e.target.value as TaskPriority)}
                disabled={isCreating}
                className={styles.prioritySelect}
              >
                <option value={TaskPriority.LOW}>Low Priority</option>
                <option value={TaskPriority.MEDIUM}>Medium Priority</option>
                <option value={TaskPriority.HIGH}>High Priority</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={isCreating || !newTaskTitle.trim()}
              className={styles.submitButton}
            >
              {isCreating ? '⏳ Creating...' : '➕ Add Task'}
            </button>
          </form>
        </section>

        {/* Filters Section */}
        <section className={styles.filterSection}>
          <h2 className={styles.sectionTitle}>🔍 Filter & Search</h2>
          <div className={styles.filterGrid}>
            <input
              type="text"
              placeholder="Search tasks..."
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setPage(0);
              }}
              className={styles.searchInput}
            />

            <select
              value={filters.status || ''}
              onChange={(e) => {
                setFilters({ ...filters, status: e.target.value as any || null });
                setPage(0);
              }}
              className={styles.filterSelect}
            >
              <option value="">All Status</option>
              <option value="pending">Pending</option>
              <option value="complete">Completed</option>
              <option value="archived">Archived</option>
            </select>

            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className={styles.filterSelect}
            >
              <option value="created_at">Created Date</option>
              <option value="due_date">Due Date</option>
              <option value="priority">Priority</option>
              <option value="title">Title</option>
            </select>

            <select
              value={sortOrder}
              onChange={(e) => setSortOrder(e.target.value)}
              className={styles.filterSelect}
            >
              <option value="desc">Newest First</option>
              <option value="asc">Oldest First</option>
            </select>

            {(search || filters.status) && (
              <button
                onClick={() => {
                  setFilters({});
                  setSearch('');
                  setPage(0);
                }}
                className={styles.clearButton}
              >
                ✕ Clear Filters
              </button>
            )}
          </div>
        </section>

        {/* Task List Section */}
        <section className={styles.taskSection}>
          <h2 className={styles.sectionTitle}>📋 Tasks ({total})</h2>

          {isLoading ? (
            <div className={styles.emptyState}>
              <div className={styles.spinner}></div>
              <p>Loading your tasks...</p>
            </div>
          ) : tasks.length === 0 ? (
            <div className={styles.emptyState}>
              <p style={{ fontSize: '3rem' }}>🎉</p>
              <p>No tasks found. Create one to get started!</p>
            </div>
          ) : (
            <div className={styles.taskList}>
              {tasks.map((task) => (
                <div
                  key={task.id}
                  className={`${styles.taskCard} ${
                    task.status === TaskStatus.COMPLETE ? styles.completed : ''
                  }`}
                >
                  {/* Checkbox */}
                  <input
                    type="checkbox"
                    checked={task.status === TaskStatus.COMPLETE}
                    onChange={() => handleToggleStatus(task)}
                    className={styles.checkbox}
                  />

                  {/* Task Content */}
                  <div className={styles.taskContent}>
                    <h3 className={styles.taskTitle}>{task.title}</h3>
                    {task.description && (
                      <p className={styles.taskDescription}>{task.description}</p>
                    )}
                    <div className={styles.taskMeta}>
                      <span className={`${styles.priority} ${styles[`priority${task.priority}`.toLowerCase()]}`}>
                        {task.priority}
                      </span>
                      {task.due_date && (
                        <span className={styles.dueDate}>
                          📅 {new Date(task.due_date).toLocaleDateString()}
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Delete Button */}
                  <button
                    onClick={() => handleDelete(task.id)}
                    className={styles.deleteButton}
                    title="Delete task"
                  >
                    🗑️
                  </button>
                </div>
              ))}
            </div>
          )}

          {/* Pagination */}
          {total > 50 && (
            <div className={styles.pagination}>
              <button
                onClick={() => setPage(Math.max(0, page - 1))}
                disabled={page === 0}
                className={styles.paginationButton}
              >
                ← Previous
              </button>
              <span className={styles.pageInfo}>
                Page {page + 1} of {Math.ceil(total / 50)}
              </span>
              <button
                onClick={() => setPage(page + 1)}
                disabled={(page + 1) * 50 >= total}
                className={styles.paginationButton}
              >
                Next →
              </button>
            </div>
          )}
        </section>
      </main>

      {/* Footer */}
      <footer className={styles.footer}>
        <p>✨ Phase II Full-Stack Todo Application</p>
        <p>Built with Next.js & FastAPI</p>
      </footer>
    </div>
  );
}
