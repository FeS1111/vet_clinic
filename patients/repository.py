from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Patient


class PatientRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, patient_id: int) -> Patient | None:
        return self.db.get(Patient, patient_id)

    def get_by_phone(self, phone: str) -> Patient | None:
        stmt = select(Patient).where(Patient.phone == phone)
        return self.db.scalar(stmt)

    def list(self, limit: int = 50, offset: int = 0) -> list[Patient]:
        stmt = select(Patient).order_by(Patient.id.desc()).limit(limit).offset(offset)
        return list(self.db.scalars(stmt).all())

    def add(self, patient: Patient) -> Patient:
        self.db.add(patient)
        self.db.commit()
        self.db.refresh(patient)
        return patient

    def delete(self, patient: Patient) -> None:
        self.db.delete(patient)
        self.db.commit()
