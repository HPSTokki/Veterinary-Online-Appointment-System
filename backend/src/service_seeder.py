from sqlmodel import Session, select
from src.models.appointment_models import Service
from src.deps.session import engine

def seed_service():
    with Session(engine) as session:
        existing = session.exec(select(Service)).all()
        if existing:
            return
        services = [
            Service(name="Wellness", duration_mins=30, staff_type="doctor", price=600),
            Service(name="Vaccination", duration_mins=30, staff_type="doctor", price=700),
            Service(name="Check Up", duration_mins=30, staff_type="doctor", price=580),
            Service(name="Grooming", duration_mins=60, staff_type="groomer", price=650),
            Service(name="Diagnostic", duration_mins=30, staff_type="doctor", price=770),
            Service(name="Ultrasound", duration_mins=30, staff_type="doctor", price=2150),
            Service(name="Fecalysis", duration_mins=30, staff_type="doctor", price=420),
        ]
        session.add_all(services)
        session.commit()


seed_service()