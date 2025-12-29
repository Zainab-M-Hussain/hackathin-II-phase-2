"""Console interface for todo application."""

from src.services.todo_service import TodoService


class TodoApp:
    """Menu-driven console interface for managing tasks."""

    def __init__(self, service: TodoService):
        """Initialize TodoApp with a TodoService instance.

        Args:
            service: TodoService instance for task management
        """
        self.service = service

    def main_menu(self) -> None:
        """Display the main menu options."""
        print("\n" + "=" * 50)
        print("        WELCOME TO TODO APPLICATION")
        print("=" * 50)
        print("\n1. Add Task")
        print("2. View All Tasks")
        print("3. Mark Task Complete/Incomplete")
        print("4. Update Task")
        print("5. Delete Task")
        print("6. Exit")
        print("\n" + "=" * 50)

    def add_task_flow(self) -> None:
        """Handle the add task flow."""
        print("\n--- Add New Task ---")
        try:
            title = input("Enter task title: ").strip()
            description = input("Enter task description (optional): ").strip()

            task = self.service.add_task(title, description)
            print(f"✓ Task added successfully (ID: {task.id})")
        except ValueError as e:
            print(f"✗ Error: {e}")

    def view_tasks_flow(self) -> None:
        """Handle the view all tasks flow."""
        print("\n--- All Tasks ---")
        tasks = self.service.get_all_tasks()

        if not tasks:
            print("No tasks available. Add one with option 1.")
            return

        print()
        for task in tasks:
            self._display_task(task)
        print()

    def toggle_task_status_flow(self) -> None:
        """Handle toggling task completion status."""
        print("\n--- Mark Task Complete/Incomplete ---")
        tasks = self.service.get_all_tasks()

        if not tasks:
            print("No tasks available.")
            return

        try:
            task_id = self._prompt_for_task_id()
            task = self.service.get_task(task_id)

            if task is None:
                print(f"✗ Task not found with ID {task_id}")
                return

            if task.is_completed:
                self.service.mark_incomplete(task_id)
                print(f"✓ Task {task_id} marked as incomplete")
            else:
                self.service.mark_complete(task_id)
                print(f"✓ Task {task_id} marked as complete")
        except ValueError as e:
            print(f"✗ Error: {e}")

    def update_task_flow(self) -> None:
        """Handle the update task flow."""
        print("\n--- Update Task ---")
        tasks = self.service.get_all_tasks()

        if not tasks:
            print("No tasks available.")
            return

        try:
            task_id = self._prompt_for_task_id()
            task = self.service.get_task(task_id)

            if task is None:
                print(f"✗ Task not found with ID {task_id}")
                return

            print(f"\nCurrent title: {task.title}")
            new_title = input("Enter new title (or press Enter to keep): ").strip()
            if not new_title:
                new_title = task.title

            print(f"Current description: {task.description if task.description else '(none)'}")
            new_description = input("Enter new description (or press Enter to keep): ").strip()
            if not new_description:
                new_description = task.description

            self.service.update_task(task_id, new_title, new_description)
            print(f"✓ Task {task_id} updated successfully")
        except ValueError as e:
            print(f"✗ Error: {e}")

    def delete_task_flow(self) -> None:
        """Handle the delete task flow."""
        print("\n--- Delete Task ---")
        tasks = self.service.get_all_tasks()

        if not tasks:
            print("No tasks available.")
            return

        try:
            task_id = self._prompt_for_task_id()
            task = self.service.get_task(task_id)

            if task is None:
                print(f"✗ Task not found with ID {task_id}")
                return

            print(f"\nTask to delete: {self._format_task(task)}")
            confirmation = input("Are you sure you want to delete this task? (Y/N): ").strip().upper()

            if confirmation == "Y":
                self.service.delete_task(task_id)
                print(f"✓ Task {task_id} deleted successfully")
            else:
                print("Task deletion cancelled")
        except ValueError as e:
            print(f"✗ Error: {e}")

    def run(self) -> None:
        """Main application loop."""
        while True:
            self.main_menu()
            try:
                choice = input("Select an option (1-6): ").strip()

                if choice == "1":
                    self.add_task_flow()
                elif choice == "2":
                    self.view_tasks_flow()
                elif choice == "3":
                    self.toggle_task_status_flow()
                elif choice == "4":
                    self.update_task_flow()
                elif choice == "5":
                    self.delete_task_flow()
                elif choice == "6":
                    print("\nThank you for using Todo App. Goodbye!")
                    break
                else:
                    print("✗ Invalid option. Please select 1-6.")
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"✗ An unexpected error occurred: {e}")

    def _prompt_for_task_id(self) -> int:
        """Prompt user for a task ID and validate input.

        Returns:
            The task ID as an integer

        Raises:
            ValueError: If input is not a valid integer
        """
        try:
            task_id = input("Enter task ID: ").strip()
            return int(task_id)
        except ValueError:
            raise ValueError("Invalid task ID. Please enter a number.")

    def _format_task(self, task) -> str:
        """Format a task for display.

        Args:
            task: The Task object to format

        Returns:
            Formatted task string
        """
        return f"[{task.id}] {self._get_status_symbol(task)} {task.title}"

    def _display_task(self, task) -> None:
        """Display a single task with formatted output.

        Args:
            task: The Task object to display
        """
        status = self._get_status_symbol(task)
        print(f"[{task.id}] {status} {task.title}")
        if task.description:
            print(f"     └─ {task.description}")

    @staticmethod
    def _get_status_symbol(task) -> str:
        """Get the status symbol for a task.

        Args:
            task: The Task object

        Returns:
            Status symbol (✓ for complete, ○ for incomplete)
        """
        return "✓" if task.is_completed else "○"
