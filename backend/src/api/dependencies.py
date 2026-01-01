"""
FastAPI dependency injection functions.

Provides dependencies for endpoints like database sessions and authentication.
"""

from typing import Generator
from sqlmodel import Session
from fastapi import Depends, HTTPException, status

from src.services.db import get_db_session


# ============================================================================
# Database Session Dependency
# ============================================================================

async def get_db() -> Generator[Session, None, None]:
    """
    Dependency to inject database session into endpoints.

    Usage in endpoints:
        @router.get("/tasks")
        async def list_tasks(session: Session = Depends(get_db)):
            ...

    The session is:
    - Created fresh for each request
    - Automatically committed on success
    - Automatically rolled back on error
    - Properly closed after request
    """
    async for session in get_db_session():
        yield session


# ============================================================================
# Authentication Placeholder (for future)
# ============================================================================

async def get_current_user() -> str:
    """
    Placeholder for future authentication.

    Currently returns a default user ID for Phase II (single-session).
    In Phase III, will validate JWT tokens or session cookies.

    Usage in endpoints:
        @router.get("/tasks")
        async def list_tasks(user_id: str = Depends(get_current_user)):
            ...
    """
    # Phase II: Single-session, no authentication
    return "default-user"


# ============================================================================
# Rate Limiting Placeholder (for future)
# ============================================================================

async def check_rate_limit(user_id: str = Depends(get_current_user)):
    """
    Placeholder for rate limiting.

    Currently disabled. In Phase III, will enforce rate limits:
    - 100 requests per minute per session (configurable)
    - Returns 429 Too Many Requests if limit exceeded

    Usage in endpoints:
        @router.post("/tasks")
        async def create_task(
            task_create: TaskCreate,
            session: Session = Depends(get_db),
            rate_limit: bool = Depends(check_rate_limit)
        ):
            ...
    """
    # Phase II: No rate limiting
    return True
