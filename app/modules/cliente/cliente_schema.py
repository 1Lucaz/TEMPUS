from pydantic import BaseModel, EmailStr
from typing import Optional

class ClienteBase(BaseModel):
    id: int
    nome: str
    telefone: str
    email: Optional[EmailStr] = None
    ativo: bool

class ClienteCreate(ClienteBase):
    nome: str
    telefone: str
    email: Optional[EmailStr]
    ativo: bool = True

class ClienteUpdate(ClienteCreate):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    ativo: Optional[bool] = None
