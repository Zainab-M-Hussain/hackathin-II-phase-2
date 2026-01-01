/**
 * FilterBar Component - Search, filter, and sort controls
 */

import React from 'react';
import { TaskStatus } from '@/types/task';

interface FilterBarProps {
  search: string;
  onSearchChange: (value: string) => void;
  status: string | null;
  onStatusChange: (value: string | null) => void;
  sortBy: string;
  onSortByChange: (value: string) => void;
  sortOrder: 'asc' | 'desc';
  onSortOrderChange: (value: 'asc' | 'desc') => void;
  onClearFilters: () => void;
  hasActiveFilters: boolean;
}

export default function FilterBar({
  search,
  onSearchChange,
  status,
  onStatusChange,
  sortBy,
  onSortByChange,
  sortOrder,
  onSortOrderChange,
  onClearFilters,
  hasActiveFilters,
}: FilterBarProps) {
  return (
    <section style={{ marginBottom: '20px', padding: '15px', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
      <h3>Filters & Search</h3>
      <div style={{ display: 'flex', gap: '15px', flexWrap: 'wrap', alignItems: 'center' }}>
        <input
          type="text"
          placeholder="Search tasks..."
          value={search}
          onChange={(e) => onSearchChange(e.target.value)}
          style={{
            padding: '8px',
            fontSize: '14px',
            border: '1px solid #ddd',
            borderRadius: '4px',
            minWidth: '200px',
          }}
        />

        <select
          value={status || ''}
          onChange={(e) => onStatusChange(e.target.value || null)}
          style={{
            padding: '8px',
            fontSize: '14px',
            border: '1px solid #ddd',
            borderRadius: '4px',
          }}
        >
          <option value="">All Status</option>
          <option value={TaskStatus.PENDING}>Pending</option>
          <option value={TaskStatus.COMPLETE}>Complete</option>
          <option value={TaskStatus.ARCHIVED}>Archived</option>
        </select>

        <select
          value={sortBy}
          onChange={(e) => onSortByChange(e.target.value)}
          style={{
            padding: '8px',
            fontSize: '14px',
            border: '1px solid #ddd',
            borderRadius: '4px',
          }}
        >
          <option value="created_at">Created Date</option>
          <option value="due_date">Due Date</option>
          <option value="priority">Priority</option>
          <option value="title">Title</option>
        </select>

        <select
          value={sortOrder}
          onChange={(e) => onSortOrderChange(e.target.value as 'asc' | 'desc')}
          style={{
            padding: '8px',
            fontSize: '14px',
            border: '1px solid #ddd',
            borderRadius: '4px',
          }}
        >
          <option value="desc">Descending</option>
          <option value="asc">Ascending</option>
        </select>

        {hasActiveFilters && (
          <button
            onClick={onClearFilters}
            style={{
              padding: '8px 15px',
              backgroundColor: '#6c757d',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
          >
            Clear Filters
          </button>
        )}
      </div>
    </section>
  );
}
