from __future__ import annotations

import datetime as dt
from sqlalchemy import Date, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    first_name: Mapped[str] = mapped_column(String(80))
    last_name: Mapped[str] = mapped_column(String(80))

    phone: Mapped[str | None] = mapped_column(String(30), unique=True, nullable=True)
    email: Mapped[str | None] = mapped_column(String(120), nullable=True)

    birth_date: Mapped[dt.date | None] = mapped_column(Date, nullable=True)

    species: Mapped[str | None] = mapped_column(String(40), nullable=True)
    breed: Mapped[str | None] = mapped_column(String(60), nullable=True)

    owner_name: Mapped[str] = mapped_column(String(120))

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
