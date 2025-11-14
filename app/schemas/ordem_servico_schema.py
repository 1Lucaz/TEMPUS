from pydantic import BaseModel
from typing import Optional
from datetime import date

class OrdemBase(BaseModel):
    cliente_id: int
    data_abertura: date
    status: str = "aberta"

class OrdemCreate(OrdemBase):
    pass

class OrdemUpdate(BaseModel):
    cliente_id: Optional[int] = None
    status: Optional[str] = None

class OrdemResponse(OrdemBase):
    id: int
    ativo: bool = True
    funcionario_id: Optional[int] = None
    model_config = { "from_attributes": True }
