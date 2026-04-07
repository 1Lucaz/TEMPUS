from pydantic import BaseModel

class ItemBase(BaseModel):
    id: int
    ordem_servico_id: int
    servico_id: int
    valor: float
    ativo: bool

    model_config = {"from_attributes": True}


class ItemCreate(BaseModel):
    ordem_servico_id: int
    servico_id: int
    valor: float
    ativo: bool = True

    model_config = {"from_attributes": True}


class ItemUpdate(BaseModel):
    ordem_servico_id: int | None = None
    servico_id: int | None = None
    valor: float | None = None
    ativo: bool | None = None

    model_config = {"from_attributes": True}


class ItemInput(BaseModel):
    id: int | None = None
    ordem_servico_id: int | None = None
    servico_id: int | None = None
    valor: float | None = None
    ativo: bool | None = None

    model_config = {"from_attributes": True}
