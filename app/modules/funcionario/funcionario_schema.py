from pydantic import BaseModel, EmailStr

class FuncionarioCreate(BaseModel):
    nome: str
    email: EmailStr
    cargo: str
    ativo: bool = True
    senha: str
    is_admin: bool
    is_colaborador: bool

    access_cliente: bool
    access_funcionario: bool
    access_servico: bool
    access_item_servico: bool
    access_ordem_servico: bool


    model_config = {"from_attributes": True}

class FuncionarioUpdate(BaseModel):
    novo_nome: str | None = None
    novo_cargo: str | None = None
    novo_email: EmailStr | None = None
    ativo: bool | None = None
    is_admin: bool | None = None
    is_colaborador: bool | None = None

    access_cliente: bool | None = None
    access_funcionario: bool | None = None
    access_servico: bool | None = None
    access_item_servico: bool | None = None
    access_ordem_servico: bool | None = None

    model_config = {"from_attributes": True}

class FuncionarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    cargo: str
    ativo: bool
    is_colaborador: bool
    is_admin: bool

    access_cliente: bool
    access_funcionario: bool
    access_servico: bool
    access_item_servico: bool
    access_ordem_servico: bool

    model_config = {"from_attributes": True}

class FuncionarioInput (BaseModel):
        id: int | None = None
        nome: str | None = None
        email: EmailStr | None = None

        cargo: str | None = None
        ativo: bool | None = None

        is_admin: bool | None = None
        is_colaborador: bool | None = None

        access_cliente: bool | None = None
        access_funcionario: bool | None = None
        access_servico: bool | None = None
        access_item_servico: bool | None = None
        access_ordem_servico: bool | None = None

        model_config = {"from_attributes": True}
