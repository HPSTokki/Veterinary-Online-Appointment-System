from fastapi import APIRouter

from src.deps.session import SessionDep
from src.deps.dependencies import CurrentUser
from src.models.appointment_models import Client
from src.dtos.user_dtos import InsertClient, UpdateClient, ReadClient
from src.services.client_service import ClientService

router = APIRouter(prefix="/client", tags=["Client"])

@router.post("/profile", response_model=ReadClient, status_code=201)
def create_client(client_data: InsertClient, session: SessionDep, current_user: CurrentUser):
    service = ClientService(session)
    return service.create_client(client_data, current_user.id)

@router.get("/profile/me", response_model=ReadClient, status_code=201)
def get_client(session: SessionDep, current_user: CurrentUser):
    service = ClientService(session)
    return service.get_client(current_user.id)

@router.put("/profile/me", response_model=ReadClient, status_code=201)
def update_client(client_data: UpdateClient, session: SessionDep, current_user: CurrentUser):
    service = ClientService(session)
    return service.update_client(client_data, current_user.id)