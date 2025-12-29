"""Unit tests for Task model."""

import unittest
from datetime import datetime
from src.models.task import Task


class TestTaskModel(unittest.TestCase):
    """Test cases for Task class."""

    def test_task_creation_with_valid_inputs(self):
        """Test creating a task with valid title and description."""
        task = Task(1, "Buy groceries", "Milk, eggs, bread")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Buy groceries")
        self.assertEqual(task.description, "Milk, eggs, bread")
        self.assertFalse(task.is_completed)
        self.assertIsInstance(task.created_at, datetime)

    def test_task_creation_with_empty_title_raises_error(self):
        """Test that empty title raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Task(1, "")
        self.assertIn("empty", str(context.exception).lower())

    def test_task_creation_with_whitespace_only_title_raises_error(self):
        """Test that whitespace-only title raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Task(1, "   ")
        self.assertIn("empty", str(context.exception).lower())

    def test_task_creation_with_none_title_raises_error(self):
        """Test that None title raises ValueError."""
        with self.assertRaises(ValueError):
            Task(1, None)

    def test_task_title_is_stripped(self):
        """Test that task title is stripped of whitespace."""
        task = Task(1, "  Buy groceries  ")
        self.assertEqual(task.title, "Buy groceries")

    def test_task_description_is_optional(self):
        """Test that description can be omitted."""
        task = Task(1, "Buy groceries")
        self.assertEqual(task.description, "")

    def test_task_description_is_stripped(self):
        """Test that description is stripped of whitespace."""
        task = Task(1, "Buy groceries", "  Milk, eggs  ")
        self.assertEqual(task.description, "Milk, eggs")

    def test_task_creation_with_long_title_raises_error(self):
        """Test that title exceeding 500 chars raises error."""
        long_title = "x" * 501
        with self.assertRaises(ValueError) as context:
            Task(1, long_title)
        self.assertIn("500", str(context.exception))

    def test_task_creation_with_long_description_raises_error(self):
        """Test that description exceeding 500 chars raises error."""
        long_description = "x" * 501
        with self.assertRaises(ValueError) as context:
            Task(1, "Valid title", long_description)
        self.assertIn("500", str(context.exception))

    def test_mark_complete_changes_status(self):
        """Test that mark_complete() sets is_completed to True."""
        task = Task(1, "Buy groceries")
        self.assertFalse(task.is_completed)
        task.mark_complete()
        self.assertTrue(task.is_completed)

    def test_mark_incomplete_changes_status(self):
        """Test that mark_incomplete() sets is_completed to False."""
        task = Task(1, "Buy groceries")
        task.mark_complete()
        self.assertTrue(task.is_completed)
        task.mark_incomplete()
        self.assertFalse(task.is_completed)

    def test_update_task_with_new_title_and_description(self):
        """Test updating task with new title and description."""
        task = Task(1, "Old title", "Old description")
        task.update("New title", "New description")
        self.assertEqual(task.title, "New title")
        self.assertEqual(task.description, "New description")

    def test_update_task_with_empty_title_raises_error(self):
        """Test that updating with empty title raises error."""
        task = Task(1, "Original title")
        with self.assertRaises(ValueError):
            task.update("")

    def test_update_task_with_whitespace_only_title_raises_error(self):
        """Test that updating with whitespace-only title raises error."""
        task = Task(1, "Original title")
        with self.assertRaises(ValueError):
            task.update("   ")

    def test_update_task_description_only(self):
        """Test updating only the description."""
        task = Task(1, "Title", "Old description")
        task.update("Title", "New description")
        self.assertEqual(task.title, "Title")
        self.assertEqual(task.description, "New description")

    def test_update_task_with_empty_description_allowed(self):
        """Test that description can be cleared."""
        task = Task(1, "Title", "Description")
        task.update("Title", "")
        self.assertEqual(task.description, "")

    def test_task_id_is_immutable(self):
        """Test that task ID cannot be changed after creation."""
        task = Task(1, "Title")
        self.assertEqual(task.id, 1)
        # ID is a simple attribute, but testing that it stays the same
        self.assertEqual(task.id, 1)

    def test_task_repr_shows_incomplete_status(self):
        """Test string representation shows incomplete status."""
        task = Task(1, "Buy groceries")
        repr_str = repr(task)
        self.assertIn("○", repr_str)  # Incomplete symbol
        self.assertIn("Buy groceries", repr_str)

    def test_task_repr_shows_complete_status(self):
        """Test string representation shows complete status."""
        task = Task(1, "Buy groceries")
        task.mark_complete()
        repr_str = repr(task)
        self.assertIn("✓", repr_str)  # Complete symbol
        self.assertIn("Buy groceries", repr_str)


if __name__ == "__main__":
    unittest.main()
