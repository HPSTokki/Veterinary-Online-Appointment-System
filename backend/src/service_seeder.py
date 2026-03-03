from sqlmodel import Session, select
from src.models.appointment_models import Service
from src.deps.session import engine

def seed_service():
    with Session(engine) as session:
        existing = session.exec(select(Service)).all()
        if existing:
            return
        services = [
            Service(name="Wellness", duration_mins=30, staff_type="doctor"),
            Service(name="Vaccination", duration_mins=30, staff_type="doctor"),
            Service(name="Check Up", duration_mins=30, staff_type="doctor"),
            Service(name="Grooming", duration_mins=60, staff_type="groomer"),
            Service(name="Diagnostic", duration_mins=30, staff_type="doctor"),
            Service(name="Ultrasound", duration_mins=30, staff_type="doctor"),
            Service(name="Fecalysis", duration_mins=30, staff_type="doctor"),
        ]
        session.add_all(services)
        session.commit()


seed_service()