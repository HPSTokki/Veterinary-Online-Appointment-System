from pydantic import BaseModel
from datetime import datetime

class InsertPet(BaseModel):
    name: str
    breed: str
    species_type: str
    is_spayed_neutered: bool
    weight_kg: float | None = None
    date_of_birth: datetime
    sex: str

class ReadPet(BaseModel):
    id: int
    client_id: int
    name: str
    breed: str
    species_type: str
    is_spayed_neutered: bool
    weight_kg: float | None = None
    date_of_birth: datetime
    sex: str
    
class UpdatePet(BaseModel):
    is_spayed_neutered: bool | None = None
    weight_kg: float | None = None

class ListReadPet(BaseModel):
    pets: list[ReadPet]