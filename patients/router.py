from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import get_db
from patients.schemas import PatientCreate, PatientOut, PatientUpdate
from patients.service import PatientService, ConflictError, NotFoundError

router = APIRouter(prefix="/patients", tags=["patients"])


def get_service(db: Session = Depends(get_db)) -> PatientService:
    return PatientService(db)


@router.post("", response_model=PatientOut, status_code=status.HTTP_201_CREATED)
def create_patient(payload: PatientCreate, service: PatientService = Depends(get_service)):
    try:
        return service.create(payload)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("", response_model=list[PatientOut])
def list_patients(limit: int = 50, offset: int = 0, service: PatientService = Depends(get_service)):
    return service.list(limit=limit, offset=offset)


@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: int, service: PatientService = Depends(get_service)):
    try:
        return service.get(patient_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{patient_id}", response_model=PatientOut)
def update_patient(patient_id: int, payload: PatientUpdate, service: PatientService = Depends(get_service)):
    try:
        return service.update(patient_id, payload)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, service: PatientService = Depends(get_service)):
    try:
        service.delete(patient_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
