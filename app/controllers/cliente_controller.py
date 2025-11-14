from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.schemas.cliente_schema import ClienteCreate, ClienteUpdate, ClienteResponse
from app.services.cliente_service import ClienteService

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=ClienteResponse)
def criar_cliente(data: ClienteCreate, db: Session = Depends(get_session)):
    try:
        return ClienteService.criar(data, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ClienteResponse])
def listar_clientes(ativo: bool | None = None, nome: str | None = None, db: Session = Depends(get_session)):
    return ClienteService.listar(db, ativo, nome)

@router.get("/{id}", response_model=ClienteResponse)
def obter_cliente(id: int, db: Session = Depends(get_session)):
    cliente = ClienteService.buscar_por_id(id, db)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@router.put("/{id}", response_model=ClienteResponse)
def atualizar_cliente(id: int, data: ClienteUpdate, db: Session = Depends(get_session)):
    cliente = ClienteService.atualizar(id, data, db)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@router.post("/{id}/desativar")
def desativar_cliente(id: int, db: Session = Depends(get_session)):
    cliente = ClienteService.desativar(id, db)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return { "id": cliente.id, "ativo": cliente.ativo }
