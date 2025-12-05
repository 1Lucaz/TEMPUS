from pydantic import BaseModel, Field
from typing import Optional

class FuncionarioBase(BaseModel):
    id: int
    nome: str
    cargo: str
    ativo: bool

class FuncionarioCreate(BaseModel):
    nome: str
    cargo: str
    ativo: bool = True

class FuncionarioUpdate(BaseModel):
    nome: Optional[str] = Field(default=None)
    cargo: Optional[str] = Field(default=None)
    ativo: Optional[bool] = Field(default=None)
