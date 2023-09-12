from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal


router = APIRouter(
    prefix='/auth',  # everything here is under /auth
    tags=['auth']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
