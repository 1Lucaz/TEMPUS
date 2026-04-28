from datetime import datetime

from pydantic import BaseModel

class CategoriaResponse(BaseModel):
    id: int
    descricao: str
    ativo: bool
    created_at: datetime
    updated_at: datetime | None
    
    model_config = {"from_attributes": True}


class CategoriaCreate(BaseModel):
    id: int
    descricao: str  | None = None
    ativo: bool = True 

    model_config = {"from_attributes": True}
    
    
   

class CategoriaUpdate(BaseModel):
    descricao: str | None = None
    ativo: bool | None = None

    model_config = {"from_attributes": True}
    


