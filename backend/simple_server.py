"""
Simple minimal FastAPI server for Phase II Todo App
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Phase II Todo API",
    description="REST API for todo application",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (for demo purposes)
from datetime import datetime

def create_task_with_timestamps(**kwargs):
    now = datetime.utcnow().isoformat()
    return {
        "created_at": now,
        "updated_at": now,
        "tags": [],
        **kwargs
    }

tasks_db = {
    1: create_task_with_timestamps(id=1, title="Learn FastAPI", description="Study FastAPI basics", status="pending", priority="HIGH"),
    2: create_task_with_timestamps(id=2, title="Build Todo App", description="Create a todo application", status="pending", priority="MEDIUM"),
    3: create_task_with_timestamps(id=3, title="Deploy to production", description="Deploy the app", status="complete", priority="HIGH"),
}
task_counter = 4

tags_db = {
    1: {"id": 1, "name": "work"},
    2: {"id": 2, "name": "personal"},
}
tag_counter = 3

# Pydantic models
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "pending"
    priority: str = "MEDIUM"

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int

# Root endpoints
@app.get("/")
async def root():
    """Root endpoint - API status check"""
    return {
        "status": "ok",
        "title": "Phase II Todo API",
        "version": "2.0.0",
        "environment": "development",
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "todo-api",
        "version": "2.0.0",
    }

# Task endpoints
@app.get("/api/tasks")
async def list_tasks(skip: int = 0, limit: int = 50):
    """Get all tasks with pagination"""
    all_tasks = list(tasks_db.values())
    total = len(all_tasks)
    paginated_tasks = all_tasks[skip:skip + limit]

    return {
        "items": paginated_tasks,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@app.post("/api/tasks")
async def create_task(task: TaskCreate) -> Task:
    """Create a new task"""
    global task_counter
    new_id = task_counter
    task_counter += 1
    new_task = create_task_with_timestamps(
        id=new_id,
        **task.dict()
    )
    tasks_db[new_id] = new_task
    return new_task

@app.get("/api/tasks/{task_id}")
async def get_task(task_id: int) -> Task:
    """Get a specific task"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db[task_id]

@app.put("/api/tasks/{task_id}")
async def update_task(task_id: int, task: TaskCreate) -> Task:
    """Update a task"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    existing = tasks_db[task_id]
    updated_task = {
        **existing,
        "id": task_id,
        "updated_at": datetime.utcnow().isoformat(),
        **task.dict()
    }
    tasks_db[task_id] = updated_task
    return updated_task

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int):
    """Delete a task"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks_db[task_id]
    return {"message": "Task deleted"}

# Tag endpoints
@app.get("/api/tags")
async def list_tags():
    """Get all tags"""
    return list(tags_db.values())

@app.post("/api/tags")
async def create_tag(tag: TagCreate) -> Tag:
    """Create a new tag"""
    global tag_counter
    new_id = tag_counter
    tag_counter += 1
    new_tag = {
        "id": new_id,
        **tag.dict()
    }
    tags_db[new_id] = new_tag
    return new_tag

@app.get("/api/tags/{tag_id}")
async def get_tag(tag_id: int) -> Tag:
    """Get a specific tag"""
    if tag_id not in tags_db:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tags_db[tag_id]

@app.put("/api/tags/{tag_id}")
async def update_tag(tag_id: int, tag: TagCreate) -> Tag:
    """Update a tag"""
    if tag_id not in tags_db:
        raise HTTPException(status_code=404, detail="Tag not found")
    updated_tag = {
        "id": tag_id,
        **tag.dict()
    }
    tags_db[tag_id] = updated_tag
    return updated_tag

@app.delete("/api/tags/{tag_id}")
async def delete_tag(tag_id: int):
    """Delete a tag"""
    if tag_id not in tags_db:
        raise HTTPException(status_code=404, detail="Tag not found")
    del tags_db[tag_id]
    return {"message": "Tag deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "simple_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
