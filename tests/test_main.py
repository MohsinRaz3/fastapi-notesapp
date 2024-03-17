from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session

from notes_app.model import Note, NoteRead, NoteCreate
from notes_app.main import app, origins, get_session
from notes_app import settings


def test_read_home():
    client = TestClient(app=app)
    response = client.get("/")
    assert response.status == 200

test_read_home()
