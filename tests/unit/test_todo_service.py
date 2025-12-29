"""Unit tests for TodoService."""

import unittest
from src.services.todo_service import TodoService


class TestTodoService(unittest.TestCase):
    """Test cases for TodoService class."""

    def setUp(self):
        """Set up a fresh TodoService for each test."""
        self.service = TodoService()

    def test_add_task_returns_task_object(self):
        """Test that add_task returns a Task object."""
        task = self.service.add_task("Buy groceries")
        self.assertEqual(task.title, "Buy groceries")
        self.assertFalse(task.is_completed)

    def test_add_task_with_description(self):
        """Test adding a task with description."""
        task = self.service.add_task("Buy groceries", "Milk, eggs, bread")
        self.assertEqual(task.title, "Buy groceries")
        self.assertEqual(task.description, "Milk, eggs, bread")

    def test_add_task_auto_increments_id(self):
        """Test that task IDs are auto-incremented."""
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")
        task3 = self.service.add_task("Task 3")

        self.assertEqual(task1.id, 1)
        self.assertEqual(task2.id, 2)
        self.assertEqual(task3.id, 3)

    def test_add_task_with_invalid_title_raises_error(self):
        """Test that invalid title raises ValueError."""
        with self.assertRaises(ValueError):
            self.service.add_task("")

        with self.assertRaises(ValueError):
            self.service.add_task("   ")

    def test_get_all_tasks_returns_empty_list_initially(self):
        """Test that get_all_tasks returns empty list when no tasks."""
        tasks = self.service.get_all_tasks()
        self.assertEqual(tasks, [])

    def test_get_all_tasks_returns_all_tasks(self):
        """Test that get_all_tasks returns all added tasks."""
        self.service.add_task("Task 1")
        self.service.add_task("Task 2")
        self.service.add_task("Task 3")

        tasks = self.service.get_all_tasks()
        self.assertEqual(len(tasks), 3)

    def test_get_all_tasks_returns_copy(self):
        """Test that get_all_tasks returns a copy, not reference."""
        self.service.add_task("Task 1")
        tasks1 = self.service.get_all_tasks()
        tasks2 = self.service.get_all_tasks()

        # Should be different objects
        self.assertIsNot(tasks1, tasks2)

    def test_get_task_returns_task_by_id(self):
        """Test that get_task returns correct task by ID."""
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")

        found_task = self.service.get_task(2)
        self.assertEqual(found_task.id, 2)
        self.assertEqual(found_task.title, "Task 2")

    def test_get_task_returns_none_for_non_existent_id(self):
        """Test that get_task returns None for non-existent ID."""
        self.service.add_task("Task 1")
        found_task = self.service.get_task(999)
        self.assertIsNone(found_task)

    def test_update_task_modifies_existing_task(self):
        """Test that update_task changes title and description."""
        self.service.add_task("Old title", "Old description")
        updated_task = self.service.update_task(1, "New title", "New description")

        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(updated_task.description, "New description")

    def test_update_task_non_existent_raises_error(self):
        """Test that updating non-existent task raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.service.update_task(999, "New title")
        self.assertIn("not found", str(context.exception).lower())

    def test_update_task_invalid_title_raises_error(self):
        """Test that updating with invalid title raises error."""
        self.service.add_task("Original")
        with self.assertRaises(ValueError):
            self.service.update_task(1, "")

    def test_delete_task_removes_task(self):
        """Test that delete_task removes the task."""
        self.service.add_task("Task to delete")
        initial_count = len(self.service.get_all_tasks())
        self.assertEqual(initial_count, 1)

        success = self.service.delete_task(1)
        self.assertTrue(success)

        final_count = len(self.service.get_all_tasks())
        self.assertEqual(final_count, 0)

    def test_delete_task_returns_false_for_non_existent(self):
        """Test that delete_task returns False for non-existent ID."""
        success = self.service.delete_task(999)
        self.assertFalse(success)

    def test_delete_task_does_not_affect_other_tasks(self):
        """Test that deleting one task doesn't affect others."""
        self.service.add_task("Task 1")
        self.service.add_task("Task 2")
        self.service.add_task("Task 3")

        self.service.delete_task(2)

        tasks = self.service.get_all_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].id, 1)
        self.assertEqual(tasks[1].id, 3)

    def test_mark_complete_changes_status(self):
        """Test that mark_complete sets is_completed to True."""
        self.service.add_task("Task")
        success = self.service.mark_complete(1)

        self.assertTrue(success)
        task = self.service.get_task(1)
        self.assertTrue(task.is_completed)

    def test_mark_complete_non_existent_returns_false(self):
        """Test that mark_complete returns False for non-existent ID."""
        success = self.service.mark_complete(999)
        self.assertFalse(success)

    def test_mark_incomplete_changes_status(self):
        """Test that mark_incomplete sets is_completed to False."""
        self.service.add_task("Task")
        self.service.mark_complete(1)
        success = self.service.mark_incomplete(1)

        self.assertTrue(success)
        task = self.service.get_task(1)
        self.assertFalse(task.is_completed)

    def test_mark_incomplete_non_existent_returns_false(self):
        """Test that mark_incomplete returns False for non-existent ID."""
        success = self.service.mark_incomplete(999)
        self.assertFalse(success)

    def test_multiple_tasks_independence(self):
        """Test that multiple tasks remain independent."""
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")
        task3 = self.service.add_task("Task 3")

        # Mark task1 and task3 complete
        self.service.mark_complete(1)
        self.service.mark_complete(3)

        # task2 should still be incomplete
        self.assertTrue(self.service.get_task(1).is_completed)
        self.assertFalse(self.service.get_task(2).is_completed)
        self.assertTrue(self.service.get_task(3).is_completed)

    def test_task_list_maintains_creation_order(self):
        """Test that tasks are returned in creation order."""
        self.service.add_task("First")
        self.service.add_task("Second")
        self.service.add_task("Third")

        tasks = self.service.get_all_tasks()
        self.assertEqual(tasks[0].title, "First")
        self.assertEqual(tasks[1].title, "Second")
        self.assertEqual(tasks[2].title, "Third")


if __name__ == "__main__":
    unittest.main()
