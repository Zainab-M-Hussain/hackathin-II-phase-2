from fastapi import APIRouter, Depends
from sqlmodel import Session
from .... import schemas, crud
from ....database import get_session

router = APIRouter()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_session)):
    return crud.create_user(db=db, user=user)
