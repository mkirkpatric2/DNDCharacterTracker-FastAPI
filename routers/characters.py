from typing import Annotated
from fastapi import APIRouter, Depends, Path, HTTPException
from pydantic import Field, BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Characters

router = APIRouter(
    prefix='/characters',  # everything here is under /auth
    tags=['characters']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class CharacterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=15)
    character_class: str = Field(min_length=3, max_length=20)
    level: int = Field(gt=0, lt=21)
    race: str = Field(min_length=3, max_length=20)
    current_exp: int = Field(gt=0, lt=150)
    strength: int = Field(gt=0, lt=21)
    dexterity: int = Field(gt=0, lt=21)
    constitution: int = Field(gt=0, lt=21)
    intelligence: int = Field(gt=0, lt=21)
    wisdom: int = Field(gt=0, lt=21)
    charisma: int = Field(gt=0, lt=21)
    alive: bool


@router.get("/", status_code=status.HTTP_200_OK)
async def print_chars(db: db_dependency):
    return db.query(Characters).all()


@router.post("/new-character", status_code=status.HTTP_201_CREATED)
async def create_char(db: db_dependency, new_char: CharacterRequest):
    character_model = Characters(**new_char.model_dump())

    db.add(character_model)
    db.commit()


@router.get("/{char_id}", status_code=status.HTTP_200_OK)
async def get_char_by_id(db: db_dependency, char_id: int = Path(gt=0, lt=100)):
    char_model = db.query(Characters).filter(Characters.id == char_id).first()
    if char_model is not None:
        return char_model
    raise HTTPException(status_code=404, detail='Char ID not found')


@router.post("/update/{char_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_char(db: db_dependency,
                      char_request: CharacterRequest,
                      char_id: int = Path(gt=0, lt=25)):
    char_model = db.query(Characters).filter(Characters.id == char_id).first()
    if char_model is None:
        raise HTTPException(status_code=404, details='not found')

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

