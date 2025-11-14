from pydantic import BaseModel
from typing import Optional

class FuncionarioBase(BaseModel):
    nome: str
    cargo: Optional[str] = None

class FuncionarioCreate(FuncionarioBase):
    pass

class FuncionarioUpdate(BaseModel):
    nome: Optional[str] = None
    cargo: Optional[str] = None

class FuncionarioResponse(FuncionarioBase):
    id: int
    ativo: bool = True
    model_config = { "from_attributes": True }
