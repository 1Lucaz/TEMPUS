from pydantic import BaseModel
from typing import Optional

class OrdemBase(BaseModel):
    cliente_id: int
    data_abertura: Optional[str] = None
    status: Optional[str] = "aberta"

class OrdemCreate(OrdemBase):
    pass

class OrdemUpdate(BaseModel):
    status: str

class OrdemResponse(OrdemBase):
    id: int
    ativo: bool = True
    model_config = { "from_attributes": True }
