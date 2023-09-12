from fastapi import FastAPI
from routers import auth, characters #import router files
from database import engine
import models

app = FastAPI()

app.include_router(auth.router) #connect the two files in project/routers
app.include_router(characters.router)

models.Base.metadata.create_all(bind=engine) #creates dndrecord.db everything from database and models


@app.get("/")
async def root():
    return {"message": "UI free DND character tracker"}


