/**
 * EmptyState Component - Empty state message
 */

import React from 'react';

interface EmptyStateProps {
  title?: string;
  message?: string;
  icon?: string;
}

export default function EmptyState({
  title = 'No Tasks Found',
  message = 'Create a task to get started',
  icon = '📝',
}: EmptyStateProps) {
  return (
    <div
      style={{
        textAlign: 'center',
        padding: '60px 20px',
        color: '#999',
      }}
    >
      <div style={{ fontSize: '48px', marginBottom: '15px' }}>{icon}</div>
      <h3 style={{ margin: '0 0 10px 0', color: '#666' }}>{title}</h3>
      <p style={{ margin: 0 }}>{message}</p>
    </div>
  );
}
