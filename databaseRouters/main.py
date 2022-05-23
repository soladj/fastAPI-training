from typing import List

from fastapi import FastAPI, Depends
from pydantic import BaseModel

from databaseRouters.models import Note, NoteIn

from databaseRouters.database import database, notes

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(
    Note.make_router(),
    prefix='/notes',
    tags=["Notes"]
)
