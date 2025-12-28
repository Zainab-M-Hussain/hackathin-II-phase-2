import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, select
from uuid import UUID
from .database import engine, get_session
from . import models, schemas
from .api.endpoints import tasks, users, auth, chat
from .middleware import JWTAuthMiddleware
from . import config
from .crud import get_password_hash

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add JWT middleware
app.add_middleware(JWTAuthMiddleware)

def create_hardcoded_user_on_startup():
    with Session(engine) as session:
        user = session.get(models.User, UUID("00000000-0000-0000-0000-000000000001"))
        if not user:
            user = models.User(
                id=UUID("00000000-0000-0000-0000-000000000001"),
                email="testuser@example.com",
                name="Test User",
                password=get_password_hash("password"),
            )
            session.add(user)
            session.commit()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    create_hardcoded_user_on_startup()

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(tasks.router, prefix="/api/users", tags=["tasks"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

@app.get("/")
def read_root():
    return {"Hello": "World"}