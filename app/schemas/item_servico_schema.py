from pydantic import BaseModel

class ItemCreate(BaseModel):
    ordem_servico_id: int
    servico_id: int
    valor: float

class ItemUpdate(BaseModel):
    valor: float

class ItemResponse(BaseModel):
    id: int
    ordem_servico_id: int
    servico_id: int
    valor: float
    ativo: bool = True

    class Config:
        orm_mode = True
