from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select, col
from typing import Annotated, cast
from fastapi.security import OAuth2PasswordRequestForm

from backend.src.models.appointment_models import UserAccount, Client
from backend.src.dtos.user_dtos import InsertUser, ReadUser, ListReadUser, UpdateUser
from backend.src.deps.security import create_access_token, hash_password, verify_password

oauth2_form = Annotated[OAuth2PasswordRequestForm, Depends()]

class UserService():
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def register_user(self, reg_data: InsertUser) -> ReadUser:
        user = UserAccount(**reg_data.model_dump(exclude_unset=True))
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return cast(ReadUser, user)
    
    def get_all_user(self) -> list[ReadUser]:
        users = self.session.exec(select(UserAccount)).all()
        return cast(list[ReadUser], users)
    
    def get_user_by_id(self, user_id: int) -> ReadUser | None:
        user = self.session.exec(select(UserAccount).where(UserAccount.id == user_id)).first()
        if not user:
            return None
        return cast(ReadUser, user)
    
    def get_user_by_email(self, email: str) -> ReadUser | None:
        user = self.session.exec(select(UserAccount).where(col(UserAccount.email).ilike(f"%{email}%"))).first()
        if not user:
            return None
        return cast(ReadUser, user)
    
#    def login_user(self, login_data: InsertUser) -> ReadUser | None:
#        stmt = select(UserAccount).where(
#            col(UserAccount.email) == login_data.email
#        )
#        result = self.session.exec(stmt).first()
#        if result is None:
#            return None
#        is_pass_valid = verify_password(
#            login_data.password_hash, result.password_hash
#        )
#        if not is_pass_valid:
#            return None
#        return cast(ReadUser, result)

    def login_user(self, form: oauth2_form):
        user = self.session.exec(
            select(UserAccount).where(col(UserAccount.email) == form.username)
        ).first()
        if not user or not verify_password(form.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive account",
            )
            
        token = create_access_token({ "sub": str(user.id), "role": str(user.role) })
        return { "access_token": token, "token_type": "bearer" }