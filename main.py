from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import select

from database import get_session, init_db, Session
from models import Record

from contextlib import asynccontextmanager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs on application startup
    logger.info("Database and Tables: Initialize")
    init_db()
    logger.info("Database and Tables: Success")
    yield


app = FastAPI(lifespan=lifespan)

@app.post("/records/", response_model=Record, status_code=status.HTTP_201_CREATED)
def create_record(record_data: Record, session: Session = Depends(get_session)):
    logger.info(f"Beginning validation and parsing for payload: {record_data.model_dump()}")

    try:
        db_record = Record.model_validate(record_data) # validates the data from the user based on Record from models.
        session.add(db_record) # Prepare the Record instance to be stored in the database
        session.commit() # Process the Record instance added and flush the session
        session.refresh(db_record) # Refetch the data based on db_record to get the latest data from the database
        return db_record
    except Exception as e:
        logger.error(f"Failed to store record to database: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal database storage error")
    
@app.get("/records/", response_model=list[Record], status_code=status.HTTP_200_OK)
def read_records(session: Session = Depends(get_session)):
    statement = select(Record)
    records = session.exec(statement).all()
    return records