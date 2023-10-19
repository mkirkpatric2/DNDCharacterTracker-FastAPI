from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Characters(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    character_class = Column(String)
    level = Column(Integer)
    race = Column(String)
    current_exp = Column(Integer)
    strength = Column(Integer)
    dexterity = Column(Integer)
    constitution = Column(Integer)
    intelligence = Column(Integer)
    wisdom = Column(Integer)
    charisma = Column(Integer)
    alive = Column(Boolean)
    owner_id = Column(Integer, ForeignKey('players.id'))
    game_id = Column(Integer, ForeignKey('games.id'))


class Players(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String)


class Games(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, index=True)
    world = Column(String)
    dm_id = Column(Integer, ForeignKey('players.id'))
