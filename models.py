from sqlmodel import Field, SQLModel

from decimal import Decimal

class RecordBase(SQLModel):
    name: str
    latitude: Decimal = Field(max_digits=9, decimal_places=6)
    longitude: Decimal = Field(max_digits=9, decimal_places=6)

class RecordCreateUpdate(RecordBase):
    pass

class Record(RecordBase, table=True):
    id: int | None = Field(default=None, primary_key=True)