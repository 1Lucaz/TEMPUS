from pydantic import BaseModel, EmailStr

class FuncionarioCreate(BaseModel):
    nome: str
    email: EmailStr
    cargo: str
    ativo: bool = True
    senha: str
    is_admin: bool
    is_colaborador: bool

    model_config = {"from_attributes": True}

class FuncionarioUpdate(BaseModel):
    novo_nome: str | None = None
    novo_cargo: str | None = None
    novo_email: EmailStr | None = None
    ativo: bool | None = None
    is_admin: bool | None = None
    is_colaborador: bool | None = None

    model_config = {"from_attributes": True}

class FuncionarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    cargo: str
    ativo: bool
    is_colaborador: bool
    is_admin: bool

    model_config = {"from_attributes": True}
