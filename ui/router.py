from __future__ import annotations

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from db import get_db
from patients.schemas import PatientCreate, PatientUpdate
from patients.service import PatientService, ConflictError, NotFoundError

router = APIRouter(prefix="/ui", tags=["ui"])
templates = Jinja2Templates(directory="templates")


def get_service(db: Session = Depends(get_db)) -> PatientService:
    return PatientService(db)


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
def ui_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/patients", response_class=HTMLResponse)
def ui_patients(request: Request, service: PatientService = Depends(get_service)):
    patients = service.list(limit=200, offset=0)
    return templates.TemplateResponse(
        "patients.html",
        {"request": request, "patients": patients, "error": None},
    )


@router.post("/patients")
def ui_create_patient(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    owner_name: str = Form(...),
    phone: str | None = Form(None),
    email: str | None = Form(None),
    species: str | None = Form(None),
    breed: str | None = Form(None),
    service: PatientService = Depends(get_service),
):
    try:
        payload = PatientCreate(
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            owner_name=owner_name.strip(),
            phone=(phone.strip() if phone else None),
            email=(email.strip() if email else None),
            species=(species.strip() if species else None),
            breed=(breed.strip() if breed else None),
        )
        service.create(payload)
        return RedirectResponse(url="/ui/patients", status_code=303)
    except ConflictError as e:
        patients = service.list(limit=200, offset=0)
        return templates.TemplateResponse(
            "patients.html",
            {"request": request, "patients": patients, "error": str(e)},
        )


@router.get("/patients/{patient_id}/edit", response_class=HTMLResponse)
def ui_edit_patient_form(
    request: Request,
    patient_id: int,
    service: PatientService = Depends(get_service),
):
    try:
        patient = service.get(patient_id)
        return templates.TemplateResponse(
            "patient_edit.html",
            {"request": request, "patient": patient, "error": None},
        )
    except NotFoundError:
        return RedirectResponse(url="/ui/patients", status_code=303)


@router.post("/patients/{patient_id}/edit")
def ui_edit_patient_save(
    request: Request,
    patient_id: int,
    first_name: str = Form(...),
    last_name: str = Form(...),
    owner_name: str = Form(...),
    phone: str | None = Form(None),
    email: str | None = Form(None),
    species: str | None = Form(None),
    breed: str | None = Form(None),
    service: PatientService = Depends(get_service),
):
    try:
        payload = PatientUpdate(
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            owner_name=owner_name.strip(),
            phone=(phone.strip() if phone else None),
            email=(email.strip() if email else None),
            species=(species.strip() if species else None),
            breed=(breed.strip() if breed else None),
        )
        service.update(patient_id, payload)
        return RedirectResponse(url="/ui/patients", status_code=303)
    except ConflictError as e:
        patient = service.get(patient_id)
        return templates.TemplateResponse(
            "patient_edit.html",
            {"request": request, "patient": patient, "error": str(e)},
        )
    except NotFoundError:
        return RedirectResponse(url="/ui/patients", status_code=303)


@router.post("/patients/{patient_id}/delete")
def ui_delete_patient(patient_id: int, service: PatientService = Depends(get_service)):
    try:
        service.delete(patient_id)
    except NotFoundError:
        pass
    return RedirectResponse(url="/ui/patients", status_code=303)
