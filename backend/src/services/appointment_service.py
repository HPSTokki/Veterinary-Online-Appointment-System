from datetime import datetime, timedelta
from typing import cast
from sqlmodel import Session, col, select
from sqlalchemy import func 

from src.exception import AppointmentNotFound, ClientProfileNotExist, ClinicIsClosed, PetNotFound, SlotUnavailable
from src.models.appointment_models import Appointment, Client, Pet, Service
from src.dtos.appointment_dtos import InsertAppointment, ReadAppointment, UpdateAppointment, ListReadAppointment

# Monday–Saturday: 10AM–6PM
# Sunday: 12PM–5PM
SCHEDULE = {
    0: {"start": 10, "end": 18},  # Monday
    1: {"start": 10, "end": 18},  # Tuesday
    2: {"start": 10, "end": 18},  # Wednesday
    3: {"start": 10, "end": 18},  # Thursday
    4: {"start": 10, "end": 18},  # Friday
    5: {"start": 10, "end": 18},  # Saturday
    6: {"start": 12, "end": 17},  # Sunday
}

STAFF_COUNT    = { "doctor": 1, "groomer": 1 }
SLOT_DURATION  = { "doctor": 30, "groomer": 60 }
LEAD_TIME_MINS = 60  # must book at least 1 hour ahead

DAILY_CAP = {
    staff: (480 // SLOT_DURATION[staff]) * STAFF_COUNT[staff]
    for staff in SLOT_DURATION
}


class AppointmentService():
    def __init__(self, session: Session) -> None:
        self.session = session

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _get_client(self, user_id: int) -> Client:
        client = self.session.exec(
            select(Client).where(col(Client.user_id) == user_id)
        ).first()
        if not client:
            raise ClientProfileNotExist
        return cast(Client, client)

    def _get_pet(self, pet_id: int, client_id: int) -> Pet:
        pet = self.session.exec(
            select(Pet).where(
                col(Pet.id) == pet_id,
                col(Pet.client_id) == client_id
            )
        ).first()
        if not pet:
            raise PetNotFound()
        return cast(Pet, pet)

    def _get_services(self, service_id: int) -> Service:
        service = self.session.get(Service, service_id)
        if not service:
            raise AppointmentNotFound()
        return service

    def _get_schedule(self, date: datetime) -> dict | None:
        """Return the day's schedule dict, or None if the clinic is closed."""
        return SCHEDULE.get(date.weekday())

    def _is_clinic_open(self, date: datetime) -> bool:
        return self._get_schedule(date) is not None

    def _get_booked_slots(self, staff_type: str, date: datetime) -> list[tuple[datetime, datetime]]:
        booked = self.session.exec(
            select(Appointment)
            .join(Service, col(Appointment.service_id) == col(Service.id))
            .where(
                col(Service.staff_type) == staff_type,
                func.date(Appointment.appointment_date) == date.date(),
                col(Appointment.status) != "cancelled"
            )
        ).all()
        return [(a.start_time, a.end_time) for a in booked]

    def _is_slot_taken(self, booked: list[tuple[datetime, datetime]], start: datetime, end: datetime) -> bool:
        return any(
            existing_start < end and existing_end > start
            for existing_start, existing_end in booked
        )

    def _to_read(self, appointment: Appointment) -> ReadAppointment:
        service = self.session.get(Service, appointment.service_id)
        pet = self.session.get(Pet, appointment.pet_id)
        result = ReadAppointment.model_validate(appointment, from_attributes=True)
        result.pet_name = pet.name if pet else None
        result.service_name = service.name if service else None
        return result

    # ── Public Methods ────────────────────────────────────────────────────────

    def get_available_slots(self, service_id: int, date: datetime) -> list[dict]:
        schedule = self._get_schedule(date)
        if not schedule:
            raise ClinicIsClosed()

        service   = self._get_services(service_id)
        staff_type = service.staff_type
        duration  = timedelta(minutes=SLOT_DURATION[staff_type])

        day_start = date.replace(hour=schedule["start"], minute=0, second=0, microsecond=0)
        day_end   = date.replace(hour=schedule["end"],   minute=0, second=0, microsecond=0)

        # For today: earliest bookable slot must be at least LEAD_TIME_MINS from now
        now = datetime.now()
        if date.date() == now.date():
            earliest = now + timedelta(minutes=LEAD_TIME_MINS)
            # Snap forward to the next clean slot boundary
            if earliest > day_start:
                elapsed = (earliest - day_start).total_seconds() / 60
                slots_elapsed = int(elapsed // SLOT_DURATION[staff_type]) + 1
                day_start = day_start + timedelta(minutes=SLOT_DURATION[staff_type] * slots_elapsed)

        # If the snapped start is already past closing, no slots available
        if day_start >= day_end:
            return []

        booked = self._get_booked_slots(staff_type, date)

        if len(booked) >= DAILY_CAP[staff_type]:
            return []

        slots = []
        cursor = day_start
        while cursor + duration <= day_end:
            slot_end = cursor + duration
            if not self._is_slot_taken(booked, cursor, slot_end):
                slots.append({"start_time": cursor, "end_time": slot_end})
            cursor += duration

        return slots

    def create_appointment(self, data: InsertAppointment, user_id: int) -> ReadAppointment:
        client  = self._get_client(user_id)
        pet     = self._get_pet(data.pet_id, cast(int, client.id))
        service = self._get_services(data.service_id)

        schedule = self._get_schedule(data.appointment_date)
        if not schedule:
            raise ClinicIsClosed()

        # Lead time guard on booking
        now = datetime.now()
        if data.appointment_date.date() == now.date():
            if data.start_time < now + timedelta(minutes=LEAD_TIME_MINS):
                raise SlotUnavailable()

        booked = self._get_booked_slots(service.staff_type, data.appointment_date)

        if len(booked) >= DAILY_CAP[service.staff_type]:
            raise SlotUnavailable()
        if self._is_slot_taken(booked, data.start_time, data.end_time):
            raise SlotUnavailable()

        appointment = Appointment(
            **data.model_dump(),
            client_id=client.id
        )
        self.session.add(appointment)
        self.session.commit()
        self.session.refresh(appointment)
        return self._to_read(appointment)

    def get_appointments(self, user_id: int) -> ListReadAppointment:
        client = self._get_client(user_id)
        appointments = self.session.exec(
            select(Appointment).where(col(Appointment.client_id) == client.id)
        ).all()
        validated_appointment = [self._to_read(a) for a in appointments]
        return ListReadAppointment(appointments=validated_appointment)

    def get_appointment(self, appointment_id: int, user_id: int) -> ReadAppointment:
        client = self._get_client(user_id)
        appointment = self.session.exec(
            select(Appointment).where(
                col(Appointment.id) == appointment_id,
                col(Appointment.client_id) == client.id
            )
        ).first()
        if not appointment:
            raise AppointmentNotFound()
        return self._to_read(appointment)

    def update_appointment(self, appointment_id: int, user_id: int, data: UpdateAppointment) -> ReadAppointment:
        client = self._get_client(user_id)
        appointment = self.session.exec(
            select(Appointment).where(
                col(Appointment.id) == appointment_id,
                col(Appointment.client_id) == client.id
            )
        ).first()
        if not appointment:
            raise AppointmentNotFound()

        if data.start_time or data.end_time or data.appointment_date:
            service    = self._get_services(appointment.service_id)
            check_date = data.appointment_date or appointment.appointment_date
            check_start = data.start_time or appointment.start_time
            check_end   = data.end_time   or appointment.end_time

            schedule = self._get_schedule(check_date)
            if not schedule:
                raise ClinicIsClosed()

            booked = self._get_booked_slots(service.staff_type, check_date)
            # Exclude this appointment's own slot from the conflict check
            booked = [(s, e) for s, e in booked if s != appointment.start_time]

            if self._is_slot_taken(booked, check_start, check_end):
                raise SlotUnavailable()

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(appointment, key, value)
        self.session.commit()
        self.session.refresh(appointment)
        return self._to_read(appointment)