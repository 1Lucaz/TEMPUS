from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, field_serializer
from app.modules.utils.status import Status

class OrdemBase(BaseModel):
    id: int
    cliente_id: int
    data_abertura: datetime
    status: Status
    ativo: bool

    @field_serializer("data_abertura")
    def serialize_data_abertura(self, value: datetime):
        return value.date()

class OrdemCreate(BaseModel):
    cliente_id: int
    data_abertura: date = date.today()
    status: Status = Status.ABERTA
    ativo: bool = True

class OrdemUpdate(BaseModel):
    cliente_id: Optional[int] = Field(default=None)
    data_abertura: Optional[date] = Field(default=None)
    status: Optional[Status] = Field(default=None)
    ativo: Optional[bool] = Field(default=None)
