from pydantic import BaseModel
from typing import Optional

class ServicoBase(BaseModel):
    descricao: str
    valor_base: float

class ServicoCreate(ServicoBase):
    pass

class ServicoUpdate(BaseModel):
    descricao: Optional[str] = None
    valor_base: Optional[float] = None

class ServicoResponse(ServicoBase):
    id: int
    ativo: bool = True
    model_config = { "from_attributes": True }
