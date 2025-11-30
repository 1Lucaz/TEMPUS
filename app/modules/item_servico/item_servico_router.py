from fastapi import APIRouter, status
from typing import List, Optional
from app.modules.item_servico.item_servico_schema import ItemCreate, ItemUpdate, ItemBase
from app.modules.item_servico.item_servico_service import ItemService
from app.modules.utils.exceptions import tratar_exception

router = APIRouter(prefix="/itens", tags=["Itens de Serviço"])

@router.get("/", response_model=List[ItemBase])
def listar_itens(ativo: Optional[bool] = None, ordem_servico_id: Optional[int] = None):
    return ItemService.listar(ativo=ativo, ordem_servico_id=ordem_servico_id)

@router.post("/", response_model=ItemBase, status_code=status.HTTP_201_CREATED)
def criar_item(item: ItemCreate):
    try:
        return ItemService.criar_item(item)
    except Exception as e:
        tratar_exception(e)

@router.get("/{id}", response_model=ItemBase)
def buscar_item(id: int):
    item = ItemService.buscar_por_id(id)
    if not item:
        tratar_exception(ValueError("ITEM NÃO ENCONTRADO"))
    return item

@router.put("/{id}", response_model=ItemBase)
def atualizar_item(id: int, dados: ItemUpdate):
    try:
        return ItemService.atualizar(id, dados)
    except Exception as e:
        tratar_exception(e)

@router.post("/{id}/desativar", response_model=ItemBase)
def desativar_item(id: int):
    try:
        return ItemService.desativar(id)
    except Exception as e:
        tratar_exception(e)