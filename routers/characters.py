from typing import Annotated
from fastapi import APIRouter, Depends, Path, HTTPException
from pydantic import Field, BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from starlette import status
from database import SessionLocal, engine
from models import Characters, Players
from routers.auth import get_current_user

router = APIRouter(
    prefix='/characters',  # everything here is under /characters
    tags=['characters']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


user_dependency = Annotated[dict, Depends(get_current_user)]
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
    game_id: int = Field(gt=0)


# Read all characters by player. Available to everyone.
@router.get("/", status_code=status.HTTP_200_OK)
async def print_chars(db: db_dependency):

    with engine.connect() as con:
        rs = con.execute(text('SELECT name, username, world as player, world, alive FROM characters '
                              'JOIN players ON players.id=characters.owner_id '
                              'JOIN games ON games.id=characters.game_id '
                              'ORDER BY world DESC'))
        rs_dict = rs.mappings().all()

    return rs_dict


# Returns all living characters by username and game world
@router.get("/living-chars", status_code=status.HTTP_200_OK)
async def print_chars(db: db_dependency):
    with engine.connect() as con:
        rs = con.execute(text('SELECT name, username as player, world, alive FROM characters '
                              'JOIN players ON players.id=characters.owner_id '
                              'JOIN games ON games.id=characters.game_id '
                              'WHERE alive = True '
                              'ORDER BY world DESC'))
        rs_dict = rs.mappings().all()
    return rs_dict


# Returns all dead characters
@router.get("/dead-chars", status_code=status.HTTP_200_OK)
async def print_chars(db: db_dependency):
    with engine.connect() as con:
        rs = con.execute(text('SELECT name, username as player, world, alive FROM characters '
                              'JOIN players ON players.id=characters.owner_id '
                              'JOIN games ON games.id=characters.game_id '
                              'WHERE alive = FALSE '
                              'ORDER BY world DESC'))
        rs_dict = rs.mappings().all()
    return rs_dict


# Create a character. Must be logged in. Owner ID of the character is tied to creator's ID
@router.post("/new-character", status_code=status.HTTP_201_CREATED)
async def create_char(db: db_dependency, new_char: CharacterRequest, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Not Authorized')

    character_model = Characters(**new_char.model_dump(), owner_id=user.get('id'))

    with engine.connect() as con:
        con.execute(text(f"INSERT INTO characters (name, character_class, level, race, current_exp, strength, dexterity, constitution, intelligence, wisdom, charisma, alive, owner_id, game_id) "
                         f"VALUES ('{character_model.name}', '{character_model.character_class}', {character_model.level}, "
                         f"'{character_model.race}', {character_model.current_exp}, {character_model.strength}, {character_model.dexterity}, "
                         f"{character_model.constitution}, {character_model.intelligence}, {character_model.wisdom}, "
                         f"{character_model.charisma}, {character_model.alive}, {user.get('id')}, {character_model.game_id})"))

        con.commit()

# Allows registered users to search for specific characters by character name.
@router.get("/{char_name}", status_code=status.HTTP_200_OK)
async def get_char_by_name(db: db_dependency, user: user_dependency,
                           char_name: str = Path(min_length=3, max_length=20)):
    if user is None:
        raise HTTPException(status_code=401, detail="not authorized")

    with engine.connect() as con:
        rs = con.execute(text("SELECT * FROM characters "
                              f"WHERE name = '{char_name}'"))
        rs_dict = rs.mappings().all()

    if len(rs_dict) > 0:
        return rs_dict

    raise HTTPException(status_code=404, detail='Char Name not found')


# Allow users to update only their characters.
@router.post("/update/{char_id}", status_code=status.HTTP_204_NO_CONTENT)  # update
async def update_char(db: db_dependency,
                      char_request: CharacterRequest,
                      user: user_dependency,
                      char_id: int = Path(gt=0, lt=25)):

    with engine.connect() as con:
        rs = con.execute(text(f"SELECT owner_id FROM characters WHERE id = {char_id}"))
        rs_list = rs.mappings().all()
        rs_dict = rs_list[0]


        if rs_dict["owner_id"] == user.get('id'):
            con.execute(text(f"UPDATE characters SET "
                             f"name = '{char_request.name}', character_class = '{char_request.character_class}', "
                             f"level = {char_request.level}, race = '{char_request.race}', "
                             f"current_exp = {char_request.current_exp}, strength = {char_request.strength}, "
                             f"dexterity = {char_request.dexterity}, constitution = {char_request.constitution}, "
                             f"intelligence = {char_request.intelligence}, wisdom = {char_request.wisdom}, "
                             f"charisma = {char_request.charisma}, alive = {char_request.alive}, owner_id = {user.get('id')}, "
                             f"game_id = {char_request.game_id} "
                             f"WHERE id = {char_id}"))
            con.commit()

        else:
            raise HTTPException(status_code=404, detail='not found')

    char_model = db.query(Characters).filter(Characters.id == char_id).first()

    if user.get('id') != char_model.owner_id:
        raise HTTPException(status_code=401, detail="Can't update someone else's character bud. Not Authorized.")

    elif char_model is None:
        raise HTTPException(status_code=404, detail='not found')
