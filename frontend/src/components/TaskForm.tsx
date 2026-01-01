/**
 * TaskForm Component - Create new task form
 */

import React, { useState } from 'react';
import { TaskPriority } from '@/types/task';

interface TaskFormProps {
  onSubmit: (title: string, priority: string) => Promise<void>;
  isLoading?: boolean;
}

export default function TaskForm({ onSubmit, isLoading = false }: TaskFormProps) {
  const [title, setTitle] = useState('');
  const [priority, setPriority] = useState(TaskPriority.MEDIUM);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setIsSubmitting(true);
    try {
      await onSubmit(title, priority);
      setTitle('');
      setPriority(TaskPriority.MEDIUM);
    } finally {
      setIsSubmitting(false);
    }
  };

  const isDisabled = isSubmitting || isLoading || !title.trim();

  return (
    <section style={{ marginBottom: '30px', padding: '20px', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
      <h2>Create Task</h2>
      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
        <input
          type="text"
          placeholder="Enter task title..."
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          disabled={isSubmitting || isLoading}
          style={{
            flex: 1,
            minWidth: '200px',
            padding: '10px',
            fontSize: '14px',
            border: '1px solid #ddd',
            borderRadius: '4px',
          }}
        />

        <select
          value={priority}
          onChange={(e) => setPriority(e.target.value)}
          disabled={isSubmitting || isLoading}
          style={{
            padding: '10px',
            fontSize: '14px',
            border: '1px solid #ddd',
            borderRadius: '4px',
          }}
        >
          <option value={TaskPriority.LOW}>Low Priority</option>
          <option value={TaskPriority.MEDIUM}>Medium Priority</option>
          <option value={TaskPriority.HIGH}>High Priority</option>
        </select>

        <button
          type="submit"
          disabled={isDisabled}
          style={{
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: isDisabled ? 'not-allowed' : 'pointer',
            opacity: isDisabled ? 0.5 : 1,
          }}
        >
          {isSubmitting ? 'Creating...' : 'Create'}
        </button>
      </form>
    </section>
  );
}
