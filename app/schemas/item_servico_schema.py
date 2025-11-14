from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    ordem_servico_id: int
    servico_id: int
    valor: float

class ItemCreate(BaseModel):
    servico_id: int
    valor: float

class ItemResponse(ItemBase):
    id: int
    ativo: bool = True
    model_config = { "from_attributes": True }
