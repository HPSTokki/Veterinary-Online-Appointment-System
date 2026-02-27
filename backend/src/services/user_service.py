from sqlmodel import Session, select, col
from typing import cast

from backend.src.models.appointment_models import UserAccount, Client
from backend.src.dtos.user_dtos import InsertUser, ReadUser, ListReadUser, UpdateUser
from backend.src.deps.security import hash_password, verify_password

class UserService():
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def register_user(self, reg_data: InsertUser) -> ReadUser:
        user = UserAccount(**reg_data.model_dump(exclude_unset=True))
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return cast(ReadUser, user)
    
    def get_all_user(self, email: str | None = None) -> list[ReadUser]:
        stmt = select(UserAccount)
        if email:
            stmt = stmt.where(col(UserAccount.email).ilike(f"%{email}%"))
        users = self.session.exec(stmt).all()
        return cast(list[ReadUser], users)