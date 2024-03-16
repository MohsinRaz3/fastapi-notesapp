from sqlmodel import Field, SQLModel
from typing import Optional


class NoteBase(SQLModel):
    task: str 
    is_completed: Optional[bool] = False

class Note(NoteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
 
class NoteCreate(NoteBase):
    pass

class NoteRead(NoteBase):
    id:int

class NoteUpdate(SQLModel):
    task: Optional[str] = None
    is_completed: Optional[bool] = False