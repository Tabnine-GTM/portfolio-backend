import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.dependencies import get_db
from app.schemas.user import UserCreate
from app.crud.user import create_user
from app.database import Base

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)


# Add this function to create tables
def setup_database():
    Base.metadata.create_all(bind=engine)


def seed_db(db):
    # Create a test user
    test_user = UserCreate(
        username="testuser", email="testuser@example.com", password="testpassword"
    )
    create_user(db, test_user)


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    setup_database()
    yield


@pytest.fixture(scope="function")
def db():
    connection = engine.connect()
    transaction = connection.begin()
    db = TestingSessionLocal(bind=connection)
    try:
        seed_db(db)
        yield db
    finally:
        db.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]


@pytest.fixture(scope="function")
def test_user(db):
    user = create_user(
        db,
        UserCreate(
            username="testuser", email="testuser@example.com", password="testpassword"
        ),
    )
    return user
