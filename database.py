from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:112490@localhost:1000/milk'

# check_same_thread: False mandates only one thread active at a time
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#bind to engine above. ensure autocommit/autoflush are false
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
