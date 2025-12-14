from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from .... import schemas, crud
from ....database import get_session

router = APIRouter()

@router.post("/{user_id}/tasks/", response_model=schemas.Task)
def create_task_for_user(user_id: int, task: schemas.TaskCreate, db: Session = Depends(get_session)):
    return crud.create_task(db=db, task=task, user_id=user_id)

@router.get("/{user_id}/tasks/", response_model=List[schemas.Task])
def read_tasks(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    tasks = crud.get_tasks(db, user_id=user_id, skip=skip, limit=limit)
    return tasks

@router.get("/{user_id}/tasks/{task_id}", response_model=schemas.Task)
def read_task(user_id: int, task_id: int, db: Session = Depends(get_session)):
    db_task = crud.get_task(db, user_id=user_id, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.put("/{user_id}/tasks/{task_id}", response_model=schemas.Task)
def update_task(user_id: int, task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_session)):
    db_task = crud.update_task(db, user_id=user_id, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/{user_id}/tasks/{task_id}", response_model=schemas.Task)
def delete_task(user_id: int, task_id: int, db: Session = Depends(get_session)):
    db_task = crud.delete_task(db, user_id=user_id, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
