from pydantic import BaseModel
from app.modules.categoria.categoria_schema import CategoriaCreate, CategoriaUpdate, CategoriaResponse, CategoriaInput


class ItemResponse(BaseModel):
    id: int
    categoria_id: int
    descricao: str
    valor: float
    ativo: bool
    categoria_servico: CategoriaResponse | None = None

    model_config = {"from_attributes": True}


class ItemCreate(BaseModel):
    categoria_id: int
    descricao: str | None = None
    valor: float
    ativo: bool = True
    categoria_servico: CategoriaCreate | None = None

    model_config = {"from_attributes": True}


class ItemUpdate(BaseModel):
    categoria_id: int | None = None
    descricao: str | None = None
    valor: float | None = None
    ativo: bool | None = None
    categoria_servico: CategoriaUpdate | None = None

    model_config = {"from_attributes": True}


class ItemInput(BaseModel):
    id: int | None = None
    descricao: str | None = None
    categoria_id: int | None = None
    valor: float | None = None
    ativo: bool | None = None
    categoria_servico: CategoriaInput | None = None

    model_config = {"from_attributes": True}
