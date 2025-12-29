#!/usr/bin/env python3
"""Entry point for Todo Application."""

from src.services.todo_service import TodoService
from src.cli.app import TodoApp


def main():
    """Run the todo application."""
    try:
        service = TodoService()
        app = TodoApp(service)
        app.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1
    return 0


if __name__ == "__main__":
    exit(main())
