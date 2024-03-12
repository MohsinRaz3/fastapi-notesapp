from sqlmodel import Field, SQLModel, create_engine
from typing import Optional
import os

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

databasekey = os.getenv('NEON_DB')
engine = create_engine(databasekey)

