from pydantic import BaseModel, EmailStr
from typing import Optional

class ClienteBase(BaseModel):
    nome: str
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None

class ClienteResponse(ClienteBase):
    id: int
    ativo: bool = True
    model_config = { "from_attributes": True }
