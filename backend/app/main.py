from fastapi import FastAPI
from .database import engine
from . import models
from .api.endpoints import users, tasks

models.SQLModel.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])

@app.get("/")
def read_root():
    return {"Hello": "World"}
