from pydantic import BaseModel, ConfigDict
from datetime import datetime

class InsertAppointment(BaseModel):
    pet_id: int
    service_id: int
    appointment_date: datetime
    start_time: datetime
    end_time: datetime
    visit_type_code: str
    chief_complaint: str
    booking_source: str
    status: str

class ReadAppointment(BaseModel):
    id: int 
    pet_id: int
    client_id: int
    service_id: int
    appointment_date: datetime
    start_time: datetime
    end_time: datetime
    visit_type_code: str
    chief_complaint: str
    booking_source: str
    status: str
    created_at: datetime
    
    service_name: str | None = None
    
class UpdateAppointment(BaseModel):
    appointment_date: datetime | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    visit_type_code: str | None = None
    chief_complaint: str | None = None
    status: str | None = None

class ListReadAppointment(BaseModel):
    appointments: list[ReadAppointment]
    
class ReadService(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    duration_mins: int
    staff_type: str