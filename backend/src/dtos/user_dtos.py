from pydantic import BaseModel
from datetime import datetime

class InsertUser(BaseModel):
    email: str
    password_hash: str

class ReadUser(BaseModel):
    id: int
    email: str
    role: str
    is_active: bool

class UpdateUser(BaseModel):
    password_hash: str

class ListReadUser(BaseModel):
    users: list[ReadUser]
    
class InsertClient(BaseModel):
    user_id: int | None = None
    full_name: str
    mobile_no: str | None = None
    tel_no: str | None = None
    preferred_contact_method: str | None = "Mobile No."
    address: str 

class ReadClient(BaseModel):
    id: int
    user_id: int | None = None
    full_name: str
    mobile_no: str | None = None
    tel_no: str | None = None
    preferred_contact_method: str | None = None
    address: str | None = None
    is_new_client: bool
    created_at: datetime
    
    email: str | None = None

class UpdateClient(BaseModel):
    mobile_no: str | None = None
    tel_no: str | None = None
    preferred_contact_method: str = "Mobile No."
    address: str | None = None
    is_new_client: bool | None = True 

class ListResponseClient(BaseModel):
    clients: list[ReadClient]