from typing import Optional
from pydantic import BaseModel
from datetime import date
from TEMPUS.app.modules.utils.status import Status

class OrdemBase(BaseModel):
    id: int
    cliente_id: int
    data_abertura: str
    status: Status

class OrdemCreate(OrdemBase):
    cliente_id: int
    data_abertura: str = date.today().fromisoformat()
    status: Status = Status.ABERTA

class OrdemUpdate(OrdemCreate):
    cliente_id: Optional [int] = None
    data_abertura: Optional[str] = None
    status: Optional[Status] = None


