from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.schemas.item_servico_schema import ItemCreate, ItemResponse
from app.services.item_servico_service import ItemServicoService

router = APIRouter(prefix="/itens", tags=["Itens"])

@router.post("/", response_model=ItemResponse)
def criar_item(data: ItemCreate, ordem_servico_id: int | None = None, db: Session = Depends(get_session)):
    try:
        if ordem_servico_id:
            return ItemServicoService.criar(ordem_servico_id, data, db)
        raise HTTPException(status_code=400, detail="ordem_servico_id required when posting to /itens/")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ItemResponse])
def listar_itens(ordem_servico_id: int | None = None, ativo: bool | None = None, db: Session = Depends(get_session)):
    return ItemServicoService.listar(db, ativo, ordem_servico_id)

@router.get("/{id}", response_model=ItemResponse)
def obter_item(id: int, db: Session = Depends(get_session)):
    item = ItemServicoService.buscar_por_id(id, db)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item

@router.put("/{id}", response_model=ItemResponse)
def atualizar_item(id: int, data: ItemCreate, db: Session = Depends(get_session)):
    item = ItemServicoService.atualizar(id, data.valor, db)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item

@router.post("/{id}/desativar")
def desativar_item(id: int, db: Session = Depends(get_session)):
    item = ItemServicoService.desativar(id, db)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return {"id": item.id, "ativo": item.ativo}
