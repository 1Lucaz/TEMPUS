from pydantic import BaseModel

class CategoriaServicoResponse(BaseModel):
    id: int
    descricao: str
    ativo: bool
    model_config = {"from_attributes": True}


class CategoriaServicoCreate(BaseModel):
    id: int
    descricao: str
    ativo: bool = True

    model_config = {"from_attributes": True}
    