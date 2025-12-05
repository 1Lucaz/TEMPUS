from pydantic import BaseModel, Field
from typing import Optional

class ServicoBase(BaseModel):
    id: int
    descricao: str
    valor_base: float
    ativo: bool

class ServicoCreate(BaseModel):
    descricao: str
    valor_base: float
    ativo: bool = True

class ServicoUpdate(BaseModel):
    descricao: Optional[str] = Field(default=None)
    valor_base: Optional[float] = Field(default=None)
    ativo : Optional [bool] =  Field(default=None)
