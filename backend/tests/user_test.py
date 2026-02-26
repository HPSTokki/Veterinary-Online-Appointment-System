import pytest

from sqlmodel import SQLModel, create_engine, Session

from backend.src.deps.security import hash_password
from backend.src.services.user_service import UserService
from backend.src.dtos.user_dtos import InsertUser, ReadUser

@pytest.fixture
def session():
    sqlite = "sqlite:///:memory:"
    engine = create_engine(sqlite)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_register_user(session):
    service = UserService(session)
    mock_data = [
        InsertUser(
            email="mockmail@gmail.com",
            password_hash=hash_password("mockpass123"),
        ),
        InsertUser(
            email="mockmail2@gmail.com",
            password_hash=hash_password("mockpass123"),
        )
    ]
    
    for task in mock_data:
        service.register_user(task)
        
    result = service.get_all_user()
    
    assert result is not None
    assert result[0].id == 1
    assert result[1].id == 2