from pydantic import BaseModel
from typing import Optional

class FuncionarioBase(BaseModel):
    id: int
    nome: str
    cargo: str
    ativo: bool

class FuncionarioCreate(BaseModel):
    nome: str
    cargo: str
    ativo: bool

class FuncionarioUpdate(BaseModel):
    nome: Optional[str] = None
    cargo: Optional[str] = None
    ativo: Optional [bool] = None
