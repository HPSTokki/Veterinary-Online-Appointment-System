from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel import select, Session

from src.deps.security import authDeps, decode_access_token
from src.deps.session import SessionDep
from src.models.appointment_models import UserAccount

def get_current_user(token: authDeps, session: SessionDep) -> UserAccount:
    payload = decode_access_token(token)
    
    user_id: int | None = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token Payload",
        )
    
    user = session.get(UserAccount, int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive Account",
        )
    return user

CurrentUser = Annotated[UserAccount, Depends(get_current_user)]