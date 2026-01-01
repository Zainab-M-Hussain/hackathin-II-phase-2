"""
Integration tests for Task API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

from src.main import app
from src.services.db import get_session
from src.models.task import Task, TaskStatus, TaskPriority


@pytest.fixture(name="session")
def session_fixture():
    """Create test database session"""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create test client with session override"""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_task(client: TestClient):
    """Test creating a new task"""
    response = client.post(
        "/api/tasks",
        json={
            "title": "Test Task",
            "priority": "MEDIUM",
            "description": "Test description"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["priority"] == "MEDIUM"
    assert data["status"] == "pending"
    assert data["id"] is not None


def test_get_tasks_empty(client: TestClient):
    """Test getting tasks when list is empty"""
    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


def test_list_tasks_with_pagination(client: TestClient):
    """Test listing tasks with pagination"""
    # Create 5 tasks
    for i in range(5):
        client.post(
            "/api/tasks",
            json={
                "title": f"Task {i+1}",
                "priority": "MEDIUM"
            }
        )

    # Get first 2
    response = client.get("/api/tasks?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 5
    assert data["skip"] == 0
    assert data["limit"] == 2


def test_filter_tasks_by_status(client: TestClient):
    """Test filtering tasks by status"""
    # Create task
    response = client.post(
        "/api/tasks",
        json={"title": "Pending Task", "priority": "MEDIUM"}
    )
    task_id = response.json()["id"]

    # Filter by pending
    response = client.get("/api/tasks?status=pending")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 1

    # Mark as complete
    client.patch(
        f"/api/tasks/{task_id}/status",
        json={"status": "complete"}
    )

    # Filter by complete
    response = client.get("/api/tasks?status=complete")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 1

    # Filter by pending (should be empty)
    response = client.get("/api/tasks?status=pending")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 0


def test_filter_tasks_by_priority(client: TestClient):
    """Test filtering tasks by priority"""
    # Create tasks with different priorities
    for priority in ["LOW", "MEDIUM", "HIGH"]:
        client.post(
            "/api/tasks",
            json={"title": f"Task {priority}", "priority": priority}
        )

    # Filter by HIGH
    response = client.get("/api/tasks?priority=HIGH")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["priority"] == "HIGH"


def test_search_tasks(client: TestClient):
    """Test searching tasks"""
    # Create tasks
    client.post("/api/tasks", json={"title": "Buy groceries", "priority": "MEDIUM"})
    client.post("/api/tasks", json={"title": "Call mom", "priority": "LOW"})
    client.post("/api/tasks", json={"title": "Fix bug in app", "priority": "HIGH"})

    # Search for "bug"
    response = client.get("/api/tasks?search=bug")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert "bug" in data["items"][0]["title"].lower()


def test_sort_tasks(client: TestClient):
    """Test sorting tasks"""
    # Create tasks
    titles = ["Buy groceries", "Call mom", "Fix bug"]
    for title in titles:
        client.post("/api/tasks", json={"title": title, "priority": "MEDIUM"})

    # Sort by title ascending
    response = client.get("/api/tasks?sort_by=title&sort_order=asc")
    assert response.status_code == 200
    data = response.json()
    returned_titles = [t["title"] for t in data["items"]]
    assert returned_titles == sorted(titles)

    # Sort by title descending
    response = client.get("/api/tasks?sort_by=title&sort_order=desc")
    assert response.status_code == 200
    data = response.json()
    returned_titles = [t["title"] for t in data["items"]]
    assert returned_titles == sorted(titles, reverse=True)


def test_get_single_task(client: TestClient):
    """Test getting a single task"""
    # Create task
    create_response = client.post(
        "/api/tasks",
        json={"title": "Test Task", "priority": "MEDIUM"}
    )
    task_id = create_response.json()["id"]

    # Get task
    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["id"] == task_id


def test_update_task(client: TestClient):
    """Test updating a task"""
    # Create task
    create_response = client.post(
        "/api/tasks",
        json={"title": "Original Title", "priority": "MEDIUM"}
    )
    task_id = create_response.json()["id"]

    # Update task
    response = client.put(
        f"/api/tasks/{task_id}",
        json={
            "title": "Updated Title",
            "priority": "HIGH",
            "description": "Updated description"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["priority"] == "HIGH"
    assert data["description"] == "Updated description"


def test_update_task_status(client: TestClient):
    """Test updating task status"""
    # Create task
    create_response = client.post(
        "/api/tasks",
        json={"title": "Test Task", "priority": "MEDIUM"}
    )
    task_id = create_response.json()["id"]
    assert create_response.json()["status"] == "pending"

    # Mark as complete
    response = client.patch(
        f"/api/tasks/{task_id}/status",
        json={"status": "complete", "reason": "Finished"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "complete"

    # Mark as archived
    response = client.patch(
        f"/api/tasks/{task_id}/status",
        json={"status": "archived"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "archived"


def test_delete_task(client: TestClient):
    """Test deleting a task"""
    # Create task
    create_response = client.post(
        "/api/tasks",
        json={"title": "Task to delete", "priority": "MEDIUM"}
    )
    task_id = create_response.json()["id"]

    # Delete task
    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 200

    # Verify task is deleted
    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 404


def test_get_task_history(client: TestClient):
    """Test getting task audit history"""
    # Create task
    create_response = client.post(
        "/api/tasks",
        json={"title": "Test Task", "priority": "MEDIUM"}
    )
    task_id = create_response.json()["id"]

    # Update task
    client.put(
        f"/api/tasks/{task_id}",
        json={"title": "Updated Task", "priority": "HIGH"}
    )

    # Get history
    response = client.get(f"/api/tasks/{task_id}/history")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2  # Create + Update
    assert data[0]["action"] == "CREATE"


def test_get_task_statistics(client: TestClient):
    """Test getting task statistics"""
    # Create tasks
    for i in range(3):
        client.post("/api/tasks", json={"title": f"Task {i+1}", "priority": "MEDIUM"})

    # Mark one as complete
    tasks = client.get("/api/tasks?limit=100").json()["items"]
    client.patch(f"/api/tasks/{tasks[0]['id']}/status", json={"status": "complete"})

    # Get stats
    response = client.get("/api/tasks/stats/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert data["completed"] == 1
    assert data["pending"] == 2


def test_error_not_found(client: TestClient):
    """Test 404 error for non-existent task"""
    response = client.get("/api/tasks/99999")
    assert response.status_code == 404


def test_error_invalid_data(client: TestClient):
    """Test validation error for invalid data"""
    # Missing required field
    response = client.post("/api/tasks", json={"priority": "MEDIUM"})
    assert response.status_code == 422  # Validation error


def test_concurrent_updates(client: TestClient):
    """Test handling concurrent updates"""
    # Create task
    create_response = client.post(
        "/api/tasks",
        json={"title": "Concurrent Task", "priority": "MEDIUM"}
    )
    task_id = create_response.json()["id"]

    # Update multiple times
    for i in range(3):
        response = client.put(
            f"/api/tasks/{task_id}",
            json={"title": f"Update {i+1}", "priority": "MEDIUM"}
        )
        assert response.status_code == 200
        assert response.json()["title"] == f"Update {i+1}"
