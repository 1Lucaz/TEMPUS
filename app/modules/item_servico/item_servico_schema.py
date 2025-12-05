from pydantic import BaseModel, Field
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
    ordem_servico_id: Optional[int] = Field(default=None)
    servico_id: Optional[int] = Field(default=None)
    valor: Optional[float] = Field(default=None)
    ativo: Optional[bool] = Field(default=None)
