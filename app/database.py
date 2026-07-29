from sqlmodel import SQLModel, create_engine

DATABASE_URL = "sqlite:///./jobtracker.db"
engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)