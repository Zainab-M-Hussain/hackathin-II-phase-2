import os # Keep this if needed for other os operations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, select
from .database import engine, get_session # Import engine directly
from . import models, schemas
from .api.endpoints import tasks, users, auth # Import routers and auth
from .middleware import JWTAuthMiddleware
from . import config # Import config module to ensure dotenv is loaded

app = FastAPI()

# Add JWT middleware
app.add_middleware(JWTAuthMiddleware)

# In production, you would replace this with the actual URL of your frontend application
# For example: origins = ["https://www.your-production-app.com"]
origins = [
    "http://localhost:3000", # Allow local frontend
    "http://127.0.0.1:3000", # Allow local frontend
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Use the defined origins list
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup to ensure schema matches models
@app.on_event("startup")
def create_db_and_tables():
    SQLModel.metadata.create_all(engine) # Create all tables based on models

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(tasks.router, prefix="/api/users", tags=["tasks"])
app.include_router(auth.router, prefix="/api", tags=["auth"]) # Include auth router

@app.get("/")
def read_root():
    return {"Hello": "World"}
