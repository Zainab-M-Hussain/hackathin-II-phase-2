# Full-Stack Web Todo App

This document provides instructions on how to set up and run the project, including newly added features.

## New Features Overview

This application has been enhanced with the following features:
-   **Authentication**: User signup and login with JWT-based authentication.
-   **Task Management**: Tasks now include optional due dates, priorities (Low, Medium, High), and categories/tags.
-   **Search & Filter**: Search tasks by title/description and filter by status, priority, creation date, due date, and categories.
-   **Task Actions**: Edit, delete, and toggle completion for individual tasks.
-   **Bulk Actions**: Select multiple tasks to delete or mark as completed/pending.
-   **UX Improvements**: Subtle animations for task changes and toast notifications for actions.
-   **Advanced Features**: Export tasks to JSON/CSV, and a dark mode toggle for the UI.
-   **Localization**: Support for English and Urdu languages.

## Prerequisites

- Python 3.13+
- Node.js 18+
- `uv` package installed (`pip install uv`)
- A Neon Serverless PostgreSQL database
- A Better Auth account and project

## Setup

1.  **Clone the repository.**
2.  **Create a `.env` file** in the `backend` directory and add your Neon database connection string and Better Auth secret:
    ```
    DATABASE_URL="postgresql://user:password@host:port/dbname"
    BETTER_AUTH_SECRET="your_better_auth_secret"
    ```
3.  **Create a `.env.local` file** in the `frontend` directory and add your Better Auth project ID and secret:
    ```
    NEXT_PUBLIC_BETTER_AUTH_PROJECT_ID="your_better_auth_project_id"
    BETTER_AUTH_SECRET="your_better_auth_secret"
    ```
4.  **Backend Setup:**
    ```bash
    cd backend
    uv venv
    uv pip install -e .
    ```
    *Note: If `alembic` related issues prevent database migration, please ensure your Python environment is correctly set up and alembic is installed within your virtual environment.*
5.  **Frontend Setup:**
    ```bash
    cd frontend
    npm install
    ```
    *Note: If `npm install` reports peer dependency conflicts (e.g., with `@testing-library/react` and React 19), you may need to use `npm install --legacy-peer-deps` or ensure your environment satisfies the peer dependency requirements.*

## Running the Application

1.  **Start the backend server:**
    ```bash
    cd backend
    uv run uvicorn app.main:app --reload
    ```
2.  **Start the frontend development server:**
    ```bash
    cd frontend
    npm run dev
    ```

The application will be available at `http://localhost:3000`. You can sign up or log in to start using the application.

## Interacting with New Features

Detailed instructions and API examples for interacting with the new features can be found in the feature's quickstart guide:
[specs/004-todo-app-features/quickstart.md](specs/004-todo-app-features/quickstart.md)

### Language Switching

The frontend supports English and Urdu. Use the language switcher component in the UI to change the language.

### Dark Mode

Toggle between light and dark themes using the dark mode switcher component in the UI.