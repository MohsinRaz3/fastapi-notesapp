from sqlmodel import Session, SQLModel, select, create_engine
from .model import Note, NoteCreate, NoteRead
from fastapi import FastAPI, HTTPException, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List, Annotated
from notes_app import settings


connection_string = str(settings.DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine( connection_string, connect_args= {"sslmode" : "require"}, pool_recycle=300)

# Function to create tables on startup
async def create_tables():
    SQLModel.metadata.create_all(engine)
    
@asynccontextmanager
async def lifespan(app: FastAPI):
     await create_tables()
     yield

app: FastAPI = FastAPI(
    title="NoteApp",
    description="A note taking app",
    docs_url="/docs",
    version="v1",
    lifespan=lifespan
)

origins = [
    "https://fastapi-notesapp.onrender.com/",
    "https://fastapi-notesapp.onrender.com",
    "https://fastapi-notesapp.onrender.com/notes",
    "https://fastapi-notesapp.onrender.com/notes/",
    "https://fastapi-sqlmodel-1.onrender.com/",
    "http://localhost:3000/",
    "http://localhost:3000",
    "http://localhost:3001/",
    "https://notes-fastapi.vercel.app",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Dependency function
async def get_session():
    with Session(engine) as session:
           yield session

@app.get("/")
async def home_notes():
    return {"message":"Nextjs FastAPI Notes-App"}

#Get single note
@app.get("/notes/{note_id}", response_model=NoteRead)
async def get_single_note(note_id: int, session: Annotated[Session, Depends(get_session)]):
    note_data = session.get(Note, note_id)
    if not note_data:
        raise HTTPException(status_code=404, detail="Note not found")
    return note_data

# FastAPI endpoint for getting all notes
@app.get("/notes/",response_model=List[NoteRead])
async def get_all_notes(session: Annotated[Session, Depends(get_session)])-> List[NoteRead]:
        notes = session.exec(select(Note)).all()
        if not notes:
            raise HTTPException(status_code=404,detail="notes not found")
        return notes
    
# POST FastAPI endpoint for heroes
@app.post("/notes/") 
async def create_note(note: NoteCreate,session: Annotated[Session, Depends(get_session)]):
        db_note = Note.model_validate(note) 
        session.add(db_note)
        session.commit()
        session.refresh(db_note)
        return db_note

#FastAPI endpoint to Update Heros    
@app.patch("/notes/{note_id}",response_model=NoteRead)
async def update_note(note_id : int, note:Note,session: Annotated[Session, Depends(get_session)]):
        
        note_item = session.get(Note, note_id)
        if not note_item:
             raise HTTPException(status_code=404, detail="not note found")
        
        note_data = note.model_dump(exclude_unset=True)
        for key, value in note_data.items():
             setattr(note_item, key, value)

        session.add(note_item)
        session.commit()
        session.refresh(note_item)
        return note_item


@app.delete("/notes/{note_id}")
def delete_note(note_id:int,session: Annotated[Session, Depends(get_session)]):
        notee = session.get(Note,note_id)
        if not notee:
            raise HTTPException(status_code=404,detail="hero not found")
        session.delete(notee)
        session.commit()
        return {"message": "item is deleted!"}


if __name__ == "__main__": 
    import uvicorn
    uvicorn.run("main:app", reload=True)