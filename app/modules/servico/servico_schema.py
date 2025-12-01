from pydantic import BaseModel
from typing import Optional

class ServicoBase(BaseModel):
    id: int
    descricao: str
    valor_base: float

class ServicoCreate(BaseModel):
    descricao: str
    valor_base: float

class ServicoUpdate(BaseModel):
    descricao: Optional[str] = None
    valor_base: Optional[float] = None