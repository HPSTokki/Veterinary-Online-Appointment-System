from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select, col
from typing import Annotated, cast
from fastapi.security import OAuth2PasswordRequestForm

from src.models.appointment_models import UserAccount, Client, PasswordResetPin
from src.dtos.user_dtos import InsertUser, ReadUser, ListReadUser, UpdateUser, UpdatePassword, ForgotPasswordRequest, ResetPasswordRequest
from src.deps.security import create_access_token, hash_password, verify_password
from src.exception import DuplicateAccountCredentials, LoginInvalidCredentials
from src.deps.emailer import send_password_reset_email

import random
from datetime import datetime, timedelta

oauth2_form = Annotated[OAuth2PasswordRequestForm, Depends()]

class UserService():
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def register_user(self, reg_data: InsertUser) -> ReadUser:
        stmt = select(UserAccount).where(col(UserAccount.email) == reg_data.email)
        result = self.session.exec(stmt).first()
        if result is not None:
            raise DuplicateAccountCredentials()
        user = UserAccount(
            email=reg_data.email,
            password_hash=hash_password(reg_data.password_hash)
        )
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

    def login_user(self, form: oauth2_form) -> dict:
        user = self.session.exec(
            select(UserAccount).where(col(UserAccount.email) == form.username)
        ).first()
        print(form.password)
        print(form.username)
        if not user or not verify_password(form.password, user.password_hash):
            raise LoginInvalidCredentials()
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive account",
            )
            
        token = create_access_token({ "sub": str(user.id), "role": str(user.role) })
        return { "access_token": token, "token_type": "bearer" }
    
    async def forgot_password(self, email: str) -> dict:
        user = self.session.exec(
            select(UserAccount).where(col(UserAccount.email) == email)
        ).first()

        # always return success — don't reveal if email exists
        if not user:
            return {"message": "If that email exists, a PIN has been sent"}

        # invalidate existing pins
        existing_pins = self.session.exec(
            select(PasswordResetPin).where(
                col(PasswordResetPin.user_id) == user.id,
                col(PasswordResetPin.used) == False
            )
        ).all()
        for p in existing_pins:
            p.used = True

        # generate 6 digit pin
        pin = str(random.randint(100000, 999999))
        expires_at = datetime.now() + timedelta(minutes=10)

        reset = PasswordResetPin(
            user_id=cast(int, user.id),
            pin=hash_password(pin),  # hash the pin for security
            expires_at=expires_at
        )
        self.session.add(reset)
        self.session.commit()

        await send_password_reset_email(
            to_email=email,
            pin=pin  # send plain pin to email
        )

        return {"message": "If that email exists, a PIN has been sent"}

    def reset_password(self, data: ResetPasswordRequest) -> dict:
        user = self.session.exec(
            select(UserAccount).where(col(UserAccount.email) == data.email)
        ).first()
        if not user:
            raise HTTPException(status_code=400, detail="Invalid request")

        # find valid pin
        reset = self.session.exec(
            select(PasswordResetPin).where(
                col(PasswordResetPin.user_id) == user.id,
                col(PasswordResetPin.used) == False,
                col(PasswordResetPin.expires_at) > datetime.now()
            )
        ).first()

        if not reset or not verify_password(data.pin, reset.pin):
            raise HTTPException(status_code=400, detail="Invalid or expired PIN")

        # update password
        user.password_hash = hash_password(data.new_password)

        # mark pin as used
        reset.used = True

        self.session.commit()
        return {"message": "Password reset successfully"}

    def update_password(self, data: UpdatePassword, user_id: int) -> dict:
        user = self.session.get(UserAccount, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not verify_password(data.current_password, user.password_hash):
            raise HTTPException(status_code=400, detail="Current password is incorrect")
        user.password_hash = hash_password(data.new_password)
        self.session.commit()
        return {"message": "Password updated successfully"}