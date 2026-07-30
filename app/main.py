from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select

from app.database import engine, create_db_and_tables
from app.models import Application, ApplicationUpdate, ApplicationCreate

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

@app.patch("/applications/{id}")
def update_application(id: int, payload: ApplicationUpdate):
    with Session(engine) as session:
        existing = session.get(Application, id)

        if existing is None:
            raise HTTPException(status_code=404, detail="Application not found")
        
        update_data = payload.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(existing, key, value)
        
        session.add(existing)
        session.commit()
        session.refresh(existing)
        return existing

@app.delete("/applications/{id}", status_code=204)
def delete_application(id: int):
    with Session(engine) as session:
        to_delete = session.get(Application, id)

        if to_delete is None:
            raise HTTPException(status_code=404, detail="Application not found")
        
        session.delete(to_delete)
        session.commit()