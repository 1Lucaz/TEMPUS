from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ClienteBase(BaseModel):
    id: int
    nome: str
    telefone: str
    email: EmailStr
    ativo: bool

class ClienteCreate(BaseModel):
    nome: str = Field(...)
    telefone: str = Field(...)
    email: EmailStr = Field(...)
    ativo: bool = Field(default=True)

class ClienteUpdate(BaseModel):
    nome: Optional[str] = Field(default=None)
    telefone: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    ativo: Optional[bool] = Field(default=None)
