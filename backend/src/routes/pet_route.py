from fastapi import APIRouter

from src.deps.session import SessionDep
from src.deps.dependencies import CurrentUser
from src.dtos.pet_dtos import InsertPet, UpdatePet, ListReadPet, ReadPet
from src.services.pet_service import PetService

router = APIRouter(prefix="/pet", tags=["Pets"])

@router.post("/", response_model=ReadPet, status_code=201)
def create_pet(session: SessionDep, pet_data: InsertPet, current_user: CurrentUser):
    service = PetService(session)
    return service.create_pet(pet_data, user_id=current_user.id)

@router.get("/", response_model=ListReadPet, status_code=200)
def get_all_pets(session: SessionDep, current_user: CurrentUser):
    service = PetService(session)
    return service.get_pets(current_user.id)

@router.get("/{pet_id}", response_model=ReadPet, status_code=201)
def get_one_pet(session: SessionDep,pet_id: int, current_user: CurrentUser):
    service = PetService(session)
    return service.get_pet(pet_id, current_user.id)

@router.put("/{pet_id}", response_model=ReadPet, status_code=201)
def update_pet(session: SessionDep, update_data: UpdatePet, pet_id: int, current_user: CurrentUser):
    service = PetService(session)
    return service.update_pet(update_data, current_user.id, pet_id)