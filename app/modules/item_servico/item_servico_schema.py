from pydantic import BaseModel

class ItemResponse(BaseModel):
    id: int
    servico_id: int
    categoria_id: int
    valor: float
    ativo: bool

    model_config = {"from_attributes": True}


class ItemCreate(BaseModel):
    id: int
    servico_id: int
    categoria_id: int
    valor: float
    ativo: bool = True

    model_config = {"from_attributes": True}


class ItemUpdate(BaseModel):
    servico_id: int | None = None
    categoria_id: int | None = None
    valor: float | None = None
    ativo: bool | None = None

    model_config = {"from_attributes": True}


class ItemInput(BaseModel):
    id: int | None = None
    servico_id: int | None = None
    categoria_id: int | None = None
    valor: float | None = None
    ativo: bool | None = None

    model_config = {"from_attributes": True}
