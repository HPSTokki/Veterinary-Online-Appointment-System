from sqlmodel import SQLModel, Field
from sqlalchemy import String
from datetime import datetime

class UserAccount(SQLModel, table=True):
    __tablename__: str = "users"
    
    id: int = Field(default=None, primary_key=True)
    email: str = Field(sa_type=String, max_length=255, unique=True, index=True)
    password_hash: str = Field(sa_type=String)
    role: str = Field(sa_type=String, default="customer")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
class Client(SQLModel, table=True):
    __tablename__: str = "clients"
    
    id: int = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id")
    full_name: str = Field(sa_type=String)
    mobile_no: str | None = Field(default=None, sa_type=String)
    tel_no: str | None = Field(default=None, sa_type=String)
    preferred_contact_method: str = Field(sa_type=String, default="Mobile No.")
    address: str = Field(sa_type=String)
    is_new_client: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
class Pet(SQLModel, table=True):
    __tablename__: str = "pets"

    id: int = Field(default=None, primary_key=True)
    client_id: int = Field(default=None, foreign_key="clients.id")
    name: str = Field(sa_type=String)
    breed: str = Field(sa_type=String)
    species_type: str = Field(sa_type=String)
    is_spayed_neutered: bool = Field(default=False)
    weight_kg: float | None = None
    date_of_birth: datetime
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class Service(SQLModel, table=True):
    __tablename__: str = "services"
    
    id: int = Field(default=None, primary_key=True)
    name: str = Field(sa_type=String, unique=True, index=True)
    duration_mins: int
    staff_type: str = Field(sa_type=String) 

class Appointment(SQLModel, table=True):
    __tablename__: str = "appointments"
    
    id: int = Field(default=None, primary_key=True)
    pet_id: int = Field(default=None, foreign_key="pets.id")
    client_id: int = Field(default=None, foreign_key="clients.id")
    service_id: int = Field(default=None, foreign_key="services.id")
    appointment_date: datetime
    start_time: datetime
    end_time: datetime
    visit_type_code: str = Field(sa_type=String)
    chief_complaint: str = Field(sa_type=String)
    booking_source: str = Field(sa_type=String)
    status: str = Field(sa_type=String)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)