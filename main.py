from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import select

from database import get_session, init_db, Session
from models import Record, RecordCreateUpdate, RecordPatch

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
def create_record(record_data: RecordCreateUpdate, session: Session = Depends(get_session)):
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

@app.get("/records/{record_id}", response_model=Record, status_code=status.HTTP_200_OK)
def read_record(record_id: int, session: Session = Depends(get_session)):
    record = session.get(Record, record_id)

    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Record with ID {record_id} not found")
    
    return record

@app.put("/records/{record_id}", response_model=Record, status_code=status.HTTP_200_OK)
def update_record(record_data: RecordCreateUpdate, record_id: int, session: Session = Depends(get_session)):
    record = session.get(Record, record_id)

    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Record with ID {record_id} not found")
    
    logger.info(f"Beginning strict validation and parsing to update record {record.model_dump()} into payload {record_data.model_dump()}")

    try:
        update_data = record_data.model_dump() # return a dictionary representation of the model
        record.sqlmodel_update(update_data) # update the fields from update_record into record
        session.add(record)
        session.commit()
        session.refresh(record)
        return record
    except Exception as e:
        logger.error(f"Failed to update record to database: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal database storage error")
    
@app.patch("/records/{record_id}", response_model=Record, status_code=status.HTTP_200_OK)
def patch_record(record_data: RecordPatch, record_id: int, session: Session = Depends(get_session)):
    record = session.get(Record, record_id)

    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Record with ID {record_id} not found")
    
    logger.info(f"Beginning validation and parsing to update record {record.model_dump()} into payload {record_data.model_dump()}")

    try:
        update_data = record_data.model_dump(exclude_unset=True) # return a dictionary representation of the model
        record.sqlmodel_update(update_data) # update the fields from update_record into record
        session.add(record)
        session.commit()
        session.refresh(record)
        return record
    except Exception as e:
        logger.error(f"Failed to update record to database: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal database storage error")
    
@app.delete("/records/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(record_id: int, session: Session = Depends(get_session)):
    record = session.get(Record, record_id)

    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Record with ID {record_id} not found")
    
    session.delete(record) # Prepare the Record instance to be deleted in the database
    session.commit()
    
    logger.info(f"Record {record.model_dump()} deleted")

    return None