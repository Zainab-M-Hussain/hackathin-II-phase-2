"""
FastAPI application entry point.

Initializes the FastAPI app with:
- Database connection pooling
- Error handling and middleware
- CORS configuration
- Route registration
- Startup/shutdown events
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler

from src.core.config import settings
from src.core.errors import TodoException, exception_to_http_response
from src.services.db import init_db, teardown_db


# ============================================================================
# Startup/Shutdown Events
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan event handler.

    Runs on startup: Initialize database connections
    Runs on shutdown: Clean up connections
    """
    # Startup
    print("🚀 Starting Phase II Todo API...")
    init_db()
    print(f"✅ API running on {settings.SERVER_HOST}:{settings.SERVER_PORT}")
    print(f"📖 Docs: http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/docs")

    yield

    # Shutdown
    print("🛑 Shutting down Phase II Todo API...")
    teardown_db()
    print("✅ Goodbye!")


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)


# ============================================================================
# Middleware Setup
# ============================================================================

# CORS Middleware: Allow frontend (Next.js) to call backend API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)


# ============================================================================
# Exception Handlers
# ============================================================================

@app.exception_handler(TodoException)
async def todo_exception_handler(request: Request, exc: TodoException):
    """Handle custom todo exceptions"""
    error_response = exception_to_http_response(exc, path=str(request.url.path))
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict(exclude_none=True)
    )


# ============================================================================
# Root Route
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint - API status check"""
    return {
        "status": "ok",
        "title": settings.API_TITLE,
        "version": settings.API_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "todo-api",
        "version": settings.API_VERSION,
    }


# ============================================================================
# Route Registration
# ============================================================================

from src.api.endpoints import tasks_router, tags_router

app.include_router(tasks_router, prefix=settings.API_PREFIX)
app.include_router(tags_router, prefix=settings.API_PREFIX)


# ============================================================================
# Application Factory (for testing)
# ============================================================================

def get_app() -> FastAPI:
    """Get the FastAPI application instance"""
    return app


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.src.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
