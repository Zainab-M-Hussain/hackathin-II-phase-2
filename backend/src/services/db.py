"""
Database connection and session management.

Handles Neon Serverless Postgres connection pooling and session creation.
"""

from typing import Generator, Optional
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine as sqlmodel_create_engine

from src.core.config import settings
from src.core.errors import DatabaseError


# ============================================================================
# Database Engine Setup
# ============================================================================

def create_db_engine() -> Engine:
    """
    Create SQLAlchemy engine with connection pooling for Neon.

    Uses psycopg2 driver with:
    - Connection pooling for performance
    - Connection recycling to prevent idle timeouts
    - Echo disabled in production
    """
    try:
        engine = sqlmodel_create_engine(
            settings.DATABASE_URL,
            echo=settings.DATABASE_ECHO,
            pool_size=settings.DATABASE_POOL_SIZE,
            max_overflow=10,
            pool_recycle=settings.DATABASE_POOL_RECYCLE,
            pool_pre_ping=True,  # Test connection before using
            future=True,  # Enable SQLAlchemy 2.0 style
        )
        return engine
    except Exception as e:
        raise DatabaseError(
            f"Failed to create database engine: {str(e)}",
            original_error=e
        )


# ============================================================================
# Session Factory
# ============================================================================

# Global engine instance
_engine: Optional[Engine] = None


def get_engine() -> Engine:
    """Get or create the global database engine"""
    global _engine
    if _engine is None:
        _engine = create_db_engine()
    return _engine


def get_session_factory() -> sessionmaker:
    """Get SQLAlchemy session factory"""
    return sessionmaker(
        bind=get_engine(),
        class_=Session,
        expire_on_commit=False,
        autoflush=False,
    )


# ============================================================================
# Session Management
# ============================================================================

def get_db_session() -> Generator[Session, None, None]:
    """
    Dependency injection for FastAPI endpoints.

    Usage in endpoints:
        @router.get("/tasks")
        async def list_tasks(session: Session = Depends(get_db_session)):
            tasks = session.query(Task).all()
            return tasks

    Ensures session is:
    - Created fresh for each request
    - Properly closed after request completes
    - Rolled back on error
    """
    SessionLocal = get_session_factory()
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# ============================================================================
# Database Initialization
# ============================================================================

def init_db() -> None:
    """
    Initialize database schema.

    Creates all tables defined in SQLModel entities.
    Safe to call multiple times (idempotent).

    Called at application startup.
    """
    try:
        engine = get_engine()
        SQLModel.metadata.create_all(engine)
        print("✅ Database schema initialized successfully")
    except Exception as e:
        raise DatabaseError(
            f"Failed to initialize database schema: {str(e)}",
            original_error=e
        )


def teardown_db() -> None:
    """
    Clean up database connections.

    Called at application shutdown.
    """
    try:
        engine = get_engine()
        engine.dispose()
        print("✅ Database connections closed")
    except Exception as e:
        print(f"⚠️  Error closing database connections: {str(e)}")


# ============================================================================
# Event Handlers (Optional: For debugging/monitoring)
# ============================================================================

@event.listens_for(Engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    """Called when a new database connection is created"""
    # Can add connection initialization here if needed
    pass


@event.listens_for(Engine, "checkout")
def receive_checkout(dbapi_conn, connection_record, connection_proxy):
    """Called when a connection is checked out from the pool"""
    # Can add monitoring/logging here
    pass
