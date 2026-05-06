from fastapi import APIRouter

from src.deps.session import SessionDep
from src.deps.dependencies import CurrentUser

from src.models.appointment_models import UserAccount
from src.dtos.user_dtos import InsertUser, UpdateUser, ReadUser, ListReadUser, UpdatePassword

from src.services.user_service import UserService, oauth2_form

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/auth/reg", response_model=ReadUser)
def register_user(session: SessionDep, reg_data: InsertUser):
    service = UserService(session)
    new_user = service.register_user(reg_data)
    return new_user

@router.post("/auth/login", response_model=dict)
def login_user(session: SessionDep, form: oauth2_form) -> dict:
    service = UserService(session)
    login_user = service.login_user(form)
    return login_user

from src.dtos.user_dtos import ForgotPasswordRequest, ResetPasswordRequest, UpdatePassword

@router.post("/auth/forgot-password")
async def forgot_password(body: ForgotPasswordRequest, session: SessionDep):
    service = UserService(session)
    return await service.forgot_password(body.email)

@router.post("/auth/reset-password")
def reset_password(body: ResetPasswordRequest, session: SessionDep):
    service = UserService(session)
    return service.reset_password(body)

@router.patch("/auth/password")
def update_password(body: UpdatePassword, session: SessionDep, current_user: CurrentUser):
    service = UserService(session)
    return service.update_password(body, current_user.id)

@router.get("/me")
def get_me(current: CurrentUser):
    return current