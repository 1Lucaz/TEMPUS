from pydantic import BaseModel, EmailStr

class ClienteCreate(BaseModel):
    nome: str
    email: EmailStr
    telefone: str | None = None
    senha: str
    ativo: bool = True

    model_config = {"from_attributes": True}

class ClienteUpdate(BaseModel):
    novo_nome: str | None = None
    novo_email: str | None = None
    novo_telefone: str | None
    nova_senha: str | None = None
    ativo: bool | None = None

    model_config = {"from_attributes": True}

class ClienteResponse(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str
    ativo: bool
    updated_by: str | None = None

    model_config = {"from_attributes": True}

class ClienteRequest(BaseModel):
    id: int | None = None
    nome: str | None = None
    email: str | None = None
    telefone: str | None = None
    ativo: bool | None = None

    model_config = {"from_attributes": True}