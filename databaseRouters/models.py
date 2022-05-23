from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status

from pydantic import BaseModel, Field

from databaseRouters.database import database, notes


class PaginationParameters:
    def __init__(
        self,
        offset: int = 0,
        limit: int = 10
    ):
        self.offset = offset
        self.limit = limit


class NoteIn(BaseModel):
    text: str
    completed: bool

class Note(BaseModel):
    id: int
    text: str
    completed: bool

    @classmethod
    def make_router(cls) -> APIRouter:
        router = APIRouter()

        @router.get('/', response_model=List[Note])
        async def list_notes(pagination: PaginationParameters = Depends()):
            query = notes.select()
            note_list = await database.fetch_all(query)
            return note_list[pagination.offset:pagination.limit]

        @router.get(
            '/{note_id}',
            response_model=Note,
            responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}}
        )
        async def get_note(note_id: int):
            query = notes.select().where(notes.c.id==note_id)
            note = await database.fetch_one(query)
            if note:
                return {**note}
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) 

        @router.post("/", response_model=Note)
        async def create_note(note: NoteIn):
            query = notes.insert().values(text=note.text, completed=note.completed)
            last_record_id = await database.execute(query)
            return {**note.dict(), "id": last_record_id}

        return router
