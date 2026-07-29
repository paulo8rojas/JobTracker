from fastapi import FastAPI
from sqlmodel import Session, select

from app.database import engine, create_db_and_tables
from app.models import Application

app = FastAPI(title="Job Application Tracker")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/applications")
def list_applications():
    with Session(engine) as session:
        return session.exec(select(Application)).all()