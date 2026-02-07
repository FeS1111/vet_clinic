from fastapi import FastAPI

from fastapi.responses import RedirectResponse
from ui.router import router as ui_router
from db import Base, engine
from patients.router import router as patients_router

app = FastAPI(title="Ветеринарная клиника")
app.include_router(ui_router)

# Упрощенно: создаём таблицы при старте (для задания ок; позже можно Alembic)
Base.metadata.create_all(bind=engine)

app.include_router(patients_router)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/ui/patients", status_code=303)


@app.get("/health")
async def health():
    return {"status": "ok"}
