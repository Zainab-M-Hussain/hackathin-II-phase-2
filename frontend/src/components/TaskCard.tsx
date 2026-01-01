/**
 * TaskCard Component - Individual task display with actions
 */

import React from 'react';
import { Task, TaskStatus } from '@/types/task';

interface TaskCardProps {
  task: Task;
  onToggleStatus: (task: Task) => void;
  onDelete: (taskId: number) => void;
  isLoading?: boolean;
}

export default function TaskCard({ task, onToggleStatus, onDelete, isLoading = false }: TaskCardProps) {
  const isComplete = task.status === TaskStatus.COMPLETE;

  return (
    <div
      style={{
        padding: '15px',
        marginBottom: '10px',
        border: '1px solid #ddd',
        borderRadius: '4px',
        backgroundColor: isComplete ? '#f0f0f0' : '#fff',
        display: 'flex',
        gap: '15px',
        alignItems: 'flex-start',
        opacity: isLoading ? 0.6 : 1,
        pointerEvents: isLoading ? 'none' : 'auto',
      }}
    >
      {/* Checkbox */}
      <input
        type="checkbox"
        checked={isComplete}
        onChange={() => onToggleStatus(task)}
        disabled={isLoading}
        style={{ marginTop: '2px', cursor: 'pointer' }}
      />

      {/* Task Info */}
      <div style={{ flex: 1 }}>
        <h4
          style={{
            margin: '0 0 5px 0',
            textDecoration: isComplete ? 'line-through' : 'none',
            color: isComplete ? '#999' : '#000',
          }}
        >
          {task.title}
        </h4>
        {task.description && (
          <p style={{ margin: '5px 0', fontSize: '14px', color: '#666' }}>
            {task.description}
          </p>
        )}
        <div style={{ fontSize: '12px', color: '#999', marginTop: '5px' }}>
          <span style={{ marginRight: '15px' }}>
            Priority: <strong>{task.priority}</strong>
          </span>
          {task.due_date && (
            <span>
              Due: <strong>{new Date(task.due_date).toLocaleDateString()}</strong>
            </span>
          )}
          {task.tags && task.tags.length > 0 && (
            <div style={{ marginTop: '5px' }}>
              Tags: {task.tags.map((tag) => tag.name || tag).join(', ')}
            </div>
          )}
        </div>
      </div>

      {/* Delete Button */}
      <button
        onClick={() => onDelete(task.id)}
        disabled={isLoading}
        style={{
          padding: '5px 10px',
          backgroundColor: '#dc3545',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: isLoading ? 'default' : 'pointer',
          fontSize: '12px',
          opacity: isLoading ? 0.6 : 1,
        }}
      >
        Delete
      </button>
    </div>
  );
}
