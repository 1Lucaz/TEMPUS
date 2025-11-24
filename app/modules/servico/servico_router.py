from fastapi import APIRouter, status
from typing import List, Optional

from TEMPUS.app.modules.utils.exceptions import tratar_exception
from servico_schema import ServicoCreate, ServicoUpdate, ServicoBase
from servico_service import ServicoService

router = APIRouter(prefix="/servicos", tags=["Serviços"])

@router.get("/", response_model=List[ServicoBase])
def listar_servicos(ativo: Optional[bool] = None, descricao: Optional[str] = None):
    return ServicoService.listar(ativo=ativo, descricao=descricao)

@router.post("/", response_model=ServicoBase, status_code=status.HTTP_201_CREATED)
def criar_servico(servico: ServicoCreate):
    try:
        return ServicoService.criar_servico(servico)
    except Exception as e:
        tratar_exception(e)

@router.get("/{id}", response_model=ServicoBase)
def buscar_servico(id: int):
    servico = ServicoService.buscar_por_id(id)
    if not servico:
        tratar_exception(ValueError("SERVIÇO NÃO ENCONTRADO"))
    return servico

@router.put("/{id}", response_model=ServicoBase)
def atualizar_servico(id: int, dados: ServicoUpdate):
    try:
        return ServicoService.atualizar(id, dados)
    except Exception as e:
        tratar_exception(e)

@router.post("/{id}/desativar", response_model=ServicoBase)
def desativar_servico(id: int):
    try:
        return ServicoService.desativar(id)
    except Exception as e:
        tratar_exception(e)