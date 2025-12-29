"""Integration tests for complete todo app workflows."""

import unittest
from src.cli.app import TodoApp
from src.services.todo_service import TodoService


class TestAppWorkflow(unittest.TestCase):
    """Integration tests for complete user workflows."""

    def setUp(self):
        """Set up a fresh app for each test."""
        self.service = TodoService()
        self.app = TodoApp(self.service)

    def test_add_task_workflow(self):
        """Test adding a task and verifying it appears in the list."""
        # Add a task
        task = self.service.add_task("Buy groceries", "Milk, eggs, bread")

        # Verify task was added
        tasks = self.service.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Buy groceries")
        self.assertEqual(tasks[0].description, "Milk, eggs, bread")
        self.assertFalse(tasks[0].is_completed)

    def test_view_tasks_workflow(self):
        """Test viewing tasks after adding multiple tasks."""
        # Add multiple tasks
        self.service.add_task("Task 1", "Description 1")
        self.service.add_task("Task 2")
        self.service.add_task("Task 3", "Description 3")

        # Get all tasks
        tasks = self.service.get_all_tasks()

        # Verify all tasks appear
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0].title, "Task 1")
        self.assertEqual(tasks[1].title, "Task 2")
        self.assertEqual(tasks[2].title, "Task 3")

    def test_mark_task_complete_workflow(self):
        """Test marking task complete and verifying status changes."""
        # Add a task
        task = self.service.add_task("Buy groceries")
        self.assertFalse(task.is_completed)

        # Mark as complete
        self.service.mark_complete(task.id)

        # Verify status changed
        updated_task = self.service.get_task(task.id)
        self.assertTrue(updated_task.is_completed)

        # Verify it shows in list with complete status
        tasks = self.service.get_all_tasks()
        self.assertTrue(tasks[0].is_completed)

    def test_mark_task_incomplete_workflow(self):
        """Test toggling task from complete to incomplete."""
        # Add and complete a task
        task = self.service.add_task("Task")
        self.service.mark_complete(task.id)
        self.assertTrue(self.service.get_task(task.id).is_completed)

        # Mark as incomplete
        self.service.mark_incomplete(task.id)

        # Verify status changed
        updated_task = self.service.get_task(task.id)
        self.assertFalse(updated_task.is_completed)

    def test_update_task_workflow(self):
        """Test updating a task and verifying changes persist."""
        # Add a task
        task = self.service.add_task("Old title", "Old description")
        original_id = task.id

        # Update the task
        self.service.update_task(original_id, "New title", "New description")

        # Verify changes
        updated_task = self.service.get_task(original_id)
        self.assertEqual(updated_task.id, original_id)
        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(updated_task.description, "New description")

    def test_delete_task_workflow(self):
        """Test deleting a task and verifying it's removed."""
        # Add tasks
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")
        task3 = self.service.add_task("Task 3")

        # Delete task 2
        self.service.delete_task(task2.id)

        # Verify it's gone
        tasks = self.service.get_all_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].id, task1.id)
        self.assertEqual(tasks[1].id, task3.id)

    def test_complete_workflow_all_operations(self):
        """Test complete workflow: add → view → update → mark complete → delete."""
        # 1. Add multiple tasks
        task1 = self.service.add_task("Buy groceries", "Milk, eggs, bread")
        task2 = self.service.add_task("Clean house")
        task3 = self.service.add_task("Finish project", "Deadline: Friday")

        # 2. Verify all tasks are present
        tasks = self.service.get_all_tasks()
        self.assertEqual(len(tasks), 3)

        # 3. Mark task1 as complete
        self.service.mark_complete(task1.id)
        self.assertTrue(self.service.get_task(task1.id).is_completed)

        # 4. Update task2
        self.service.update_task(task2.id, "Clean house thoroughly")
        self.assertEqual(self.service.get_task(task2.id).title, "Clean house thoroughly")

        # 5. Mark task3 as complete
        self.service.mark_complete(task3.id)
        self.assertTrue(self.service.get_task(task3.id).is_completed)

        # 6. Delete task2
        self.service.delete_task(task2.id)

        # 7. Verify final state
        tasks = self.service.get_all_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertTrue(tasks[0].is_completed)
        self.assertTrue(tasks[1].is_completed)
        self.assertIsNone(self.service.get_task(task2.id))

    def test_workflow_no_tasks_then_add(self):
        """Test workflow starting with empty list."""
        # Verify empty
        tasks = self.service.get_all_tasks()
        self.assertEqual(len(tasks), 0)

        # Add task
        self.service.add_task("First task")

        # Verify it appears
        tasks = self.service.get_all_tasks()
        self.assertEqual(len(tasks), 1)

    def test_workflow_multiple_updates_same_task(self):
        """Test updating the same task multiple times."""
        task = self.service.add_task("Original")

        # Update 1
        self.service.update_task(task.id, "Update 1")
        self.assertEqual(self.service.get_task(task.id).title, "Update 1")

        # Update 2
        self.service.update_task(task.id, "Update 2", "With description")
        updated = self.service.get_task(task.id)
        self.assertEqual(updated.title, "Update 2")
        self.assertEqual(updated.description, "With description")

        # Update 3 - clear description
        self.service.update_task(task.id, "Final", "")
        updated = self.service.get_task(task.id)
        self.assertEqual(updated.title, "Final")
        self.assertEqual(updated.description, "")

    def test_workflow_toggle_completion_multiple_times(self):
        """Test toggling task completion status multiple times."""
        task = self.service.add_task("Task")

        # Toggle: incomplete → complete
        self.service.mark_complete(task.id)
        self.assertTrue(self.service.get_task(task.id).is_completed)

        # Toggle: complete → incomplete
        self.service.mark_incomplete(task.id)
        self.assertFalse(self.service.get_task(task.id).is_completed)

        # Toggle: incomplete → complete again
        self.service.mark_complete(task.id)
        self.assertTrue(self.service.get_task(task.id).is_completed)

    def test_workflow_tasks_independence(self):
        """Test that operations on one task don't affect others."""
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")
        task3 = self.service.add_task("Task 3")

        # Modify task1
        self.service.mark_complete(task1.id)
        self.service.update_task(task1.id, "Updated Task 1")

        # Verify other tasks unchanged
        self.assertEqual(self.service.get_task(task2.id).title, "Task 2")
        self.assertFalse(self.service.get_task(task2.id).is_completed)
        self.assertEqual(self.service.get_task(task3.id).title, "Task 3")
        self.assertFalse(self.service.get_task(task3.id).is_completed)

        # Delete task2
        self.service.delete_task(task2.id)

        # Verify task1 and task3 still exist with correct state
        self.assertEqual(self.service.get_task(task1.id).title, "Updated Task 1")
        self.assertTrue(self.service.get_task(task1.id).is_completed)
        self.assertEqual(self.service.get_task(task3.id).title, "Task 3")

    def test_workflow_error_handling_non_existent_task(self):
        """Test that operations on non-existent tasks are handled."""
        # Try to get non-existent task
        self.assertIsNone(self.service.get_task(999))

        # Try to update non-existent task
        with self.assertRaises(ValueError):
            self.service.update_task(999, "New title")

        # Try to mark complete non-existent task
        result = self.service.mark_complete(999)
        self.assertFalse(result)

        # Try to delete non-existent task
        result = self.service.delete_task(999)
        self.assertFalse(result)

    def test_workflow_validation_invalid_title(self):
        """Test that invalid titles are rejected."""
        # Try to add task with empty title
        with self.assertRaises(ValueError):
            self.service.add_task("")

        # Try to add task with whitespace-only title
        with self.assertRaises(ValueError):
            self.service.add_task("   ")

        # Verify no task was added
        self.assertEqual(len(self.service.get_all_tasks()), 0)

        # Try to update with empty title
        task = self.service.add_task("Valid title")
        with self.assertRaises(ValueError):
            self.service.update_task(task.id, "")

        # Task should still exist with original title
        self.assertEqual(self.service.get_task(task.id).title, "Valid title")


if __name__ == "__main__":
    unittest.main()
