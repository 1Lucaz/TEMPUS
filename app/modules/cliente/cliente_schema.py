from pydantic import BaseModel, EmailStr

class ClienteCreate(BaseModel):
    nome: str
    email: EmailStr
    telefone: str | None = None
    senha: str

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

    model_config = {"from_attributes": True}

class ClienteInput(BaseModel):
    nome: str | None = None
    email: str | None = None
    telefone: str | None = None
    ativo: bool | None = None

    model_config = {"from_attributes": True}