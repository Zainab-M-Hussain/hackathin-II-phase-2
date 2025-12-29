"""Unit tests for TodoApp CLI."""

import unittest
from io import StringIO
from unittest.mock import patch
from src.cli.app import TodoApp
from src.services.todo_service import TodoService


class TestTodoApp(unittest.TestCase):
    """Test cases for TodoApp class."""

    def setUp(self):
        """Set up a fresh TodoApp for each test."""
        self.service = TodoService()
        self.app = TodoApp(self.service)

    def test_format_task_shows_incomplete_status(self):
        """Test that format_task shows incomplete symbol."""
        task = self.service.add_task("Buy groceries")
        formatted = self.app._format_task(task)
        self.assertIn("○", formatted)
        self.assertIn("Buy groceries", formatted)

    def test_format_task_shows_complete_status(self):
        """Test that format_task shows complete symbol."""
        task = self.service.add_task("Buy groceries")
        self.service.mark_complete(task.id)
        formatted = self.app._format_task(task)
        self.assertIn("✓", formatted)

    def test_get_status_symbol_incomplete(self):
        """Test status symbol for incomplete task."""
        task = self.service.add_task("Task")
        symbol = TodoApp._get_status_symbol(task)
        self.assertEqual(symbol, "○")

    def test_get_status_symbol_complete(self):
        """Test status symbol for complete task."""
        task = self.service.add_task("Task")
        self.service.mark_complete(task.id)
        symbol = TodoApp._get_status_symbol(task)
        self.assertEqual(symbol, "✓")

    @patch("builtins.input", side_effect=["Buy groceries", ""])
    def test_add_task_flow_success(self, mock_input):
        """Test successful task addition flow."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.app.add_task_flow()
            output = fake_out.getvalue()
            self.assertIn("added successfully", output)

        tasks = self.service.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Buy groceries")

    @patch("builtins.input", side_effect=["", ""])
    def test_add_task_flow_empty_title_error(self, mock_input):
        """Test that empty title shows error."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.app.add_task_flow()
            output = fake_out.getvalue()
            self.assertIn("Error", output)
            self.assertIn("empty", output.lower())

    @patch("builtins.input", side_effect=["   ", ""])
    def test_add_task_flow_whitespace_title_error(self, mock_input):
        """Test that whitespace-only title shows error."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.app.add_task_flow()
            output = fake_out.getvalue()
            self.assertIn("Error", output)

    @patch("builtins.input", side_effect=["Task with description", "Do this tomorrow"])
    def test_add_task_flow_with_description(self, mock_input):
        """Test adding task with description."""
        with patch("sys.stdout", new=StringIO()):
            self.app.add_task_flow()
        tasks = self.service.get_all_tasks()
        self.assertEqual(tasks[0].description, "Do this tomorrow")

    def test_view_tasks_flow_empty_list(self):
        """Test viewing tasks when list is empty."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.app.view_tasks_flow()
            output = fake_out.getvalue()
            self.assertIn("No tasks available", output)

    def test_view_tasks_flow_with_tasks(self):
        """Test viewing tasks when tasks exist."""
        self.service.add_task("Task 1", "Description 1")
        self.service.add_task("Task 2")

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.app.view_tasks_flow()
            output = fake_out.getvalue()
            self.assertIn("Task 1", output)
            self.assertIn("Task 2", output)

    def test_view_tasks_shows_completion_status(self):
        """Test that view shows completion status."""
        task = self.service.add_task("Task")
        self.service.mark_complete(task.id)

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.app.view_tasks_flow()
            output = fake_out.getvalue()
            self.assertIn("✓", output)

    @patch("builtins.input", side_effect=["1"])
    def test_toggle_status_complete_to_incomplete(self, mock_input):
        """Test toggling completed task to incomplete."""
        task = self.service.add_task("Task")
        self.service.mark_complete(task.id)

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.app.toggle_task_status_flow()
            output = fake_out.getvalue()
            self.assertIn("incomplete", output)

        task = self.service.get_task(1)
        self.assertFalse(task.is_completed)

    @patch("builtins.input", side_effect=["1"])
    def test_toggle_status_incomplete_to_complete(self, mock_input):
        """Test toggling incomplete task to complete."""
        self.service.add_task("Task")

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.app.toggle_task_status_flow()
            output = fake_out.getvalue()
            self.assertIn("complete", output)

        task = self.service.get_task(1)
        self.assertTrue(task.is_completed)

    @patch("builtins.input", side_effect=["999"])
    def test_toggle_status_non_existent_task(self, mock_input):
        """Test toggling non-existent task shows error."""
        self.service.add_task("Task")  # Add at least one task so we get past the "No tasks" check
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.app.toggle_task_status_flow()
            output = fake_out.getvalue()
            self.assertIn("not found", output)

    @patch("builtins.input", side_effect=["abc"])
    def test_toggle_status_invalid_id_input(self, mock_input):
        """Test that non-numeric ID input shows error."""
        self.service.add_task("Task")

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.app.toggle_task_status_flow()
            output = fake_out.getvalue()
            self.assertIn("Error", output)

    @patch("builtins.input", side_effect=["1", "New title", "New description"])
    def test_update_task_flow_success(self, mock_input):
        """Test successful task update."""
        self.service.add_task("Old title", "Old description")

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.app.update_task_flow()
            output = fake_out.getvalue()
            self.assertIn("updated successfully", output)

        task = self.service.get_task(1)
        self.assertEqual(task.title, "New title")
        self.assertEqual(task.description, "New description")

    @patch("builtins.input", side_effect=["1", "New title", ""])
    def test_update_task_keep_description(self, mock_input):
        """Test updating title while keeping description."""
        self.service.add_task("Old title", "Keep this description")

        with patch("sys.stdout", new=StringIO()):
            self.app.update_task_flow()

        task = self.service.get_task(1)
        self.assertEqual(task.title, "New title")
        self.assertEqual(task.description, "Keep this description")

    @patch("builtins.input", side_effect=["1", "", "New description"])
    def test_update_task_keep_title(self, mock_input):
        """Test updating description while keeping title."""
        self.service.add_task("Keep this title")

        with patch("sys.stdout", new=StringIO()):
            self.app.update_task_flow()

        task = self.service.get_task(1)
        self.assertEqual(task.title, "Keep this title")
        self.assertEqual(task.description, "New description")

    @patch("builtins.input", side_effect=["999", "Title", "Description"])
    def test_update_task_non_existent(self, mock_input):
        """Test updating non-existent task shows error."""
        self.service.add_task("Task")  # Add at least one task so we get past the "No tasks" check
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.app.update_task_flow()
            output = fake_out.getvalue()
            self.assertIn("not found", output)

    @patch("builtins.input", side_effect=["1", "Y"])
    def test_delete_task_flow_success(self, mock_input):
        """Test successful task deletion."""
        self.service.add_task("Task to delete")

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.app.delete_task_flow()
            output = fake_out.getvalue()
            self.assertIn("deleted successfully", output)

        tasks = self.service.get_all_tasks()
        self.assertEqual(len(tasks), 0)

    @patch("builtins.input", side_effect=["1", "N"])
    def test_delete_task_flow_cancelled(self, mock_input):
        """Test cancelling task deletion."""
        self.service.add_task("Task to delete")

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.app.delete_task_flow()
            output = fake_out.getvalue()
            self.assertIn("cancelled", output)

        tasks = self.service.get_all_tasks()
        self.assertEqual(len(tasks), 1)

    @patch("builtins.input", side_effect=["999", "Y"])
    def test_delete_task_non_existent(self, mock_input):
        """Test deleting non-existent task shows error."""
        self.service.add_task("Task")  # Add at least one task so we get past the "No tasks" check
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.app.delete_task_flow()
            output = fake_out.getvalue()
            self.assertIn("not found", output)

    def test_prompt_for_task_id_valid_input(self):
        """Test prompting for valid task ID."""
        with patch("builtins.input", return_value="42"):
            task_id = self.app._prompt_for_task_id()
            self.assertEqual(task_id, 42)

    def test_prompt_for_task_id_invalid_input(self):
        """Test prompting for non-numeric task ID raises error."""
        with patch("builtins.input", return_value="not_a_number"):
            with self.assertRaises(ValueError):
                self.app._prompt_for_task_id()


if __name__ == "__main__":
    unittest.main()
