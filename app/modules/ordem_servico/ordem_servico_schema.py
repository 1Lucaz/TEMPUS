from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel
from app.modules.utils.status import Status

class OrdemBase(BaseModel):
    id: int
    cliente_id: int
    data_abertura: datetime
    status: Status

class OrdemCreate(BaseModel):
    cliente_id: int
    data_abertura: datetime = date.today()
    status: Status = Status.ABERTA

class OrdemUpdate(BaseModel):
    cliente_id: Optional [int] = None
    data_abertura: Optional[datetime] = None
    status: Optional[Status] = None


