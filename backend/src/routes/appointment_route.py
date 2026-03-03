from datetime import datetime
from fastapi import APIRouter, Query
from src.deps.session import SessionDep
from src.deps.dependencies import CurrentUser
from src.dtos.appointment_dtos import InsertAppointment, ListReadAppointment, ReadAppointment, UpdateAppointment
from src.services.appointment_service import AppointmentService

router = APIRouter(prefix="/appointment", tags=["Appointments"])

@router.get("/available-slots")
def get_available_slots(service_id: int, session: SessionDep, current_user: CurrentUser, date: datetime = Query(..., description="Format: YYYY-MM-DD")):
    service = AppointmentService(session)
    return service.get_available_slots(service_id, date)

@router.post("/", response_model=ReadAppointment, status_code=201)
def create_appointment(body: InsertAppointment, session: SessionDep, current_user: CurrentUser):
    service = AppointmentService(session)
    return service.create_appointment(body, current_user.id)

@router.get("/", response_model=ListReadAppointment)
def get_appointments(session: SessionDep, current_user: CurrentUser):
    service = AppointmentService(session)
    return service.get_appointments(current_user.id)

@router.get("/{appointment_id}", response_model=ReadAppointment)
def get_appointment(appointment_id: int, session: SessionDep, current_user: CurrentUser):
    service = AppointmentService(session)
    return service.get_appointment(appointment_id, current_user.id)

@router.put("/{appointment_id}", response_model=ReadAppointment)
def update_appointment(appointment_id: int, update_data: UpdateAppointment, session: SessionDep, current_user: CurrentUser):
    service = AppointmentService(session)
    return service.update_appointment(appointment_id, current_user.id, update_data)