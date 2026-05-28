from sqlmodel import SQLModel, create_engine, Session

from typing import Generator

from dotenv import load_dotenv
import os

load_dotenv()

database_name = os.getenv('DB_NAME', 'database.db')
database_url = f"sqlite:///./{database_name}"
engine = create_engine(database_url, echo=True)

def init_db():
    # Create database tables from models if they do not exist
    import models
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session