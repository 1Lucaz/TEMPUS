from datetime import date, datetime

from pydantic import BaseModel, field_serializer

from app.modules.utils.prioridade import Prioridade
from app.modules.utils.status import Status


class OrdemResponse(BaseModel):
    id: int
    cliente_id: int
    data_abertura: datetime
    status: Status
    ativo: bool
    prioridade: Prioridade

    model_config = {"from_attributes": True}

    @field_serializer("data_abertura")
    def serialize_data_abertura(self, value: datetime):
        return value.date()


class OrdemCreate(BaseModel):
    cliente_id: int
    data_abertura: date = date.today()
    status: Status = Status.ABERTA
    ativo: bool = True
    prioridade: Prioridade

    model_config = {"from_attributes": True}


class OrdemUpdate(BaseModel):
    cliente_id: int | None = None
    data_abertura: date | None = None
    status: Status | None = None
    ativo: bool | None = None
    prioridade: Prioridade | None = None

    model_config = {"from_attributes": True}


class OrdemInput(BaseModel):
    id: int | None = None
    cliente_id: int | None = None
    status: Status | None = None
    ativo: bool | None = None
    data_inicio: date | None = None
    data_fim: date | None = None
    prioridade: Prioridade | None = None

    model_config = {"from_attributes": True}