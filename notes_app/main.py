from sqlmodel import Session, SQLModel, select
from .model import engine, Note, NoteCreate, NoteRead
from fastapi import FastAPI, HTTPException, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List, Annotated

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
    "https://fastapi-sqlmodel.onrender.com",
    "https://fastapi-sqlmodel.onrender.com/heroes",
    "https://fastapi-sqlmodel-1.onrender.com",
    "http://localhost:3000",
    "https://localhost:3000",
    "https://localhost:3001",
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

# Function to create tables on startup
async def create_tables():
    SQLModel.metadata.create_all(engine)

#Dependency function
async def get_session():
    with Session(engine) as session:
           yield session

# Event to create tables on startup
# @app.on_event("startup")
# async def startup_event():
#     await create_tables()

#Home route
@app.get("/")
async def home_notes():
    return {"message":"Nextjs FastAPI Notes-App"}

#Get single hero
@app.get("/notes/", response_model=NoteRead)
async def get_single_note(note_id: int, session: Annotated[Session, Depends(get_session)]):
    note_data = session.get(Note, note_id)
    # If note_data is None, it means the note with the given ID doesn't exist
    if not note_data:
        raise HTTPException(status_code=404, detail="Note not found")
    return note_data

# FastAPI endpoint for getting heroes
@app.get("/notes",response_model=List[NoteRead])
async def get_all_notes(session: Annotated[Session, Depends(get_session)])-> List[NoteRead]:
        notes = session.exec(select(Note)).all()
        if not notes:
            raise HTTPException(status_code=404,detail="notes not found")
        return notes
    
# FastAPI endpoint for creating heroes
@app.post("/notes") 
async def create_note(note: NoteCreate = Body(embed=True), session: Session = Depends(get_session)):
        db_note = Note.model_validate(note) 
        session.add(db_note)
        session.commit()
        session.refresh(db_note)
        return db_note

#FastAPI endpoint to Update Heros    
@app.patch("/notes",response_model=NoteRead)
async def update_note(note_id : int, note:Note, session: Session = Depends(get_session)):
        
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


@app.delete("/notes/")
def delete_note(note_id:int, session: Session = Depends(get_session)):
        notee = session.get(Note,note_id)
        if not notee:
            raise HTTPException(status_code=404,detail="hero not found")
        session.delete(notee)
        session.commit()
        return {"message": "item is deleted!"}


if __name__ == "__main__": 
    import uvicorn
    uvicorn.run("main:app", reload=True)