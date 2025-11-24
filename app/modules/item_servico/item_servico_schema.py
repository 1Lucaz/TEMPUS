from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    id: int
    ordem_servico_id: int
    servico_id: int
    valor: float
    ativo: bool

class ItemCreate(BaseModel):
    ordem_servico_id: int
    servico_id: int
    valor: float
    ativo: bool = True

class ItemUpdate(BaseModel):
    valor: Optional[float] = None
    ordem_servico_id: Optional[int] = None
    servico_id: Optional[int] = None
    ativo: Optional[bool] = None



