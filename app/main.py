from fastapi import FastAPI
from sqlmodel import Session, select

from app.database import engine, create_db_and_tables
from app.models import Application, ApplicationCreate

app = FastAPI(title="Job Application Tracker")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/applications")
def list_applications():
    with Session(engine) as session:
        return session.exec(select(Application)).all()

@app.post("/applications")
def create_application(payload: ApplicationCreate):
    new_app = Application(company=payload.company, role_title=payload.role_title, status=payload.status)
    with Session(engine) as session:
        session.add(new_app)
        session.commit()
        session.refresh(new_app)
        return new_app