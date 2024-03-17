from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel

from notes_app.model import Note, NoteRead, NoteCreate
from notes_app.main import app, origins, get_session
from notes_app import settings


def test_home_notes():
    client = TestClient(app=app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"Nextjs FastAPI Notes-App"}


def test_get_single_note():
    connection_string = str(settings.TEST_DATABASE_URL).replace("postgresql", "postgresql+psycopg")
    engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        def get_session_override():
            return session
        
        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app=app)
        
        response = client.get("/notes/55")
        data = response.json()
        print(data)
        assert response.status_code == 200
        assert data == {
  "task": "whyy",
  "is_completed": False
}



def test_get_all_notes():
    connection_string = str(settings.TEST_DATABASE_URL).replace("postgresql", "postgresql+psycopg")
    engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        def get_session_override():
            return session
        
        app.dependency_overrides[get_session] = get_session_override

        client = TestClient(app=app)

        response = client.get("/notes/")
        data = response.json()
        print(data)
        assert response.status_code == 200


def test_create_note():
    connection_string = str(settings.TEST_DATABASE_URL).replace("postgresql", "postgresql+psycopg")
    engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        def get_session_override():
            return session
        
        app.dependency_overrides[get_session] = get_session_override

        client = TestClient(app=app)

        data = {"task": "ahsan", "is_completed": True}
        response = client.post("/notes/", json=data)
        data = response.json()

        assert response.status_code == 200
        assert data == data



