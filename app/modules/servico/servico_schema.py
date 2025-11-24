from pydantic import BaseModel
from typing import Optional

class ServicoBase(BaseModel):
    id: int
    descricao: str
    valor_base: float

class ServicoCreate(ServicoBase):
    descricao: str
    valor_base: float

class ServicoUpdate(ServicoCreate):
    descricao: Optional[str] = None
    valor_base: Optional[float] = None