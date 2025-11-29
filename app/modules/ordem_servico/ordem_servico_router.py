from fastapi import APIRouter, status
from typing import List, Optional
from datetime import date
from .ordem_servico_schema import OrdemCreate, OrdemUpdate, OrdemBase
from .ordem_servico_service import OrdemServicoService
from TEMPUS.app.modules.utils.exceptions import tratar_exception

router = APIRouter(prefix="/ordens", tags=["Ordens de Serviço"])

@router.get("/", response_model=List[OrdemBase])
def listar_ordens(
    ativo: Optional[bool] = None,
    status_os: Optional[str] = None,
    cliente_id: Optional[int] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None
):
    return OrdemServicoService.listar(
        ativo=ativo,
        status=status_os,
        cliente_id=cliente_id,
        data_inicio=data_inicio,
        data_fim=data_fim
    )

@router.post("/", response_model=OrdemBase, status_code=status.HTTP_201_CREATED)
def criar_ordem(ordem: OrdemCreate):
    try:
        return OrdemServicoService.criar(ordem)
    except Exception as e:
        tratar_exception(e)

@router.get("/{id}", response_model=OrdemBase)
def buscar_ordem(id: int):
    ordem = OrdemServicoService.buscar_por_id(id)
    if not ordem:
        tratar_exception(ValueError("ORDEM NÃO ENCONTRADA"))
    return ordem

@router.put("/{id}", response_model=OrdemBase)
def atualizar_ordem(id: int, dados: OrdemUpdate):
    try:
        return OrdemServicoService.atualizar(id, dados)
    except Exception as e:
        tratar_exception(e)

@router.post("/{id}/desativar", response_model=OrdemBase)
def desativar_ordem(id: int):
    try:
        return OrdemServicoService.desativar(id)
    except Exception as e:
        tratar_exception(e)