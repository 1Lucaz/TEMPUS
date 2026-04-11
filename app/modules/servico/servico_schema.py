from pydantic import BaseModel

class ServicoResponse(BaseModel):
    id: int
    descricao: str
    valor_base: float
    ativo: bool

class ServicoCreate(BaseModel):
    descricao: str
    valor_base: float
    ativo: bool = True

class ServicoUpdate(BaseModel):
    descricao: str | None = None
    valor_base: float | None = None
    ativo : bool | None = None

class ServicoInput(BaseModel):
    id: int | None = None
    descricao: str | None = None
    valor_base: float | None = None
    ativo: bool | None = None
