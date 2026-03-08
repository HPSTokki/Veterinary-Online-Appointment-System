from typing import cast
from sqlmodel import Session, select, col

from src.exception import PetHasActiveAppointments, PetNotFound, ClientProfileNotExist
from src.models.appointment_models import Appointment, Pet, Client
from src.dtos.pet_dtos import InsertPet, ListReadPet, UpdatePet, ReadPet

class PetService():
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def _get_client(self, user_id: int) -> Client:
        client = self.session.exec(
            select(Client).where(col(Client.user_id) == user_id)
        ).first()
        if not client:
            raise ClientProfileNotExist
        return client
    
    def _get_pet(self, pet_id: int, client_id: int) -> Pet:
        pet = self.session.exec(
            select(Pet).where(
                col(Pet.id) == pet_id,
                col(Pet.client_id) == client_id
            )
        ).first()
        if not pet:
            raise PetNotFound
        return cast(Pet, pet)
    
    def create_pet(self, pet_data: InsertPet, user_id: int) -> ReadPet:
        client = self._get_client(user_id)
        pet = Pet(**pet_data.model_dump(), client_id=client.id)
        self.session.add(pet)
        self.session.commit()
        self.session.refresh(pet)
        return ReadPet.model_validate(pet, from_attributes=True)
    
    def get_pets(self, user_id: int) -> ListReadPet:
        client = self._get_client(user_id)
        pets = self.session.exec(
            select(Pet).where(
                col(Pet.client_id) == client.id
            )
        ).all()
        validated_pet = [ReadPet.model_validate(p, from_attributes=True) for p in pets]
        return ListReadPet(pets=validated_pet)
    
    def get_pet(self, pet_id: int, user_id: int) -> ReadPet:
        client = self._get_client(user_id)
        pet = self._get_pet(pet_id, cast(int, client.id))
        return ReadPet.model_validate(pet, from_attributes=True)
    
    def update_pet(self, pet_data: UpdatePet, user_id: int, pet_id: int) -> ReadPet:
        client = self._get_client(user_id)
        pet = self._get_pet(pet_id, cast(int, client.id))
        
        for key, value in pet_data.model_dump(exclude_unset=True).items():
            setattr(pet, key, value)
        self.session.commit()
        self.session.refresh(pet)
        return ReadPet.model_validate(cast(Pet, pet), from_attributes=True)
    
    def delete_pet(self, pet_id: int, user_id: int) -> None:
        client = self._get_client(user_id)
        pet = self._get_pet(pet_id, cast(int, client.id))
        active = self.session.exec(select(Appointment).where(
            col(Appointment.pet_id) == pet.id,
            col(Appointment.status).in_(['pending', 'confirmed'])
        )).first()
        
        if active:
            raise PetHasActiveAppointments()
        
        self.session.delete(cast(Pet, pet))
        self.session.commit()