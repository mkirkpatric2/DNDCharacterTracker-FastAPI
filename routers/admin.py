from datetime import timedelta, datetime
from typing import Annotated
from starlette import status
from models import Players, Characters
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from passlib.context import CryptContext
from jose import jwt, JWTError
from routers.auth import get_current_user
from routers.characters import CharacterRequest

router = APIRouter(
    prefix='/admin',  # everything here is under /auth
    tags=['admin']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class CreatePlayerRequest(BaseModel):
    username: str
    password: str
    role: str


user_dependency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]


# Allow admin to update any character
@router.post("/update/{char_id}", status_code=status.HTTP_204_NO_CONTENT)  # update
async def update_char(db: db_dependency,
                      char_request: CharacterRequest,
                      user: user_dependency,
                      char_id: int = Path(gt=0, lt=25)):
    char_model = db.query(Characters).filter(Characters.id == char_id).first()

    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401,
                            detail="Not Authorized.")

    elif char_model is None:
        raise HTTPException(status_code=404, detail='not found')

    char_model.name = char_request.name
    char_model.character_class = char_request.character_class
    char_model.level = char_request.level
    char_model.race = char_request.race
    char_model.current_exp = char_request.current_exp
    char_model.strength = char_request.strength
    char_model.dexterity = char_request.dexterity
    char_model.constitution = char_request.constitution
    char_model.intelligence = char_request.intelligence
    char_model.wisdom = char_request.wisdom
    char_model.charisma = char_request.charisma
    char_model.alive = char_request.alive

    db.add(char_model)
    db.commit()


# Allow Admin to delete characters.
@router.delete("/delete/{char_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_char(db: db_dependency, user: user_dependency, char_id: int = Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Not Authorized')

    char_model = db.query(Characters).filter(Characters.id == char_id).first()
    if char_model is None:
        raise HTTPException(status_code=404, detail='not found')

    db.query(Characters).filter(Characters.id == char_id).delete()
    db.commit()
