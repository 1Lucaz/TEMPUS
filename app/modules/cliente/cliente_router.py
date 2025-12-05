from fastapi import APIRouter, status, Body
from typing import List, Optional

from app.modules.utils.exceptions import tratar_exception
from app.modules.cliente.cliente_schema import ClienteCreate, ClienteUpdate, ClienteBase
from app.modules.cliente.cliente_service import ClienteService

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("/", response_model=List[ClienteBase])
def listar_clientes(ativo: Optional[bool] = None, nome: Optional[str] = None):
    return ClienteService.listar(ativo=ativo, nome=nome)


@router.post("/", response_model=ClienteBase, status_code=status.HTTP_201_CREATED)
def criar_cliente(cliente: ClienteCreate = Body(...)):
    try:
        return ClienteService.criar_cliente(cliente)
    except Exception as e:
        tratar_exception(e)


@router.get("/{id}", response_model=ClienteBase)
def buscar_cliente(id: int):
    cliente = ClienteService.buscar_por_id(id)
    if not cliente:
        tratar_exception(ValueError("CLIENTE NÃO ENCONTRADO"))
    return cliente


@router.put("/{id}", response_model=ClienteBase)
def atualizar_cliente(
    id: int,
    dados: ClienteUpdate = Body(..., example={})
):
    try:
        return ClienteService.atualizar(id, dados)
    except Exception as e:
        tratar_exception(e)


@router.post("/{id}/desativar", response_model=ClienteBase)
def desativar_cliente(id: int):
    try:
        return ClienteService.desativar(id)
    except Exception as e:
        tratar_exception(e)
