import pytest

from sqlmodel import SQLModel, create_engine, Session

from backend.src.deps.security import hash_password, verify_password
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
    """ 
        This one already does the get_all_user function so no need for another
    """
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
    expected_email = ["mockmail@gmail.com", "mockmail2@gmail.com"]
    expected_id = [1, 2]
    assert result != []
    for id, task in enumerate(result):
        assert task.email == expected_email[id]
        assert task.id == expected_id[id]
        
def test_get_all_user_none(session):
    """ 
        Wrote this test to double check empty return values
    """
    service = UserService(session)
    result = service.get_all_user()
    assert result == []

def test_get_one_user(session):
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
    result = service.get_all_user(email="mockmail@gmail.com")
    assert result != []
    assert result[0].email == "mockmail@gmail.com"
    assert result[0].id == 1
    