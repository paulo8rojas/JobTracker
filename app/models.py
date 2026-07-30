from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class Application(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company: str
    role_title: str
    status: str = "applied"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ApplicationCreate(SQLModel):
    company: str
    role_title: str
    status: str = "applied"

class ApplicationUpdate(SQLModel):
    company: Optional[str] = None
    role_title: Optional[str] = None
    status: Optional[str] = None