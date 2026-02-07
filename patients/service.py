from __future__ import annotations

from sqlalchemy.orm import Session

from models import Patient
from patients.repository import PatientRepository
from patients.schemas import PatientCreate, PatientUpdate


class DomainError(Exception):
    pass


class NotFoundError(DomainError):
    pass


class ConflictError(DomainError):
    pass


class PatientService:
    def __init__(self, db: Session) -> None:
        self.repo = PatientRepository(db)

    def create(self, data: PatientCreate) -> Patient:
        if data.phone and self.repo.get_by_phone(data.phone):
            raise ConflictError("Пациент с таким телефоном уже существует.")

        patient = Patient(
            first_name=data.first_name,
            last_name=data.last_name,
            owner_name=data.owner_name,
            phone=data.phone,
            email=str(data.email) if data.email else None,
            birth_date=data.birth_date,
            species=data.species,
            breed=data.breed,
        )
        return self.repo.add(patient)

    def get(self, patient_id: int) -> Patient:
        patient = self.repo.get(patient_id)
        if not patient:
            raise NotFoundError("Пациент не найден.")
        return patient

    def list(self, limit: int = 50, offset: int = 0) -> list[Patient]:
        return self.repo.list(limit=limit, offset=offset)

    def update(self, patient_id: int, data: PatientUpdate) -> Patient:
        patient = self.get(patient_id)

        if data.phone and data.phone != patient.phone:
            if self.repo.get_by_phone(data.phone):
                raise ConflictError("Пациент с таким телефоном уже существует.")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(patient, field, value)

        self.repo.db.commit()
        self.repo.db.refresh(patient)
        return patient

    def delete(self, patient_id: int) -> None:
        patient = self.get(patient_id)
        self.repo.delete(patient)
