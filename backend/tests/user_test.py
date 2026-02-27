from pprint import pprint
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
    for id, user in enumerate(result):
        assert user.email == expected_email[id]
        assert user.id == expected_id[id]
        assert user.role == "customer"
        
def test_get_all_user_none(session):
    """ 
        Wrote this test to double check empty return values
    """
    service = UserService(session)
    result = service.get_all_user()
    assert result == []

def test_get_one_user_by_id(session):
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
    result = service.get_user_by_id(1)
    assert result is not None
    assert result.email == "mockmail@gmail.com"
    assert result.id == 1
    assert result.role == "customer"

def test_get_one_user_by_email(session):
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
    result = service.get_user_by_email("mockmail@gmail.com")
    assert result is not None
    assert result.email == "mockmail@gmail.com"
    assert result.id == 1
    assert result.role == "customer"

def test_login_user(session):
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
    result = service.login_user(InsertUser(email="mockmail@gmail.com", password_hash="mockpass123"))
    pprint(result)
    assert result is not None
    assert result.id == 1
    assert result.role == "customer"