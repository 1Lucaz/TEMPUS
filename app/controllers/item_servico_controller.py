from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.item_servico_schema import ItemCreate, ItemUpdate, ItemResponse
from app.services.item_servico_service import ItemServicoService
from app.core.database import get_session

router = APIRouter(prefix="/itens", tags=["Itens"])

# POST /itens
@router.post("/", response_model=ItemResponse)
def criar_item(data: ItemCreate, db: Session = Depends(get_session)):
    return ItemServicoService.criar(data, db)

# GET /itens
@router.get("/", response_model=list[ItemResponse])
def listar_itens(ordem_servico_id: int | None = None, ativo: bool | None = None, db: Session = Depends(get_session)):
    return ItemServicoService.listar(db, ativo, ordem_servico_id)

# GET /itens/{id}
@router.get("/{id}", response_model=ItemResponse)
def obter_item(id: int, db: Session = Depends(get_session)):
    item = ItemServicoService.buscar_por_id(id, db)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item

# PUT /itens/{id}
@router.put("/{id}", response_model=ItemResponse)
def atualizar_item(id: int, data: ItemUpdate, db: Session = Depends(get_session)):
    item = ItemServicoService.atualizar(id, data.valor, db)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item

# POST /itens/{id}/desativar
@router.post("/{id}/desativar", response_model=ItemResponse)
def desativar_item(id: int, db: Session = Depends(get_session)):
    item = ItemServicoService.desativar(id, db)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item
