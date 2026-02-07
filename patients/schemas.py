from __future__ import annotations

import datetime as dt
from pydantic import BaseModel, EmailStr, Field


class PatientCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    owner_name: str = Field(min_length=1, max_length=120)

    phone: str | None = Field(default=None, max_length=30)
    email: EmailStr | None = None

    birth_date: dt.date | None = None
    species: str | None = Field(default=None, max_length=40)
    breed: str | None = Field(default=None, max_length=60)


class PatientUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=80)
    last_name: str | None = Field(default=None, min_length=1, max_length=80)
    owner_name: str | None = Field(default=None, min_length=1, max_length=120)

    phone: str | None = Field(default=None, max_length=30)
    email: EmailStr | None = None

    birth_date: dt.date | None = None
    species: str | None = Field(default=None, max_length=40)
    breed: str | None = Field(default=None, max_length=60)


class PatientOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    owner_name: str
    phone: str | None
    email: str | None
    birth_date: dt.date | None
    species: str | None
    breed: str | None

    class Config:
        from_attributes = True
